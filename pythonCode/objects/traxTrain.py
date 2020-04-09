#internal classes
from .vehicle import Vehicle

class TraxTrain(Vehicle):

    def __init__(self, i, st, et, stopList = None, routeTime = -1):
        #Things that will not change once set
        super().__init__(
            i, #ID
            0, #energyUsePerSec
            stopList, #stops
            .5, #maxSpeed
            routeTime,
            st, #startTime
            et #endTime
        )
        self.energyProfile = {}

        #Things that will change, but only by internal processes

        #This that the larger program may signal to change

    #Implementing EnvConsumer functions---------------------
    def step(self, time):
        super().step(time)

    def energyUseForStep(self):
        if self.nearHub() == True:
        #For the train, we will have to take into account the regenerative stuff when leaving station (or is it when breaking?)
            return .4
        else:
            return 0

    def textOutput(self):
        output = "Trax " + super().textOutput()
        return output

    def changePowerFlow(self, e):
        raise Error("You Cannot Change Power Flow to the Trax! The Trax is Unchanging and Uncaring.")

    #-------------------------------------------------------