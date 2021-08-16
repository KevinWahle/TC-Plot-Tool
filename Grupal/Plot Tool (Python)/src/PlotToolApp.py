from Excitation import Excitation
from PyQt5 import QtCore
from PyQt5.QtWidgets import QListView, QListWidgetItem, QMainWindow
from Curve import Curve, graphCurves
from src.ui.widgets.PlotTool_MainWindow_design import PlotTool_MainWindow_design
# from src.ui.widgets.PlotTool_MainWindow_design import PlotTool_MainWindow_design
from src.ui.widgets.FromFile_Window import FromFile_Window
from src.ui.widgets.H_Window import H_Window
from src.ui.widgets.Respuesta_Window import Respuesta_Window

from fileReader import *
class PlotToolApp(QMainWindow, PlotTool_MainWindow_design):
    def __init__(self, *args, **kwargs):
        # Inicializacion
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.verticalWidget_6.setVisible(False)     # Grafico de Respuesta

        self.checkAmplitud.stateChanged.connect(lambda state: self.verticalWidget_7.setVisible(state))  # Grafico de Modulo
        self.checkFase.stateChanged.connect(lambda state: self.horizontalWidget_6.setVisible(state))    # Grafico de Fase
        self.checkRespuesta.stateChanged.connect(lambda state: self.verticalWidget_6.setVisible(state)) # Grafico de Respuesta

        self.buttonGroup.buttonClicked.connect(self.updateGraphs)   # Cambio de escala de frecuencia

        # self.listWidget.setMovement(QListView.Free)
        # self.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        # self.listWidget2.setMovement(QListView.Free)
        # self.listWidget2.setDefaultDropAction(QtCore.Qt.MoveAction)

        # Toggle check al hacer doble click
        self.listWidget.itemDoubleClicked.connect(self.toggleItem)
        self.listWidget2.itemDoubleClicked.connect(self.toggleItem)
        # Actualizar al cambiar nombre o visibilidad
        self.listWidget.itemChanged.connect(self.curveItemChanged)
        self.listWidget2.itemChanged.connect(self.excitItemChanged)

        self.delBtn1.clicked.connect(self.removeCurrentCurve)
        self.delBtn2.clicked.connect(self.removeCurrentExcit)

        self.btnH.clicked.connect(self.openHWindow)
        self.btnFiles.clicked.connect(self.openFileWindow)
        self.btnRespuesta.clicked.connect(self.openRespWindow)
        self.btnBorrar.clicked.connect(self.clearAll)

        # Ecitation and Curve arrays
        self.curves = []
        self.excits = []

    def toggleItem(self, item):
        item.setCheckState(QtCore.Qt.Checked if item.checkState() != QtCore.Qt.Checked else QtCore.Qt.Unchecked)

    def curveItemChanged(self, item):
        index = self.listWidget.row(item)
        
        # Cambio el nombre o la visibilidad, actualizo las curvas
        self.curves[index].nombre = item.text()
        self.curves[index].visibility = item.checkState() == QtCore.Qt.Checked
        # TODO: updateCurves()
        self.updateGraphs()

    def excitItemChanged(self, item):
        index = self.listWidget2.row(item)
        
        # Cambio el nombre o la visibilidad, actualizo las curvas
        self.excits[index].name = item.text()
        self.excits[index].visibility = item.checkState() == QtCore.Qt.Checked
        self.updateGraphs()

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
        self.updateGraphs()

    def updateGraphs(self):
        self.widgetModulo.clear()
        self.widgetFase.clear()
        self.widgetRespuesta.clear()

        self.widgetModulo.axes.set_xscale('log') 
        self.widgetFase.axes.set_xscale('log') 

        axes = [self.widgetModulo.axes, self.widgetFase.axes, self.widgetRespuesta.axes]
        graphCurves(curves=self.curves, axes=axes, exitaciones = self.excits, frec=self.radioButtonW.isChecked())

        self.widgetModulo.draw()
        self.widgetFase.draw()
        self.widgetRespuesta.draw()
        

    def addExcitation(self, excit):
        # Add to Excitaction array
        self.excits.append(excit)

        # Add to excitation list
        item = QListWidgetItem(excit.name)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked if excit.visibility else QtCore.Qt.Unchecked)
        self.listWidget2.addItem(item)

        # Redraw response
        self.updateGraphs()
        

    def openHWindow(self):        
        while(True):
            try:
                # Abrimos la ventana de seleccion de archivo
                transFuncW = H_Window()
                if(transFuncW.exec()):   # Vuelve sin error
                    # print(transFuncW.name, transFuncW.numArr, transFuncW.denArr)
                    Hcurve = Curve(nombre=transFuncW.name, Hnum=transFuncW.numArr, Hden=transFuncW.denArr)
                    self.addCurve(Hcurve)
                break
            except:
                pass


    def openFileWindow(self):
        while(True):
            try:
                # Abrimos la ventana de seleccion de archivo
                fileW = FromFile_Window()
                if(fileW.exec()):   # Vuelve sin error
                    # print(fileW.name, fileW.path, fileW.type)
                    fileCurve = Curve(nombre=fileW.name, path=fileW.path, modo=fileW.type)
                    self.addCurve(fileCurve)
                break
            except:
                pass

    def openRespWindow(self):
        while(True):
            try:
                # Abrimos la ventana de generacion de la excitacion
                respW = Respuesta_Window()
                if(respW.exec()):   # Vuelve sin error
                    # print(respW.name, respW.type, respW.amp, respW.freq, respW.freqType, resp.duty)
                    excit = Excitation(name=respW.name, type=respW.type, amp=respW.amp, freq=respW.freq,    \
                                        freqType=respW.freqType, duty=respW.duty, path=respW.path)
                    self.addExcitation(excit)
                break
            except:
                pass

    def removeCurrentCurve(self):
        index = self.listWidget.currentRow()
        if index >= 0:
            self.listWidget.removeItemWidget(self.listWidget.takeItem(index))
            self.curves.pop(index)
            self.updateGraphs()

    def removeCurrentExcit(self):
        index = self.listWidget2.currentRow()
        if index >= 0:
            self.listWidget2.removeItemWidget(self.listWidget2.takeItem(index))
            self.excits.pop(index)
            self.updateGraphs()

    def clearAll(self):
        self.curves = []
        self.excits = []
        self.clearFigs()

    def clearFigs(self):
        self.listWidget.clear()
        self.listWidget2.clear()

        self.widgetModulo.clear()
        self.widgetFase.clear()
        self.widgetRespuesta.clear()