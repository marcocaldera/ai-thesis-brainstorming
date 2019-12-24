import gym
import numpy as np
from gym import wrappers

env = gym.make('CartPole-v0')

best_length = 0
episode_length = []

best_weights = np.zeros(4)

for i in range(100):
    new_weight = np.random.uniform(-1.0, 1.0, size=4)
    length = []

    # Gioco 100 episodi per ogni peso provato
    for i_episode in range(100):
        observation = env.reset()
        done = False
        count = 0

        while not done:
            count += 1
            action = 1 if np.dot(observation, new_weight) > 0 else 0

            observation, reward, done, _ = env.step(action)
        length.append(count)

    average_length = float(sum(length) / len(length))

    if average_length > best_length:
        best_length = average_length
        best_weights = new_weight

    episode_length.append(average_length)

    if i % 10 == 0:
        print('Best length is: ', best_length)

# Testing con i migliori pesi trovati
done = False
count = 0
env = wrappers.Monitor(env, 'VideoTest', force=True)
observation = env.reset()

while not done:
    count += 1
    action = 1 if np.dot(observation, best_weights) > 0 else 0

    observation, reward, done, _ = env.step(action)

print("Il gioco è durato: ", count, ' mosse')  # ricorda che il gioco dura al massimo 200 mosse
env.close()
