import numpy as np
import pandas as pd
import scipy.signal as ss

# NO se usa
def getDataSpice(path):
    no_deseado=["(","\n",")","dB","°","Â"]
    file= open(path, "r")
    
    #Headers
    headers= file.readline().split("\t")
    headers[len(headers)-1]=headers[len(headers)-1].replace("\n","")
    
    #content
    signal={"frec":[], "amp":[], "phase":[]}

    lines= file.readlines()
    for line in lines:
        line=line.split("\t")

        signal["frec"].append(float(line[0]))
        bode= line[1]

        for caracter in no_deseado:
            bode = bode.replace(caracter,'')
        bode = bode.split(",")
        signal["amp"].append(float(bode[0]))
        signal["phase"].append(float(bode[1]))
    return signal

def getDataFromMonteCarlo(path):
    no_deseado=["(","\n",")","dB","°","Â"]  #Caracteres molesto del simulacion.txt
    file= open(path, "r")    

    #Headers
    headers= file.readline().split("\t")
    rawData= file.readlines()

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
                
                for linea in rawData[init:fin]:         # Para cada frecuencia de la Run
                    line=linea.split("\t")              # Separamos Frec de Bode
                    aux["frec"].append(float(line[0]))  # Appendamos la Frec al dict
                    bode= line[1]      
                
                    for caracter in no_deseado:
                        bode = bode.replace(caracter,'')    # Sacamos los caracteres molestos al dato del Bode(amp+fase)
                
                    bode = bode.split(",")                  # Separamos el bode en Amp y Fase
                    aux["amp"].append(float(bode[0]))       # Agregamos la Amp al dict 
                    aux["phase"].append(float(bode[1]))     # Agregamos la Fase al dict

                signal["frec"].append(aux["frec"])          # Apendeamos la frec de la run a la frec del dict de la señal
                signal["amp"].append(aux["amp"])            # Apendeamos la Amp de la run a la Amp del dict de la señal
                signal["phase"].append(aux["phase"])        # Apendeamos la fase de la run a la fase del dict de la señal
                
                init = index+1                              # Movemos el Inicio al primer dato de la prox Run

    return signal

def getDataMediciones(path):
    data = pd.read_csv(path)
    return data

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
    signal["frec"], signal["amp"], signal["phase"] = ss.bode(H) 

    return signal

#class Curve:

#Tests

#my_data=getDataFromMonteCarlo("Basuli.txt")
#my_data=getDataTeorica("1,1,0","1,1,1")
