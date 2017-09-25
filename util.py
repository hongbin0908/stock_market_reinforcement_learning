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
            sys.stdout.write(out)
            sys.stdout.flush()
        err = p.stderr.read(1)
        if err == '' and p.poll() != None:
            break
        if err != '':
            sys.stderr.write(out)
            sys.stderr.flush()
