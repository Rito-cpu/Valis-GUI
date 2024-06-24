import subprocess

from src.core.pyqt_core import *


class ValisWorker(QObject):
    """PyQt Object class to run subprocess through a QThread.

    Args:
        QObject: 
    """
    finished = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.my_thread = None
    
    class DockerWorker(QThread):
        """Runs a Docker container in a separate thread, allowing for asynchronous execution of commands.

        Args:
            QThread: The base class for threads in PyQT.
        """
        output = pyqtSignal(str)
        error = pyqtSignal(str)

        def __init__(self, command):
            super().__init__()
            self.command = command

        def run(self):
            """Executes the stored command in a subprocess and saves the result.
            """
            try:
                result = subprocess.run(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    self.output.emit(result.stdout)
                else:
                    self.error.emit(result.stderr)
            except Exception as command_error:
                self.error.emit(str(command_error))

    def begin_process(self, docker_path: str, settings_data: dict = None):
        """Not configured yet.

        Args:
            docker_path (str): User defined path to valis docker container instance in users environment.
            settings_data (dict): Contains setting widget states to use for command line.
        """
        if settings_data:
            # Major setting categories
            process_data = settings_data['processing_settings']
            rigid_data = settings_data['rigid_settings']
            non_rigid_settings = settings_data['non_rigid_settings']

            proc_max_size = process_data['maximum_size']
            proc_type = process_data['process_type']
            proc_opt = process_data['options']
            # TODO: How do we handle different data from processing options since it has various attributes?

            rigid_detector = rigid_data['detector']
            rigid_matching_metric = rigid_data['matching_metric']
            rigid_similarity_metric = rigid_data['similarity_metric']
            rigid_image_scaling = rigid_data['image_scaling']
            rigid_maximize_mi = rigid_data['maximize_mi']
            use_non_rigid = rigid_data['use_non_rigid']

            non_rigid_method = non_rigid_settings['method']

            build_command = ["docker", "build", "-t", "docker-test", docker_path]
            print('Building docker container...\n')
            self.my_thread = ValisWorker.DockerWorker(build_command)
            self.my_thread.output.connect(self.on_build_complete)
            self.my_thread.error.connect(self.print_error)
            self.my_thread.start()
        else:
            print('No data given!')

    def on_build_complete(self, output):
        print(output)
        print("Running Docker container...\n")
        self.my_thread = ValisWorker.DockerWorker(["docker", "run", "--rm", "docker-test"])
        self.my_thread.output.connect(self.print_result)
        self.my_thread.error.connect(self.print_error)
        self.my_thread.start()

    def print_result(self, result):
        print(result)
        self.finished.emit(True)

    def print_error(self, error):
        print(error)
