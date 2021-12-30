from matplotlib import pyplot as plt
import numpy as np
import scipy.signal as ss

# from fileReader import getDataFromFile
from src.fileReader import getDataFromFile

class Curve:

    def __init__(self, name: str, axes, visibility=True):   # axes = [ Magnitude, Phase, Time ]
        self.name = name
        self.visibility = visibility

    def setName(self, name):
        self.name = name

    def setVisible(self, visibility=True):
        self.visibility = visibility
    
    def setXUnits(self, units):
        pass

    def delete(self):
        pass
    
    # @staticmethod
    # def drawCurves(curves, axes):   # axes = [ Magnitude, Phase, Time ]
    #     for curve in curves:
    #         curve.draw(axes)


# Curva a partir de función transferencia
# freqUnits: Unidad en la que se interpreta freqrange. (Hz/rads)
# plotUnits: Unidad en la que se grafica la función. (Hz/rads)
class TFCurve(Curve):

    def __init__(self, name: str, Hnum: list[float], Hden: list[float], freqRange: list[float], \
                logscale: bool, axes, freqUnits='Hz', plotUnits='Hz', visibility=True):
        super().__init__(name, axes, visibility=visibility)
        self.H = ss.TransferFunction(Hnum, Hden)
        self.units = plotUnits
        self.plot = [None, None, []]    # [ Magnitude, Phase, [resp1, resp2, ...] ]

        # Creación de la curva
        start = np.log10(freqRange[0])
        end = np.log10(freqRange[1])
        ppd = 1e4   # Puntos por decada
        num = int(np.ceil(end-start)*ppd)
        frec = np.logspace(start, end, num=num)

        if (freqUnits == 'Hz'):
            w = 2*np.pi*frec
        else:
            w = frec

        if logscale:
            _, mag, phase = ss.bode(self.H, w=w)
        else:
            _, h = ss.freqresp(self.H, w=w)
            mag = abs(h)
            phase = np.angle(h, deg=True)

        # Fase limitada entre -180 y 180
        phase[phase > 180] -= 360
        phase[phase < -180] += 360

        # Ajuste de unidades
        if plotUnits == 'Hz':
            frec = w/(2*np.pi)
        else:
            frec = w

        # Guarda las curvas linkeadas al eje
        self.plot[0], = axes[0].plot(frec, mag, label=self.name)
        self.plot[1], = axes[1].plot(frec, phase, label=self.name)

    def addResponse(self, excitation, axes):
        
        timeAxis = axes[2]  # Solo en el tiempo

        t, y = excitation.getResponse(self.H)

        # Linkeo y creación de la respuesta
        line, = timeAxis.plot(t, y, label= self.name + " - " + excitation.name)
        line.set_visible(self.visibility)
        self.plot[2].append(line)

    def delResponse(self, index):
        self.plot[2][index].remove()    # Borra la curva y despues lo saca
        self.plot[2].pop(index)

    def setName(self, name):
        old = self.name
        super().setName(name)
        for plot in self.plot[0:1]:
            if plot is not None:
                plot.set_label(name)

        for plot in self.plot[2]:
            if plot is not None:
                plot.set_label(plot.get_label().replace(old, name, 1))

    def setVisible(self, visibility=True):
        super().setVisible(visibility=visibility)
        for plot in self.plot[0:2]+self.plot[2]:   #TODO: Revisar si funciona esa concatenacion
            if plot is not None:
                plot.set_visible(self.visibility)

    def setXUnits(self, units):
        if units != self.units:
            self.units = units
            if units == 'Hz':
                mux = 1/(2*np.pi)
            elif units == 'rads':
                mux = 2*np.pi
            else:
                raise ValueError("Units not supported")
            self.plot[0].set_xdata(self.plot[0].get_xdata()*mux)
            self.plot[1].set_xdata(self.plot[1].get_xdata()*mux)

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

                mag, = axes[0].plot(freq, self.data["amp"], label=name)
                phase, = axes[1].plot(freq, self.data["phase"], label=name)
                self.plot = [mag, phase, None]
            else:
                #TODO: Ver caso MonteCarlo
                pass

        else:   # En el tiempo
            time, = axes[2].plot(self.data["time"], self.data["y"], label=name)
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


# Curva que representa una Excitación
# Type: 0 Escalon, 1 Senoidal, 2 Impulso, 3 tren de pulsos, 4 Archivo CSV
# FreqType: F en Hz, W en rad/s
# Duty: 0.0 - 1.0
# Duration: en segundos
class ExcitCurve(Curve):

    def __init__(self, name: str, axes, type, amp=0, freq=0, freqType='F', duty=1, path='', duration=10e-3, visibility=True):
        super().__init__(name, axes, visibility=visibility)
        self.type = type
        self.amp = amp
        self.freq = freq if freqType == 'W' else 2*np.pi*freq   # Se guarda en rad/s
        self.duty = duty
        self.path = path
        self.duration = duration

        self.plot = self._plotExcit(axes)

    def setName(self, name):
        super().setName(name)
        self.plot.set_label(name)
        
    def setVisible(self, visibility=True):
        super().setVisible(visibility=visibility)
        self.plot.set_visible(self.visibility)
        
    def delete(self):
        self.plot.remove()

    # Devuelve (x, y) con la respuesta a la excitación del sistema lti
    def getResponse(self, lti: ss.lti):

        if self.type == 1:            # escalon
            t, y = ss.step(lti, T=self.plot.get_xdata())        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.step.html#scipy.signal.step
            y *= self.amp  

        elif self.type == 3:          # impulso
            t, y = ss.impulse(lti, T=self.plot.get_xdata())     #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.impulse.html#scipy.signal.impulse
        
        else:                          # Otro caso, tomo los puntos
            tin, signal = np.array(self.plot.get_xydata()).T    # Obtiene los puntos de la curva
            t, y,_ = ss.lsim(lti, U=signal, T=tin)

        return t, y


    def _plotExcit(self, axes):

        ax = axes[2]    # Solo en el tiempo

        A = self.amp
        w = self.freq
        T = 2*np.pi/w  if w!= 0 else 0
        tMax = self.duration
        line = None

        if self.type == 0:                    # Senoidal
            tin = np.linspace(0, tMax, 50000, endpoint=False)
            seno = A*(np.sin(w*tin))
            line, = ax.plot(tin, seno, label=self.name)

        elif self.type == 1:                      # Escalon
            tin = np.linspace(0, tMax, 100, endpoint=False)
            step = A*np.ones(100)
            tin = np.concatenate(([0], tin))      # Agrega un punto en (0, 0)
            step = np.concatenate(([0], step))    # Para ver el salto
            line, = ax.plot(tin, step, label=self.name)

        elif self.type == 2:                    # Tren de pulsos
            tin = np.linspace(0, tMax, 50000, endpoint=False)
            cuadrada = self.amp*ss.square(w*tin, self.duty)
            line, = ax.plot(tin, cuadrada, label=self.name)

        elif self.type == 3:                    # Impulso
            tin = [0, 0]
            impulse = [0, 1]
            line, = ax.plot(tin, impulse, marker='^', label=self.name)      #TODO: Hacer mas bonito

        elif self.type == 4:                    # Desde archivo CSV
            tin, y = self._readFile(self.path)
            line, = ax.plot(tin, y, label=self.name)

        return line

    def _readFile(self, path):
        
        if path.endswith(".txt"):
            delim = '\t'
        elif path.endswith(".csv"):
            delim = ','
        else:
            raise Exception("Archivo no soportado") 

        # Parsea el archivo, saltea primer linea (header) y usa solo las dos primeras columnas
        x, y = np.loadtxt(path, delimiter=delim, usecols=(0,1), skiprows=1, unpack=True)

        return x, y



 # DEBUG
 
if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot()

    ExcitCurve("Seno", [None, None, ax], 4, path='D:\Electronica\Fisica Electronica 2021\TP FE - Dispositivos\BJT\BJT_PS_5_10_15mV.txt')

    plt.show()