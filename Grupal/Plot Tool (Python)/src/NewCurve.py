from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
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
    
    def delete(self):
        pass
    
    # @staticmethod
    # def drawCurves(curves, axes):   # axes = [ Magnitude, Phase, Time ]
    #     for curve in curves:
    #         curve.draw(axes)


# Curva a partir de función transferencia
# freqUnits: Unidad en la que se interpreta freqrange. (Hz/rads)
class TFCurve(Curve):

    def __init__(self, name: str, Hnum: list[float], Hden: list[float], freqRange: list[float], \
                logscale: bool, axes, freqUnits, visibility=True):
        super().__init__(name, axes, visibility=visibility)
        self.H = ss.TransferFunction(Hnum, Hden)
        self.plot = [None, None, []]    # [ Magnitude, Phase, [resp1, resp2, ...] ]

        # Creación de la curva
        start = np.log10(freqRange[0])
        end = np.log10(freqRange[1])
        ppd = 1e3   # Puntos por decada
        num = int(np.ceil(end-start)*ppd)
        frec = np.logspace(start, end, num=num) * freqUnits
        # Seteo de unidades
        w = frec.to('rad/s').magnitude

        if logscale:
            _, mag, phase = ss.bode(self.H, w=w)
        else:
            _, h = ss.freqresp(self.H, w=w)
            mag = abs(h)
            phase = np.angle(h, deg=True)

        # Fase limitada entre -180 y 180
        phase[phase > 180] -= 360
        phase[phase < -180] += 360

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
        for plot in self.plot[0:2]+self.plot[2]:
            if plot is not None:
                plot.set_visible(self.visibility)

    def delete(self):
        for plot in self.plot[0:2]+self.plot[2]:
            if plot is not None:
                plot.remove()

# Curva a partir de archhivo (.txt o .csv)
# mode: 0  Frecuencia   |   Modulo      |   Fase
#       1  Tiempo       |   Magnitud
# freqUnits: Unidad en la que se interpreta el eje de la frecuencia. (Hz/rads)
class FileCurve(Curve):

    def __init__(self, name: str, path: str, mode: int, axes, freqUnits, visibility=True):
        super().__init__(name, axes, visibility=visibility)
        self.plot = [None, None, None]    # [ Magnitude, Phase, time ]
        self.mode = mode
        self.data = getDataFromFile(path, mode)


        if mode == 0:   # En frecuencia

            if len(self.data['frec']) > 1:  # MonteCarlo
                style = 'solid'
                color = 'grey'
                zorder = 1
                # TODO: Ver como soportar unidades
                # ampSegments = [ list(zip(x*freqUnits, y)) for x,y in zip(self.data['frec'], self.data['amp']) ]
                # phaseSegments = [ list(zip(x*freqUnits, y)) for x,y in zip(self.data['frec'], self.data['phase']) ]
                ampSegments = [ list(zip(x, y)) for x,y in zip(self.data['frec'], self.data['amp']) ]
                phaseSegments = [ list(zip(x, y)) for x,y in zip(self.data['frec'], self.data['phase']) ]
                ampLines = LineCollection(ampSegments, colors=color, linestyles=style, zorder=zorder, label=self.name)
                phaseLines = LineCollection(phaseSegments, colors=color, linestyles=style, zorder=zorder, label=self.name)
                mag = axes[0].add_collection(ampLines)
                phase = axes[1].add_collection(phaseLines)

            else:
                freq = self.data["frec"][0] * freqUnits

                mag, = axes[0].plot(freq, self.data["amp"][0], label=self.name)
                phase, = axes[1].plot(freq, self.data["phase"][0], label=self.name)

            self.plot = [mag, phase, None]	

        else:   # En el tiempo

            if len(self.data['time']) > 1:  # MonteCarlo
                style = 'solid'
                color = 'grey'
                zorder = 1
                segments = [ list(zip(x, y)) for x,y in zip(self.data['time'], self.data['y']) ]
                lines = LineCollection(segments, colors=color, linestyles=style, zorder=zorder, label=self.name)
                time = axes[2].add_collection(lines)
            else:
                time, = axes[2].plot(self.data["time"][0], self.data["y"][0], label=self.name)
            
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

        if self.type == 1:            # escalon     (Descarta primer valor poque empieza con [0, 0, ...])
            t, y = ss.step(lti, T=self.plot.get_xdata()[1:])        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.step.html#scipy.signal.step
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

    ExcitCurve("Seno", [None, None, ax], 0, amp=1, freq=1e3, freqType='W', duty=0.5, path='', duration=10e-3)

    plt.show()