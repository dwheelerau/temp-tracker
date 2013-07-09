#!/usr/bin/env python
import numpy
import serial
import time
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
from serial import SerialException

#get the serial
ser = serial.Serial('/dev/ttyUSB0',9600)
#these are reset each hour
temp_rec = []
#change this to [4] for testing will run every 1 min and draw graph at 12mins
#this is reset each day 12 to 12
filename = time.ctime()+".txt"

while True:
    try:
        #lets sleep for 10 seconds to save power
        #time.sleep(10)
        #main action part of the loop
        if ser.read(1) == '~':#start bite
            vals = []
            for x in range(25):
                #get rid of the first chunck of bytes
                discard_btye = ser.read()
                vals.append(ord(discard_btye))
                #print "this is btye number %s\n----"%x
            analH= vals[19]
            analL =  vals[20]
            analVal = (analH*256) + analL
            temp = (analVal/1023.0*1.2*3.0*100)-273.15
            temp_rec.append(temp)
            #write out the temp every hour need to add day function
            #write a graph sometime between 0-23 hr each day change to [4] for min
            nowh = time.localtime()[3]
            nowm = time.localtime()[4]
            #record each hour, start loop as clock ticks over
            if nowm == 59:
                ave_temp = numpy.average(temp_rec)
                print "On %s the temperature was %s deg C"%(time.ctime(),round(ave_temp,1))
                outfile = open(filename,'a')
                #hour\ttemp add 1 to hour since 59min
                out_data = "%s\t%s\n"%(nowh+1,round(ave_temp,1))
                outfile.write(out_data)
                outfile.close()
                #reset
                temp_rec = []
                hour = nowh
                #12 stuffs up the graph, use 0 instead
                if nowh == 12:
                    #draw a grahp ending in png here
                    temp_data = DataFrame(pd.read_table(filename,index_col=0\
                            ,header=None))
                    temp_data.plot(legend=False)
                    plt.xticks(temp_data.index)
                    plt.xlabel("Time of the day")
                    plt.ylabel("Temperature in celius")
                    plt.title("The temperature for  %s"%(filename[:-4]))
                    plt.savefig(filename[:-4])
                    plt.close()
                    #new file for writing todays temps
                    filename = time.ctime()+'.txt'
                else:
                    #testing make a graph every 2 hrs
                    pass


    except KeyboardInterrupt:
        ser.close()
        break

    except SerialException:
        pass

    except:
        print "some random error, just let if fly!"
        pass
