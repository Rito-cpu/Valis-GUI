import os.path
from pathlib import PureWindowsPath, PurePosixPath
import sys
import subprocess
import json
from threading import Thread
import progress_bar


def on_register_press():

    # check for user platform and reformat running directory as needed, also obtain home dir for use within docker container
    # THIS CODE HAS NOT BEEN TESTED ON A WINDOWS MACHINE
    if sys.platform.startswith("win32"):
        running_dir = PureWindowsPath(
            r'C:\Users\80029349\Documents\GUI-Repo\Valis-GUI\src\core\scripts\valis\on_register_press.py').as_posix()
        home_dir = str(PurePosixPath(PureWindowsPath(os.path.expanduser("~"))))
    else:
        running_dir = PurePosixPath(__file__)
        home_dir = os.path.expanduser("~")

    # generate paths for necessary files to be passed into docker container, replacing home_dir with "/root"
    running_dir_list = list(running_dir.parts)

    running_dir_list[-1] = "launch_with_selections.py"
    script_dir = os.path.join(*running_dir_list)
    script_dir = script_dir.replace(home_dir, '/root')

    running_dir_list[-1] = "user_settings.JSON"
    json_dir = os.path.join(*running_dir_list)
    json_dir = json_dir.replace(home_dir, '/root')

    running_dir_list[-1] = "sample.JSON"
    img_dir = os.path.join(*running_dir_list)
    img_dir = img_dir.replace(home_dir, '/root')

    # run launchscript.sh with generated arguments
    subprocess.run(["bash", "./launchscript.sh", script_dir, json_dir, img_dir, home_dir])


def start_prog_bar():

    # get names of samples and number of steps selected by the user to be passed to the progress bar

    f = open("user_settings.json")
    reader = json.load(f)["user_selections"]
    do_rigid, do_micro, do_non_rigid = reader["do_rigid"], reader["micro_rigid_registrar_cls"], reader[
        "non_rigid_registrar_cls"]

    f = open("sample.json")
    reader = json.load(f)
    sample_list = list(reader.keys())
    f.close()

    del reader

    # create a dictionary of steps to be passed into the progress bar. This will determine how many steps
    # are given to the progress bar on initialization.

    steps_dict = {"rigid": do_rigid, "micro_rigid": do_micro, "non_rigid": do_non_rigid}
    steps_dict = {k: v for k, v in steps_dict.items() if v is not False or None}
    progress_bar.init_prog_bar("/Users/80029349/Documents/DummyOutput2", steps_dict, sample_list)


if __name__ == "__main__":

    x = Thread(target=on_register_press)
    x.start()
    start_prog_bar()
    x.join()
