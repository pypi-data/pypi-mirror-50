import autofit as af
import os

workspace_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))
output_path = workspace_path + "output/"

pipeline = "pipeline_normal__parallel_x2"
phase = "phase_1_parallel_x2"

aggregator = af.Aggregator(directory=output_path)

optimizers = aggregator.optimizers_with(pipeline=pipeline, phase=phase)

most_probables = list(map(lambda opt: opt.most_probable_model_parameters, optimizers))
upper_errors = list(
    map(lambda opt: opt.model_errors_at_upper_sigma_limit(sigma_limit=3.0), optimizers)
)
lower_errors = list(
    map(lambda opt: opt.model_errors_at_lower_sigma_limit(sigma_limit=3.0), optimizers)
)

slopes = most_probables[:][5]
slopes_uppers = upper_errors[:][5]
slopes_lowers = lower_errors[:][5]
