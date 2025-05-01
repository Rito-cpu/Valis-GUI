import argparse
import json
import argparse
import pathlib

from valis import registration
from return_selections import *
from keyword_store import *


def test(user_settings_path, slide_settings_path, home_dir):
    # read in JSON file as a dictionary
    json_file = open(user_settings_path)
    reader = json.load(json_file)
    selections_dict = reader['user_selections']
    json_file = open(slide_settings_path)
    reader = json.load(json_file)
    outer_image_dict = reader
    json_file.close()
    del reader

    # Puts slide source into destination src variable
    selections_dict["src_dir"] = outer_image_dict["src_dir"]

    # DST_DIR = dst_dir
    # NAME = name
    directory_list = []
    name_list = []

    # create list of sample directories and their corresponding names
    for sample_name, sample_dict in outer_image_dict.items():
        if sample_name == "src_dir":
            continue
        name_list.append(sample_name)
        slide_data = sample_dict["files"]
        directory_list.append(slide_data)

    for i in range(0, len(directory_list)):
        #slide_number refers to each slide within sample directory, slide_settings refers to the individual image settings in those samples
        for slide_number, slide_settings in directory_list[i].items():
            # if individual image is marked as "include," update value of image in directory_list to be its filepath
            # also add file to "processor_dict" with "/root" replacement and image type (this will be important if
            # the user has manually changed an image type in pre-registration settings).

            if slide_settings["Include"]:
                directory_list[i][slide_number] = slide_settings["File"]
            else:
                # if the user has chosen not to include an image, simply change the value to None
                directory_list[i][slide_number] = None
        directory_list[i] = {key: value.replace(home_dir, "/root") for key, value in directory_list[i].items() if value}

    for i in range(len(directory_list) - 1, -1, -1):
        # delete dirs if user has marked less than 2 images to be included
        if len(directory_list[i]) <= 1:
            directory_list.pop(i)
            name_list.pop(i)

    # directory_count will be used to determine how many runs of valis are needed
    directory_count = len(directory_list)

    for i in range(0, directory_count):
        selections_dict[IMG_LIST] = list(directory_list[i].values())
        selections_dict[NAME] = name_list[i]

        # code to run valis with the formatted data above
        registrar = registration.Valis(**selections_dict)
        registrar.warp_and_save_slides(selections_dict[DST_DIR] + "/" + selections_dict[NAME], crop="overlap")

def export_sample(selections_dict, sample_name, slide_data, home_dir):
    # Prepare filtered slide list (only included)
    filtered_dict = {
        slide_num: slide["File"]
        for slide_num, slide in slide_data.items()
        if slide["Include"]
    }

    if len(filtered_dict) <= 1:
        print(f"[SKIPPED] Sample '{sample_name}' has <=1 included images.")
        return

    # Convert paths to Docker container form
    filtered_dict = {
        k: v.replace(home_dir, "/root") for k, v in filtered_dict.items()
    }

    selections_dict[IMG_LIST] = list(filtered_dict.values())
    selections_dict[NAME] = sample_name

    output_path = pathlib.Path(selections_dict[DST_DIR]) / sample_name
    print(f"[EXPORTING] -> {str(output_path)}")


    #registrar = registration.Valis(**selections_dict)
    registrar_pickle_file = sample_name + "_registrar.pickle"
    pickle_path = output_path / "data" / registrar_pickle_file
    registrar = registration.load_registrar(pickle_path)
    registrar.warp_and_save_slides(str(output_path), crop="overlap")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", required=True, help="Path to user_settings.json")
    parser.add_argument("-il", required=True, help="Path to sample.json")
    parser.add_argument("-hdir", required=True, help="Host home directory")
    parser.add_argument("-name", required=False, help="(Optional) Export only this sample")
    args = parser.parse_args()

    home_dir = args.hdir

    # Load settings
    with open(args.path, "r") as f:
        selections_dict = json.load(f)["user_selections"]

    with open(args.il, "r") as f:
        sample_data = json.load(f)

    # Path conversions
    selections_dict[DST_DIR] = selections_dict[DST_DIR].replace(home_dir, "/root")
    selections_dict[SRC_DIR] = sample_data["src_dir"].replace(home_dir, "/root")

    selections_dict["matcher"] = get_matcher_obj(
        selections_dict.pop(MATCH_FILTER_METHOD),
        selections_dict.pop(FEATURE_MATCHING_METRIC),
        selections_dict[FEATURE_DETECTOR_CLS]
    )
    selections_dict[FEATURE_DETECTOR_CLS] = get_feature_detector_obj(selections_dict[FEATURE_DETECTOR_CLS])
    selections_dict[TRANSFORMER_CLS] = get_image_transformer(selections_dict[TRANSFORMER_CLS])
    selections_dict[AFFINE_OPTIMIZER_CLS] = get_affine_optimizer((selections_dict[AFFINE_OPTIMIZER_CLS]))
    selections_dict[MICRO_RIGID_REGISTRAR_CLS] = get_micro_rigid_registrar(selections_dict[MICRO_RIGID_REGISTRAR_CLS])

    selections_dict = {k: v for k, v in selections_dict.items() if v}

    if NON_RIGID_REGISTRAR_CLS not in selections_dict:
        selections_dict[NON_RIGID_REGISTRAR_CLS] = None
    selections_dict[NON_RIGID_REGISTRAR_CLS], selections_dict[NON_RIGID_REG_PARAMS] = get_nonrigid_registrar_obj(
        selections_dict[NON_RIGID_REGISTRAR_CLS])
    
    _ = selections_dict.pop(IF_PROCESSOR)
    _ = selections_dict.pop(BF_PROCESSOR)

    if args.name:
        if args.name not in sample_data:
            raise ValueError(f"Sample '{args.name}' not found in sample.json.")
        export_sample(selections_dict, args.name, sample_data[args.name]["files"], home_dir)
    else:
        # Iterates through sample settings: src_dir, sample-0, ..., sample-n
        for sample_name, slide_info in sample_data.items():
            if sample_name == "src_dir":
                continue
            export_sample(selections_dict, sample_name, slide_info["files"], home_dir)

if __name__ == "__main__":
    main()
