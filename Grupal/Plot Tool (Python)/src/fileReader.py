import numpy as np

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
            # bode[0]=10**(float(bode[0])/20.0)    #Descomentar para escalas no logarítmicas
            aux["amp"].append(float(bode[0]))    # Agregamos la Amp al dict   
            
            #Limitamos el rango de la fase entre -180 y 180
            if float(bode[1]) > 180:
                bode[1] -= 360
            elif float(bode[1]) < -180:
                bode[1] +=360

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
    file.close()
    
    if "Step" in data[0]:
        signal = getDataFromMonteCarlo(data, modo)
    else:
        signal = getDataSpice(data, modo)

    return signal    

def getDataMediciones(path, modo):
    data = np.loadtxt(path, delimiter=',', skiprows=1)       # Pasamos de .csv a matriz 
    # data = (pd.read_csv(path)).to_numpy()       # Pasamos de .csv a matriz 

    signal = {"frec":[], "amp":[], "phase":[], "time":[], "y":[]}
    aux = {"frec":[], "amp":[], "phase":[], "time":[], "y":[]}  # Diccionario aux para manipular los datos.

    if modo == 0:
        aux["frec"] = data[:,0]      # Para cada columna, appendeo TODOS los datos de cada una 
        aux["amp"] = data[:,1]       # de sus filas en un arreglo distinto. 
        aux["phase"] = data[:,2]
    elif modo == 1:
        aux["time"] = data[:,0]      # Para cada columna, appendeo TODOS los datos de cada una 
        aux["y"] = data[:,1]         # de sus filas en un arreglo distinto. 
    
    # filas = (data.shape)[0]

    # for index in range(filas):
    #     if modo == 0:
    #         aux["frec"].append(data[index][0])      # Para cada columna, appendeo TODOS los datos de cada una 
    #         aux["amp"].append(data[index][1])       # de sus filas en un arreglo distinto. 
    #         aux["phase"].append(data[index][2])

    #     elif modo == 1:
    #         aux["time"].append(data[index][0])      # Para cada columna, appendeo TODOS los datos de cada una 
    #         aux["y"].append(data[index][1])         # de sus filas en un arreglo distinto. 

    return appendCurve(signal, aux, modo)

def getDataFromFile(path, modo):
    if ".txt" in path:
        signal = getDataSimulation(path, modo)
    elif ".csv" in path:
        signal = getDataMediciones(path, modo)
    
    return signal

# def getTransfFunct(numList, denList):
#     num=[]
#     for index in range(len(numList)):
#         num.append(float(numList[index]))

#     den=[]
#     for index in range(len(denList)):
#         den.append(float(denList[index]))

#     H = ss.TransferFunction(num,den)

#     return H

# def simBode(H, signal):
#     signal={"frec":[], "amp":[], "phase":[], "time":[], "y":[]}

#     frec=np.logspace(0, 7, num=int(1e4))               # Fijado de 1 Hz a 10 MHz
    
#     bode = ss.bode(H, w=2*np.pi*frec)                   # Calculamos el Bode
#     signal["frec"].append(frec)            

#     #for i in range(len(bode[1])):                       #Descomentar para transferencias no logaritmicas
#     #    bode[1][i]=10**(bode[1][i]/20)                  #Descomentar para transferencias no logaritmicas
    
#     signal["amp"].append(bode[1])                       # Guardamos el Bode
    
#     # aux=[]
#     # for elem in bode[2]:
#     #     #Limitamos el rango de la fase entre -180 y 180
#     #     if elem > 180:
#     #         aux.append(elem - 360)
#     #     elif elem < -180:
#     #         aux.append(elem + 360)
#     #     else:
#     #         aux.append(elem)

#     phase = bode[2]

#     phase[phase > 180] -= 360
#     phase[phase < -180] += 360

#     signal["phase"].append(phase)

#     return signal

# def getDataTeorica(H):
#     # Calculamos el Bode y lo appendeamos al dict
#     signal={"frec":[], "amp":[], "phase":[], "time":[], "y":[]}
#     signal = simBode(H, signal) 

#     return signal

if __name__ == '__main__':
    pass