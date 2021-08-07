# Agregar a la estructura el calculo del transitorio transitorio.

import numpy as np
import pandas as pd
import scipy.signal as ss

def appendCurve(signal, aux):
    signal["frec"].append(aux["frec"])          # Apendeamos la frec de la run a la frec del dict de la señal
    signal["amp"].append(aux["amp"])            # Apendeamos la Amp de la run a la Amp del dict de la señal
    signal["phase"].append(aux["phase"])        # Apendeamos la fase de la run a la fase del dict de la señal
    return signal

# Te pasa los datos de UNA curva (no montecarlo) a un dict de arreglos(NO matrices) de datos
def Data2Dict(data):
    no_deseado=["(","\n",")","dB","°","Â"]
    aux = {"frec":[], "amp":[], "phase":[]} # Diccionario aux para manipular los datos
    
    for line in data:
        line=line.split("\t")                   # Separamos cada renglón en frecuencia, módulo y fase

        aux["frec"].append(float(line[0]))  # Agregamos la frec al arreglo de frecuencias
        bode= line[1]                            

        for caracter in no_deseado:
            bode = bode.replace(caracter,'')    # Remplazamos los caracteres molestos         
        bode = bode.split(",")                  # Separamos el bode en Amp y Fase
        aux["amp"].append(float(bode[0]))    # Agregamos la Amp al dict   
        aux["phase"].append(float(bode[1]))  # Agregamos la Fase al dict
        
    return aux

def getDataSpice(lines):  
    signal={"frec":[], "amp":[], "phase":[]}# Diccionario aux para manipular los datos
    aux = {"frec":[], "amp":[], "phase":[]} # Diccionario aux para manipular los datos

    aux = Data2Dict(lines)      # Dictionario con los arreglos de datos

    return appendCurve(signal, aux)

def getDataFromMonteCarlo(rawData):
    # Inicializamos variables
    signal={"frec":[], "amp":[], "phase":[]}
    init = -1
    fin = 0
    last=len(rawData)

    for index in range(last):

        if rawData[index][0:4] == "Step" or (index == last and rawData[index][0:4] != "Step"):
            if init == -1:      # Caso encuentro el Step de la primera Run
                init = index+1  # Seteo solamente el init
            
            else:
                fin = index                             # Determinamos el último punto a medir
                aux = {"frec":[], "amp":[], "phase":[]} # Diccionario aux para manipular los datos
                
                aux = Data2Dict(rawData[init:fin])
                signal = appendCurve(signal, aux)
                init = index+1                              # Movemos el Inicio al primer dato de la prox Run

    return signal

def getDataSimulation(path):
    file= open(path, "r")
    
    #Headers
    headers= file.readline().split("\t")
    headers[len(headers)-1]=headers[len(headers)-1].replace("\n","")

    signal={"frec":[], "amp":[], "phase":[]}

    data = file.readlines()
    if data[0][0:4] == "Step":
        signal = getDataFromMonteCarlo(data)
        print("MonteCarlo")
    else:
        signal = getDataSpice(data)
        print("Spice")

    return signal    

def getDataMediciones(path):
    data = (pd.read_csv(path)).to_numpy()       # Pasamos de .csv a matriz 

    signal = {"frec":[], "amp":[], "phase":[]}  # Dict para guardar la matriz de datas.
    aux = {"frec":[], "amp":[], "phase":[]}     # Diccionario aux para manipular los datos.

    filas= (data.shape)[0]
    for index in range(filas):
        aux["frec"].append(data[index][0])      # Para cada columna, appendeo TODOS los datos de cada una 
        aux["amp"].append(data[index][1])       # de sus filas en un arreglo distinto. 
        aux["phase"].append(data[index][2])

    return appendCurve(signal, aux)

def getCoef(listStr):
    # Pasa los coeficientes de array(String) a array(float)
    list=[]
    for index in range(len(listStr)):
        list.append(float(listStr[index]))
    return list

def getDataTeorica(Hnum, Hden):
    
    # Pasamos los coef del numerador a array(int)
    coefNumStr=Hnum.split(",")
    coefNum=getCoef(coefNumStr)

    # Pasamos los coef del denominador a array(int)
    coefDenStr=Hden.split(",")
    coefDen=getCoef(coefDenStr)
    
    # Armarmos la transferencia
    H = ss.TransferFunction(coefNum,coefDen)

    # Guardamos en un dic. el Bode del sistema
    signal = {"frec":[], "amp":[], "phase":[]}
    bode = ss.bode(H)

    signal["frec"].append(bode[0])
    signal["amp"].append(bode[1])
    signal["phase"].append(bode[2])

    return signal

#class Curve:

#Tests

my_data=getDataSimulation("inputExamples\Ejemplo1-simulacion.txt")
#my_data=getDataTeorica("1,1,0","1,1,1")
#my_data=getDataMediciones("inputExamples\Ejemplo2-medicion.csv")