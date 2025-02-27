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

    # Get the correct libvips library path for Homebrew
    #vips_lib_dir = "/opt/homebrew/lib"

    # If using Python 3.8+, use add_dll_directory
    #add_dll_dir = getattr(os, "add_dll_directory", None)
    #if callable(add_dll_dir):
    #    add_dll_dir(vips_lib_dir)
    #else:
    #    os.environ["DYLD_LIBRARY_PATH"] = os.pathsep.join((vips_lib_dir, os.environ.get("DYLD_LIBRARY_PATH", "")))

    # Create the application
    valis_app = QApplication(sys.argv)
    valis_app.setStyle("fusion")    # Set the look/style of the application

    # os.environ["QT_FONT_DPI"] = str(my_app.primaryScreen().logicalDotsPerInch())

    # Initialize window
    main_window = MainWindow()
    main_window.show()

    # Execute the application
    valis_app.exec()
