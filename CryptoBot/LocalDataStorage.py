import sqlite3
from datetime import datetime
import json

class LocalDataStorage(object):


    def __init__(self):
        print("Init LocalDataStorage")

        #Start with clean local db
        #self.cleanDb()

    def connect2db(self):
        conn = sqlite3.connect('CryptoBotBD.db')
        conn.row_factory = self.dict_factory
        return conn


    def disconnectFromDb(self, conn):
        conn.close()


    def cleanDb(self):
        conn = self.connect2db()
        c = conn.cursor()
        c.execute("DELETE From CBTable")
        conn.commit()
        conn.close()


    def getDataAsJson(self):
        print("getDataAsJson")
        conn = self.connect2db()
        cursor = conn.cursor()
        cursor.execute("SELECT * From CBTable")
        results = cursor.fetchall()
        conn.close()
        #print(json.dumps(results))
        return json.dumps(results)


    def appendData(self, worth, coins, currentPrice, x, diff, balance, thLower, thUpper):

        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y, %H:%M:%S")

        conn = self.connect2db()
        c = conn.cursor()

        sqlite_insert_with_param = """INSERT INTO CBTable
                                  (ID, worth , coins, current_price, x, diff, balance, th_lower, th_upper, timestamp) 
                                  VALUES (NULL , ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        data_tuple = (worth, coins, currentPrice, x, diff, balance, thLower, thUpper, date_time)
        c.execute(sqlite_insert_with_param, data_tuple)

        conn.commit()
        conn.close()


    def getLastEntry(self):
        conn = self.connect2db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CBTable ORDER BY ID DESC LIMIT 1")
        results = cursor.fetchall()
        #print(results)
        conn.close()
        return results


    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

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
