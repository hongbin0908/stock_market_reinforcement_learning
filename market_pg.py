import os
import sys
import numpy as np
import pandas as pd

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)

from market_env import MarketEnv
from market_model_builder import MarketPolicyGradientModelBuilder
from keras import backend as K
K.set_image_dim_ordering('th')
import tensorflow as tf

config = tf.ConfigProto(intra_op_parallelism_threads=1, \
                        inter_op_parallelism_threads=1, \
                        allow_soft_placement=True, \
                        device_count = {'CPU': 1})
session = tf.Session(config=config)
K.set_session(session)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PolicyGradient:

    def __init__(self, env, env_test, discount = 0.99, model_filename = None, history_filename = None):
        self.env = env
        self.env_test = env_test
        self.discount = discount
        self.model_filename = model_filename
        self.history_filename = history_filename

        from keras.optimizers import SGD
        self.model = MarketPolicyGradientModelBuilder(modelFilename).getModel()
        sgd = SGD(lr = 0.1, decay = 1e-6, momentum = 0.9, nesterov = True)
        self.model.compile(loss='mse', optimizer='rmsprop')

        self.test_avg_reward_sum = 0
        self.avg_reward_sum = 0

    def discount_rewards(self, r):
        discounted_r = np.zeros_like(r)
        running_add = 0
        r = r.flatten()

        for t in reversed(range(0, r.size)):
            if r[t] != 0:
                running_add = 0

            running_add = running_add * self.discount + r[t]
            discounted_r[t] = running_add

        return discounted_r

    def paper(self, code):
        def take_position():
            date2position = {}
            game_over = False
            observation = self.env_test._reset(code)
            while not game_over:
                aprob = self.model.predict(observation)[0]
                if aprob.shape[0] > 1:
                    action = np.random.choice(env_test.action_space.n, 1, p=aprob / np.sum(aprob))[0]
                else:
                    action = 0 if np.random.uniform() < aprob else 1
                observation, reward, game_over, info = env_test.step(action)
                date2position[info['dt']] = action
            return date2position
        def cum_return(sym, row):
            date = row['date']
            close_rel = row['close_rel']
            if date in date2position:
                position = date2position[date]
                if 1 == position:
                    result['cum'] *= close_rel
                    return result['cum']
                elif 0 == position:
                    result['cum'] *= 2 - close_rel
                    return result['cum']
            else:
                print(date , 'not in date2postion')
                return result['cum']
        def cum_return_bh(sym, row): ## buy and hold
            def bought_every_day(sym, current_day):
                return 1
            position = bought_every_day(sym ,row['date'])
            if 1 == position:
                result['cum'] *= row['close_rel']
            elif 0 == position:
                pass
            elif -1 == position:
                pass # no short
            return result['cum']
        def cum_return_sh(sym, row): # short and hold
            def bought_every_day(sym, current_day):
                return -1
            position = bought_every_day(sym ,row['date'])
            if 1 == position:
                result['cum'] *= row['close_rel']
            elif 0 == position:
                pass
            elif -1 == position:
                result['cum'] *= 2 - row['close_rel']
            return result['cum']

        df = pd.read_csv(os.path.join(local_path, 'data', '%s.csv' % code))
        start = self.env_test.startDate
        end = self.env_test.endDate
        df = df[(df.date >= start) & (df.date < end)]
        dates = pd.to_datetime(df.date, format='%Y-%m-%d')
        df['close_rel']  = (df.close / df.close.shift(1)).fillna(1.0)

        date2position = take_position()
        result = {'cum':1}
        df_cum = df.apply(lambda x: cum_return('^DJI', x), axis = 1)
        import matplotlib.pyplot as plt
        plt.plot(dates, df_cum)
        df_cum = df.apply(lambda x: cum_return_bh('^DJI', x), axis = 1)
        plt.plot(dates, df_cum)
        df_cum = df.apply(lambda x: cum_return_sh('^DJI', x), axis = 1)
        plt.plot(dates, df_cum)
        plt.show()

    def test(self, e, code, verbose=False):
        env_test = self.env_test
        model = self.model
        env_test._reset(code)
        observation = env_test._reset(code)
        game_over = False
        reward_sum = 0
        while not game_over:
            aprob = model.predict(observation)[0]
            if aprob.shape[0] > 1:
                action = np.random.choice(env_test.action_space.n, 1, p = aprob / np.sum(aprob))[0]
            else:
                action = 0 if np.random.uniform() < aprob else 1

            observation, reward, game_over, info = env_test.step(action)
            reward_sum += float(reward)
            if verbose > 0:
                if env_test.actions[action] == "LONG" or env_test.actions[action] == "SHORT":
                    color = bcolors.FAIL if env_test.actions[action] == "LONG" else bcolors.OKBLUE
                    print("%s:\t%s\t%.2f\t%.2f\t" % (info["dt"], color + env_test.actions[action] + bcolors.ENDC, reward_sum, info["cum"]) + ("\t".join(["%s:%.2f" % (l, i) for l, i in zip(env_test.actions, aprob.tolist())])))

        self.test_avg_reward_sum = self.test_avg_reward_sum * 0.99 + reward_sum * 0.01
        toPrint = "%d\t%s\t%s\t%.2f\t%.2f" % (e, info["code"], (bcolors.FAIL if reward_sum >= 0 else bcolors.OKBLUE) + ("%.2f" % reward_sum) + bcolors.ENDC, info["cum"], self.test_avg_reward_sum)
        return toPrint

    def train(self, max_episode = 1000000, max_path_length = 200, verbose = True):
        env = self.env
        model = self.model

        for e in range(max_episode):
            from random import random
            code = self.env.targetCodes[int(random() * len(self.env.targetCodes))]
            env._reset(code)
            observation = env._reset(code)
            game_over = False
            reward_sum = 0

            inputs = []
            outputs = []
            predicteds = []
            rewards = []

            while not game_over:
                aprob = model.predict(observation)[0]
                inputs.append(observation)
                predicteds.append(aprob)
                
                if aprob.shape[0] > 1:
                    action = np.random.choice(self.env.action_space.n, 1, p = aprob / np.sum(aprob))[0]

                    y = np.zeros([self.env.action_space.n])
                    y[action] = 1.

                    outputs.append(y)
                else:
                    action = 0 if np.random.uniform() < aprob else 1

                    y = [float(action)]
                    outputs.append(y)

                observation, reward, game_over, info = self.env.step(action)
                reward_sum += float(reward)

                rewards.append(float(reward))

                if verbose > 0:
                    if env.actions[action] == "LONG" or env.actions[action] == "SHORT":
                        color = bcolors.FAIL if env.actions[action] == "LONG" else bcolors.OKBLUE
                        print("%s:\t%s\t%.2f\t%.2f\t" % (info["dt"], color + env.actions[action] + bcolors.ENDC, reward_sum, info["cum"]) + ("\t".join(["%s:%.2f" % (l, i) for l, i in zip(env.actions, aprob.tolist())])))

            self.avg_reward_sum = self.avg_reward_sum * 0.99 + reward_sum * 0.01
            toPrint = "%d\t%s\t%s\t%.2f\t%.2f" % (e, info["code"], (bcolors.FAIL if reward_sum >= 0 else bcolors.OKBLUE) + ("%.2f" % reward_sum) + bcolors.ENDC, info["cum"], self.avg_reward_sum)
            print(toPrint,'\t', self.test(e, code))
            if self.history_filename != None:
                os.system("echo %s >> %s" % (toPrint, self.history_filename))


            dim = len(inputs[0])
            inputs_ = [[] for i in range(dim)]
            for obs in inputs:
                for i, block in enumerate(obs):
                    inputs_[i].append(block[0])
            inputs_ = [np.array(inputs_[i]) for i in range(dim)]

            outputs_ = np.vstack(outputs)
            predicteds_ = np.vstack(predicteds)
            rewards_ = np.vstack(rewards)

            discounted_rewards_ = self.discount_rewards(rewards_)
            #discounted_rewards_ -= np.mean(discounted_rewards_)
            discounted_rewards_ /= np.std(discounted_rewards_)

            #outputs_ *= discounted_rewards_
            for i, r in enumerate(zip(rewards, discounted_rewards_)):
                reward, discounted_reward = r

                if verbose > 1:
                    print(outputs_[i], end=' ')
                
                #outputs_[i] = 0.5 + (2 * outputs_[i] - 1) * discounted_reward
                if discounted_reward < 0:
                    outputs_[i] = 1 - outputs_[i]
                    outputs_[i] = outputs_[i] / sum(outputs_[i])
                outputs_[i] = np.minimum(1, np.maximum(0, predicteds_[i] + (outputs_[i] - predicteds_[i]) * abs(discounted_reward)))

                if verbose > 1:
                    print(predicteds_[i], outputs_[i], reward, discounted_reward)

            model.fit(inputs_, outputs_, nb_epoch = 1, verbose = 0, shuffle = True)
            model.save_weights(self.model_filename)

if __name__ == "__main__":
    import sys
    import codecs

    argi = 1
    mode = sys.argv[argi]; argi += 1
    codeListFilename = sys.argv[argi]; argi +=1
    modelFilename = sys.argv[argi]; argi +=1
    historyFilename = sys.argv[argi]; argi +=1

    codeMap = {}
    f = codecs.open(codeListFilename, "r", "utf-8")

    for line in f:
        if line.strip() != "":
            tokens = line.strip().split(",") if not "\t" in line else line.strip().split("\t")
            codeMap[tokens[0]] = tokens[1]

    f.close()

    env = MarketEnv(dir_path = "./data/", target_codes = list(codeMap.keys()), input_codes = [], start_date = "2002-12-25", end_date = "2007-12-25", sudden_death = -1.0)
    env_test = MarketEnv(dir_path = "./data/", target_codes = list(codeMap.keys()), input_codes = [], start_date = "2007-12-26", end_date = "2008-12-25", sudden_death = -1.0)
    pg = PolicyGradient(env, env_test, discount = 0.9, model_filename = modelFilename, history_filename = historyFilename)
    if mode == 'train':
        pg.train(verbose = 0)
    elif mode == 'paper':
        pg.paper('^DJI')
    else:
        assert False
