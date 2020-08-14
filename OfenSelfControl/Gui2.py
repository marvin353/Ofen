#import webview

#webview.create_window('Hello world', 'https://pywebview.flowrl.com/')
#webview.create_window('OfenWatch', 'http://localhost/controlfrog/layouts/b/layout-8.html')
#webview.start()

import eel
import os

class Gui2(object):

    def __init__(self):
        print("Init Gui")

    def startGUI(self, ofenMain):
        print("Start GUI (EEL) with PID:" + str(os.getpid()))
        eel.init('web')

        eel.start('controlfrog/layouts/b/layout-8.html', mode="Chrome")

        #eel.start('controlfrog/layouts/b/eeltestmain.html', mode="Chrome")
        #eel.start('main.html', mode="Chrome")  # Start

    #def test(self):
     #   print("GUI Test with PID:" + str(os.getpid()))
      #  eel.say_hello_js("Python World! P calls J")

    def updateView(self, data):
        print("GUI UpdateView")
        eel.loadData_Interrupt(str(data))#"HALLO PARKUHR")
        #eel.say_hello_js("Python World! P calls J")

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

