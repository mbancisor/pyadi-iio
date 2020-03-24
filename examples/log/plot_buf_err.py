import matplotlib.pyplot as plt
import numpy as np
import sys
from numpy import genfromtxt


if len(sys.argv) > 1:
    path=sys.argv[1]
    file_name = sys.argv[2]
else:
    print("Specify file name ... ")
    exit()
my_data = genfromtxt(path +'/'+ file_name, delimiter=',', dtype=complex)

plt.figure(0)
# plt.plot(my_data[0][:100], label="Chan1 SOM A")
# plt.plot(my_data[2][:100], label="Chan2 SOM A")
# plt.plot(my_data[4][:100], label="Chan1 SOM B")

plt.plot(my_data[0][:100], label="Chan1 SOM A")
plt.plot(my_data[1][:100], label="Chan2 SOM A")
plt.plot(my_data[2][:100], label="Chan3 SOM A")
plt.plot(my_data[3][:100], label="Chan4 SOM A")
plt.plot(my_data[4][:100], label="Chan1 SOM B")
plt.plot(my_data[5][:100], label="Chan2 SOM B")
plt.plot(my_data[6][:100], label="Chan3 SOM B")
plt.plot(my_data[7][:100], label="Chan4 SOM B")

plt.legend()
plt.draw()

plt.show()

