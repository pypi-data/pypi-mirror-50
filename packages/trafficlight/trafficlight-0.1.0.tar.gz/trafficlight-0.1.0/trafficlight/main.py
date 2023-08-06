#!/usr/bin/env python

"""start or stop (depending on current state) ec2 instances with tag Name:example"""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
import signal
import json
import subprocess
import pkg_resources

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

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None

def main():
    '''starts and stops ec2 instances with tag names.'''
    version = pkg_resources.require("trafficlight")[0].version
    parser = argparse.ArgumentParser(
        description='start or stop (depending on current state) ec2 instances with tag Name:example',
        prog='trafficlight',
        formatter_class=rawtxt
    )

    #parser.print_help()
    parser.add_argument(
        "tag",
        help="""starts and stops ec2 instances with tag names.\n\n
    $ trafficlight example\n
    where example is the value for the tag with key Name""",
        nargs='?',
        default='none'
    )
    parser.add_argument('--key', help="optional. use a tag key besides Name", default="Name")
    parser.add_argument('-g', '--green', action='store_true', help='start all.')
    parser.add_argument('-r', '--red', action='store_true', help='stop all.')
    parser.add_argument('-y', '--yes', action='store_true', help='automatically approve instance state change.')
    parser.add_argument('-H', '--host', action='store_true', help='use hostnames instead of ip addresses.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()
    tag = args.tag
    key = args.key
    green = args.green
    red = args.red
    host = args.host
    yes = args.yes
    do_nothing = False
    # check for aws
    if not is_tool("aws"):
        print(Bcolors.WARNING+"this program requires aws cli"+Bcolors.ENDC)
        print("to install it run "+Bcolors.MAGENTA+"pip3 install awscli --upgrade --user"+Bcolors.ENDC)
        exit()
    # error checking for both stop and start and no flags.
    if green and red:
        print(Bcolors.WARNING+"you cannot both start and stop.")
        print(Bcolors.ENDC+"either "+Bcolors.OKGREEN+"--green"+Bcolors.ENDC+" to start instances or "+Bcolors.RED+"--red"+Bcolors.ENDC+" to stop.")
        print("omit the flag to "+Bcolors.OKGREEN+"green light"+Bcolors.ENDC+" stopped instances and "+Bcolors.RED+"red light"+Bcolors.ENDC+" running instances.")
        exit()
    print(Bcolors.ENDC+"checking for instances...")
    if tag == "none":
        cmd = "aws ec2 describe-instances --output json"
        instances = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        if not red and not green:
            do_nothing = True
    else:
        cmd = "aws ec2 describe-instances --filters 'Name=tag:{},Values={}' --output json"
        instances = subprocess.check_output(cmd.format(key, tag), shell=True).decode("utf-8").strip()
    instances = json.loads(instances)
    instances = instances['Reservations']
    number_of_instances = len(instances)
    if number_of_instances == 0:
        print(Bcolors.WARNING+"no instances found."+Bcolors.ENDC)
        exit()
    state_code = 0
    for instance in instances:
        instance_id = instance['Instances'][0]['InstanceId']
        state_code = instance['Instances'][0]['State']['Code']
        state_name = instance['Instances'][0]['State']['Name']
        instance_type = instance['Instances'][0]['InstanceType']
        try:
            instance_tags = instance['Instances'][0]['Tags']
        except KeyError as e:
            instance_tags = ""
        tags_list = ""
        for instance_tag in instance_tags:
            tags_list += instance_tag['Key']+":"+instance_tag['Value']+", "
        tags_list = tags_list[:-2]
        if state_code == 16:
            state_color = Bcolors.OKGREEN
            instance_ip = instance['Instances'][0]['PublicIpAddress']
            instance_host = instance['Instances'][0]['PublicDnsName']
            if host:
                description = instance_id+" - "+instance_type+" - "+instance_host
            else:
                description = instance_id+" - "+instance_type+" - "+instance_ip
        elif state_code == 80:
            state_color = Bcolors.RED
            description = instance_id+" - "+instance_type
        else:
            state_color = Bcolors.WARNING
            description = instance_id+" - "+instance_type
        print(state_color+state_name+"\n"+description+"\nTags: "+tags_list)
        print("-------"+Bcolors.ENDC)
    switch = False
    verbing = False
    if green:
        question = "start instances?"
        switch = "start-instances"
        verb = "started"
        verbing = Bcolors.OKGREEN+"starting"+Bcolors.ENDC
    elif red:
        question = "stop instances?"
        switch = "stop-instances"
        verb = "stopped"
        verbing = Bcolors.RED+"stopping"+Bcolors.ENDC
    else:
        question = "switch instance state?"
        verb = "switched"
    if not do_nothing:
        if yes or query_yes_no(question, "yes"):
            state_code = 0
            tmp_switch = ""
            for instance in instances:
                instance_id = instance['Instances'][0]['InstanceId']
                state_code = instance['Instances'][0]['State']['Code']
                if state_code == 16  or state_code == 80:
                    if state_code == 16:
                        tmp_switch = "stop-instances"
                        tmp_verbing = Bcolors.RED+"stopping"+Bcolors.ENDC
                    else:
                        tmp_switch = "start-instances"
                        tmp_verbing = Bcolors.OKGREEN+"starting"+Bcolors.ENDC
                    if switch:
                        cmd = "aws ec2 "+switch+" --instance-ids "+instance_id
                        run = subprocess.check_output(cmd, shell=True)
                    else:
                        cmd = "aws ec2 "+tmp_switch+" --instance-ids "+instance_id
                        run = subprocess.check_output(cmd, shell=True)
                    if verbing:
                        print(verbing+" "+instance_id)
                    else:
                        print(tmp_verbing+" "+instance_id)
                else:
                    print(Bcolors.WARNING+instance_id+" not in a state to be "+verb+Bcolors.ENDC)

if __name__ == "__main__":
    main()
