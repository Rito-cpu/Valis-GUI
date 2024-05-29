import os

from src.core.pyqt_core import *
from src.core.keyword_store import PENDING_S, CONVERTING_S, COMPLETE_S


# **** Results Test Objects ****

class ResultsObj:
    status: str = "Finished alignment"
    sample_id: str

    def __init__(self, new_id: str):
        self.sample_id = new_id

    def set_status(self, new_status: str):
        self.status = new_status

results_obj_1 = ResultsObj('1')
results_obj_1.set_status(COMPLETE_S)

results_obj_2 = ResultsObj('2')
results_obj_2.set_status(CONVERTING_S)

results_obj_3 = ResultsObj('3')
results_obj_3.set_status(PENDING_S)
results_table_list = [results_obj_1, results_obj_2, results_obj_3]

# **** Export Test Objects  ****
class ExportObj:
    sample_id: str
    to_export: bool = True
    path_to_non_rigid_reg: str
    rigid_complete: bool = False
    non_rigid_complete: bool = False
    do_non_rigid: bool = False

    def __init__(self, id, path):
        self.sample_id = id
        self.path_to_non_rigid_reg = path

    def set_to_export(self, export):
        self.to_export = export

    def set_rigid_complete(self, complete):
        self.rigid_complete = complete

    def set_non_rigid_complete(self, complete):
        self.non_rigid_complete = complete

    def perform_non_rigid(self, perform):
        self.do_non_rigid = perform

export_obj_1 = ExportObj('One', '/Users/4474613/Documents')
export_obj_2 = ExportObj('Two', '/Users/4474613/Documents')
export_obj_3 = ExportObj('Three', '/Users/4474613/Documents')
export_obj_4 = ExportObj('Four', '/Users/4474613/Documents')
export_obj_data = [export_obj_1, export_obj_2, export_obj_3, export_obj_4]
