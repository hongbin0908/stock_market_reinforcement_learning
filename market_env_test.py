import os, sys
import pandas as pd
import math

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)


import util
from market_env import MarketEnv

def init_env1():
    dir_path = os.path.join(local_path, 'tmp', 'market_env')
    util.mkdirp(dir_path)

    df = pd.DataFrame(data = {
        'date': [10000 + i for i in range(1,  21)],
        'open': [1.0 + 0.1 * i for i in range(1, 21)],
        'high': [1.0 + 0.1 * i for i in range(1, 21)],
        'low': [1.0 + 0.1 * i for i in range(1, 21)],
        'close': [1.0 + 0.1 * i for i in range(1, 21)],
        'volume': [1000 + 10 * i for i in range(1, 21)],
    })

    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df.to_csv(os.path.join(dir_path, 'SYM1.csv'), index=False)

    env = MarketEnv(dir_path=dir_path, codes=['SYM1'], target_date_start='10015', target_date_end='10020', scope=4)
    return env
def test_MarketEnv__init__():
    env = init_env1()
    print(env.observation_space)
    dates = sorted(env.data_map['SYM1'].keys())
    assert True


def test_MarketEnv_reset():
    env = init_env1()
    env._reset()

    assert env.dates[env.current_target_index] == str(int(env.target_date_start))


def test_MarketEnv_defineState():
    import numpy as np
    env = init_env1()
    env._reset()
    env.defineState()
    print(env.target)
    assert np.array([1,0,0]).sum() == env.state[0].sum()
    assert round(env.state[1][0][0][0][0],4) == round((2.4 - 2.3)/2.3,4)
    assert round(env.state[1][0][0][1][0],4) == round((2.3 - 2.2)/2.2,4)
    assert round(env.state[1][0][0][2][0],4) == round((2.2 - 2.1)/2.1,4)
    assert round(env.state[1][0][0][3][0],4) == round((2.1 - 2.0)/2.0,4)

def test_MarketEnv_step():
    env = init_env1(); env._reset()
    assert False == env.done
    state, reward, done , info = env._step(0)
    assert 1 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round(2.5/2.4,4) == round(info["cum"],4)
    assert '10015' == info['dt']

    state, reward, done , info = env._step(0)
    assert 2 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5),4) == round(info["cum"],4)
    assert '10016' == info['dt']

    state, reward, done , info = env._step(0)
    assert 3 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5) * (2.7/2.6),4) == round(info["cum"],4)
    assert '10017' == info['dt']

    state, reward, done , info = env._step(0)
    assert 4 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7),4) == round(info["cum"],4)
    assert '10018' == info['dt']

    state, reward, done , info = env._step(0)
    assert 5 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8),4) == round(info["cum"],4)
    assert '10019' == info['dt']

    state, reward, done , info = env._step(0)
    assert 0 == len(env.boughts)
    e  = ((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8) * (3.0/2.9)*math.pow(env.PENALTY,6)) - 1
    e += ((2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8) * (3.0/2.9)*math.pow(env.PENALTY,5)) - 1
    e += ((2.7/2.6)*(2.8/2.7)*(2.9/2.8) * (3.0/2.9)*math.pow(env.PENALTY,4)) - 1
    e += ((2.8/2.7)*(2.9/2.8) * (3.0/2.9)*math.pow(env.PENALTY,3)) - 1
    e += ((2.9/2.8) * (3.0/2.9)*math.pow(env.PENALTY,2)) - 1
    e += ((3.0/2.9)*math.pow(env.PENALTY,1)) - 1
    assert round(reward,4) == round(e,4)
    assert True == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8) * (3.0/2.9),4) == round(info["cum"],4)
    assert '10020' == info['dt']

def test_MarketEnv_step2():
    env = init_env1(); env._reset()
    assert False == env.done
    state, reward, done , info = env._step(1) # short
    assert 1 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round(2.5/2.4,4) == round(info["cum"],4)
    assert '10015' == info['dt']

    state, reward, done , info = env._step(1)
    assert 2 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5),4) == round(info["cum"],4)
    assert '10016' == info['dt']

    state, reward, done , info = env._step(1)
    assert 3 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5) * (2.7/2.6),4) == round(info["cum"],4)
    assert '10017' == info['dt']

    state, reward, done , info = env._step(1)
    assert 4 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7),4) == round(info["cum"],4)
    assert '10018' == info['dt']

    state, reward, done , info = env._step(1)
    assert 5 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8),4) == round(info["cum"],4)
    assert '10019' == info['dt']

    state, reward, done , info = env._step(1)
    assert 0 == len(env.boughts)
    e  = ((2.3/2.4)*(2.4/2.5)*(2.5/2.6)*(2.6/2.7)*(2.7/2.8) * (2.8/2.9)*math.pow(env.PENALTY,6)) - 1
    e += ((2.4/2.5)*(2.5/2.6)*(2.6/2.7)*(2.7/2.8) * (2.8/2.9)*math.pow(env.PENALTY,5)) - 1
    e += ((2.5/2.6)*(2.6/2.7)*(2.7/2.8) * (2.8/2.9)*math.pow(env.PENALTY,4)) - 1
    e += ((2.6/2.7)*(2.7/2.8) * (2.8/2.9)*math.pow(env.PENALTY,3)) - 1
    e += ((2.7/2.8) * (2.8/2.9)*math.pow(env.PENALTY,2)) - 1
    e += ((2.8/2.9)*math.pow(env.PENALTY,1)) - 1
    assert round(reward,4) == round(e,4)
    assert True == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8) * (3.0/2.9),4) == round(info["cum"],4)
    assert '10020' == info['dt']

def test_MarketEnv_step3():
    env = init_env1(); env._reset()
    assert False == env.done
    state, reward, done , info = env._step(1) # short
    assert 1 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round(2.5/2.4,4) == round(info["cum"],4)
    assert '10015' == info['dt']

    state, reward, done , info = env._step(1)
    assert 2 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5),4) == round(info["cum"],4)
    assert '10016' == info['dt']

    state, reward, done , info = env._step(1)
    assert 3 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5) * (2.7/2.6),4) == round(info["cum"],4)
    assert '10017' == info['dt']

    state, reward, done , info = env._step(0)
    assert 1 == len(env.boughts)
    e  = ((2.3/2.4)*(2.4/2.5)*(2.5/2.6)*math.pow(env.PENALTY,3)) - 1
    e += ((2.4/2.5)*(2.5/2.6)*math.pow(env.PENALTY,2)) - 1
    e += ((2.5/2.6)*math.pow(env.PENALTY,1)) - 1
    assert round(reward,4) == round(e,4)
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7),4) == round(info["cum"],4)
    assert '10018' == info['dt']

    state, reward, done , info = env._step(0)
    assert 2 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8),4) == round(info["cum"],4)
    assert '10019' == info['dt']

    state, reward, done , info = env._step(0)
    assert 0 == len(env.boughts)
    e  = ((2.8/2.7)*(2.9/2.8)*(3.0/2.9)*math.pow(env.PENALTY,3)) - 1
    e += ((2.9/2.8)*(3.0/2.9)*math.pow(env.PENALTY,2)) - 1
    e += ((3.0/2.9)*math.pow(env.PENALTY, 4)) - 1
    assert round(reward,4) == round(e,4)
    assert True == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8) * (3.0/2.9),4) == round(info["cum"],4)
    assert '10020' == info['dt']

def test_MarketEnv_step4():
    env = init_env1(); env._reset()
    assert False == env.done
    state, reward, done , info = env._step(1) # short
    assert 1 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round(2.5/2.4,4) == round(info["cum"],4)
    assert '10015' == info['dt']

    state, reward, done , info = env._step(1)
    assert 2 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5),4) == round(info["cum"],4)
    assert '10016' == info['dt']

    state, reward, done , info = env._step(1)
    assert 3 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5) * (2.7/2.6),4) == round(info["cum"],4)
    assert '10017' == info['dt']

    state, reward, done , info = env._step(0)
    assert 1 == len(env.boughts)
    e  = ((2.3/2.4)*(2.4/2.5)*(2.5/2.6)*math.pow(env.PENALTY,3)) - 1
    e += ((2.4/2.5)*(2.5/2.6)*math.pow(env.PENALTY,2)) - 1
    e += ((2.5/2.6)*math.pow(env.PENALTY,1)) - 1
    assert round(reward,4) == round(e,4)
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7),4) == round(info["cum"],4)
    assert '10018' == info['dt']

    state, reward, done , info = env._step(0)
    assert 2 == len(env.boughts)
    assert reward == 0
    assert False == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8),4) == round(info["cum"],4)
    assert '10019' == info['dt']

    state, reward, done , info = env._step(1)
    assert 0 == len(env.boughts)
    e  = ((2.8/2.7)*(2.9/2.8)*math.pow(env.PENALTY,2)) - 1
    e += ((2.9/2.8)*math.pow(env.PENALTY,1)) - 1
    e += ((2.8/2.9)*math.pow(env.PENALTY, 1)) - 1
    assert round(reward,4) == round(e,4)
    assert True == done
    assert round((2.5/2.4)*(2.6/2.5)*(2.7/2.6)*(2.8/2.7)*(2.9/2.8) * (3.0/2.9),4) == round(info["cum"],4)
    assert '10020' == info['dt']
