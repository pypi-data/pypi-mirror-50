#!/usr/bin/env python

"""bunker is a command line program for creating a development backup ec2 in AWS. It will install software, and clone your git repos, then it will transfer ignored files from your machine to the ec2."""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
import signal
import os
from os.path import expanduser
import shutil
import json
import subprocess
from datetime import datetime
from pathlib import Path
import pkg_resources

#from init import init_bunker
#from install import install
#from extras import extras
#from prompt import prompt
#from emergency import emergency
from .init import init_bunker
from .install import install
from .extras import extras
from .prompt import prompt
from .emergency import emergency

def signal_handler(sig, frame):
    """handle control c"""
    print('\nuser cancelled')
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

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None

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

def bunker():
    """bunker is a command line program for creating a dev/backup ec2 in AWS. It will install software, and clone your git repos, then it will transfer ignored files from your machine to the ec2."""
    version = pkg_resources.require("aws-bunker")[0].version
    parser = argparse.ArgumentParser(
        description='bunker is a command line program for creating a dev/backup ec2 in AWS. It will install software, and clone your git repos, then it will transfer ignored files from your machine to the ec2.',
        prog='bunker',
        formatter_class=rawtxt
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    
    subparsers = parser.add_subparsers(title='subcommands', required=True, dest="subcommand", help="""for more info: type `bunker subcommand -h`

the """+Bcolors.PINK+"""install"""+Bcolors.ENDC+""", """+Bcolors.PINK+"""extra """+Bcolors.ENDC+"""and """+Bcolors.PINK+"""prompt """+Bcolors.ENDC+"""subcommands require custom bash scripts to exist on your EC2. The scripts also need to be executable.
for example scripts please visit the project homepage:
"""+Bcolors.GOLD+"""https://gitlab.com/shindagger/bunker **"""+Bcolors.ENDC)
    #parser.print_help()
    
    parser_init = subparsers.add_parser('init', formatter_class=argparse.RawTextHelpFormatter, help='init bunker by writing ~/.config-bunker', description="init bunker by writing ~/.config-bunker")
    parser_init.set_defaults(func=init_bunker)
    parser_install = subparsers.add_parser('install', formatter_class=argparse.RawTextHelpFormatter, help="""install essential software
"""+Bcolors.GOLD+"""** requires `install-essentials.sh`"""+Bcolors.ENDC, description="""install essential software
requires a file named: """+Bcolors.GOLD+"""`install-essentials.sh`"""+Bcolors.ENDC+""" on the EC2.
the file should be executable """+Bcolors.OKGREEN+"""`chmod a+x install-essentials.sh`"""+Bcolors.ENDC+"""
for example files please visit: """+Bcolors.PALEBLUE+"""https://gitlab.com/shindagger/bunker"""+Bcolors.ENDC)
    parser_install.add_argument('-y', '--yes', action='store_true', help='auto approve installing essentials.')
    parser_install.add_argument('-s', action='store_true', help='startup EC2 first.')
    parser_install.set_defaults(func=install)
    parser_extras = subparsers.add_parser('extra', formatter_class=argparse.RawTextHelpFormatter, help="""install extra software
"""+Bcolors.GOLD+"""** requires `install-extras.sh`"""+Bcolors.ENDC, description="""install extra software.
requires a file named: """+Bcolors.GOLD+"""`install-extras.sh`"""+Bcolors.ENDC+""" on the EC2.
the file should be executable """+Bcolors.OKGREEN+"""`chmod a+x install-extras.sh`"""+Bcolors.ENDC+"""
for example files please visit: """+Bcolors.PALEBLUE+"""https://gitlab.com/shindagger/bunker"""+Bcolors.ENDC)
    parser_extras.add_argument('-y', '--yes', action='store_true', help='auto approve installing extras.')
    parser_extras.add_argument('-s', action='store_true', help='startup EC2 first.')
    parser_extras.set_defaults(func=extras)
    parser_prompt = subparsers.add_parser('prompt', formatter_class=argparse.RawTextHelpFormatter, help="""install a custom bash prompt
"""+Bcolors.GOLD+"""** requires `prompt.sh`"""+Bcolors.ENDC, description="""install a custom bash prompt
requires a file named: """+Bcolors.GOLD+"""`prompt.sh`"""+Bcolors.ENDC+""" on the EC2.
the file should be executable """+Bcolors.OKGREEN+"""`chmod a+x prompt.sh`"""+Bcolors.ENDC+"""
for example files please visit: """+Bcolors.PALEBLUE+"""https://gitlab.com/shindagger/bunker"""+Bcolors.ENDC)
    parser_prompt.add_argument('-y', '--yes', action='store_true', help='auto approve customizing bash prompt.')
    parser_prompt.add_argument('-s', action='store_true', help='startup EC2 first.')
    parser_prompt.set_defaults(func=prompt)
    parser_build = subparsers.add_parser('build', help='clone git repos and copy over ignored files', description="clone git repos and copy over ignored files")
    parser_build.add_argument('-y', '--yes', action='store_true', help='auto approve cloning repos and backing up files.')
    parser_build.add_argument('-S', action='store_true', help='stop EC2 after running.')
    parser_build.add_argument('-s', action='store_true', help='startup EC2 first.')
    parser_build.add_argument('-r', '--repo', help='Source directory to be duplicated to remote bunker')
    parser_build.set_defaults(func=emergency)
    args = parser.parse_args()
    if args.subcommand == 'build':
        yes = args.yes
        running = args.S
        dostart = args.s
        source = args.repo
        args.func(running, dostart, source, yes)
    elif args.subcommand == 'install':
        yes = args.yes
        dostart = args.s
        args.func(dostart=dostart, yes=yes)
    elif args.subcommand == 'extra':
        yes = args.yes
        dostart = args.s
        args.func(dostart=dostart, yes=yes)
    elif args.subcommand == 'prompt':
        yes = args.yes
        dostart = args.s
        args.func(dostart=dostart, yes=yes)
    else:
        args.func()

if __name__ == "__main__":
    bunker()
