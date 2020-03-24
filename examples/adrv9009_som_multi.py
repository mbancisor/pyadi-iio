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

plt.figure(1)
def measure_phase(chan0, chan1):
    assert len(chan0) == len(chan1)
    errorV = np.angle(chan0 * np.conj(chan1)) * 180 / np.pi
    error = np.mean(errorV)
    return error


def out_of_range(measure, value, tolerance):
    if measure < (value - tolerance) or measure > (value + tolerance):
        return True
    return False

buff_size = 2 ** 12

no_of_runs = 1
if(len(sys.argv)>1):
    no_of_runs = int(sys.argv[1])

now=datetime.datetime.now()
now_str=now.strftime("%Y-%m-%d-%H-%M-%S")
log_path=os.getcwd()+"/log/"+now_str+'/'
print("Creating logs in - ", log_path)
os.makedirs(log_path)


def log_debug_info(multi, run_no,subrun_no, x):
    log_file_name = "buffers_" + str(run_no) + "_" + str(subrun_no) + ".csv"
    log_file_path = log_path + log_file_name
    np.savetxt(log_file_path, x, delimiter=",")
    log_file_name = "jesd_link_" + str(run_no) + "_" + str(subrun_no) + ".txt"
    log_file_path = log_path + log_file_name
    with open(log_file_path, 'w') as f:
        f.write(multi._adrv9009_zu11eg_multi__read_all_jesd_status())

    iio_regs_str = multi._adrv9009_zu11eg_multi__read_adrv9009_all_regs()
    log_file_name = "iio_regs_" + str(run_no) + "_" + str(subrun_no) + ".txt"
    log_file_path = log_path + log_file_name
    with open(log_file_path, "w") as f:
        f.write(iio_regs_str);


for run_no in range(no_of_runs):

    # Create radio
    # def run_dev():
    master = "ip:192.168.0.60"
    slave = "ip:192.168.0.61"

    #master = "ip:10.48.65.100"
    #slave = "ip:10.48.65.107"

    print("--Connecting to devices  ", run_no)
    for k in range(10):
        try:
            multi = adi.adrv9009_zu11eg_multi(master, [slave])
            break
        except:
            time.sleep(2)
            pass

#    print("--Connecting to devices")
#    multi = adi.adrv9009_zu11eg_multi(master, [slave])
    # multi._dma_show_arming = True
    multi.rx_buffer_size = 2 ** 12

    # Configure LOs
    multi.master.trx_lo = 1228800000
    multi.master.trx_lo_chip_b = 1228800000

    for slave in multi.slaves:
        slave.trx_lo = 1228800000
        slave.trx_lo_chip_b = 1228800000

    multi.master.dds_single_tone(4000000, 1)

    test_log_file_name = "log.csv"
    test_log_file_path = log_path + test_log_file_name

    test_log_file_name_1 = "log1.csv"
    test_log_file_path_1 = log_path + test_log_file_name_1


    log = [[], [], [], [], [], [], [], []]
    log1 = [[], [], [], [], [], [], [], []]

    for r in range(5):
        #time.sleep(0.1)
        # Collect data
        print("Pulling buffers")
        x = multi.rx()
        #single chip phase
        rx1rx2 = measure_phase(x[0], x[1])
        rx3rx4 = measure_phase(x[2], x[3])
        rx5rx6 = measure_phase(x[4], x[5])
        rx7rx8 = measure_phase(x[6], x[7])
        #phase across chips
        rx1rx3 = measure_phase(x[0], x[2])
        rx5rx7 = measure_phase(x[4], x[6])
        #phase across SOMS
        rx1rx5 = measure_phase(x[0], x[4])
        rx3rx7 = measure_phase(x[2], x[6])
# Setup2 1.2288 G
        # if out_of_range(rx1rx2, 0.5, 2) or \
        #     out_of_range(rx3rx4, 3.5, 2) or \
        #     out_of_range(rx5rx6, 0.5, 2) or \
        #     out_of_range(rx7rx8, -0.8, 2) or \
        #     out_of_range(rx1rx3, -26, 3) or \
        #     out_of_range(rx5rx7, -31, 3) or \
        #     out_of_range(rx1rx5, 39, 4) or \
        #     out_of_range(rx3rx7, 37, 4):
        #     log_debug_info(multi, run_no, r, x)
# Setup2 1 G
        if out_of_range(rx1rx2, 13.0, 2) or \
            out_of_range(rx3rx4, 1.5, 2) or \
            out_of_range(rx5rx6, 3.0, 2) or \
            out_of_range(rx7rx8, 8.0, 2) or \
            out_of_range(rx1rx3, -28.0, 3) or \
            out_of_range(rx5rx7, -9.0, 3) or \
            out_of_range(rx1rx5, -48.0, 4) or \
            out_of_range(rx3rx7, -28.0, 4):
            log_debug_info(multi, run_no, r, x)

        # if rx1rx2 > 1.5 or rx1rx2 < -1.5 or rx1rx3 > -22 or rx1rx3 < -32 or rx1rx5 > 42 or rx1rx5 < 32:
        # input("Press Enter to continue...")

        log[0].append(rx1rx2)
        log[1].append(rx3rx4)
        log[2].append(rx5rx6)
        log[3].append(rx7rx8)
        log[4].append(rx1rx3)
        log[5].append(rx5rx7)
        log[6].append(rx1rx5)
        log[7].append(rx3rx7)

        print("###########")
        print("Same Chip1 SOM1      ", rx1rx2)
        print("Same Chip2 SOM1      ", rx3rx4)

        print("Same Chip1 SOM2      ", rx5rx6)
        print("Same Chip2 SOM2      ", rx7rx8)

        print("Across Chip SOM1     ", rx1rx3)
        print("Across Chip SOM2     ", rx5rx7)

        print("Across SOMS1(AB)     ", rx1rx5)
        print("Across SOMS2(AB)     ", rx3rx7)
        print("###########")

        # plt.clf()
        # plt.plot(x[0][:100], label="Chan1 SOM A")
        # plt.plot(x[1][:100], label="Chan2 SOM A")
        # plt.plot(x[2][:100], label="Chan3 SOM A")
        # plt.plot(x[3][:100], label="Chan4 SOM A")
        # plt.plot(x[4][:100], label="Chan1 SOM B")
        # plt.plot(x[5][:100], label="Chan2 SOM B")
        # plt.plot(x[6][:100], label="Chan3 SOM B")
        # plt.plot(x[7][:100], label="Chan4 SOM B")

        #
        # plt.legend()
        # plt.draw()
        # plt.pause(0.1)

    fields = []
    #chip 1
    fields.append(sum(log[0]) / len(log[0]))
    fields.append(min(log[0]))
    fields.append(max(log[0]))
    #chip 2
    fields.append(sum(log[1]) / len(log[1]))
    fields.append(min(log[1]))
    fields.append(max(log[1]))
    #chip 3
    fields.append(sum(log[2]) / len(log[2]))
    fields.append(min(log[2]))
    fields.append(max(log[2]))
    #chip 4
    fields.append(sum(log[3]) / len(log[3]))
    fields.append(min(log[3]))
    fields.append(max(log[3]))
    #SOM1
    fields.append(sum(log[4]) / len(log[4]))
    fields.append(min(log[4]))
    fields.append(max(log[4]))
    #SOM2
    fields.append(sum(log[5]) / len(log[5]))
    fields.append(min(log[5]))
    fields.append(max(log[5]))
    #system
    fields.append(sum(log[6]) / len(log[6]))
    fields.append(min(log[6]))
    fields.append(max(log[6]))
    fields.append(sum(log[7]) / len(log[7]))
    fields.append(min(log[7]))
    fields.append(max(log[7]))

    #with open(test_log_file_path, 'a') as f:
    with open(r'log/log.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    with open(test_log_file_path, 'a') as f1:
        writer = csv.writer(f1)
        writer.writerow(fields)
#=========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================

    for r in range(5):
        #time.sleep(0.1)
        # Collect data
        print("Pulling buffers")
        x = multi.rx1()
        #single chip phase
        rx1rx2 = measure_phase(x[0], x[1])
        rx3rx4 = measure_phase(x[2], x[3])
        rx5rx6 = measure_phase(x[4], x[5])
        rx7rx8 = measure_phase(x[6], x[7])
        #phase across chips
        rx1rx3 = measure_phase(x[0], x[2])
        rx5rx7 = measure_phase(x[4], x[6])
        #phase across SOMS
        rx1rx5 = measure_phase(x[0], x[4])
        rx3rx7 = measure_phase(x[2], x[6])

        log1[0].append(rx1rx2)
        log1[1].append(rx3rx4)
        log1[2].append(rx5rx6)
        log1[3].append(rx7rx8)
        log1[4].append(rx1rx3)
        log1[5].append(rx5rx7)
        log1[6].append(rx1rx5)
        log1[7].append(rx3rx7)

        print("###########")
        print("Same Chip1 SOM1      ", rx1rx2)
        print("Same Chip2 SOM1      ", rx3rx4)

        print("Same Chip1 SOM2      ", rx5rx6)
        print("Same Chip2 SOM2      ", rx7rx8)

        print("Across Chip SOM1     ", rx1rx3)
        print("Across Chip SOM2     ", rx5rx7)

        print("Across SOMS1(AB)     ", rx1rx5)
        print("Across SOMS2(AB)     ", rx3rx7)
        print("###########")

        # plt.clf()
        # plt.plot(x[0][:100], label="Chan1 SOM A")
        # plt.plot(x[1][:100], label="Chan2 SOM A")
        # plt.plot(x[2][:100], label="Chan3 SOM A")
        # plt.plot(x[3][:100], label="Chan4 SOM A")
        # plt.plot(x[4][:100], label="Chan1 SOM B")
        # plt.plot(x[5][:100], label="Chan2 SOM B")
        # plt.plot(x[6][:100], label="Chan3 SOM B")
        # plt.plot(x[7][:100], label="Chan4 SOM B")

        #
        # plt.legend()
        # plt.draw()
        # plt.pause(0.1)

    fields = []
    #chip 1
    fields.append(sum(log1[0]) / len(log1[0]))
    fields.append(min(log1[0]))
    fields.append(max(log1[0]))
    #chip 2
    fields.append(sum(log1[1]) / len(log1[1]))
    fields.append(min(log1[1]))
    fields.append(max(log1[1]))
    #chip 3
    fields.append(sum(log1[2]) / len(log1[2]))
    fields.append(min(log1[2]))
    fields.append(max(log1[2]))
    #chip 4
    fields.append(sum(log1[3]) / len(log1[3]))
    fields.append(min(log1[3]))
    fields.append(max(log1[3]))
    #SOM1
    fields.append(sum(log1[4]) / len(log1[4]))
    fields.append(min(log1[4]))
    fields.append(max(log1[4]))
    #SOM2
    fields.append(sum(log1[5]) / len(log1[5]))
    fields.append(min(log1[5]))
    fields.append(max(log1[5]))
    #system
    fields.append(sum(log1[6]) / len(log1[6]))
    fields.append(min(log1[6]))
    fields.append(max(log1[6]))
    fields.append(sum(log1[7]) / len(log1[7]))
    fields.append(min(log1[7]))
    fields.append(max(log1[7]))

    #with open(test_log_file_path, 'a') as f:
    with open(r'log/log1.csv', 'a') as f2:
        writer = csv.writer(f2)
        writer.writerow(fields)
    with open(test_log_file_path_1, 'a') as f3:
        writer = csv.writer(f3)
        writer.writerow(fields)






    # =========================================================================================================================
    # =========================================================================================================================
    # =========================================================================================================================

    # plt.show(block=False)
    # plt.pause(2)
    # plt.close()

    del multi
