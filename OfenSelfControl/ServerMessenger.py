from OfenTempAnalyzer import OfenTempAnalyzer
#from BTObserver import BTObserver
import threading
import time
import numpy as np

class ServerMessenger:

    a = [[0,0,0,0,0,0,0]]
    link_API = "http://..."
    link_Dashboard = "http://..."


    def __init__(self, ofen):
        self.ofen = ofen


    def uploadData(self):
        print("Uploading new data...")

    def sendOfflineSignal(self):
        print("Uploading new data...")

    def sendOnlineSignal(self):
        print("Uploading new data...")
