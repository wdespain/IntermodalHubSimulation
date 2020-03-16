#python libs
import math
import random

#internal classes
from .vehicle import Vehicle

class Bus(Vehicle):

    def __init__(self, i, s):
        #Things that will not change once set\
        super().__init__(
            i, #ID
            .4, #energyUsePerSecond
            s, #stops
            .3 #maxSpeed
        )
        self.maxCharge = 700
        
        #Things that will change, but only by internal processes
        self.currCharge = 700 #in kWh

        #This that the larger program may signal to change
        self.charging = False
        self.chargingRate = .4

    #Implementing EnvAgent functions---------------------

    def step(self):
        if(self.charging == True):
            #since stopped will be changed by the base class, we check here to see if the base function has told the bus to go
            # if so, we obviously need to stop charging
            if(self.stopped == False):
                self.charging = False
            else:
                self.charge()
        if(self.stopped == False):
            self.currCharge -= self.energyUsePerSec
        super().step()

    def energyUseForStep(self):
        if self.charging == True:
            return self.chargingRate
        else:
            return 0

    def textOutput(self):
        output = "Bus " + super().textOutput()
        output += " Charge: " + str(math.trunc((self.currCharge / self.maxCharge)*100)) + "%" +"(" + str(self.currCharge) + "/" + str(self.maxCharge) + ")"
        return output

    #-------------------------------------------------------

    def charge(self):
        self.currCharge += self.chargingRate
        if self.currCharge > self.maxCharge:
            self.currCharge = self.maxCharge
            self.charging = False