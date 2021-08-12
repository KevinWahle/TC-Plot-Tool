import matplotlib.pyplot as plt
from Curve import *
from Excitation import *

fig1, axAmp = plt.subplots()
fig2, axPh = plt.subplots()
fig3, axRta = plt.subplots()

axis=[axAmp, axPh, axRta]
curves =    [Curve(nombre="Montecarlo", Hnum="", Hden="", path='inputExamples/montecarlo-simulacion.txt', modo=0),
            Curve(nombre="Sim", Hnum="", Hden="", path='inputExamples/Ejemplo1-simulacion.txt', modo=0),
            Curve(nombre="Med", Hnum="", Hden="", path='inputExamples/Ejemplo1-medicion.csv', modo=0),
            Curve(nombre="Teórica", Hnum=[1], Hden=[1,2,1], path='', modo=0)
            ]
exitaciones = [Excitation(name ="escalón", type=0, amp=1, freq=0, freqType='F', duty=1)]

graphCurves(curves=curves, axes=axis, exitaciones = exitaciones, frec=1)

plt.show()