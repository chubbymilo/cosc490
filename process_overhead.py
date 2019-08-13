import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# process_memory cpu block and network methods process the raw data and shows the difference of time between each data
# point in ms.
# The main difference method is the number of lines need to be processed.


def process_memory(filename):
    with open(filename) as f:
        count= 0
        count_mesurement = 1
        list_x = [ ]
        list_y = [ ]
        temp = 0
        pre_timestamp = 0
        start = 0

        for line in f:
            line = line.split(" ")
            count += 1
            if count == 1:
                tmp_time = int((line[ 0 ])[ 0:19 ])
                if count_mesurement == 1:
                    pre_timestamp = tmp_time
                    start = tmp_time
                else:
                    list_y.append((tmp_time - pre_timestamp) / 1000000)
                    if ((tmp_time - pre_timestamp) / 1000000) < 0:
                        print((tmp_time - pre_timestamp) / 1000000)
                        print(count_mesurement)
                    # print((int(line[0])-pre_timestamp)/1000000)
                    pre_timestamp = tmp_time
                    list_x.append(count_mesurement)
            # print(count, line)
            if count == 34:
                temp = 0
                count_mesurement += 1
                count = 0
        print(count_mesurement - 1)
        print("start time is ", start)
        print("End time is ", pre_timestamp)
        print("Duration is", pre_timestamp - start)
        print("Time for each command : ", (pre_timestamp - start) / float(count_mesurement) / 1000000)
        # print list_x
        # print (list_y)
        plt.plot(list_x, list_y, "o")
        print(list_y)
        plt.show()


def process_cpu(filename):
    with open(filename) as f:
        count = 0
        count_measurement = 1
        list_x = []
        list_y = []
        pre_timestamp = 0
        start = 0

        for line in f:
            line = line.split(" ")
            count += 1
            if count == 1:
                tmp_time = int((line[ 0 ])[ 0:19 ])
                if count_measurement == 1:
                    pre_timestamp = tmp_time
                    start = tmp_time
                else:
                    list_y.append((tmp_time - pre_timestamp) / 1000000)
                    if ((tmp_time - pre_timestamp) / 1000000) < 0:
                        print((tmp_time - pre_timestamp) / 1000000)
                        print(count_measurement)
                    pre_timestamp = tmp_time
                    list_x.append(count_measurement)
            if count == 2:
                count_measurement += 1
                count = 0
        print(count_measurement - 1)
        print("start time is ", start)
        print("End time is ", pre_timestamp)
        print("Duration is", pre_timestamp - start)
        print("Time for each command : ", (pre_timestamp - start) / float(count_measurement) / 1000000)
        # print list_x
        # print (list_y)
        plt.plot(list_x, list_y)
        print(list_y)
        plt.show()


def process_block(filename):
    with open(filename) as f:
        count = 0
        count_measurement = 1
        list_x = [ ]
        list_y = [ ]
        pre_timestamp = 0
        start = 0

        for line in f:
            line = line.split(" ")
            count += 1
            if count == 1:
                tmp_time = int((line[ 0 ])[ 0:19 ])
                if count_measurement == 1:
                    pre_timestamp = tmp_time
                    start = tmp_time
                else:
                    list_y.append((tmp_time - pre_timestamp) / 1000000)
                    if ((tmp_time - pre_timestamp) / 1000000) < 0:
                        print((tmp_time - pre_timestamp) / 1000000)
                        print(count_measurement)
                    pre_timestamp = tmp_time
                    list_x.append(count_measurement)
            if count == 12:
                count_measurement += 1
                count = 0
        print(count_measurement - 1)
        print("start time is ", start)
        print("End time is ", pre_timestamp)
        print("Duration is", pre_timestamp - start)
        print("Time for each command : ", (pre_timestamp - start) / float(count_measurement) /1000000)
        # print list_x
        # print (list_y)
        plt.plot(list_x, list_y,"o")
        print(list_y)
        plt.show()


def process_network(filename):
    with open(filename) as f:
        count = 0
        count_measurement = 1
        list_x = [ ]
        list_y = [ ]
        pre_timestamp = 0
        start = 0

        for line in f:
            line = line.split(" ")
            count += 1
            if count == 1:
                tmp_time = int((line[ 0 ])[ 0:19 ])
                if count_measurement == 1:
                    pre_timestamp = tmp_time
                    start = tmp_time
                else:
                    list_y.append((tmp_time - pre_timestamp) / 1000000)
                    if ((tmp_time - pre_timestamp) / 1000000) < 0:
                        print((tmp_time - pre_timestamp) / 1000000)
                        print(count_measurement)
                    pre_timestamp = tmp_time
                    list_x.append(count_measurement)
            if count == 6:
                count_measurement += 1
                count = 0
        print(count_measurement - 1)
        print("start time is ", start)
        print("End time is ", pre_timestamp)
        print("Duration is", pre_timestamp - start)
        print("Time for each command : ", (pre_timestamp - start) / float(count_measurement) /1000000)
        # print list_x
        # print (list_y)
        plt.plot(list_x, list_y,"o")
        print(list_y)
        plt.show()


if  __name__ ==  "__main__":


   process_memory('memory_log_c4.txt')
  # process_network('network_log_c.txt')
  # process_cpu('cpu_log_c.txt')
  # process_block('block_log_c.txt')
