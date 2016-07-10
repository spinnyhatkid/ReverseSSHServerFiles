#!/usr/bin/python2

import subprocess
import re

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
        for p in range(len(ports)):
            port = ports[p]
            whois_info = bash_command("ssh -p %d -o StrictHostKeyChecking=no localhost cat /tmp/netInfo.tmp" % (int(port) + 1000))
            ports[p] += "," + re.search(r".*OrgId.*", whois_info).group().split(":")[1].strip()
            ports[p] += "," + re.search(r".*OrgName.*", whois_info).group().split(":")[1].strip()
            if re.search("db_nmap", bash_command("ssh -p %d -o StrictHostKeyChecking=no localhost ps aux" % (int(port) + 1000))) is not None:
                ports[p] += ",Nmap"
            else:
                ports[p] += "," + bash_command("ssh -p %d -o StrictHostKeyChecking=no localhost /etc/penScanCall.py -t s" % (int(port) + 1000))
    except:
        ports = []

with open("/var/www/ssshp", "w") as out_file:
    out_file.write('\n'.join(ports))

open("/var/www/ssshp.tmp", "w").close()
