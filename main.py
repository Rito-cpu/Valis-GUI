#! /usr/bin/python
import sys
import subprocess

from pathlib import Path
from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.scripts.valis.gui_options import *
from src.main_window import MainWindow


def start_docker_container():
    home_dir = Path.home()
    output_mount = home_dir  # You can refine this if you want to mount a subfolder

    # Check if a container with the name exists (even if stopped)
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.Image}}", DOCKER_SESSION_CONTAINER],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    if result.returncode == 0:
        container_image_id = result.stdout.strip()
        # Get the image ID of the current app image
        image_id_result = subprocess.run(
            ["docker", "images", "--no-trunc", "--quiet", DOCKER_GUI_IMAGE],
            stdout=subprocess.PIPE,
            text=True
        )
        current_image_id = image_id_result.stdout.strip()

        if container_image_id != current_image_id:
            print(f"Outdated container detected. Removing {DOCKER_SESSION_CONTAINER}...")
            subprocess.run(["docker", "rm", "-f", DOCKER_SESSION_CONTAINER])
        else:
            print("Container already exists and uses latest image.")
            return

    # Run the container in detached mode
    docker_command = [
        "docker", "run", "-d",
        "--name", DOCKER_SESSION_CONTAINER,
        "--memory=16g",
        "--cpus=4",
        "-v", f"{str(output_mount)}:/root:cached",
        DOCKER_GUI_IMAGE,
        "tail", "-f", "/dev/null"
    ]

    try:
        subprocess.run(docker_command, check=True)
        print("Docker container started in detached mode.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Docker container: {e}")


if __name__ == '__main__':
    import os
    if hasattr(sys, '_MEIPASS'):
        lib_dir = os.path.join(sys._MEIPASS, '_internal')
        os.environ['DYLD_LIBRARY_PATH'] = lib_dir

    start_docker_container()

    # Create the application
    valis_app = QApplication(sys.argv)
    valis_app.setStyle("fusion")    # Set the look/style of the application

    # Initialize window
    main_window = MainWindow()
    main_window.show()

    # Execute the application
    valis_app.exec()
