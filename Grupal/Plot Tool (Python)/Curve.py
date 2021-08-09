class Curve:

   def __init__(self, nombre, trazo, Hnum=0, Hden=0, path, modo):
   
        self.nombre = nombre
        self.path = path
        self.visibility = True 
        
        if Hnum != 0 and Hden != 0:
            self.H = getTransfFunct(Hnum, Hden)

        if ".txt" in path:
            self.data = getDataSimulation(path, modo)
            self.trazo = "solid"

        elif ".csv" in path:
            self.data = getDataMediciones(path, modo)
            self.trazo= "dashdot"

        elif Hnum != 0 and Hden != 0:
            self.data = getDataTeorica(self.H)
            self.trazo = "dotted"


    def calcRta(self, exitacion, w=0, A=0, duty=0.5):
    
        if exitacion == 0:                      # escalon
            t, y = ss.step((self.H.num, self.H.den))        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.step.html#scipy.signal.step
            
        elif exitacion == 1:                    # senoidal
            tMax= 5 * (2*np.pi/w)   
            tin = np.linspace(0, tMax, 50000, endpoint=False)
            seno = A*(np.sin(w*t))
            
            t, y,  = ss.lsim((self.H.num, self.H.den), U=seno, T=t)  # Calculamos la Rta
        
        elif exitacion == 2:                    # impulso
            t, y = ss.impulse((self.H.num, self.H.den))     #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.impulse.html#scipy.signal.impulse

        elif exitacion == 3:                    # pulso
            tMax= 5 * (2*np.pi/w)   
            tin = np.linspace(0, tMax, 50000, endpoint=False)
            cuadrada = ss.square(5*(2*np.pi)*tin, duty)
            t, y,  = ss.lsim((self.H.num, self.H.den), U=cuadrada, T=t) # Calculamos la Rta

        #else:
        # Cargar archivo de exitación. 

        self.data["time"] = t   # Guardamos el arreglo temporal
        self.data["y"] = y      # Guardamos el arreglo Y

    def graphCurve(self, axes):
        print("Proximamente")

    def setVisibility(self, state):
        self.visibility = state