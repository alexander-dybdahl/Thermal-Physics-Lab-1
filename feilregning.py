import numpy as np


p = np.array([[9.3, 7.0, 3.2, 1.0],
            [14.0, 13.9, 4.7, 1.2],
            [20.2, 19.4, 6.5, 1.6],
            [21.2, 20.3, 6.6, 1.4]])



def gauss(V_surface, V_black):
    dV = 0.05
    
    error = np.sqrt((dV/V_black)**2 + (V_surface/V_black**2 * dV)**2)
    
    return error



p_error = np.zeros((4, 4))
p_relativ = np.zeros((4, 4))


for i in range(4):
    for j in range(4):
        p_relativ[i, j] = p[i,j]/p[i,0]
        p_error[i, j] = gauss(p[i,j], p[i,0])

print(p_relativ)

p_mean = np.zeros(4)
p_var = np.zeros(4)
for i in range(4):
    p_mean[i] = np.mean(p_relativ[:,i])
    p_var[i] = np.var(p_relativ[:,i])

print(p_mean)
print(p_error)
print(p_var)
