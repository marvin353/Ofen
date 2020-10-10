import serial
import RPi.GPIO as GPIO
import time
import re
#from Ofen import Ofen
import threading
#from HardwareController import HardwareController

class PiArduinoCommunicator:

    def __init__(self, ofen):
        print("PiArduinoCommunicator initialized")

        #self.controller = controller
        self.ofen = ofen

        self.ser = serial.Serial("/dev/ttyACM0", 9600)  # change ACM number as found from ls /dev/tty/ACM*
        self.ser.baudrate = 9600

        self.values = [0, 0, 0, 0, 0, 0, 0]
        self.error = {"error":False, "message":"none"}

        self.t1 = threading.Thread(target=self.readFromSerialLoop, args=())
        self.t1.start()

    def get_error(self):
        return self.error

    def get_values(self):
        return self.values

    def processTempString(self,stri):
        error = 0
        values = [0,0,0,0,0,0,0]

        #str = "Temp1: NAN-Temp2: NAN-Temp3: NAN-Temp4: NAN-Temp5: NAN-Temp6: NAN-Temp7: NAN"

        print("REgexed0: " + str(stri))
        
        try:
            stri = str(stri)
            #print("REgexed1: " + stri)
            #stri = re.sub("b'", "", stri)
            #print("REgexed2: " + stri)
            #stri = re.sub("\\r\\n'", "", stri)
            stri = stri[2:]
            stri = stri[:-5]
            print("REgexed3: " + stri)

            strParts = re.split("-",stri)
            #for strPart in strParts:
                #print(strPart)

            for idx, strPart in enumerate(strParts):
                tempParts = re.split(":",strPart)
                if True:#tempParts[1].isdigit():
                    try:
                        #print(tempParts[1])
                        if(tempParts[1].lower() == "nan"):
                            msg = "TemperatureStringParsingException NO DIGIT (NAN): Please check serial connection and temperature sensors "
                            print(msg)
                            self.error["error"] = True
                            self.error["message"] = msg
                            values[idx] = 0
                        else:
                            a = float(tempParts[1])
                            print(int(a))
                            values[idx] = int(a)
                            self.error = {"error":False, "message":"none"}
                    except:
                        msg = "TemperatureStringParsingException INT CAST: Please check serial connection and temperature sensors "
                        print(msg)
                        self.error["error"] = True
                        self.error["message"] = msg
                else:
                    msg ="TemperatureStringParsingException NO DIGIT: Please check serial connection and temperature sensors "
                    print(msg)
                    self.error["error"] = True
                    self.error["message"] = msg
        except:
            msg = "TemperatureStringParsingException: Please check serial connection and temperature sensors "
            print(msg)
            self.error["error"] = True
            self.error["message"] = msg

        self.values = values

    def readFromSerialLoop(self):
        while self.ofen.isOnline:
            read_ser=self.ser.readline()
            print(read_ser)
            self.processTempString(read_ser)

    def onShutdown(self):
        self.t1.join()
