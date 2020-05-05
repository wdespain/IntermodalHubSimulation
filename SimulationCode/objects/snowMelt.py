#python libraries
import random

#internal classes
from .envConsumer import EnvConsumer

class SnowMelt(EnvConsumer):

    def __init__(self, i):
        #Things that will not change once set
        super().__init__(
            i, #ID
            .4 #energyUsePerSec
        )

        #Things that will change, but only by internal processes
        self.runningTimer = 0 

        #This that the larger program may signal to change
        self.running = False

    #Implementing EnvConsumer functions---------------------

    #This doesn't move so nothing needs to happen in step right now
    #but this needs to be implemented so nothing gets messed up
    #in the future checking for time of day/year may need to happen
    def step(self, time): 
        self.running = self.running

    def energyUseForStep(self):
        if self.running == True:
            return self.energyUsePerSec
        else:
            return 0

    def textOutput(self):
        return "Snow Melt " + str(self.ID) + "Potential Energy: " + str(self.energyUsePerSec) + " On? " + str(self.running)

    #-------------------------------------------------------

    def switchRunning(self):
        self.running = not self.running