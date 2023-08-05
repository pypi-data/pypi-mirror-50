from autofit import conf
import os

import autofit as af
from autocti.charge_injection import ci_pattern
from autocti.charge_injection import ci_data

from autocti.model import arctic_settings

from workspace_jam.tools.data_makers import tools

from multiprocessing import Pool

# Setup the path to the workspace, using a relative directory name.
workspace_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))
output_path = workspace_path + "../../outputs/PyAutoCTI/"
af.conf.instance = af.conf.Config(
    config_path=workspace_path + "config", output_path=output_path
)

# Welcome to the pipeline runner. This tool allows you to CTI calibration data on strong lenses, and pass it to
# pipelines for a PyAutoCTI analysis. To show you around, we'll load up some example data and run it through some of
# the example pipelines that come distributed with PyAutoCTI.

# The runner is supplied as both this Python script and a Juypter notebook. Its up to you which you use - I personally
# prefer the python script as provided you keep it relatively small, its quick and easy to comment out data-set names
# and pipelines to perform different analyses. However, notebooks are a tidier way to manage visualization - so
# feel free to use notebooks. Or, use both for a bit, and decide your favourite!

# The pipeline runner is fairly self explanatory. Make sure to checkout the pipelines in the
#  workspace/pipelines/examples/ folder - they come with detailed descriptions of what they do. I hope that you'll
# expand on them for your own personal scientific needs

# It is convenient to specify the image type and model used to simulate that image as strings, so that if the
# pipeline is applied to multiple images we don't have to change all of the path entries in the
# load_ci_data_from_fits function below.

ci_data_type = (
    "ci_lines_uniform"
)  # Charge injection data consisting of 2 images with uniform injections.
ci_data_model = (
    "serial_x3"
)  # Shows the data was creating using a serial CTI model with one species.

# Create the path where the data will be output, which in this case is
# '/workspace/data/ci_lines_uniform/serial_x2_species/high_res/'
ci_data_path = af.path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=["data", ci_data_type, ci_data_model]
)

# This tools loads the correct shape of the line and frame geometry, for the ci_data_resoultion string.
shape, frame_geometry = tools.charge_line_shape_and_frame_geometry_from_direction(
    direction="serial"
)

# Specify the charge injection regions on the CCD, which in this case is 7 equally spaced rectangular blocks.
ci_regions = [(0, 1, 51, shape[1] - 20)]

# The normalization of the charge injection for each image.
normalizations = [100.0, 500.0, 1000.0, 5000.0, 10000.0, 25000.0, 50000.0, 84700.0]

# Create the charge injection pattern objects used for this pipeline.
patterns = ci_pattern.uniform_from_lists(
    normalizations=normalizations, regions=ci_regions
)

# There are 8 images to load, which is what the normalizations list tells us. To load them, its easiest to create a
# 'data' list and then iterate over a for loop, to append each set of data to the list of data we pass to the pipeline
# when we run it.

datas = []

for index, normalization in enumerate(normalizations):

    datas.append(
        ci_data.ci_data_from_fits(
            frame_geometry=frame_geometry,
            ci_pattern=patterns[index],
            image_path=ci_data_path + "line_" + str(int(normalization)) + ".fits",
            ci_pre_cti_path=ci_data_path
            + "/ci_pre_cti_"
            + str(int(normalization))
            + ".fits",
            noise_map_from_single_value=0.1,
        )
    )

# The CTI settings of arCTIc, which models the CCD read-out including CTI. For serial ci data, we include 'charge
# injection mode' which accounts for the fact that every pixel is transferred over the full CCD.
serial_cti_settings = arctic_settings.Settings(
    well_depth=84700,
    niter=1,
    express=2,
    n_levels=2000,
    charge_injection_mode=False,
    readout_offset=0,
)
cti_settings = arctic_settings.ArcticSettings(serial=serial_cti_settings)

# Running a pipeline is easy, we simply import it from the pipelines folder and pass the ci data to its run function.
# Below, we'll' use a 2 phase example pipeline to fit the data with a one species serial CTI model.
# Checkout workspace/pipelines/examples/serial_x1_species.py' for a full description of the pipeline.

# The pool command tells our code to serialize the analysis over 2 CPU's, where each CPU fits a different charge
# injection image

from workspace_jam.pipelines.initialize import serial_x3

pipeline_init = serial_x3.make_pipeline(phase_folders=[ci_data_type, ci_data_model])

from workspace_jam.pipelines.normal.from_initialize import serial_x3

pipeline_normal = serial_x3.make_pipeline(phase_folders=[ci_data_type, ci_data_model])

pipeline = pipeline_init + pipeline_normal

pipeline.run(
    ci_datas=datas,
    cti_settings=cti_settings,
    pool=Pool(processes=2),
    assert_optimizer_pickle_matches=False,
)
