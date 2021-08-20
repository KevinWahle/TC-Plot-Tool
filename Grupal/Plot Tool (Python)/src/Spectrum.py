import matplotlib.pyplot as plt 
import numpy as np

f0 = 8e3
numMax=10
n = 2*np.linspace(1, numMax, num=numMax)-1
nLabels = np.array([1, 3, 5, 7, 9, 11, 15, 19])

labels = ['$'+str(int(i))+'f_0$' for i in nLabels] # MODO SHERMAN
Xn = 20*np.log10(1/n)
plt.stem(n*f0, Xn, basefmt="", label='$|X_n|$  normalizado')

R = 1e3
C = 10e-9
f = np.linspace(1*f0, n[len(n)-1]*f0, num=10000)
H = 20*np.log10(1/np.sqrt(np.pi**2*4*f**2*R**2*C**2 + 1))
plt.plot(f, H, marker="o", markersize=1.2, label='$|H(f)|$')

plt.xscale("log")
plt.xticks(nLabels*f0, labels, rotation='horizontal')
plt.xlabel("$Frecuencia [Hz]$")
plt.ylabel("")
plt.legend()
plt.grid(which="both")
plt.show()