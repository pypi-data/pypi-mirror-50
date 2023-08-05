import autofit as af
from autocti.data import mask as msk
from autocti.pipeline import pipeline as pl
from autocti.pipeline import phase as ph
from autocti.model import arctic_params

# In this pipeline, we'll perform an analysis which fits two parallel trap species to a set of charge
# injection imaging data. This will include a hyper-phase which scales the noise in the analysis, to prevent
# over-fitting the highest S/N charge injection images. The pipeline uses four phases:

# Phase 1) Fit a small section (60 columns of every charge injection) using a parallel CTI model
#          with 1 trap species and a model for the parallel CCD volume filling parameters.

# Phase 2) Fit a small section (again, 60 columns) using a parallel CTI model with 2 trap species and a model for the
#          parallel CCD volume filling parameters. The priors on trap densities and volume filling parameters are
#          initialized from the results of phase 1.

# Phase 3) Use the best-fit model from phase 2 to scale the noise of each image, to ensure that the higher and
#          lower S/N images are weighted more equally in their contribution to the likelihood.

# Phase 4) Refit the phase 2 model, using priors initialized from the results of phase 2 and the scaled noise-map
#          computed in phase 3.


def make_pipeline(
    phase_folders=None,
    tag_phases=True,
    mask_function=msk.Mask.empty_for_shape,
    parallel_front_edge_mask_rows=None,
    parallel_trails_mask_rows=None,
    parallel_total_density_range=None,
    serial_front_edge_mask_columns=None,
    serial_trails_mask_columns=None,
    serial_total_density_range=None,
    cosmic_ray_parallel_buffer=None,
    cosmic_ray_serial_buffer=None,
    cosmic_ray_diagonal_buffer=None,
):

    ### SETUP PIPELINE AND PHASE NAMES, TAGS AND PATHS ###

    # We setup the pipeline name using the tagging module. In this case, the pipeline name is not given a tag and
    # will be the string specified below However, its good practise to use the 'tag.' function below, incase
    # a pipeline does use customized tag names.

    pipeline_name = "pipeline_normal__parallel_x2_serial"

    phase_folders.append(pipeline_name)

    ### PHASE 1 ###

    # In phase 1, we will fit the data with a two species parallel and three species serial CTI model. In this
    # phase we will:

    # 1) Initialize the priors on this model from phases 2 and 4 of the initialize pipeline.

    class ParallelSerialPhase(ph.ParallelSerialPhase):
        def pass_priors(self, results):

            self.parallel_ccd = results.from_phase(
                "phase_2_parallel_x2"
            ).variable.parallel_ccd
            self.parallel_species = results.from_phase(
                "phase_2_parallel_x2"
            ).variable.parallel_species
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0
            self.serial_ccd = results.from_phase(
                "phase_4_serial_x3"
            ).variable.serial_ccd
            self.serial_species = results.from_phase(
                "phase_4_serial_x3"
            ).variable.serial_species
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase1 = ParallelSerialPhase(
        phase_name="phase_1_parallel_x2_serial_x3",
        phase_folders=phase_folders,
        tag_phases=tag_phases,
        parallel_species=[
            af.PriorModel(arctic_params.Species),
            af.PriorModel(arctic_params.Species),
        ],
        parallel_ccd=arctic_params.CCD,
        serial_species=[
            af.PriorModel(arctic_params.Species),
            af.PriorModel(arctic_params.Species),
            af.PriorModel(arctic_params.Species),
        ],
        serial_ccd=arctic_params.CCD,
        optimizer_class=af.MultiNest,
        mask_function=mask_function,
        parallel_front_edge_mask_rows=parallel_front_edge_mask_rows,
        parallel_trails_mask_rows=parallel_trails_mask_rows,
        serial_front_edge_mask_columns=serial_front_edge_mask_columns,
        serial_trails_mask_columns=serial_trails_mask_columns,
        parallel_total_density_range=parallel_total_density_range,
        serial_total_density_range=serial_total_density_range,
        cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
        cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
        cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer,
    )

    phase1.optimizer.const_efficiency_mode = False
    phase1.optimizer.n_live_points = 80
    phase1.optimizer.sampling_efficiency = 0.3

    return pl.Pipeline(pipeline_name, phase1)
