import gym
import itertools
import matplotlib
import matplotlib.style
import numpy as np
import pandas as pd
import sys
import random

#internal libraries
import gym_utaTransit
env = gym.make("gym_utaTransit:utaTransit-v0")

# Initializations
number_states = 100     # number_of_states
number_actions = 100    # number_of_actions
max_iteration = 5000    # max_iteration
num_episode = 100       # number of episodes

# parameters for Q learning
gamma = 1.0      # ---discount_factor: varies on the range of [0,1]. It controls the importance of the future rewards versus the immediate ones.
alpha = 0.6      # ---alpha: learning rate
epsilon = 0.05   # ---epsilon: exploratiuon rate

# call the reward funcation
rewards=rewards_funcation()

# Train the model
Qagent=QLearning(env, num_episodes, gamma, alpha, epsilon, rewards)
# Plot important statistics
print(Qagent)





