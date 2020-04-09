#python libraries
import datetime
import math

#other libraries
import gym
from gym import error, spaces, utils
from gym.utils import seeding

#internal classes
from objects.bus import Bus
from objects.snowMelt import SnowMelt
from objects.traxTrain import TraxTrain
from objects.busCharger import BusCharger
from objects.pricingSchema import PricingSchema

class HubEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    #start time
    self.simulationDateTime = datetime.datetime(2000, 1, 1, 5, 30) #Year, month, day, hour, min
    
    #make consumers
    self.consumers = []

    #routeTime is in seconds
    self.consumers.append(BusCharger(1)) #Note: Bus Charger Should be added to the list before buses for later logic reasons
    self.consumers.append(Bus(2, "6:15", "20:15", routeTime = 5400)) #length of one hour and a half
    self.consumers.append(Bus(3, "5:45", "22:30", routeTime = 1800)) #length of a half hour
    self.consumers.append(Bus(4, "6:00", "23:30", routeTime = 3600)) #length of one hour 
    self.consumers.append(TraxTrain(5, "5:43", "23:28", routeTime = 6240)) #represents one train of Blue Line (701)
    self.consumers.append(TraxTrain(7, "5:58", "23:28", routeTime = 6240)) #represents one train of Blue Line (701)
    self.consumers.append(SnowMelt(8))
    #an example of stopList:
    #self.consumers.append(Bus(2, stopList = [[5,5], [4,4], [3,3], [2,2], [1,1], [0, 0]])) #[5, 5 is hub]

    #set up energy stuff
    self.currEnergyUse = 0 #this keeps track of the energy use at a step
    self.energyUseForMonth = 0

    #set up pricing stuff
    self.pricingSchema = PricingSchema(54, 14.62, 10.91, .038127, .035143, 2300)
    self.chargeForMonth = self.pricingSchema.baseCharge

    self.observation_space = self.createObservationSpace()

    self.action_space = spaces.Tuple((
      spaces.Tuple((
        spaces.Discrete(1),
        spaces.Discrete(40),
      )),
      spaces.Tuple((
        spaces.Discrete(1),
        spaces.Discrete(40)
      ))
    ))

  #needed for gym Env---

  def step(self, action):
    self.currEnergyUse = 0

    self.implementAction(action)

    #update time
    oldMonth = self.simulationDateTime.month
    self.simulationDateTime += datetime.timedelta(seconds=1)
    if(self.simulationDateTime.month > oldMonth): #reset month counters
      self.energyUseForMonth = 0
      self.chargeForMonth = self.pricingSchema.baseCharge

    #get energy for step
    for p in self.consumers:
      p.step(self.simulationDateTime)
      self.currEnergyUse += p.energyUseForStep()

    self.energyUseForMonth += self.currEnergyUse

    #update charges
    self.calcChargeForStep()

    reward = self.calculateReward()
    #return : observation, reward, done (this will always be false for us), info (not really sure what this needs to be, so empty obj)
    return self.createObservationSpace(), reward, False, {}

  def reset(self):
    self.consumers = []

  def render(self, mode='human', close=False):
    self.consolePrintState()

  def calculateReward(self): #need to implement
    return 1

  #------------------------

  def createObservationSpace(self):
    return spaces.Tuple((
      spaces.Tuple(( #All Bus Chargers
        spaces.Tuple(( #Specific Bus Charger Tuple
          spaces.Discrete(self.consumers[0].occupied if 1 else 0), #Occupied - a Bool, just 1 or 0
          spaces.Discrete(int(self.consumers[0].energyUseForStep()*10))
        ))
      )),
      spaces.Tuple(( #All Buses
        spaces.Tuple(( #Bus 1
          spaces.Discrete(int(self.consumers[1].currCharge/self.consumers[1].maxCharge)), #bus charge
          spaces.Discrete(self.consumers[1].minChargeForRoute), # min charge needed for route
          spaces.Discrete(self.consumers[1].timeToHub)
        )),
        spaces.Tuple(( #Bus 2
          spaces.Discrete(int(self.consumers[2].currCharge/self.consumers[1].maxCharge)), #bus charge
          spaces.Discrete(self.consumers[2].minChargeForRoute), # min charge needed for route
          spaces.Discrete(self.consumers[2].timeToHub)
        )),
        spaces.Tuple(( #Bus 3
          spaces.Discrete(int(self.consumers[3].currCharge/self.consumers[1].maxCharge)), #bus charge
          spaces.Discrete(self.consumers[3].minChargeForRoute), # min charge needed for route
          spaces.Discrete(self.consumers[3].timeToHub)
        ))
      )),
      spaces.Tuple(( #All Trax Trains
        spaces.Tuple(( #Trax train 1
          spaces.Discrete(int(self.consumers[4].energyUseForStep()*10)), # Energy use
          spaces.Discrete(self.consumers[4].timeToHub)
        )),
        spaces.Tuple(( #Trax train 1
          spaces.Discrete(int(self.consumers[5].energyUseForStep()*10)), # Energy use
          spaces.Discrete(self.consumers[5].timeToHub)
        ))
      )),
      spaces.Tuple(( #All Snowmelts Tuple 
        spaces.Tuple(( #Specific Snowmelt Tuple
          spaces.Discrete(self.consumers[6].running if 1 else 0), #On or Off - a Bool, just 1 or 0
          spaces.Discrete(int(self.consumers[6].energyUseForStep()*10)) #Energy use, multiplied by 10 so it can be an int
        ))
      )),
      spaces.Discrete(10), #fixed power consumption
      spaces.Discrete(int(self.pricingSchema.peakSummerChargeKWH*1000000)), #current price per kwh
      spaces.Discrete(self.pricingSchema.peakEnergyThreashold), # peak power
      spaces.Discrete(int(self.energyUseForMonth * 100)) #power usage for the month
    ))

  def implementAction(self, action):
    print("--TEST ACTION--")
    print(action)
    #First - bool. Tell incoming bus to charge, or if a bus is charging tell it to leave
    if action[0][0] == 1:
      if self.consumers[0].occupied == True:
        self.busLeaveCharging()
      else:
        self.busToCharging()
    #Second - int kWh * 100. Change power going to bus charger
    self.consumers[0].changePowerFlow(action[0][1]/100) 
    #Third - bool. Turn snowmelt on or off
    if action[1][1] == 1:
      self.consumers[6].switchRunning()
      print("snowmelt switch")
    #Fourth - int. kWh * 100. Charge power going to snowmelt
    self.consumers[6].changePowerFlow(action[1][1]/100)

  def busToCharging(self):
    if self.consumers[1].nearHub() == True:
      print("Bus "+str(self.consumers[1].ID) +" to charge")
      self.consumers[1].signalToCharge()
      self.consumers[0].occupy(self.consumers[1].ID)
    elif self.consumers[2].nearHub() == True:
      print("Bus "+str(self.consumers[1].ID) +" to charge")
      self.consumers[2].signalToCharge()
      self.consumers[0].occupy(self.consumers[2].ID)
    elif self.consumers[3].nearHub() == True:
      print("Bus "+str(self.consumers[1].ID) +" to charge")
      self.consumers[3].signalToCharge()
      self.consumers[0].occupy(self.consumers[3].ID)

  def busLeaveCharging(self):
    busID = self.consumers[0].busChargingID
    print("Bus "+str(busID)+" leaving charging")
    self.consumers[0].deoccupy()
    c = self.getBusWithID(busID)
    c.signalToStopCharging()

  def getBusWithID(self, busID):
    for c in self.consumers:
      if c.ID == busID:
        return c

  def consolePrintState(self):
    print("timestamp: " + self.simulationDateTime.strftime("%d/%m/%Y, %H:%M:%S"))
    for p in self.consumers:
      print(p.textOutput())
    print("Current Hub Energy Use: " + str(self.currEnergyUse))
    print("Energy use for the month: "+str(self.energyUseForMonth))
    print("Cost for month: $"+str(self.chargeForMonth))

  def calcChargeForStep(self):
    if(self.isSummer() == True):
      self.chargeForMonth += self.pricingSchema.summerChargeKWH * self.currEnergyUse
      if self.energyUseForMonth > self.pricingSchema.peakEnergyThreashold:
        self.chargeForMonth += self.pricingSchema.peakSummerChargeKWH * self.currEnergyUse
    else:
      self.chargeForMonth += self.pricingSchema.winterChargeKWH * self.currEnergyUse
      if self.energyUseForMonth > self.pricingSchema.peakEnergyThreashold:
        self.chargeForMonth += self.pricingSchema.peakWinterChargeKWH * self.currEnergyUse

  def isSummer(self):
    if self.simulationDateTime.month in [5, 6, 7, 8, 9]:
      return True
    else:
      return False

  def packageInfoForRenderer(self):
    info = {}
    info["busChargerOccupied"] = self.consumers[0].occupied
    info["busInfo"] = []
    info["busInfo"].append({ "busNearHub" : self.consumers[1].nearHub() })
    info["busInfo"].append({ "busNearHub" : self.consumers[2].nearHub() })
    info["busInfo"].append({ "busNearHub" : self.consumers[3].nearHub() })
    info["traxInfo"] = []
    info["traxInfo"].append({ "traxNearHub" : self.consumers[4].nearHub() })
    info["traxInfo"].append({ "traxNearHub" : self.consumers[5].nearHub() })
    info["snowMeltRunning"] = self.consumers[6].running
    info["currEnergyUse"] = self.currEnergyUse
    return info