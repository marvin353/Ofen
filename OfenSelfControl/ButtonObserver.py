from Ofen import Ofen
import pigpio
import time
import threading
import RPi.GPIO as GPIO
import time

class ButtonObserver(object):

    def __init__(self,ofenMain, ofen):
        print("Init ButtonObserver")
        self.ofenMain = ofenMain
        self.ofen = ofen

        #Buttons
        self.pin_btn_red = 0
        self.pin_btn_green = 0
        self.pin_btn_white_1 = 0
        self.pin_btn_white_2 = 0

        self.pi = pigpio.pi()
        self.pi.set_pull_up_down(self.pin_btn_red, pigpio.PUD_UP)

        #DIGs
        self.pin1_dig1 = 2
        self.pin2_dig1 = 3
        self.old_a_dig1 = 1
        self.old_b_dig1 = 1

        self.pin1_dig2 = 0
        self.pin2_dig2 = 0
        self.old_a_dig2 = 1
        self.old_b_dig2 = 1

        GPIO.setup(self.pin1_dig1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin2_dig1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.pin1_dig2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin2_dig2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.locks = [0,0,0,0,0,0] #red,      green , white1,   white2, dig1,      dig2
#                                  #shutdown, SRZs,   Autopilot, ka   , temp2hold, drosselklappe(/luft)

        self.shutdownRequest = False

        # Start thrads
        t1 = threading.Thread(target=self.buttonEvent, args=())
        t1.start()

    def buttonEvent(self):
        while (True):
            if (self.pi.read(self.pin_btn_red) == 1):
                self.buttonpressed_shutdown()
                time.sleep(0.1)
                self.ofenMain.interruptAction()
            if (self.pi.read(self.pin_btn_green) == 1):
                self.buttonpressed_steamRegularizers()
                time.sleep(0.1)
                self.ofenMain.interruptAction()
            if (self.pi.read(self.pin_btn_white_1) == 1):
                self.buttonpressed_autoMode()
                time.sleep(0.1)
                self.ofenMain.interruptAction()
            if (self.pi.read(self.pin_btn_white_2) == 1):
                self.pi.write(14, 0)
                time.sleep(0.1)
                self.ofenMain.interruptAction()

            change = get_encoder_DIG1()
            if change != 0:
                x = x + change * 5
                if (x <= 0):
                    x = 0
                print(x)
                self.DIGTurned_temp2hold(change)
                change = 0

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
            self.unlockIt(0, 2)

    def buttonpressed_steamRegularizers(self):
        if (self.lockIt(1)):
            print("Button pressed: SteamRegulaerizers")
            self.ofen.moveSteamRegularizers()
            self.unlockIt(1, 2)

    def buttonpressed_autoMode(self):
        if (self.lockIt(2)):
            print("Button pressed: Auto Mode")
            self.ofen.autoModeAction()
            self.unlockIt(2, 2)

    def DIG1Turned_temp2hold(self, change):
        newVal = self.ofen.get_temp2hold() + change * 5
        if (newVal <= 0):
            newVal = 0
        self.ofen.set_temp2hold(newVal)
        self.ofenMain.interruptActionDIG()
        print("DIG Turned: temp2Hold, With Value:" + newVal)

    def DIGTurned_drosselklappe(self, change):
        newVal = self.ofen.get_Drosselklappe() + change * 5
        if (newVal <= 0):
            newVal = 0
        self.ofen.set_Drosselklappe(newVal)
        self.ofenMain.interruptActionDIG()
        print("DIG Turned: Drosselklappe, With Value:" + newVal)

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


"""


=====================



# GPIO-Bezeichnung BCM stezen
GPIO.setmode(GPIO.BCM)

# GPIO-Pins Encoder (gemeinsamer Encoder-Pin auf GND)
in_a = 2
in_b = 3

# Merker fuer Encoder-Zustand (global)
old_a = 1
old_b = 1

# Pullup-Widerstand einschalten
GPIO.setup(in_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(in_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_encoder_DIG1():
  # liest den Encoder aus. Falls die Werte der Eingangspins
  # alten Wert abweichen, Richtung detektieren.
  # Rueckgabewert: -1, 0, +1
  global old_a, old_b
  result = 0

  # GPIO-Pins einlesen
  new_a = GPIO.input(in_a)
  new_b = GPIO.input(in_b)

  # Falls sich etwas geaendert hat, Richtung feststellen
  if (new_a != old_a or new_b != old_b):
    if (old_a == 0 and new_a == 1):
      result = (old_b * 2 - 1)
    elif (old_b == 0 and new_b == 1):
      result = -(old_a * 2 - 1)
  old_a = new_a
  old_b = new_b
  # entprellen
  #time.sleep(0.01)
  if (result != 0):
    print (result)
  return result

# Testprogramm
x = 0
while True:
  change = get_encoder_A()
  if change != 0:
    x = x + change * 5
    if (x <= 0):
      x = 0
    print(x)
    change = 0
  time.sleep(0.001)


"""