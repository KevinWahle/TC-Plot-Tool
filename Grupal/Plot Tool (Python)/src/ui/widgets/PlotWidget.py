# ------------------------------------------------------
# -------------------- PlotWidget.py --------------------
# ------------------------------------------------------
import sys
from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QLineEdit, QWidget, QVBoxLayout

import numpy as np
import scipy.signal as ss

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT

from LabelEditWidget import LabelEditWidget

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #  Create widgets
        self.canvas = FigureCanvas(Figure())
        self.axes = self.canvas.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.labelEdit = LabelEditWidget()


        # self.toolbar.addWidget(self.labelEdit)
        self.toolbar.insertSeparator(self.toolbar.actions()[len(self.toolbar.actions())-1])
        self.toolbar.insertWidget(self.toolbar.actions()[len(self.toolbar.actions())-1], self.labelEdit)

        # self.toolbar.addWidget(QLineEdit())
        # self.toolbar.addWidget(QLineEdit())

        # self.x_input = QLineEdit()
        # self.y_input = QLineEdit()
        # self.x_input.setPlaceholderText("X label")
        # self.y_input.setPlaceholderText("Y label")

        #  Create layout
        # input_layout = QHBoxLayout()
        # input_layout.setContentsMargins(0,0,0,0)

        # input_layout.addWidget(self.x_input)
        # input_layout.addWidget(self.y_input)

        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0,0,0,0)
        vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.canvas)
        # vlayout.addLayout(input_layout)
        # self.toolbar.addWidget(input_layout)

        self.setLayout(vlayout)

        # Connect inputs with on_change method
        self.labelEdit.x_input.textChanged.connect(self._update_label)
        self.labelEdit.y_input.textChanged.connect(self._update_label)

    # Para dibujar directamente
    def plot(self, *args, **kargs):
        self.axes.plot(args, *args, **kargs)

    # Borra los ejes
    def clear(self):
        self.axes.clear()
        self.canvas.draw()

    def drawModule(self, H, *args, freq='rad', **kargs):
        try:

            eje, modulo, fase = ss.bode(H)      # Calculo del Bode (La fase no se usa)

            # Frecuencia en Hertz
            if freq.lower() == 'hertz' or freq.lower() == 'h':
                eje = eje / (2*np.pi)

            # Pasamos a escala logaritmica 
            self.axes.set_xscale('log')
            
            # Agregamos la cuadricula
            self.axes.grid(True)

            # Graficamos
            self.axes.plot(eje, modulo, *args, **kargs)
            self.canvas.draw()

        except:
            print('Error al graficar')

    # Actualiza los valores de los ejes
    def _update_label(self):
        x_label = self.labelEdit.x_input.text()
        y_label = self.labelEdit.y_input.text()

        try:    # Para que no tire error al ingresar algo invalido
            self.axes.set_xlabel(x_label)
            self.axes.set_ylabel(y_label)
            self.canvas.draw()
        except:
            print('Entrada inválida')

        self.drawModule(ss.TransferFunction([1,0,1], [1,4,1]), linestyle='-', linewidth=2)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = PlotWidget()
    w.show()
    sys.exit(app.exec())