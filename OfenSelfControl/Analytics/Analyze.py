import urllib
import json
from urllib.request import urlopen
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime





data = urllib.request.urlopen("http://ofenwatch.woller.pizza/php/ofenwatch/get_data.php").read()
output = json.loads(data)
#print(output)
#audios = output['temperatures']
#print(output['audios'][0])

#o0 = output[0]
#o0_timestamp = o0['timestamp']

#print(o0_timestamp)
format = "%Y-%m-%d %H:%M:%S"

#pPot 1
#timestamp1 = "2021-01-23 10:52:54"
#timestamp2 = "2021-01-23 10:51:59"

time_start1 = datetime.strptime("2021-01-23 16:35:00", format)
time_end1 = datetime.strptime("2021-01-23 19:05:00", format)



#t1 = datetime.strptime(timestamp1, format)
#t2 = datetime.strptime(timestamp2, format)

# Plot 2
time_start2 = datetime.strptime("2021-02-06 13:40:00", format)
time_end2 = datetime.strptime("2021-02-06 16:10:00", format)

#difference = t2 - t1

#print(difference.seconds) # 380, in this case

#if timestamp1 < timestamp2:
 #   print("kleiner")
#else:
#    print("größer")




temps1 = []
t2hs1 = []
timePoints1 = []
timeStamps1 = []
i = 0
i_start = 0

for x in output:
    temp1 = x['temp1']
    timestamp = datetime.strptime(x['timestamp'], format)
    temp2hold = x['temp2hold']
    ##if x['linktofile'] == "recording2_17-07-2019_15-15-15-1515.wav":
      ##  linktofile = x['linktofile']
        ##print("processing: " + linktofile)

    if timestamp > time_start1 and timestamp < time_end1:
        if not temp1 == '0':
            i_start = 1
            print(temp1)
            temps1.append(int(temp1))
            t2hs1.append(int(230))
            timePoints1.append(i)
            timeStamps1.append(timestamp)

    if i_start == 1:
        i = i + 10



temps2 = []
t2hs2 = []
timePoints2 = []
timeStamps2 = []
j = 0
j_start = 0

for x in output:
    temp1 = x['temp1']
    timestamp = datetime.strptime(x['timestamp'], format)
    temp2hold = x['temp2hold']
    ##if x['linktofile'] == "recording2_17-07-2019_15-15-15-1515.wav":
      ##  linktofile = x['linktofile']
        ##print("processing: " + linktofile)

    if timestamp > time_start2 and timestamp < time_end2:
        j_start = 1
        if not temp1 == '0':
            print(temp1)
            temps2.append(int(temp1))
            t2hs2.append(int(220))
            timePoints2.append(j)
            timeStamps2.append(timestamp)

    if j_start == 1:
        j = j + 10

#print(temps)
print("i: " + str(i))
#print(len(temps))
#plt.plot(timePoints, temps)
plt.plot(timePoints1, temps1)
#plt.plot(timePoints1, t2hs1)
plt.plot(timePoints2, temps2)
plt.plot(timePoints2, t2hs2)
plt.ylabel('Temperatur °C')
plt.xlabel('Zeit in Sekunden')
plt.yticks(np.arange(100, 300, step=10))
plt.show()
