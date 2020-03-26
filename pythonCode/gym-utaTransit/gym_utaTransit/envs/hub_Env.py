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

class HubEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.simulationTimeInSeconds = math.trunc(datetime.datetime(2000, 1, 1).timestamp())

    self.consumers = []

    #make consumers
    self.consumers.append(BusCharger(1)) #Note: Bus Charger Should be added to the list before buses for later logic reasons
    self.consumers.append(Bus(2, [[5,5], [4,4], [3,3], [2,2], [1,1], [0, 0]])) #[5, 5 is hub]
    self.consumers.append(TraxTrain(3, [[5,5], [4,4], [3,3], [2,2], [1,1], [0, 0]]))
    self.consumers.append(SnowMelt(4))

    self.currEnergyUse = 0

    self.observation_space = spaces.Box(low=0, high=255, shape=(0,0,3))
    self.action_space = spaces.Tuple((
      spaces.Discrete(1),
      spaces.Discrete(1)
    ))

  #needed for gym Env---

  def step(self, action):
    self.simulationTimeInSeconds += 1

    self.currEnergyUse = 0

    for p in self.consumers:
      p.step()
      self.currEnergyUse += p.energyUseForStep()

    reward = self.calculateReward()
    #return : observation, reward, done (this will always be false for us), info (not really sure what this needs to be, so empty obj)
    return self.consumers, reward, False, {}

  def reset(self):
    self.consumers = []

  def render(self, mode='human', close=False):
    print("timestamp: "+datetime.datetime.utcfromtimestamp(self.simulationTimeInSeconds).strftime("%d/%m/%Y, %H:%M:%S"))
    self.consolePrintState()

  def calculateReward(self): #need to implement
    return 1

  #------------------------

  def consolePrintState(self):
    for p in self.consumers:
      print(p.textOutput())
    print("Current Hub Energy Use: " + str(self.currEnergyUse))

  def packageInfoForRenderer(self):
    info = {}
    info["traxNearHub"] = self.consumers[2].nearHub()
    info["currEnergyUse"] = self.currEnergyUse
    info["busNearHub"] = self.consumers[1].nearHub()
    info["snowMeltRunning"] = self.consumers[3].running
    info["busChargerOccupied"] = self.consumers[0].occupied
    return info