#python libraries
import random

#other libraries
import numpy as np

#internal classes
from .envAgent import EnvAgent

class Vehicle(EnvAgent):

    def __init__(self, i, e, s, m):
        #Things that will not change once set
        super().__init__(
            i, #ID
            e #energyUsePerSecond
        )
        self.stops = s
        self.maxSpeed = m

        #Things that will change, but only by internal processes
        self.location = [5, 5] #x, y
        self.stopCountdown = 0 #this will tell how long the vehicle should be stopped at a stop
        self.speedUp = True
        self.slowDown = False
        self.stopped = False
        self.movementDirection = -1 #this will be -1 or 1 to say which direction the vehicle is moving along the line

        #This that the larger program may signal to change
        self.movementPerSec = 0 #mph, but may be pos/neg to denote direction

    #Implementing EnvAgent functions------------------------
    #This holds the most basic functionality of a vehicle,
    # child classes should extend this, not just overide
    def step(self):
        self.stopCountdown -= 1
        if(self.stopped == True and self.stopCountdown <= 0 ):
            self.stopped = False
            self.speedUp = True
            self.slowDown = False #just in case
        if(self.stopped == False):
            self.updateSpeed()
            self.updateLocation()
            self.checkForUpcomingStop()

    #outputs basic information for vehicle
    #  child clases should extend, not overide
    def textOutput(self):
        output = str(self.ID)
        output += " Location: " + str(self.location)
        output += " Curr Speed/Sec: " + str(self.movementPerSec*np.sign(self.movementDirection))
        output += " Going? "
        if self.stopped == True:
            output +=  "Stopped (" + str(self.stopCountdown) + ")"
        if self.speedUp == True:
            output += " Accelerating "
        if self.slowDown == True:
            output += " Decelerating "
        return output

    #-------------------------------------------------------

    #updates speed based on speeding up or slowing down
    #note : since movementPerSec may be negative, the speed change needs to take into account the pos/neg of movementPerSec
    def updateSpeed(self):
        if(self.speedUp == True):
            if self.movementPerSec < self.maxSpeed:
                self.movementPerSec += .1
        elif(self.slowDown == True):
            if self.movementPerSec > .1:
                self.movementPerSec -= .1
        self.movementPerSec = np.around(self.movementPerSec, decimals=1)
    
    def updateLocation(self):
        self.location[1] += (self.movementPerSec*np.sign(self.movementDirection))
        self.location[0] += (self.movementPerSec*np.sign(self.movementDirection))
        self.checkForEnds()

    #This is super janky right now because I'm just using the dummy stops
    #this will probably need a bigger overhaul when dealing with actual stops
    def checkForEnds(self):
        if(self.location[0] <= self.stops[len(self.stops) - 1][0]):
            self.movementDirection = 1
        elif(self.location[0] >= self.stops[0][0]):
            self.movementDirection = -1

    def checkForUpcomingStop(self):
        for s in self.stops:
            xPos = xNeg = yPos = yNeg = 0
            # which side that needs checking depends on which way the vehicle is approaching
            if self.movementDirection == -1:
                xPos = yPos = .1
            else:
                xNeg = yNeg = .1
            if self.checkIfLocationInRange(s, xPos, xNeg, yPos, yNeg): #checking if it is close enough to just go to the stop
                self.location[0] = s[0]
                self.location[1] = s[1]
                self.stopped = True
                self.speedUp = False
                self.slowDown = False
                self.stopCountdown = random.randrange(2, 5)
                self.movementPerSec = 0
            else:
                xPos = xNeg = yPos = yNeg = 0
                if self.movementDirection == -1:
                    xPos = yPos = .5
                else:
                    xNeg = yNeg = .5
                if self.checkIfLocationInRange(s, xPos, xNeg, yPos, yNeg):
                    self.speedUp = False
                    self.slowDown = True

    #Checks if the current location is near a given location within given bounds
    def checkIfLocationInRange(self, checkLoc, xPos, xNeg, yPos, yNeg):
        if(self.location[0] <= (checkLoc[0] + xPos) and self.location[0] >= (checkLoc[0] - xNeg)
        and self.location[1] <= (checkLoc[1] + yPos) and self.location[1] >= (checkLoc[1] - yNeg)):
            return True
        else:
            return False

    #assumption: hub is stop[0]
    def nearHub(self):
        if self.checkIfLocationInRange(self.stops[0], .5, .5, .5, .5):
            return True
        else:
            return False