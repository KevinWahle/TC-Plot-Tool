from PyQt5.QtWidgets import QMainWindow
from src.ui.widgets.PlotTool_MainWindow import PlotTool_MainWindow

class PlotToolApp(QMainWindow, PlotTool_MainWindow):
    def __init__(self, *args, **kwargs):
        # Inicializacion
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        

