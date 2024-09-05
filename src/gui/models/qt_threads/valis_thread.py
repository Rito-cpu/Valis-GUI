import os.path
import sys
import subprocess
import json
from pathlib import PureWindowsPath, PurePosixPath
from src.core.pyqt_core import *
from src.core.app_config import APP_ROOT, SCRIPTS_PATH
from src.core.validation.platform_retrieval import is_windows_platform
from src.core.validation import is_windows_platform, is_valid_json_file, is_existing_path


class ValisProcessObject(QProcess):
    def __init__(self):
        super().__init__()

        self.process_killed = False

    def start_process(self):
        # implement process logic here
        # check for user platform and reformat running directory as needed, also obtain home dir for use within docker container
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

        # APP_CONFIG is valis_gui_main
        scripts_dir = os.path.join(SCRIPTS_PATH, "valis")  # src/core/scripts/valis
        output_dir = os.path.join(APP_ROOT, *["src", "core", "output", "states"])

        selections_script = os.path.join(scripts_dir, "launch_with_selections.py")
        if not is_existing_path(selections_script):
            print("Error: launch_with_selections.py not found!")
            return

        json_dir = os.path.join(output_dir, "user_settings.json")
        if not is_valid_json_file(json_dir):
            print("Error: user_settings.json not found!")
            return

        img_dir = os.path.join(output_dir, "sample.json")
        if not is_valid_json_file(img_dir):
            print("Error: sample.json not found!")
            return

        selections_script = selections_script.replace(home_dir, '/root')
        json_dir = json_dir.replace(home_dir, '/root')
        img_dir = img_dir.replace(home_dir, '/root')

        self.readyReadStandardOutput.connect(self.handle_output)
        self.readyReadStandardError.connect(self.handle_error)

        # run launchscript.sh with generated arguments
        launch_build = os.path.join(scripts_dir, "launchscript.sh")

        self.setProgram("bash")
        self.setArguments([launch_build, selections_script, json_dir, img_dir, home_dir])
        self.start()

    def handle_output(self):
        output = self.readAllStandardOutput()
        output_str = output.data().decode('utf-8')
        print(output_str)

    def handle_error(self):
        error = self.readAllStandardError()
        error_str = error.data().decode('utf-8')
        print(error_str)

    def kill(self):
        subprocess.run(["docker", "kill", "pyqt_valis_container"])
        self.process_killed = True
        super().kill()
