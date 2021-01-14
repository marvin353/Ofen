from OfenTempAnalyzer import OfenTempAnalyzer
#from BTObserver import BTObserver
import threading
import time
import numpy as np
from HardwareController import HardwareController
from PiArduinoComunicator2 import PiArduinoCommunicator2

class Ofen:

    a = [[0,0,0,0,0,0,0]]

    def __init__(self, ofenID, isSimulation):

        self.isSimulation = isSimulation

        self.isOnline = True

        self.ofenID = ofenID
        self.drosselklappe = 0.0
        self.airInput = 0.0
        self.fan = 0.0
        self.temp2hold = 0.0
        self.currentMainTemp = 0.0
        self.currentTemps = [0, 0, 0, 0, 0, 0, 0]
        self.isFastHeatUpActive = False
        self.alertCodes= {"lesswood":False, "sensorerror":False, "programfail":False}
        
        if(not self.isSimulation):
            self.hardwareController = HardwareController(self)
            self.arduinoComm = PiArduinoCommunicator2(self)
        else:
            self.t1 = threading.Thread(target=self.collectDataSimulation, args=())
            self.t1.start()

        self.tempAnalyzer = OfenTempAnalyzer(self)
        #self.tempAnalyzer.activateAutonomousMode()



    def setTempData(self, x):

        print("X:" + str(x) + ",L: " + str(len(self.a)))

        self.currentTemps[0] = x[0]
        self.currentTemps[1] = x[1]
        self.currentTemps[2] = x[2]
        self.currentTemps[3] = x[3]
        self.currentTemps[4] = x[4]
        self.currentTemps[5] = x[5]
        self.currentTemps[6] = x[6]

        if (len(self.a) > 59):
            self.a = self.a[1:60]
            self.a.append(x)
        else:
            self.a.append(x)

        self.currentMainTemp = x[0]


    def fanAction(self):
        if(self.fan == 0.0):
            self.fan = 1.0
            if (not self.isSimulation):
                self.hardwareController.turnFanOn()
            print("Fan: 100%")
        else:
            self.fan = 0.0
            if (not self.isSimulation):
                self.hardwareController.turnFanOff()
            print("Fan: 0%")

    def get_FanValue(self):
        return self.fan

    def set_Drosselklappe(self, value):
        self.drosselklappe = value
        if (not self.isSimulation):
            self.hardwareController.moveDrosselklappeStepper(self.drosselklappe)
        print("Drosselklappe: " + str(int(value * 100)) + "%")

    def get_Drosselklappe(self):
        return self.drosselklappe

    def set_airInput(self, value):
        self.airInput = value
        if (not self.isSimulation):
            self.hardwareController.moveAirInputStepper(self.airInput)
        print("AirInput: " + str(int(value * 100)) + "%")

    def get_airInput(self):
        return self.airInput

    def fastHeatUpAction(self):
        if (self.isFastHeatUpActive == 0.0):
            self.set_Drosselklappe(1.0)
            self.activateFan()
            self.isFastHeatUpActive = 1.0
            print("Fast heat up mode active")
        else:
            self.set_Drosselklappe(0.5)
            self.stopFan()
            self.isFastHeatUpActive = 0.0
            print("Fast heat up mode stopped")

    def get_FastHeatupValue(self):
        return self.isFastHeatUpActive

    def autoModeAction(self):
        if(self.tempAnalyzer.get_AutonomousModeState()):
            self.tempAnalyzer.deactivateAutonomousMode()
        else:
            self.tempAnalyzer.activateAutonomousMode()

    def get_autoMode(self):
        return self.tempAnalyzer.get_AutonomousModeState()

    def set_temp2hold(self, a):
        self.temp2hold = a
        print("Set temp2hold")

    def get_temp2hold(self):
        return self.temp2hold

    def get_a(self):
        return np.array(self.a)

    def get_a_n_last_values(self, length):
        ind_start = len(self.a) - length
        b = np.array(self.a[ind_start:])
        return np.array(b)

    def get_currentMainTemp(self):
        return self.currentMainTemp

    def get_currentTempsArray(self):
        return self.currentTemps

    def get_ofenid(self):
        return self.ofenID



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
        self.currentMainTemp = dict["temp1"]
        self.currentTemps = [dict["temp1"], dict["temp2"], dict["temp3"], dict["temp4"], dict["temp5"], dict["temp6"], dict["temp7"]]
        self.isFastHeatUpActive = dict["fastHeatupActive"]

    def triggerAlert(self, code, message):
        if code == "lessWood":
            # trigger push notification for adding new wood
            self.arduinoComm.write2Serial_woodWarning()
            print("time to add more wood")
            self.alertCodes["lesswood"] = False
        elif code == "sensor_error":
            self.arduinoComm.write2Serial_errorWarning()
            self.alertCodes["lesswood"] = False
            print("Error occured check Sensors")
        elif code == "read_serial_error":
            self.arduinoComm.write2Serial_errorWarning()
            self.alertCodes["lesswood"] = False
            print("Error occured check Sensors")

    def get_alertCodes(self):
        return self.alertCodes

    def printCurrentState(self):
        print("Fan: " + str(int(self.fan*100)) + "% ; Drosselklappe: " + str(int(self.drosselklappe*100)) + "% ; CurrentTemp: " + str(self.currentMainTemp) + "; SRZs: " + str(self.steamRegularizers))

################################################# Simulation ###############################################
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


    def collectDataSimulation(self):

        while self.isOnline:
            x = self.simulation()
            self.setTempData(x)
            time.sleep(0.5)