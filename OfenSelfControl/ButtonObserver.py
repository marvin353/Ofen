#from Ofen import Ofen
import pigpio
import time
import threading
import RPi.GPIO as GPIO
import time

class ButtonObserver(object):

    def __init__(self,ofenMain, ofen):
    #def __init__(self):
        print("Init ButtonObserver")
        self.ofenMain = ofenMain
        self.ofen = ofen
        
        self.x1 = 0
        self.x2 = 0

        #Buttons
        GPIO.setmode(GPIO.BCM)
        self.pin_btn_red = 23
        self.pin_btn_green = 10
        self.pin_btn_white_1 = 9
        self.pin_btn_white_2 = 25

        self.pi = pigpio.pi()
        self.pi.set_pull_up_down(self.pin_btn_red, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.pin_btn_green, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.pin_btn_white_1, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.pin_btn_white_2, pigpio.PUD_UP)

        #DIGs
        self.pin1_dig1 = 2
        self.pin2_dig1 = 3
        self.old_a_dig1 = 1
        self.old_b_dig1 = 1

        self.pin1_dig2 = 14
        self.pin2_dig2 = 15
        self.old_a_dig2 = 1
        self.old_b_dig2 = 1

        GPIO.setup(self.pin1_dig1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin2_dig1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.pin1_dig2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin2_dig2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.locks = [0,0,0,0,0,0] #red,      green, white1,   white2, dig1,      dig2
#                                  #shutdown, SRZs,  Automode, fan,     luft, drosselklappe(/luft)

        self.shutdownRequest = False

        # Start thrads
        t1 = threading.Thread(target=self.buttonEvent, args=())
        t1.start()

    def buttonEvent(self):
        while (self.ofen.isOnline):
            if (self.pi.read(self.pin_btn_red) == 0):
                self.buttonpressed_shutdown()
                time.sleep(0.1)
            if (self.pi.read(self.pin_btn_green) == 0):
                self.buttonpressed_steamRegularizers()
                time.sleep(0.1)
            if (self.pi.read(self.pin_btn_white_1) == 0):
                self.buttonpressed_autoMode()
                time.sleep(0.1)
            if (self.pi.read(self.pin_btn_white_2) == 0):
                self.buttonpressed_fan()
                time.sleep(0.1)

            change = self.get_encoder_DIG1()
            if change != 0:
                self.DIGTurned_airInput(change)
                change = 0

            change2 = self.get_encoder_DIG2()
            if change2 != 0:
                self.DIGTurned_drosselklappe(change2)
                change2 = 0

            time.sleep(0.01)

    def lockIt(self, idx):
        if (self.locks[idx] == 0):
            self.locks[idx] = 1
            return True
        return False

    def unlockIt(self, idx, waitingTime):
        time.sleep(waitingTime)
        if (self.locks[idx] == 1):
            self.locks[idx] = 0
            return True
        return False


    def buttonpressed_shutdown(self):
        if (self.lockIt(0)):
            print("Button pressed: Shutdown")
            self.shutdownRequest = True
            self.ofenMain.onShutdown()
            self.ofenMain.interruptAction()
            self.unlockIt(0, 5)

    def buttonpressed_steamRegularizers(self):
        if (self.lockIt(1)):
            print("Button pressed: SteamRegulaerizers")
            #self.ofen.moveSteamRegularizers()
            self.ofenMain.interruptAction()
            self.unlockIt(1, 1)

    def buttonpressed_autoMode(self):
        if (self.lockIt(2)):
            print("Button pressed: Auto Mode")
            self.ofen.autoModeAction()
            self.ofenMain.interruptAction()
            self.unlockIt(2, 1)

    def buttonpressed_fan(self):
        if (self.lockIt(3)):
            print("Button pressed: Fan")
            self.ofen.fanAction()
            self.ofenMain.interruptAction()
            self.unlockIt(3, 1)

    def DIGTurned_airInput(self, change):
        #newVal = self.x1 + change * 5
        newVal = self.ofen.get_airInput() + change * 0.1
        #newVal = round(newVal, 2)
        if (newVal <= 0):
            newVal = 0
        if (newVal > 1):
            newVal = 1
        self.ofen.set_airInput(newVal)
        self.ofenMain.interruptAction_DIG()
        #self.x1 = newVal
        print("DIG Turned: airInput, With Value:" + str(newVal))

    def DIGTurned_drosselklappe(self, change):
        #newVal = self.x2 + change * 0.02
        newVal = self.ofen.get_Drosselklappe() + change * 0.02
        newVal = round(newVal, 2)
        if (newVal <= 0):
            newVal = 0

        self.ofen.set_Drosselklappe(newVal)
        self.ofenMain.interruptAction_DIG()
        #self.x2 = newVal
        print("DIG Turned: Drosselklappe, With Value:" + str(newVal))

    def get_encoder_DIG1(self):
        # liest den Encoder aus. Falls die Werte der Eingangspins
        # alten Wert abweichen, Richtung detektieren.
        # Rueckgabewert: -1, 0, +1
        result = 0

        # GPIO-Pins einlesen
        new_a = GPIO.input(self.pin1_dig1)
        new_b = GPIO.input(self.pin2_dig1)

        # Falls sich etwas geaendert hat, Richtung feststellen
        if (new_a != self.old_a_dig1 or new_b != self.old_b_dig1):
            if (self.old_a_dig1 == 0 and new_a == 1):
                result = (self.old_b_dig1 * 2 - 1)
            elif (self.old_b_dig1 == 0 and new_b == 1):
                result = -(self.old_a_dig1 * 2 - 1)
        self.old_a_dig1 = new_a
        self.old_b_dig1 = new_b
        # entprellen
        # time.sleep(0.01)
        if (result != 0):
            print(result)
        return result

    def get_encoder_DIG2(self):
        # liest den Encoder aus. Falls die Werte der Eingangspins
        # alten Wert abweichen, Richtung detektieren.
        # Rueckgabewert: -1, 0, +1
        result = 0

        # GPIO-Pins einlesen
        new_a = GPIO.input(self.pin1_dig2)
        new_b = GPIO.input(self.pin2_dig2)

        # Falls sich etwas geaendert hat, Richtung feststellen
        if (new_a != self.old_a_dig2 or new_b != self.old_b_dig2):
            if (self.old_a_dig2 == 0 and new_a == 1):
                result = (self.old_b_dig2 * 2 - 1)
            elif (self.old_b_dig2 == 0 and new_b == 1):
                result = -(self.old_a_dig2 * 2 - 1)
        self.old_a_dig2 = new_a
        self.old_b_dig2 = new_b
        # entprellen
        # time.sleep(0.01)
        if (result != 0):
            print(result)
        return result
        
#b = ButtonObserver()
#while(True):
#    time.sleep(10)

