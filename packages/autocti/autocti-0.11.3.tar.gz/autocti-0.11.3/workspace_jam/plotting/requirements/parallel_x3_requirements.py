import autofit as af
from autocti.model import arctic_params as ap
import os

from workspace_jam.plotting.requirements.tools import weighted_avg_and_std


def parallel_x3_requirements_of_resolutions(ci_resolutions):

    # Setup the path to the workspace, using a relative directory name.
    workspace_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))
    output_path = workspace_path + "../../outputs/PyAutoCTI/"

    # Use this path to explicitly set the config path and output path.
    af.conf.instance = af.conf.Config(
        config_path=workspace_path + "config", output_path=output_path
    )

    input_parallel_species_0 = ap.Species(trap_density=0.01, trap_lifetime=0.8)
    input_parallel_species_1 = ap.Species(trap_density=0.03, trap_lifetime=4.0)
    input_parallel_species_2 = ap.Species(trap_density=0.9, trap_lifetime=20.0)
    input_arctic_params = ap.ArcticParams(
        parallel_species=[
            input_parallel_species_0,
            input_parallel_species_1,
            input_parallel_species_2,
        ]
    )
    input_delta_ellipticity = input_arctic_params.delta_ellipticity

    pipeline = "pipeline_hyper__parallel_x3"
    pipeline_meta = "pipeline_init__parallel_x3 + pipeline_hyper__parallel_x3"
    phase = "phase_2_parallel_x3_noise_scaled"

    ci_image = "ci_images_non_uniform_cosmic_rays"
    ci_model = "parallel_x3_poisson"
    ci_setting = "settings_cr_p10s10d3"

    requirement_means_of_resolutions = []
    requirement_stds_of_resolutions = []
    requirement_errors_of_resolutions = []

    for ci_resolution in ci_resolutions:

        agg = af.Aggregator(
            directory=output_path
            + ci_image
            + "/"
            + ci_model
            + "/"
            + ci_resolution
            + "/"
            + pipeline
            + "/"
            + phase
            + "/"
            + ci_setting
        )
        print(
            output_path
            + ci_image
            + "/"
            + ci_model
            + "/"
            + ci_resolution
            + "/"
            + pipeline
            + "/"
            + phase
            + "/"
            + ci_setting
        )
        optimizer = agg.optimizers_with(pipeline=pipeline_meta, phase=phase)[0]

        weights = []
        requirements = []

        for sample_index in range(optimizer.total_samples):

            weight = optimizer.sample_weight_from_sample_index(
                sample_index=sample_index
            )

            if weight > 1.0e-4:

                params = optimizer.sample_model_parameters_from_sample_index(
                    sample_index=sample_index
                )
                instance = optimizer.variable.instance_from_physical_vector(
                    physical_vector=params
                )
                params = ap.ArcticParams(parallel_species=instance.parallel_species)
                requirement = params.delta_ellipticity - input_delta_ellipticity
                weights.append(weight)
                requirements.append(requirement)

        requirement_mean, requirement_std = weighted_avg_and_std(
            values=requirements, weights=weights
        )

        requirement_means_of_resolutions.append(requirement_mean)
        requirement_stds_of_resolutions.append(requirement_std)
        requirement_errors_of_resolutions.append(requirement_std / 2.0)

    return requirement_means_of_resolutions, requirement_errors_of_resolutions
