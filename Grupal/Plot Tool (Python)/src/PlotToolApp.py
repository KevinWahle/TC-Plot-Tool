from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidgetItem, QMainWindow
from src.ui.widgets.MainWindow_design import MainWindow_design
from src.ui.widgets.FromFile_Window import FromFile_Window
from src.ui.widgets.H_Window import H_Window
from src.ui.widgets.Respuesta_Window import Respuesta_Window

from src.NewCurve import ExcitCurve, FileCurve, TFCurve

class PlotToolApp(QMainWindow, MainWindow_design):
    def __init__(self, *args, **kwargs):
        # Inicializacion
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.verticalWidget_6.setVisible(False)     # Grafico de Respuesta

        self.checkAmplitud.stateChanged.connect(lambda state: self.verticalWidget_7.setVisible(state))  # Grafico de Modulo
        self.checkFase.stateChanged.connect(lambda state: self.horizontalWidget_6.setVisible(state))    # Grafico de Fase
        self.checkRespuesta.stateChanged.connect(lambda state: self.verticalWidget_6.setVisible(state)) # Grafico de Respuesta

        # Cambio de unidad (rad/s - Hz)
        self.buttonGroup.buttonClicked.connect(self.updateGraphs)

        # Cambio de escala (lineal - logaritmica)
        self.freqTypeGroup.buttonClicked.connect(self.updateGraphs)

        # self.listWidget.setMovement(QListView.Free)
        # self.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        # self.listWidget2.setMovement(QListView.Free)
        # self.listWidget2.setDefaultDropAction(QtCore.Qt.MoveAction)

        # Toggle check al hacer doble click
        # TODO: Cambiar por edit de la curva
        # self.listWidget.itemDoubleClicked.connect(self.toggleItem)
        # self.listWidget2.itemDoubleClicked.connect(self.toggleItem)

        # Actualizar al cambiar nombre o visibilidad
        self.listWidget.itemChanged.connect(self.curveItemChanged)
        self.listWidget2.itemChanged.connect(self.excitItemChanged)

        self.delBtn1.clicked.connect(self.removeCurrentCurve)
        self.delBtn2.clicked.connect(self.removeCurrentExcit)

        self.btnH.clicked.connect(self.openHWindow)
        self.btnFiles.clicked.connect(self.openFileWindow)
        self.btnRespuesta.clicked.connect(self.openRespWindow)
        self.btnBorrar.clicked.connect(self.clearAll)

        # Axes array
        self.axes = [self.widgetModulo.axes, self.widgetFase.axes, self.widgetRespuesta.axes]

        # Ecitation and Curve arrays
        self.curves = []
        self.excits = []

        self.units = self.getUnits()

        self.initGraphs()

    def getUnits(self):
        return 'Hz' if self.radioButtonF.isChecked() else 'rads'

    def initGraphs(self):

        self.axes[0].grid(which='both', zorder=0)
        self.axes[0].set_axisbelow(True)

        self.axes[1].grid(which='both', zorder=0)
        self.axes[1].set_axisbelow(True)

        self.axes[2].grid(which='both', zorder=0)
        self.axes[2].set_axisbelow(True)

        self.updateGraphs()

    def updateGraphs(self):

        self.updateGraphsXScale()

        self.updateGraphsXUnits()

        self.updateGraphsLegends()

        self.widgetModulo.draw()
        self.widgetFase.draw()
        self.widgetRespuesta.draw()

    
    def updateGraphsXScale(self):
        xscale = 'log' if self.freqLogRbtn.isChecked() else 'linear'
        self.axes[0].set_xscale(xscale) 
        self.axes[1].set_xscale(xscale)
        self.axes[2].set_xscale('linear')

    def updateGraphsXUnits(self):
        self.units = self.getUnits()

        for curve in self.curves:
            curve.setXUnits(self.units)

    def updateGraphsLegends(self):

        # Gráficos de frecuencia

        # Revisa si estan creados los legends
        anyLegend = any(ax.get_legend() is not None for ax in self.axes[0:2])

        # Solo mostrar los legends si hay una curva visible
        anyCurve = any(curve.visibility for curve in self.curves)
        
        # TODO: Ver de reemplazar los anyCurve con una funcion que devuelva los labels o las curvas
        # para no mostrar los legends de las ocultas y poder ver las que empiezan con '_'
        # Referencia: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html (3)

        if anyCurve:           # Actualiza legend si hay algo para mostrar (para evitar warning)
            self.axes[0].legend()
            self.axes[1].legend()

        if anyLegend:           # Si hay legend, actualizo visibilidad
            self.axes[0].get_legend().set_visible(anyCurve)
            self.axes[1].get_legend().set_visible(anyCurve)

        # Graficos de tiempo

        timeLegend = self.axes[2].get_legend()
        anyExcit = any(excit.visibility for excit in self.excits)
        if anyExcit:
            self.axes[2].legend()
        if timeLegend:
            self.axes[2].get_legend().set_visible(anyExcit)


    # def toggleItem(self, item):
    #     item.setCheckState(QtCore.Qt.Checked if item.checkState() != QtCore.Qt.Checked else QtCore.Qt.Unchecked)


    def curveItemChanged(self, item):
        index = self.listWidget.row(item)
        
        # Cambio el nombre o la visibilidad, actualizo las curvas
        self.curves[index].setName(item.text())
        self.curves[index].setVisible(item.checkState() == QtCore.Qt.Checked)
        self.updateGraphs()

    def excitItemChanged(self, item):
        index = self.listWidget2.row(item)
        
        # Cambio el nombre o la visibilidad, actualizo las curvas
        self.excits[index].setName(item.text())
        self.excits[index].setVisible(item.checkState() == QtCore.Qt.Checked)
        self.updateGraphs()

    def openHWindow(self):        
        while(True):
            try:
                # Abrimos la ventana de seleccion de archivo
                transFuncW = H_Window()
                if(transFuncW.exec()):   # Vuelve sin error
                    # print(transFuncW.name, transFuncW.numArr, transFuncW.denArr)
                    # Hcurve = Curve(nombre=transFuncW.name, Hnum=transFuncW.numArr, Hden=transFuncW.denArr)
                    Hcurve = TFCurve(name=transFuncW.name, Hnum=transFuncW.numArr, Hden=transFuncW.denArr,      \
                                    freqRange=transFuncW.freqRange, logscale=transFuncW.logscale, axes=self.axes, \
                                    plotUnits=self.units)
                    self.addCurve(Hcurve)
                break
            except Exception as e:
                print(e)


    def openFileWindow(self):
        while(True):
            # try:
                # Abrimos la ventana de seleccion de archivo
                fileW = FromFile_Window()
                if(fileW.exec()):   # Vuelve sin error
                    # print(fileW.name, fileW.path, fileW.type)
                    fileCurve = FileCurve(name=fileW.name, path=fileW.path, mode=fileW.type, axes=self.axes, \
                                            freqUnits='Hz', plotUnits=self.units)
                    self.addCurve(fileCurve)
                break
            # except Exception as e:
            #     print(e)

    def openRespWindow(self):
        while(True):
            # try:
                # Abrimos la ventana de generacion de la excitacion
                respW = Respuesta_Window()
                if(respW.exec()):   # Vuelve sin error
                    # print(respW.name, respW.type, respW.amp, respW.freq, respW.freqType, resp.duty)
                    excit = ExcitCurve(name=respW.name, axes=self.axes, type=respW.type, amp=respW.amp, freq=respW.freq,    \
                                        freqType=respW.freqType, duty=respW.duty, path=respW.path)
                    self.addExcitation(excit)
                break
            # except Exception as e:
            #     print(e)

    def addCurve(self, curve):
        # Add to curve array
        self.curves.append(curve)

        # Add to curve list
        item = QListWidgetItem(curve.name)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked if curve.visibility else QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)

        # Redraw curves
        self.updateGraphs()


    def addExcitation(self, excit):
        # Add to Excitaction array
        self.excits.append(excit)

        for curve in self.curves:
            if isinstance(curve, TFCurve):  # Solo si es una curva de transferencia
                curve.addResponse(excit, self.axes)

        # Add to excitation list
        item = QListWidgetItem(excit.name)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked if excit.visibility else QtCore.Qt.Unchecked)
        self.listWidget2.addItem(item)

        # Redraw response
        self.updateGraphs()


    def removeCurrentCurve(self):
        index = self.listWidget.currentRow()
        if index >= 0:
            self.listWidget.removeItemWidget(self.listWidget.takeItem(index))
            self.curves[index].delete()
            self.curves.pop(index)
            self.updateGraphs()

    def removeCurrentExcit(self):
        index = self.listWidget2.currentRow()
        if index >= 0:
            self.listWidget2.removeItemWidget(self.listWidget2.takeItem(index))
            self.excits.pop(index)
            self.updateGraphs()

    def clearAll(self):

        for curve in self.curves:
            curve.delete()

        for excit in self.excits:
            excit.delete()

        self.curves.clear()
        self.excits.clear()
        self.clearFigs()

    def clearFigs(self):
        self.listWidget.clear()
        self.listWidget2.clear()

        self.widgetModulo.clear()
        self.widgetFase.clear()
        self.widgetRespuesta.clear()