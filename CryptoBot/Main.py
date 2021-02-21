import numpy as np
import time
import threading
from LocalDataStorage import LocalDataStorage
import sys
import os
import urllib
import json
from urllib.request import urlopen

class CBMain(object):


    def __init__(self):

        self.balance = 1000
        self.worth = 1000
        self.coins = 0
        self.currentPrice = 0
        self.x = 0
        self.diff = 0
        self.th_upper = 0.01
        self.th_lower = -0.01

        self.nextAction = "null" # "sell or buy"

        self.localDataStorage = LocalDataStorage()

        self.initialBuy()

        self.t1 = threading.Thread(target=self.performAlgo, args=())
        self.t1.start()


    def initialBuy(self):
        try:
            print("Initial Buy")
            self.currentPrice = self.getCurrentPrice()
            self.x = self.currentPrice
            self.buyAction()
            self.nextAction = "sell"
        except Exception as e:
            print(e)


    def performAlgo(self):
        while(True):
            try:
                print("Make decision")
                self.currentPrice = self.getCurrentPrice()

                self.diff = (self.currentPrice / self.x) - 1
                print("Diff: " + str(self.diff) + ", X: " + str(self.x) + ", CP: " + str(self.currentPrice) + ", Bal: " + str(self.balance) + ", Coins: " + str(self.coins))

                if self.nextAction == "sell" and self.diff >= self.th_upper:
                    #sell action
                    self.sellAction()
                    self.nextAction = "buy"
                    self.x = self.currentPrice

                if self.nextAction == "buy" and self.diff <= self.th_lower:
                    #buy action
                    self.buyAction()
                    self.nextAction = "sell"
                    self.x = self.currentPrice

                self.worth = self.coins * self.currentPrice + self.balance
                self.storeData()
                time.sleep(60)
            except Exception as e:
                print(e)
                time.sleep(60)


    def sellAction(self):
        print("Sell")
        self.balance = self.coins * self.currentPrice
        self.coins = 0

    def buyAction(self):
        print("Buy")
        self.coins = self.balance / self.currentPrice
        self.balance = 0


    def getCurrentPrice(self):
        data = urllib.request.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json").read()
        output = json.loads(data)
        price_str = output["bpi"]["USD"]["rate"]
        price_str = price_str.replace(",", "")
        price = float(price_str)
        return price


    def storeData(self):
        self.localDataStorage.appendData(self.worth, self.coins, self.currentPrice, self.x, self.diff, self.balance, self.th_lower, self.th_upper)




if __name__ == '__main__':

    finished = False

    try:
        print("Starting with main...")
        main = CBMain()
        while(not finished):
            print("main loop")
            if (finished):
                sys.exit()
            time.sleep(10)
    except:
        print("Perform Shutdown")
        finished = True

