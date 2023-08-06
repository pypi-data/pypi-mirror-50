#!/usr/bin/env python

"""init bunker config file"""

import configparser
import sys
import os
from os.path import expanduser
import inquirer

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

def init_bunker(instance_id=None):
    #config here
    home = expanduser('~')
    bunker_config = os.path.join(home, ".config-bunker.ini")
    config_exists = False
    gitkeys_arr = []
    if os.path.exists(bunker_config):
        config = configparser.ConfigParser()
        config.read(bunker_config)
        if "gitkeys" in config['default']:
            config_exists = True
            prefix = config['default']['prefix']
            pem = config['default']['pem']
            if instance_id is None:
                instance_id = config['default']['instance_id']
            username = config['default']['username']
            gitkeys = config['default']['gitkeys']
            keycount = gitkeys.count(', ')
            if keycount > 0:
                gitkeys_arr = config['default']['gitkeys'].split(", ")
            else:
                gitkeys_arr.append(config['default']['gitkeys'])
    if not config_exists:
        print(Bcolors.PALEYELLOW+"deprecated config file or no config file found."+Bcolors.ENDC)
        prefix, pem, instance_id, username, gitkeys = home+"/", "unknown", "unknown", "ubuntu", "unknown"

    newconfig = """[default]
prefix = {prefix}
repos = {repos}
ignored = {ignored}
pem = {pem}
instance_id = {iid}
username = {username}
gitkeys = {gitkeys}
"""
    instance_id = input(Bcolors.ENDC+"EC2 Instance ID ["+Bcolors.UNDERLINE+instance_id+Bcolors.ENDC+"] : "+Bcolors.PALEYELLOW) or instance_id
    while True:
        prefix = input(Bcolors.ENDC+"Directory where you will store repositories file ["+Bcolors.UNDERLINE+prefix+Bcolors.ENDC+"] : "+Bcolors.PALEYELLOW) or prefix
        if not prefix.endswith("/"):
            if config['default']['prefix']:
                prefix = config['default']['prefix']
            else:
                prefix = "unknown"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"prefix must end with a /"+Bcolors.ENDC)
            continue
        elif not os.path.isdir(prefix):
            if config['default']['prefix']:
                prefix = config['default']['prefix']
            else:
                prefix = home+"/"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"directory does not exist"+Bcolors.ENDC)
            continue
        else:
            break
    while True:
        repofile = input(Bcolors.ENDC+"Name of repository file ["+Bcolors.UNDERLINE+"repositories.txt"+Bcolors.ENDC+"] : "+Bcolors.PALEYELLOW) or "repositories.txt"
        if not repofile.endswith(".txt"):
            repofile = "repositories.txt"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"repository filename must be .txt"+Bcolors.ENDC)
            continue
        else:
            break
    while True:
        ignorefile = input(Bcolors.ENDC+"Name of ignored-git-files file ["+Bcolors.UNDERLINE+"ignoredfiles.txt"+Bcolors.ENDC+"] : "+Bcolors.PALEYELLOW) or "ignoredfiles.txt"
        if not ignorefile.endswith(".txt"):
            ignorefile = "ignoredfiles.txt"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"ignored filename must be .txt"+Bcolors.ENDC)
            continue
        else:
            break
    while True:
        pem = input(Bcolors.ENDC+"Full path to .pem keyfile ["+Bcolors.UNDERLINE+pem+Bcolors.ENDC+"] : "+Bcolors.PALEYELLOW) or pem
        if not pem.endswith(".pem"):
            if config['default']['pem']:
                pem = config['default']['pem']
            else:
                pem = "unknown"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"keyfile name must be .pem"+Bcolors.ENDC)
            continue
        elif not os.path.isfile(pem):
            if config['default']['pem']:
                pem = config['default']['pem']
            else:
                pem = "unknown"
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"file does not exist"+Bcolors.ENDC)
            continue
        else:
            break
    while True:
        username = input(Bcolors.ENDC+"EC2 username ["+Bcolors.UNDERLINE+username+Bcolors.ENDC+"] : ") or username
        if username != "ubuntu":
            print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"bunker currently only supports ubuntu"+Bcolors.ENDC)
            continue
        else:
            break
    
    f = []
    d = []
    for root, dirs, files in os.walk(os.path.join(home, ".ssh"), topdown=False):
        for name in files:
            if ".pub" in name:
                name = name.replace(".pub", "")
                if os.path.join(root, name) in gitkeys_arr:
                    d.append(os.path.join(root, name))
                f.append(os.path.join(root, name))
    questions = [inquirer.Checkbox(
        'keyfiles',
        message="Select key files (use arrow keys) to copy to the EC2.\n"+Bcolors.GOLD+"NOTE: "+Bcolors.ENDC+"Select only keys you need for access to your git provider(s)",
        choices=f,
        default=d,
    )]
    answers = inquirer.prompt(questions)  # returns a dict
    if len(answers['keyfiles']) < 1:
        print(Bcolors.FAIL+"WARNING: "+Bcolors.WARNING+"you did not select a key file, so bunker build will not be able to clone your git repos."+Bcolors.ENDC)
        print("if this was not your intention, please re-run: "+Bcolors.PINK+"bunker init"+Bcolors.ENDC)
        newkeyfiles = []
    else:
        newkeyfiles = answers['keyfiles']
    newgitkeys = ""
    for item in newkeyfiles:
        newgitkeys += item+", "
    newgitkeys = newgitkeys[:-2]
    print(Bcolors.OKGREEN+"bunker is now configured."+Bcolors.ENDC+" writing: "+Bcolors.PALEBLUE+"~/.config-bunker.ini"+Bcolors.ENDC)
    print("if your ec2 is up and running, try: "+Bcolors.PINK+"bunker install"+Bcolors.ENDC)
    newconfig = newconfig.format(prefix=prefix, repos=repofile, ignored=ignorefile, pem=pem, iid=instance_id, username=username, gitkeys=newgitkeys) 
    with open(bunker_config, 'w+') as f:
        f.write(newconfig)
    exit()

if __name__ == "__main__":
    init_bunker()
