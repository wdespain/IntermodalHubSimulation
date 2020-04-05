#internal classes
from .envConsumer import EnvConsumer

class BusCharger(EnvConsumer):

    def __init__(self, i):
        #Things that will not change once set
        super().__init__(
            i, #ID
            .4 #energyUsePerSecond
        )

        #Things that will change, but only by internal processes

        #This that the larger program may signal to change
        self.occupied = False
        self.busChargingID = None

    #Implementing EnvConsumer functions---------------------

    #This doesn't move so nothing needs to happen in step right now
    def step(self, time): 
        self.occupied = self.occupied #this needs to be here because this func needs to be implemented so nothing gets messed up

    def energyUseForStep(self):
        if self.occupied == True:
            return self.energyUsePerSec
        else:
            return 0

    def textOutput(self):
        return "Bus Charger " + str(self.ID) + " Occupied? " + str(self.occupied)

    #-------------------------------------------------------

    def occupy(self, bID):
        self.occupied = True
        self.busChargingID = bID

    def deoccupy(self):
        self.occupied = False
        self.busChargingID = None

    def changePowerFlow(self, e):
        self.energyUsePerSec = e
