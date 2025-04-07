import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class QtMplCanvas(FigureCanvasQTAgg):
    def __init__(
        self,
        error_data: dict,
        parent=None
    ):
        fig, ax = plt.subplots()
        super().__init__(fig)
        if parent is not None:
            self.setParent(parent)

        print(f'\nThis is the error dict: {error_data}')
        sample_names = list(error_data.keys())
        errors = list(error_data.values())
        print(f'Sample names: {sample_names}')
        print(f'Errors: {errors}\n')

        ax.bar(sample_names, errors)
        ax.set_title("Registration Error per Sample")
        ax.set_ylabel("Error (D)")
        ax.set_xlabel("Sample Name")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        fig.tight_layout()

    def set_dpi(self, dpi: int):
        self.figure.set_dpi(dpi)
