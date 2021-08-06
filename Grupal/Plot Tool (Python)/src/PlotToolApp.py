from PyQt5.QtWidgets import QMainWindow
from src.ui.designer.PlotToolDesign import PlotTool_MainWindow

class MyApp(QMainWindow, PlotTool_MainWindow):
    def __init__(self, *args, **kwargs):
        # Inicializacion
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        

