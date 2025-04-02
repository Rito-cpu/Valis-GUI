import os
import os.path
import shutil
import subprocess
import pathlib
import sys
import json

from pathlib import PureWindowsPath, PurePosixPath
from src.core.pyqt_core import *
from src.core.app_config import APP_ROOT, SCRIPTS_PATH, DOCKER_SESSION_CONTAINER
from src.core.json.json_themes import Themes
from src.core.validation.platform_retrieval import is_windows_platform
from src.core.validation import is_windows_platform, is_valid_json_file, is_existing_path
from src.gui.models.qt_message import QtMessage


class ValisProcessObject(QProcess):
    def __init__(
        self,
        dest_dir,
        parent=None
    ):
        super().__init__()

        themes = Themes()
        self.themes = themes.items
        self.dest_dir = dest_dir

        self.process_killed = False

    def start_process(self):
        if is_windows_platform():
            home_dir = str(PurePosixPath(PureWindowsPath(os.path.expanduser("~"))))
        else:
            home_dir = str(pathlib.Path.home())

        # Define paths to key scripts and files
        selections_script = SCRIPTS_PATH / "launch_valis.py"
        local_user_settings = pathlib.Path(self.dest_dir) / "session_settings" / "user_settings.json"
        local_sample_settings = pathlib.Path(self.dest_dir) / "session_settings" / "sample.json"

        # Validate file existence
        if not is_existing_path(selections_script):
            print("Error: launch_valis.py not found!")
            return False
        if not is_valid_json_file(local_user_settings):
            print("Error: user_settings.json not found!")
            return False
        if not is_valid_json_file(local_sample_settings):
            print("Error: sample.json not found!")
            return False

        # Load src_dir from sample.json and resolve it
        with open(local_sample_settings, "r") as f:
            sample_data = json.load(f)
        sample_src_dir = pathlib.Path(sample_data["src_dir"]).expanduser().resolve()

        # Convert all paths to Docker container equivalents
        docker_user_settings = str(local_user_settings).replace(home_dir, "/root")
        docker_sample_settings = str(local_sample_settings).replace(home_dir, "/root")
        docker_script_path = str(selections_script).replace(home_dir, "/root")
        docker_home_dir = home_dir  # still passed as an argument
        docker_output_path = str(self.dest_dir).replace(home_dir, "/root")

        # Connect stdout/stderr handlers
        self.readyReadStandardOutput.connect(self.handle_output)
        self.readyReadStandardError.connect(self.handle_error)

        check = subprocess.run(["docker", "inspect", DOCKER_SESSION_CONTAINER], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check.returncode != 0:
            print("Docker container not found!")
            return False
        else:
            # Run the script inside the existing container
            self.setProgram("docker")
            self.setArguments([
                "exec", DOCKER_SESSION_CONTAINER,
                "python3", "/app/launch_valis.py",
                "-path", docker_user_settings,
                "-il", docker_sample_settings,
                "-hdir", docker_home_dir
            ])

            self.start()
            return True

    def start_process2(self):
        # implement process logic here
        # check for user platform and reformat running directory as needed, also obtain home dir for use within docker container
        # TODO: Configure windows portion
        if is_windows_platform():
            running_dir = pathlib.PureWindowsPath(
                r'C:\Users\80029349\Documents\GUI-Repo\Valis-GUI\src\core\scripts\valis\on_register_press.py').as_posix()
            home_dir = str(PurePosixPath(PureWindowsPath(os.path.expanduser("~"))))
        else:
            running_dir = PurePosixPath(__file__)
            home_dir = str(pathlib.Path.home())
            #home_dir = os.path.expanduser("~")

        # generate paths for necessary files to be passed into docker container, replacing home_dir with "/root"

        #selections_script = scripts_dir / "launch_valis.py"
        #if getattr(sys, 'frozen', False):   # Detects if we are running from pyinstaller package
        #    launch_script = pathlib.Path(sys._MEIPASS) / "src/core/scripts/valis/launch_valis.py"
        #else:
        #    launch_script = SCRIPTS_PATH / "launch_valis.py"

        #if not is_existing_path(selections_script):
        #    print("Error: launch_valis.py not found!")
        #   return

        local_user_settings = pathlib.Path(self.dest_dir) / "session_settings" / "user_settings.json"
        if not is_valid_json_file(local_user_settings):
            print("Error: user_settings.json not found!")
            return

        local_sample_settings = pathlib.Path(self.dest_dir) / "session_settings" / "sample.json"
        if not is_valid_json_file(local_sample_settings):
            print("Error: sample.json not found!")
            return
        with open(local_sample_settings, "r") as f:
            sample_data = json.load(f)
        sample_src_dir = pathlib.Path(sample_data["src_dir"]).expanduser().resolve()
        #print(f'\nFile name:\n{str(launch_script)}')
        #print(f'Is this file real? {launch_script.exists()}\n')

        #launch_script = str(launch_script).replace(home_dir, "/root")
        #local_user_settings = str(local_user_settings).replace(home_dir, "/root")
        #local_sample_settings = str(local_sample_settings).replace(home_dir, "/root")
        docker_user_settings = str(local_user_settings).replace(home_dir, "/root")
        docker_sample_settings = str(local_sample_settings).replace(home_dir, "/root")
        docker_sample_src_dir = str(sample_src_dir).replace(home_dir, "/root")
        docker_output_path = str(self.dest_dir).replace(home_dir, "/root")

        self.readyReadStandardOutput.connect(self.handle_output)
        self.readyReadStandardError.connect(self.handle_error)

        # run launchscript.sh with generated arguments
        launch_build = SCRIPTS_PATH / "launchscript.sh"

        if self.check_docker_running():
            docker_args = [
                "docker", "run", "--rm",
                "--name", "pyqt_valis_container",
                "--memory=20g",
                "--cpus=4",
                "-v", f"{self.dest_dir}:{docker_output_path}:cached",
                "-v", f"{sample_src_dir}:{docker_sample_src_dir}:cached",
                "valis-wsi:dev",
                "-path", docker_user_settings,
                "-il", docker_sample_settings,
                "-hdir", home_dir
            ]
            self.setProgram(docker_args[0])
            self.setArguments(docker_args[1:])
            #self.setProgram("bash")
            #self.setArguments([
            #    str(launch_build),
            #    str(launch_script),
            #    local_user_settings,
            #    local_sample_settings,
            #    home_dir
            #])
            self.start()
            return True
        else:
            return False

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

    def check_docker_running(self):
        error_bttns = {
            "Ok": QMessageBox.ButtonRole.AcceptRole
        }
        error_msg = QtMessage(
            buttons=error_bttns,
            color=self.themes["app_color"]["main_bg"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        error_msg.setIcon(QMessageBox.Icon.Warning)

        # Setup full path to Docker
        docker_cmd = shutil.which("docker")
        
        # If Docker is not found in PATH, try common install locations
        if docker_cmd is None:
            if os.name == "nt":  # Windows
                docker_cmd = r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"
            else:  # macOS/Linux
                docker_cmd = "/usr/local/bin/docker"

        # Final check if Docker command exists
        if not os.path.exists(docker_cmd):
            error_msg.setText('Docker Not Found.')
            error_msg.setDetailedText(f'Please ensure that Docker is installed and accessible in your system PATH.\n\n{e}')
            error_msg.exec()
            return False

        try:
            result = subprocess.run([docker_cmd, "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                # Docker is running
                return True
            else:
                # Docker is not running
                return False
        except Exception as e:
            # Docker command not found (Docker is not installed)
            error_msg.setText('Docker Not Running')
            error_msg.setDetailedText(f'Please ensure that Docker is installed and running.\n\n{e}')
            error_msg.exec()
            return False
