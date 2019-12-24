import gym
from gym import wrappers

# https://towardsdatascience.com/cartpole-introduction-to-reinforcement-learning-ed0eb5b58288
# https://gym.openai.com/envs/CartPole-v0/

env = gym.make('CartPole-v0')
# env = gym.make('MountainCar-v0')
# env = gym.make('MsPacman-v0')

"""
Test 1
"""
env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample())  # take a random action
env.close()

"""
Test 2
"""
# for i_episode in range(1):
#     env = wrappers.Monitor(env, 'VideoMain', force=True)
#     observation = env.reset()
#     for t in range(100):
#         env.render()
#         action = env.action_space.sample()
#         observation, reward, done, info = env.step(action)
#         if done:
#             print("Episode finished after {} timesteps".format(t + 1))
#             break
# env.close()

# print(env.action_space)
# print(env.observation_space)
