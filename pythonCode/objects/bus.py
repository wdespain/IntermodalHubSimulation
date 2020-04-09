#python libs
import math
import random

#internal classes
from .vehicle import Vehicle

class Bus(Vehicle):

    def __init__(self, i, st, et, stopList = None, routeTime = -1):
        #Things that will not change once set
        super().__init__(
            i, #ID
            .04, #energyUsePerSec
            stopList, #stops
            .3, #maxSpeed
            routeTime,
            st, #startTime
            et #endTime
        )
        self.maxCharge = 700
        self.minChargeForRoute = .04 * routeTime
        
        #Things that will change, but only by internal processes
        self.currCharge = 700 #in kWh

        #This that the larger program may signal to change
        self.charging = False
        self.chargingRate = 0

    #Implementing EnvConsumer functions---------------------

    def step(self, time):
        if(self.charging == True):
            self.charge()
        else:
            self.currCharge -= self.energyUsePerSec
            super().step(time)

    def energyUseForStep(self):
        return 0 #This returns 0 because a bus itself never actually takes energy from the hub, 
        #it only ever gets power from a busCharger, so if a bus is charging the busCharger object will reflect that energy usage

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

    def setChargingRate(self, c):
        self.chargingRate = c

    def signalToCharge(self):
        self.charging = True

    def signalToStopCharging(self):
        self.charging = False
        