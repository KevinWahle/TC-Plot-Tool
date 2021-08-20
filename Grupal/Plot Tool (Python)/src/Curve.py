from src.fileReader import *
from src.Excitation import *

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

        if exitacion.type == 0:                    # senoidal
            tin,seno =exitacion.getValues()
            t, y,_  = ss.lsim((self.H.num, self.H.den), U=seno, T=tin)  # Calculamos la Rta
        
        elif exitacion.type == 1:                      # escalon
            t, y = ss.step((self.H.num, self.H.den))        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.step.html#scipy.signal.step
            y = y * exitacion.amp  

        elif exitacion.type == 2:                           # cuadrada
            tin,cuadrada = exitacion.getValues()
            t, y,_ = ss.lsim((self.H.num, self.H.den), U=cuadrada, T=tin) # Calculamos la Rta

        elif exitacion.type == 3:                           # impulso
            t, y = ss.impulse((self.H.num, self.H.den))     #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.impulse.html#scipy.signal.impulse
        
        # Cargar archivo de exitación. 
        else:
            tin, signal = exitacion.getValues()
            t, y,_ = ss.lsim((self.H.num, self.H.den), U=signal, T=tin) # Calculamos la Rta


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
                    self.trazo = "solid"
                    curveColor = "grey"
                    alpha=1
                    zorder = 1
                else:
                    curveColor = 'C'+str(cIndex)
                    alpha=1
                    zorder = 2

                if index == 0:  # Primera curva del arreglo

                    if self.trazo == "marker":       # Caso mediciones (va con marker)
                        axes[0].scatter(frecArr, self.data["amp"][index], 
                                s=5, color=curveColor, label= self.nombre, alpha=alpha, zorder=2.5)
                        axes[1].scatter(frecArr, self.data["phase"][index], 
                                s=5, color=curveColor, label= self.nombre, alpha=alpha, zorder=2.5)
                    

                    else:                           # Caso no mediciones (va con linestyle)
                        axes[0].plot(frecArr, self.data["amp"][index], color=curveColor, 
                                    linestyle = self.trazo, label= self.nombre, alpha=alpha, zorder=zorder)
                        axes[1].plot(frecArr, self.data["phase"][index], color=curveColor, 
                                    linestyle = self.trazo, label= self.nombre, alpha=alpha, zorder=zorder)
                
                else:       # Caso montecarlo, no primera curva
                    if self.trazo == "marker":      # Caso mediciones (va con marker)                      
                        axes[0].plot(frecArr, self.data["amp"][index], 
                                color=curveColor, marker="o", alpha=alpha, zorder=zorder)
                        axes[1].plot(frecArr, self.data["phase"][index], 
                                color=curveColor, marker="o", alpha=alpha, zorder=zorder)

                    else:                           # Caso no mediciones (va con linestyle)
                        axes[0].plot(frecArr, self.data["amp"][index], 
                                color=curveColor, linestyle = self.trazo, alpha=alpha, zorder=zorder)
                        axes[1].plot(frecArr, self.data["phase"][index], 
                                color=curveColor, linestyle = self.trazo, alpha=alpha, zorder=zorder)
                dibujeBode = 1
        
            for index in range(len(self.data["time"])):  # Grafico de Rtas
                
                if len(self.data["time"]) > 1 and self.H == 0:  # Si es montecarlo en el tiempo,
                    curveColor = "grey"                    # pinto de color gris
                    self.trazo = "solid"
                    alpha=1
                    zorder = 1
                else:
                    curveColor = 'C'+str(cIndex)                # Sino le doy colorcitos
                    alpha=1
                    zorder = 2

                if index == 0 or self.H != 0:

                    if self.H == 0: # Si no hay transferencia, la curva NO es una rta
                        my_label = self.nombre

                    else:           # Si hay transferencia, la curva SI es una rta
                        exiVisibles = [exitacion for exitacion in exitaciones if exitacion.visibility == True]
                        my_label = self.nombre+ "-" + exiVisibles[index].name
                    
                    if self.trazo == "marker":       # Caso mediciones (va con marker)
                        axes[2].scatter(self.data["time"][index], self.data["y"][index], 
                                color=curveColor, s=5, label= my_label, alpha=alpha, zorder=2.5)
                    else:
                        axes[2].plot(self.data["time"][index], self.data["y"][index], 
                                color=curveColor, linestyle = self.trazo, label= my_label, alpha=alpha, zorder=2.5)
                else:
                    if self.trazo == "marker":       # Caso mediciones (va con marker)
                        axes[2].scatter(self.data["time"][index], self.data["y"][index], 
                                color=curveColor, s=5, alpha=alpha, zorder=zorder)
                    else:
                        axes[2].plot(self.data["time"][index], self.data["y"][index], 
                                color=curveColor, linestyle = self.trazo, alpha=alpha, zorder=zorder)
                dibujeRta = 1

        return dibujeBode, dibujeRta       

    def setVisibility(self, state):
        self.visibility = state

def graphCurves(curves=[], axes=[], exitaciones = [], frec = 0):
    dibuje = [0,0]  # DibujeBode, dibujeRta
    exitacionesDibujadas = np.zeros_like(exitaciones) # Arreglo con flags si las exitaciones fueron o no dibujadas.

    # Primero dibujamos las funciones de excitacion
    for j in range(len(exitaciones)):
        if exitaciones[j].visibility:
            exitaciones[j].graphExcit(axes[2], j+len(curves))       # Graficamos las exitaciones visibles
            exitacionesDibujadas[j]=1
            dibuje = np.add([0,1], dibuje)          # Es asi???                        
    
    for i in range(len(curves)):
        
        if curves[i].H != 0:
            curves[i].data["time"].clear()  # Limpiamos sólo las Respuestas
            curves[i].data["y"].clear()      

        for j in range(len(exitaciones)):  # Para cada excitación, le calculamos la respuesta a cada curva teórica
            if exitaciones[j].visibility == True and curves[i].H !=0 and curves[i].modo == 0:
                curves[i].calcRta(exitaciones[j])

            # Lo comento porque se grafican aparte, aunque no haya curvas
            # if exitaciones[j].visibility == True and exitacionesDibujadas[j] == 0:
            #     exitaciones[j].graphExcit(axes[2], j+len(curves))       # Graficamos las exitaciones visibles
            #     exitacionesDibujadas[j]=1


        aux = curves[i].graphCurve(axes, i, frec, exitaciones)   # Graficamos la curva
        dibuje = np.add(aux, dibuje)
    


    if dibuje[0] > 0:               # Si dibuje algún Bode
            axes[0].legend(); axes[1].legend()   
            axes[0].grid(which='both', zorder=0); axes[1].grid(which='both', zorder=0)
            axes[0].set_axisbelow(True); axes[1].set_axisbelow(True)


    if dibuje[1] > 0:               # Si dibujé alguna Rta
        axes[2].legend()   
        axes[2].grid(zorder=0)
        axes[2].set_axisbelow(True) 
