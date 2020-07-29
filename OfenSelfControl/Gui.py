#import webview

#webview.create_window('Hello world', 'https://pywebview.flowrl.com/')
#webview.create_window('OfenWatch', 'http://localhost/controlfrog/layouts/b/layout-8.html')
#webview.start()

import eel

class Gui(object):

    def __init__(self, ofen):
        print("Init Gui")

        self.ofen = ofen

        eel.init('web')
        #my_options = {
        #    'mode': "chrome",  # or "chrome-app",
        #    'host': 'localhost',
        #    'port': 8080,
        #    'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
        #}
        eel.start('controlfrog/layouts/b/layout-8.html')

    # call the javascript function update the view
    def updateView(self):
        i = 0

    def checkForAlert(self):
        alerts = self.ofen.get_alertCodes

    def showFailureOverlay(self):


