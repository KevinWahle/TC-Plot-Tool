from Excitation import Excitation
from PyQt5 import QtCore
from PyQt5.QtWidgets import QListView, QListWidgetItem, QMainWindow
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

        # self.listWidget.setMovement(QListView.Free)
        # self.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        # self.listWidget2.setMovement(QListView.Free)
        # self.listWidget2.setDefaultDropAction(QtCore.Qt.MoveAction)

        self.listWidget.itemClicked.connect(self.listItemClicked)
        self.listWidget2.itemClicked.connect(self.listItemClicked)
        # self.listWidget.itemChanged.connect(self.curveItemChanged)

        self.btnH.clicked.connect(self.openHWindow)
        self.btnFiles.clicked.connect(self.openFileWindow)
        self.btnRespuesta.clicked.connect(self.openRespWindow)
        self.btnBorrar.clicked.connect(self.clearFigs)

        # Ecitation and Curve arrays
        self.curves = []
        self.excits = []

    def listItemClicked(self, item):
        item.setCheckState(QtCore.Qt.Checked if item.checkState() != QtCore.Qt.Checked else QtCore.Qt.Unchecked)
        #TODO: Mostrar/Ocultar curvas

    def curveItemChanged(self, item):
        index = self.listWidget.row(item)
        if self.curves[index].name != item.text():
            self.curves[index].name = item.text()
            #TODO: updateCurves()

    # def updateCurvesList(self):
    #     # Update curves list
    #     self.listWidget.clear()
    #     for curve in self.cuves:
    #         item = QListWidgetItem(text=curve.name)
    #         item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
    #         item.setCheckState(QtCore.Qt.Checked if curve.visibility else QtCore.Qt.Unchecked)
    #         self.listWidget.addItem(item)

    def addCurve(self, curve):
        # Add to curve array
        self.curves.append(curve)

        # Add to curve list
        item = QListWidgetItem(curve.nombre)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked if curve.visibility else QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)

        # Redraw curves
        #TODO: drawCurves()

    def addExcitation(self, excit):
        # Add to Excitaction array
        self.excits.append(excit)

        # Add to excitation list
        item = QListWidgetItem(excit.name)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked if excit.visibility else QtCore.Qt.Unchecked)
        self.listWidget2.addItem(item)

        # Redraw response
        #TODO: drawCurves() / drawResp()
        

    def openHWindow(self):
        # Abrimos la ventana de seleccion de archivo
        transFuncW = H_Window()
        if(transFuncW.exec()):   # Vuelve sin error
            # print(transFuncW.name, transFuncW.numArr, transFuncW.denArr)
            Hcurve = Curve(nombre=transFuncW.name, Hnum=transFuncW.numArr, Hden=transFuncW.denArr)
            self.addCurve(Hcurve)

    def openFileWindow(self):
        # Abrimos la ventana de seleccion de archivo
        fileW = FromFile_Window()
        if(fileW.exec()):   # Vuelve sin error
            # print(fileW.name, fileW.path, fileW.type)
            fileCurve = Curve(nombre=fileW.name, path=fileW.path, modo=fileW.type)
            self.addCurve(fileCurve)

    def openRespWindow(self):
        # Abrimos la ventana de seleccion de archivo
        respW = Respuesta_Window()
        if(respW.exec()):   # Vuelve sin error
            # print(respW.name, respW.type, respW.amp, respW.freq, respW.freqType, resp.duty)
            excit = Excitation(name=respW.name, type=respW.type, amp=respW.amp, freq=respW.freq,    \
                                freqType=respW.freqType, duty=respW.duty)
            self.addExcitation(excit)


    def clearFigs(self):
        self.widgetModulo.clear()
        self.widgetFase.clear()
        self.widgetRespuesta.clear()