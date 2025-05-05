import argparse
import json
import argparse
import pathlib

from valis import registration
from return_selections import *
from keyword_store import *


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
