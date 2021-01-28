import urllib
import json
from urllib.request import urlopen
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime





data = urllib.request.urlopen("http://ofenwatch.woller.pizza/php/ofenwatch/get_data.php").read()
output = json.loads(data)
print(output)
#audios = output['temperatures']
#print(output['audios'][0])

o0 = output[0]
o0_timestamp = o0['timestamp']

print(o0_timestamp)
format = "%Y-%m-%d %H:%M:%S"


timestamp1 = "2021-01-23 10:52:54"
timestamp2 = "2021-01-23 10:51:59"

time_start = datetime.strptime("2021-01-23 16:35:00", format)
time_end = datetime.strptime("2021-01-23 19:35:00", format)

t1 = datetime.strptime(timestamp1, format)
t2 = datetime.strptime(timestamp2, format)

difference = t2 - t1

print(difference.seconds) # 380, in this case

if timestamp1 < timestamp2:
    print("kleiner")
else:
    print("größer")




temps = []
t2hs = []
timePoints = []
timeStamps = []
i = 0

for x in output:
    temp1 = x['temp1']
    timestamp = datetime.strptime(x['timestamp'], format)
    temp2hold = x['temp2hold']
    ##if x['linktofile'] == "recording2_17-07-2019_15-15-15-1515.wav":
      ##  linktofile = x['linktofile']
        ##print("processing: " + linktofile)

    if timestamp > time_start and timestamp < time_end:
        if not temp1 == '0':
            print(temp1)
            temps.append(int(temp1))
            t2hs.append(int(230))
            timePoints.append(i)
            timeStamps.append(timestamp)

    i = i + 1

#print(temps)
print("i: " + str(i))
print(len(temps))
#plt.plot(timePoints, temps)
plt.plot(timePoints, temps)
plt.plot(timePoints, t2hs)
plt.ylabel('Temperatur °C')
plt.yticks(np.arange(100, 300, step=10))
plt.show()
