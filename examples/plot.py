import matplotlib.pyplot as plt
import numpy as np
import sys
from numpy import genfromtxt

if len(sys.argv) > 1:
    file_name=sys.argv[1]
else:
    print("Specify file name ... ")
    exit()
my_data = genfromtxt(file_name, delimiter=',')
rx1rx2 = my_data[:,1]
rx1rx3 = my_data[:,2]
rx1rx5 = my_data[:,3]



l = np.linspace(1, len(my_data), num = len(my_data))


mean = my_data[:,0]
mini = np.abs(mean - my_data[:,1])
maxi = np.abs(my_data[:,2] - mean)
err = np.vstack((mini,maxi))

plt.figure(1)
plt.errorbar(l, mean, yerr = err, xerr = None, label="Chan1-2 SOM A")
plt.legend()
plt.draw()

mean = my_data[:,3]
mini = np.abs(mean - my_data[:,4])
maxi = np.abs(my_data[:,5] - mean)
err = np.vstack((mini,maxi))

plt.figure(2)
plt.errorbar(l, mean, yerr = err, xerr = None, label="Chan1-3 SOM A")
plt.legend()
plt.draw()

mean = my_data[:,6]
mini = np.abs(mean - my_data[:,7])
maxi = np.abs(my_data[:,8] - mean)
err = np.vstack((mini,maxi))

plt.figure(3)
plt.errorbar(l, mean, yerr = err, xerr = None, label="Chan1 SOM A-B")
plt.legend()
plt.draw()




plt.show()
