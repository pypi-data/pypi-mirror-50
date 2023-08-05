import autofit as af
import os

import matplotlib.pyplot as plt

# Setup the path to the workspace, using a relative directory name.
workspace_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))
plot_path = "{}/plotting/results/plots/".format(workspace_path)
output_path = workspace_path + "../../outputs/PyAutoCTI/"

# Use this path to explicitly set the config path and output path.
af.conf.instance = af.conf.Config(
    config_path=workspace_path + "config", output_path=output_path
)

input_model_parameters = [0.13, 0.25, 1.25, 4.4, 1.0e-4, 0.58]
ylabels = [r"$\rho_{1}$", r"$\rho_{2}$", r"$\tau_{1}$", r"$\tau_{2}$", "d", r"$\beta$"]

pipeline = "pipeline_hyper__serial_x2"
pipeline_meta = "pipeline_init__serial_x2 + pipeline_hyper__serial_x2"
phase = "phase_2_serial_x2_noise_scaled"

sigma_limit = 2.0

columns = [517, 1034 , 2068, 4136]

ci_images = [
    "ci_images_uniform",
    "ci_images_non_uniform",
    "ci_images_uniform_cosmic_rays",
    "ci_images_non_uniform_cosmic_rays",
    "ci_images_non_uniform_cosmic_rays",
]
ci_models = ["serial_x2", "serial_x2",
             "serial_x2",
             "serial_x2", "serial_x2"]
ci_settings = [
    "settings",
    "settings",
    "settings_cr_p10s10d3",
    "settings_cr_p10s10d3",
    "settings_ser_front_mask_col_(0,2048)_cr_p10s10d3",
]

ci_resolutions = ["low_resolution", "mid_resolution", 'high_resolution', 'x2_high_resolution']

total_params = len(input_model_parameters)
total_images = len(ci_images)
total_resolutions = len(ci_resolutions)

most_probables_of_images = []
upper_errors_of_images = []
lower_errors_of_images = []
model_errors_of_images = []

for ci_image, ci_model, ci_setting in zip(ci_images, ci_models, ci_settings):

    optimizers = []

    for ci_resolution in ci_resolutions:

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
        optimizers.append(agg.optimizers_with(pipeline=pipeline_meta, phase=phase)[0])

    most_probables_of_resolutions = list(
        map(lambda opt: opt.most_probable_model_parameters, optimizers)
    )
    upper_errors_of_resolution = list(
        map(
            lambda opt: opt.model_errors_at_upper_sigma_limit(sigma_limit=sigma_limit),
            optimizers,
        )
    )
    lower_errors_of_resolutions = list(
        map(
            lambda opt: opt.model_errors_at_lower_sigma_limit(sigma_limit=sigma_limit),
            optimizers,
        )
    )
    model_errors_of_resolutions = list(
        map(
            lambda opt: opt.model_errors_at_sigma_limit(sigma_limit=sigma_limit),
            optimizers,
        )
    )

    most_probables_of_images.append(most_probables_of_resolutions)
    upper_errors_of_images.append(upper_errors_of_resolution)
    lower_errors_of_images.append(lower_errors_of_resolutions)
    model_errors_of_images.append(model_errors_of_resolutions)

plt.figure(figsize=(20, 15))
plt.suptitle("Accuracy of Serial CTI Model", fontsize=20)

ebs = []

jitters = [-40.0, -20.0, 0.0, 20.0, 40.0]

for param_index in range(total_params):

    plt.subplot(2, 3, param_index + 1)

    columns_plot = [min(columns) + min(jitters), 1034, 2068, 4136]

    plt.plot(
        columns_plot,
        [input_model_parameters[param_index] for j in range(len(columns))],
        linestyle="-",
        linewidth=2,
    )

    for image_index in range(total_images):

        columns_plot = list(map(lambda column: column + jitters[image_index], columns))

        eb = plt.errorbar(
            x=columns_plot,
            y=[
                most_probables_of_image[param_index]
                for most_probables_of_image in most_probables_of_images[image_index]
            ],
            yerr=[
                [
                    lower_errors_of_image[param_index]
                    for lower_errors_of_image in lower_errors_of_images[image_index]
                ],
                [
                    upper_errors_of_image[param_index]
                    for upper_errors_of_image in upper_errors_of_images[image_index]
                ],
            ],
            capsize=5,
            elinewidth=1,
            markeredgewidth=3,
            linestyle="--",
        )
        eb[-1][0].set_linestyle("-")
        eb[-1][0].set_linewidth(1)

    plt.xlabel("Number of rows", fontsize=12)
    plt.ylabel(ylabels[param_index], fontsize=12)

plt.figlegend(
    labels=[
        "Uniform",
        "Non-uniform",
        "Poisson",
        "Cosmic Rays",
        "All",
        "All (No FPR)",
        "Input Value",
    ],
    bbox_to_anchor=(0.91, 0.96),
    ncol=7,
    fontsize=17,
)

plt.savefig(plot_path + "/serial_x2_accuracy_hyper.png")
plt.show()


plt.figure(figsize=(20, 15))
plt.suptitle("Precision of Serial CTI Model", fontsize=20)

for param_index in range(6):

    plt.subplot(2, 3, param_index + 1)

    for image_index in range(total_images):

        plt.plot(
            columns,
            [
                model_errors_of_image[param_index]
                for model_errors_of_image in model_errors_of_images[image_index]
            ],
        )

    plt.xlabel("Number of rows", fontsize=12)
    plt.ylabel(ylabels[param_index], fontsize=12)

plt.figlegend(
    labels=["Uniform", "Non-uniform", "Poisson", "Cosmic Rays", "All", "All (No FPR)"],
    bbox_to_anchor=(0.91, 0.96),
    ncol=6,
    fontsize=21,
)

import os

plt.savefig(plot_path + "/serial_x2_precision_hyper.png")
plt.show()
