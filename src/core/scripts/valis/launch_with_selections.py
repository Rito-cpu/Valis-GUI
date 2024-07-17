import os
import sys
import time

sys.path.append("/".join(os.path.realpath(__file__).split("/")[0:-3]))

from return_selections import *
import json
from keyword_store import *
from threading import Thread
from completion_checker import check_completion
from valis import registration
import argparse


def launch_with_selections(settings_path: str, image_path: str):

    # read in JSON file as a dictionary
    f = open(settings_path)
    reader = json.load(f)
    selections_dict = reader['user_selections']
    f = open(image_path)
    reader = json.load(f)
    outer_image_dict = reader
    f.close()
    del reader


    # convert strings in dictionary to needed object
    selections_dict["matcher"] = get_matcher_obj(selections_dict.pop(MATCH_FILTER_METHOD),
                                                 selections_dict.pop(FEATURE_MATCHING_METRIC),
                                                 selections_dict[FEATURE_DETECTOR_CLS])
    selections_dict[FEATURE_DETECTOR_CLS] = get_feature_detector_obj(selections_dict[FEATURE_DETECTOR_CLS])
    selections_dict[TRANSFORMER_CLS] = get_image_transformer(selections_dict[TRANSFORMER_CLS])
    selections_dict[AFFINE_OPTIMIZER_CLS] = get_affine_optimizer((selections_dict[AFFINE_OPTIMIZER_CLS]))
    selections_dict[MICRO_RIGID_REGISTRAR_CLS] = get_micro_rigid_registrar(selections_dict[MICRO_RIGID_REGISTRAR_CLS])

    # remove all None values from dictionary
    selections_dict = {k: v for k, v in selections_dict.items() if v}

    # check for non-rigid registrar in dictionary
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

    # generate image dictionaries and determine the amount of runs of valis that are needed
    directory_list = []
    name_list = []

    for k, v in outer_image_dict.items():
        directory_list.append(v)
        name_list.append(k)

    for i in range(0, len(directory_list)):
        for k, v in directory_list[i].items():
            directory_list[i][k] = v["File"] if v["Include"] else None
        directory_list[i] = {key: value for key, value in directory_list[i].items() if value}

    directory_count = len(name_list)

    home_path = os.path.expanduser("~")
    selections_dict[SRC_DIR].replace(home_path, '/root')
    selections_dict[DST_DIR].replace(home_path, '/root')

    for i in range(0, directory_count):

        selections_dict[IMG_LIST] = list(directory_list[i].values())
        selections_dict[NAME] = name_list[i]

        # code to run valis with the formatted data above
        registrar = registration.Valis(**selections_dict)

        rigid_registrar, non_rigid_registrar, error_df = registrar.register(**registration_params)

        registrar.warp_and_save_slides(selections_dict[DST_DIR], crop="overlap")

    registration.kill_jvm()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Valis_launch_script", description="launches VALIS using arguments read in "
                                                                             "from a JSON file")
    parser.add_argument('-path')
    parser.add_argument('-il')

    args = parser.parse_args()

    start = time.perf_counter()

    #thread1 = Thread(target=check_completion)
    #thread1.start()
    launch_with_selections(args.path, args.il)
    #thread1.join()

    end = time.perf_counter()
    elapsed_time = end - start

    print(f"{elapsed_time} seconds have passed")
