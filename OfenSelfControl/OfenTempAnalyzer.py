import numpy as np
from sklearn.linear_model import LinearRegression
import time
#from timeloop import Timeloop
from datetime import timedelta
import Ofen
import threading

#x = np.array([0.5, 1, 1.5, 2, 2.5, 3]).reshape((-1, 1))
#y = np.array([0.5, 1, 1.5, 2, 2.5, 3])

t = np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5, 26, 26.5, 27, 27.5, 28, 28.5, 29, 29.5, 30])
t = t.reshape(-1,1)
a = np.array([[10,12,3,44,65,6,27],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[10,12,3,44,65,6,27],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]])
b = np.median(a,axis=1)

#print(x)
#print(y)
#print(b)

#model = LinearRegression()
#model.fit(t,b)

#g(x) = mx + c
#m = model.coef_
#c = model.intercept_

#r_sq = model.score(t,b)
#print('coefficient of determination:', r_sq)
#print('intercept:', c)
#print('slope:', m)

#Adjustable Parts in % (0.0 <-> 1.0)

class OfenTempAnalyzer:

    currentDrosselStep = 0

    step = 0
    STEP_MAX = 3
    DROSSELKLAPPE_STEP_VALUE_RISE = 1.33
    DROSSELKLAPPE_STEP_VALUE_COOLDOWN = 0.75

    temp2hold = -1000
    arrayLength = 20

    def __init__(self,ofen):
        self.ofen = ofen
        #drosselklappe = 0.0
        self.currentDrosselStep = 0

        #fan = 0.0
        #airInput = 0.0
        self.autoMode = True
        self.t1 = threading.Thread(target=self.regularizeTask, args=())





    def activateAutoMode(self):
        print("Starting Auto Mode")
        self.autoMode = True
        self.t1.start()

    def deactivateAutoMode(self):
        print("Stopping Auto Mode")
        self.autoMode = False
        self.t1.join()

    def get_AutoModeState(self):
        return self.autoMode

    def regularizeTask(self):

        while self.autoMode:
            print("Loop: regularizeTask")
            #a = self.ofen.get_a()

            a = self.ofen.get_a_n_last_values(self.arrayLength)

            if(len(a) < self.arrayLength):
                print("Waiting for data to be collected")
                print("Continue with Fast Heat Up mode")
                self.ofen.fastHeatUp()
            else:
                if(self.ofen.isFastHeatUpActive):
                    self.ofen.stopfastHeatUp()
                print("Call for regularization")
                self.regularize(a)

            time.sleep(self.arrayLength/2)

    def regularize(self,values):

        print("Perform regularization")

        if(len(values) == 0 or self.ofen.get_temp2hold() == -1000):
            return

        m = self.calaculate_m(values)
        temp2hold = self.ofen.get_temp2hold()
        currentTemp = self.ofen.get_currentTemp()

        if(currentTemp > (temp2hold - 10) and currentTemp < (temp2hold + 10)):
            print("Regularization not required, temperature is in acceptable range")
            self.step = 0
            return

        #temp2hold < currentTemp --> rise temperature
        if(currentTemp < temp2hold):

            if(m <= 0):
                #self.ofen.setDrosselklappe(self.DROSSELKLAPPE_STEP_VALUE * self.step if self.DROSSELKLAPPE_STEP_VALUE * self.step < 1 else 1)
                drosselvalue = self.ofen.get_Drosselklappe() * self.DROSSELKLAPPE_STEP_VALUE_RISE if self.ofen.get_Drosselklappe() * self.DROSSELKLAPPE_STEP_VALUE_RISE < 1 else 1
                self.ofen.set_Drosselklappe(drosselvalue)
                if(self.step > 2):
                    self.ofen.activateFan()
                if(self.step > self.STEP_MAX):
                    self.ofen.triggerAlert("lessWood")

            else:
                print("temp is rising, do nothing")

        else:#if(currentTemp >= temp2hold):
            if(m > 0):
                self.ofen.stopFan()
                self.ofen.set_Drosselklappe(self.ofen.get_Drosselklappe() * self.DROSSELKLAPPE_STEP_VALUE_COOLDOWN)

        if(self.step > self.STEP_MAX):
            self.step = 0
            return

        self.step += 1



    def calaculate_m(self,tempValues):

        tempValuesCondensed = self.condenseArrayValues(tempValues)

        if tempValuesCondensed.size < self.arrayLength:
            return -1000

        model = LinearRegression()
        model.fit(t[:self.arrayLength], tempValuesCondensed)

        m = model.coef_

        return m[0]


    def condenseArrayValues(self,tempValues):
        return np.median(tempValues, axis=1)



#o = Ofen(1)
#ot = OfenTempAnalyzer()
#print('calculatec: ', ot.calaculate_m(b[0:60]))
