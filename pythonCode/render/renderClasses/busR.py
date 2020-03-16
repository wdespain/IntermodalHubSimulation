#python libraries
import cmath, math

class BusR():

    def __init__(self):
        self.busSteps = [[18,30],[18,32],[15,23],[35,31],[37,18],[35,-5],[35,-34],[22,-41],[15,-34],[13,-36],[0,-20],[0, -30],[0,-40]] #busSteps is only for testing, need to update
        self.busAngles = [(7.5*math.pi)/4, (7.5*math.pi)/4, (7*math.pi)/4, (6.5*math.pi)/4, (6.25*math.pi)/4, (5.75*math.pi)/4, (5.25*math.pi)/4, (4.75*math.pi)/4, (4.25*math.pi)/4, (4*math.pi)/4, 0, 0, 0]
        self.busOn = -1 #busOn is only for testing, need to update

        self.curPos = [140, 0] #x, y of top left corner
        self.busWidth = 40
        self.busLength = 75

        self.busPos = [[140, 0], [180, 0], [180, 75], [140, 75]]

    def setCanvasObject(self, co):
        self.canvasObject = co

    def updateState(self):
        self.busOn += 1
        if self.busOn >= len(self.busSteps):
            return "delete"
        else:
            self.curPos[0] += self.busSteps[self.busOn][0]
            self.curPos[1] += self.busSteps[self.busOn][1]
            self.calculateBusPoints()
            return self.busSteps[self.busOn]

    def calculateBusPoints(self):
        self.busPos[0][0] = self.curPos[0]
        self.busPos[0][1] = self.curPos[1]

        self.busPos[1][0] = self.curPos[0] + self.busWidth
        self.busPos[1][1] = self.curPos[1]

        self.busPos[2][0] = self.curPos[0] + self.busWidth
        self.busPos[2][1] = self.curPos[1] + self.busLength

        self.busPos[3][0] = self.curPos[0]
        self.busPos[3][1] = self.curPos[1] + self.busLength
        
        center = self.getCenter()
        offset = complex(center[0], center[1])
        angle = cmath.exp(self.busAngles[self.busOn]*1j) # angle in radians
        for point in self.busPos:
            v = angle * (complex(point[0], point[1]) - offset) + offset
            point[0] = v.real
            point[1] = v.imag

    def getCenter(self):
        return [(self.curPos[0] + (self.busWidth/2)),(self.curPos[1] + (self.busLength/2))]

    def getBusDrawPoints(self):
        startX = self.curPos[0]
        startY = self.curPos[1]    

        newXY = []
        for b in self.busPos:
            newXY.append(b[0])
            newXY.append(b[1])
        return newXY