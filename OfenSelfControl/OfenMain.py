from Ofen import Ofen
from Gui import Gui
#from OfenTempAnalyzer import OfenTempAnalyzer
import numpy as np
import time
import threading
from ServerMessenger import ServerMessenger
from LocalDataStorage import LocalDataStorage
from ButtonObserver import ButtonObserver


class OfenMainn(object):

    def __init__(self):
        print("Init")
        print("main T:" + str(threading.get_ident()))

        #t2 = threading.Thread(target=self.job_1s2,args=())
        #t2.start()


        ofen = Ofen(1)
        ofen.set_temp2hold(400)

        self.gui = Gui(ofen)
        self.serverMessenger = ServerMessenger(ofen)
        self.localDataStorage = LocalDataStorage(ofen)

        self.buttonObserver = ButtonObserver(ofen)

        #Start thrads
        t1 = threading.Thread(target=self.refreshGUI, args=())
        t1.start()

        t1 = threading.Thread(target=self.storeAndUploadData, args=())
        t1.start()



    def refreshGUI(self):
        while(True):
            self.gui.updateView()
            time.sleep(2)

    def storeAndUploadData(self):
        while(True):
            self.localDataStorage.appendData()
            self.serverMessenger.uploadData()
            time.sleep(5)

    def interruptAction(self):
        self.gui.updateView()
        self.localDataStorage.appendData()
        self.serverMessenger.uploadData()

    def onLaunch(self):
        print("Launching")
        self.serverMessenger.sendOnlineSignal()

    def onShutdown(self):
        self.ofen.onShutdown()
        self.localDataStorage.onShutdown()
        self.serverMessenger.sendOfflineSignal()




#if __name__ == '__main__':
#m = OfenMainn()
#time.sleep(3)
#print("checkpoinz")
#time.sleep(3)
#print("by")

print("Starting with main...")
#ofen = Ofen(1)
#ofen.set_temp2hold(400)

main = OfenMainn()