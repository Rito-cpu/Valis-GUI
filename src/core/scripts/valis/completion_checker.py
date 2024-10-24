# this file holds the logic for determining the state of the progress bar. The process is defined in a single
# QThread object and run as a thread in progress_bar.py


# processed masks overlaps rigid registration non_rigid_registration data
import os
import time
from src.core.pyqt_core import QThread, pyqtSignal


class ValisMonitoringThread(QThread):
    step_num_signal = pyqtSignal(int)
    step_text_signal = pyqtSignal(str)
    sample_num_signal = pyqtSignal(int)
    sample_text_signal = pyqtSignal(str)

    def __init__(self, path: str, steps_dict: dict, sample_list: list):
        super().__init__()

        self._dst_dir = path
        self._steps_dict = steps_dict
        self._sample_list = sample_list

    def create_flag_file(self, flag_name: str):
        """Creates an empty flag file.

        Args:
            flag_name (str): name of the flag file to use.
        """
        flag_path = os.path.join(self._dst_dir, flag_name)
        with open(flag_path, 'w') as f:
            pass

    def check_flag_file(self, flag_file: str):
        return os.path.exists(flag_file)
    
    def check_previous_run(self):
        start_flag = os.path.join(self._dst_dir, "start.flag")
        complete_flag = os.path.join(self._dst_dir, "complete.flag")

        if self.check_flag_file(start_flag) and not self.check_flag_file(complete_flag):
            # Previous run was interrupted
            # Decide whether to resume, restart, or clean up
            print('Previous run was interrupted!')
            return True
            #user_decision = prompt_user_decision()
            #if user_decision == 'restart':
            #    clean_up_incomplete_run()
            #    start_valis_process()
            #elif user_decision == 'resume':
            #    resume_valis_process()
            #elif user_decision == 'clean':
            #    clean_up_incomplete_run()
        else:
            return False
            #start_valis_process()

    def emit_step_status(self, step_num, step_text):
        # This method will be called by the QThread object to emit the step status to the main window.
        self.step_num_signal.emit(step_num)
        self.step_text_signal.emit(step_text)

    def emit_sample_status(self, sample_num, sample_text):
        # This method will be called by the QThread object to emit the sample status to the main window.
        self.sample_num_signal.emit(sample_num)
        self.sample_text_signal.emit(sample_text)

    def run(self):
        # step iterator: tracks current step for the current valis sample
        # sample iterator: tracks current valis sample
        step_iterator = 0
        sample_iterator = 0

        # create an array with the names of each step selected by the user
        # (passed in from on_register_press.py through progress_bar.py). Also create a list of the sample names.
        step_folders = ["processed", "data"]
        step_folders[-1:-1] = list(self._steps_dict.keys())
        print(f'For this process, we are looking for these step folders:\n{step_folders}')
        # HINT: [processed, rigid, data]
        # max_steps refers to the total number of steps that Valis will do on each sample
        max_steps = len(step_folders)

        # Check for "processed" folder, determines if this is a clean registration or continuing an attempted registration
        if not os.path.exists(f"{self._dst_dir}/{self._sample_list[sample_iterator]}"):
            while sample_iterator < len(self._sample_list):
                current_sample_name = self._sample_list[sample_iterator]
                current_step_name = step_folders[step_iterator]

                self.emit_step_status(step_iterator, current_step_name)
                self.emit_sample_status(sample_iterator, current_sample_name)
                # **************************************************************
                # First step: monitor for the creation of the "processed" folder
                # **************************************************************
                if step_iterator == 0:
                    if os.path.exists(f"{self._dst_dir}/{current_sample_name}/{current_step_name}"):
                        step_iterator += 1
                        self.emit_step_status(step_iterator, step_folders[step_iterator])
                # ***************************************************************************
                # Intermediate steps: monitor for "overlaps" folder creation and its contents
                # ***************************************************************************
                elif step_iterator <= len(self._steps_dict):
                    if os.path.isfile(f"{self._dst_dir}/{current_sample_name}/overlaps/{current_sample_name}_{current_step_name}_overlap.png"):
                        step_iterator += 1
                        self.emit_step_status(step_iterator, step_folders[step_iterator])
                # **********************************************
                # Final step: monitor for "data" folder creation
                # **********************************************
                elif step_iterator < max_steps:
                    print(f'We are in the last step\n\tLooking for: {self._dst_dir}/{current_sample_name}/{current_step_name}')
                    if os.path.exists(f"{self._dst_dir}/{current_sample_name}/{current_step_name}"):
                        self.emit_step_status(step_iterator+1, step_folders[step_iterator])
                        step_iterator = 0
                        sample_iterator += 1
                        self.emit_sample_status(sample_iterator, current_sample_name)
                # While monitoring, wait one second per iteration 
                time.sleep(1)
            print(f'We have just finished the while loop, closing script...')
        else:
            # TODO: If not a clean run

            # this is the loop that will run if the user has attempted or completed a registration prior.
            # this code is dodgy, there are several edge cases for which it might not work (for example,
            # doing a registration after a successful registration followed by a failed one).

            # because registration has already been attempted once before, the first step ("processed" folder) is no
            # longer a good indicator of progress, so it is skipped.
            step_iterator += 1

            # this loop instead starts at step 2, getting the creation time of the next file in the registration process.
            # this will likely break if the user ended their previous registration between creating the
            # "processed" folder and getting to step 1 of registration.
            path = f"{self._dst_dir}/{self._sample_list[sample_iterator]}/overlaps/{self._sample_list[sample_iterator]}_{step_folders[step_iterator]}_overlap.png"
            curr_time = os.path.getctime(path)

            while sample_iterator < len(self._sample_list):
                try:
                    # the try statement is necessary here as the completion checker is constantly searching for
                    # filepaths that may not yet exist (for example, if the user completed a partial registration
                    # before attempting registration once more).

                    if os.path.getmtime(path) != curr_time:
                        # if the modification time of the first file in the overlaps folder does not equal
                        # curr_time (which is None if the file did not previously exist) begin advancing through the
                        # files, updating path and curr_time accordingly.
                        step_iterator += 1
                        self.step_num_signal.emit(step_iterator)
                        if step_iterator == max_steps - 1:
                            self.step_num_signal.emit(max_steps)
                            sample_iterator += 1
                            step_iterator = 1
                            path = f"{self._dst_dir}/{self._sample_list[sample_iterator]}/overlaps/{self._sample_list[sample_iterator]}_{step_folders[step_iterator]}_overlap.png"
                            curr_time = os.path.getctime(path)
                        else:
                            path = f"{self._dst_dir}/{self._sample_list[sample_iterator]}/overlaps/{self._sample_list[sample_iterator]}_{step_folders[step_iterator]}_overlap.png"
                            curr_time = os.path.getmtime(path)
                except FileNotFoundError:
                    # if the loop searches for a file that does not yet exist, it will error and wait one second before
                    # starting again.
                    time.sleep(1)
                    continue
                except IndexError:
                    # when the program tries to go beyond the number of samples specified by the user for registration
                    # (which will happen after the final sample is registered) the loop breaks.
                    break
                time.sleep(1)

"""an alternative that would simplify this whole process would be to insert some kind of checkfile into any 
registration that indicates whether it was failed or completed, and then creating a new folder for following 
registrations if that checkfile is detected so that the completion checker does not need to account for already 
existing files from a previous registration."""