import matplotlib.pyplot as plt
import numpy as np
import sys
from numpy import genfromtxt
import os

my_data = np.empty((0,9))

basepath = 'Weekend_log'
for fname in sorted(os.listdir(basepath)):
    path = os.path.join(basepath, fname)
    print(path)
    if os.path.isdir(path):
        dirList = os.listdir(path)
        if len(dirList) < 2:
            a = genfromtxt(path + '/log.csv', delimiter=',')
            my_data = np.append(my_data, a, axis=0)
            #continue


# if len(sys.argv) > 1:
#     path=sys.argv[1]
#     file_name = sys.argv[2]
# else:
#     print("Specify file name ... ")
#     exit()

# my_data = genfromtxt(path +'/'+ file_name, delimiter=',', dtype=complex)

# plt.figure(0)
# plt.plot(my_data[0][:100], label="Chan1 SOM A")
# plt.plot(my_data[2][:100], label="Chan2 SOM A")
# plt.plot(my_data[4][:100], label="Chan1 SOM B")
# plt.legend()
# plt.draw()
#
# my_data = genfromtxt(path + '/log.csv', delimiter=',')
# rx1rx2 = my_data[:,1]
# rx1rx3 = my_data[:,2]
# rx1rx5 = my_data[:,3]
#
#

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