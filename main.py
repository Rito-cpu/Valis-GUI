#! /usr/bin/python
import sys

from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.scripts.valis.gui_options import *
from src.main_window import MainWindow


if __name__ == '__main__':
    # Create the application right here
    valis_app = QApplication(sys.argv)

    # os.environ["QT_FONT_DPI"] = str(my_app.primaryScreen().logicalDotsPerInch())

    valis_app.setStyle("macOS")

    # icon_loc = os.path.abspath(os.path.join(PROJ_ROOT, "coe_blue.ico"))
    # valis_app.setWindowIcon(QIcon(icon_loc))

    main_window = MainWindow()
    main_window.show()

    valis_app.exec()
