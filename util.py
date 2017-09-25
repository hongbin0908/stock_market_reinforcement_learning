import os
import sys
import subprocess

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)


def run_cmd(cmd_str):
    print(cmd_str)
    p = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while True:
        out = p.stdout.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out.decode('utf-8'))
            sys.stdout.flush()
