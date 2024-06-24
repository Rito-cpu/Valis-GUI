#! /usr/bin/python
import sys

from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.scripts.valis.gui_options import *
from src.main_window import MainWindow


if __name__ == '__main__':
    # Create the application
    valis_app = QApplication(sys.argv)
    valis_app.setStyle("fusion")    # Set the look/style of the application

    # os.environ["QT_FONT_DPI"] = str(my_app.primaryScreen().logicalDotsPerInch())

    # Initialize window
    main_window = MainWindow()
    main_window.show()

    # Execute the application
    valis_app.exec()
