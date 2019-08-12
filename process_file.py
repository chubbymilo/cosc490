import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

with open('memory_log_c4.txt') as f:
    #line = f.readline()
    count= 0
    count_mesurement = 0
    list_x=[]
    list_y=[]
    temp = 0

    for line in f:
        line = line.split(" ")
        count += 1
        if count == 1:
            list_x.append(line[0])
        elif count == 2:
            temp += int(line[1])
        elif count == 3:
            temp+= int(line[1])
        elif count == 9:
            temp -= int(line[1])
        elif count ==10:
            temp -= int(line[1])
        elif count ==11:
            temp -= int(line[1])
        elif count ==12:
            temp -= int(line[1])
            list_y.append(temp)
        #print(count, line)
        if count == 35:
            temp = 0
            count_mesurement += 1
            count = 0
    print (count_mesurement)
    #print list_x
    #print list_y
    plt.ylim(8.8e7,10e7)
    plt.plot(list_x,list_y)
    plt.show()




