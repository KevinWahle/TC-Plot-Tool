from scipy.signal.ltisys import TransferFunction
from spice import *
class Curve:

    # Modo: 0  frecuencia | Moduulo | Fase
    #       1  tiempo | Magnitud
    def __init__(self, nombre, Hnum="", Hden="", path='', modo=0):
        self.nombre = nombre
        self.path = path
        self.visibility = True
        self.modo = modo

        if Hnum != "" and Hden != "":
            self.H = getTransfFunct(Hnum, Hden)
            self.data = getDataTeorica(self.H)
            self.trazo = "dotted"

        if ".txt" in path:
            self.H=0
            self.data = getDataSimulation(path, modo)
            self.trazo = "solid"

        elif ".csv" in path:
            self.H=0
            self.data = getDataMediciones(path, modo)
            self.trazo= "dashdot"


    def calcRta(self, exitacion):

        if exitacion.type == 0:                      # escalon
            t, y = ss.step((self.H.num, self.H.den))        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.step.html#scipy.signal.step
            y = y * exitacion.amp
        elif exitacion.type == 1:                    # senoidal
            tin,seno =exitacion.getValues()
            t, y,  = ss.lsim((self.H.num, self.H.den), U=seno, T=tin)  # Calculamos la Rta
        
        elif exitacion.type == 2:                    # impulso
            t, y = ss.impulse((self.H.num, self.H.den))     #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.impulse.html#scipy.signal.impulse

        elif exitacion.type == 3:                    # cuadrada
            tin,cuadrada =exitacion.getValues()
            t, y,  = ss.lsim((self.H.num, self.H.den), U=cuadrada, T=tin) # Calculamos la Rta

        #else:
        # Cargar archivo de exitación. 

        self.data["time"].append(t)   # Guardamos el arreglo temporal
        self.data["y"].append(y)      # Guardamos el arreglo Y

    def graphCurve(self, axes=[], cIndex=0):  # axes = [ModuleAxis, PhaseAxis, ResponseAxis]

        if self.visibility == True:
            for index in range(len(self.data["frec"])):  # Grafico de Bodes
                if index == 0:
                    axes[0].plot(self.data["frec"][index], self.data["amp"][index], 
                            color='C'+str(cIndex), linestyle = self.trazo, label= self.nombre)
                    axes[1].plot(self.data["frec"][index], self.data["phase"][index], 
                            color='C'+str(cIndex), linestyle = self.trazo, label= self.nombre)
                else:
                    axes[0].plot(self.data["frec"][index], self.data["amp"][index], 
                            color='C'+str(cIndex), linestyle = self.trazo)
                    axes[1].plot(self.data["frec"][index], self.data["phase"][index], 
                            color='C'+str(cIndex), linestyle = self.trazo)
        
            for index in range(len(self.data["time"])):  # Grafico de Rtas
                if index == 0:
                    axes[2].plot(self.data["time"][index], self.data["y"][index], 
                            color='C'+str(cIndex), linestyle = self.trazo, label= self.nombre)
                else:
                    axes[2].plot(self.data["time"][index], self.data["y"][index], 
                        color='C'+str(cIndex), linestyle = self.trazo)

    def setVisibility(self, state):
        self.visibility = state

def graphCurves(curves=[], axes=[], exitaciones = []):
    
    for i in range(len(curves)):
        curves[i].data["time"].clear()  # Limpiamos las Respuestas
        curves[i].data["y"].clear()

        for excitacion in exitaciones:  # Para cada excitación, le calculamos la respuesta a cada curva teórica
            if excitacion.visibility == True and curves[i].H !=0 and curves[i].modo == 0:
                curves[i].calcRta(excitacion)       

        curves[i].graphCurve(axes, i)   # Graficamos la curva
    
    for axis in axes:   # Para cada eje, ponemos leyendas y grillas
        axis.legend()   
        axis.grid()