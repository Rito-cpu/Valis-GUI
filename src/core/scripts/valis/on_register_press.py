# this is the script that will run when the user hits register in the GUI. It collects relevant filepaths for needed
# json files and the user's "~" directory and runs launch_with_selections.py with launchscript.sh. It also launches the
# progress bar using multithreading, but it may be better to change the implementation of the progress bar to run from
# another file


import os.path
from pathlib import PureWindowsPath, PurePosixPath
import sys
import subprocess
import json
from threading import Thread
from src.core.validation.platform_retrieval import is_windows_platform
from src.core.validation import is_windows_platform, is_valid_json_file, is_existing_path
# import progress_bar


def on_register_press():
    # check for user platform and reformat running directory as needed, also obtain home dir for use within docker container
    # THIS CODE HAS NOT BEEN TESTED ON A WINDOWS MACHINE
    # TODO: Configure windows portion
    if is_windows_platform():
        running_dir = PureWindowsPath(
            r'C:\Users\80029349\Documents\GUI-Repo\Valis-GUI\src\core\scripts\valis\on_register_press.py').as_posix()
        home_dir = str(PurePosixPath(PureWindowsPath(os.path.expanduser("~"))))
    else:
        running_dir = PurePosixPath(__file__)
        home_dir = os.path.expanduser("~")

    # generate paths for necessary files to be passed into docker container, replacing home_dir with "/root"
    running_dir_list = list(running_dir.parts)

    for i in reversed(range(len(running_dir_list))):
        if running_dir_list[i] == "core":
            break
        else:
            running_dir_list.pop(i)

    selections_script = ["scripts", "valis", "launch_with_selections.py"]
    script_dir = os.path.join(*running_dir_list, *selections_script)
    if not is_existing_path(script_dir):
        print("Error: launch_with_selections.py not found!")
        return

    output_dir = ["output", "states"]
    json_dir = os.path.join(*running_dir_list, *output_dir, "user_settings.json")
    if not is_valid_json_file(json_dir):
        print("Error: user_settings.json not found!")
        return

    img_dir = os.path.join(*running_dir_list, *output_dir, "sample.json")
    if not is_valid_json_file(img_dir):
        print("Error: sample.json not found!")
        return

    script_dir = script_dir.replace(home_dir, '/root')
    json_dir = json_dir.replace(home_dir, '/root')
    img_dir = img_dir.replace(home_dir, '/root')

    # run launchscript.sh with generated arguments
    launch_build = ["scripts", "valis", "launchscript.sh"]
    launch_build = os.path.join(*running_dir_list, *launch_build)
    subprocess.run(["bash", launch_build, script_dir, json_dir, img_dir, home_dir])


def start_prog_bar():
    # get names of samples and number of steps selected by the user to be passed to the progress bar
    if is_windows_platform():
        running_dir = PureWindowsPath(
            r'C:\Users\80029349\Documents\GUI-Repo\Valis-GUI\src\core\scripts\valis\on_register_press.py').as_posix()
        home_dir = str(PurePosixPath(PureWindowsPath(os.path.expanduser("~"))))
    else:
        running_dir = PurePosixPath(__file__)
        home_dir = os.path.expanduser("~")

    # generate paths for necessary files to be passed into docker container, replacing home_dir with "/root"
    running_dir_list = list(running_dir.parts)

    for i in reversed(range(len(running_dir_list))):
        if running_dir_list[i] == "core":
            break
        else:
            running_dir_list.pop(i)

    running_dir_list.append("output")
    running_dir_list.append("states")

    # output_dir = os.path.join(*running_dir_list, "output/states")

    f = open(os.path.join(*running_dir_list, "user_settings.json"))
    reader = json.load(f)["user_selections"]
    do_rigid, do_micro, do_non_rigid = reader["do_rigid"], reader["micro_rigid_registrar_cls"], reader["non_rigid_registrar_cls"]
    dest_dir = reader["dst_dir"]

    f = open(os.path.join(*running_dir_list, "sample.json"))
    reader = json.load(f)
    sample_list = list(reader.keys())
    f.close()

    del reader

    # create a dictionary of steps to be passed into the progress bar. This will determine how many steps
    # are given to the progress bar on initialization.

    steps_dict = {"rigid": do_rigid, "micro_rigid": do_micro, "non_rigid": do_non_rigid}
    steps_dict = {k: v for k, v in steps_dict.items() if v is not False or None}

    # progress_bar.init_prog_bar("/Users/80029349/Documents/DummyOutput2", steps_dict, sample_list)
    #valis_bar = ValisBar(dest_dir, steps_dict, sample_list)
    #bar_wid.create_thread(dest_dir, steps_dict, sample_list)
    #valis_bar.show()


#if __name__ == "__main__":
    #x = Thread(target=on_register_press)
    #x.start()
    #start_prog_bar()
    #x.join()
