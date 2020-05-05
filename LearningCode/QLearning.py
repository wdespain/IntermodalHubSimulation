def QLearning(env, num_episodes, gamma, alpha, epsilon, rewards):

# Yngying Zheng
# Email: yingying.zheng@usu.edu
# March-2020
# This is a Q-learning (off-policy in Reinforcement learning).
# The goal is to find an optimal policy that maximizes the return (min_energy bill/min_peak load) from any initial states.

state_size=len(env.state)                           # size of the state vector
action_size=len(env.action)                         # size of action vector
Q = np.array(np.zeros((state_size, action_size)))   # we initialize our values to zero
rewards_copy = np.copy(rewards)                     # Copy the rewards matrix to new Matrix

# Keeps track of useful statistics
stats = plotting.EpisodeStats(episode_lengths=np.zeros(num_episodes),episode_rewards=np.zeros(num_episodes))

for i in range(num_episodes):
    # Reset the environment and pick the first action
    state = env.reset()
    # Pick up a state randomly
    current_state = np.random.randint(0,state_size)
    # being inside the loop, iterate through the rewards matrix to get the states that are directly reachable from the randomly chosen current state and we will assign those state in a list named playable_actions.
    playable_actions = []
    # Iterate through the new rewards matrix and get the actions > 0
    for j in range(action_size):
        if rewards_copy[current_state, j] > 0:
            playable_actions.append(j)

            # Pick an action randomly from the list of playable actions leading us to the next state
            next_state = np.random.choice(playable_actions)

         # Compute the temporal difference
         # The action here exactly refers to going to the next state

         TD = rewards_copy[current_state, next_state] + gamma * Q[next_state, np.argmax(Q[next_state,])] \
              - Q[current_state, next_state]
         # best_next_action = np.argmax(Q[next_state])
         # Update the Q-Value using the Bellman equation
         Q[current_state, next_state] += alpha * TD


         # done is True is episode terminated
         if done:
             break



  return Q
