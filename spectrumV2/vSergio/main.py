import matplotlib.pyplot as plt 
import numpy as np

# plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
# plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True

f0 = 8e3
numMax=20
n = 2*np.array(range(1,numMax))-1
nLabels = np.array(range(1,n[-1],2))

labels = ['$'+str(int(i))+'f_0$' if i != 1 else '$f_0$' for i in nLabels]     # MODO SHERMAN
Xn = np.full(len(n), -90)

fig, ax1 = plt.subplots()
color = 'tab:red'
R = 1e3
C = 10e-9
f = np.linspace(1e3, n[len(n)-1]*f0, num=10000)
H = - np.arctan(2 * np.pi * f * R * C) * 180 / np.pi

# Yn = 1/(np.pi*n) * (6/np.sqrt(np.pi**2*4*n**2*f0**2*R**2*C**2 + 1))
Yn = Xn - np.arctan(2 * np.pi * n* f0 * R * C) * 180 / np.pi


ax1.plot(f, H, markersize=1.2, label='$Arg(H(f))$', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
ax2.stem(n*f0, Yn, basefmt="black", label='$Arg(Y_n)$ ', linefmt='C2-', markerfmt='C2o')
ax2.stem(n*f0, Xn, basefmt="black", label='$Arg(X_n)$')

#ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()

ax1.set_xscale('log')
ax1.set_xlabel('Frecuencia $[Hz]$')
ax2.set_ylabel('Fase $[°]$')
ax1.set_ylabel('Fase $[°]$')

# ax2.set_xticks(nLabels[:6]*f0)
# ax2.set_xticklabels(labels[:6])

secax = ax2.secondary_xaxis('top')

secax.set_xticks(nLabels[:6]*f0)
secax.set_xticklabels(labels[:6])


# plt.xticks(nLabels[:10]*f0, labels[:10], rotation='horizontal')
# plt.setp(ax2.get_xticklabels(), visible=True)

#ax2.xlabel("$Frecuencia [Hz]$")
#ax2.ylabel("")
#ax2.legend()
ax1.grid(which="both")

ax2.plot([],[], color=color, label='$Arg(H(f))$')
ax2.legend()
plt.show()
