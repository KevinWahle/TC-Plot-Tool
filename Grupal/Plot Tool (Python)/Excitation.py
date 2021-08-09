import numpy as np
import scipy.signal as ss

class Excitation:
    def __init__(self, name, type, amp=0, freq=0, freqType='F', duty=1):    # Type: 0 Escalon, 1 Senoidal, 2 Impulso, 3 tren de pulsos
        self.name = name                                              # FreqType: F en Hz, W en rad/s
        self.type = type
        self.amp = amp
        self.freq = freq if freqType is 'W' else 2*np.pi*freq
        self.duty = duty
        self.visibility = True
    
    def setVisibility(self, state=True):
        self.visibility = state

    def getValues(self):
        
        A = self.amp
        w = self.freq
        T = 2*np.pi/w

        if self.type == 0:                      # Escalon
            return None
            
        elif self.type == 1:                    # Senoidal
            tMax= 5*T       # Duracion: 5 periodos
            tin = np.linspace(0, tMax, 50000, endpoint=False)
            seno = A*(np.sin(w*tin))
            return tin, seno

        elif self.type == 2:                    # Impulso
            return None

        elif self.type == 3:                    # Tren de pulsos
            tMax= 5*T       # Duracion: 5 periodos
            tin = np.linspace(0, tMax, 50000, endpoint=False)
            cuadrada = self.amp*(ss.square(w*tin, self.duty)+1)/2   # Adaptacion de 0 a 1V con frecuencia deseada
            return tin, cuadrada