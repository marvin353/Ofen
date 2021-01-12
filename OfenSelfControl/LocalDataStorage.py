import sqlite3
from datetime import datetime
import json
#from Ofen import Ofen

class LocalDataStorage(object):



    def __init__(self, ofen):
        print("Init LocalDataStorage")
        self.ofen = ofen
        #self.conn = sqlite3.connect('OfenLocalDB2.db')
        #self.connect2db()

        self.cleanDb()

    def connect2db(self):
        conn = sqlite3.connect('OfenLocalDB2.db')
        conn.row_factory = self.dict_factory
        return conn

    def disconnectFromDb(self, conn):
        conn.close()

    def cleanDb(self):

        conn = self.connect2db()
        c = conn.cursor()

        c.execute("DELETE From Records")
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    def getDataAsJson(self):
        print("getDataAsJson")
        conn = self.connect2db()
        cursor = conn.cursor()

        cursor.execute("SELECT * From Records")

        results = cursor.fetchall()
        conn.close()
        #print(json.dumps(results))
        return json.dumps(results)

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def appendData(self):
        ofenid = self.ofen.get_ofenid()
        temps = self.ofen.get_currentTempsArray()
        drosselklappe = self.ofen.get_Drosselklappe()
        steamRegularizers = self.ofen.get_steamRegularizersValue()
        fan = self.ofen.get_FanValue()
        fastHeatup = self.ofen.get_FastHeatupValue()
        temp2hold = self.ofen.get_temp2hold()
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y, %H:%M:%S")
        automode = self.ofen.get_autoMode()
        predictedTemps = [0,0,0]

        #ofenid = self.ofen.get_ofenid()
        #temps = [11,12,13,14,15,16,17]
        #drosselklappe = 0.1
        #fan = 0.2
        #fastHeatup = self.ofen.get_FastHeatupValue()
        #temp2hold = self.ofen.get_temp2hold()
        #now = datetime.now()
        #date_time = now.strftime("%d-%m-%Y, %H:%M:%S")

        conn = self.connect2db()
        c = conn.cursor()

        #print("CTLocalDB:" + str(temps))

        # Insert a row of data
       # c.execute("INSERT INTO Records VALUES (NULL, ofenid, temps[0], temps[1], temps[2], temps[3], temps[4], temps[5], temps[6], temp2hold, drosselklappe, fan, steamRegularizers, fastHeatup, date_time)")

        sqlite_insert_with_param = """INSERT INTO Records
                                  (id, ofenid, temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10, temp2hold, drosselklappe, fan, steamRegularizers, fastHeatupActive, automode, timestamp) 
                                  VALUES (NULL , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        data_tuple = (ofenid, int(temps[0]), int(temps[1]), int(temps[2]), int(temps[3]), int(temps[4]), int(temps[5]), int(temps[6]), int(predictedTemps[0]), int(predictedTemps[1]), int(predictedTemps[2]),temp2hold, drosselklappe, fan, steamRegularizers, fastHeatup, automode, date_time)
        c.execute(sqlite_insert_with_param, data_tuple)

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    def onShutdown(self):
        print("Clean local DB...")
        self.cleanDb()
        #self.disconnectFromDb()

    def getLastEntry(self):
        conn = self.connect2db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Records ORDER BY id DESC LIMIT 1")

        results = cursor.fetchall()

        #print(results)

        conn.close()
        return results
"""
class Ofen:

    a = [[0,0,0,0,0,0,0]]

    def __init__(self):
        self.ofenID = 1
        self.drosselklappe = 0.1
        self.fan = 0.2
        self.steamRegularizers = 0.3
        self.temp2hold = 218.0
        self.currentTemp = 111.0
        self.currentTemps = [100, 200, 300, 400, 500, 600, 700]
        self.isFastHeatUpActive = False
        self.autoM = True

    def get_ofenid(self):
        return self.ofenID
    def get_Drosselklappe(self):
        return self.drosselklappe
    def get_FanValue(self):
        return self.fan
    def get_steamRegularizers(self):
        return self.steamRegularizers
    def get_temp2hold(self):
        return self.temp2hold
    def get_currentTemp(self):
        return self.currentTemp
    def get_currentTempsArray(self):
        return self.currentTemps
    def get_FastHeatupValue(self):
        return self.isFastHeatUpActive
    def get_steamRegularizersValue(self):
        return self.steamRegularizers
    def get_autoMode(self):
        return self.autoM


ofen = Ofen()
localStorageController = LocalDataStorage(ofen)
localStorageController.appendData()
localStorageController.getDataAsJson()
localStorageController.getLastEntry()
"""
