#internal classes
from .vehicle import Vehicle

class TraxTrain(Vehicle):

    def __init__(self, i, s):
        #Things that will not change once set
        super().__init__(
            i, #ID
            0, #energyUsePerSecond
            s, #stops
            .5 #maxSpeed
        )
        self.energyProfile = {}

        #Things that will change, but only by internal processes

        #This that the larger program may signal to change

    #Implementing EnvConsumer functions---------------------
    def step(self):
        super().step()

    def energyUseForStep(self):
        if self.nearHub() == True:
        #For the train, we will have to take into account the regenerative stuff when leaving station (or is it when breaking?)
            return .4
        else:
            return 0

    def textOutput(self):
        output = "Trax " + super().textOutput()
        return output

    #-------------------------------------------------------