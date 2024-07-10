import os.path
import pathlib
from pathlib import Path, PurePosixPath
import subprocess

if __name__ == "__main__":

    running_dir = pathlib.PurePosixPath(__file__)
    running_dir_list = list(running_dir.parts)
    home_dir = os.path.expanduser("~")

    running_dir_list[-1] = "launch_with_selections.py"
    script_dir = os.path.join(*running_dir_list)
    script_dir = script_dir.replace(home_dir,'/root')

    running_dir_list[-1] = "user_settings.JSON"
    json_dir = os.path.join(*running_dir_list)
    json_dir = json_dir.replace(home_dir, '/root')

    subprocess.run(["bash", "./launchscript.sh", script_dir, json_dir])