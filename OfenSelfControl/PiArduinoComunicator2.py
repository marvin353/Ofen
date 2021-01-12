import serial
import RPi.GPIO as GPIO
import time
import re
#from Ofen import Ofen
import threading
#from HardwareController import HardwareController

class PiArduinoCommunicator2:

    def __init__(self):
        print("PiArduinoCommunicator2 initialized")

        #self.ofen = ofen

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
        
    def decideTempOrSettings(self,stri): 
        try:
            striL = str(stri)
            striL = striL[2:]
            striL = striL[:-5]
            striL = striL.replace(" ","")
            
            if "D" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                print("D")
                print(value)
            elif "G" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                print("G")
                print(value)
            elif "L" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                print("L")
                print(value)
            elif "A" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                print("A")
                print(value)
            elif "F" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                print("F")
                print(value)
            elif "H" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                print("H")
                print(value)
            elif "T:" in striL:
                strParts = re.split(":",striL)
                #print(strParts[1])
                self.processTempString(strParts[1])
            else:
                msg = "TempSet-StringParsingError:NO MATCH Please check serial connection"
                print(msg)
                self.error["error"] = True
                self.error["message"] = msg
        
        except Exception as e:
            msg = "TempSet-StringParsingException: Please check serial connection"
            print(msg)
            print(e)
            self.error["error"] = True
            self.error["message"] = msg
            
    #def processSettingsString(self, stri):
      #  strParts = re.split("-",striL)
      #  value = float(strParts[1])
       #         print("F")
       #         print(value)

    def processTempString(self,stri):
        error = 0
        values = [0,0,0,0,0,0,0]

        #str = "NAN-NAN-NAN-NAN-NAN-NAN-NAN"

        print("Temperatures: " + str(stri))
        
        try:
            #stri = str(stri)
            #print("REgexed1: " + stri)
            #stri = re.sub("b'", "", stri)
            #print("REgexed2: " + stri)
            #stri = re.sub("\\r\\n'", "", stri)
            
            #stri = stri[2:]
            #stri = stri[:-5]
            #stri = stri.replace(" ","")
            #print("REgexed3: " + stri)

            strParts = re.split("-",stri)
            #for strPart in strParts:
                #print(strPart)

            for idx, strPart in enumerate(strParts):
                    try:
                        #print(tempParts[1])
                        if(strPart.lower() == "nan"):
                            msg = "TemperatureStringParsingException NO DIGIT (NAN): Please check serial connection and temperature sensors "
                            print(msg)
                            self.error["error"] = True
                            self.error["message"] = msg
                            values[idx] = 0
                        else:
                            a = float(strPart)
                            #print(int(a))
                            values[idx] = int(a)
                            self.error = {"error":False, "message":"none"}
                    except:
                        msg = "TemperatureStringParsingException INT CAST: Please check serial connection and temperature sensors "
                        print(msg + strPart)
                        self.error["error"] = True
                        self.error["message"] = msg
        except Exception as e:
            msg = "TemperatureStringParsingException: Please check serial connection and temperature sensors "
            print(msg)
            self.error["error"] = True
            self.error["message"] = msg

        self.values = values

    def readFromSerialLoop(self):
        while True:
            read_ser=self.ser.readline()
            #print(read_ser)
            self.decideTempOrSettings(read_ser)

    def onShutdown(self):
        self.t1.join()
        
main = PiArduinoCommunicator2()
