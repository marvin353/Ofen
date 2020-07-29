from Ofen import Ofen
class ButtonObserver(object):

    def __init__(self,ofen):
        print("Init ButtonObserver")
        self.ofen = ofen




    def buttonpressed_shutdown(self):
        print("Button pressed: Shutdown")

    def buttonpressed_steamRegularizers(self):
        print("Button pressed: SteamRegulaerizers")
        self.ofen.moveSteamRegularizers()

    def buttonpressed_autoMode(self):
        print("Button pressed: Auto Mode")

    def DIGTurnedR_temp2hold(self):
        print("DIG Turned Right: temp2Hold")

    def DIGTurnedL_temp2hold(self):
        print("DIG Turned Left: temp2Hold")

    def DIGTurnedR_drosselklappe(self):
        print("DIG Turned Right: Drosselklappe")

    def DIGTurnedL_drosselklappe(self):
        print("DIG Turned Left: Drosselklappe")
