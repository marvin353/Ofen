from OfenTempAnalyzer import OfenTempAnalyzer
#from BTObserver import BTObserver
import threading
import time
import numpy as np
from HardwareController import HardwareController

class Ofen:

    a = [[0,0,0,0,0,0,0]]

    def __init__(self, ofenID, isSimulation):

        self.isSimulation = isSimulation

        self.isOnline = True

        self.ofenID = ofenID
        self.drosselklappe = 0.0
        self.fan = 0.0
        self.steamRegularizers = 0.0
        self.temp2hold = 0.0
        self.currentTemp = 0.0
        self.currentTemps = [0, 0, 0, 0, 0, 0, 0]
        self.isFastHeatUpActive = False
        self.alertCodes= {"lesswood":False, "sensorerror":False, "programfail":False}
        
        if(not self.isSimulation):
            self.hardwareController = HardwareController(self)

        self.t1 = threading.Thread(target=self.collectData, args=())
        self.t1.start()

        self.tempAnalyzer = OfenTempAnalyzer(self)
        #self.tempAnalyzer.activateAutonomousMode()

        #self.btObserver = BTObserver(self)

        


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

        while self.isOnline:

            #x = self.currentTemps

            # Only Simulation
            if (self.isSimulation):
                x = self.simulation()
            else:
                x = self.hardwareController.readTempDataFromArduino()

            print("X:" + str(x) + ",L: " + str(len(self.a)))

            #for idx,value in enumerate(x):
                #self.currentTemps[idx] = int(x[idx])
            self.currentTemps[0] = x[0]
            self.currentTemps[1] = x[1]
            self.currentTemps[2] = x[2]
            self.currentTemps[3] = x[3]
            self.currentTemps[4] = x[4]
            self.currentTemps[5] = x[5]
            self.currentTemps[6] = x[6]

           # print("CT:" + str(self.currentTemps) + ",L: " + str(len(self.a)))

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
            if (not self.isSimulation):
                self.hardwareController.moveSteamRegularizersDown()
            print("SteamRegularizers moved down")
        elif (self.steamRegularizers == 0):
            self.steamRegularizers = 1.0
            if (not self.isSimulation):
                self.hardwareController.moveSteamRegularizersUp()
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
        if (not self.isSimulation):
            self.hardwareController.turnFanOn()
        print("Fan: 100%")

    def stopFan(self):
        if(self.fan == 0.0):
            print("Fan is already stopped")
            return

        self.fan = 0.0
        if (not self.isSimulation):
            self.hardwareController.turnFanOff()
        print("Fan: 0%")

    def get_FanValue(self):
        return self.fan

    def get_Drosselklappe(self):
        return self.drosselklappe

    def set_Drosselklappe(self, value):
        self.drosselklappe = value
        if (not self.isSimulation):
            self.hardwareController.moveDrosselklappeStepper(self.drosselklappe)
        print("Drosselklappe: " + str(int(value * 100)) + "%")

    def get_FastHeatupValue(self):
        return self.isFastHeatUpActive

    def fastHeatUp(self):
        self.set_Drosselklappe(1.0)
        self.activateFan()
        self.isFastHeatUpActive = True
        print("Fast heat up mode active")

   # def fastHeatUp(self, temp):
    #    self.set_Drosselklappe(1.0)
     #   self.activateFan()
      #  self.isFastHeatUpActive = False
       # print("Fast heat up mode active; With max temp value: " + str(int(temp)))

    def stopfastHeatUp(self):
        self.set_Drosselklappe(0.5)
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
        if(self.tempAnalyzer.get_AutonomousModeState()):
            self.tempAnalyzer.deactivateAutonomousMode()

    def autoModeAction(self):
        if(self.tempAnalyzer.get_AutonomousModeState()):
            self.set_autoModeOff()
        else:
            self.set_autoModeOn()


    def onShutdown(self):
        print("Shutdown initialized...")
        self.isOnline = False
        self.set_autoModeOff()
        self.set_Drosselklappe(0.0)
        self.stopFan()
        self.isFastHeatUpActive = False
        #TODO call all shutdown funtions
        self.t1.join()

    def restoreLastValues(self, dict):
        print("Restore last values")
        self.ofenID = dict["ofenId"]
        self.drosselklappe = dict["drosselklappe"]
        self.fan = dict["fan"]
        self.steamRegularizers = dict["steamRegularizers"]
        self.temp2hold = dict["temp2hold"]
        self.currentTemp = dict["temp1"]
        self.currentTemps = [dict["temp1"], dict["temp2"], dict["temp3"], dict["temp4"], dict["temp5"], dict["temp6"], dict["temp7"]]
        self.isFastHeatUpActive = dict["fastHeatupActive"]


    def printHalloOfen(self):
        print("hallo Ooen: " + str(threading.get_ident()))

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
