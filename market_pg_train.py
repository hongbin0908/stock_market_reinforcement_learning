import os
import sys
import numpy as np
import pandas as pd

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)

from market_env import MarketEnv
from policy_gradient import PolicyGradient

if __name__ == "__main__":
    import sys
    import codecs

    argi = 1
    codeListFilename = sys.argv[argi]; argi +=1
    #modelFilename = sys.argv[argi]; argi +=1
    #historyFilename = sys.argv[argi]; argi +=1
    train_start = sys.argv[argi]; argi += 1
    train_end = sys.argv[argi]; argi += 1
    test_start = sys.argv[argi]; argi += 1
    test_end = sys.argv[argi]; argi += 1
    max_episode = int(sys.argv[argi]); argi +=1

    model_filename = "%s-%s-%s.pg.model.h5" % (codeListFilename, train_start, train_end)
    print("model file name : %s" % model_filename)
    history_filename = "%s-%s-%s.pg.history.h5" % (codeListFilename, train_start, train_end)
    print("history file name : %s" % history_filename)

    codeMap = {}
    f = codecs.open(codeListFilename, "r", "utf-8")

    for line in f:
        if line.strip() != "":
            tokens = line.strip().split(",") if not "\t" in line else line.strip().split("\t")
            codeMap[tokens[0]] = tokens[1]

    f.close()

    env = MarketEnv(dir_path = "./data/", target_codes = list(codeMap.keys()), input_codes = [], start_date = train_start, end_date = train_end, sudden_death = -1.0)
    env_test = MarketEnv(dir_path = "./data/", target_codes = list(codeMap.keys()), input_codes = [], start_date = test_start, end_date = test_end, sudden_death = -1.0)
    pg = PolicyGradient(env, env_test, discount = 0.9, model_filename = model_filename, history_filename = history_filename)
    pg.train(verbose = 0, max_episode=max_episode)
