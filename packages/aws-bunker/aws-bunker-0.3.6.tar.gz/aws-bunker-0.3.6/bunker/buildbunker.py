#!/usr/bin/env python

"""buildbunker uses boto3/ssm to clone all your git repos and then rsync up dot files and configs"""

import configparser
import sys
import os
from os.path import expanduser
import time
import subprocess
import boto3

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

def countdown(num):
    while num > 0:
        fmtnum = str(num)
        if num < 10:
            fmtnum = "0"+str(num)
        print(fmtnum, end="\r", flush=True)
        num -= 1
        time.sleep(1)
    return

def buildbunker(running=None, dostart=None, source=None, yes=None):
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
    gitkeys = config['default']['gitkeys']
    gitkeys_arr = []
    keycount = gitkeys.count(', ')
    if keycount > 0:
        gitkeys_arr = config['default']['gitkeys'].split(", ")
    else:
        gitkeys_arr.append(config['default']['gitkeys'])
    # ec2 ssm client
    client = boto3.client('ec2')
    ssm_client = boto3.client('ssm')
    # start up if necessary
    if dostart:
        print(Bcolors.ENDC+"starting ec2 and waiting for \"running\" state...")
        client.start_instances(InstanceIds=[instance_id])
        waiter = client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        countdown(20)
        print("instance up: "+str(instance_id))
    # get ip address
    instance_ip = subprocess.run("aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text", shell=True, stdout=subprocess.PIPE)
    instance_ip = instance_ip.stdout.decode('utf-8')
    instance_ip = instance_ip.strip(' \t\n\r')
    # get instance state
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
    #
    # auf gehts
    if yes or query_yes_no("ready to transfer to "+instance_ip+"?", "yes"):
        dirs = []
        diffs = []
        similarities = []
        if source:
            if source[-1] == "/":
                source = source[:-1]
            dirs.append(source)
        else:
            # build some arrays (dirs, diffs, similarities) to use later
            with open(repos, 'r') as f:
                x = 0
                for line in f:
                    repo = line.strip()
                    if repo[-1] == "/":
                        repo = repo[:-1]
                    dirs.append(repo)
                    exploded_repo = repo.split("/")
                    for directory in exploded_repo:
                        if x == 0 and directory != "":
                            diffs.append(directory)
                        else:
                            if directory in diffs and directory not in similarities:
                                similarities.append(directory)
                    x += 1

        # check for known_hosts
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ['ls /home/'+username+'/.ssh/known_hosts']}, )
        check_id = response['Command']['CommandId']
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
            print(Bcolors.WARNING+"no "+Bcolors.ORANGE+"known_hosts"+Bcolors.WARNING+" in /home/"+username+"/.ssh/"+Bcolors.ENDC)
            print("copy local known_hosts to EC2")
            if os.path.isfile(os.path.join(home, ".ssh", "known_hosts")):
                known_hosts = os.path.join(home, ".ssh", "known_hosts")
                cmd = "scp -i "+pem+" "+known_hosts+" "+username+"@"+instance_ip+":/home/"+username+"/.ssh/"
                print(Bcolors.OKGREEN+cmd+Bcolors.ENDC)
                subprocess.call(cmd, shell=True)
            else:
                print(Bcolors.WARNING+"no known_hosts in ~/.ssh/"+Bcolors.ENDC)
                print("please configure your local ssh to connect to your git providers before using bunker.")
                print()
                exit()

        # check for config
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ['ls /home/'+username+'/.ssh/config']}, )
        check_id = response['Command']['CommandId']
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
            print(Bcolors.WARNING+"no "+Bcolors.ORANGE+"config"+Bcolors.WARNING+" in /home/"+username+"/.ssh/"+Bcolors.ENDC)
            print("copy local config to EC2")
            if os.path.isfile(os.path.join(home, ".ssh", "config")):
                sshconfig = os.path.join(home, ".ssh", "config")
                cmd = "scp -i "+pem+" "+sshconfig+" "+username+"@"+instance_ip+":/home/"+username+"/.ssh/"
                print(Bcolors.OKGREEN+cmd+Bcolors.ENDC)
                subprocess.call(cmd, shell=True)
            else:
                print(Bcolors.WARNING+"no config in ~/.ssh/"+Bcolors.ENDC)
                print("please configure your local ssh to connect to your git providers before using bunker.")
                print()
                exit()

        # check for .ssh/keys
        if gitkeys_arr[0] != "":
            for keyfile in gitkeys_arr:
                exploded = keyfile.split("/")
                kf = exploded[-1]
                response = ssm_client.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={'commands': ['ls /home/'+username+'/.ssh/'+kf]}, )
                check_id = response['Command']['CommandId']
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
                    print(Bcolors.WARNING+"no "+Bcolors.ORANGE+kf+Bcolors.WARNING+" in /home/"+username+"/.ssh/"+Bcolors.ENDC)
                    print("copy local "+kf+" to EC2")
                    cmd = "scp -i "+pem+" "+keyfile+" "+username+"@"+instance_ip+":/home/"+username+"/.ssh/"
                    print(Bcolors.OKGREEN+cmd+Bcolors.ENDC)
                    subprocess.call(cmd, shell=True)

        # declare outputs dict
        outputs = {}
        for d in dirs:
            # loop thru repos (d), check if repo dir exists, then attempt to clone
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
            repourl_arr = repourl.split("/")
            newrepourl = ""
            repo_trigger = False
            for part in repourl_arr:
                if repo_trigger or ".com" in part or ".org" in part:
                    if "@" in part:
                        exp = part.split("@")
                        part = exp[1]
                    if ".com" in part or ".org" in part:
                        newrepourl += part+":"
                    else:
                        newrepourl += part+"/"
                    repo_trigger = True
            repourl = "git@"+newrepourl[:-1]
            exploded_d = d.split("/")
            newd = ""
            for thing in exploded_d:
                if thing not in similarities:
                    newd += thing+"/"
            if newd[0] != "/":
                newd = "/"+newd
            # asdf
            response = ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': ['ls /home/'+username+newd]}, )
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
                response = ssm_client.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={'commands': ['sudo -u '+username+' git clone '+repourl+' /home/'+username+newd, 'chown -R '+username+':'+username+' /home/'+username+newd]}, )
                command_id = response['Command']['CommandId']
                outputs[command_id] = 'sudo -u '+username+' git clone '+repourl+' /home/'+username+newd, 'chown -R '+username+':'+username+' /home/'+username+newd
                print(Bcolors.YELLOW+"cloning repo: "+d+Bcolors.ENDC)
                time.sleep(1)
            else:
                print(Bcolors.OKGREEN+"repo exists: "+newd+Bcolors.ENDC)
                print(Bcolors.GREY+"we should probably pull or something?"+Bcolors.ENDC)
        if len(dirs) < 5:
            print(Bcolors.PALEYELLOW+"waiting for clone."+Bcolors.ENDC)
            countdown(10)
        # loop thru output and print any errors
        for key, value in outputs.items():
            cmdoutput = ssm_client.get_command_invocation(
                CommandId=key,
                InstanceId=instance_id,
            )
            if cmdoutput['Status'] != "Success":
                print(Bcolors.RED+"Warning - "+Bcolors.YELLOW+str(value)+Bcolors.ENDC)
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
            exploded_d = d.split("/")
            newd = ""
            for thing in exploded_d:
                if thing not in similarities:
                    newd += thing+"/"
            if newd[0] != "/":
                newd = "/"+newd
            print(Bcolors.OKGREEN+"\n - ", newd+"\n"+Bcolors.ENDC)
            for i in files:
                exists = subprocess.run("find . -name '"+i+"'", shell=True, stdout=subprocess.PIPE)
                exists = exists.stdout.decode('utf-8')
                if len(exists) > 1:
                    print(Bcolors.YELLOW+i+Bcolors.ENDC)
                    os.system("find . -name '"+i+"' | xargs -n1 -J % rsync -Ravze 'ssh -i "+pem+"' % "+username+"@"+instance_ip+":/home/"+username+newd)
    else:
        if running:
            stop = subprocess.run("aws ec2 stop-instances --instance-ids "+instance_id, shell=True, stdout=subprocess.PIPE)
            print("\nshutting down")
        else:
            print("\nleaving ec2 running")
        exit()
    
    if running:
        stop = subprocess.run("aws ec2 stop-instances --instance-ids "+instance_id, shell=True, stdout=subprocess.PIPE)
        print(Bcolors.CYAN+"\nshutting down: "+instance_ip+Bcolors.ENDC)
    else:
        print(Bcolors.CYAN+"\nleaving "+instance_ip+" running"+Bcolors.ENDC)
    return

if __name__ == "__main__":
    buildbunker()
