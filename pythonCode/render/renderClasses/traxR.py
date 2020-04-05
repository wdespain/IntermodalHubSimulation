class TraxR():

    def __init__(self, my):
        self.traxDirection = 1
        self.movementFactor = 50
        self.maxY = my + self.movementFactor

        self.startPos = [480, 0]
        self.curPos = [480, 0]

        self.rendering = False

    def setCanvasObject(self, co):
        self.canvasObject = co

    def updateState(self):
        if self.rendering == True:
            self.curPos[1] += (self.movementFactor*self.traxDirection)
            if(self.curPos[1] >= self.maxY):
                self.traxDirection = -1
            elif(self.curPos[1] + 130 <= 0.0):
                self.rendering = False
                self.curPos = self.startPos
                return "done"
            return [0, self.movementFactor*self.traxDirection]