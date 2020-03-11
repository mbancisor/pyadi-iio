import matplotlib.pyplot as plt
import numpy as np
import sys
from numpy import genfromtxt

def mean_err(idx,my_data):
    mean = my_data[:, idx]
    mini = np.abs(mean - my_data[:, idx + 1])
    maxi = np.abs(my_data[:, idx + 2] - mean)
    err = np.vstack((mini, maxi))
    return mean, err

if len(sys.argv) > 1:
    path=sys.argv[1]
#    file_name = sys.argv[2]
else:
    print("Specify file name ... ")
    exit()
#my_data = genfromtxt(path +'/'+ file_name, delimiter=',', dtype=complex)

#plt.figure(0)
#plt.plot(my_data[0][:100], label="Chan1 SOM A")
#plt.plot(my_data[2][:100], label="Chan2 SOM A")
#plt.plot(my_data[4][:100], label="Chan1 SOM B")
#plt.legend()
#plt.draw()
#my_data = genfromtxt(path + '/log.csv', delimiter=',')
my_data = genfromtxt('log.csv', delimiter=',')
rx1rx2 = my_data[:,1]
rx1rx3 = my_data[:,2]
rx1rx5 = my_data[:,3]


plt.figure(1)
l = np.linspace(1, len(my_data), num = len(my_data))

plt.figure(1)

idx = 0
mean, err = mean_err(idx,my_data)
plt.errorbar(l, mean, yerr = err, xerr = None, label="Chan1-2 SOM A")
idx += 3
mean, err = mean_err(idx,my_data)
plt.errorbar(l, mean, yerr = err, xerr = None, label="Chan3-4 SOM A")
idx += 3
mean, err = mean_err(idx,my_data)
plt.errorbar(l, mean, yerr = err, xerr = None, label="Chan1-2 SOM B")
idx += 3
mean, err = mean_err(idx,my_data)
plt.errorbar(l, mean, yerr = err, xerr = None, label="Chan3-4 SOM B")

plt.legend()
plt.draw()

plt.figure(2)
idx += 3
mean, err = mean_err(idx,my_data)
plt.errorbar(l, mean, yerr = err, xerr = None, label="Chan1-3 SOM A")
idx += 3
mean, err = mean_err(idx,my_data)
plt.errorbar(l, mean, yerr = err, xerr = None, label="Chan1-3 SOM B")

plt.legend()
plt.draw()


plt.figure(3)
idx += 3
mean, err = mean_err(idx,my_data)
plt.errorbar(l, mean, yerr = err, xerr = None, label="SOM AB 1")
idx += 3
mean, err = mean_err(idx,my_data)
plt.errorbar(l, mean, yerr = err, xerr = None, label="SOM AB 2")
plt.draw()




plt.show()