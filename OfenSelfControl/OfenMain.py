from Ofen import Ofen
from Gui2 import Gui2
#from OfenTempAnalyzer import OfenTempAnalyzer
import numpy as np
import time
import threading
from ServerMessenger import ServerMessenger
from LocalDataStorage import LocalDataStorage
import sys
import os
from ButtonObserver import ButtonObserver


class OfenMainn(object):


    def __init__(self):

        self.isSimulation = False

        print("Init")
        print("main T:" + str(threading.get_ident()))


        self.ofen = Ofen(1, self.isSimulation)
        self.ofen.set_temp2hold(300)

        self.gui = Gui2(self.ofen)
        self.serverMessenger = ServerMessenger(self.ofen) #TODO: Catch http execption if no connection to inet and turn to local monly mode
        self.localDataStorage = LocalDataStorage(self.ofen)

        if (not self.isSimulation):
            self.buttonObserver = ButtonObserver(self, self.ofen)

        self.isLoggedIn = False
        self.isLoggedIn = self.serverMessenger.logIn()

        #Start thrads
        print("Start Thread for DB and GUI")
        self.t0 = threading.Thread(target=self.makeGUIThread, args=())
        self.t0.start()

        self.t1 = threading.Thread(target=self.refreshGUI, args=())
        self.t1.start()

        self.t2 = threading.Thread(target=self.storeAndUploadData, args=())
        self.t2.start()



    def makeGUIThread(self):
       self.gui.startGUI(self)

    def refreshGUI(self):
        while(self.ofen.isOnline):
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
        while(self.ofen.isOnline):
            self.localDataStorage.appendData()
            data = self.localDataStorage.getDataAsJson()
            self.serverMessenger.uploadData()
            time.sleep(5)

    def interruptAction(self):
        self.localDataStorage.appendData()
        #Gui2.updateView(self.getData())
        self.gui.updateView_Settings()
        self.serverMessenger.uploadData()

    def interruptAction_DIG(self):
        #self.localDataStorage.appendData()
        self.gui.updateView_Settings()
        #self.serverMessenger.uploadData()

    def onLaunch(self):
        print("Launching")
        self.serverMessenger.sendOnlineSignal()

    def onShutdown(self):
        self.gui.onShutdown()
        self.ofen.onShutdown()
        self.localDataStorage.onShutdown()
        self.serverMessenger.sendOfflineSignal()
        print("end reached1")

    def onShutdown_test(self):
        print("Main Schutdown...")
        self.onShutdown()
        #self.t0.join()
        self.t1.join()
        self.t2.join()
        print("end reached2")
        sys.exit("Exit programm finally")
        os.system("shutdown now -h")





if __name__ == '__main__':

    finished = False

    try:
        print("Starting with main...")
    #ofen = Ofen(1)
    #ofen.set_temp2hold(400)

        main = OfenMainn()
        while(not finished):
            print("main loop")
            if (finished):
                sys.exit()
            time.sleep(10)
    except:
        print("Perform Shutdown")
        finished = True

        main.onShutdown_test()
        #raise KeyboardInterrupt
