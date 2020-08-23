#from Ofen import Ofen
from PiArduinoComunicator import PiArduinoCommunicator
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

class HardwareController:

    def __init__(self, ofen):
        print("HardwareController initialized")
        self.ofen = ofen

        self.arduinoComm = PiArduinoCommunicator(ofen)

        self.currentValue1 = 0.0
        self.currentStep1 = 0
        self.motor1running = False
        self.motor2running = False
       
        # Stepper
        try:
            self.Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
            self.Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
            self.Motor1.Stop()
            self.Motor2.Stop()
        except Exception as e:
            print(e)

        # Relais
        self.RELAIS_1_GPIO = 7
        GPIO.setup(self.RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen
        
        #Servo
        self.servoPIN = 5
        GPIO.setup(self.servoPIN, GPIO.OUT)
        self.p = GPIO.PWM(self.servoPIN, 50) # GPIO als PWM mit 50Hz
        self.p.start(2.5)
        self.SetAngle(self.p, 0)
        
        self.turnFanOff()

    def turnFanOn(self):
        print("Turn Relais ON: Activate Fan")
        GPIO.output(self.RELAIS_1_GPIO, GPIO.HIGH)

    def turnFanOff(self):
        print("Turn Relais OFF: Deactivate Fan")
        GPIO.output(self.RELAIS_1_GPIO, GPIO.LOW)


    def moveSteamRegularizersUp(self):
        print("Move Servo: SRZs up")
        #self.moveValueSRZs(self, self.Motor2, 1.0)
        self.SetAngle(self.p, 160)

    def moveSteamRegularizersDown(self):
        print("Move Servo: SRZs down")
        #self.moveValueSRZs(self, self.Motor2, 0.0)
        self.SetAngle(self.p, 0)
      
    def moveDrosselklappeStepper(self, value):
        print("Move Stepper: Drosselklappe")
        if (not self.motor1running):
            self.moveValueDrossel(self.Motor1, value)
        else:
            while (self.motor1running):
                print("Wait for Motor1 (Drosselklappe) to stop")
                time.sleep(1)
            self.moveDrosselklappe(value)

    def moveAirInputStepper(self, value):
        print("Move Stepper: Air Input")

    def readTempDataFromArduino(self):

       # temps = [-1000,-1000,-1000,-1000,-1000,-1000,-1000]

        error = self.arduinoComm.get_error()

        if(error["error"]):
            self.ofen.triggerAlert("sensor_error", error["message"])
            return [0,0,0,0,0,0,0]

        temps = self.arduinoComm.get_values()

        return temps






    def moveValueDrossel(self, motor, newValue):

        self.motor1running = True
        print("\nMotor move to value: " + str(newValue) + ", Current Value/Step: " + str(self.currentValue1) + " / " + str(
            self.currentStep1))

        motor.SetMicroStep('hardward', 'fullstep')
        motorDirection = 'forward'
        value2move = 0

        if (newValue > self.currentValue1):
            motorDirection = 'forward'
            value2move = int(1600 * newValue) - self.currentStep1
            self.currentStep1 = self.currentStep1 + value2move
        elif (newValue < self.currentValue1):
            motorDirection = 'backward'
            value2move = (int(1600 * newValue) - self.currentStep1) * (-1)
            self.currentStep1 = self.currentStep1 - value2move
        else:
            print("Keep Value (Drosselklappe)")

        self.currentValue1 = newValue
        motor.TurnStep(Dir=motorDirection, steps=value2move, stepdelay=0.001)
        motor.Stop()
        self.motor1running = False


    def moveValueSRZs(self, motor, newValue):

        self.motor2running = True
        print("\nMotor move to value: " + str(newValue) + ", Current Value/Step: " + str(self.currentValue2) + " / " + str(
            self.currentStep2))

        motor.SetMicroStep('hardward', 'fullstep')
        motorDirection = 'forward'
        value2move = 0

        if (newValue > self.currentValue2):
            motorDirection = 'forward'
            value2move = int(1600 * newValue) - self.currentStep2 #TODO set correct initial value
            self.currentStep2 = self.currentStep2 + value2move
        elif (newValue < self.currentValue2):
            motorDirection = 'backward'
            value2move = (int(1600 * newValue) - self.currentStep2) * (-1) #TODO set correct initial value
            self.currentStep2 = self.currentStep2 - value2move
        else:
            print("Keep Value (Drosselklappe)")

        self.currentValue2 = newValue
        motor.TurnStep(Dir=motorDirection, steps=value2move, stepdelay=0.001)
        motor.Stop()
        self.motor1running = False
        
        
    def SetAngle(self, p, angle):
        duty = angle / 18 + 2
        GPIO.output(self.servoPIN, True)
        p.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(self.servoPIN, False)
        p.ChangeDutyCycle(0)


