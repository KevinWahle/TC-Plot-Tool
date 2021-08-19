import matplotlib.pyplot as plt 
import numpy as np

f0 = 8e3
numMax=10
n = 2*np.linspace(1, numMax, num=numMax)-1
labels = ['$'+str(int(i))+'f_0$' for i in n] # MODO SHERMAN
Xn = 20*np.log10(1/n)

f = np.linspace(1*f0, n[len(n)-1]*f0, num=1000000)
R = 1e3
C = 10e-9
H = 20*np.log10(1/np.sqrt(np.pi**2*4*f**2*R**2*C**2 + 1))

plt.xticks(n*f0, labels, rotation='horizontal')
plt.stem(n*f0, Xn, basefmt="", label='$|X_n|$  normalizado')
plt.plot(f, H, marker="o", markersize=1.2, label='$|H(f)|$')
plt.xlabel("$f[Hz]$")
plt.ylabel("")

plt.title("")
plt.legend()
plt.grid(which="both")
plt.show()