#!/usr/bin/env python

"""source file in .profile. for bash prompts"""

import configparser
import sys
import os
from os.path import expanduser
import json
import time
import subprocess
import boto3

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

def countdown(num):
    while num > 0:
        fmtnum = str(num)
        if num < 10: 
            fmtnum = "0"+str(num)
        print(fmtnum, end="\r", flush=True)
        num -= 1
        time.sleep(1)
    return

def prompt(instance_id=None, dostart=None, yes=None, run=None, bucket_info=None):
    """source file in .profile. for bash prompts"""
    #config here
    home = expanduser('~')
    bunker_config = os.path.join(home, ".config-bunker.ini")
    config = configparser.ConfigParser()
    config.read(bunker_config)

    prefix = config['default']['prefix']
    pem = prefix+config['default']['pem']
    if instance_id is None:
        instance_id = config['default']['instance_id']
    username = config['default']['username']
    client = boto3.client('ec2')
    ssm_client = boto3.client('ssm')
    if dostart:
        print(Bcolors.ENDC+"starting ec2 and waiting for "+Bcolors.OKGREEN+"\"running\""+Bcolors.ENDC+" state...")
        client.start_instances(InstanceIds=[instance_id])
        waiter = client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        countdown(20)
        print("instance up: "+str(instance_id))

    instance_ip = subprocess.run("aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text", shell=True, stdout=subprocess.PIPE)
    instance_ip = instance_ip.stdout.decode('utf-8')
    instance_ip = instance_ip.strip(' \t\n\r')
    state = 0
    state = subprocess.run("aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].State.Code' --output text", shell=True, stdout=subprocess.PIPE)
    state = state.stdout.decode('utf-8')
    state = int(state)
    if state != 16:
        print(Bcolors.RED+"instance is not running."+Bcolors.ENDC)
        exit()
    if run is None:
        print("no script!")
        exit()
    else:
        if not os.path.isabs(run):
            print(Bcolors.PALEYELLOW+"Please use absolute paths to the location of the file on the EC2"+Bcolors.ENDC)
            print("example: "+Bcolors.PALEBLUE+"/home/ubuntu/.prompt.sh"+Bcolors.ENDC)
            exit()
    # INSTANCE READY FOR WORK, DO STUFF
    if yes or query_yes_no("install custom bash prompt with neofetch on: "+instance_ip+"?", "yes"):
        run_exploded = run.split("/")
        rel_run = run_exploded[-1]
        print(Bcolors.GOLD+bytes.decode(b'\xE2\x8F\xB3', 'utf8')+" sourcing "+rel_run+" in ~/.profile"+Bcolors.ENDC)
        if bucket_info != ['none', 'none', 'none'] and bucket_info is not None:
            print(Bcolors.CYAN+"will save output to: "+Bcolors.GOLD+bucket_info[0]+Bcolors.ENDC)
            cmd = "aws ssm send-command --instance-ids \""+instance_id+"\" --document-name \"AWS-RunShellScript\" --output-s3-bucket-name \""+bucket_info[0]+"\" --output-s3-region \""+bucket_info[1]+"\" --output-s3-key-prefix \""+bucket_info[2]+"\" --parameters commands=\"echo source "+run+" | sudo tee -a /home/ubuntu/.profile\""
        else:
            cmd = "aws ssm send-command --instance-ids \""+instance_id+"\" --document-name \"AWS-RunShellScript\" --parameters commands=\"echo source "+run+" | sudo tee -a /home/ubuntu/.profile\""
        ran_command = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        ran_command = json.loads(ran_command)
        command_id = ran_command["Command"]["CommandId"]
        install_status = "InProgress"
        start_time = time.time()
        while install_status == "InProgress":
            elapsed_time = time.time() - start_time
            elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            elapsed_time = str(elapsed_time)
            cmd = "aws ssm list-command-invocations --command-id \""+command_id+"\" --details" 
            ran_command = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            ran_command = json.loads(ran_command)
            install_status = ran_command["CommandInvocations"][0]["Status"]
            if install_status == "InProgress":
                print(Bcolors.WARNING+install_status+Bcolors.GREY+" Time Elapsed: "+Bcolors.ENDC+elapsed_time+"     ", end="\r")
            else:
                if install_status != "Success":
                    color = Bcolors.FAIL
                else:
                    color = Bcolors.OKGREEN
                print(color+install_status+Bcolors.GREY+" Time Elapsed: "+Bcolors.ENDC+elapsed_time+"     ")
        # echo "neofetch" | sudo tee -a /home/ubuntu/.profile
        cmdoutput = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        if cmdoutput['Status'] != "Success":
            time.sleep(1)
            print(Bcolors.GOLD+"running "+rel_run+" returned the following "+Bcolors.FAIL+"error:\n"+Bcolors.WARNING+cmdoutput['StandardErrorContent']+Bcolors.ENDC)

    complete = "complete"
    return complete

if __name__ == "__main__":
    prompt()
