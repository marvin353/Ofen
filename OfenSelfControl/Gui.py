import eel
from datetime import datetime
import sys

class Gui(object):

    def __init__(self, ofenMain ,ofen):
        print("Init Gui")

        self.ofenMain = ofenMain
        self.ofen = ofen


    def startGUI(self):
        print("Start GUI (EEL)")
        eel.init('web')
        # my_options = {
        #    'mode': "chrome",  # or "chrome-app",
        #    'host': 'localhost',
        #    'port': 8080,
        #    'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
        # }

       # eel.start('controlfrog/layouts/b/layout-8.html')
        eel.start('main.html', mode="Chrome")  # Start
        self.say_hello_py('Python World!local')
        eel.say_hello_js('Python World! P calls J')

    @eel.expose  # Expose this function to Javascript
    def say_hello_py(x):
        print('Hello from %s' % x)

    say_hello_py('Python World!local')
    eel.say_hello_js('Python World! P calls J')


    # call the javascript function update the view
    def updateView(self):
        i = 0
        print("GUI UpdateView")
        eel.loadData_Interrupt()

   # def checkForAlert(self):
        #alerts = self.ofen.get_alertCodes

    #def showFailureOverlay(self):

    def showFailureOverlay(self):
        print("show failure overlay")

    def showShutdownOverlay(self):
        print("show shutdown overlay")

    @eel.expose
    def getDataFromPython(self):
        print("Get Data from Python")
        return self.ofenMain.getData()

