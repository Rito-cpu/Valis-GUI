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

    '''def run(self):
        max_steps = 2 + len(self.steps_dict)
        step_iterator = 0
        sample_iterator = 0
        folder_array = ["processed", "data"]
        folder_array[-1:-1] = list(self.steps_dict.keys())
        print(folder_array)

        sub_path = self.path
        sample_names = self.sample_list

        while sample_iterator < len(sample_names):
            if os.path.exists(f"{sub_path}/{sample_names[sample_iterator]}/{folder_array[step_iterator]}"):
                step_iterator += 1
                self.dir_change.emit(step_iterator)
            if step_iterator == max_steps:
                step_iterator = 0
                sample_iterator += 1
            time.sleep(1)'''

    def run(self):
        max_steps = 2 + len(self.steps_dict)
        step_iterator = 0
        sample_iterator = 0
        folder_array = ["processed", "data"]
        folder_array[-1:-1] = list(self.steps_dict.keys())
        sample_names = self.sample_list

        if not os.path.exists(f"{self.path}/{sample_names[sample_iterator]}"):
            while sample_iterator < len(sample_names):
                if step_iterator == 0:
                    if os.path.exists(f"{self.path}/{sample_names[sample_iterator]}/{folder_array[step_iterator]}"):
                        step_iterator += 1
                        self.dir_change.emit(step_iterator)
                elif step_iterator <= len(self.steps_dict):
                    if os.path.isfile(
                            f"{self.path}/{sample_names[sample_iterator]}/overlaps/{sample_names[sample_iterator]}_{folder_array[step_iterator]}_overlap.png"):
                        step_iterator += 1
                        self.dir_change.emit(step_iterator)
                elif step_iterator < max_steps:
                    if os.path.exists(f"{self.path}/{sample_names[sample_iterator]}/{folder_array[step_iterator]}"):
                        step_iterator += 1
                        self.dir_change.emit(step_iterator)
                        step_iterator = 0
                        sample_iterator += 1
                time.sleep(1)
        else:
            step_iterator += 1
            path = f"{self.path}/{sample_names[sample_iterator]}/overlaps/{sample_names[sample_iterator]}_{folder_array[step_iterator]}_overlap.png"
            curr_time = os.path.getctime(path)
            while sample_iterator < len(sample_names):
                try:
                    if os.path.getmtime(path) != curr_time:
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
                    time.sleep(1)
                    continue
                except IndexError:
                    break
                time.sleep(1)
