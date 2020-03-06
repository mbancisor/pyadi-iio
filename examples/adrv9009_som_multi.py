# type: ignore

import time
import datetime
import os
import sys

import adi
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
from scipy import signal
import csv



def measure_phase_and_delay(chan0, chan1, window=None):
    assert len(chan0) == len(chan1)
    if window == None:
        window = len(chan0)
    phases = []
    delays = []
    indx = 0
    sections = len(chan0) // window
    for sec in range(sections):
        chan0_tmp = chan0[indx : indx + window]
        chan1_tmp = chan1[indx : indx + window]
        indx = indx + window + 1
        cor = np.correlate(chan0_tmp, chan1_tmp, "full")
        # plt.plot(np.real(cor))
        # plt.plot(np.imag(cor))
        # plt.plot(np.abs(cor))
        # plt.show()
        i = np.argmax(np.abs(cor))
        m = cor[i]
        sample_delay = len(chan0_tmp) - i - 1
        phases.append(np.angle(m) * 180 / np.pi)
        delays.append(sample_delay)
    return (np.mean(phases), np.mean(delays))


def measure_phase(chan0, chan1):
    assert len(chan0) == len(chan1)
    errorV = np.angle(chan0 * np.conj(chan1)) * 180 / np.pi
    error = np.mean(errorV)
    return error


buff_size = 2 ** 14

no_of_runs = 1
if(len(sys.argv)>1):
    no_of_runs = int(sys.argv[1])

now=datetime.datetime.now()
now_str=now.strftime("%Y-%m-%d-%H-%M-%S")
log_path=os.getcwd()+"/log/"+now_str+'/'
print("Creating logs in - ", log_path)
os.makedirs(log_path)

for run_no in range(no_of_runs):

    # Create radio
    # def run_dev():
    master = "ip:192.168.1.60"
    slave = "ip:192.168.1.61"

    #master = "ip:10.48.65.100"
    #slave = "ip:10.48.65.107"

    print("--Connecting to devices")
    multi = adi.adrv9009_zu11eg_multi(master, [slave])
    # multi._dma_show_arming = True
    multi.rx_buffer_size = 2 ** 12

    # Configure LOs
    multi.master.trx_lo = 1228800000
    multi.master.trx_lo_chip_b = 1228800000

    for slave in multi.slaves:
        slave.trx_lo = 1228800000
        slave.trx_lo_chip_b = 1228800000

    multi.master.dds_single_tone(30000, 0.8)

    log = [[], [], []]

    for r in range(5):
        #time.sleep(0.1)
        # Collect data
        print("Pulling buffers")
        x = multi.rx()
        rx1rx2 = measure_phase(x[0], x[1])
        rx1rx3 = measure_phase(x[0], x[2])
        if (rx1rx3 > 9 or rx1rx3 < 5):
            input("Press Enter to continue...")
        rx1rx5 = measure_phase(x[0], x[4])
        if (rx1rx5 > -45 or rx1rx5 < -53):
            input("Press Enter to continue...")
        log[0].append(rx1rx2)
        log[1].append(rx1rx3)
        log[2].append(rx1rx5)

        print("###########")
        print("Same Chip       ", rx1rx2)
        print("Across Chip     ", rx1rx3)

        print("Across SOMS (AB)", rx1rx5)
        print("###########")
    #    (p, s) = measure_phase_and_delay(x[0], x[1])
    #    print("Same Chip Sample delay       :", s)
    #    (p, s) = measure_phase_and_delay(x[0], x[2])
    #    print("Across Chips Sample delay    :", s)
    #    (p, s) = measure_phase_and_delay(x[0], x[4])
    #    print("Across SOMS (AB) Sample delay:", s)
    #    # print("Phase delay: ",p)
    #    print("------------------")

        log_file_name="buffers_"+str(run_no)+".csv"
        log_file_path=log_path+log_file_name
        np.savetxt(log_file_path, x, delimiter=",")
        log_file_name="jesd_link_"+str(run_no)+".txt"
        log_file_path=log_path+log_file_name
        with open(log_file_path, 'w') as f:
            f.write(multi._adrv9009_zu11eg_multi__read_all_jesd_status())


        plt.clf()
        plt.plot(x[0][:100], label="Chan1 SOM A")
        plt.plot(x[2][:100], label="Chan2 SOM A")
        plt.plot(x[4][:100], label="Chan1 SOM B")
        plt.legend()
        plt.draw()
        plt.pause(0.1)
    #print(log)
    fields = []
    fields.append(sum(log[0]) / len(log[0]))
    fields.append(min(log[0]))
    fields.append(max(log[0]))
    fields.append(sum(log[1]) / len(log[1]))
    fields.append(min(log[1]))
    fields.append(max(log[1]))
    fields.append(sum(log[2]) / len(log[2]))
    fields.append(min(log[2]))
    fields.append(max(log[2]))
    with open(r'log.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    plt.show(block=False)
    plt.pause(2)
    plt.close()

    del multi
