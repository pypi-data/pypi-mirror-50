import time

from autolens.data.array.util import binning_util
from autolens.data.array import grids
from autolens.data.array import mask as msk
from autolens.model.galaxy import galaxy as g
from autolens.model.profiles import light_profiles as lp
from autolens.model.profiles import mass_profiles as mp
from autolens.lens import lens_data as ld
from autolens.lens import ray_tracing
from autolens.lens import lens_fit
from autolens.model.inversion import pixelizations as pix
from autolens.model.inversion import regularization as reg
from autolens.model.inversion.util import inversion_util
from autolens.model.inversion.util import regularization_util

from test.simulation import simulation_util

import numpy as np

repeats = 1

print("Number of repeats = " + str(repeats))
print()

sub_grid_size = 2
radius_arcsec = 2.5
psf_shape = (11, 11)
cluster_pixel_scale = 0.1
pixelization_pixels = 800

print("sub grid size = " + str(sub_grid_size))
print("circular mask radius = " + str(radius_arcsec) + "\n")
print("psf shape = " + str(psf_shape) + "\n")
print("Cluster Pixel Scale = " + str(cluster_pixel_scale) + "\n")
print("pixelization pixels = " + str(pixelization_pixels) + "\n")

lens_galaxy = g.Galaxy(
    redshift=0.5,
    mass=mp.EllipticalIsothermal(
        centre=(0.0, 0.0), einstein_radius=1.6, axis_ratio=0.7, phi=45.0
    ),
)

pixelization = pix.VoronoiBrightnessImage(
    pixels=pixelization_pixels, weight_floor=0.0, weight_power=5.0
)

source_galaxy = g.Galaxy(
    redshift=1.0,
    pixelization=pixelization,
    regularization=reg.Constant(coefficient=1.0),
)

for data_resolution in ["Euclid", "HST", "HST_Up", "AO"]:

    ccd_data = simulation_util.load_test_ccd_data(
        data_type="no_lens_light_and_source_smooth",
        data_resolution=data_resolution,
        psf_shape=psf_shape,
    )
    mask = msk.Mask.circular(
        shape=ccd_data.shape,
        pixel_scale=ccd_data.pixel_scale,
        radius_arcsec=radius_arcsec,
    )
    lens_data = ld.LensData(
        ccd_data=ccd_data,
        mask=mask,
        sub_grid_size=sub_grid_size,
        cluster_pixel_scale=cluster_pixel_scale,
    )

    source_galaxy = g.Galaxy(
        redshift=1.0,
        light=lp.EllipticalSersic(
            centre=(0.0, 0.0),
            axis_ratio=0.8,
            phi=60.0,
            intensity=0.4,
            effective_radius=0.5,
            sersic_index=1.0,
        ),
    )

    hyper_image = source_galaxy.intensities_from_grid(grid=lens_data.grid_stack.regular)
    hyper_image_2d = lens_data.grid_stack.regular.scaled_array_2d_from_array_1d(
        array_1d=hyper_image
    )

    hyper_image_2d_binned = binning_util.binned_up_array_2d_using_mean_from_array_2d_and_bin_up_factor(
        array_2d=hyper_image_2d, bin_up_factor=lens_data.cluster.bin_up_factor
    )

    hyper_image_1d_binned = lens_data.cluster.mask.array_1d_from_array_2d(
        array_2d=hyper_image_2d_binned
    )

    source_galaxy = g.Galaxy(
        redshift=1.0,
        pixelization=pixelization,
        regularization=reg.Constant(coefficient=1.0),
    )

    print(
        "VoronoiBrightnessImage Inversion fit run times for image type "
        + data_resolution
        + "\n"
    )
    print("Number of points = " + str(lens_data.grid_stack.sub.shape[0]) + "\n")

    start_overall = time.time()

    start = time.time()
    for i in range(repeats):
        cluster_weight_map = pixelization.cluster_weight_map_from_hyper_image(
            hyper_image=hyper_image_1d_binned
        )
    diff = time.time() - start
    print("Time to Setup Cluster Weight Map = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        sparse_to_regular_grid = grids.SparseToRegularGrid.from_total_pixels_cluster_grid_and_cluster_weight_map(
            total_pixels=pixelization.pixels,
            regular_grid=lens_data.grid_stack.regular,
            cluster_grid=lens_data.cluster,
            cluster_weight_map=cluster_weight_map,
        )

        pixelization_grid = grids.PixelizationGrid(
            arr=sparse_to_regular_grid.sparse,
            regular_to_pixelization=sparse_to_regular_grid.regular_to_sparse,
        )

        image_plane_grid_stack = lens_data.grid_stack.new_grid_stack_with_grids_added(
            pixelization=pixelization_grid
        )

    diff = time.time() - start
    print("Time to Setup Pixelization Grid = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        tracer = ray_tracing.Tracer(
            galaxies=[lens_galaxy, source_galaxy],
            image_plane_grid_stack=image_plane_grid_stack,
        )
    diff = time.time() - start
    print("Time to Setup Tracer = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        relocated_grid_stack = lens_data.border.relocated_grid_stack_from_grid_stack(
            tracer.source_plane.grid_stack
        )
    diff = time.time() - start
    print("Time to perform border relocation = {}".format(diff / repeats))

    pixel_centres = relocated_grid_stack.pixelization
    pixels = pixel_centres.shape[0]

    start = time.time()
    for i in range(repeats):
        voronoi = pixelization.voronoi_from_pixel_centers(pixel_centers=pixel_centres)
    diff = time.time() - start
    print("Time to create Voronoi grid = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        pixel_neighbors, pixel_neighbors_size = pixelization.neighbors_from_pixelization(
            pixels=pixels, ridge_points=voronoi.ridge_points
        )
    diff = time.time() - start
    print("Time to compute pixel neighbors = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        pixelization.geometry_from_grid(
            grid=relocated_grid_stack.sub,
            pixel_centres=pixel_centres,
            pixel_neighbors=pixel_neighbors,
            pixel_neighbors_size=pixel_neighbors_size,
        )
    diff = time.time() - start
    print("Time to compute geometry of pixelization = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        adaptive_mapper = pixelization.mapper_from_grid_stack_and_border(
            grid_stack=tracer.source_plane.grid_stack, border=lens_data.border
        )
    diff = time.time() - start
    print("Time to create mapper = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        mapping_matrix = adaptive_mapper.mapping_matrix
    diff = time.time() - start
    print("Time to compute mapping matrix = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        blurred_mapping_matrix = lens_data.convolver_mapping_matrix.convolve_mapping_matrix(
            mapping_matrix=mapping_matrix
        )
    diff = time.time() - start
    print("Time to compute blurred mapping matrix = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        data_vector = inversion_util.data_vector_from_blurred_mapping_matrix_and_data(
            blurred_mapping_matrix=blurred_mapping_matrix,
            image_1d=lens_data.image_1d,
            noise_map_1d=lens_data.noise_map_1d,
        )
    diff = time.time() - start
    print("Time to compute data vector = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        curvature_matrix = inversion_util.curvature_matrix_from_blurred_mapping_matrix(
            blurred_mapping_matrix=blurred_mapping_matrix,
            noise_map_1d=lens_data.noise_map_1d,
        )
    diff = time.time() - start
    print("Time to compute curvature matrix = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        regularization_matrix = regularization_util.constant_regularization_matrix_from_pixel_neighbors(
            coefficient=1.0,
            pixel_neighbors=adaptive_mapper.geometry.pixel_neighbors,
            pixel_neighbors_size=pixel_neighbors_size,
        )
    diff = time.time() - start
    print("Time to compute reguarization matrix = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        curvature_reg_matrix = np.add(curvature_matrix, regularization_matrix)
    diff = time.time() - start
    print("Time to compute curvature reguarization Matrix = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        solution_vector = np.linalg.solve(curvature_reg_matrix, data_vector)
    diff = time.time() - start
    print("Time to compute solution vector = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        inversion_util.reconstructed_data_vector_from_blurred_mapping_matrix_and_solution_vector(
            blurred_mapping_matrix=blurred_mapping_matrix,
            solution_vector=solution_vector,
        )
    diff = time.time() - start
    print("Time to compute reconstructed data vector = {}".format(diff / repeats))

    start = time.time()
    for i in range(repeats):
        lens_fit.LensInversionFit(lens_data=lens_data, tracer=tracer)
    diff = time.time() - start
    print("Time to perform complete fit = {}".format(diff / repeats))

    print()
