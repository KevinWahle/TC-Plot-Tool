from scipy.signal.ltisys import TransferFunction
from spice import *
from Excitation import *
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
            self.trazo = "solid"

        if ".txt" in path:
            self.H=0
            self.data = getDataSimulation(path, modo)
            self.trazo = "dashdot"

        elif ".csv" in path:
            self.H=0
            self.data = getDataMediciones(path, modo)
            self.trazo= "marker"


    def calcRta(self, exitacion):

        if exitacion.type == 1:                      # escalon
            tin,step =exitacion.getValues()
            t, y,_ = ss.lsim((self.H.num, self.H.den), U=step, T=tin)
            #Modo viejo
            #t, y = ss.step((self.H.num, self.H.den))        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.step.html#scipy.signal.step
            #y = y * exitacion.amp
        
        elif exitacion.type == 0:                    # senoidal
            tin,seno =exitacion.getValues()
            t, y,_  = ss.lsim((self.H.num, self.H.den), U=seno, T=tin)  # Calculamos la Rta
        
        elif exitacion.type == 3:                    # impulso
            t, y = ss.impulse((self.H.num, self.H.den))     #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.impulse.html#scipy.signal.impulse

        elif exitacion.type == 2:                    # cuadrada
            tin,cuadrada = exitacion.getValues()
            t, y,_ = ss.lsim((self.H.num, self.H.den), U=cuadrada, T=tin) # Calculamos la Rta

        #else:
        # Cargar archivo de exitación. 

        self.data["time"].append(t)   # Guardamos el arreglo temporal
        self.data["y"].append(y)      # Guardamos el arreglo Y

    def graphCurve(self, axes=[], cIndex=0, frec = 0, exitaciones = []):    # axes = [ModuleAxis, PhaseAxis, ResponseAxis]
                                                                            # Freq: 0 = Hz; 1 = rad/s 
        dibujeBode = dibujeRta = 0
        
        if self.visibility == True:
            for index in range(len(self.data["frec"])):  # Grafico de Bodes 
                
                if frec == 1:
                    frecArr = np.multiply(self.data["frec"][index], 2*np.pi)
                else:
                    frecArr = self.data["frec"][index]

                if len(self.data["frec"]) > 1:
                    curveColor = "lightgray"
                else:
                    curveColor = 'C'+str(cIndex)

                if index == 0:  # Primera curva del arreglo

                    if self.trazo == "marker":       # Caso mediciones (va con marker)
                        axes[0].scatter(frecArr, self.data["amp"][index], 
                                s=5, color=curveColor, alpha=1, label= self.nombre)
                        axes[1].scatter(frecArr, self.data["phase"][index], 
                                s=5, color=curveColor, alpha=1, label= self.nombre)
                    

                    else:                           # Caso no mediciones (va con linestyle)
                        axes[0].plot(frecArr, self.data["amp"][index], 
                                color=curveColor, linestyle = self.trazo, label= self.nombre)
                        axes[1].plot(frecArr, self.data["phase"][index], 
                                color=curveColor, linestyle = self.trazo, label= self.nombre)
                
                else:       # Caso montecarlo, no primera curva
                    if self.trazo == "marker":      # Caso mediciones (va con marker)                      
                        axes[0].plot(frecArr, self.data["amp"][index], 
                                color=curveColor, marker="o")
                        axes[1].plot(frecArr, self.data["phase"][index], 
                                color=curveColor, marker="o")

                    else:                           # Caso no mediciones (va con linestyle)
                        axes[0].plot(frecArr, self.data["amp"][index], 
                                color=curveColor, linestyle = self.trazo)
                        axes[1].plot(frecArr, self.data["phase"][index], 
                                color=curveColor, linestyle = self.trazo)
                dibujeBode = 1
        
            for index in range(len(self.data["time"])):  # Grafico de Rtas
                
                if len(self.data["time"]) > 1 and self.H == 0:  # Si es montecarlo en el tiempo,
                    curveColor = "lightgray"                    # pinto de color gris
                else:
                    curveColor = 'C'+str(cIndex)                # Sino le doy colorcitos
                
                if index == 0 or self.H != 0:

                    if self.H == 0: # Si no hay transferencia, la curva NO es una rta
                        my_label = self.nombre

                    else:           # Si hay transferencia, la curva SI es una rta
                        my_label = self.nombre+ "-" +exitaciones[index].name
                    
                    if self.trazo == "marker":       # Caso mediciones (va con marker)
                        axes[2].scatter(self.data["time"][index], self.data["y"][index], 
                                color=curveColor, s=5, label= my_label)
                    else:
                        axes[2].plot(self.data["time"][index], self.data["y"][index], 
                                color=curveColor, linestyle = self.trazo, label= my_label)
                else:
                    if self.trazo == "marker":       # Caso mediciones (va con marker)
                        axes[2].scatter(self.data["time"][index], self.data["y"][index], 
                                color=curveColor, s=5)
                    else:
                        axes[2].plot(self.data["time"][index], self.data["y"][index], 
                                color=curveColor, linestyle = self.trazo)
                dibujeRta = 1

        return dibujeBode, dibujeRta       

    def setVisibility(self, state):
        self.visibility = state

def graphCurves(curves=[], axes=[], exitaciones = [], frec = 0):
    dibuje = [0,0]  # DibujeBode, dibujeRta
    exitacionesDibujadas = np.zeros_like(exitaciones) # Arreglo con flags si las exitaciones fueron o no dibujadas.

    for i in range(len(curves)):
        
        if curves[i].H != 0:
            curves[i].data["time"].clear()  # Limpiamos sólo las Respuestas
            curves[i].data["y"].clear()      

        for j in range(len(exitaciones)):  # Para cada excitación, le calculamos la respuesta a cada curva teórica
            if exitaciones[j].visibility == True and curves[i].H !=0 and curves[i].modo == 0:
                curves[i].calcRta(exitaciones[j])

            if exitaciones[j].visibility == True and exitacionesDibujadas[j] == 0:
                exitaciones[j].graphExcit(axes[2], j+len(curves))       # Graficamos las exitaciones visibles
                exitacionesDibujadas[j]=1                               


        aux = curves[i].graphCurve(axes, i, frec, exitaciones)   # Graficamos la curva
        dibuje = np.add(aux, dibuje)
    
    if dibuje[0] > 0:               # Si dibuje algún Bode
            axes[0].legend(); axes[1].legend()   
            axes[0].grid(); axes[1].grid()

    if dibuje[1] > 0:               # Si dibujé alguna Rta
        axes[2].legend()   
        axes[2].grid()                
