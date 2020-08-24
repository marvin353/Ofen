from OfenTempAnalyzer import OfenTempAnalyzer
#from BTObserver import BTObserver
import threading
import time
import numpy as np
import requests


class ServerMessenger:

    a = [[0,0,0,0,0,0,0]]
    link_API = "http://..."
    link_Dashboard = "http://..."

    API_ENDPOINT = "http://ofenwatch.woller.pizza/yamifood/php/ofenwatch/process_incoming_data.php"
    API_KEY = "XXXXXXXXXXXXXXXXX"

    def __init__(self, ofen):
        self.ofen = ofen


    def uploadData(self):
        print("Uploading new data...")

        ofenid = self.ofen.get_ofenid()
        temps = self.ofen.get_currentTempsArray()
        drosselklappe = self.ofen.get_Drosselklappe()
        steamRegularizers = self.ofen.get_steamRegularizersValue()
        fan = self.ofen.get_FanValue()
        fastHeatup = self.ofen.get_FastHeatupValue()
        temp2hold = self.ofen.get_temp2hold()
        #now = datetime.now()
        #date_time = now.strftime("%d-%m-%Y, %H:%M:%S")
        automode = self.ofen.get_autoMode()
        predictedTemps = [0, 0, 0]

        # data to be sent to api
        data = {'ofenid': ofenid,
                'temp1': int(temps[0]),
                'temp2': int(temps[1]),
                'temp3': int(temps[2]),
                'temp4': int(temps[3]),
                'temp5': int(temps[4]),
                'temp6': int(temps[5]),
                'temp7': int(temps[6]),
                'temp8': int(predictedTemps[0]),
                'temp9': int(predictedTemps[1]),
                'temp10': int(predictedTemps[2]),
                'temp2hold': int(temp2hold),
                'dk': drosselklappe,
                'fan': fan,
                'srzs': steamRegularizers,
                'fastheatup': fastHeatup,
                'automode': automode}

        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, data=data)

        # extracting response text
        pastebin_url = r.text
        print("Response:%s" % pastebin_url)


    def sendOfflineSignal(self):
        print("Offline signal being sent...")

    def sendOnlineSignal(self):
        print("Uploading new data...")

    def logIn(self):
        print("Login requested")

        return False












# defining the api-endpoint
API_ENDPOINT = "http://ofenwatch.woller.pizza/php/ofenwatch/process_incoming_data.php"

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"

# your source code here
source_code = ''' 
print("Hello, world!") 
a = 1 
b = 2 
print(a + b) 
'''

# data to be sent to api
data = {'ofenid': '101',
        'temp1': '100',
        'temp2': '200',
        'temp3': '300',
        'temp4': '400'}

# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, data=data)

# extracting response text
pastebin_url = r.text
print("Response:%s" % pastebin_url)
