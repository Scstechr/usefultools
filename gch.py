# Git Commit Handler

# from standard library
import os, sys
import subprocess as sp

# from outside and own library
import click
import bcolors as bc

class issues:
    def BRANCH():
        print(f'\n{bc.WARNING}>> BRANCH ISSUE!{bc.ENDC}')
    def ABORT():
        print(f'\n{bc.FAIL}>> ABORT!{bc.ENDC}')
    def EXECUTE(command):
        print(f'{bc.OKBLUE}>> EXECUTE: {command}{bc.ENDC}')
        os.system(command)

def cmd():
    issues.BRANCH()
    pass

def main():
    cmd()

if __name__ == "__main__":
    main()

