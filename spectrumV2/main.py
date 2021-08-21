import matplotlib.pyplot as plt 
import numpy as np

f0 = 8e3
numMax=10
n = 2*np.linspace(1, numMax, num=numMax)-1
nLabels = np.array([1, 3, 5, 7, 9, 11, 15, 19])

labels = ['$'+str(int(i))+'f_0$' for i in nLabels]     # MODO SHERMAN
Xn = 1/n


fig, ax1 = plt.subplots()
color = 'tab:red'
R = 1e3
C = 10e-9
f = np.linspace(f0, n[len(n)-1]*f0, num=10000)
H = 20*np.log10(1/np.sqrt(np.pi**2*4*f**2*R**2*C**2 + 1))

Yn = 1/n * (1/np.sqrt(np.pi**2*4*n**2*f0**2*R**2*C**2 + 1))

ax1.plot(f, H, markersize=1.2, label='$|H(f)|$', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
ax2.stem(n*f0, Xn, basefmt="", label='$|X_n|$  normalizado')
plt.stem(n*f0, Yn, basefmt="C3-", label='$|Y_n|$ ', linefmt='C2-', markerfmt='C2o')
plt.xticks(nLabels*f0, labels, rotation='horizontal')
#ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()

ax1.set_xscale('log')
ax1.set_xlabel('Frecuencia $[Hz]$')
ax2.set_ylabel('Amplitud $[V]$')
ax1.set_ylabel('Amplitud $[dB]$')

#ax2.xlabel("$Frecuencia [Hz]$")
#ax2.ylabel("")
#ax2.legend()
ax1.grid(which="both")
plt.show()
