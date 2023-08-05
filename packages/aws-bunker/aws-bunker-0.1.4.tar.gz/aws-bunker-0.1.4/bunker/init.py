#!/usr/bin/env python

"""init bunker config file"""

import configparser
import sys
import os
from os.path import expanduser
import json
import time
import signal
import subprocess
import pkg_resources

class Bcolors:
    """console colors"""
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    GREY = '\033[90m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;212m'
    PALEYELLOW = '\033[38;5;228m'
    PALEBLUE = '\033[38;5;111m'

def signal_handler(sig, frame):
    print('\nuser cancelled. halt and catch fire.')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def query_yes_no(question, default="yes"):
    '''confirm or decline'''
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '': 
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("\nPlease respond with 'yes' or 'no' (or 'y' or 'n').\n")

def init_bunker(instance_id=None):
    #config here
    home = expanduser('~')
    bunker_config = os.path.join(home, ".config-bunker.ini")
    if os.path.exists(bunker_config):
        config = configparser.ConfigParser()
        config.read(bunker_config)
        prefix = config['default']['prefix']
        pem = config['default']['pem']
        if instance_id is None:
            instance_id = config['default']['instance_id']
        username = config['default']['username']
        git_user = config['default']['git_user']
        git_pass = config['default']['git_pass']
        bb_user = config['default']['bb_user']
        bb_pass = config['default']['bb_pass']
    else:
        print(Bcolors.PALEYELLOW+"no config file found."+Bcolors.ENDC)
        prefix, pem, instance_id, username, git_user, git_pass, bb_user, bb_pass = "unknown", "unknown", "unknown", "unknown", "unknown", "unknown", "unknown", "unknown"

    newconfig = """[default]
prefix = {prefix}
repos = {repos}
ignored = {ignored}
pem = {pem}
instance_id = {iid}
username = {username}
git_user = {guser}
git_pass = {gpass}
bb_user = {bbuser}
bb_pass = {bbpass}
"""
    instance_id = input(Bcolors.ENDC+"EC2 Instance ID "+Bcolors.UNDERLINE+instance_id+Bcolors.ENDC+" : "+Bcolors.PALEYELLOW) or instance_id
    while True:
        prefix = input(Bcolors.ENDC+"Directory where you will store repositories file "+Bcolors.UNDERLINE+prefix+Bcolors.ENDC+"\n"+Bcolors.PALEBLUE+"absolute path like: `/Users/username/bunker_files/` : "+Bcolors.PALEYELLOW) or prefix
        if not prefix.endswith("/"):
            if config['default']['prefix']:
                prefix = config['default']['prefix']
            else:
                prefix = "unknown"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"prefix must end with a /"+Bcolors.ENDC)
            continue
        else:
            break
    while True:
        repofile = input(Bcolors.ENDC+"Name of repository file "+Bcolors.UNDERLINE+"repositories.txt"+Bcolors.ENDC+" : "+Bcolors.PALEYELLOW) or "repositories.txt"
        if not repofile.endswith(".txt"):
            repofile = "repositories.txt"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"repository filename must be .txt"+Bcolors.ENDC)
            continue
        else:
            break
    while True:
        ignorefile = input(Bcolors.ENDC+"Name of ignored-git-files file "+Bcolors.UNDERLINE+"ignoredfiles.txt"+Bcolors.ENDC+" : "+Bcolors.PALEYELLOW) or "ignoredfiles.txt"
        if not ignorefile.endswith(".txt"):
            ignorefile = "ignoredfiles.txt"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"ignored filename must be .txt"+Bcolors.ENDC)
            continue
        else:
            break
    while True:
        pem = input(Bcolors.ENDC+"Full path to .pem keyfile "+Bcolors.UNDERLINE+pem+Bcolors.ENDC+" : "+Bcolors.PALEYELLOW) or pem
        if not pem.endswith(".pem"):
            if config['default']['pem']:
                pem = config['default']['pem']
            else:
                pem = "unknown"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"keyfile name must be .pem"+Bcolors.ENDC)
            continue
        else:
            break
    while True:
        username = input(Bcolors.ENDC+"EC2 username "+Bcolors.UNDERLINE+username+Bcolors.ENDC+" : ") or username
        if username != "ubuntu":
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"bunker currently only supports ubuntu"+Bcolors.ENDC)
            continue
        else:
            break
    if query_yes_no(Bcolors.PALEYELLOW+"Add Github credentials?"+Bcolors.ENDC, "yes"):
        git_user = input(Bcolors.ENDC+"Github username "+Bcolors.UNDERLINE+git_user+Bcolors.ENDC+" : "+Bcolors.PALEYELLOW) or git_user
        git_pass = input(Bcolors.ENDC+"Github password "+Bcolors.UNDERLINE+git_pass+Bcolors.ENDC+" : "+Bcolors.PALEYELLOW) or git_pass
    if query_yes_no(Bcolors.PALEYELLOW+"Add BitBucket credentials?"+Bcolors.ENDC, "yes"):
        bb_user = input(Bcolors.ENDC+"Github username "+Bcolors.UNDERLINE+bb_user+Bcolors.ENDC+" : "+Bcolors.PALEYELLOW) or bb_user
        bb_pass = input(Bcolors.ENDC+"Github password "+Bcolors.UNDERLINE+bb_pass+Bcolors.ENDC+" : "+Bcolors.PALEYELLOW) or bb_pass
    print(Bcolors.OKGREEN+"bunker is now configured."+Bcolors.ENDC+" writing: "+Bcolors.PALEBLUE+"~/.config-bunker.ini"+Bcolors.ENDC)
    print("if you already have an ec2 created, please run "+Bcolors.PINK+"bunker install"+Bcolors.ENDC)
    newconfig = newconfig.format(prefix=prefix, repos=repofile, ignored=ignorefile, pem=pem, iid=instance_id, username=username, guser=git_user, gpass=git_pass, bbuser=bb_user, bbpass=bb_pass)    
    with open(bunker_config, 'w+') as f:
        f.write(newconfig)
    exit()

if __name__ == "__main__":
    init_bunker()
