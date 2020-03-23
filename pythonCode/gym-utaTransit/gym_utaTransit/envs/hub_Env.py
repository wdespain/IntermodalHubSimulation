#other libraries
import gym
from gym import error, spaces, utils
from gym.utils import seeding

#internal classes
from objects.bus import Bus
from objects.snowMelt import SnowMelt
from objects.traxTrain import TraxTrain

class HubEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.consumers = []

    #make consumers
    self.consumers.append(Bus(1, [[5,5], [4,4], [3,3], [2,2], [1,1], [0, 0]])) #[5, 5 is hub]
    self.consumers.append(TraxTrain(2, [[5,5], [4,4], [3,3], [2,2], [1,1], [0, 0]]))
    self.consumers.append(SnowMelt(3))

    self.currEnergyUse = 0

    self.observation_space = spaces.Box(low=0, high=255, shape=(0,0,3))
    self.action_space = spaces.Tuple((
      spaces.Discrete(1),
      spaces.Discrete(1)
    ))

  #needed for gym Env---

  def step(self, action):
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
    info["traxNearHub"] = self.consumers[1].nearHub()
    info["currEnergyUse"] = self.currEnergyUse
    info["busNearHub"] = self.consumers[0].nearHub()
    info["snowMeltRunning"] = self.consumers[2].running
    return info