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
    def EXECUTE(command, run=False):
        print(f'{bc.OKBLUE}>> EXECUTE: {command}{bc.ENDC}')
        if run:
            os.system(command)

def getCurrentBranch():
    ''' Returns current branch name '''
    l = sp.getoutput('git branch').split('\n')
    current_branch = ''.join(branch[2:] for branch in l if branch[0]=='*')
    branch_list = [branch[2:] for branch in l]
    return current_branch, branch_list

def cmd():
    issues.BRANCH()
    current_branch, branch_list = getCurrentBranch()
    print(current_branch)
    pass

def main():
    cmd()

if __name__ == "__main__":
    main()

