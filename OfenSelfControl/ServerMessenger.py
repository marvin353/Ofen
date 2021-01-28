#from OfenTempAnalyzer2 import OfenTempAnalyzer2
import threading
import time
import numpy as np
import requests


class ServerMessenger:

    API_ENDPOINT = "http://ofenwatch.woller.pizza/php/ofenwatch/process_incoming_data.php"
    #API_KEY = "XXXXXXXXXXXXXXXXX"

    def __init__(self, ofen):
        self.ofen = ofen


    def uploadData(self):
        try:
            print("Uploading new data...")

            ofenid = self.ofen.get_ofenid()
            temps = self.ofen.get_currentTempsArray()
            drosselklappe = self.ofen.get_Drosselklappe()
            airInput = self.ofen.get_airInput()
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
                    'airInput': airInput,
                    'fastheatup': fastHeatup,
                    'automode': automode}

            # sending post request and saving response as response object
            r = requests.post(url=self.API_ENDPOINT, data=data)

            # extracting response text
            pastebin_url = r.text
            print("Response:%s" % pastebin_url)
        except:
            print("Error while uploading")


    def sendOfflineSignal(self):
        print("Offline signal being sent...")

    def sendOnlineSignal(self):
        print("Uploading new data...")

    def logIn(self):
        print("Login requested")

        return False











