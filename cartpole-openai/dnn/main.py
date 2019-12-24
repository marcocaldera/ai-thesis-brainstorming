import gym
import random
import numpy as np

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter

# INFO: website https://pythonprogramming.net/openai-cartpole-neural-network-example-machine-learning-tutorial/

LR = 1e-5  # INFO: learning rate
# INFO: se l'asticella supera i 15° left o right il gioco si considera perso.
#  Se l'asticella rimane in piedi per 200 step (default) il gioco si considera vinto
env = gym.make("CartPole-v0")
env.reset()
goal_steps = 500
score_requirement = 50  # INFO: siamo interessati ad apprendere solamente dalle partite che fanno uno score di almeno 50
initial_games = 10000


def some_random_games_first():
    """
    Partiamo con qualche gioco random così per vedere che succede
    :return:
    """
    # Each of these is its own game (faccio 5 game totali).
    for episode in range(5):
        env.reset()
        # this is each frame, up to 200...but we wont make it that far.
        for t in range(goal_steps):
            # This will display the environment
            # Only display if you really want to see it.
            # Takes much longer to display it.
            env.render()

            # This will just create a sample action in any environment.
            # In this environment, the action can be 0 or 1, which is left or right
            action = env.action_space.sample()

            # this executes the environment with an action,
            # and returns the observation of the environment,
            # the reward, if the env is over, and other info.
            observation, reward, done, info = env.step(action)
            if done:
                break


# some_random_games_first()


def initial_population():
    """
    Generiamo un training-set da dare in pasto alla nostra rete neurale in modo che possa apprendere come giocare
    Per generare il training-set semplicemente giochiamo tante partite (n° initial_games) e ci salviamo i risultati
    :return:
    """
    # [OBS, MOVES]
    training_data = []
    # all scores:
    scores = []
    # just the scores that met our threshold:
    accepted_scores = []
    # iterate through however many games we want:
    for _ in range(initial_games):
        score = 0
        # moves specifically from this environment:
        game_memory = []
        # previous observation that we saw
        prev_observation = []
        # for each frame in 200
        for _ in range(goal_steps):
            # choose random action (0 or 1)
            action = random.randrange(0, 2)
            # do it!
            observation, reward, done, info = env.step(action)

            # notice that the observation is returned FROM the action
            # so we'll store the previous observation here, pairing
            # the prev observation to the action we'll take.
            if len(prev_observation) > 0:
                # ci serve la prev perche stiamo salvando la coppia <osservazione,azione-scelta-in-base-osservazione>
                game_memory.append([prev_observation, action])
            prev_observation = observation
            score += reward  # INFO: reward=0 quando abbiamo perso, altrimenti reward=1
            if done: break

        # IF our score is higher than our threshold, we'd like to save
        # every move we made
        # NOTE the reinforcement methodology here.
        # all we're doing is reinforcing the score, we're not trying
        # to influence the machine in any way as to HOW that score is
        # reached.
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                # convert to one-hot (this is the output layer for our neural network)
                # ci per la rete neurale che in ouput avrà due neuroni
                # (in questo caso base poteva anche bastarne uno ma è per generalizzare)
                if data[1] == 1:
                    output = [0, 1]
                elif data[1] == 0:
                    output = [1, 0]

                # saving our training data
                training_data.append([data[0], output])

        # reset env to play again
        env.reset()
        # save overall scores INFO: (tanto per vederli)
        scores.append(score)

    # just in case you wanted to reference later
    training_data_save = np.array(training_data)
    np.save('training-set.npy', training_data_save)

    # some stats here, to further illustrate the neural network magic!
    print('Average accepted score:', mean(accepted_scores))
    print('Median score for accepted scores:', median(accepted_scores))
    # Raggruppa valori identici dell'array e restituisce un dict con gli elementi ordinati
    # dove ogni elemento ha associato il numero di volte in cui compare
    print(Counter(accepted_scores))

    return training_data


# initial_population()

def neural_network_model(input_size):
    # input layer
    network = input_data(shape=[None, input_size, 1], name='input')

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    # output layer
    network = fully_connected(network, 2, activation='softmax')

    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
    model = tflearn.DNN(network, tensorboard_dir='log')

    return model


def train_model(training_data, model=False):
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]), 1)
    y = [i[1] for i in training_data]

    if not model:
        model = neural_network_model(input_size=len(X[0]))

    model.fit({'input': X}, {'targets': y}, n_epoch=5, snapshot_step=500, show_metric=True, run_id='openai_learning')
    return model


# INFO: salviamo il modello (utile quando il modello ci mette tanto a fittare)
training_data = initial_population()
model = train_model(training_data)
# model.save('cartpole-openai.tflearn')

# model = neural_network_model(input_size=4)
# model.load('./cartpole-openai.tflearn')

scores = []
choices = []
for each_game in range(10):
    score = 0
    game_memory = []
    prev_obs = []
    env.reset()
    for _ in range(goal_steps):
        # env.render()

        # inizialmente non abbiamo osservazioni quindi proviamo in maniera casuale
        if len(prev_obs) == 0:
            action = random.randrange(0, 2)
        else:
            # print(prev_obs)
            # print(prev_obs.reshape(-1, len(prev_obs), 1))
            action = np.argmax(model.predict(prev_obs.reshape(-1, len(prev_obs), 1))[0])

        choices.append(action)

        new_observation, reward, done, info = env.step(action)
        prev_obs = new_observation
        game_memory.append([new_observation, action])
        score += reward
        if done: break

    scores.append(score)

print('Average Score:', sum(scores) / len(scores))
print('choice 1:{}  choice 0:{}'.format(choices.count(1) / len(choices), choices.count(0) / len(choices)))
print(score_requirement)

# guida da console
# import sys
# for path in sys.path:
#     print(path)
# exec(open(path+'/dnn/main.py').read())

# exec(open('/Users/marcocaldera/Documents/Progetti GIT/thesis-brainstorming/cartpole-openai/dnn/main.py').read())
# model.save('200.model')
