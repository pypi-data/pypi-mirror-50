#!/usr/bin/env python

""" simple git commits """

import argparse
from argparse import RawTextHelpFormatter
import sys
import os
import subprocess
import signal
import time
import inquirer
import pkg_resources

def signal_handler(sig, frame):
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

Colors = {
    'CYAN': '\033[96m',
    'MAGENTA': '\033[95m',
    'GREY': '\033[90m',
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[33m',
    'RED': '\033[31m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'ORANGE': '\033[38;5;208m',
    'PINK': '\033[38;5;212m',
    'PALEYELLOW': '\033[38;5;228m',
    'PALEBLUE': '\033[38;5;111m',
    'GOLD': '\033[38;5;178m'
}
def cs(string, color):
    color_upper = color.upper()
    if color_upper not in Colors:
        return string
    else:
        string = Colors[color_upper]+string+Colors['ENDC']
        return string

def main():
    """simple git commits"""
    version = pkg_resources.require("git-client")[0].version
    parser = argparse.ArgumentParser(description="simple git client\n"+bytes.decode(b'\xF0\x9F\x9A\xA7', 'utf8')+cs(" under construction. version: {} ".format(version), "paleyellow")+bytes.decode(b'\xF0\x9F\x9A\xA7', 'utf8'), prog='gc', formatter_class=RawTextHelpFormatter)
    #parser.print_help()
    parser.add_argument("subject", help="the subject message you want to commit with.\n\nexample: $ gc added state var to file.js", nargs='+')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s'+version)
    args = parser.parse_args()
    message = ""
    for item in args.subject:
        message += item+" "
    os.system("git status -u")
    print(cs("========", "grey"))
    op = subprocess.check_output("git status -u", shell=True).decode("utf-8")
    if "nothing to commit, working tree clean" in op:
        exit()
    if query_yes_no("Commit?", "yes"):
        fullcmd = "git commit -m \""+message+"\""
        git_root = subprocess.check_output("git rev-parse --show-toplevel", shell=True).decode("utf-8").strip()
        os.chdir(git_root)
        print("Subject: "+cs(message, "pink"))
        if query_yes_no("Add body?", "yes"):
            print(cs("Type below, finish by hitting enter twice:", "gold"))
            lines = []
            while True:
                line = input("> ")
                if line:
                    lines.append(line)
                else:
                    break
            if lines:
                fullcmd += " -m "
                for l in lines:
                    fullcmd += "\""+l+"\"$'\\n'"
        untracked = subprocess.check_output("git ls-files . --exclude-standard --others --modified", shell=True).decode("utf-8")
        if untracked:
            sani_tracked = []
            for ut in untracked.split("\n"):
                if ut:
                    sani_tracked.append(ut)
            questions = [inquirer.Checkbox(
                'untracked or modified files',
                message="Use arrow keys to unselect any untracked files you DON'T want to add.",
                choices=sani_tracked,
                default=sani_tracked,
            )]  
            answers = inquirer.prompt(questions)  # returns a dict
            ufs = answers['untracked or modified files']
            for uf in ufs:
                print(cs("git add "+uf, "green"))
                subprocess.call("git add "+uf, shell=True, stdout=subprocess.PIPE)
            print()
        else:
            print(cs("  No untracked or modified files.", "grey"))
        deleted = subprocess.check_output("git ls-files . --exclude-standard --deleted", shell=True).decode("utf-8")
        if deleted:
            sani_deleted = []
            for d in deleted.split("\n"):
                if d:
                    sani_deleted.append(d)
            questions = [inquirer.Checkbox(
                'deleted files',
                message="Use arrow keys to unselect any deleted files you DON'T want to rm.",
                choices=sani_deleted,
                default=sani_deleted,
            )]  
            answers = inquirer.prompt(questions)  # returns a dict
            ds = answers['deleted files']
            for d in ds:
                print(cs("git rm "+d, "red"))
                subprocess.call("git rm "+d, shell=True, stdout=subprocess.PIPE)
            print()
        else:
            print(cs("  No deleted files.", "grey"))
        print("Committing...")
        time.sleep(1)
        print(fullcmd)
        os.system(fullcmd)
        if query_yes_no("Push?", "yes"):
            print("Pushing...")
            os.system("git push")
        else:
            print(cs("Leaving without a push!", "warning"))

if __name__ == "__main__":
    main()
