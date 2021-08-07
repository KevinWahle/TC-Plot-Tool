from PyQt5.QtWidgets import QMainWindow
from src.ui.widgets.PlotTool_MainWindow_design import PlotTool_MainWindow_design
from src.ui.widgets.FromFile_Window import FromFile_Window
from src.ui.widgets.H_Window import H_Window
from src.ui.widgets.RespuestaWindow import Respuesta_Window

class PlotToolApp(QMainWindow, PlotTool_MainWindow_design):
    def __init__(self, *args, **kwargs):
        # Inicializacion
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        
        self.verticalWidget_6.setVisible(False)

        self.checkAmplitud.stateChanged.connect(lambda state: self.verticalWidget_7.setVisible(state))
        self.checkFase.stateChanged.connect(lambda state: self.horizontalWidget_6.setVisible(state))
        self.checkRespuesta.stateChanged.connect(lambda state: self.verticalWidget_6.setVisible(state))

        self.btnH.clicked.connect(self.openHWindow)
        self.btnSpice.clicked.connect(self.openFileWindow)
        self.btnRespuesta.clicked.connect(self.openRespWindow)

    def openFileWindow(self):
        # Abrimos la ventana de seleccion de archivo
        fileW = FromFile_Window()
        if(fileW.exec()):   # Vuelve sin error
            #TODO: Graficar
            print("Se cerro SIN error")
        else:
            print("Se cerro CON error")

    def openHWindow(self):
        # Abrimos la ventana de seleccion de archivo
        transFuncW = H_Window()
        if(transFuncW.exec()):   # Vuelve sin error
            #TODO: Graficar
            print("Se cerro SIN error")
        else:
            print("Se cerro CON error")

    def openRespWindow(self):
        # Abrimos la ventana de seleccion de archivo
        respW = Respuesta_Window()
        if(respW.exec()):   # Vuelve sin error
            #TODO: Graficar
            print("Se cerro SIN error")
        else:
            print("Se cerro CON error")
