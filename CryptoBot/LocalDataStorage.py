import sqlite3
from datetime import datetime
import json

class LocalDataStorage(object):


    def __init__(self):
        print("Init LocalDataStorage")

        #Start with clean local db
        #self.cleanDb()

    def connect2db(self):
        conn = sqlite3.connect('CryptoBotBD0.25.db')
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
