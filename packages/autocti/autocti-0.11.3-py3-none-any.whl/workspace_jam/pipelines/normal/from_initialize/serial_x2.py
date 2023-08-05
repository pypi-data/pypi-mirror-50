import autofit as af
from autocti.data import mask as msk
from autocti.pipeline import pipeline as pl
from autocti.pipeline import phase as ph
from autocti.model import arctic_params

# In this pipeline, we'll perform an analysis which fits two serial trap species to a set of charge
# injection imaging data. This will include a hyper-phase which scales the noise in the analysis, to prevent
# over-fitting the highest S/N charge injection images. The pipeline uses four phases:

# Phase 1) Fit a small section (60 columns of every charge injection) using a serial CTI model
#          with 1 trap species and a model for the serial CCD volume filling parameters.

# Phase 2) Fit a small section (again, 60 columns) using a serial CTI model with 2 trap species and a model for the
#          serial CCD volume filling parameters. The priors on trap densities and volume filling parameters are
#          initialized from the results of phase 1.

# Phase 3) Use the best-fit model from phase 2 to scale the noise of each image, to ensure that the higher and
#          lower S/N images are weighted more equally in their contribution to the likelihood.

# Phase 4) Refit the phase 2 model, using priors initialized from the results of phase 2 and the scaled noise-map
#          computed in phase 3.


def make_pipeline(
    phase_folders=None,
    tag_phases=True,
    mask_function=msk.Mask.empty_for_shape,
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

    pipeline_name = "pipeline_normal__serial_x2"

    phase_folders.append(pipeline_name)

    ### PHASE 1 ###

    # In phase 1, we will fit the data with a 3 species serial CTI model and serial CCD filling model. In this
    # phase we will:

    # 1) Use the complete charge injection image, as opposed to extracting a sub-set of columns.
    # 3) Initialize the priors on the serial CTI model from the results of the initialize pipeline's phase 2.

    class SerialPhase(ph.SerialPhase):
        def pass_priors(self, results):

            self.serial_species = results.from_phase(
                "phase_2_serial_x2"
            ).variable.serial_species
            self.serial_ccd = results.from_phase(
                "phase_2_serial_x2"
            ).variable.serial_ccd
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase1 = SerialPhase(
        phase_name="phase_1_serial_x2",
        phase_folders=phase_folders,
        tag_phases=tag_phases,
        serial_species=[
            af.PriorModel(arctic_params.Species),
            af.PriorModel(arctic_params.Species),
        ],
        serial_ccd=arctic_params.CCD,
        mask_function=mask_function,
        serial_front_edge_mask_columns=serial_front_edge_mask_columns,
        serial_trails_mask_columns=serial_trails_mask_columns,
        serial_total_density_range=serial_total_density_range,
        cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
        cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
        cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer,
        optimizer_class=af.MultiNest,
    )

    # For the final CTI model, constant efficiency mode has a tendency to sample parameter space too fast and infer an
    # inaccurate model. Thus, we turn it off for phase 2.

    phase1.optimizer.const_efficiency_mode = False
    phase1.optimizer.n_live_points = 50
    phase1.optimizer.sampling_efficiency = 0.3

    return pl.Pipeline(pipeline_name, phase1)
