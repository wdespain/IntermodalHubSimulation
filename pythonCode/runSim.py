#other libraries
import gym

#internal libraries
import gym_utaTransit
from render.renderer import envRender

def main():
    env = gym.make("gym_utaTransit:utaTransit-v0")
    #if you want to run without the visualization, comment out the next three lines and line 22
    renderer = envRender(550, 400) #pass box size
    renderer.setupView("./render/assets/drawing.gif")
    renderer.setupState()

    #observation = env.reset()
    while True:
      env.render()
      
      action = env.action_space.sample() # your agent here (this takes random actions)
      observation, reward, done, info = env.step(action)

      renderer.updateState(env.packageInfoForRenderer())

      if done:
        observation = env.reset()
    env.close()

if __name__ == "__main__":
    main()