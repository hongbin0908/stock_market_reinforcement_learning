import os
import sys
import re
import numpy as np
import pandas as pd

local_path = os.path.realpath(os.path.dirname(__file__))
root = os.path.join(local_path, '..')
sys.path.append(root)

if __name__ == "__main__":

    argi = 1
    code = sys.argv[argi]; argi += 1
    start = sys.argv[argi]; argi += 1
    end = sys.argv[argi]; argi += 1

    contents = os.walk(local_path)
    for root, dirs, files in contents:
        for f in files:
            m = re.match(r"paper-\\.*csv", f)
            if m:
                print(os.path.join(root, f))
