from OfenTempAnalyzer import OfenTempAnalyzer
#from BTObserver import BTObserver
import threading
import time
import numpy as np
from HardwareController import HardwareController

class Ofen:

    a = [[0,0,0,0,0,0,0]]

    def __init__(self, ofenID):
        self.ofenID = ofenID
        self.drosselklappe = 0.0
        self.fan = 0.0
        self.steamRegularizers = 0.0
        self.temp2hold = 0.0
        self.currentTemp = 0.0
        self.currentTemps = [0, 0, 0, 0, 0, 0, 0]
        self.isFastHeatUpActive = False
        self.alertCodes= {"lesswood":False, "sensorerror":False, "programfail":False}

        t1 = threading.Thread(target=self.collectData, args=())
        t1.start()

        self.tempAnalyzer = OfenTempAnalyzer(self)
        self.tempAnalyzer.activateAutonomousMode()
       # self.btObserver = BTObserver(self)
        self.hardwareController = HardwareController(self)


    def simulation(self):
        l = self.a[len(self.a)-1]
        x = []
        if(l[0] > 300):
            if (self.drosselklappe > 0.5):
                if (self.fan == 1.0):
                    x = np.random.randint(l[0]+5, l[0]+15, 7)
                else:
                    x = np.random.randint(l[0] - 5, l[0] + 10, 7)
            else:
                x = np.random.randint(l[0] - 10, l[0] + 5, 7)
        else:
            x = np.random.randint(l[0], l[0] + 10, 7)

        return x


    def collectData(self):

        while True:

            x = self.hardwareController.readTempDataFromArduino()

            #Only Simulation
            #x = self.simulation()

            print("X:" + str(x) + ",L: " + str(len(self.a)))

            if (len(self.a) > 59):
                self.a = self.a[1:60]
                self.a.append(x)
            else:
                 self.a.append(x)

            self.currentTemp = x[0]

            time.sleep(0.5)


    #value should be 0 or 1
    def moveSteamRegularizers(self):
        if (self.steamRegularizers == 1):
            self.steamRegularizers = 0.0
            self.hardwareController.moveSteamRegularizersDown()
            #TODO: Send message to server
            print("SteamRegularizers moved down")
        elif (self.steamRegularizers == 0):
            self.steamRegularizers = 1.0
            self.hardwareController.moveSteamRegularizersDown()

            #TODO: Send message to server
            print("SteamRegularizers moved up")
        else:
            print("SteamRegularizers could not be moved")

    def get_steamRegularizersValue(self):
        return self.steamRegularizers

    def activateFan(self):
        if (self.fan == 1.0):
            print("Fan is already running")
            return

        self.fan = 1.0
        self.hardwareController.turnFanOn()
        print("Fan: 100%")

    def stopFan(self):
        if(self.fan == 0.0):
            print("Fan is already stopped")
            return

        self.fan = 0.0
        self.hardwareController.turnFanOff()
        print("Fan: 0%")

    def get_FanValue(self):
        return self.fan

    def get_Drosselklappe(self):
        return self.drosselklappe

    def set_Drosselklappe(self, value):
        self.drosselklappe = value
        #TODO: Pi move drosselklappe to value
        print("Drosselklappe: " + str(int(value * 100)) + "%")

    def get_FastHeatupValue(self):
        return self.isFastHeatUpActive

    def fastHeatUp(self):
        self.setDrosselklappe(1.0)
        self.activateFan()
        self.isFastHeatUpActive = True
        print("Fast heat up mode active")

   # def fastHeatUp(self, temp):
    #    self.setDrosselklappe(1.0)
     #   self.activateFan()
      #  self.isFastHeatUpActive = False
       # print("Fast heat up mode active; With max temp value: " + str(int(temp)))

    def stopfastHeatUp(self):
        self.setDrosselklappe(0.5)
        self.stopFan()
        self.isFastHeatUpActive = False
        print("Fast heat up mode stopped")

    def get_a(self):
        return np.array(self.a)

    def get_a_n_last_values(self, length):
        ind_start = len(self.a) - length
        b = np.array(self.a[ind_start:])
        return np.array(b)

    def set_temp2hold(self, a):
        self.temp2hold = a

    def get_temp2hold(self):
        return self.temp2hold

    def get_currentTemp(self):
        return self.currentTemp

    def get_currentTempsArray(self):
        return self.currentTemps

    def get_ofenid(self):
        return self.ofenID

    def get_autoMode(self):
        return self.tempAnalyzer.get_AutonomousModeState()

    def set_autoModeOn(self):
        self.tempAnalyzer.activateAutonomousMode()

    def set_autoModeOff(self):
        self.tempAnalyzer.deactivateAutonomousMode()


    def onShutdown(self):
        print("Shutdown initialized...")
        self.set_autoModeOff()
        self.setDrosselklappe(0.0)
        self.stopFan()
        self.isFastHeatUpActive = False
        #TODO call all shutdown funtions

    def restoreLastValues(self, dict):




    def printHalloOfen(self):
        print("hallo OFen: " + str(threading.get_ident()))

    def triggerAlert(self, code, message):
        if code == "lessWood":
            # trigger push notification for adding new wood
            print("time to add more wood")
            self.alertCodes["lesswood"] = True
        elif code == "sensor_error":
            print("Error occured check Sensors")
        elif code == "read_serial_error":
            print("Error occured check Sensors")

    def get_alertCodes(self):
        return self.alertCodes

    def printCurrentState(self):
        print("Fan: " + str(int(self.fan*100)) + "% ; Drosselklappe: " + str(int(self.drosselklappe*100)) + "% ; CurrentTemp: " + str(self.currentTemp) + "; SRZs: " + str(self.steamRegularizers))