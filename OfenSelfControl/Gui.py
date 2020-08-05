import eel
from datetime import datetime

class Gui(object):

    def __init__(self):
        print("Init Gui")

        #self.ofen = ofen

        now = datetime.now()
        text_file = open("/home/pi/Desktop/OfenAlt/TEXT.txt", "w")
        n = text_file.write(str(now))
        text_file.close()
        
        my_options = {
          'mode': "chromium", #or "chrome-app",
          'host': 'localhost',
          'port': 8000,
          'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
        }
        
        eel.init('web')
        eel.start('controlfrog/layouts/b/layout-8.html', options=my_options, suppress_error = True)


    # call the javascript function update the view
    def updateView(self):
        i = 0

   # def checkForAlert(self):
        #alerts = self.ofen.get_alertCodes

    #def showFailureOverlay(self):
		


gui = Gui()

