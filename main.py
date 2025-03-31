#! /usr/bin/python
import sys

from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.scripts.valis.gui_options import *
from src.main_window import MainWindow


if __name__ == '__main__':
    import os
    if hasattr(sys, '_MEIPASS'):
        lib_dir = os.path.join(sys._MEIPASS, '_internal')
        os.environ['DYLD_LIBRARY_PATH'] = lib_dir

    # Create the application
    valis_app = QApplication(sys.argv)
    valis_app.setStyle("fusion")    # Set the look/style of the application

    # Initialize window
    main_window = MainWindow()
    main_window.show()

    # Execute the application
    valis_app.exec()
