from PyQt5.QtWidgets import QApplication
from src.ui.widgets.PlotWidget import PlotWidget
import sys

app = QApplication(sys.argv)
win = PlotWidget()
win.show()
sys.exit(app.exec())