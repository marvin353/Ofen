#from Ofen import Ofen
import pigpio
import time
import threading
import RPi.GPIO as GPIO
import time

class ButtonObserver(object):

    def __init__(self):
        print("Init ButtonObserver")
        #self.ofen = ofen

        self.pin_btn_red = 23
        self.pin_btn_green = 10
        self.pin_btn_white_1 = 9
        self.pin_btn_white_2 = 25

        self.pin_dig1_1 = 2
        self.pin_dig1_2 = 3

        self.pin_dig2_1 = 14
        self.pin_dig2_2 = 15

        self.pi = pigpio.pi()
        self.pi.set_pull_up_down(self.pin_btn_red, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.pin_btn_green, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.pin_btn_white_1, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.pin_btn_white_2, pigpio.PUD_UP)

        self.locks = [0,0,0,0,0,0] #red,      green , white1,   white2, dig1,      dig2
#                                  #shutdown, SRZs,   Autopilot, ka   , temp2hold, drosselklappe(/luft)

        self.shutdownRequest = False

        # Start thrads
        t1 = threading.Thread(target=self.buttonEvent, args=())
        t1.start()

    def buttonEvent(self):
        while (True):
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
                self.buttonpressed_w2()
                time.sleep(0.1)
            time.sleep(0.1)

    def lockIt(self, idx):
        if (self.locks[idx] == 0):
            self.locks[idx] = 1
            return True
        return False

    def unlockIt(self, idx, waitingTime):
        #time.sleep(waitingTime)
        time.sleep(1.001)
        if (self.locks[idx] == 1):
            self.locks[idx] = 0
            return True
        return False


    def buttonpressed_shutdown(self):
        if (self.lockIt(0)):
            print("Button pressed: Shutdown")
            self.shutdownRequest = True
            self.unlockIt(0,2)

    def buttonpressed_steamRegularizers(self):
        if (self.lockIt(1)):
            print("Button pressed: SteamRegulaerizers")
            #self.ofen.moveSteamRegularizers()
            self.unlockIt(1,2)

    def buttonpressed_autoMode(self):
        if (self.lockIt(2)):
            print("Button pressed: Auto Mode")
            #self.ofen.autoModeAction()
            self.unlockIt(2,2)
    
    def buttonpressed_w2(self):
        if (self.lockIt(3)):
            print("Button pressed: W2")
            #self.ofen.autoModeAction()
            self.unlockIt(3,2)

    def DIGTurnedR_temp2hold(self):
        print("DIG Turned Right: temp2Hold")

    def DIGTurnedL_temp2hold(self):
        print("DIG Turned Left: temp2Hold")

    def DIGTurnedR_drosselklappe(self):
        print("DIG Turned Right: Drosselklappe")

    def DIGTurnedL_drosselklappe(self):
        print("DIG Turned Left: Drosselklappe")

ButtonObserver = ButtonObserver()
while(True):
	time.sleep(10)

