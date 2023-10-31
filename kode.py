import numpy as np
import matplotlib.pyplot as plt

# Temperaturkoeffisienten til wolfram (K^-1)
alpha = 4.5 * 10**-3 

# Stefan-Boltzmanns konstant (W/m^2 K^4)
sigma = 5.67 * 10**-8

# Epsilon
epsilon = 0.95 # 3.7 * 10**-10

# Målt med Wheatstonebridge (Ohm)
R_0 = 0.350

# Romtemperatur (K)
T_0 = 22.2 + 273.15

# Spenning på strømforsyningen (V)
V = np.linspace(1,10,10)

# Spenning på sensor (mV)
V_s = np.array([0.1, 0.4, 0.9, 1.6, 2.5, 3.5, 4.6, 5.9, 7.4, 8.8]) * 10**-3

# Strøm må DMM (mV)
I = np.array([895, 1171, 1408, 1619, 1813, 1993, 2162, 2318, 2470, 2611]) * 10**-3

# Strøm på strømforsyningen (mV)
I_s = np.array([909, 1186, 1425, 1634, 1828, 2008, 2175, 2331, 2482, 2625]) * 10**-3

# Ohms lov for resistans (Ohm)
R  = V / I

# Relativ resistans
R_relativ = R / R_0

# Tabell verdier for relativ resistans (kK)
T_tabell =   np.array([800,    1100,    1300,    1500,    1600,    1800,    1900,    2000,   2100,    2150]) * 10**-3
T_tabell_2 = np.array([767.51, 1087.61, 1310.28, 1485.47, 1630.75, 1756.52, 1867.98, 1971.3, 2063.27, 2151.2])

# Temperatur ved å bruke T = T_0 + (R - R_0) / (alpha R_0)
T = T_0 + (R - R_0) / (alpha * R_0)

# Proporsjonalitetskonstant c
c = 0.5*10**4

# Stefan-Boltzmanns lov
j = c * epsilon * sigma * T_tabell**4


# plotting
plot = False



if plot:
    plt.figure()
    plt.title('Strålingsintensiteten som funksjon av glødetrådens temperatur')
    plt.loglog(T_tabell*10**3, V_s, label=r'$V_s(T)$ ved å bruke $T$ fra tabellen', color='g')
    plt.loglog(T_tabell*10**3, j, '--', label=r'Stefan-Boltzmanns lov: $j = c \epsilon \sigma T^4$', color='r')
    plt.loglog(T, V_s, label=r'$V_s(T)$ ved å bruke $T = T_0 + \frac{R-R_0}{\alpha R_0}$', color='b')
    plt.xlabel('T')
    plt.ylabel(r'Strålingsintensitet $V_s$')
    plt.legend()
    plt.grid()
    plt.savefig('Strålingsintensitet.png')
    plt.show()


# regresjonsplot for relativ resistans mellom 3 - 11
def T_func(x):
    return -1.84*x**2 + 204.54*x + 133.3

# rejustering til presis temperatur
justering = False

if justering:
    R_1 = 9.82*10**3
    R_3 = 94.1
    R_2 = 36.5 # målt verdi
    dR_2 = 0
    
    R_0_old = R_0
    R_0 = R_3 * R_2 / R_1 # lite å si for målt R_0
    dR_0 = abs(R_3 / R_1 * dR_2)
    print('R_0:\n', R_0, '+-', dR_0)
    
    R  = V / I
    R_relativ = R / R_0
    dR_relativ = np.mean(R / R_0**2 * dR_0)
    print('dR_relativ:\n', dR_relativ)

    T = T_0 + (R - R_0) / (alpha * R_0)
    dT_1 = np.sqrt((dR_0 / (alpha * R_0))**2 + (R_0 / (alpha * R_0**2) * dR_0)**2)
    print('dT_1:\n', dT_1)
    
    dT_2 = np.mean(abs(- 2 * 1.84 * R_relativ + 204.54) * dR_relativ)
    print('dT_2:\n', dT_2)
    
    T_tabell_old = T_tabell * 10**3
    T_tabell = T_func(R_relativ)
    j = c * epsilon * sigma * T_tabell**4

    dT_arr = np.zeros(len(T_tabell))
    for i in range(len(T_tabell)):
        dT = abs(T_tabell[i] - T_tabell_old[i])
        dT_arr[i] = dT

    dT_3 = np.mean(dT_arr)
    print('forskjell i temperatur:\n', dT_3, '+-', np.std(dT_arr))
    
    dV = 0.05
    dT = 0
    print('total dT:\n', dT)
    a = V_s[-1] * 10**3
    b = V_s[0] * 10**3
    c = T_tabell[-1]
    d = T_tabell[0]
else:
    dV = 0.05 * 10**-3
    dT = 50 * 10**-3
    
    a = V_s[-1]
    b = V_s[0]
    c = T_tabell[-1]
    d = T_tabell[0]

# feilanalyse

p = np.sqrt((dV/(a*np.log(c/d)))**2 + (dV/(b*np.log(c/d)))**2 + (dT*np.log(a/b)/(c*np.log(c/d)**2))**2 + (dT*np.log(a/b)/(d*np.log(c/d)**2))**2)
print('feil i stigningstall:\n', p)

dT = 25 * 10**-3
p1 = np.sqrt((dV/(a*np.log(c/d)))**2 + (dV/(b*np.log(c/d)))**2 + (dT*np.log(a/b)/(c*np.log(c/d)**2))**2 + (dT*np.log(a/b)/(d*np.log(c/d)**2))**2)
print('feil grunnet dR_2:\n', abs(p1-p))

# feil start/slutt
c1 = (np.log(V_s[-1]/V_s[0]))/(np.log(T_tabell[-1]/T_tabell[0]))
c2 = (np.log(j[-1]/j[0]))/(np.log(T_tabell[-1]/T_tabell[0]))
c3 = (np.log(V_s[-1]/V_s[0]))/(np.log(T[-1]/T[0]))

print('stigning start/slutt:\n', c1, c2, c3)

# feil hvert punkt
arr = np.zeros(len(V_s)-1)
for i in range(1, len(V_s)):
    arr[i-1] = np.log(V_s[i]/V_s[i-1])/np.log(T_tabell[i]/T_tabell[i-1])

# gjennomsnitt
print('stigning punktvis:\n', np.mean(arr))

# varians
print('standardavvik:\n', np.sqrt(np.var(arr)))


# feilanalyse for blå graf

a = V_s[-1] * 10**3
b = V_s[0] * 10**3
c = T[-1]
d = T[0]
dV = 0.05
dT = 50

p = np.sqrt((dV/(a*np.log(c/d)))**2 + (dV/(b*np.log(c/d)))**2 + (dT*np.log(a/b)/(c*np.log(c/d)**2))**2 + (dT*np.log(a/b)/(d*np.log(c/d)**2))**2)
print('feil i stigningstall:\n', p)


