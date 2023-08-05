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

from .init import init_bunker
from .install import install

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

def bunker():
    """bunker is a command line program for creating a dev/backup ec2 in AWS. It will install software, and clone your git repos, then it will transfer ignored files from your machine to the ec2."""
    version = pkg_resources.require("aws-bunker")[0].version
    parser = argparse.ArgumentParser(
        description='bunker is a command line program for creating a dev/backup ec2 in AWS. It will install software, and clone your git repos, then it will transfer ignored files from your machine to the ec2.',
        prog='bunker',
        formatter_class=rawtxt
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    
    subparsers = parser.add_subparsers(title='subcommands', required=True, dest="subcommand", help='for more info: type `bunker subcommand -h`')
    #parser.print_help()
    
    parser_init = subparsers.add_parser('init', help='init bunker by writing ~/.config-bunker')
    parser_init.set_defaults(func=init_bunker)
    parser_install = subparsers.add_parser('install', help='install essential software')
    parser_install.set_defaults(func=install)
    parser_build = subparsers.add_parser('build', help='clone git repos and copy over ignored files')
    args = parser.parse_args()
    args.func()

if __name__ == "__main__":
    bunker()
