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

        self.trax = [] 

    def setupView(self, backgroundImg):
        hold = PhotoImage(file=backgroundImg)
        self.background_image = hold.subsample(4)
        self.canvas.create_image(0, 0, image=self.background_image, anchor=NW)

    def setupState(self, setupInfo):
        self.energyText = StringVar()
        self.energyLabel = Label(self.tk, textvariable = self.energyText, anchor=S, fg="red", font=("Helvetica", 16))
        self.energyLabel.pack()

        self.createBuses(setupInfo["busInfo"])
        self.createTrax(setupInfo["traxInfo"])
        self.createSnowMelt()

    def updateState(self, information):
        #update bus
        for i in range(0, len(self.buses)):
            if self.buses[i].rendering == True:
                response = self.buses[i].updateState()
                if response != "done":
                    self.canvas.coords(self.buses[i].canvasObject, self.buses[i].getBusDrawPoints())
            else:
                if information["busInfo"][i]["busNearHub"] == True:
                    self.buses[i].rendering = True

        #update trax
        for i in range(0, len(self.trax)):
            if self.trax[i].rendering == True:
                response = self.trax[i].updateState()
                if response != "done":
                    self.canvas.move(self.trax[i].canvasObject, response[0], response[1])
            else:
                if information["traxInfo"][i]["traxNearHub"] == True:
                    self.trax[i].rendering = True

        #update Energy
        self.energyText.set("Curr Energy Use: " + str(information["currEnergyUse"]))

        #update Snow Melt
        if information["snowMeltRunning"] == True:
            self.canvas.itemconfig(self.snowMelt.textObject, text="on")
        else:
            self.canvas.itemconfig(self.snowMelt.textObject, text="off")

    def createBuses(self, buses):
        for i in range(0, len(buses)):
            newBus = BusR()
            newBus.setCanvasObject(self.canvas.create_polygon(newBus.getBusDrawPoints(), fill="black"))
            self.buses.append(newBus)

    def createTrax(self, trax):
        for i in range(0, len(trax)):
            newTrax = TraxR(200) #max Y pos of the top of the rectange
            startX = newTrax.startPos[0]
            startY = newTrax.startPos[1]
            newTrax.setCanvasObject(self.canvas.create_rectangle(startX, startY, startX + 50, startY - 130, fill="black"))
            self.trax.append(newTrax)

    def createSnowMelt(self):
        self.snowMelt = SnowMeltR()
        startX = self.snowMelt.startPos[0]
        startY = self.snowMelt.startPos[1]
        self.snowMelt.setCanvasObject(self.canvas.create_rectangle(startX, startY, startY + self.snowMelt.boxSize, startY + self.snowMelt.boxSize, fill="gray"))
        self.snowMelt.setTextObject(self.canvas.create_text(275, 320, text="off"))