from Ofen import Ofen
from Gui2 import Gui2
#from OfenTempAnalyzer import OfenTempAnalyzer
import numpy as np
import time
import threading
from ServerMessenger import ServerMessenger
from LocalDataStorage import LocalDataStorage
#from ButtonObserver import ButtonObserver


class OfenMainn(object):


    def __init__(self):

        self.isSimulation = True

        print("Init")
        print("main T:" + str(threading.get_ident()))

        #t2 = threading.Thread(target=self.job_1s2,args=())
        #t2.start()

        ofen = Ofen(1, self.isSimulation)
        ofen.set_temp2hold(300)

        self.gui = Gui2()
        self.serverMessenger = ServerMessenger(ofen)
        self.localDataStorage = LocalDataStorage(ofen)

        if (not self.isSimulation):
            self.buttonObserver = ButtonObserver(self, ofen)

        self.isLoggedIn = False
        self.isLoggedIn = self.serverMessenger.logIn()


        #Start thrads
        print("Start Thread for DB and GUI")
        t0 = threading.Thread(target=self.makeGUIThread, args=())
        t0.start()

        t1 = threading.Thread(target=self.refreshGUI, args=())
        t1.start()

        t2 = threading.Thread(target=self.storeAndUploadData, args=())
        t2.start()



    #def initializeOfen(self):

    def makeGUIThread(self):
       self.gui.startGUI(self)

    def refreshGUI(self):
        while(True):
            try:
                self.gui.updateView(self.getData())
                time.sleep(2)
            except Exception as e:
                print(e)
                time.sleep(2)

    def getData(self):
        self.localDataStorage.appendData()
        data = self.localDataStorage.getDataAsJson()
        return data

    def storeAndUploadData(self):
        while(True):
            self.localDataStorage.appendData()
            data = self.localDataStorage.getDataAsJson()
            #self.serverMessenger.uploadData(data)
            time.sleep(5)

    def interruptAction(self):
        self.localDataStorage.appendData()
        #Gui2.updateView(self.getData())
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