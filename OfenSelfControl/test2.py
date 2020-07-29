class Ofen:
    a = [[0, 0, 0, 0, 0, 0, 0]]


    def __init__(self):
        self.ofenID = 1
        self.drosselklappe = 0.1
        self.fan = 0.2
        self.steamRegularizers = 0.3
        self.temp2hold = 218.0
        self.currentTemp = 111.0
        self.currentTemps = [100, 200, 300, 400, 500, 600, 700]
        self.isFastHeatUpActive = False

    def get_ofenIDm(self):
        return self.ofenID
    def get_drosselklappe(self):
        return self.drosselklappe
    def get_fan(self):
        return self.fan
    def get_steamRegularizers(self):
        return self.steamRegularizers
    def get_temp2hold(self):
        return self.temp2hold
    def get_currentTemp(self):
        return self.currentTemp
    def get_currentTemps(self):
        return self.currentTemps
    def get_isFastHeatUpActive(self):
        return self.isFastHeatUpActive


ofen = Ofen()
id = ofen.get_ofenIDm()
print(id)
