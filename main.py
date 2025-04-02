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
        ["docker", "ps", "-a", "--filter", f"name={DOCKER_SESSION_CONTAINER}", "--format", "{{.Status}}"],
        stdout=subprocess.PIPE,
        text=True
    )

    if result.stdout:
        print(f"Found a leftover container: {DOCKER_SESSION_CONTAINER}. Removing...")
        subprocess.run(["docker", "rm", "-f", DOCKER_SESSION_CONTAINER])

    # Check if container is already running
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", DOCKER_SESSION_CONTAINER],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip() == "true":
            print("Docker container is already running.")
            return
    except Exception as e:
        print(f"Error checking container: {e}")
        return
    
    # Run the container in detached mode if not already running
    docker_command = [
        "docker", "run", "-d",
        "--name", DOCKER_SESSION_CONTAINER,
        "--memory=16g",
        "--cpus=4",
        "-v", f"{str(output_mount)}:/root:cached",
        "valis-wsi:dev",
        "tail", "-f", "/dev/null"  # Keep the container alive
    ]

    try:
        subprocess.run(docker_command, check=True)
        print("Docker container started in detached mode.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Docker container: {e}")
        return


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
