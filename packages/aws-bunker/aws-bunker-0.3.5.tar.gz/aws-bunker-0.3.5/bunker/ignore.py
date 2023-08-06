#!/usr/bin/env python

"""add or remove file from ignores file"""

import configparser
import sys
import os
from os.path import expanduser
import subprocess

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
    GOLD = '\033[38;5;178m'

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

def ignore(ignores, yes=None, backup=None):
    """add or remove file from ignores"""
    #config here
    home = expanduser('~')
    bunker_config = os.path.join(home, ".config-bunker.ini")
    config_exists = False
    if os.path.exists(bunker_config):
        config = configparser.ConfigParser()
        config.read(bunker_config)
        config_exists = True
        prefix = config['default']['prefix']
        ignore_file = config['default']['ignored']
    else:
        print(Bcolors.PALEYELLOW+"no config file found."+Bcolors.ENDC)
        print("please run: "+Bcolors.PINK+"bunker init"+Bcolors.ENDC)
        print()
        exit()
    # read ignore file into array
    if os.path.exists(prefix+ignore_file):
        with open(prefix+ignore_file) as f:
            ignorefile_arr = f.readlines()
        ignorefile_arr = [x.strip() for x in ignorefile_arr]
    else:
        ignorefile_arr = []
    # loop sanitized list and add and remove items ass needed
    for r in ignores:
        if r in ignorefile_arr:
            if yes or query_yes_no("remove "+Bcolors.PALEYELLOW+r+Bcolors.ENDC+" from "+Bcolors.PALEBLUE+ignore_file+"?"+Bcolors.ENDC, default="yes"):
                ignorefile_arr.remove(r)
                print(Bcolors.FAIL+r+Bcolors.ENDC)
        else:
            ignorefile_arr.append(r)
            print(Bcolors.OKGREEN+r+Bcolors.ENDC)
    # finally, backup and over-write editted array to ignore file
    if backup:
        backup_ignore = prefix+ignore_file+".bak"
        print(Bcolors.PALEBLUE+"backing up ignore file to: "+Bcolors.PALEYELLOW+backup_ignore+Bcolors.ENDC)
        bcmd = "cp "+prefix+ignore_file+" "+backup_ignore
        subprocess.call(bcmd, shell=True)
    newif = ""
    print()
    print(Bcolors.OKGREEN+"over-writing "+ignore_file+Bcolors.ENDC)
    for r in ignorefile_arr:
        newif += r+"\n"
    f = open(prefix+ignore_file, "w+")
    f.write(newif)
    f.close()

if __name__ == "__main__":
    ignore()
