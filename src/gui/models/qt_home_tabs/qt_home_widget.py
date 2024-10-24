from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from .qt_new_tab import NewTab
from .qt_saved_settings_tab import SavedSettingsTab


class HomeTabWidget(QTabWidget):
    def __init__(
        self,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

    def _setup_widget(self):
        self._new_tab = NewTab()
        self._saved_settings_tab = SavedSettingsTab()

        self.addTab(self._new_tab, 'New')
        self.addTab(self._saved_settings_tab, 'Use Settings')
        self.setCurrentWidget(self._new_tab)

        self.setTabToolTip(0, "Start New Valis Registration Session")
        self.setTabToolTip(1, "Use Previous Valis Registration Session")
        self.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)

        
