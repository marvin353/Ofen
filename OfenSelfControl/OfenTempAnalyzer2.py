import numpy as np
from sklearn.linear_model import LinearRegression
import time
import threading


class OfenTempAnalyzer:

    t = np.array(range(0,60))
    t = t.reshape(-1, 1)

    eps = 10
    CURRENT_TEMP_ARRAY_LENGTH = 10
    arrayLength = 60 # Entspricht der halben Intervalllänge da 1 mal pro Sekunde Daten gesammelt werden und 50% überlappen

    def __init__(self,ofen):
        self.ofen = ofen

        self.autoMode = False
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

            a = self.ofen.get_a_n_last_values(self.arrayLength)

            if(len(a) < self.arrayLength):
                print("Waiting for data to be collected")
            else:
                print("Call for regularization")
                self.regularize(a)

            #Werte überlappen zur Hälfte
            time.sleep(self.arrayLength/2)

    def regularize(self, values):

        print("Perform regularization")

        if (len(values) == 0 or self.ofen.get_temp2hold() == -1000):
            return

        p = 1000
        new_AirInput_value = 0.0
        new_drosselvalue = 0.0
        d_th = 10

        # Aktuelle Temperatur (Median über die letzten n Werte)
        ti = self.medianCurrentTemp(self.ofen.get_a_n_last_values(self.CURRENT_TEMP_ARRAY_LENGTH))

        # Steigung des letzten Intervalls
        m = self.calaculate_m(values)

        # Geschätzte Temperatur am nächsten Messzeitpunkt + erreichter Wert in Prozent zur Zieltemperatur
        t2h = self.ofen.get_temp2hold()
        t_i1 = ti + m
        reached = t_i1 / t2h  # Wert zwischen 0.0 und 1.0

        # Neuen Wert für Lufteinlass berechnen
        if reached <= 0.5:
            new_AirInput_value = 1.0

            # Gebläse einschalten
            if not self.ofen.get_FanValue():
                self.ofen.fanAction()
        else:
            new_AirInput_value = round(pow((1 / p), (reached - 0.5)), 2)

            # Gebläse ausschalten
            if self.ofen.get_FanValue():
                self.ofen.fanAction()

        # Neuen Wert für drosselklappe bestimmen
        if m > 0:
            if m > d_th:
                # drosselklappe öffnen --> Feuer brennt, Rauch rauslassen
                new_drosselvalue = 1.0
            else:
                # drosselklappe schließen --> Energie sparen
                new_drosselvalue = 0.0
        else:
            # drosselklappe schließen --> Weil temp2hold vermutlich erreicht, dann Energie sparen
            drosselvalue = 0.0

        # Temperatur kann nicht gehalten werden --> mehr Brennmaterial wird benötigt --> Alarm auslösen
        if m < 0 and self.ofen.get_Drosselklappe() == 0.0 and self.ofen.get_airInput() > 0.90:
            self.ofen.triggerAlert("lessWood")

        self.ofen.set_airInput(new_AirInput_value)
        self.ofen.set_Drosselklappe(drosselvalue)


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


    def medianCurrentTemp(self, tempValues):
        temp1values = [item[0] for item in tempValues]
        return np.median(temp1values, axis=1)




######################
    """def regularize_old(self, values):

        print("Perform regularization")

        if (len(values) == 0 or self.ofen.get_temp2hold() == -1000):
            return

        m = self.calaculate_m(values)
        temp2hold = self.ofen.get_temp2hold()
        currentTemp = self.medianCurrentTemp(
            self.ofen.get_a_n_last_values(self.CURRENT_TEMP_ARRAY_LENGTH))  # self.ofen.get_currentTemp()

        # Distanz in % --> z.B. t= 20, t2h = 100 => distance_t_t2h = 0.2 (20%)
        distance_t_t2h = currentTemp / temp2hold

        if (currentTemp > (temp2hold - self.eps) and currentTemp < (temp2hold + self.eps)):
            print("Regularization not required, temperature is in acceptable range")
            self.step = 0
            return

        # temp2hold < currentTemp --> rise temperature
        if (currentTemp < temp2hold):

            if (m <= 0):
                # self.ofen.setDrosselklappe(self.DROSSELKLAPPE_STEP_VALUE * self.step if self.DROSSELKLAPPE_STEP_VALUE * self.step < 1 else 1)
                drosselvalue = self.ofen.get_Drosselklappe() * self.DROSSELKLAPPE_STEP_VALUE_RISE if self.ofen.get_Drosselklappe() * self.DROSSELKLAPPE_STEP_VALUE_RISE < 1 else 1
                self.ofen.set_Drosselklappe(drosselvalue)
                if (self.step > 2):
                    self.ofen.activateFan()
                if (self.step > self.STEP_MAX):
                    self.ofen.triggerAlert("lessWood")

            else:
                print("temp is rising, do nothing")

        else:  # if(currentTemp >= temp2hold):
            if (m > 0):
                self.ofen.stopFan()
                self.ofen.set_Drosselklappe(self.ofen.get_Drosselklappe() * self.DROSSELKLAPPE_STEP_VALUE_COOLDOWN)

        if (self.step > self.STEP_MAX):
            self.step = 0
            return

        self.step += 1"""




#o = Ofen(1)
#ot = OfenTempAnalyzer()
#print('calculatec: ', ot.calaculate_m(b[0:60]))






# temp == temp2hold +- eps:
#   do nothing

# temp < temp2hold:
#   m = Steigung der letzten 30 sek
#   m > 0:   ---> Temperatur Steigt
#       --->Gut, nichts tun oder schnelleren Anstieg erzeugen
#   m <= 0:
#       --->Schlecht, weil Tempratur steigen soll
#       mehrLuft + wenn Luft == 100% dann Fan --> mehrLuft abhängig von m? oder nur funktion auf %t/t2h basis?
#       + overshot predict and avoid, temp + m*intervall > t2h+eps?
#
# temp > temp2hold
#
####
#
#   p = 1000
#   ti = median last n
#   m = Steigung des letzten Intervalls
#   t_i1 = ti + m
#   reached = t_i1/t2h
#   if reached <= 0.5:
#        new_AirInput_value = 1.0
#   else:
#       new_AirInput_value = (1/p)^(reached - 0.5)
#
#
#
#
#
#
#
#
#
#DRosselklappe
#
# schwellwert d_th = 123456789?
# m > 0:
#   m über d_th:
#       drosselklappe öffnen --> Feuer brennt, Rauch rauslassen
#   m unter d_th
#        drosselklappe schließen --> Energie sparen
#
# m <=0:
#   drosselklappe schließen --> Weil temp2hold vermutlich erreicht, dann Energie sparen
#
#
#
#
#
#
#
#
#
