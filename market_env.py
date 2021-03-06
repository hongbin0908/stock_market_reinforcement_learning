import os, sys
from random import random
import numpy as np
import math

import gym
from gym import spaces

class MarketEnv(gym.Env):

    PENALTY = 1 #0.999756079

    def __init__(self, dir_path, codes, target_date_start, target_date_end, scope = 60, sudden_death = -1., cumulative_reward = False):
        self.target_date_start = target_date_start
        self.target_date_end = target_date_end
        self.scope = scope # 考虑历史数据的长度 60天
        self.sudden_death = sudden_death # 控制game over的变量, -1表示不会结束.
        self.cumulative_reward = cumulative_reward

        self.codes = []
        self.data_map = {} # symbol: [{'date':(high, low ,close, volumn)}..]

        for code in (codes):
            fn = os.path.join(dir_path,  code + ".csv")
            data = {}
            lastClose = 0
            lastVolume = 0
            try:
                f = open(fn, "r")
                for line in f:
                    if line.strip() != "":
                        dt, openPrice, high, low, close, volume = line.strip().split(",")
                        try:
                            high = float(high) if high != "" else float(close)
                            low = float(low) if low != "" else float(close)
                            close = float(close)
                            volume = int(float(volume))
                            # 正则化 这个正则化的过程不是很懂? 能保证 high > close > low??
                            if lastClose > 0 and close > 0 and lastVolume > 0:
                                close_ = (close - lastClose) / lastClose
                                high_ = (high - close) / close
                                low_ = (low - close) / close
                                volume_ = (volume - lastVolume) / lastVolume

                                data[dt] = (high_, low_, close_, volume_)

                            lastClose = close
                            lastVolume = volume
                        except Exception as e:
                            print(e, line.strip().split(","))
                f.close()
            except Exception as e:
                print(e)

            if len(list(data.keys())) > scope:
                self.data_map[code] = data
                if code in codes:
                    self.codes.append(code)

        self.actions = [
            "LONG",
            "SHORT",
        ]

        self.action_space = spaces.Discrete(len(self.actions))
        #self.observation_space = spaces.Box(np.ones(scope * (len(input_codes) + 1)) * -1, np.ones(scope * (len(input_codes) + 1)))

        #self._reset()
        self._seed()

    def _step(self, action):
        if self.done:
            return self.state, self.reward, self.done, {}

        self.reward = 0
        if self.actions[action] == "LONG":
            if sum(self.boughts) < 0:
                for b in self.boughts:
                    self.reward += -(b + 1)
                if self.cumulative_reward:
                    self.reward = self.reward / max(1, len(self.boughts))

                if self.sudden_death * len(self.boughts) > self.reward:
                    self.done = True

                self.boughts = []

            self.boughts.append(1.0)
        elif self.actions[action] == "SHORT":
            if sum(self.boughts) > 0:
                for b in self.boughts:
                    self.reward += b - 1
                if self.cumulative_reward:
                    self.reward = self.reward / max(1, len(self.boughts))

                if self.sudden_death * len(self.boughts) > self.reward:
                    self.done = True

                self.boughts = []

            self.boughts.append(-1.0)
        else:
            pass

        vari = self.target[self.dates[self.current_target_index]][2]
        self.cum = self.cum * (1 + vari)

        for i in range(len(self.boughts)):
            self.boughts[i] = self.boughts[i] * MarketEnv.PENALTY * (1 + vari * (-1 if sum(self.boughts) < 0 else 1))

        self.defineState()
        if self.current_target_index >= len(self.dates)-1 or self.target_date_end <= self.dates[self.current_target_index]:
            self.done = True

        if self.done:
            for b in self.boughts:
                self.reward += (b * (1 if sum(self.boughts) > 0 else -1)) - 1
            if self.cumulative_reward:
                self.reward = self.reward / max(1, len(self.boughts))

            self.boughts = []

        e = self.state, self.reward, self.done, {"dt": self.dates[self.current_target_index], "cum": self.cum, "code": self.current_code}
        self.current_target_index += 1
        return e

    def _reset(self, code=None):
        if not code is None:
            self.current_code = code
        else:
            self.current_code = self.codes[int(random() * len(self.codes))]
        self.target = self.data_map[self.current_code] # 随意选择一个股票
        self.dates = sorted(self.target.keys())
        for i in range(len(self.dates)):
            if self.dates[i] >= self.target_date_start:
                self.current_target_index = i
                break
        if self.current_target_index < self.scope:
            self.current_target_index = self.scope

        print(self.dates[self.current_target_index])
        self.boughts = []
        self.cum = 1.

        self.done = False
        self.reward = 0

        self.defineState()

        return self.state

    def _render(self, mode='human', close=False):
        if close:
            return
        return self.state

    '''
    def _close(self):
        pass

    def _configure(self):
        pass
    '''

    def _seed(self):
        return int(random() * 100)

    def defineState(self):
        tmpState = []

        budget = (sum(self.boughts) / len(self.boughts)) if len(self.boughts) > 0 else 1.
        size = math.log(max(1., len(self.boughts)), 100)
        position = 1. if sum(self.boughts) > 0 else 0. # postion =1 做多, =0 做空 或者不做
        tmpState.append([[budget, size, position]])

        subject = []
        subjectVolume = []
        for i in range(self.scope):
            try:
                subject.append([self.target[self.dates[self.current_target_index - 1 - i]][2]]) # close
                subjectVolume.append([self.target[self.dates[self.current_target_index - 1 - i]][3]]) # volume
            except Exception as e:
                assert False
                print(self.current_code, self.current_target_index, i, len(self.dates))
                self.done = True
        tmpState.append([[subject, subjectVolume]])

        tmpState = [np.array(i) for i in tmpState]
        self.state = tmpState
        assert (1,3) == self.state[0].shape
        assert (1,2,self.scope, 1) == self.state[1].shape
