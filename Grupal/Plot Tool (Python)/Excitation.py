import numpy as np
import scipy.signal as ss

class Excitation:
    def __init__(self, name, type, amp=0, freq=0, freqType='F', duty=1):    # Type: 0 Escalon, 1 Senoidal, 2 Impulso, 3 tren de pulsos
        self.name = name                                                    # FreqType: F en Hz, W en rad/s
        self.type = type
        self.amp = amp
        self.freq = freq if freqType == 'W' else 2*np.pi*freq
        self.duty = duty
        self.visibility = True
    
    def setVisibility(self, state=True):
        self.visibility = state

    def getValues(self):
        
        A = self.amp
        w = self.freq
        T = 2*np.pi/w  if w!= 0 else 0
        tMax= 20*T       # Duracion: 20 periodos
            
        if self.type == 0:                    # Senoidal
            tin = np.linspace(0, tMax, 50000, endpoint=False)
            seno = A*(np.sin(w*tin))
            return tin, seno

        elif self.type == 1:                      # Escalon
            tin = np.linspace(0, 10, 100, endpoint=False)   # Por 10 segundos
            step = A*np.ones(100)
            return tin, step

        elif self.type == 2:                    # Tren de pulsos
            tin = np.linspace(0, tMax, 50000, endpoint=False)
            cuadrada = self.amp*(ss.square(w*tin, self.duty)+1)/2   # Adaptacion de 0 a 1V con frecuencia deseada
            return tin, cuadrada

        elif self.type == 3:                    # Impulso
            return None

    def graphExcit(self, axis, cIndex=0):
        if self.visibility == True:
            color = 'C' + str(cIndex)
            if self.type == 3:  # Impulso
                axis.stem([0], [1], linefmt=color, markerfmt=color+'^', label=self.name)     # Dibujo una flecha del origen a (0, 1)
            else:
                t, y = self.getValues()
                axis.plot(t,y, color=color, label=self.name)



    # For Debug
    def __str__(self) -> str:
        return f'''Name: {self.name}
Type: {self.type}
Amplitude: {self.amp}
Freq: {self.freq}
Duty: {self.duty}'''