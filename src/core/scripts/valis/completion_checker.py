# this file holds the logic for determining the state of the progress bar. The process is defined in a single
# QThread object and run as a thread in progress_bar.py


# processed masks overlaps rigid registration non_rigid_registration data


import os
import time
from PyQt6.QtCore import QThread, pyqtSignal


class Thread(QThread):
    dir_change = pyqtSignal(int)

    def __init__(self, path: str, steps_dict: dict, sample_list: list):
        super().__init__()
        self.path = path
        self.steps_dict = steps_dict
        self.sample_list = sample_list

    def run(self):

        # max_steps refers to the total number of steps that Valis will do on each sample
        max_steps = 2 + len(self.steps_dict)

        # step iterator will be used to keep track of what step Valis is on for each sample,
        # sample iterator will keep track of which sample it is on.
        step_iterator = 0
        sample_iterator = 0

        # create an array with the names of each step selected by the user
        # (passed in from on_register_press.py through progress_bar.py). Also create a list of the sample names.
        folder_array = ["processed", "data"]
        folder_array[-1:-1] = list(self.steps_dict.keys())
        sample_names = self.sample_list

        # check to see if the first step of registration ("processed" folder) has been created,
        # effectively determining if registration has already been attempted once before.
        if not os.path.exists(f"{self.path}/{sample_names[sample_iterator]}"):
            # if registration has not been attempted, this loop will be used,
            while sample_iterator < len(sample_names):
                # for the first step, check if the "processed" folder has been created before advancing.
                if step_iterator == 0:
                    if os.path.exists(f"{self.path}/{sample_names[sample_iterator]}/{folder_array[step_iterator]}"):
                        step_iterator += 1
                        self.dir_change.emit(step_iterator)
                # for the following steps, check the "overlaps" folder for the correct files that indicate
                # when a step has been completed.
                elif step_iterator <= len(self.steps_dict):
                    if os.path.isfile(
                            f"{self.path}/{sample_names[sample_iterator]}/overlaps/{sample_names[sample_iterator]}_{folder_array[step_iterator]}_overlap.png"):
                        step_iterator += 1
                        self.dir_change.emit(step_iterator)
                # when step_iterator reaches the final step, check for the "data" folder before advancing
                # sample_iterator and resetting step_iterator back to 0
                elif step_iterator < max_steps:
                    if os.path.exists(f"{self.path}/{sample_names[sample_iterator]}/{folder_array[step_iterator]}"):
                        step_iterator += 1
                        self.dir_change.emit(step_iterator)
                        step_iterator = 0
                        sample_iterator += 1
                # on every run of the loop, wait one second before going back through
                time.sleep(1)
        else:

            # this is the loop that will run if the user has attempted or completed a registration prior.
            # this code is dodgy, there are several edge cases for which it might not work (for example,
            # doing a registration after a successful registration followed by a failed one).

            # because registration has already been attempted once before, the first step ("processed" folder) is no
            # longer a good indicator of progress, so it is skipped.
            step_iterator += 1

            # this loop instead starts at step 2, getting the creation time of the next file in the registration process.
            # this will likely break if the user ended their previous registration between creating the
            # "processed" folder and getting to step 1 of registration.
            path = f"{self.path}/{sample_names[sample_iterator]}/overlaps/{sample_names[sample_iterator]}_{folder_array[step_iterator]}_overlap.png"
            curr_time = os.path.getctime(path)

            while sample_iterator < len(sample_names):
                try:
                    # the try statement is necessary here as the completion checker is constantly searching for
                    # filepaths that may not yet exist (for example, if the user completed a partial registration
                    # before attempting registration once more).

                    if os.path.getmtime(path) != curr_time:
                        # if the modification time of the first file in the overlaps folder does not equal
                        # curr_time (which is None if the file did not previously exist) begin advancing through the
                        # files, updating path and curr_time accordingly.
                        step_iterator += 1
                        self.dir_change.emit(step_iterator)
                        if step_iterator == max_steps - 1:
                            self.dir_change.emit(max_steps)
                            sample_iterator += 1
                            step_iterator = 1
                            path = f"{self.path}/{sample_names[sample_iterator]}/overlaps/{sample_names[sample_iterator]}_{folder_array[step_iterator]}_overlap.png"
                            curr_time = os.path.getctime(path)
                        else:
                            path = f"{self.path}/{sample_names[sample_iterator]}/overlaps/{sample_names[sample_iterator]}_{folder_array[step_iterator]}_overlap.png"
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