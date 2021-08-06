from PyQt5.QtWidgets import QApplication
import sys
from src.PlotToolApp import PlotToolApp

app = QApplication(sys.argv)
win = PlotToolApp()
win.show()
sys.exit(app.exec())