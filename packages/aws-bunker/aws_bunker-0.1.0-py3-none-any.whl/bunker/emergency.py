#!/usr/bin/env python

"""emergency uses boto3/ssm to clone all your git repos and then rsync up dot files and configs"""

import configparser
import sys
import os
from os.path import expanduser
import signal
import time
import subprocess
import boto3

#parser = argparse.ArgumentParser(description='back up git repos to ec2', prog='emergency', formatter_class=RawTextHelpFormatter)

#parser.print_help()
#parser.add_argument('-l', action='store_true', help='leave ec2 running.')
#parser.add_argument('-s', action='store_true', help='skip startup.')
#parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
#args = parser.parse_args()
#running = args.l
#skipstart = args.s


class Bcolors:
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

def signal_handler(sig, frame):
    print('\nuser cancelled. halt and catch fire.')
    if not running:
        stop = subprocess.run("aws ec2 stop-instances --instance-ids "+instance_id, shell=True, stdout=subprocess.PIPE)
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

def countdown(num):
    while num > 0:
        fmtnum = str(num)
        if num < 10:
            fmtnum = "0"+str(num)
        print(fmtnum, end="\r", flush=True)
        num -= 1
        time.sleep(1)
    return

def emergency(running=None, skipstart=None):
    """clone git repos on ec2, then copy over ignored files"""
    #config here
    home = expanduser('~')
    bunker_config = os.path.join(home, ".config-bunker.ini")
    config = configparser.ConfigParser()
    config.read(bunker_config)

    prefix = config['default']['prefix']
    repos = prefix+config['default']['repos']
    ignored = prefix+config['default']['ignored']
    pem = config['default']['pem']
    instance_id = config['default']['instance_id']
    username = config['default']['username']
    git_user = config['default']['git_user']
    git_pass = config['default']['git_pass']
    git_auth = git_user+":"+git_pass
    bb_user = config['default']['bb_user']
    bb_pass = config['default']['bb_pass']
    bb_auth = bb_user+":"+bb_pass

    client = boto3.client('ec2')
    ssm_client = boto3.client('ssm')

    if not skipstart:
        print(Bcolors.ENDC+"starting emergency ec2 and waiting for \"running\" state...")
        client.start_instances(InstanceIds=[instance_id])
        waiter = client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
    else:
        print(Bcolors.ENDC+"skipping startup...")

    instance_ip = subprocess.run("aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text", shell=True, stdout=subprocess.PIPE)
    instance_ip = instance_ip.stdout.decode('utf-8')
    instance_ip = instance_ip.strip(' \t\n\r')
    if not skipstart:
        state = 0
        trigger = 0
        while state != 16:
            if trigger > 0:
                print("...")
            else:
                trigger = 666
            state = subprocess.run("aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].State.Code' --output text", shell=True, stdout=subprocess.PIPE)
            state = state.stdout.decode('utf-8')
            state = int(state)
            time.sleep(1)
        countdown(20)
        print("instance up: "+str(instance_ip))
    else:
        state = 0
        state = subprocess.run("aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].State.Code' --output text", shell=True, stdout=subprocess.PIPE)
        state = state.stdout.decode('utf-8')
        state = int(state)
        if state != 16:
            print(Bcolors.RED+"instance is not running."+Bcolors.ENDC)
            if not running:
                stop = subprocess.run("aws ec2 stop-instances --instance-ids "+instance_id, shell=True, stdout=subprocess.PIPE)
            exit()
    # INSTANCE READY FOR WORK, DO STUFF
    if query_yes_no("ready to transfer to "+instance_ip+"?", "yes"):
        dirs = []
        with open(repos, 'r') as f:
            for line in f:
                repo = line.strip()
                dirs.append(repo)
        outputs = {}
        for d in dirs:
            gitconfig = d+"/.git/config"
            catcher = False
            # getting repo url from .git/config
            with open(gitconfig, 'r') as gconfig:
                for line in gconfig:
                    if catcher:
                        repourl = line
                        break
                    if "[remote \"origin\"]" in line:
                        catcher = True
            repourl = repourl.strip(' \t\n\r')
            repoarr = repourl.split(" = ")
            repourl = repoarr[1]
            response = ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': ['ls /home/'+username+'/'+d]}, )
            check_id = response['Command']['CommandId']
            # wait for response
            time.sleep(1)
            checkoutput = ssm_client.get_command_invocation(
                CommandId=check_id,
                InstanceId=instance_id,
            )
            while checkoutput['Status'] != "Success" and checkoutput['Status'] != "Failed":
                time.sleep(1)
                checkoutput = ssm_client.get_command_invocation(
                    CommandId=check_id,
                    InstanceId=instance_id,
                )
            if checkoutput['Status'] != "Success":
                #print(repourl)
                if "github" in repourl:
                    authstr = git_auth
                    authuser = git_user
                else:
                    authstr = bb_auth
                    authuser = bb_user

                if authuser in repourl:
                    repourl = repourl.replace(authuser, authstr, 1)
                else:
                    repoarr = repourl.split("//")
                    repourl = repoarr[0]+"//"+authstr+"@"+repoarr[1]
                #print("after: "+repourl)
                response = ssm_client.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={'commands': ['git clone '+repourl+' /home/'+username+'/'+d, 'chown -R '+username+':'+username+' /home/'+username+'/'+d]}, )
                command_id = response['Command']['CommandId']
                outputs[command_id] = 'git clone '+repourl+' /home/'+username+'/'+d
                print(Bcolors.YELLOW+"cloning repo: "+d+Bcolors.ENDC)
                time.sleep(1)
            else:
                print(Bcolors.OKGREEN+"repo exists: "+d+Bcolors.ENDC)
        for key, value in outputs.items():
            cmdoutput = ssm_client.get_command_invocation(
                CommandId=key,
                InstanceId=instance_id,
            )
            if cmdoutput['Status'] != "Success":
                print(Bcolors.RED+"Warning - "+Bcolors.YELLOW+value+Bcolors.ENDC)
                print(Bcolors.RED+"Command output ===\n"+Bcolors.YELLOW+cmdoutput['StandardErrorContent']+Bcolors.ENDC)
                print(Bcolors.RED+'===\nCloning Repo: '+cmdoutput['Status']+". "+Bcolors.YELLOW+"We will still attemp to rsync files"+Bcolors.ENDC)
        #
        #
        # backup hidden files and configs below
        #
        #
        print("cleaning up...")
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ['chown -R '+username+':'+username+' /home/'+username]}, )
        command_id = response['Command']['CommandId']
        time.sleep(1)
        files = []
        with open(ignored, 'r') as f:
            for line in f:
                ignore = line.strip()
                files.append(ignore)
        for d in dirs:
            os.chdir(d)
            print(Bcolors.OKGREEN+"\n - ", d+"\n"+Bcolors.ENDC)
            for i in files:
                exists = subprocess.run("find . -name '"+i+"'", shell=True, stdout=subprocess.PIPE)
                exists = exists.stdout.decode('utf-8')
                if len(exists) > 1:
                    print(Bcolors.YELLOW+i+Bcolors.ENDC)
                    os.system("find . -name '"+i+"' | xargs -n1 -J % rsync -Ravze 'ssh -i "+pem+"' % "+username+"@"+instance_ip+":/home/"+username+"/"+d)
    else:
        if not running:
            stop = subprocess.run("aws ec2 stop-instances --instance-ids "+instance_id, shell=True, stdout=subprocess.PIPE)
        print("\nshutting down")
        exit()
    
    print(Bcolors.CYAN+"\nshutting down: "+instance_ip+Bcolors.ENDC)
    if not running:
        stop = subprocess.run("aws ec2 stop-instances --instance-ids "+instance_id, shell=True, stdout=subprocess.PIPE)
    return

if __name__ == "__main__":
    emergency()
