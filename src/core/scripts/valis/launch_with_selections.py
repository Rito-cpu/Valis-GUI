# this is script that reads the selections in user_settings.json and sample.json and runs valis using those files.
# This script will run within the docker container, so any filepath needs to be formatted with a "/root" in place
# of the "~" directory on the host machine.



#there are a couple "problem" areas that may not function on a windows machine, they will be commented throughout this code


import os
import sys

# this particular line of code may not work on windows because of the use of a backslash.
# A simple if statement using sys.platform.startswith("win32") should be able to fix this.
# Alternatively, if you can modify the import statements entirely so that this code is no longer needed,
# that would be ideal.
sys.path.append("/".join(os.path.realpath(__file__).split("/")[0:-3]))

from return_selections import *
import json
from keyword_store import *
from valis import registration
import argparse


def launch_with_selections(settings_path: str, image_path: str, home_dir: str):
    """
    Args:
        settings_path: the full filepath to the user_settings.json file within the docker container
        image_path: the full filepath to sample.json file within the docker container
        home_dir: the value of os.expanduser("~") on the host machines OS,
        required for manipulation of filepaths within the docker container
    """

    # read in JSON file as a dictionary
    f = open(settings_path)
    reader = json.load(f)
    selections_dict = reader['user_selections']
    f = open(image_path)
    reader = json.load(f)
    outer_image_dict = reader
    f.close()
    del reader

    selections_dict["src_dir"] = outer_image_dict["src_dir"]

    # convert strings in dictionary to needed objects using functions in return_selections.py
    selections_dict["matcher"] = get_matcher_obj(
        selections_dict.pop(MATCH_FILTER_METHOD),
        selections_dict.pop(FEATURE_MATCHING_METRIC),
        selections_dict[FEATURE_DETECTOR_CLS]
    )
    selections_dict[FEATURE_DETECTOR_CLS] = get_feature_detector_obj(selections_dict[FEATURE_DETECTOR_CLS])
    selections_dict[TRANSFORMER_CLS] = get_image_transformer(selections_dict[TRANSFORMER_CLS])
    selections_dict[AFFINE_OPTIMIZER_CLS] = get_affine_optimizer((selections_dict[AFFINE_OPTIMIZER_CLS]))
    selections_dict[MICRO_RIGID_REGISTRAR_CLS] = get_micro_rigid_registrar(selections_dict[MICRO_RIGID_REGISTRAR_CLS])

    # convert user filepaths into compatible docker container filepaths
    selections_dict[SRC_DIR] = selections_dict[SRC_DIR].replace(home_dir, "/root")
    selections_dict[DST_DIR] = selections_dict[DST_DIR].replace(home_dir, "/root")

    # remove all None values from dictionary
    selections_dict = {k: v for k, v in selections_dict.items() if v}

    # check for non-rigid registrar in dictionary and initialize one if doesnt exist
    if NON_RIGID_REGISTRAR_CLS not in selections_dict:
        selections_dict[NON_RIGID_REGISTRAR_CLS] = None
    selections_dict[NON_RIGID_REGISTRAR_CLS], selections_dict[NON_RIGID_REG_PARAMS] = get_nonrigid_registrar_obj(
        selections_dict[NON_RIGID_REGISTRAR_CLS])

    # separate registration parameters from main dictionary
    registration_params = selections_dict.pop(IF_PROCESSOR)
    registration_params.update(selections_dict.pop(BF_PROCESSOR))

    # convert strings to needed processor object
    registration_params[IF_PROCESSING_CLS], registration_params[BRIGHTFIELD_PROCESSING_CLS] = get_image_processor_obj(
        registration_params[IF_PROCESSING_CLS], registration_params[BRIGHTFIELD_PROCESSING_CLS])

    # generate dictionaries of image paths and determine the amount of runs of valis that are needed
    directory_list = []
    name_list = []
    processor_dict = {}
    processor_dict_list = []

    r'''
    Explanation of home_dir and "/root":
        home_dir refers to the "~" directory of the users host system (Users/Username on POSIX, C:\Users\username on windows).
        "/root" refers to the directory within the docker container to which the host system is mounted. In order for 
        this code to work correctly, any instance of home_dir passed into the container must be corrected to "/root" so 
        that the filepath is accurate to the file structure of the linux-based docker container. 
        '''

    # create list of sample directories and their corresponding names
    for k, v in outer_image_dict.items():
        if k == "src_dir":
            continue
        name_list.append(k)
        samples = v["files"]
        directory_list.append(samples)

    for i in range(0, len(directory_list)):
        #k refers to each sample directory, v refers to the individual images in those samples
        for k, v in directory_list[i].items():

            # if individual image is marked as "include," update value of image in directory_list to be its filepath
            # also add file to "processor_dict" with "/root" replacement and image type (this will be important if
            # the user has manually changed an image type in pre-registration settings).

            if v["Include"]:
                directory_list[i][k] = v["File"]
                processor_dict.update({v["File"].replace(home_dir, "/root"): v["Image type"]})
            else:
                # if the user has chosen not to include an image, simply change the value to None
                directory_list[i][k] = None

        # change all "home_dir" values to "/root" in dictionary
        directory_list[i] = {key: value.replace(home_dir, "/root") for key, value in directory_list[i].items() if value}

    for i in range(len(directory_list) - 1, -1, -1):
        # delete dirs if user has marked less than 2 images to be included
        if len(directory_list[i]) <= 1:
            directory_list.pop(i)
            name_list.pop(i)


    # generates a new list of image types based on newly updated directory list
    for i in range(0, len(directory_list)):
        processor_dict_list.append(
            {key: value for key, value in processor_dict.items() if key in list(directory_list[i].values())})

    # replaces stored string values referring to image type within each sample with the correct processor object
    for i in processor_dict_list:
        # i refers to the processor dict for each sample, k refers to the filepaths
        for k in i:
            if i[k] == "fluorescence":
                i[k] = registration_params[IF_PROCESSING_CLS]
            else:
                i[k] = registration_params[BRIGHTFIELD_PROCESSING_CLS]


    # directory_count will be used to determine how many runs of valis are needed
    directory_count = len(directory_list)

    for i in range(0, directory_count):
        # assign list of processor objects corresponding to each filepath
        registration_params["processor_dict"] = processor_dict_list[i]

        selections_dict[IMG_LIST] = list(directory_list[i].values())
        selections_dict[NAME] = name_list[i]

        # code to run valis with the formatted data above
        registrar = registration.Valis(**selections_dict)

        rigid_registrar, non_rigid_registrar, error_df = registrar.register(**registration_params)

        registrar.warp_and_save_slides(selections_dict[DST_DIR] + "/" + selections_dict[NAME], crop="overlap")

    registration.kill_jvm()


if __name__ == "__main__":

    # create args to pass file locations into python script when called in launchscript.sh

    parser = argparse.ArgumentParser(prog="Valis_launch_script", description="launches VALIS using arguments read in "
                                                                             "from a JSON file")
    # -path is the path to the user_settings.json file, -il is the path to the sample.json file,
    # -hdir is the string representing os.expanduser("~") on the user's system.
    parser.add_argument('-path')
    parser.add_argument('-il')
    parser.add_argument("-hdir")

    args = parser.parse_args()

    launch_with_selections(args.path, args.il, args.hdir)
