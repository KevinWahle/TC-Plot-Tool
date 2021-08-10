# Vale la pena guardar el tiempo?


import numpy as np
import pandas as pd
import scipy.signal as ss

def appendCurve(toAppend, appended, modo):

    if modo == 0:
        toAppend["frec"].append(appended["frec"])          # Apendeamos la frec de la run a la frec del dict de la señal
        toAppend["amp"].append(appended["amp"])            # Apendeamos la Amp de la run a la Amp del dict de la señal
        toAppend["phase"].append(appended["phase"])        # Apendeamos la fase de la run a la fase del dict de la señal
    elif modo == 1:
        toAppend["time"].append(appended["time"])          # Apendeamos el time de la run al time del dict de la señal
        toAppend["y"].append(appended["y"])                # Apendeamos la y de la run a la y del dict de la señal
    
    return toAppend

# Te pasa los datos de UNA curva (no montecarlo) a un dict de arreglos(NO matrices) de datos
def Data2Dict(data, modo):
    no_deseado=["(","\n",")","dB","°","Â","A","W","V", "Ω"]
    aux = {"frec":[], "amp":[], "phase":[], "time":[], "y":[]} # Diccionario aux para manipular los datos
    
    for line in data:
        
        for caracter in no_deseado:
            line = line.replace(caracter,'')    # Remplazamos los caracteres molestos         
        
        line=line.split("\t")                   # Separamos cada renglón en frecuencia, módulo y fase
        
        if modo == 0:           # Caso bode(f)
            aux["frec"].append(float(line[0]))  # Agregamos la frec al arreglo de frecuencias
            bode= line[1]                            

            
            bode = bode.split(",")                  # Separamos el bode en Amp y Fase
            aux["amp"].append(float(bode[0]))    # Agregamos la Amp al dict   
            aux["phase"].append(float(bode[1]))  # Agregamos la Fase al dict
        
        elif modo == 1:         # Caso y(t)
            aux["time"].append(float(line[0]))  # Agregamos el tiempo al dict
            aux["y"].append(float(line[1]))

    return aux

def getDataSpice(lines, modo):  
    signal={"frec":[], "amp":[], "phase":[], "time":[], "y":[]}
    aux = {"frec":[], "amp":[], "phase":[], "time":[], "y":[]}      # Diccionario aux para manipular los datos
    aux = Data2Dict(lines, modo)      # Dictionario con los arreglos de datos

    return appendCurve(signal, aux, modo)

def getDataFromMonteCarlo(rawData, modo):
    # Inicializamos variables
    signal={"frec":[], "amp":[], "phase":[], "time":[], "y":[]}
    init = -1
    fin = 0
    last=len(rawData)

    for index in range(last):

        if ("Step" in rawData[index])  or index == last-1:
            if init == -1:      # Caso encuentro el Step de la primera Run
                init = index+1  # Seteo solamente el init
            
            else:
                fin = index                                 # Determinamos el último punto a medir
                print(rawData[index])
                # Transformo los renglones en una curva y la appendeo a signal (arreglo de curvas) 
                signal = appendCurve(signal, Data2Dict(rawData[init:fin], modo), modo)    
                init = index+1                              # Movemos el Inicio al primer dato de la prox Run

    return signal

def getDataSimulation(path, modo):
    file= open(path, "r")
    
    #Headers
    headers= file.readline().split("\t")
    headers[len(headers)-1]=headers[len(headers)-1].replace("\n","")
    
    data = file.readlines()
    if "Step" in data[0]:
        signal = getDataFromMonteCarlo(data, modo)
    else:
        signal = getDataSpice(data, modo)

    return signal    

def getDataMediciones(path, modo):
    data = (pd.read_csv(path)).to_numpy()       # Pasamos de .csv a matriz 
    aux={"frec":[], "amp":[], "phase":[], "time":[], "y":[]}  # Diccionario aux para manipular los datos.

    filas= (data.shape)[0]
    for index in range(filas):
        if modo == 0:
            aux["frec"].append(data[index][0])      # Para cada columna, appendeo TODOS los datos de cada una 
            aux["amp"].append(data[index][1])       # de sus filas en un arreglo distinto. 
            aux["phase"].append(data[index][2])

        elif modo == 1:
            aux["time"].append(data[index][0])      # Para cada columna, appendeo TODOS los datos de cada una 
            aux["y"].append(data[index][1])         # de sus filas en un arreglo distinto. 

    return appendCurve(aux, modo)

def getDataFromFile(path, modo):
    if ".txt" in path:
        signal = getDataSimulation(path, modo)
    elif ".csv" in path:
        signal = getDataMediciones(path, modo)
    
    return signal

def getTransfFunct(numStr, denStr):
    # Pasa los coeficientes de array(String) a array(float)
    numList=numStr.split(",")
    denList=denStr.split(",")

    num=[]
    for index in range(len(numList)):
        num.append(float(numList[index]))

    den=[]
    for index in range(len(denList)):
        den.append(float(denList[index]))

    H = ss.TransferFunction(num,den)

    return H

def simBode(H, signal):
    signal={"frec":[], "amp":[], "phase":[], "time":[], "y":[]}

    bode = ss.bode(H)                           # Calculamos el Bode
    signal["frec"].append(bode[0]/(2*np.pi))    # Guardamos el Bode
    signal["amp"].append(bode[1])
    signal["phase"].append(bode[2])

    return signal

def getDataTeorica(Hnum, Hden):
    # Calculamos el Bode y lo appendeamos al dict
    signal={"frec":[], "amp":[], "phase":[], "time":[], "y":[]}
    H = getTransfFunct(Hnum, Hden)
    signal = simBode(H, signal) 

    return signal


#No se usa
def calcRta(H, exitacion, w=0, A=0, duty=0.5):
    
    if exitacion == 0:                      # escalon
        t, y = ss.step((H.num, H.den))      #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.step.html#scipy.signal.step
        
    elif exitacion == 1:                    # senoidal
        tMax= 5 * (2*np.pi/w)   
        tin = np.linspace(0, tMax, 50000, endpoint=False)
        seno = A*(np.sin(w*tin))
        
        t, y,  = ss.lsim((H.num, H.den), U=seno, T=tin)  # Calculamos la Rta
    
    elif exitacion == 2:                    # impulso
        t, y = ss.impulse((H.num, H.den))   #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.impulse.html#scipy.signal.impulse

    elif exitacion == 3:                    # pulso
        tMax= 5 * (2*np.pi/w)   
        tin = np.linspace(0, tMax, 50000, endpoint=False)
        cuadrada = ss.square(5*(2*np.pi)*tin, duty)     #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.square.html#scipy.signal.square
        t, y,  = ss.lsim((H.num, H.den), U=cuadrada, T=tin)  # Calculamos la Rta

    #else:
    # Cargar archivo de exitación. 

    return  t, y        


#Tests

my_data=getDataFromFile("inputExamples\Basuli.txt", 0)  #Montecarlo
#my_data=getDataFromFile("inputExamples\Ejemplo2-simulacion.txt", 0)  #No montecarlo
#my_data=getDataTeorica("1,1,0","1,1,1")

#print(my_data["amp"][4])
#print(len(my_data["frec"]))