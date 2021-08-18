import numpy as np
import pandas as pd
import scipy.signal as ss

class Excitation:
    def __init__(self, name, type, amp=0, freq=0, freqType='F', duty=1, path=''):    # Type: 0 Escalon, 1 Senoidal, 2 Impulso, 3 tren de pulsos
        self.name = name                                                    # FreqType: F en Hz, W en rad/s
        self.type = type
        self.amp = amp
        self.freq = freq if freqType == 'W' else 2*np.pi*freq
        self.duty = duty
        self.path = path
        self.visibility = True
        self.dict = {}

        if type == 4:
            self.dict = self._saveValuesFromCSV(path)
    
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

        elif self.type == 4:                    # Desde archivo CSV
            return self.dict['time'], self.dict['y']

    def graphExcit(self, axis, cIndex=0, alpha=0.75):
        if self.visibility == True:
            color = 'C' + str(cIndex)
            if self.type == 3:  # Impulso
                axis.stem([0], [1], linefmt=color, markerfmt=color+'^', label=self.name, alpha=alpha)     # Dibujo una flecha del origen a (0, 1)
            else:
                t, y = self.getValues()
                axis.plot(t,y, color=color, label=self.name, alpha=alpha)

    def _saveValuesFromCSV(self, path):
        data = (pd.read_csv(path)).to_numpy()       # Pasamos de .csv a matriz 
        aux={"time":[], "y":[]}  # Diccionario aux para manipular los datos.

        filas= (data.shape)[0]
        for index in range(filas):
                aux["time"].append(data[index][0])      # Para cada columna, appendeo TODOS los datos de cada una 
                aux["y"].append(data[index][1])         # de sus filas en un arreglo distinto. 

        return aux

    # For Debug
    def __str__(self) -> str:
        return f'''Name: {self.name}
Type: {self.type}
Amplitude: {self.amp}
Freq: {self.freq}
Duty: {self.duty}'''