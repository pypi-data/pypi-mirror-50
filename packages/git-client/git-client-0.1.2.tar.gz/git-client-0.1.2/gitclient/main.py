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

#from ignore import ignore
from .ignore import ignore

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

COLORS = {
    'CYAN': '\033[96m',
    'MAGENTA': '\033[95m',
    'GREY': '\033[90m',
    'LIGHTGREY': '\033[38;5;248m',
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
    if color_upper not in COLORS:
        return string
    else:
        string = COLORS[color_upper]+string+COLORS['ENDC']
        return string

def si():
    try:
        git_root = subprocess.check_output("git rev-parse --show-toplevel", shell=True).decode("utf-8").strip()
        os.chdir(git_root)
    except:
        print(cs("You don't appear to be in a git repo.", "warning"))
        exit()
    print(cs("=== .gitignore ===", "grey"))
    with open(git_root+'/.gitignore', 'r') as f:
        print(f.read())
        exit()

def main():
    """simple git commits"""
    
    version = pkg_resources.require("git-client")[0].version
    parser = argparse.ArgumentParser(
        description="simple git client\n"+bytes.decode(b'\xF0\x9F\x9A\xA7', 'utf8')+cs(" under construction. version: {} ".format(version), "paleyellow")+bytes.decode(b'\xF0\x9F\x9A\xA7', 'utf8'), 
        prog='gc', 
        formatter_class=RawTextHelpFormatter
    )
    #parser.print_help()
    parser.add_argument("subject", help="the subject message you want to commit with.\n\nexample: $ gc added state var to file.js", nargs="?")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    parser.add_argument('-y', '--yes', action='store_true', help='approve all prompts as yes.')
    parser.add_argument('-I', '--showignore', action='store_true', help='print the current .gitignore, and exit.')
    parser.add_argument('-i', '--ignore', nargs='+', help='a list of filenames to add or remove to/from the ignore file. requires at least one file to ignore.')
    parser.add_argument('-b', '--backup', action='store_true', help='backup .gitignore file before over-writing.\nused in combinatoin with --ignore. '+cs("(otherwise this flag is ignored)", "lightgrey"))
    args = parser.parse_args()
    ignores = args.ignore
    show_ignore = args.showignore
    yes = args.yes

    if ignores is None and not show_ignore:
        message = ""
        for item in args.subject.split(" "):
            message += item+" "
        message = message[:-1]
        os.system("git status -u")
        print(cs("========", "grey"))
        op = subprocess.check_output("git status -u", shell=True).decode("utf-8")
        if "nothing to commit, working tree clean" in op:
            exit()
        if yes or query_yes_no("Commit?", "yes"):
            fullcmd = "git commit -m \""+message+"\""
            git_root = subprocess.check_output("git rev-parse --show-toplevel", shell=True).decode("utf-8").strip()
            os.chdir(git_root)
            print("Subject: "+cs(message, "pink"))
            if yes or query_yes_no("Add body?", "yes"):
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
            # UNTRACKED FILES
            untracked = subprocess.check_output("git ls-files . --exclude-standard --others --modified", shell=True).decode("utf-8")
            if untracked:
                sani_tracked = []
                for ut in untracked.split("\n"):
                    if ut:
                        sani_tracked.append(ut)
                deleted = subprocess.check_output("git ls-files . --exclude-standard --deleted", shell=True).decode("utf-8")
                sani_deleted = []
                if deleted:
                    for d in deleted.split("\n"):
                        if d:
                            sani_deleted.append(d)
                questions = [inquirer.Checkbox(
                    'untracked or modified files',
                    message="Use arrow keys to unselect any untracked files you DON'T want to add or rm",
                    choices=sani_tracked,
                    default=sani_tracked,
                )]  
                answers = inquirer.prompt(questions)  # returns a dict
                ufs = answers['untracked or modified files']
                for uf in ufs:
                    if uf in sani_deleted:
                        print(cs("git rm "+uf, "red"))
                        subprocess.call("git rm "+uf, shell=True, stdout=subprocess.PIPE)
                    else:
                        print(cs("git add "+uf, "green"))
                        subprocess.call("git add "+uf, shell=True, stdout=subprocess.PIPE)
                print()
            else:
                print(cs("  No untracked or modified files.", "grey"))
            print("Committing...")
            time.sleep(1)
            #print(fullcmd)
            os.system(fullcmd)
            if yes or query_yes_no("Push?", "yes"):
                print("Pushing...")
                os.system("git push")
            else:
                print(cs("Leaving without a push!", "warning"))
    else:
        # ignore flag 
        if show_ignore:
            si()
        else:
            backup = args.backup
            ignore(ignores, yes, backup)

if __name__ == "__main__":
    main()
