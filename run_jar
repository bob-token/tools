#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import sys
import argparse

import os, time, subprocess

def runCmd(cmd):
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # stdout = p.communicate()[0].decode('utf-8').strip()
    return p


def exec(command):
    print(command)
    return runCmd(command)

def tailf(file):
    cmd='tail -f {}'.format(file)
    print(cmd)
    process=runCmd(cmd)
    # lines = process.stdout.readlines()
    for line in iter(process.stdout):
        print(line)
    process.stdout.close()
    # process.wait()

def main(argv):
    parser = argparse.ArgumentParser(description='运行jar')
    parser.add_argument("jar",help='jar文件路径')
    parser.add_argument("--log",help='日志文件路径',default=argv[0]+".log")
    parser.add_argument("--profile",help='运行配置',default="dev".strip())
    args = parser.parse_args()
    log = '/data/logs/{}'.format(args.log)
    command = 'nohup java -Xmx512m -server -jar {} --spring.profiles.active={} >{}& '.format(args.jar,args.profile,log)
    exec(command)
    tailf(log)

if __name__ == "__main__":
    main(sys.argv[1:])
