#python libraries
import random

#internal classes
from .envAgent import EnvAgent

class SnowMelt(EnvAgent):

    def __init__(self, i):
        #Things that will not change once set
        super().__init__(
            i, #ID
            .4 #energyUsePerSecond
        )

        #Things that will change, but only by internal processes
        self.runningTimer = 0 

        #This that the larger program may signal to change
        self.running = False

    #Implementing EnvAgent functions---------------------

    #This doesn't move so nothing needs to happen in step right now
    #but this needs to be implemented so nothing gets messed up
    def step(self): 
        if(self.running == False): #all this stuff is only for demo, take out!
            chance = random.randrange(1, 8)
            if chance == 3:
                self.running = True
                self.runningTimer = 10
        else:
            self.runningTimer -= 1
            if self.runningTimer <= 0:
                self.running = False#take out to here!-----------------------
        #self.running = self.running

    def energyUseForStep(self):
        if self.running == True:
            return self.energyUsePerSec
        else:
            return 0

    def textOutput(self):
        return "Snow Melt " + str(self.ID) + " On? " + str(self.running)

    #-------------------------------------------------------