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

	def processTempString(self,str):
		error = 0
		values = [0,0,0,0,0,0,0]

		#str = "Temp1: NAN-Temp2: NAN-Temp3: NAN-Temp4: NAN-Temp5: NAN-Temp6: NAN-Temp7: NAN"

		try:
			strParts = re.split("-",str)
			#for strPart in strParts:
				#print(strPart)

			for idx, strPart in enumerate(strParts):
				tempParts = re.split(":",strPart)
				if tempParts[1].isdigit():
					try:
						values[idx] = int(tempParts[1])
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

