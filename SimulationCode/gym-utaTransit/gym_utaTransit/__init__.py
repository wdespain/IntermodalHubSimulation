from gym.envs.registration import register

register(
    id='utaTransit-v0',
    entry_point='gym_utaTransit.envs:HubEnv',
)