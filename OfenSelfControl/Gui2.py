import eel
import os
import sys
from Ofen import Ofen


class Gui2(object):

    def __init__(self, ofen):
        print("Init Gui")
        self.ofen = ofen

    def startGUI(self, ofenMain):
        print("Start GUI (EEL) with PID:" + str(os.getpid()))
        eel.init('web')

        #eel.start('controlfrog/layouts/b/layout-8.html', mode="Chrome")
        eel.start('ofen.html', mode="Chrome")


    def updateView(self, data):
        print("GUI UpdateView")
        eel.loadData_Interrupt(str(data))

    def updateView_Settings(self):
        drosselklappe = str(self.ofen.get_Drosselklappe() * 100) + "%"
        if(self.ofen.get_FastHeatupValue() == 1):
            fastheatup = "AN"
        else:
            fastheatup = "AUS"
        if(self.ofen.get_autoMode() == 1):
            automode = "AN"
        else:
            automode = "AUS"
        temp2hold = str(self.ofen.get_temp2hold()) + "°C"
        air = str(self.ofen.get_airInput() * 100) + "%"
        errors = "Keine"
        fan = str(self.ofen.get_FanValue() * 100) + "%"

        eel.loadData_Interrupt_Settings(drosselklappe, air, automode, fastheatup, temp2hold, fan ,errors)

    def onShutdown(self):
        print("Shutdown gui")
        #eel._shutdown
        #sys.exit("Exit Gui")


#@eel.expose                         # Expose this function to Javascript
#def say_hello_py(x):
 #   print('Hello from %s' % x)


# Call the javascript function update the view
"""def updateView(data):
    print("GUI UpdateView")
    #eel.loadData_Interrupt(data)
    test()
    
#def checkForAlert():
 #   alerts = self.ofen.get_alertCodes

def showFailureOverlay(self):
    print("show failure overlay")

def showShutdownOverlay(self):
    print("show shutdown overlay")



"""

