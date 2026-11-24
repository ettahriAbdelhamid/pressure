import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def autoCorrFunc(data, k):
    data = np.asarray(data, dtype=np.float32)
    mean = data.mean()
    data-=mean 
    N=len(data)

    
    num=sum([
        (data[i])*(data[i+k])
        for i in range(len(data)-k)
    ])/N
    den =sum([
        (x)**2
        for x in data
    ])/(N-k)
    
    return num/den
    
M=10000
stepsize = 0.5
array=[0]
np.random.seed(0)
for i in range(M):
    array.append(stepsize*(np.random.random()-0.5))


rho = np.array([
    autoCorrFunc(array, k)
    for k in range(1000)
])
    

plt.figure()
plt.plot(rho)
plt.savefig("test3.png")
plt.close()

plt.figure()
plt.plot(array)
plt.savefig("test4.png")
plt.close()
