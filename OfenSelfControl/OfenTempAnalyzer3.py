import numpy as np
from sklearn.linear_model import LinearRegression
import time
import threading

t = np.array(
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
     31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
     59])
t = t.reshape(-1, 1)


class OfenTempAnalyzer3:
    eps = 10
    CURRENT_TEMP_ARRAY_LENGTH = 10
    arrayLength = 60  # Entspricht der doppelten Intervalllänge da 1 mal pro Sekunde Daten gesammelt werden und 50% überlappen

    def __init__(self, ofen):

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

            if (len(a) < self.arrayLength):
                print("Waiting for data to be collected")
            else:
                print("Call for regularization")
                self.regularize(a)

            # Werte überlappen zur Hälfte
            time.sleep(self.arrayLength / 2)


    def regularize(self, values):

        print("Perform regularization")

        if (len(values) == 0 or self.ofen.get_temp2hold() == -1000):
            return

        p = 1000
        air = self.ofen.get_airInput()
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
        t_i10 = ti + 10*m
        reached = t_i1 / t2h  # Wert zwischen 0.0 und 1.0

        # Neuen Wert für Lufteinlass berechnen
        """print("ti########################################")
        print(ti)
        print("m########################################")
        print(m)
        print("t2h########################################")
        print(t2h)
        print("REACHED########################################")
        print(reached)"""

        # Lufteinlass:
        # Temperatur unter Zieltemperatur
        if t_i1 < t2h:
            # Temperatur steigt
            if m > 0:
                # Temperatur steigt zu langsam?
                if t_i10 < t2h:
                    # Schnelleren Temperaturanstieg erzeugen
                    new_AirInput_value = air + 0.1
            #Temperatur fällt
            else:
                # Temperaturanstieg erzeugen
                new_AirInput_value = air + 0.1
        # Temperatur über Zieltemperatur
        elif t_i1 > t2h:
            # Temperatur fällt
            if m < 0:
                # Temperatur fällt zu langsam?
                if t_i10 > t2h:
                    # Schnelleren Temperaturabfall erzeugen
                    new_AirInput_value = air - 0.1
                    if new_AirInput_value < 0.0:
                        new_AirInput_value = 0.0
                        # Drosselklappe öffnen und abkühlen lassen
                        new_drosselvalue = 1.0
            # Temperatur steigt
            else:
                # Temperaturabfall erzeugen
                new_AirInput_value = air - 0.1
                if new_AirInput_value < 0.0:
                    new_AirInput_value = 0.0
                    # Drosselklappe öffnen und abkühlen lassen
                    new_drosselvalue = 1.0
        # Temperatur == Zieltemperatur
        else:
            print("No regularization required")

        # Gebläse:
        # Gebläse aktivieren wenn Lufteinlass bereits ganz offen ist
        if new_AirInput_value > 1.0:
            new_AirInput_value = 1.0
            if self.ofen.get_FanValue() == 0.0:
                self.ofen.fanAction()
        # Gebläse ausschalten wenn Lufteinlass <= 100% ist
        else:
            if self.ofen.get_FanValue() == 1.0:
                self.ofen.fanAction()

        # Drosselklappe:
        # Neuen Wert für drosselklappe bestimmen
        if new_drosselvalue == 0.0:
            if m > d_th:
                # drosselklappe öffnen --> Feuer brennt, Rauch rauslassen
                new_drosselvalue = 1.0
            else:
                # drosselklappe schließen --> Energie sparen
                new_drosselvalue = 0.0


        # Temperatur kann nicht gehalten werden --> mehr Brennmaterial wird benötigt --> Alarm auslösen
        if m < 0 and self.ofen.get_Drosselklappe() == 0.0 and self.ofen.get_airInput() > 0.90 and self.ofen.get_FanValue() == 1.0:
            self.ofen.triggerAlert("lessWood")


        self.ofen.set_airInput(new_AirInput_value)
        self.ofen.set_Drosselklappe(new_drosselvalue)


    def calaculate_m(self, tempValues):

        tempValuesCondensed = self.condenseArrayValues(tempValues)

        if tempValuesCondensed.size < self.arrayLength:
            return -1000

        model = LinearRegression()
        model.fit(t[:self.arrayLength], tempValuesCondensed)

        m = model.coef_

        return m[0]


    def condenseArrayValues(self, tempValues):
        temp1values = np.max(tempValues, axis=1)

        x = np.array(temp1values)
        y = x[np.nonzero(x)]

        # do nothing on error
        if y == []:
            y = [1, 1]
        return y

        #return np.median(tempValues, axis=1)


    def medianCurrentTemp(self, tempValues):
        print(tempValues)

        temp1values = [item[0] for item in tempValues]

        x = np.array(temp1values)
        y = x[np.nonzero(x)]

        return np.median(y)












#######################################################################


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
# DRosselklappe
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
