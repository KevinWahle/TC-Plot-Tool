import matplotlib.pyplot as plt 
import numpy as np

Vp = 3
f0 = 8e3                                        # Frecuencia natural
numMax=10                                       # Cantidad de frecs a plottear
n = 2*np.linspace(1, numMax, num=numMax)-1      # Multiplos de f0 a plottear
nLabels = np.array([1, 3, 5, 7, 9, 11, 13, 15, 17, 19]) # Multiplos de f0 a utilizar como Label

labels = ['$'+str(int(i))+'f_0$' for i in nLabels]  # Generación de labels
Xbn = 4*Vp/(np.pi*n)                                # Calculo de Coef de Fourier

R = 1e3
C = 10e-9
f = np.linspace(1*f0, n[len(n)-1]*f0, num=10000)        # Puntos en frec a plottear el |H|[dB] 
H = 1/np.sqrt((2*np.pi*f*R*C)**2 + 1)                   # Calculo |H| en veces
Hdb = 20*np.log10(H)                                    # Calculo |H|[dB]
Ybn= Xbn * 1/np.sqrt((2*np.pi*f0*n*R*C)**2 + 1)           # Calculo los coef de la salida Y

fig, axH = plt.subplots()                               # Seteo los ejes y los ticks
axH.set_xscale("log")                   
plt.xticks(nLabels*f0, labels, rotation='vertical')
axSpect = axH.twinx()

c1, = axH.plot(f, Hdb, label='$|H(f)|$', color="m")           # Plotteo |H|[dB]
c2 = axSpect.stem(n*f0, Xbn, basefmt="dimgray", label='$|X_n|$', 
            linefmt='r-', markerfmt='ro')               # Realizo el diagrama espectral de la entrada
c3 = axSpect.stem(n*f0, Ybn, basefmt="dimgray", label='$|Y_n|$ ', 
            linefmt='b-', markerfmt='bo')               # Realizo el diagrama espectral de la salida

axH.tick_params(axis='y', labelcolor="m")
axH.set_xlabel("$Frecuencia [Hz]$")                     # Seteo de Labels
axH.set_ylabel("Amplitud [dB]", color="m")
axSpect.set_ylabel("Amplitud [V]")
plt.title("Diagrama espectral vs $H(f)$")               # Seteo de títulos
axH.grid(which="major")                                 # Seteos secundarios
axH.legend(handles=[c1, c2, c3])
plt.tight_layout()
plt.show()