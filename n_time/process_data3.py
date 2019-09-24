import matplotlib
# matplotlib.use('TkAgg')

# matplotlib.use('agg')

import matplotlib.pyplot as plt
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

plt.rcParams["figure.figsize"] = [16, 10]

def nano_read(nano):
    dt = datetime.datetime.fromtimestamp(nano / 1e9)
    return '{}{:03.0f}'.format(dt.strftime('%Y-%m-%d %H:%M:%S.%f'), nano % 1e3)


def process_memory(time_phase, file, output_file, title_name, container_name):
    count = 0
    count_measurement = 0
    list_x = []
    list_y = []
    temp = 0
    time_phase_temp = []

    with open(file) as f:
        for line in f:
            line = line.split(" ")
            count += 1
            if count == 1:
                list_x.append(int(line[0]))
            elif count == 2:
                temp = int(line[0])
                temp = (temp / 1048576.0)
                list_y.append(temp)
                temp = 0
                count_measurement += 1
                count = 0
    f.close()
    start = list_x[0]
    max_index = list_y.index(max(list_y))
    min_index = list_y.index(min(list_y))
    time_max = list_x[max_index]
    time_min = list_x[min_index]
    for k in range(len(list_x)):
        if k == 0:
            list_x[k] = 0
        else:
            list_x[k] = (list_x[k] - start) / 1000000000.0
    for k in range(len(time_phase)):
        time_phase_temp.append((int(time_phase[k]) - start) / 1000000000.0)

    fig, ax = plt.subplots(1, 1)
    ax.plot(list_x, list_y)
    ax.set_xlabel("Time relatives to start time(s)")
    ax.set_ylabel("Memory usage(MB)")
    ax.set_title("Memory usage of " + title_name, y=1.08)

    # plt.text(0, 0, 'matplotlib', ha='center', va='center', transform=ax.transAxes)
    # plt.xticks([0], [nano_read(start)])
    # 1568551346332221200, 1568551351300437000, 1568551351846610000, 1568551352013609600, 1568551353051183800, 1568551353132183600, 1568551353722235000, 1568551353800244400, 1568551353862255000
    for xc in time_phase_temp:
        ax.axvline(x=xc, color='r', linewidth=0.5, linestyle='dashed')

        # for i in range(0, len(time_phase)-1):
        # plt.xlim(int(time_phase[3]), int(time_phase[4]))
        # plt.xticks(list_x_tick3, list_x_label3, rotation=90)

        # fig, ax = plt.subplots(1, 4)

    fig1, ax1 = plt.subplots(1, 2)
    i = 0
    # fig.add_subplot(111, frameon=False)
    fig1.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Time relatives to start time(s)")
    plt.ylabel("Memory usage(MB)", y=1.07)
    plt.title("Memory usage of " + title_name, y=1.08)

    for col in ax1:
        col.plot(list_x, list_y)
        col.axvline(x=time_phase_temp[i], color='r', linewidth=0.5, linestyle='dashed')
        col.axvline(x=time_phase_temp[i + 1], color='r', linewidth=0.5, linestyle='dashed')
        col.set_xlim(time_phase_temp[i] - 0.02, time_phase_temp[i + 1] + 0.02)
        i = i + 1
        col.set_title("Phase {}".format(str(i)))

        # fig2, ax2 = plt.subplots(1, 3)
    if len(time_phase) == 5:

        fig2, ax2 = plt.subplots(1, 2)

        fig2.add_subplot(111, frameon=False)
        # hide tick and tick label of the big axis
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.xlabel("Time relatives to start time(s)")
        plt.ylabel("Memory usage(MB)", y=1.07)
        plt.title("Memory usage of " + container_name, y=1.08)

        for col2 in ax2:
            col2.plot(list_x, list_y)
            col2.axvline(x=time_phase_temp[i], color='r', linewidth=0.5, linestyle='dashed')
            col2.axvline(x=time_phase_temp[i + 1], color='r', linewidth=0.5, linestyle='dashed')
            col2.set_xlim(time_phase_temp[i] - 0.02, time_phase_temp[i + 1] + 0.02)
            i = i + 1
            col2.set_title("Phase {}".format(str(i)))

    #     g = plt.figure(4)
    #     #fig, ax = plt.subplots(nrows=1, ncols=1)
    #     plt.plot(list_x, list_y)
    #     plt.axvline(x=time_phase[len(time_phase)-1], color='r', linewidth=0.5, linestyle='dashed')
    #     plt.xlim(time_phase[len(time_phase)-1] - 0.5, list_x[len(list_x)-1])
    #     plt.xlabel("Time relatives to start time(S)")
    #     plt.ylabel("Memory usage (MB)")
    #     plt.title("Memory usage of WordPress")
    # #    plt.xticks(list_x_tick3, list_x_label3,rotation=90)
    #     g.show()
    fig3, ax3 = plt.subplots(1, 2)
    fig3.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Time relatives to start time(s)")
    plt.ylabel("Memory usage(MB)", y=1.07)
    plt.title("Memory usage of " + title_name, y=1.08)

    tem_count = 0
    for col3 in ax3:
        if tem_count == 1:
            col3.plot(list_x, list_y)
            col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
            col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.5, list_x[len(list_x) - 1])
            col3.set_title("Resource usage after the last phase")
        else:
            col3.plot(list_x, list_y)
            col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
            col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.05, time_phase_temp[len(time_phase) - 1] + 1)
            col3.set_title("Resource usage after the last phase (ZOOMED IN)")
            tem_count += 1

    with open(output_file, "a") as f:
        f.write("The start time of performance metrics gathering is at: " + str(start) + ". Real time: " + str(
            nano_read(start)) + "\n")
        f.write("Phases start times (seconds after the start time) on the graph: " + str(time_phase_temp).strip(
            '[]') + "\n\n")
        f.write("Memory Information:\n\n")
        f.write("The maximum memory usage is " + str(max(list_y)) + "MB" + " at " + "(" + str(
            list_x[max_index]) + " seconds after the start) " + str(time_max) + ". Real time: " + str(nano_read(time_max)) + "\n")
        f.write("The minimum memory usage is " + str(min(list_y)) + "MB" + " at " + "(" + str(
            list_x[min_index]) + " seconds after the start) " + str(time_min) + ". Real time: " + str(nano_read(time_min)) + "\n")
        f.write("The maximum difference of memory usage is " + str(int(max(list_y)) - int(min(list_y))) + "MB\n\n")
    f.close()

    if len(time_phase) == 5:
        memory1 = "memory_overview.pdf"
        memory2 = "memory_phase1.pdf"
        memory3 = "memory_phase2.pdf"
        memory4 = "memory_phase3.pdf"
        fig.savefig(container_name + memory1, dpi=fig.dpi)
        fig1.savefig(container_name + memory2, dpi=fig1.dpi)
        fig2.savefig(container_name + memory3, dpi=fig2.dpi)
        fig3.savefig(container_name + memory4, dpi=fig3.dpi)
        plt.close(fig)
        plt.close(fig1)
        plt.close(fig2)
        plt.close(fig3)
    else:
        memory1 = "memory_overview.pdf"
        memory2 = "memory_phase1.pdf"
        memory3 = "memory_phase2.pdf"
        fig.savefig(container_name + memory1, dpi=fig.dpi)
        fig1.savefig(container_name + memory2, dpi=fig1.dpi)
        fig3.savefig(container_name + memory3, dpi=fig3.dpi)
        plt.close(fig)
        plt.close(fig1)
        plt.close(fig3)
    # plt.show()


def process_block(time_phase, file, output_file, title_name, container_name):
    count = 0
    count_measurement = 0
    list_x = []
    list_y_read = []
    list_y_write = []
    temp = 0
    time_phase_temp = []
    current_read = 0
    previous_read = 0
    current_write = 0
    previous_write = 0


    with open(file) as f2:

        for line in f2:
            line = line.split()
            count += 1
            if count == 1:
                list_x.append(int(line[0]))
            elif count == 2:
                # temp = int(line[2])
                current_read = int(line[2])
                if count_measurement == 0:
                    temp = 0
                else:
                    temp = current_read - previous_read

                list_y_read.append(temp / 1000000.0)
                # list_y_read.append(temp)
                previous_read = current_read
            elif count == 3:
                current_write = int(line[2])
                # temp = int(line[2])
                if count_measurement == 0:
                    temp = 0
                else:
                    temp = current_write - previous_write

                list_y_write.append(temp / 1000000.0)
                # list_y_write.append(temp)
                previous_write = current_write
                count_measurement += 1
                count = 0
    f2.close()
    # print(list_y_read)
    start = list_x[0]
    max_index_read = list_y_read.index(max(list_y_read))
    max_index_write = list_y_write.index(max(list_y_write))
    min_index_read = list_y_read.index(min(list_y_read))
    min_index_write = list_y_write.index(min(list_y_write))
    max_read_time = list_x[max_index_read]
    max_write_time = list_x[max_index_write]
    min_read_time = list_x[min_index_read]
    min_write_time = list_x[min_index_write]
    for k in range(len(list_x)):
        if k == 0:
            list_x[k] = 0
        else:
            list_x[k] = (list_x[k] - start) / 1000000000.0
    for k in range(len(time_phase)):
        time_phase_temp.append((int(time_phase[k]) - start) / 1000000000.0)

    fig4, ax4 = plt.subplots(1, 1)
    ax4.plot(list_x, list_y_read, label='Read')
    ax4.plot(list_x, list_y_write, label='Write')
    ax4.set_xlabel("Time relatives to start time(s)")
    ax4.set_ylabel("Disk usage(MB)")
    ax4.set_title("Disk usage of " + title_name, y=1.08)
    # ax4.legend(loc='center right')
    ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)
    for xc in time_phase_temp:
        ax4.axvline(x=xc, color='r', linewidth=0.5, linestyle='dashed')

    fig5, ax5 = plt.subplots(1, 2)
    i = 0
    fig5.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Time relatives to start time(s)")
    plt.ylabel("Disk  usage(MB)", y=1.07)
    plt.title("Disk usage of " + title_name, y=1.08)

    for col in ax5:
        col.plot(list_x, list_y_read, label='Read')
        col.plot(list_x, list_y_write, label='Write')
        col.axvline(x=time_phase_temp[i], color='r', linewidth=0.5, linestyle='dashed')
        col.axvline(x=time_phase_temp[i + 1], color='r', linewidth=0.5, linestyle='dashed')
        col.set_xlim(time_phase_temp[i] - 0.02, time_phase_temp[i + 1] + 0.02)
        i = i + 1
        col.set_title("Phase {}".format(str(i)))
        col.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=5)

        # fig2, ax2 = plt.subplots(1, 3)
    if len(time_phase) == 5:
        fig6, ax6 = plt.subplots(1, 2)
        fig6.add_subplot(111, frameon=False)
        # hide tick and tick label of the big axis
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.xlabel("Time relatives to start time(s)")
        plt.ylabel("Disk  usage(MB)", y=1.07)
        plt.title("Disk usage of " + title_name, y=1.08)

        for col2 in ax6:
            col2.plot(list_x, list_y_read, label="Read")
            col2.plot(list_x, list_y_write, label="Write")
            col2.axvline(x=time_phase_temp[i], color='r', linewidth=0.5, linestyle='dashed')
            col2.axvline(x=time_phase_temp[i + 1], color='r', linewidth=0.5, linestyle='dashed')
            col2.set_xlim(time_phase_temp[i] - 0.02, time_phase_temp[i + 1] + 0.02)
            i = i + 1
            col2.set_title("Phase {}".format(str(i)))
            col2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        fancybox=True, shadow=True, ncol=5)

    fig7, ax7 = plt.subplots(1, 2)
    fig7.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Time relatives to start time(s)")
    plt.ylabel("Disk usage(MB)", y=1.07)
    plt.title("Disk usage of " + title_name, y=1.08)

    tem_count = 0
    for col3 in ax7:
        if tem_count == 1:
            col3.plot(list_x, list_y_read, label="Read")
            col3.plot(list_x, list_y_write, label="Write")
            col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
            col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.5, list_x[len(list_x) - 1])
            col3.set_title("Resource usage after the last phase")
            col3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        fancybox=True, shadow=True, ncol=5)
        else:
            col3.plot(list_x, list_y_read, label="Read")
            col3.plot(list_x, list_y_write, label="Write")
            col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
            col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.05, time_phase_temp[len(time_phase) - 1] + 1)
            col3.set_title("Resource usage after the last phase (ZOOMED IN)")
            col3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        fancybox=True, shadow=True, ncol=5)
            tem_count += 1
    with open(output_file, "a") as f:
        f.write("Block information:\n\n")
        f.write("The maximum difference of disk-reading usage is " + str(max(list_y_read)) + "MB" + " at " + "(" + str(
            list_x[max_index_read]) + " seconds after the start) " + str(max_read_time) + ". Real time: " + str(
            nano_read(max_read_time)) + "\n")
        # f.write("The minimum difference of disk-reading usage is " + str(min(list_y_read)) + "MB" + " at "+"("+str(list_x[min_index_read])+") " + str(min_read_time) + ". Real time: " + str(nano_read(min_read_time)) + " .\n")
        f.write("The maximum difference of disk-writing usage is " + str(max(list_y_write)) + "MB" + " at " + "(" + str(
            list_x[max_index_write]) + " seconds after the start) " + str(max_write_time) + ". Real time: " + str(
            nano_read(max_write_time)) + "\n\n")

        # f.write("The minimum difference of disk-writing usage is " + str(min(list_y_write)) + "MB" + " at " + "(" + str(
        #     list_x[min_index_write]) + ") " + str(min_write_time) + ". Real time: " + str(
        #     nano_read(min_write_time)) + " .\n")
    f.close()

    if len(time_phase) == 5:
        block1 = "block_overview.pdf"
        block2 = "block_phase1.pdf"
        block3 = "block_phase2.pdf"
        block4 = "block_phase3.pdf"
        fig4.savefig(container_name + block1, dpi=fig4.dpi)
        fig5.savefig(container_name + block2, dpi=fig5.dpi)
        fig6.savefig(container_name + block3, dpi=fig6.dpi)
        fig7.savefig(container_name + block4, dpi=fig7.dpi)
        plt.close(fig4)
        plt.close(fig5)
        plt.close(fig6)
        plt.close(fig7)
    else:
        block1 = "block_overview.pdf"
        block2 = "block_phase1.pdf"
        block3 = "block_phase2.pdf"
        fig4.savefig(container_name + block1, dpi=fig4.dpi)
        fig5.savefig(container_name + block2, dpi=fig5.dpi)
        fig7.savefig(container_name + block3, dpi=fig7.dpi)
        plt.close(fig4)
        plt.close(fig5)
        plt.close(fig7)

    # plt.show()


def process_network(time_phase, file, output_file, title_name, container_name):
    count = 0
    count_measurement = 0
    list_x = []
    list_y_receive = []
    list_y_transmit = []
    temp = 0
    current_receive = 0
    previous_receive = 0
    current_transmit = 0
    previous_transmit = 0

    with open(file) as f:
        for line in f:
            line = line.split()
            count += 1
            if count == 1:
                list_x.append(int(line[0]))
            elif count == 2:
                current_receive = int(line[1])
                current_transmit = int(line[9])
                if count_measurement == 0:
                    temp = 0
                    temp2 = 0
                else:
                    current_receive = int(line[1])
                    current_transmit = int(line[9])
                    temp = current_receive - previous_receive
                    temp2 = current_transmit - previous_transmit
                # temp = int(line[1])
                list_y_receive.append(temp / 1000000.0)
                previous_receive = current_receive
                previous_transmit = current_transmit
                # temp = int(line[9])
                # print (temp)
                list_y_transmit.append(temp2 / 1000000.0)
                count_measurement += 1
                count = 0
    f.close()
    start = list_x[0]
    max_index_receive = list_y_receive.index(max(list_y_receive))
    max_index_transmit = list_y_transmit.index(max(list_y_transmit))
    min_index_receive = list_y_receive.index(min(list_y_receive))
    min_index_transmit = list_y_transmit.index(min(list_y_transmit))
    max_receive_time = list_x[max_index_receive]
    max_transmit_time = list_x[max_index_transmit]
    min_receive_time = list_x[min_index_receive]
    min_transmit_time = list_x[min_index_transmit]
    time_phase_temp = []
    for k in range(len(list_x)):
        if k == 0:
            list_x[k] = 0
        else:
            list_x[k] = (list_x[k] - start) / 1000000000.0
    for j in range(len(time_phase)):
        time_phase_temp.append((int(time_phase[j]) - start) / 1000000000.0)

    fig4, ax4 = plt.subplots(1, 1)

    ax4.plot(list_x, list_y_receive, label='Receive')
    ax4.plot(list_x, list_y_transmit, label='Transmit')
    ax4.set_ylabel("Network usage(MB)")
    ax4.set_title("Network usage of " + title_name, y=1.08)
    ax4.set_xlabel("Time relatives to start time(s)")
    ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)
    for xc in time_phase_temp:
        ax4.axvline(x=xc, color='r', linewidth=0.5, linestyle='dashed')

    fig, ax = plt.subplots(1, 2)
    i = 0
    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Time relatives to start time(s)")
    plt.ylabel("Network  usage(MB)", y=1.07)
    plt.title("Network usage of " + title_name, y=1.08)

    for col in ax:
        col.plot(list_x, list_y_receive, label='Receive')
        col.plot(list_x, list_y_transmit, label='Transmit')
        col.axvline(x=time_phase_temp[i], color='r', linewidth=0.5, linestyle='dashed')
        col.axvline(x=time_phase_temp[i + 1], color='r', linewidth=0.5, linestyle='dashed')
        col.set_xlim(time_phase_temp[i] - 0.02, time_phase_temp[i + 1] + 0.02)
        # col.legend(loc='right')
        # col.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        col.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=5)
        i = i + 1
        col.set_title("Phase {}".format(str(i)))

        # fig2, ax2 = plt.subplots(1, 3)

    if len(time_phase) == 5:
        fig2, ax2 = plt.subplots(1, 2)
        fig2.add_subplot(111, frameon=False)
        # hide tick and tick label of the big axis
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.xlabel("Time relatives to start time(s)")
        plt.ylabel("Network  usage(MB)", y=1.07)
        plt.title("Network usage of " + title_name, y=1.08)

        for col2 in ax2:
            col2.plot(list_x, list_y_receive, label="Receive")
            col2.plot(list_x, list_y_transmit, label="Transmit")
            col2.axvline(x=time_phase_temp[i], color='r', linewidth=0.5, linestyle='dashed')
            col2.axvline(x=time_phase_temp[i + 1], color='r', linewidth=0.5, linestyle='dashed')
            col2.set_xlim(time_phase_temp[i] - 0.02, time_phase_temp[i + 1] + 0.02)
            col2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        fancybox=True, shadow=True, ncol=5)
            i = i + 1
            col2.set_title("Phase {}".format(str(i)))

    fig3, ax3 = plt.subplots(1, 2)
    fig3.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Time relatives to start time(s)")
    plt.ylabel("Network usage(MB)", y=1.07)
    plt.title("Network usage of " + title_name, y=1.08)

    tem_count = 0
    for col3 in ax3:
        if tem_count == 1:
            col3.plot(list_x, list_y_receive, label="Receive")
            col3.plot(list_x, list_y_transmit, label="Transmit")
            col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
            col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.5, list_x[len(list_x) - 1])
            col3.set_title("Resource usage after the last phase")
            col3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        fancybox=True, shadow=True, ncol=5)
        else:
            col3.plot(list_x, list_y_receive, label="Receive")
            col3.plot(list_x, list_y_transmit, label="Transmit")
            col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
            col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.05, time_phase_temp[len(time_phase) - 1] + 1)
            col3.set_title("Resource usage after the last phase (ZOOMED IN)")
            col3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        fancybox=True, shadow=True, ncol=5)
            tem_count += 1
    with open(output_file, "a") as f:
        f.write("Network information:\n\n")
        f.write("The maximum difference of network-receive usage is " + str(
            max(list_y_receive)) + "MB" + " at " + "(" + str(
            list_x[max_index_receive]) + " seconds after the start) " + str(max_receive_time) + ". Real time: " + str(
            nano_read(max_receive_time)) + "\n")
        # f.write("The minimum difference of network-receive usage is " + str(min(list_y_receive)) + "MB" + " at " + "(" + str(
        #     list_x[min_index_receive]) + ") " + str(min_receive_time) + ". Real time: " + str(
        #     nano_read(min_receive_time)) + " .\n")
        f.write("The maximum difference of network-transmit usage is " + str(
            max(list_y_transmit)) + "MB" + " at " + "(" + str(
            list_x[max_index_transmit]) + " seconds after the start) " + str(max_transmit_time) + ". Real time: " + str(
            nano_read(max_transmit_time)) + "\n\n")
        # f.write("The minimum difference of network-transmit usage is " + str(min(list_y_transmit)) + "MB" + " at " + "(" + str(
        #     list_x[min_index_transmit]) + ") " + str(min_transmit_time) + ". Real time: " + str(
        #     nano_read(min_transmit_time)) + " .\n")
    f.close()
    if len(time_phase) == 5:
        network1 = "network_overview.pdf"
        network2 = "network_phase1.pdf"
        network3 = "network_phase2.pdf"
        network4 = "network_phase3.pdf"
        fig4.savefig(container_name + network1, dpi=fig4.dpi)
        fig.savefig(container_name + network2, dpi=fig.dpi)
        fig2.savefig(container_name + network3, dpi=fig2.dpi)
        fig3.savefig(container_name + network4, dpi=fig3.dpi)
        # plt.show()
        plt.close(fig4)
        plt.close(fig)
        plt.close(fig2)
        plt.close(fig3)
    else:
        network1 = "network_overview.pdf"
        network2 = "network_phase1.pdf"
        network3 = "network_phase2.pdf"
        fig4.savefig(container_name + network1, dpi=fig4.dpi)
        fig.savefig(container_name + network2, dpi=fig.dpi)
        fig3.savefig(container_name + network3, dpi=fig3.dpi)
        plt.close(fig4)
        plt.close(fig)
        plt.close(fig3)



def process_cpu(time_phase, file, output_file, title_name, container_name):
    count = 0
    count_measurement = 0
    list_x = []
    list_y = []
    user = 0
    previous_user = 0
    time_phase_temp = []

    with open(file) as f:
        for line in f:
            line = line.split()
            count += 1
            if count == 1:
                list_x.append(int(line[0]))
            elif count == 2:
                user = int(line[0])
                if count_measurement == 0:
                    list_y.append(0)
                else:
                    user = int(line[0])
                    temp = user - previous_user
                    list_y.append(temp / 1000000000.0)
                    # else:
                    # temp = (user - previous_user)/1000000000
                    # temp = (((user - previous_user)) / ((cpu_sys - previous_sys) *10000000.0))*2 *100.0
                previous_user = user
                count_measurement += 1
                count = 0
        f.close()
        start = list_x[0]

        max_index = list_y.index(max(list_y))
        time_max = list_x[max_index]

        for k in range(len(list_x)):
            if k == 0:
                list_x[k] = 0
            else:
                list_x[k] = (list_x[k] - start) / 1000000000.0
        for k in range(len(time_phase)):
            time_phase_temp.append((int(time_phase[k]) - start) / 1000000000.0)

        fig, ax = plt.subplots(1, 1)
        ax.plot(list_x, list_y)
        ax.set_xlabel("Time relatives to start time(s)")
        ax.set_ylabel("CPU usage(s)")
        ax.set_title("CPU usage of " + title_name, y=1.08)
        for xc in time_phase_temp:
            ax.axvline(x=xc, color='r', linewidth=0.5, linestyle='dashed')

        fig1, ax1 = plt.subplots(1, 2)
        i = 0
        # fig.add_subplot(111, frameon=False)
        fig1.add_subplot(111, frameon=False)
        # hide tick and tick label of the big axis
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.xlabel("Time relatives to start time(s)")
        plt.ylabel("CPU usage(s)", y=1.07)
        plt.title("CPU usage of " + title_name, y=1.08)

        for col in ax1:
            col.plot(list_x, list_y)
            col.axvline(x=time_phase_temp[i], color='r', linewidth=0.5, linestyle='dashed')
            col.axvline(x=time_phase_temp[i + 1], color='r', linewidth=0.5, linestyle='dashed')
            col.set_xlim(time_phase_temp[i] - 0.02, time_phase_temp[i + 1] + 0.02)
            i = i + 1
            col.set_title("Phase {}".format(str(i)))

            # fig2, ax2 = plt.subplots(1, 3)
        if len(time_phase) == 5:
            fig2, ax2 = plt.subplots(1, 2)
            fig2.add_subplot(111, frameon=False)
            # hide tick and tick label of the big axis
            plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
            plt.xlabel("Time relatives to start time(s)")
            plt.ylabel("CPU usage(s)", y=1.07)
            plt.title("CPU usage of " + title_name, y=1.08)

            for col2 in ax2:
                col2.plot(list_x, list_y)
                col2.axvline(x=time_phase_temp[i], color='r', linewidth=0.5, linestyle='dashed')
                col2.axvline(x=time_phase_temp[i + 1], color='r', linewidth=0.5, linestyle='dashed')
                col2.set_xlim(time_phase_temp[i] - 0.02, time_phase_temp[i + 1] + 0.02)
                i = i + 1
                col2.set_title("Phase {}".format(str(i)))

        #     g = plt.figure(4)
        #     #fig, ax = plt.subplots(nrows=1, ncols=1)
        #     plt.plot(list_x, list_y)
        #     plt.axvline(x=time_phase[len(time_phase)-1], color='r', linewidth=0.5, linestyle='dashed')
        #     plt.xlim(time_phase[len(time_phase)-1] - 0.5, list_x[len(list_x)-1])
        #     plt.xlabel("Time relatives to start time(S)")
        #     plt.ylabel("Memory usage (MB)")
        #     plt.title("Memory usage of WordPress")
        # #    plt.xticks(list_x_tick3, list_x_label3,rotation=90)
        #     g.show()
        fig3, ax3 = plt.subplots(1, 2)
        fig3.add_subplot(111, frameon=False)
        # hide tick and tick label of the big axis
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.xlabel("Time relatives to start time(s)")
        plt.ylabel("CPU usage(s)", y=1.07)
        plt.title("CPU usage of " + title_name, y=1.08)

        tem_count = 0
        for col3 in ax3:
            if tem_count == 1:
                col3.plot(list_x, list_y, )
                col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
                col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.5, list_x[len(list_x) - 1])
                col3.set_title("Resource usage after the last phase")
            else:
                col3.plot(list_x, list_y, )
                col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
                col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.05, time_phase_temp[len(time_phase) - 1] + 1)
                col3.set_title("Resource usage after the last phase (ZOOMED IN)")
                tem_count += 1

        with open(output_file, "a") as f:
            f.write("CPU information:\n\n")
            f.write("The maximum CPU time difference is " + str(max(list_y)) + "s" + " at " + "(" + str(
                list_x[max_index]) + " seconds after the start) " + str(time_max) + ". Real time: " + str(nano_read(time_max)) + "\n")
        f.close()
        if len(time_phase) == 5:
            cpu1 = "cpu_overview.pdf"
            cpu2 = "cpu_phase1.pdf"
            cpu3 = "cpu_phase2.pdf"
            cpu4 = "cpu_phase3.pdf"
            fig.savefig(container_name + cpu1, dpi=fig.dpi)
            fig1.savefig(container_name + cpu2, dpi=fig1.dpi)
            fig2.savefig(container_name + cpu3, dpi=fig2.dpi)
            fig3.savefig(container_name + cpu4, dpi=fig3.dpi)
            # plt.show()
            plt.close(fig)
            plt.close(fig1)
            plt.close(fig2)
            plt.close(fig3)
        else:
            cpu1 = "cpu_overview.pdf"
            cpu2 = "cpu_phase1.pdf"
            cpu3 = "cpu_phase2.pdf"
            fig.savefig(container_name + cpu1, dpi=fig.dpi)
            fig1.savefig(container_name + cpu2, dpi=fig1.dpi)
            fig3.savefig(container_name + cpu3, dpi=fig3.dpi)
            plt.close(fig)
            plt.close(fig1)
            plt.close(fig3)



# 7 phases(not needed)
def update_wp():
    email = "414052254@qq.com"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"
    time_point = []
    temp = 0

    # options = webdriver.ChromeOptions()
    # options.add_argument("user-data-dir=/Users/james/Library/Application Support/Google/Chrome")
    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')  # use chromedriver as driver to open browser.
    temp = time.time_ns()
    print("Before open website", temp)
    time_point.append(temp)
    driver.get('http://localhost:8000/wp-admin')  # go to the website.

    elem = driver.find_element_by_id("user_login")  # find the element to put login.
    elem.send_keys(email)  # send the login information.
    elem = driver.find_element_by_id("user_pass")
    elem.send_keys(pass_code)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    temp = time.time_ns()
    print("After open website and login", temp)
    time_point.append(temp)

    elem = driver.find_element_by_id("wp-admin-bar-site-name")  # Find the topleft corner to view the website.
    elem.click()
    temp = time.time_ns()
    print("After clicking the top-left coner", temp)
    time_point.append(temp)

    elem = driver.find_element_by_class_name("post-edit-link")  # Find the edit link.
    elem.click()
    temp = time.time_ns()
    print("After finding the edit link and click", temp)
    time_point.append(temp)

    elem = driver.find_element_by_class_name(
        "edit-post-more-menu")  # Find the menu to change the visual mode to code mode,
    # so we can find the "post-content-0" to edit content.
    elem.click()
    temp = time.time_ns()
    print("After finding the the menu and click", temp)
    time_point.append(temp)
    # elem =driver.find_element_by_class_name("components-button components-menu-item__button")
    # elem.click()
    elem = driver.find_element_by_css_selector(".components-menu-group:nth-child(2) .components-button:nth-child(2)")
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                       ".components-menu-group:nth-child(2) .components-button:nth-child(2)")))  # Found the element through the Seleium IDE. Could not find it
    # elem = driver.find_element_by_xpath("//div[2]/div[2]/button[2]")
    # in the inspect of the website.
    elem.click()
    temp = time.time_ns()
    print("After finding the Code-editor and click", temp)
    time_point.append(temp)

    elem = driver.find_element_by_id("post-content-0")
    elem.send_keys(content)
    temp = time.time_ns()
    print("After the element is found and put the new content.", temp)
    time_point.append(temp)

    elem = driver.find_element_by_css_selector(".editor-post-publish-button")
    elem.click()
    temp = time.time_ns()
    print("After finding the update button and update", temp)
    time_point.append(temp)
    time.sleep(2)
    with open("terminate.txt", "w") as f:
        f.write("")
    return time_point  #


# 4 phases ( match to drupal)
def update_wordpress(output_file):
    email = "414052254@qq.com"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"
    time_phase = []
    temp = 0

    # options = webdriver.ChromeOptions()
    # options.add_argument("user-data-dir=/Users/james/Library/Application Support/Google/Chrome")
    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')  # use chromedriver as driver to open browser.
    temp = time.time_ns()
    print("Before open website", temp)
    time_phase.append(temp)
    driver.get('http://localhost:8000/wp-admin')  # go to the website.

    elem = driver.find_element_by_id("user_login")  # find the element to put login.
    elem.send_keys(email)  # send the login information.
    elem = driver.find_element_by_id("user_pass")
    elem.send_keys(pass_code)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    temp = time.time_ns()
    print("After open website and login", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_css_selector(".menu-icon-post > .wp-menu-name")  # Find the POST.
    elem.click()
    temp = time.time_ns()
    print("After clicking the post", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'New Title')]")  # Find the post to edit.
    elem.click()
    temp = time.time_ns()
    print("After finding the post to edit and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_class_name(
        "edit-post-more-menu")  # Find the menu to change the visual mode to code mode,
    # so we can find the "post-content-0" to edit content.
    elem.click()
    # temp = time.time_ns()
    # print("After finding the the menu and click", temp)
    # time_point.append(temp)
    # elem =driver.find_element_by_class_name("components-button components-menu-item__button")
    # elem.click()
    elem = driver.find_element_by_css_selector(".components-menu-group:nth-child(2) .components-button:nth-child(2)")
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                       ".components-menu-group:nth-child(2) .components-button:nth-child(2)")))  # Found the element through the Seleium IDE. Could not find it
    # elem = driver.find_element_by_xpath("//div[2]/div[2]/button[2]")
    # in the inspect of the website.
    elem.click()
    # temp = time.time_ns()
    # print("After finding the Code-editor and click", temp)
    # time_point.append(temp)

    elem = driver.find_element_by_id("post-content-0")
    elem.send_keys(content)
    # temp = time.time_ns()
    # print("After the element is found and put the new content.", temp)
    # time_point.append(temp)

    elem = driver.find_element_by_css_selector(".editor-post-publish-button")
    elem.click()
    temp = time.time_ns()
    print("After updating and finding the update button and update", temp)
    time_phase.append(temp)
    time.sleep(2)
    with open(output_file, "w") as f:
        f.write("Information about the phases of adding new contents to a post in a WordPress website.\n\n")
        f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
        f.write("Phase 1 : Open the website and log in." + "\n")
        f.write(
            "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
                nano_read(time_phase[1])) + "\n")
        f.write("Phase 2 : Find and click the post button that manages posts of the website." + "\n")
        f.write("The time after clicking the post button to manage posts is at: " + str(
            time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
        f.write("Phase 3 : Find the particular post to edit." + "\n")
        f.write("The time after finding the post to edit is at: " + str(time_phase[3]) + ". Real time: " + str(
            nano_read(time_phase[3])) + "\n")
        f.write("Phase 4 : Add new content to the post and update it." + "\n")
        f.write("The time after updating the post is at: " + str(time_phase[4]) + ". Real time: " + str(
            nano_read(time_phase[4])) + "\n\n")
    f.close()
    return time_phase


def update_drupal(output_file):
    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')
    time_phase = []
    before = time.time_ns()
    print("before open website", before)
    time_phase.append(before)
    driver.get("http://localhost:8010/user/login")  # go to the website.

    user = "jameszhao"
    # user = "James Zhao"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"

    elem = driver.find_element_by_id("edit-name")  # find the element to put login.
    elem.send_keys(user)  # send the login information.
    elem = driver.find_element_by_id("edit-pass")
    elem.send_keys(pass_code)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    after = time.time_ns()
    print("after open website and login", after)
    time_phase.append(after)

    elem = driver.find_element_by_id("toolbar-link-system-admin_content")  # find the Content

    elem.click()
    temp = time.time_ns()
    print("After finding the content button and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'First Post')]")
    elem.click()

    elem = driver.find_element_by_link_text("Edit")  # Find the edit button.

    elem.click()
    temp = time.time_ns()
    print("After finding the post, edit button and click it", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//html/body")
    elem.click()

    driver.switch_to.frame(0)  # switch to frame0 which has html for the new post.

    elem = driver.find_element_by_xpath("//html/body")  # find the element again.
    elem.send_keys(content)

    driver.switch_to.default_content()  # swtich back to the page.

    elem = driver.find_element_by_id("edit-submit")
    elem.click()
    temp = time.time_ns()

    print("After finding the place to put new content and update.", temp)
    time_phase.append(temp)

    with open(output_file, "w") as f:
        f.write("Information about the phases of adding new contents to a post in a Drupal website.\n\n")
        f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
        f.write("Phase 1 : Open the website and log in." + "\n")
        f.write(
            "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
                nano_read(time_phase[1])) + "\n")
        f.write("Phase 2 : Find and click the content button that manages posts of the website." + "\n")
        f.write("The time after clicking the content button to manage posts is at: " + str(
            time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
        f.write("Phase 3 : Find the particular post to edit." + "\n")
        f.write("The time after finding the post to edit is at: " + str(time_phase[3]) + ". Real time: " + str(
            nano_read(time_phase[3])) + "\n")
        f.write("Phase 4 : Add new content to the post and update it." + "\n")
        f.write("The time after updating the post is at: " + str(time_phase[4]) + ". Real time: " + str(
            nano_read(time_phase[4])) + "\n\n")
    f.close()
    return time_phase


def create_wordpress(output_file):
    email = "414052254@qq.com"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"
    time_phase = []
    temp = 0

    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')  # use chromedriver as driver to open browser.
    temp = time.time_ns()
    print("Before open website", temp)
    time_phase.append(temp)
    driver.get('http://localhost:8000/wp-admin')  # go to the website.

    elem = driver.find_element_by_id("user_login")  # find the element to put login.
    elem.send_keys(email)  # send the login information.
    elem = driver.find_element_by_id("user_pass")
    elem.send_keys(pass_code)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    temp = time.time_ns()
    print("After open website and login", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_css_selector(".menu-icon-post > .wp-menu-name")  # Find the POST.
    elem.click()
    temp = time.time_ns()
    print("After clicking the post", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("(//a[contains(text(),'Add New')])[6]")  # Find the ADD NEW to click.
    elem.click()
    temp = time.time_ns()
    print("After finding the ADD NEW button and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_id("post-title-0")
    elem.send_keys(title)

    elem = driver.find_element_by_class_name(
        "edit-post-more-menu")  # Find the menu to change the visual mode to code mode,
    # so we can find the "post-content-0" to edit content.
    elem.click()
    elem = driver.find_element_by_css_selector(".components-menu-group:nth-child(2) .components-button:nth-child(2)")
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                       ".components-menu-group:nth-child(2) .components-button:nth-child(2)")))  # Found the element through the Seleium IDE. Could not find it
    elem.click()
    elem = driver.find_element_by_id("post-content-0")
    elem.send_keys(content)

    elem = driver.find_element_by_css_selector(".editor-post-publish-panel__toggle")
    elem.click()

    elem = driver.find_element_by_css_selector(".editor-post-publish-button")
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".editor-post-publish-button")))
    elem.click()
    elem.click()

    temp = time.time_ns()
    print("After create a new post and finding the update button and update", temp)
    time_phase.append(temp)

    with open(output_file, "w") as f:
        f.write("Information about the phases of creating a new post in a WordPress website.\n\n")
        f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
        f.write("Phase 1 : Open the website and log in." + "\n")
        f.write(
            "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
                nano_read(time_phase[1])) + "\n")
        f.write("Phase 2 : Find and click the post button that manages posts of the website." + "\n")
        f.write("The time after clicking the post button to manage posts is at: " + str(
            time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
        f.write("Phase 3 : Find the add new button to creat a post." + "\n")
        f.write("The time after finding the add new button is at: " + str(time_phase[3]) + ". Real time: " + str(
            nano_read(time_phase[3])) + "\n")
        f.write("Phase 4 : Add new title and content to the post and publish it." + "\n")
        f.write("The time after creating the post is at: " + str(time_phase[4]) + ". Real time: " + str(
            nano_read(time_phase[4])) + "\n\n")
    f.close()
    return time_phase


def create_drupal(output_file):
    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')
    time_phase = []
    before = time.time_ns()
    print("before open website", before)
    time_phase.append(before)
    driver.get("http://localhost:8010/user/login")  # go to the website.

    user = "jameszhao"
    # user = "James Zhao"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"

    elem = driver.find_element_by_id("edit-name")  # find the element to put login.
    elem.send_keys(user)  # send the login information.
    elem = driver.find_element_by_id("edit-pass")
    elem.send_keys(pass_code)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    after = time.time_ns()
    print("after open website and login", after)
    time_phase.append(after)

    elem = driver.find_element_by_id("toolbar-link-system-admin_content")  # find the Content

    elem.click()
    temp = time.time_ns()
    print("After finding the content button and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_link_text("Add content")  # find ADD CONTENT button
    elem.click()
    temp = time.time_ns()
    print("After finding ADD CONTENT button and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_css_selector(".clearfix:nth-child(1) > a:nth-child(1)")  # Select the type article.
    elem.click()
    # temp = time.time_ns()
    # print("After selecting the type of article and click", temp)
    # time_phase.append(temp)

    elem = driver.find_element_by_id("edit-title-0-value")
    elem.send_keys(title)

    elem = driver.find_element_by_xpath("//html/body")
    elem.click()

    driver.switch_to.frame(0)  # switch to frame0 which has html for the new post.

    elem = driver.find_element_by_xpath("//html/body")  # find the element again.
    elem.send_keys(content)

    driver.switch_to.default_content()  # swtich back to the page.

    elem = driver.find_element_by_id("edit-submit")
    elem.click()
    temp = time.time_ns()
    print("After creating a new post and publish.", temp)
    time_phase.append(temp)

    with open(output_file, "w") as f:
        f.write("Information about the phases of creating a new post in a Drupal website.\n\n")
        f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
        f.write("Phase 1 : Open the website and log in." + "\n")
        f.write(
            "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
                nano_read(time_phase[1])) + "\n")
        f.write("Phase 2 : Find and click the content button that manages posts of the website." + "\n")
        f.write("The time after clicking the content button to manage posts is at: " + str(
            time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
        f.write("Phase 3 : Find the add content button to creat a post." + "\n")
        f.write("The time after finding the add content button is at: " + str(time_phase[3]) + ". Real time: " + str(
            nano_read(time_phase[3])) + "\n")
        f.write("Phase 4 : Add new title and content to the post and publish it." + "\n")
        f.write("The time after creating the post is at: " + str(time_phase[4]) + ". Real time: " + str(
            nano_read(time_phase[4])) + "\n\n")
    f.close()
    return time_phase


def delete_wordpress(output_file):
    email = "414052254@qq.com"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"
    time_phase = []
    temp = 0

    # options = webdriver.ChromeOptions()
    # options.add_argument("user-data-dir=/Users/james/Library/Application Support/Google/Chrome")
    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')  # use chromedriver as driver to open browser.
    temp = time.time_ns()
    print("Before open website", temp)
    time_phase.append(temp)
    driver.get('http://localhost:8000/wp-admin')  # go to the website.

    elem = driver.find_element_by_id("user_login")  # find the element to put login.
    elem.send_keys(email)  # send the login information.
    elem = driver.find_element_by_id("user_pass")
    elem.send_keys(pass_code)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    temp = time.time_ns()
    print("After open website and login", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_css_selector(".menu-icon-post > .wp-menu-name")  # Find the POST.
    elem.click()
    temp = time.time_ns()
    print("After clicking the post", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'New Title')]")  # Find the post to delete.
    elem.click()
    temp = time.time_ns()
    print("After finding the post to delete and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_css_selector(".editor-post-trash")
    elem.click()
    temp = time.time_ns()
    print("After putting the post into the trash", temp)
    time_phase.append(temp)

    with open(output_file, "w") as f:
        f.write("Information about the phases of deleting a post in a WordPress website.\n\n")
        f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
        f.write("Phase 1 : Open the website and log in." + "\n")
        f.write(
            "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
                nano_read(time_phase[1])) + "\n")
        f.write("Phase 2 : Find and click the post button that manages posts of the website." + "\n")
        f.write("The time after clicking the post button to manage posts is at: " + str(
            time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
        f.write("Phase 3 : Find the post to delete." + "\n")
        f.write("The time after finding the post to delete is at: " + str(time_phase[3]) + ". Real time: " + str(
            nano_read(time_phase[3])) + "\n")
        f.write("Phase 4 : Put the post into the trash." + "\n")
        f.write("The time after deleting the post is at: " + str(time_phase[4]) + ". Real time: " + str(
            nano_read(time_phase[4])) + "\n\n")
    f.close()
    return time_phase


def delete_drupal(output_file):
    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')
    time_phase = []
    before = time.time_ns()
    print("before open website", before)
    time_phase.append(before)
    driver.get("http://localhost:8010/user/login")  # go to the website.

    user = "jameszhao"
    # user = "James Zhao"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"

    elem = driver.find_element_by_id("edit-name")  # find the element to put login.
    elem.send_keys(user)  # send the login information.
    elem = driver.find_element_by_id("edit-pass")
    elem.send_keys(pass_code)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    after = time.time_ns()
    print("after open website and login", after)
    time_phase.append(after)

    elem = driver.find_element_by_id("toolbar-link-system-admin_content")  # find the Content

    elem.click()
    temp = time.time_ns()
    print("After finding the content button and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'New Title')]")  # Find the post to delete.
    elem.click()
    temp = time.time_ns()
    print("After finding the post to delete and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'Delete')]")  # Find the delete button.
    elem.click()

    elem = driver.find_element_by_id("edit-submit")
    elem.click()
    temp = time.time_ns()
    print("After deleting the post.", temp)
    time_phase.append(temp)

    with open(output_file, "w") as f:
        f.write("Information about the phases of deleting a post in a Drupal website.\n\n")
        f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
        f.write("Phase 1 : Open the website and log in." + "\n")
        f.write(
            "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
                nano_read(time_phase[1])) + "\n")
        f.write("Phase 2 : Find and click the content button that manages posts of the website." + "\n")
        f.write("The time after clicking the content button to manage posts is at: " + str(
            time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
        f.write("Phase 3 : Find the post to delete." + "\n")
        f.write("The time after finding the post to delete is at: " + str(time_phase[3]) + ". Real time: " + str(
            nano_read(time_phase[3])) + "\n")
        f.write("Phase 4 : Deleting the post." + "\n")
        f.write("The time after deleting the post is at: " + str(time_phase[4]) + ". Real time: " + str(
            nano_read(time_phase[4])) + "\n\n")
    f.close()
    return time_phase

def view_wordpress_post(output_file):
    time_phase = []
    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')  # use chromedriver as driver to open browser.
    temp = time.time_ns()
    print("Before opening the website", temp)
    time_phase.append(temp)
    driver.get('http://localhost:8000')  # go to the website.
    temp = time.time_ns()
    time_phase.append(temp)
    print("After opening the website", temp)
    elem = driver.find_element_by_link_text("New Title")
    elem.click()
    temp = time.time_ns()
    time_phase.append(temp)
    print("After finding the post and click it", temp)

    with open(output_file, "w") as f:
        f.write("Information about the phases of viewing a post in a WordPress website.\n\n")
        f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
        f.write("Phase 1 : Open the website." + "\n")
        f.write(
            "The time after opening the website is at: " + str(time_phase[1]) + ". Real time: " + str(
                nano_read(time_phase[1])) + "\n")
        f.write("Phase 2 : Find the post and view it." + "\n")
        f.write("The time after clicking the post to view is at: " + str(
            time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    f.close()
    return time_phase

def view_drupal_post(output_file):
    time_phase = []
    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')  # use chromedriver as driver to open browser.
    temp = time.time_ns()
    print("Before opening the website", temp)
    time_phase.append(temp)
    driver.get('http://localhost:8010')  # go to the website.
    temp = time.time_ns()
    time_phase.append(temp)
    print("After opening the website", temp)
    elem = driver.find_element_by_link_text("New Title")
    elem.click()
    temp = time.time_ns()
    time_phase.append(temp)
    print("After finding the post and click it", temp)

    with open(output_file, "w") as f:
        f.write("Information about the phases of viewing a post in a Drupal website.\n\n")
        f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
        f.write("Phase 1 : Open the website." + "\n")
        f.write(
            "The time after opening the website is at: " + str(time_phase[1]) + ". Real time: " + str(
                nano_read(time_phase[1])) + "\n")
        f.write("Phase 2 : Find the post and view it." + "\n")
        f.write("The time after clicking the post to view is at: " + str(
            time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    f.close()
    return time_phase




def get_variables(ct_name, operation_type):
    global cpu_file, memory_file, block_file, network_file, update_wp_file, update_dp_file, create_wp_file, create_dp_file
    global create_wp_file, delete_dp_file, delete_wp_file, update_title_name_dp, update_title_name_wp, create_title_name_dp
    global create_title_name_wp, delete_title_name_dp, delete_title_name_wp, container_name
    global view_wp_file, view_dp_file, view_title_name_wp, view_title_namp_dp

    cpu_file = ct_name + "_" + operation_type + "_" + "cpu_log.txt"
    memory_file = ct_name + "_" + operation_type + "_" + "memory_log.txt"
    block_file = ct_name + "_" + operation_type + "_" + "block_log.txt"
    network_file = ct_name + "_" + operation_type + "_" + "network_log.txt"

    update_wp_file = ct_name + "_" + operation_type + ".txt"
    update_dp_file = ct_name + "_" + operation_type + ".txt"

    create_wp_file = ct_name + "_" + operation_type + ".txt"
    create_dp_file = ct_name + "_" + operation_type + ".txt"

    delete_wp_file = ct_name + "_" + operation_type + ".txt"
    delete_dp_file = ct_name + "_" + operation_type + ".txt"

    view_wp_file = ct_name + "_" + operation_type + ".txt"
    view_dp_file = ct_name + "_" + operation_type + ".txt"

    update_title_name_wp = ct_name + " container of adding new content to a WordPress website"
    update_title_name_dp = ct_name + " container of adding new content to a Drupal website"
    create_title_name_wp = ct_name + " container of creating a new post to a WordPress website"
    create_title_name_dp = ct_name + " container of creating a new post to a Drupal website"
    delete_title_name_wp = ct_name + " container of deleting a post to a WordPress website"
    delete_title_name_dp = ct_name + " container of deleting a post to a Drupal website"
    view_title_name_wp = ct_name + "container of viewing a post on a WordPress website"
    view_title_namp_dp = ct_name + "container of viewing a post on a Drupal website"

    container_name = ct_name + "_" + operation_type + "_"

def process_files():
    process_memory(time_phase, memory_file, update_wp_file, update_title_name_wp, container_name)
    process_block(time_phase, block_file, update_wp_file, update_title_name_wp, container_name)
    process_network(time_phase, network_file, update_wp_file, update_title_name_wp, container_name)
    process_cpu(time_phase, cpu_file, update_wp_file, update_title_name_wp, container_name)



if __name__ == "__main__":
    operation_type = sys.argv[1]

    time_phase = []

    if operation_type == "update":
        if len(sys.argv) == 3:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase = update_wordpress(update_wp_file)
                time.sleep(15)
                process_files()
            elif "drupal" in container_name:
                time_phase = update_drupal(update_dp_file)
                time.sleep(15)
                process_files()
        elif len(sys.argv) == 4:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase = update_wordpress(update_wp_file)
                time.sleep(15)
                process_files()
                get_variables(sys.argv[3], operation_type)
                process_files()
            elif "drupal" in container_name:
                time_phase = update_drupal(update_dp_file)
                time.sleep(15)
                process_files()
                get_variables(sys.argv[3], operation_type)
                process_files()
    elif operation_type == "create":
        if len(sys.argv) == 3:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase = create_wordpress(create_wp_file)
                time.sleep(15)
                process_files()
            elif "drupal" in container_name:
                time_phase = create_drupal(create_dp_file)
                time.sleep(15)
                process_files()
        elif len(sys.argv) == 4:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase = create_wordpress(create_wp_file)
                time.sleep(15)
                process_files()
                get_variables(sys.argv[3], operation_type)
                process_files()
            elif "drupal" in container_name:
                time_phase = create_drupal(create_dp_file)
                time.sleep(15)
                process_files()
                get_variables(sys.argv[3], operation_type)
                process_files()
    elif operation_type == "delete":
        if len(sys.argv) == 3:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase = delete_wordpress(delete_wp_file)
                time.sleep(15)
                process_files()
            elif "drupal" in container_name:
                time_phase = delete_drupal(delete_dp_file)
                time.sleep(15)
                process_files()
        elif len(sys.argv) == 4:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase = delete_wordpress(delete_wp_file)
                time.sleep(15)
                process_files()
                get_variables(sys.argv[3], operation_type)
                process_files()
            elif "drupal" in container_name:
                time_phase = delete_drupal(delete_dp_file)
                time.sleep(15)
                process_files()
                get_variables(sys.argv[3], operation_type)
                process_files()
    elif operation_type == "view":
        if len(sys.argv) == 3:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase = view_wordpress_post(view_wp_file)
                time.sleep(15)
                process_files()
            elif "drupal" in container_name:
                time_phase = view_drupal_post(view_dp_file)
                time.sleep(15)
                process_files()
        elif len(sys.argv) == 4:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase = view_wordpress_post(view_wp_file)
                time.sleep(19)
                process_files()
                get_variables(sys.argv[3], operation_type)
                process_files()
            elif "drupal" in container_name:
                time_phase = view_drupal_post(view_dp_file)
                time.sleep(19)
                process_files()
                get_variables(sys.argv[3], operation_type)
                process_files()


