import os
import sys
import subprocess

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)


def run_cmd(cmd_str):
    print(cmd_str)
    p = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    return (out, err)
