import serial
import re
import threading
from Ofen import Ofen

class PiArduinoCommunicator2:

    def __init__(self, ofen):
        print("PiArduinoCommunicator2 initialized")

        self.ofen = ofen

        self.ser = serial.Serial("/dev/ttyACM0", 9600)  # change ACM number as found from ls /dev/tty/ACM*
        self.ser.baudrate = 9600

        self.error = {"error":False, "message":"none"}

        self.t1 = threading.Thread(target=self.readFromSerialLoop, args=())
        self.t1.start()

    def get_error(self):
        return self.error

    def decideTempOrSettings(self,stri): 
        try:
            striL = str(stri)
            striL = striL[2:]
            striL = striL[:-5]
            striL = striL.replace(" ","")
            
            if "D" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                self.ofen.set_Drosselklappe(value)
                print("D")
                print(value)
            elif "G" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                if value >= 0.5:
                    value = 1.0
                else:
                    value = 0.0
                if not self.ofen.get_FanValue() == value:
                    self.ofen.fanAction()
                print("G")
                print(value)
            elif "L" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                self.ofen.set_airInput(value)
                print("L")
                print(value)
            elif "A" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                if not self.ofen.get_autoMode() == value:
                    self.ofen.autoModeAction()
                print("A")
                print(value)
            elif "F" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                if not self.ofen.get_FastHeatupValue() == value
                    self.ofen.fastHeatUpAction()
                print("F")
                print(value)
            elif "H" in striL:
                strParts = re.split("-",striL)
                value = round(float(strParts[-1]),1)
                self.ofen.set_temp2hold(value)
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


    def processTempString(self,stri):
        error = 0
        values = [0,0,0,0,0,0,0]

        #str = "NAN-NAN-NAN-NAN-NAN-NAN-NAN"

        print("Temperatures: " + str(stri))
        
        try:

            strParts = re.split("-",stri)

            for idx, strPart in enumerate(strParts):
                    try:
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
                        values[idx] = 0
        except Exception as e:
            msg = "TemperatureStringParsingException: Please check serial connection and temperature sensors "
            print(msg)
            self.error["error"] = True
            self.error["message"] = msg
            values = [0,0,0,0,0,0,0]

        self.ofen.setTempData(values)

    def readFromSerialLoop(self):
        while True:
            try:
                read_ser=self.ser.readline()
            #Read incomind Data from Serial, decode Bytes as UTF-8 String, cut \r\n (=trailing characters)
            #read_ser = self.ser.readline().decode('utf-8').rstrip()
                self.decideTempOrSettings(read_ser)
            except:
                print("Serial Connection ERROR")
                self.ofen.setTempData([0,0,0,0,0,0,0])

    def write2Serial_woodWarning(self):
        print("Write 2 Serial")
        self.ser.write("wood\n".encode('utf-8'))

    def write2Serial_errorWarning(self):
        print("Write 2 Serial")
        self.ser.write("error\n".encode('utf-8'))

    def onShutdown(self):
        self.t1.join()
        
#main = PiArduinoCommunicator2()
