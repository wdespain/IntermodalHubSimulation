#python libraries
from tkinter import *

#render (internal) libraries
from render.renderClasses.busR import BusR
from render.renderClasses.traxR import TraxR
from render.renderClasses.snowMeltR import SnowMeltR

class envRender():

    def __init__(self, xSize, ySize):
        self.tk = Tk()
        self.canvas = Canvas(self.tk, width=xSize, height=ySize)
        self.tk.title("Intermodal Hub")
        self.canvas.pack()

        self.width = xSize
        self.height = ySize

        self.buses = []

        self.trax = None #there should only be one train at a time

    def setupView(self, backgroundImg):
        hold = PhotoImage(file=backgroundImg)
        self.background_image = hold.subsample(4)
        self.canvas.create_image(0, 0, image=self.background_image, anchor=NW)

    def setupState(self):
        self.energyText = StringVar()
        self.energyLabel = Label(self.tk, textvariable = self.energyText, anchor=S, fg="red", font=("Helvetica", 16))
        self.energyLabel.pack()

        self.createBus()
        self.createTrax()
        self.createSnowMelt()

    def updateState(self, information):
        #update bus
        if len(self.buses) != 0:
            for i in range(0, len(self.buses)):
                response = self.buses[i].updateState()
                if response == "delete":
                    self.buses.remove(self.buses[i]) #TODO: handle removing buses better, this could fuck up the itteration of the bus list later
                else:
                    self.canvas.coords(self.buses[i].canvasObject, self.buses[i].getBusDrawPoints())
        else:
            if information["busNearHub"] == True:
                self.createBus()

        #update trax
        if self.trax != None:
            response = self.trax.updateState()
            if response == "delete":
                self.trax = None
            else:
                self.canvas.move(self.trax.canvasObject, response[0], response[1])
        else:
            if information["traxNearHub"] == True:
                self.createTrax()

        #update Energy
        self.energyText.set("Curr Energy Use: " + str(information["currEnergyUse"]))

        #update Snow Melt
        if information["snowMeltRunning"] == True:
            self.canvas.itemconfig(self.snowMelt.textObject, text="on")
        else:
            self.canvas.itemconfig(self.snowMelt.textObject, text="off")

    def createBus(self):
        newBus = BusR()
        newBus.setCanvasObject(self.canvas.create_polygon(newBus.getBusDrawPoints(), fill="black"))
        self.buses.append(newBus)

    def createTrax(self):
        self.trax = TraxR(200) #max Y pos of the top of the rectange
        startX = self.trax.startPos[0]
        startY = self.trax.startPos[1]
        self.trax.setCanvasObject(self.canvas.create_rectangle(startX, startY, startX + 50, startY + 130, fill="black"))

    def createSnowMelt(self):
        self.snowMelt = SnowMeltR()
        startX = self.snowMelt.startPos[0]
        startY = self.snowMelt.startPos[1]
        self.snowMelt.setCanvasObject(self.canvas.create_rectangle(startX, startY, startY + self.snowMelt.boxSize, startY + self.snowMelt.boxSize, fill="gray"))
        self.snowMelt.setTextObject(self.canvas.create_text(275, 320, text="off"))