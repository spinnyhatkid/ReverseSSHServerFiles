#!/usr/bin/python2

import subprocess

min_port = 29000
max_port = 29999

def bash_call(cmd):
    return subprocess.call(['/bin/bash', '-c', cmd])

def bash_command(cmd):
    return subprocess.check_output(['/bin/bash', '-c', cmd])

with open("/var/www/ssshp", "r") as in_file:
    existing = in_file.read().splitlines()

ports = []
try:
    b = bash_command("netstat -l | grep tcp | grep LISTEN | grep '*:[[:digit:]]'").splitlines()
    ports = map(lambda line: line.split()[3][2:], b)
    ports = filter(lambda port: int(port) >= min_port and int(port) <= max_port, ports)
except:
    ports = []

with open("/var/www/ssshp", "w") as out_file:
    out_file.write('\n'.join(ports))
