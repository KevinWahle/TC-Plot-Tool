import numpy as np
import scipy.signal as ss

from src.fileReader import getDataFromFile

class Curve:

    def __init__(self, name: str, axes, visibility=True):   # axes = [ Magnitude, Phase, Time ]
        self.name = name
        self.visibility = visibility

    def setName(self, name):
        self.name = name

    def setVisible(self, visibility=True):
        self.visibility = visibility
    
    def delete(self):
        pass
    
    # @staticmethod
    # def drawCurves(curves, axes):   # axes = [ Magnitude, Phase, Time ]
    #     for curve in curves:
    #         curve.draw(axes)


# Curva a partir de función transferencia
class TFCurve(Curve):

    def __init__(self, name: str, Hnum: list[float], Hden: list[float], freqRange: list[float], logscale: bool, axes, visibility=True):
        super().__init__(name, axes, visibility=visibility)
        self.H = ss.TransferFunction(Hnum, Hden)
        self.plot = [None, None, []]    # [ Magnitude, Phase, [resp1, resp2, ...] ]

        # Creación de la curva
        start = np.log10(freqRange[0])
        end = np.log10(freqRange[1])
        ppd = 1e4   # Puntos por decada
        num = int(np.ceil(end-start)*ppd)
        frec = np.logspace(start, end, num=num)

        if logscale:
            _, mag, phase = ss.bode(self.H, w=2*np.pi*frec)
        else:
            _, h = ss.freqresp(self.H, w=2*np.pi*frec)
            mag = abs(h)
            phase = np.angle(h, deg=True)

        # Fase limitada entre -180 y 180
        phase[phase > 180] -= 360
        phase[phase < -180] += 360

        # Guarda las curvas linkeadas al eje
        self.plot[0] = axes[0].plot(frec, mag, label=self.name)[0]
        self.plot[1] = axes[1].plot(frec, phase, label=self.name)[0]

    def addResponse(self, excitation, timeAxis):
        
        if excitation.type == 0:                    # senoidal
            tin,seno =excitation.getValues()
            t, y,_  = ss.lsim((self.H.num, self.H.den), U=seno, T=tin)  # Calculamos la Rta
        
        elif excitation.type == 1:                      # escalon
            t, y = ss.step((self.H.num, self.H.den))        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.step.html#scipy.signal.step
            y = y * excitation.amp  

        elif excitation.type == 2:                           # cuadrada
            tin,cuadrada = excitation.getValues()
            t, y,_ = ss.lsim((self.H.num, self.H.den), U=cuadrada, T=tin) # Calculamos la Rta

        elif excitation.type == 3:                           # impulso
            t, y = ss.impulse((self.H.num, self.H.den))     #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.impulse.html#scipy.signal.impulse
        
        # Cargar archivo de exitación. 
        else:
            tin, signal = excitation.getValues()
            t, y,_ = ss.lsim((self.H.num, self.H.den), U=signal, T=tin) # Calculamos la Rta

        # Linkeo y creación de la respuesta
        line = timeAxis.plot(t, y, label= self.name + " - " + excitation.name)
        line.set_visible(self.visibility)
        self.plot[2].append(line)

    def delResponse(self, index):
        self.plot[2].pop(index)

    def setName(self, name):
        super().setName(name)
        for plot in self.plot[0:1]:
            if plot is not None:
                plot.set_label(name)
        #TODO: Cambiar el nombre de las respuestas

    def setVisible(self, visibility=True):
        super().setVisible(visibility=visibility)
        for plot in self.plot[0:2]+self.plot[2]:   #TODO: Revisar si funciona esa concatenacion
            if plot is not None:
                plot.set_visible(self.visibility)
                # if visibility:
                #     plot.set_visible(self.visibility)
                # else:
                #     plot.remove()

    def delete(self):
        for plot in self.plot[0:2]+self.plot[2]:   #TODO: Revisar si funciona esa concatenacion
            if plot is not None:
                plot.remove()

# Curva a partir de archhivo (.txt o .csv)
class FileCurve(Curve):

    def __init__(self, name: str, path: str, mode: int, axes, visibility=True):
        super().__init__(name, axes, visibility=visibility)
        self.plot = [None, None, None]    # [ Magnitude, Phase, time ]
        self.mode = mode
        self.data = getDataFromFile(path, mode)

        if mode == 0:   # En frecuencia

            if len(self.data["frec"]) > 1:
                freq = self.data["frec"]

                mag = axes[0].plot(freq, self.data["amp"], label=name)[0]
                phase = axes[1].plot(freq, self.data["phase"], label=name)[0]
                self.plot = [mag, phase, None]
            else:
                #TODO: Ver caso MonteCarlo
                pass

        else:   # En el tiempo
            time = axes[2].plot(self.data["time"], self.data["y"], label=name)[0]
            self.plot = [None, None, time]

    def setName(self, name):
        super().setName(name)
        for plot in self.plot:
            if plot is not None:
                plot.set_label(name)

    def setVisible(self, visibility=True):
        super().setVisible(visibility=visibility)
        for plot in self.plot:
            if plot is not None:
                plot.set_visible(self.visibility)

    def delete(self):
        for plot in self.plot:
            if plot is not None:
                plot.remove()