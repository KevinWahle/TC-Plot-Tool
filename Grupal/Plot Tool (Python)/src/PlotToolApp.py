from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from Curve import Curve
from src.ui.widgets.PlotTool_MainWindow_design import PlotTool_MainWindow_design
# from src.ui.widgets.PlotTool_MainWindow_design import PlotTool_MainWindow_design
from src.ui.widgets.FromFile_Window import FromFile_Window
from src.ui.widgets.H_Window import H_Window
from src.ui.widgets.Respuesta_Window import Respuesta_Window

class PlotToolApp(QMainWindow, PlotTool_MainWindow_design):
    def __init__(self, *args, **kwargs):
        # Inicializacion
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.verticalWidget_6.setVisible(False)     # Grafico de Respuesta

        self.checkAmplitud.stateChanged.connect(lambda state: self.verticalWidget_7.setVisible(state))  # Grafico de Modulo
        self.checkFase.stateChanged.connect(lambda state: self.horizontalWidget_6.setVisible(state))    # Grafico de Fase
        self.checkRespuesta.stateChanged.connect(lambda state: self.verticalWidget_6.setVisible(state)) # Grafico de Respuesta


        self.listWidget.itemClicked.connect(self.listItemClicked)

        self.btnH.clicked.connect(self.openHWindow)
        self.btnFiles.clicked.connect(self.openFileWindow)
        self.btnRespuesta.clicked.connect(self.openRespWindow)
        self.btnBorrar.clicked.connect(self.clearFigs)

        self.curves = []
        self.excits = []

    def listItemClicked(self, item):
        item.setCheckState(QtCore.Qt.Checked if item.checkState() != QtCore.Qt.Checked else QtCore.Qt.Unchecked)
        #TODO: Mostrar/Ocultar curvas

    def openHWindow(self):
        # Abrimos la ventana de seleccion de archivo
        transFuncW = H_Window()
        if(transFuncW.exec()):   # Vuelve sin error
            #TODO: Graficar
            # print(transFuncW.name, transFuncW.numArr, transFuncW.denArr)
            Hcurve = Curve(nombre=transFuncW.name, Hnum=transFuncW.numArr, Hden=transFuncW.denArr)
            self.curves.append(Hcurve)

    def openFileWindow(self):
        # Abrimos la ventana de seleccion de archivo
        fileW = FromFile_Window()
        if(fileW.exec()):   # Vuelve sin error
            #TODO: Graficar
            # print(fileW.name, fileW.path, fileW.type)
            pass

    def openRespWindow(self):
        # Abrimos la ventana de seleccion de archivo
        respW = Respuesta_Window()
        if(respW.exec()):   # Vuelve sin error
            #TODO: Graficar
            # print(respW.name, respW.type, respW.amp, respW.freq, respW.freqType)
            pass

    def clearFigs(self):
        self.widgetModulo.clear()
        self.widgetFase.clear()
        self.widgetRespuesta.clear()