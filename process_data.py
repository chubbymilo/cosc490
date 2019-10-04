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
# Change the executable path for the web driver.
executable_path = './chromedriver.exe'

#  Read nanosecond precision timestamp and convert it to a human readble format.
def nano_read(nano):
    dt = datetime.datetime.fromtimestamp(nano / 1e9)
    return '{}{:03.0f}'.format(dt.strftime('%Y-%m-%d %H:%M:%S.%f'), nano % 1e3)


#  Generate plot for processing memory and CPU data.
def generate_plot(data_x, data_y, data_phase, ylabel, title, color_s, phase_index, phase_info, ax=None):
    i = phase_index
    ax = ax
    ymax = max(data_y)
    ypos = data_y.index(ymax)
    xmax = data_x[ypos]
    max_diff = ymax - min(data_y)
    # fig.add_subplot(111, frameon=False)
    # fig1.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    # plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)

    color_index = int(i / 3)
    ax.set_xlabel("Time relatives to start time(s)")
    ax.set_ylabel(ylabel)
    ax.set_title(title + "--Phase {}: ".format(str(int(i / 3) + 1)) + phase_info[color_index])

    ax.plot(data_x, data_y)
    ax.plot([], [], ' ', label='Max: {} at {}'.format(ymax, xmax))
    ax.plot([], [], ' ', label='Max difference : {}'.format(max_diff))
    ax.axvline(x=data_phase[i], color=color_s[color_index], linewidth=0.5, linestyle='dashed',
               label="Phase start: " + str(data_phase[i]))
    i = i + 1
    ax.axvline(x=data_phase[i], color='black', linewidth=0.5, linestyle='-',
               label="Back end finished: " + str(data_phase[i]))
    i = i + 1
    ax.axvline(x=data_phase[i], color=color_s[color_index], linewidth=0.5, linestyle='dashed',
               label="Phase end: " + str(data_phase[i]))

    ax.set_xlim(data_phase[i - 2] - 0.08, data_phase[i] + 0.08)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=3)
    # ax.annotate('Max: {} at {}'.format(ymax, xmax), xy=(xmax, ymax), xytext=(xmax, ymax - 0.5),
    #             arrowprops=dict(arrowstyle='->', facecolor='black'),
    #             )


#  Generate plot for processing disk and network data.
def generate_plot2(data_x, data_y, data_y2, data_phase, ylabel, title, color_s, phase_index, phase_info, ax=None):
    i = phase_index
    ax = ax
    ymax = max(data_y)
    ypos = data_y.index(ymax)
    xmax = data_x[ypos]
    max_diff = ymax - min(data_y)

    ymax2 = max(data_y2)
    ypos2 = data_y2.index(ymax2)
    xmax2 = data_x[ypos2]
    max_diff2 = ymax - min(data_y2)
    # fig.add_subplot(111, frameon=False)
    # fig1.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    # plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)

    color_index = int(i / 3)
    ax.set_xlabel("Time relatives to start time(s)")
    ax.set_ylabel(ylabel)
    ax.set_title(title + "--Phase {}: ".format(str(int(i / 3) + 1)) + phase_info[color_index])
    if "Disk" in ylabel:
        ax.plot(data_x, data_y, label='Read')
        ax.plot(data_x, data_y2, label='Write')
        ax.plot([], [], ' ', label='Max difference  of read: {} at {}'.format(max_diff, xmax))
        ax.plot([], [], ' ', label='Max difference  of write: {} at {}'.format(max_diff2, xmax2))
    else:
        ax.plot(data_x, data_y, label='Receive')
        ax.plot(data_x, data_y2, label='Transmit')
        ax.plot([], [], ' ', label='Max difference  of receive: {} at {}'.format(max_diff, xmax))
        ax.plot([], [], ' ', label='Max difference  of transmit: {} at {}'.format(max_diff2, xmax2))
    ax.axvline(x=data_phase[i], color=color_s[color_index], linewidth=0.5, linestyle='dashed',
               label="Phase start: " + str(data_phase[i]))
    i = i + 1
    ax.axvline(x=data_phase[i], color='black', linewidth=0.5, linestyle='-',
               label="Back end finished: " + str(data_phase[i]))
    i = i + 1
    ax.axvline(x=data_phase[i], color=color_s[color_index], linewidth=0.5, linestyle='dashed',
               label="Phase end: " + str(data_phase[i]))

    ax.set_xlim(data_phase[i - 2] - 0.08, data_phase[i] + 0.08)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=3)
    # ax.annotate('Max: {} at {}'.format(ymax, xmax), xy=(xmax, ymax), xytext=(xmax, ymax - 0.5),
    #             arrowprops=dict(arrowstyle='->', facecolor='black'),
    #             )


#  Process the memory data.
def process_memory(time_phase, file, output_file, title_name, container_name, phase_information):
    count = 0
    count_measurement = 0
    list_x = []
    list_y = []
    temp = 0
    time_phase_temp = []
    time_response_phase_temp = [None] * len(time_phase)
    color_set = ['r', 'g', 'c', 'orange', 'purple', 'tab:brown']

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
        time_response_phase_temp[k] = ((int(time_phase[k]) * 1000000) - start) / 1000000000.0

    # time_phase_temp.append((int(time_phase[k]) - start) / 1000000000.0)

    ymax = max(list_y)
    ypos = list_y.index(ymax)
    xmax = list_x[ypos]
    max_diff = max(list_y) - min(list_y)

    fig, ax = plt.subplots(1, 1)
    ax.plot(list_x, list_y)
    ax.plot([], [], ' ', label='Max: {} at {}'.format(ymax, xmax))
    ax.plot([], [], ' ', label='Max difference : {}'.format(max_diff))
    ax.set_xlabel("Time relatives to start time(s)")
    ax.set_ylabel("Memory usage(MB)")
    ax.set_title("Memory usage of " + title_name, y=1.08)

    # plt.text(0, 0, 'matplotlib', ha='center', va='center', transform=ax.transAxes)
    # plt.xticks([0], [nano_read(start)])
    # 1568551346332221200, 1568551351300437000, 1568551351846610000, 1568551352013609600, 1568551353051183800, 1568551353132183600, 1568551353722235000, 1568551353800244400, 1568551353862255000
    j = 0

    for xc in range(len(time_response_phase_temp)):
        t = xc % 3
        if xc > 0 and t == 0:
            j += 1
        if t == 0:
            ax.axvline(x=time_response_phase_temp[xc], color=color_set[j], linewidth=0.5, linestyle='--',
                       label='Phase {}: '.format(str(j + 1)) + phase_information[j])
        else:
            ax.axvline(x=time_response_phase_temp[xc], color=color_set[j], linewidth=0.5, linestyle='--')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=3)

    fig.savefig(container_name + "memory_overview.pdf", dpi=fig.dpi)
    # plt.show()
    plt.close(fig)

    phase_reminder = len(time_response_phase_temp) % 3
    phase_range = (len(time_response_phase_temp) - phase_reminder) / 3

    for k in range(int(phase_range)):
        fig1, ax1 = plt.subplots(1, 1)
        generate_plot(list_x, list_y, time_response_phase_temp, "Memory usage(MB)", "Memory usage of " + title_name,
                      color_set, k * 3, phase_information, ax1)
        fig1.savefig(container_name + "memory_phase%s.pdf" % str(k + 1), dpi=fig1.dpi)
        # plt.show()
        plt.close(fig1)

    if phase_reminder != 0:
        fig3, ax3 = plt.subplots(1, 1)
        ax3.plot(list_x, list_y)
        ax3.set_xlabel("Time relatives to start time(s)")
        ax3.set_ylabel("Memory usage(MB)")
        ax3.set_title("Memory usage of " + title_name + " -- phase {}: ".format(k + 2) + phase_information[k + 1],
                      y=1.08)
        ax3.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
                    linestyle='dashed',
                    label="last phase start: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))
        # ax3.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
        #             linestyle='dashed',
        #             label="last phase end: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))

        ax3.plot([], [], ' ', label='Max: {} at {}'.format(ymax, xmax))
        ax3.plot([], [], ' ', label='Max difference : {}'.format(max_diff))

        ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=5)

        ax3.set_xlim(time_response_phase_temp[len(time_response_phase_temp) - 1] - 0.03,
                     time_response_phase_temp[len(time_response_phase_temp) - 1] + 0.5)
        fig3.savefig(container_name + "memory_phase{}.pdf".format(k + 2))
        plt.close(fig3)

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(list_x, list_y)
    ax2.set_xlabel("Time relatives to start time(s)")
    ax2.set_ylabel("Memory usage(MB)")
    ax2.set_title("Memory usage of " + title_name + " -- After the last phase", y=1.08)
    ax2.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
                linestyle='dashed',
                label="last phase end: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))

    ax2.plot([], [], ' ', label='Max: {} at {}'.format(ymax, xmax))
    ax2.plot([], [], ' ', label='Max difference : {}'.format(max_diff))

    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)

    ax2.set_xlim(time_response_phase_temp[len(time_response_phase_temp) - 1] - 0.03,
                 time_response_phase_temp[len(time_response_phase_temp) - 1] + 4)
    fig2.savefig(container_name + "memory_after_last_phase.pdf")
    # plt.show()
    plt.close(fig2)

    # i = 6
    # fig2, ax2 = plt.subplots(1, 2)
    #
    # fig2.add_subplot(111, frameon=False)
    #     # hide tick and tick label of the big axis
    # plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    # plt.xlabel("Time relatives to start time(s)")
    # plt.ylabel("Memory usage(MB)", y=1.07)
    # plt.title("Memory usage of " + title_name, y=1.08)
    # for col2 in ax2:
    #     col2.plot(list_x, list_y)
    #     col2.axvline(x=time_response_phase_temp[i], color=color_set[color_index], linewidth=0.5, linestyle='dashed')
    #     i = i + 1
    #     col2.axvline(x=time_response_phase_temp[i], color=color_set[color_index], linewidth=0.5, linestyle='dashed')
    #     i = i + 1
    #     col2.axvline(x=time_response_phase_temp[i], color=color_set[color_index], linewidth=0.5, linestyle='dashed')
    #     col2.set_xlim(time_response_phase_temp[i - 2] - 0.02, time_response_phase_temp[i] + 0.02)
    #     i = i + 1
    #     color_index += 1
    #     col2.set_title("Phase {}".format(str(int(i / 3))))
    #
    #     # col2.plot(list_x, list_y)
    #     # col2.axvline(x=time_phase_temp[i], color='r', linewidth=0.5, linestyle='dashed')
    #     # col2.axvline(x=time_phase_temp[i + 1], color='r', linewidth=0.5, linestyle='dashed')
    #     # col2.set_xlim(time_phase_temp[i] - 0.02, time_phase_temp[i + 1] + 0.02)
    #     # i = i + 1
    #     # col2.set_title("Phase {}".format(str(i)))
    #
    # #     g = plt.figure(4)
    # #     #fig, ax = plt.subplots(nrows=1, ncols=1)
    # #     plt.plot(list_x, list_y)
    # #     plt.axvline(x=time_phase[len(time_phase)-1], color='r', linewidth=0.5, linestyle='dashed')
    # #     plt.xlim(time_phase[len(time_phase)-1] - 0.5, list_x[len(list_x)-1])
    # #     plt.xlabel("Time relatives to start time(S)")
    # #     plt.ylabel("Memory usage (MB)")
    # #     plt.title("Memory usage of WordPress")
    # # #    plt.xticks(list_x_tick3, list_x_label3,rotation=90)
    # #     g.show()
    #
    # fig3, ax3 = plt.subplots(1, 2)
    # fig3.add_subplot(111, frameon=False)
    # # hide tick and tick label of the big axis
    # plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    # plt.xlabel("Time relatives to start time(s)")
    # plt.ylabel("Memory usage(MB)", y=1.07)
    # plt.title("Memory usage of " + title_name, y=1.08)
    # tem_count = 0
    # for col3 in ax3:
    #     col3.plot(list_x, list_y)
    #     col3.axvline(x=time_response_phase_temp[i], color=color_set[color_index], linewidth=0.5, linestyle='dashed')
    #     i = i + 1
    #     col3.axvline(x=time_response_phase_temp[i], color=color_set[color_index], linewidth=0.5, linestyle='dashed')
    #     i = i + 1
    #     col3.axvline(x=time_response_phase_temp[i], color=color_set[color_index], linewidth=0.5, linestyle='dashed')
    #     col3.set_xlim(time_response_phase_temp[i - 2] - 0.02, time_response_phase_temp[i] + 0.02)
    #     i = i + 1
    #     color_index += 1
    #     col3.set_title("Phase {}".format(str(int(i / 3))))
    # plt.show()
    #
    #     # if tem_count == 1:
    #     #     col3.plot(list_x, list_y)
    #     #     col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
    #     #     col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.5, list_x[len(list_x) - 1])
    #     #     col3.set_title("Resource usage after the last phase")
    #     # else:
    #     #     col3.plot(list_x, list_y)
    #     #     col3.axvline(x=time_phase_temp[len(time_phase) - 1], color='r', linewidth=0.5, linestyle='dashed')
    #     #     col3.set_xlim(time_phase_temp[len(time_phase) - 1] - 0.05, time_phase_temp[len(time_phase) - 1] + 1)
    #     #     col3.set_title("Resource usage after the last phase (ZOOMED IN)")
    #     #     tem_count += 1


#  Process the block data.
def process_block(time_phase, file, output_file, title_name, container_name, phase_information):
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
    time_response_phase_temp = [None] * len(time_phase)
    color_set = ['r', 'g', 'c', 'orange', 'purple', 'tab:brown']

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

    for k in range(len(list_x)):
        if k == 0:
            list_x[k] = 0
        else:
            list_x[k] = (list_x[k] - start) / 1000000000.0

    for k in range(len(time_phase)):
        time_response_phase_temp[k] = ((int(time_phase[k]) * 1000000) - start) / 1000000000.0

    max_index_read = list_y_read.index(max(list_y_read))
    max_index_write = list_y_write.index(max(list_y_write))
    max_read_time = list_x[max_index_read]
    max_write_time = list_x[max_index_write]

    fig4, ax4 = plt.subplots(1, 1)
    ax4.plot(list_x, list_y_read, label='Read')
    ax4.plot(list_x, list_y_write, label='Write')
    ax4.set_xlabel("Time relatives to start time(s)")
    ax4.set_ylabel("Disk usage(MB)")
    ax4.set_title("Disk usage of " + title_name, y=1.08)
    ax4.plot([], [], ' ', label='Max difference of read: {} at {}'.format(list_y_read[max_index_read]
                                                                          , max_read_time))
    ax4.plot([], [], ' ', label='Max difference of write {} at {}'.format(list_y_write[max_index_write]
                                                                          , max_write_time))
    j = 0
    for xc in range(len(time_response_phase_temp)):
        t = xc % 3
        if xc > 0 and t == 0:
            j += 1
        if t == 0:
            ax4.axvline(x=time_response_phase_temp[xc], color=color_set[j], linewidth=0.5, linestyle='--',
                        label='Phase {}: '.format(str(j + 1)) + phase_information[j])
        else:
            ax4.axvline(x=time_response_phase_temp[xc], color=color_set[j], linewidth=0.5, linestyle='--')
    ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=4)

    phase_reminder = len(time_response_phase_temp) % 3
    phase_range = (len(time_response_phase_temp) - phase_reminder) / 3
    fig4.savefig(container_name + "disk_overview.pdf", dpi=fig4.dpi)
    plt.close(fig4)

    for k in range(int(phase_range)):
        fig1, ax1 = plt.subplots(1, 1)
        generate_plot2(list_x, list_y_read, list_y_write, time_response_phase_temp, "Disk usage(s)",
                       "Disk usage of " + title_name,
                       color_set, k * 3, phase_information, ax1)
        fig1.savefig(container_name + "disk_phase%s.pdf" % str(k + 1), dpi=fig1.dpi)
        plt.close(fig1)

    if phase_reminder != 0:
        fig3, ax3 = plt.subplots(1, 1)
        ax3.plot(list_x, list_y_read, label='Read')
        ax3.plot(list_x, list_y_write, label='Write')

        ax3.set_xlabel("Time relatives to start time(s)")
        ax3.set_ylabel("Disk usage(MB)")
        ax3.set_title("Disk usage of " + title_name + " -- phase {}: ".format(k + 2) + phase_information[k + 1], y=1.08)
        ax3.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
                    linestyle='dashed',
                    label="last phase start: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))
        # ax3.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
        #             linestyle='dashed',
        #             label="last phase end: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))

        ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=5)

        ax3.plot([], [], ' ', label='Max difference of read: {} at {}'.format(list_y_read[max_index_read]
                                                                              , max_read_time))
        ax3.plot([], [], ' ', label='Max difference of write {} at {}'.format(list_y_read[max_index_read]
                                                                              , max_read_time))
        ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=3)
        ax3.set_xlim(time_response_phase_temp[len(time_response_phase_temp) - 1] - 0.03,
                     time_response_phase_temp[len(time_response_phase_temp) - 1] + 0.5)
        fig3.savefig(container_name + "disk_phase{}.pdf".format(k + 2))
        plt.close(fig3)

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(list_x, list_y_read, label='Read')
    ax2.plot(list_x, list_y_write, label='write')
    ax2.set_xlabel("Time relatives to start time(s)")
    ax2.set_ylabel("Disk usage(MB)")
    ax2.set_title("Disk usage of " + title_name + " -- After the last phase", y=1.08)
    ax2.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
                linestyle='dashed',
                label="last phase end: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))
    ax2.plot([], [], ' ', label='Max difference of read: {} at {}'.format(list_y_read[max_index_read]
                                                                          , max_read_time))
    ax2.plot([], [], ' ', label='Max difference of write {} at {}'.format(list_y_write[max_index_write]
                                                                          , max_write_time))
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)

    ax2.set_xlim(time_response_phase_temp[len(time_response_phase_temp) - 1] - 0.03,
                 time_response_phase_temp[len(time_response_phase_temp) - 1] + 4)
    fig2.savefig(container_name + "disk_after_last_phase.pdf")
    # plt.show()
    plt.close(fig2)


#  Process the network data.
def process_network(time_phase, file, output_file, title_name, container_name, phase_information):
    count = 0
    count_measurement = 0
    list_x = []
    list_y_receive = []
    list_y_transmit = []
    time_response_phase_temp = [None] * len(time_phase)
    color_set = ['r', 'g', 'c', 'orange', 'purple', 'tab:brown']
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

    time_phase_temp = []
    for k in range(len(list_x)):
        if k == 0:
            list_x[k] = 0
        else:
            list_x[k] = (list_x[k] - start) / 1000000000.0
    for k in range(len(time_phase)):
        time_response_phase_temp[k] = ((int(time_phase[k]) * 1000000) - start) / 1000000000.0

    max_index_receive = list_y_receive.index(max(list_y_receive))
    max_index_transmit = list_y_transmit.index(max(list_y_transmit))
    max_receive_time = list_x[max_index_receive]
    max_transmit_time = list_x[max_index_transmit]

    fig4, ax4 = plt.subplots(1, 1)

    ax4.plot(list_x, list_y_receive, label='Receive')
    ax4.plot(list_x, list_y_transmit, label='Transmit')
    ax4.plot([], [], ' ', label='Max difference of receive: {} at {}'.format(list_y_receive[max_index_receive]
                                                                             , max_receive_time))
    ax4.plot([], [], ' ', label='Max difference of transmit {} at {}'.format(list_y_transmit[max_index_transmit]
                                                                             , max_transmit_time))
    ax4.set_ylabel("Network usage(MB)")
    ax4.set_title("Network usage of " + title_name, y=1.08)
    ax4.set_xlabel("Time relatives to start time(s)")
    j = 0
    for xc in range(len(time_response_phase_temp)):
        t = xc % 3
        if xc > 0 and t == 0:
            j += 1
        if t == 0:
            ax4.axvline(x=time_response_phase_temp[xc], color=color_set[j], linewidth=0.5, linestyle='--',
                        label='Phase {}: '.format(str(j + 1)) + phase_information[j])
        else:
            ax4.axvline(x=time_response_phase_temp[xc], color=color_set[j], linewidth=0.5, linestyle='--')
    ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=4)
    fig4.savefig(container_name + "network_overview.pdf", dpi=fig4.dpi)
    plt.close(fig4)
    # plt.show()

    phase_reminder = len(time_response_phase_temp) % 3
    phase_range = (len(time_response_phase_temp) - phase_reminder) / 3

    for k in range(int(phase_range)):
        fig1, ax1 = plt.subplots(1, 1)
        generate_plot2(list_x, list_y_receive, list_y_transmit, time_response_phase_temp, "Network usage(s)",
                       "Network usage of " + title_name,
                       color_set, k * 3, phase_information, ax1)
        fig1.savefig(container_name + "network_phase%s.pdf" % str(k + 1), dpi=fig1.dpi)
        plt.close(fig1)

    if phase_reminder != 0:
        fig3, ax3 = plt.subplots(1, 1)
        ax3.plot(list_x, list_y_receive, label='Receive')
        ax3.plot(list_x, list_y_transmit, label='Transmit')

        ax3.set_xlabel("Time relatives to start time(s)")
        ax3.set_ylabel("Network usage(MB)")
        ax3.set_title("Network usage of " + title_name + " -- phase {}: ".format(k + 2) + phase_information[k + 1],
                      y=1.08)
        ax3.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
                    linestyle='dashed',
                    label="last phase start: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))
        # ax3.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
        #             linestyle='dashed',
        #             label="last phase end: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))

        ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=5)

        ax3.plot([], [], ' ', label='Max difference of receive: {} at {}'.format(list_y_receive[max_index_receive]
                                                                                 , max_receive_time))
        ax3.plot([], [], ' ', label='Max difference of transmit {} at {}'.format(list_y_transmit[max_index_transmit]
                                                                                 , max_transmit_time))
        ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=3)
        ax3.set_xlim(time_response_phase_temp[len(time_response_phase_temp) - 1] - 0.03,
                     time_response_phase_temp[len(time_response_phase_temp) - 1] + 0.5)
        fig3.savefig(container_name + "network_phase{}.pdf".format(k + 2))
        plt.close(fig3)

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(list_x, list_y_receive, label='Receive')
    ax2.plot(list_x, list_y_transmit, label='Transmit')
    ax2.set_xlabel("Time relatives to start time(s)")
    ax2.set_ylabel("Network usage(s)")
    ax2.set_title("Network usage of " + title_name + " -- After the last phase", y=1.08)
    ax2.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
                linestyle='dashed',
                label="last phase end: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))
    ax2.plot([], [], ' ', label='Max difference of receive: {} at {}'.format(list_y_receive[max_index_receive]
                                                                             , max_receive_time))
    ax2.plot([], [], ' ', label='Max difference of transmit {} at {}'.format(list_y_transmit[max_index_transmit]
                                                                             , max_transmit_time))
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)

    ax2.set_xlim(time_response_phase_temp[len(time_response_phase_temp) - 1] - 0.03,
                 time_response_phase_temp[len(time_response_phase_temp) - 1] + 4)
    fig2.savefig(container_name + "network_after_last_phase.pdf")
    # plt.show()
    plt.close(fig2)


#  Process the CPU data.
def process_cpu(time_phase, file, output_file, title_name, container_name, phase_information):
    count = 0
    count_measurement = 0
    list_x = []
    list_y = []
    user = 0
    previous_user = 0
    time_phase_temp = []
    time_response_phase_temp = [None] * len(time_phase)
    color_set = ['r', 'g', 'c', 'orange', 'purple', 'tab:brown']

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
        time_response_phase_temp[k] = ((int(time_phase[k]) * 1000000) - start) / 1000000000.0

    ymax = max(list_y)
    ypos = list_y.index(ymax)
    xmax = list_x[ypos]
    max_diff = max(list_y) - min(list_y)

    fig, ax = plt.subplots(1, 1)
    ax.plot(list_x, list_y)
    ax.plot([], [], ' ', label='Max: {} at {}'.format(ymax, xmax))
    ax.plot([], [], ' ', label='Max difference : {}'.format(max_diff))
    ax.set_xlabel("Time relatives to start time(s)")
    ax.set_ylabel("CPU usage(s)")
    ax.set_title("CPU usage of " + title_name, y=1.08)

    j = 0
    for xc in range(len(time_response_phase_temp)):
        t = xc % 3
        if xc > 0 and t == 0:
            j += 1
        if t == 0:
            ax.axvline(x=time_response_phase_temp[xc], color=color_set[j], linewidth=0.5, linestyle='--',
                       label='Phase {}: '.format(str(j + 1)) + phase_information[j])
        else:
            ax.axvline(x=time_response_phase_temp[xc], color=color_set[j], linewidth=0.5, linestyle='--')

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=3)

    fig.savefig(container_name + "cpu_overview.pdf", dpi=fig.dpi)
    # plt.show()
    plt.close(fig)

    phase_reminder = len(time_response_phase_temp) % 3
    phase_range = (len(time_response_phase_temp) - phase_reminder) / 3

    for k in range(int(phase_range)):
        fig1, ax1 = plt.subplots(1, 1)
        generate_plot(list_x, list_y, time_response_phase_temp, "CPU usage(s)", "CPU usage of " + title_name,
                      color_set, k * 3, phase_information, ax1)
        # plt.show()
        fig1.savefig(container_name + "cpu_phase%s.pdf" % str(k + 1), dpi=fig1.dpi)
        plt.close(fig1)

    if phase_reminder != 0:
        fig3, ax3 = plt.subplots(1, 1)
        ax3.plot(list_x, list_y)
        ax3.set_xlabel("Time relatives to start time(s)")
        ax3.set_ylabel("CPU usage(s)")
        ax3.set_title("CPU usage of " + title_name + " -- phase {}: ".format(k + 2) + phase_information[k + 1], y=1.08)
        ax3.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
                    linestyle='dashed',
                    label="last phase start: " + str(time_response_phase_temp[len(time_response_phase_temp) - 2]))
        # ax3.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
        #             linestyle='dashed',
        #             label="last phase end: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))
        ax3.plot([], [], ' ', label='Max: {} at {}'.format(ymax, xmax))
        ax3.plot([], [], ' ', label='Max difference : {}'.format(max_diff))

        ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=5)

        ax3.set_xlim(time_response_phase_temp[len(time_response_phase_temp) - 1] - 0.03,
                     time_response_phase_temp[len(time_response_phase_temp) - 1] + 0.5)
        fig3.savefig(container_name + "cpu_phase{}.pdf".format(k + 2))
        plt.close(fig3)

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(list_x, list_y)
    ax2.set_xlabel("Time relatives to start time(s)")
    ax2.set_ylabel("CPU usage(s)")
    ax2.set_title("CPU usage of " + title_name + " -- After the last phase", y=1.08)
    ax2.axvline(x=time_response_phase_temp[len(time_response_phase_temp) - 1], color=color_set[j], linewidth=0.5,
                linestyle='dashed',
                label="last phase end: " + str(time_response_phase_temp[len(time_response_phase_temp) - 1]))

    ax2.plot([], [], ' ', label='Max: {} at {}'.format(ymax, xmax))
    ax2.plot([], [], ' ', label='Max difference : {}'.format(max_diff))

    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)

    ax2.set_xlim(time_response_phase_temp[len(time_response_phase_temp) - 1] - 0.03,
                 time_response_phase_temp[len(time_response_phase_temp) - 1] + 4)
    fig2.savefig(container_name + "cpu_after_last_phase.pdf")
    # plt.show()
    plt.close(fig2)


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
    driver = webdriver.Chrome(executable_path)  # use chromedriver as driver to open browser.
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


# Update a post on the WordPress website.
def update_wordpress(output_file):
    email = "414052254@qq.com"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"
    time_phase = []
    time_phase_total = []
    phase_info = []
    temp = 0

    # options = webdriver.ChromeOptions()
    # options.add_argument("user-data-dir=/Users/james/Library/Application Support/Google/Chrome")
    driver = webdriver.Chrome(executable_path)  # use chromedriver as driver to open browser.
    temp = time.time_ns()
    # print("Before open website", temp)
    time_phase.append(temp)
    driver.get('http://localhost:8000/wp-admin')  # go to the website.
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    elem = driver.find_element_by_id("user_login")  # find the element to put login.
    elem.send_keys(email)  # send the login information.
    elem = driver.find_element_by_id("user_pass")
    elem.send_keys(pass_code)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    time.sleep(1)

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    temp = time.time_ns()
    # print("After open website and login", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_css_selector(".menu-icon-post > .wp-menu-name")  # Find the POST.
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After clicking the post", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'New Title')]")  # Find the post to edit.
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After finding the post to edit and click", temp)
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
    time.sleep(1)
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
    time.sleep(1)

    elem.click()

    time_ms = time.time_ns() / 1000000
    time_phase_total.append(time_ms)
    temp = time.time_ns()
    # print("After updating and finding the update button and update", temp)
    time_phase.append(temp)

    phase_info.append("Open the website")
    phase_info.append("Login to the admin page")
    phase_info.append("Find and click the 'Post button")
    phase_info.append("Find and click the post to update")
    phase_info.append("Update content and publish the post")

    # with open(output_file, "w") as f:
    #     f.write("Information about the phases of adding new contents to a post in a WordPress website.\n\n")
    #     f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
    #     f.write("Phase 1 : Open the website and log in." + "\n")
    #     f.write(
    #         "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
    #             nano_read(time_phase[1])) + "\n")
    #     f.write("Phase 2 : Find and click the post button that manages posts of the website." + "\n")
    #     f.write("The time after clicking the post button to manage posts is at: " + str(
    #         time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    #     f.write("Phase 3 : Find the particular post to edit." + "\n")
    #     f.write("The time after finding the post to edit is at: " + str(time_phase[3]) + ". Real time: " + str(
    #         nano_read(time_phase[3])) + "\n")
    #     f.write("Phase 4 : Add new content to the post and update it." + "\n")
    #     f.write("The time after updating the post is at: " + str(time_phase[4]) + ". Real time: " + str(
    #         nano_read(time_phase[4])) + "\n\n")
    # f.close()
    return time_phase_total, phase_info


# Update a post on the Drupal website.
def update_drupal(output_file):
    time_phase_total = []
    phase_info = []

    driver = webdriver.Chrome(executable_path)
    time_phase = []
    before = time.time_ns()
    # print("before open website", before)
    time_phase.append(before)
    driver.get("http://localhost:8010/user/login")  # go to the website.

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    user = "jameszhao"
    # user = "James Zhao"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"

    elem = driver.find_element_by_id("edit-name")  # find the element to put login.
    elem.send_keys(user)  # send the login information.
    elem = driver.find_element_by_id("edit-pass")
    elem.send_keys(pass_code)
    time.sleep(1)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    after = time.time_ns()
    # print("after open website and login", after)
    time_phase.append(after)

    elem = driver.find_element_by_id("toolbar-link-system-admin_content")  # find the Content
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After finding the content button and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'New Title')]")
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)
    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    elem = driver.find_element_by_link_text("Edit")  # Find the edit button.
    time.sleep(1)

    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After finding the post, edit button and click it", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//html/body")
    elem.click()

    driver.switch_to.frame(0)  # switch to frame0 which has html for the new post.

    elem = driver.find_element_by_xpath("//html/body")  # find the element again.
    elem.send_keys(content)

    driver.switch_to.default_content()  # swtich back to the page.

    elem = driver.find_element_by_id("edit-submit")
    time.sleep(1)
    elem.click()

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()

    # print("After finding the place to put new content and update.", temp)
    time_phase.append(temp)

    phase_info.append("Open the website")
    phase_info.append("Login to the admin page")
    phase_info.append("Find and click the 'Content' button")
    phase_info.append("Find and click the post to update")
    phase_info.append("Find and click the 'Edit' button")
    phase_info.append("Update content and publish the post")

    # with open(output_file, "w") as f:
    #     f.write("Information about the phases of adding new contents to a post in a Drupal website.\n\n")
    #     f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
    #     f.write("Phase 1 : Open the website and log in." + "\n")
    #     f.write(
    #         "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
    #             nano_read(time_phase[1])) + "\n")
    #     f.write("Phase 2 : Find and click the content button that manages posts of the website." + "\n")
    #     f.write("The time after clicking the content button to manage posts is at: " + str(
    #         time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    #     f.write("Phase 3 : Find the particular post to edit." + "\n")
    #     f.write("The time after finding the post to edit is at: " + str(time_phase[3]) + ". Real time: " + str(
    #         nano_read(time_phase[3])) + "\n")
    #     f.write("Phase 4 : Add new content to the post and update it." + "\n")
    #     f.write("The time after updating the post is at: " + str(time_phase[4]) + ". Real time: " + str(
    #         nano_read(time_phase[4])) + "\n\n")
    # f.close()
    return time_phase_total, phase_info


#  Create a post on the WordPress website.
def create_wordpress(output_file):
    email = "414052254@qq.com"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"
    time_phase_total = []
    tiem_phase = []
    temp = 0
    phase_info = []

    driver = webdriver.Chrome(executable_path)  # use chromedriver as driver to open browser.

    driver.get('http://localhost:8000/wp-admin')  # go to the website.

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    temp = time.time_ns()
    time_phase.append(temp)
    # print("Before open website", temp)
    # print("end ", domComplete)
    # print("backend: ", backend)
    # print("frontend: ", frontend)

    elem = driver.find_element_by_id("user_login")  # find the element to put login.
    elem.send_keys(email)  # send the login information.
    elem = driver.find_element_by_id("user_pass")
    elem.send_keys(pass_code)
    time.sleep(1)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    temp = time.time_ns()

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")

    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    time_phase.append(temp)
    # print("After open website and login", temp)
    # print("backend: ", backend)
    # print("frontend: ", frontend)
    # print("end", responseStart)

    elem = driver.find_element_by_css_selector(".menu-icon-post > .wp-menu-name")  # Find the POST.
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    temp = time.time_ns()
    time_phase.append(temp)
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart
    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    # print("After clicking the post", temp)
    # print("backend: ", backend)
    # print("frontend: ", frontend)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("(//a[contains(text(),'Add New')])[6]")  # Find the ADD NEW to click.
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    temp = time.time_ns()
    # print("After finding the ADD NEW button and click", temp)
    # print("backend: ", backend)
    # print("frontend: ", frontend)
    time_phase.append(temp)

    elem = driver.find_element_by_id("post-title-0")
    elem.send_keys(title)

    elem = driver.find_element_by_class_name(
        "edit-post-more-menu")  # Find the menu to change the visual mode to code mode,
    # so we can find the "post-content-0" to edit content.

    elem.click()

    elem = driver.find_element_by_css_selector(".components-menu-group:nth-child(2) .components-button:nth-child(2)")
    time.sleep(0.5)
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                       ".components-menu-group:nth-child(2) .components-button:nth-child(2)")))  # Found the element through the Seleium IDE. Could not find it
    elem.click()

    elem = driver.find_element_by_id("post-content-0")
    elem.send_keys(content)
    elem = driver.find_element_by_css_selector(".editor-post-publish-panel__toggle")
    elem.click()

    elem = driver.find_element_by_css_selector(".editor-post-publish-button")
    time.sleep(1)
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".editor-post-publish-button")))
    elem.click()

    time_ms = time.time_ns() / 1000000

    # navigationStart = driver.execute_script("return window.performance.timing.requestStart")
    # responseStart = driver.execute_script("return window.performance.timing.responseStart")
    # domComplete = driver.execute_script("return window.performance.timing.domComplete")
    # print("After create a new post and finding the update button and update", temp)
    temp = time.time_ns()
    #print(time_ms - domComplete)
    time_phase_total.append(time_ms)
    # backend = responseStart - navigationStart
    # frontend = domComplete - navigationStart
    # time_phase_total.append(navigationStart)
    # time_phase_total.append(responseStart)
    # time_phase_total.append(domComplete)
    # print("backend: ", backend)
    # print("frontend: ", frontend)

    # print("After create a new post and finding the update button and update", temp)
    time_phase.append(temp)

    phase_info.append("Open the website")
    phase_info.append("Login to the admin page")
    phase_info.append("Find and click the 'Post button")
    phase_info.append("Find and click the 'Add new' button")
    phase_info.append("Add content and publish the post")

    # with open(output_file, "w") as f:
    #     f.write("Information about the phases of creating a new post in a WordPress website.\n\n")
    #     f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
    #     f.write("Phase 1 : Open the website and log in." + "\n")
    #     f.write(
    #         "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
    #             nano_read(time_phase[1])) + "\n")
    #     f.write("Phase 2 : Find and click the post button that manages posts of the website." + "\n")
    #     f.write("The time after clicking the post button to manage posts is at: " + str(
    #         time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    #     f.write("Phase 3 : Find the add new button to creat a post." + "\n")
    #     f.write("The time after finding the add new button is at: " + str(time_phase[3]) + ". Real time: " + str(
    #         nano_read(time_phase[3])) + "\n")
    #     f.write("Phase 4 : Add new title and content to the post and publish it." + "\n")
    #     f.write("The time after creating the post is at: " + str(time_phase[4]) + ". Real time: " + str(
    #         nano_read(time_phase[4])) + "\n\n")
    # f.close()
    return time_phase_total, phase_info


#  Create a post on the Drupal website.
def create_drupal(output_file):
    driver = webdriver.Chrome(executable_path)
    time_phase = []
    time_phase_total = []
    phase_info = []
    user = "jameszhao"
    # user = "James Zhao"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"

    before = time.time_ns()
    # print("before open website", before)
    time_phase.append(before)
    driver.get("http://localhost:8010/user/login")  # go to the website.
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("backend:", backend)
    # print("frontend", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    elem = driver.find_element_by_id("edit-name")  # find the element to put login.
    elem.send_keys(user)  # send the login information.
    elem = driver.find_element_by_id("edit-pass")
    elem.send_keys(pass_code)
    time.sleep(1)
    elem.send_keys(Keys.RETURN)  # send the Enter command.

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("backend:", backend)
    # print("frontend", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    after = time.time_ns()
    # print("after open website and login", after)
    time_phase.append(after)

    elem = driver.find_element_by_id("toolbar-link-system-admin_content")  # find the Content

    time.sleep(1)

    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("backend:", backend)
    # print("frontend", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After finding the content button and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_link_text("Add content")  # find ADD CONTENT button
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("backend:", backend)
    # print("frontend", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    temp = time.time_ns()
    # print("After finding ADD CONTENT button and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_css_selector(".clearfix:nth-child(1) > a:nth-child(1)")  # Select the type article.
    time.sleep(1)
    elem.click()

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("backend:", backend)
    # print("frontend", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    elem = driver.find_element_by_id("edit-title-0-value")
    elem.send_keys(title)

    elem = driver.find_element_by_xpath("//html/body")
    elem.click()

    driver.switch_to.frame(0)  # switch to frame0 which has html for the new post.

    elem = driver.find_element_by_xpath("//html/body")  # find the element again.
    elem.send_keys(content)

    driver.switch_to.default_content()  # swtich back to the page.

    elem = driver.find_element_by_id("edit-submit")
    time.sleep(1)
    elem.click()

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("After creating a new post and publish.", temp)
    #
    # print("backend:", backend)
    # print("frontend", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    temp = time.time_ns()

    time_phase.append(temp)
    phase_info.append("Open the website")
    phase_info.append("Login to the admin page")
    phase_info.append("Find and click the 'Content' button")
    phase_info.append("Find and click the 'Add content' button")
    phase_info.append("Select the article type")
    phase_info.append("Add content and publish the post")
    # with open(output_file, "w") as f:
    #     f.write("Information about the phases of creating a new post in a Drupal website.\n\n")
    #     f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
    #     f.write("Phase 1 : Open the website and log in." + "\n")
    #     f.write(
    #         "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
    #             nano_read(time_phase[1])) + "\n")
    #     f.write("Phase 2 : Find and click the content button that manages posts of the website." + "\n")
    #     f.write("The time after clicking the content button to manage posts is at: " + str(
    #         time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    #     f.write("Phase 3 : Find the add content button to creat a post." + "\n")
    #     f.write("The time after finding the add content button is at: " + str(time_phase[3]) + ". Real time: " + str(
    #         nano_read(time_phase[3])) + "\n")
    #     f.write("Phase 4 : Add new title and content to the post and publish it." + "\n")
    #     f.write("The time after creating the post is at: " + str(time_phase[4]) + ". Real time: " + str(
    #         nano_read(time_phase[4])) + "\n\n")
    # f.close()
    return time_phase_total, phase_info


#  Delete a post on the WordPress website.
def delete_wordpress(output_file):
    email = "414052254@qq.com"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"
    time_phase = []
    temp = 0
    time_phase_total = []
    phase_info = []

    # options = webdriver.ChromeOptions()
    # options.add_argument("user-data-dir=/Users/james/Library/Application Support/Google/Chrome")
    driver = webdriver.Chrome(executable_path)  # use chromedriver as driver to open browser.
    temp = time.time_ns()
    # print("Before open website", temp)
    time_phase.append(temp)
    driver.get('http://localhost:8000/wp-admin')  # go to the website.

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart
    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    elem = driver.find_element_by_id("user_login")  # find the element to put login.
    elem.send_keys(email)  # send the login information.
    elem = driver.find_element_by_id("user_pass")
    elem.send_keys(pass_code)
    time.sleep(1)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After open website and login", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_css_selector(".menu-icon-post > .wp-menu-name")  # Find the POST.
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After clicking the post", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'New Title')]")  # Find the post to delete.
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After finding the post to delete and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_css_selector(".editor-post-trash")
    time.sleep(1)
    elem.click()
    time_ms = time.time_ns() / 1000000
    time_phase_total.append(time_ms)
    temp = time.time_ns()
    # print("After putting the post into the trash", temp)
    time_phase.append(temp)

    phase_info.append("Open the website")
    phase_info.append("Login to the admin page")
    phase_info.append("Find and click the 'Post button")
    phase_info.append("Find and click the post to delete")
    phase_info.append("Move the post to trash")

    # with open(output_file, "w") as f:
    #     f.write("Information about the phases of deleting a post in a WordPress website.\n\n")
    #     f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
    #     f.write("Phase 1 : Open the website and log in." + "\n")
    #     f.write(
    #         "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
    #             nano_read(time_phase[1])) + "\n")
    #     f.write("Phase 2 : Find and click the post button that manages posts of the website." + "\n")
    #     f.write("The time after clicking the post button to manage posts is at: " + str(
    #         time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    #     f.write("Phase 3 : Find the post to delete." + "\n")
    #     f.write("The time after finding the post to delete is at: " + str(time_phase[3]) + ". Real time: " + str(
    #         nano_read(time_phase[3])) + "\n")
    #     f.write("Phase 4 : Put the post into the trash." + "\n")
    #     f.write("The time after deleting the post is at: " + str(time_phase[4]) + ". Real time: " + str(
    #         nano_read(time_phase[4])) + "\n\n")
    # f.close()
    return time_phase_total, phase_info


#  Delete a post on the Drupal website.
def delete_drupal(output_file):
    time_phase_total = []
    phase_info = []
    driver = webdriver.Chrome(executable_path)
    time_phase = []
    before = time.time_ns()
    # print("before open website", before)
    time_phase.append(before)
    driver.get("http://localhost:8010/user/login")  # go to the website.

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    user = "jameszhao"
    # user = "James Zhao"
    pass_code = "zhaohaiyu"
    title = "New Title"
    content = "New content"

    elem = driver.find_element_by_id("edit-name")  # find the element to put login.
    elem.send_keys(user)  # send the login information.
    elem = driver.find_element_by_id("edit-pass")
    elem.send_keys(pass_code)
    time.sleep(1)
    elem.send_keys(Keys.RETURN)  # send the Enter command.
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    after = time.time_ns()
    # print("after open website and login", after)
    time_phase.append(after)

    elem = driver.find_element_by_id("toolbar-link-system-admin_content")  # find the Content

    time.sleep(1)

    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After finding the content button and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'New Title')]")  # Find the post to delete.
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After finding the post to delete and click", temp)
    time_phase.append(temp)

    elem = driver.find_element_by_xpath("//a[contains(text(),'Delete')]")  # Find the delete button.
    time.sleep(1)
    elem.click()
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    elem = driver.find_element_by_id("edit-submit")
    time.sleep(1)
    elem.click()

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart

    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    # print("After deleting the post.", temp)
    time_phase.append(temp)

    phase_info.append("Open the website")
    phase_info.append("Login to the admin page")
    phase_info.append("Find and click the 'Content' button")
    phase_info.append("Find and click the post to delete")
    phase_info.append("Find and click the 'Delete' button")
    phase_info.append("Confirm deleting the post")

    # with open(output_file, "w") as f:
    #     f.write("Information about the phases of deleting a post in a Drupal website.\n\n")
    #     f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
    #     f.write("Phase 1 : Open the website and log in." + "\n")
    #     f.write(
    #         "The time after opening the website and logging in is at: " + str(time_phase[1]) + ". Real time: " + str(
    #             nano_read(time_phase[1])) + "\n")
    #     f.write("Phase 2 : Find and click the content button that manages posts of the website." + "\n")
    #     f.write("The time after clicking the content button to manage posts is at: " + str(
    #         time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    #     f.write("Phase 3 : Find the post to delete." + "\n")
    #     f.write("The time after finding the post to delete is at: " + str(time_phase[3]) + ". Real time: " + str(
    #         nano_read(time_phase[3])) + "\n")
    #     f.write("Phase 4 : Deleting the post." + "\n")
    #     f.write("The time after deleting the post is at: " + str(time_phase[4]) + ". Real time: " + str(
    #         nano_read(time_phase[4])) + "\n\n")
    # f.close()
    return time_phase_total, phase_info


#  View a post on the WordPress website.
def view_wordpress_post(output_file):
    time_phase_total = []
    phase_info = []
    time_phase = []
    driver = webdriver.Chrome(executable_path)  # use chromedriver as driver to open browser.
    temp = time.time_ns()
    # print("Before opening the website", temp)
    time_phase.append(temp)
    driver.get('http://localhost:8000')  # go to the website.
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart
    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    temp = time.time_ns()
    time_phase.append(temp)
    # print("After opening the website", temp)
    elem = driver.find_element_by_link_text("New Title")
    time.sleep(1)
    elem.click()

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart
    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)
    temp = time.time_ns()
    time_phase.append(temp)
    # print("After finding the post and click it", temp)
    phase_info.append("Open the website")
    phase_info.append("Find and click the post to view")
    # with open(output_file, "w") as f:
    #     f.write("Information about the phases of viewing a post in a WordPress website.\n\n")
    #     f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
    #     f.write("Phase 1 : Open the website." + "\n")
    #     f.write(
    #         "The time after opening the website is at: " + str(time_phase[1]) + ". Real time: " + str(
    #             nano_read(time_phase[1])) + "\n")
    #     f.write("Phase 2 : Find the post and view it." + "\n")
    #     f.write("The time after clicking the post to view is at: " + str(
    #         time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    # f.close()
    return time_phase_total, phase_info


#  View a post on the Drupal website.
def view_drupal_post(output_file):
    phase_info = []
    time_phase_total = []

    time_phase = []
    driver = webdriver.Chrome(executable_path)  # use chromedriver as driver to open browser.
    temp = time.time_ns()

    time_phase.append(temp)
    # print("Before opening the website", temp)
    driver.get('http://localhost:8010')  # go to the website.
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    temp = time.time_ns()
    # print("After opening the website", temp)
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart
    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    temp = time.time_ns()
    time_phase.append(temp)

    elem = driver.find_element_by_link_text("New Title")
    time.sleep(1)
    elem.click()

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    backend = responseStart - navigationStart
    frontend = domComplete - responseStart
    # print("back end", backend)
    # print("front end", frontend)

    time_phase_total.append(navigationStart)
    time_phase_total.append(responseStart)
    time_phase_total.append(domComplete)

    temp = time.time_ns()
    time_phase.append(temp)
    # print("After finding the post and click it", temp)
    phase_info.append("Open the website")
    phase_info.append("Find and click the post to view")

    # with open(output_file, "w") as f:
    #     f.write("Information about the phases of viewing a post in a Drupal website.\n\n")
    #     f.write("The start time is at : " + str(time_phase[0]) + ". Real time: " + str(nano_read(time_phase[0])) + "\n")
    #     f.write("Phase 1 : Open the website." + "\n")
    #     f.write(
    #         "The time after opening the website is at: " + str(time_phase[1]) + ". Real time: " + str(
    #             nano_read(time_phase[1])) + "\n")
    #     f.write("Phase 2 : Find the post and view it." + "\n")
    #     f.write("The time after clicking the post to view is at: " + str(
    #         time_phase[2]) + ". Real time: " + str(nano_read(time_phase[2])) + "\n")
    # f.close()
    return time_phase_total, phase_info


# Update the varibale names for each workload.
def get_variables(ct_name, operation_type):
    global cpu_file, memory_file, block_file, network_file, update_wp_file, update_dp_file, create_wp_file, create_dp_file
    global create_wp_file, delete_dp_file, delete_wp_file, update_title_name_dp, update_title_name_wp, create_title_name_dp
    global create_title_name_wp, delete_title_name_dp, delete_title_name_wp, container_name
    global view_wp_file, view_dp_file, view_title_name_wp, view_title_name_dp

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
    view_title_name_dp = ct_name + "container of viewing a post on a Drupal website"

    container_name = ct_name + "_" + operation_type + "_"


if __name__ == "__main__":
    # Depends on the operation type, call different functions to process files and produce graphs.
    operation_type = sys.argv[1]
    time_phase = []
    time_response_phase = []
    phase_information = []

    if operation_type == "update":
        if len(sys.argv) == 3:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase, phase_information = update_wordpress(update_wp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, update_wp_file, update_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, update_wp_file, update_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, update_wp_file, update_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, update_wp_file, update_title_name_wp, container_name,
                            phase_information)

            elif "drupal" in container_name:
                time_phase, phase_information = update_drupal(update_dp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, update_dp_file, update_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, update_dp_file, update_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, update_dp_file, update_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, update_dp_file, update_title_name_dp, container_name,
                            phase_information)
        elif len(sys.argv) == 4:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase, phase_information = update_wordpress(update_wp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, update_wp_file, update_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, update_wp_file, update_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, update_wp_file, update_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, update_wp_file, update_title_name_wp, container_name,
                            phase_information)

                get_variables(sys.argv[3], operation_type)

                process_memory(time_phase, memory_file, update_wp_file, update_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, update_wp_file, update_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, update_wp_file, update_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, update_wp_file, update_title_name_wp, container_name,
                            phase_information)
            elif "drupal" in container_name:
                time_phase, phase_information = update_drupal(update_dp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, update_dp_file, update_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, update_dp_file, update_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, update_dp_file, update_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, update_dp_file, update_title_name_dp, container_name,
                            phase_information)
                get_variables(sys.argv[3], operation_type)
                process_memory(time_phase, memory_file, update_dp_file, update_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, update_dp_file, update_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, update_dp_file, update_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, update_dp_file, update_title_name_dp, container_name,
                            phase_information)
    elif operation_type == "create":
        if len(sys.argv) == 3:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase, phase_information = create_wordpress(create_wp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, create_wp_file, create_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, create_wp_file, create_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, create_wp_file, create_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, create_wp_file, create_title_name_wp, container_name,
                            phase_information)
            elif "drupal" in container_name:
                time_phase, phase_information = create_drupal(create_dp_file)
                # for h in range(len(time_phase)-1):
                #     print(int(time_phase[h + 1]) - int(time_phase[h]))
                time.sleep(15)
                process_memory(time_phase, memory_file, create_dp_file, create_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, create_dp_file, create_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, create_dp_file, create_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, create_dp_file, create_title_name_dp, container_name,
                            phase_information)
        elif len(sys.argv) == 4:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase, phase_information = create_wordpress(create_wp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, create_wp_file, create_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, create_wp_file, create_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, create_wp_file, create_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, create_wp_file, create_title_name_wp, container_name,
                            phase_information)

                get_variables(sys.argv[3], operation_type)

                process_memory(time_phase, memory_file, create_wp_file, create_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, create_wp_file, create_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, create_wp_file, create_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, create_wp_file, create_title_name_wp, container_name,
                            phase_information)
            elif "drupal" in container_name:
                time_phase, phase_information = create_drupal(create_dp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, create_dp_file, create_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, create_dp_file, create_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, create_dp_file, create_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, create_dp_file, create_title_name_dp, container_name,
                            phase_information)

                get_variables(sys.argv[3], operation_type)

                process_memory(time_phase, memory_file, create_dp_file, create_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, create_dp_file, create_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, create_dp_file, create_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, create_dp_file, create_title_name_dp, container_name,
                            phase_information)
    elif operation_type == "delete":
        if len(sys.argv) == 3:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase, phase_information = delete_wordpress(delete_wp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, delete_wp_file, delete_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, delete_wp_file, delete_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, delete_wp_file, delete_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, delete_wp_file, delete_title_name_wp, container_name,
                            phase_information)
            elif "drupal" in container_name:
                time_phase, phase_information = delete_drupal(delete_dp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, delete_dp_file, delete_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, delete_dp_file, delete_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, delete_dp_file, delete_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, delete_dp_file, delete_title_name_dp, container_name,
                            phase_information)
        elif len(sys.argv) == 4:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase, phase_information = delete_wordpress(delete_wp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, delete_wp_file, delete_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, delete_wp_file, delete_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, delete_wp_file, delete_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, delete_wp_file, delete_title_name_wp, container_name,
                            phase_information)
                get_variables(sys.argv[3], operation_type)
                process_memory(time_phase, memory_file, delete_wp_file, delete_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, delete_wp_file, delete_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, delete_wp_file, delete_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, delete_wp_file, delete_title_name_wp, container_name,
                            phase_information)
            elif "drupal" in container_name:
                time_phase, phase_information = delete_drupal(delete_dp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, delete_dp_file, delete_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, delete_dp_file, delete_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, delete_dp_file, delete_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, delete_dp_file, delete_title_name_dp, container_name,
                            phase_information)
                get_variables(sys.argv[3], operation_type)
                process_memory(time_phase, memory_file, delete_dp_file, delete_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, delete_dp_file, delete_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, delete_dp_file, delete_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, delete_dp_file, delete_title_name_dp, container_name,
                            phase_information)
    elif operation_type == "view":
        if len(sys.argv) == 3:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase, phase_information = view_wordpress_post(view_wp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, view_wp_file, view_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, view_wp_file, view_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, view_wp_file, view_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, view_wp_file, view_title_name_wp, container_name,
                            phase_information)
            elif "drupal" in container_name:
                time_phase, phase_information = view_drupal_post(view_dp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, view_dp_file, view_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, view_dp_file, view_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, view_dp_file, view_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, view_dp_file, view_title_name_dp, container_name,
                            phase_information)
        elif len(sys.argv) == 4:
            get_variables(sys.argv[2], operation_type)
            if "wordpress" in container_name:
                time_phase, phase_information = view_wordpress_post(view_wp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, view_wp_file, view_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, view_wp_file, view_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, view_wp_file, view_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, view_wp_file, view_title_name_wp, container_name,
                            phase_information)
                get_variables(sys.argv[3], operation_type)
                process_memory(time_phase, memory_file, view_wp_file, view_title_name_wp, container_name,
                               phase_information)
                process_block(time_phase, block_file, view_wp_file, view_title_name_wp, container_name,
                              phase_information)
                process_network(time_phase, network_file, view_wp_file, view_title_name_wp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, view_wp_file, view_title_name_wp, container_name,
                            phase_information)
            elif "drupal" in container_name:
                time_phase, phase_information = view_drupal_post(view_dp_file)
                time.sleep(15)
                process_memory(time_phase, memory_file, view_dp_file, view_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, view_dp_file, view_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, view_dp_file, view_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, view_dp_file, view_title_name_dp, container_name,
                            phase_information)
                get_variables(sys.argv[3], operation_type)
                process_memory(time_phase, memory_file, view_dp_file, view_title_name_dp, container_name,
                               phase_information)
                process_block(time_phase, block_file, view_dp_file, view_title_name_dp, container_name,
                              phase_information)
                process_network(time_phase, network_file, view_dp_file, view_title_name_dp, container_name,
                                phase_information)
                process_cpu(time_phase, cpu_file, view_dp_file, view_title_name_dp, container_name,
                            phase_information)
