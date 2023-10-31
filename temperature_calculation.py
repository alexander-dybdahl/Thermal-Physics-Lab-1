import numpy as np


R_0 = 0.350
V = np.linspace(1,10,10)
V_s = np.array([0.1, 0.4, 0.9, 1.6, 2.5, 3.5, 4.6, 5.9, 7.4, 8.8]) * 10**-3
I = np.array([895, 1171, 1408, 1619, 1813, 1993, 2162, 2318, 2470, 2611]) * 10**-3
R  = V / I
R_relativ = R / R_0
T_tabell_1 = np.array([800, 1100, 1300, 1500, 1600, 1800, 1900, 2000, 2100, 2150]) * 10**-3


def T(x):
    return -1.84*x**2 + 204.54*x + 133.3

T_tabell = T(R_relativ)

for i in T_
print(T_tabell)
