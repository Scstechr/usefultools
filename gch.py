#!/usr/bin/env python
"""
==================
Git Commit Handler
==================
"""

import os, sys, subprocess as sp
try:
    import click
except ImportError:
    print('execute `pip install -r requirements.txt`')

# Print w/ color and run shell commands in EXECUTE
class issues:
    def BRANCH():
        print(f'\n\033[93m>> BRANCH ISSUE!\033[0m')
    def ABORT():
        print(f'\n\033[91m>> ABORT!\033[0m')
    def WARNING():
        print(f'\n\033[91m>> WARNING!\033[0m')
    def EXECUTE(command, run=False):
        print(f'\033[94m>> EXECUTE: {command}\033[0m')
        if run == True:
            sp.call(command, shell=True)

# Generates selection list and answering sequence
def getAnswer(lst):
    # Adds Abort as a option
    lst.append('Abort')
    while(1):
        [print(f'{idx+1}: {option}') for idx, option in enumerate(lst)]
        answer = input('Answer: ')
        if answer.isdigit():
            answer = int(answer)
            if answer > 0 and answer < len(lst):
                break;
            elif answer == len(lst):
                issues.ABORT()
                sys.exit(0)
            else:
                issues.WARNING()
                print('Please choose right answer from below:')
        else:
            issues.WARNING()
            print('Please choose right answer from below:')
    return answer

def Commit():
    ''' Commit '''
    commit_message = input('Commit Message: ')
    issues.EXECUTE(f'git commit -m "{commit_message}"', run=True)

def isStatusClean():
    ''' Checks for any modified/new/deleted files since last commit '''
    status_list = [status for status in sp.getoutput(f'git status').split('\n')\
                                                         if status[0:1] =='\t']
    status = True if len(status_list) == 0 else False
    return status

def getCurrentBranch(lst=False):
    ''' Returns current branch name '''
    l = sp.getoutput('git branch').split('\n')
    current_branch = ''.join(branch[2:] for branch in l if branch[0]=='*')
    branch_list = [branch[2:] for branch in l]
    if lst:
        return current_branch, branch_list
    else:
        return current_branch

def setCheckout(branch, current_branch, filepath, detail):
    ''' Handles Checkout Matters '''
    if isStatusClean():
        issues.EXECUTE(f'git checkout {branch}', run=True)
    else:
        print(f'Theres some changes in {current_branch}')
        answer_2 = getAnswer([f'Commit changes of `{current_branch}`', \
                              f'Stash changes of `{current_branch}`', \
                              f'Force Checkout to `{branch}`', ])
        if answer_2 == 1:
            issues.EXECUTE(f'git add {filepath}', run=True)
            Commit(detail)
            issues.EXECUTE(f'git checkout {branch}', run=True)
        elif answer_2 == 2:
            issues.EXECUTE(f'git stash', run=True)
            issues.EXECUTE(f'git checkout {branch}', run=True)
        else:
            issues.EXECUTE(f'git checkout -f {branch}', run=True)

def setBranch(branch, filepath, detail):
    current_branch, branch_list = getCurrentBranch(lst=True)
    if branch not in branch_list:
        print(f'Branch `{branch}` not found.')
        answer = getAnswer([f'Make new branch `{branch}`',\
                            f'Stay on current branch `{current_branch}`'])
        if answer == 1:
            issues.EXECUTE(f'git checkout -b {branch}', run=True)
        else:
            print(f'commiting branch set to {current_branch}')
            branch = current_branch
    else:
        print(f'Currently on branch `{current_branch}` but commiting branch is set to `{branch}`.')
        answer = getAnswer([f'Merge branch `{current_branch}` -> `{branch}`', \
                            f'Stay on branch `{current_branch}`',\
                            f'Checkout to branch `{branch}`'])
        if answer == 1:
            setCheckout(branch, current_branch, filepath, detail)
            issues.EXECUTE(f'git merge {current_branch}', run=True)
        elif answer == 2:
            print(f'commiting branch set to {current_branch}')
            branch = current_branch
        else:
            pass
    return branch

def isGitExist(gitpath):
    gitfolder = os.path.join(gitpath, '.git')
    flag = True if os.path.exists(gitfolder) else False
    return flag

def isExist(command):
    output = sp.getoutput(command)
    flag = False if len(output) == 0 else True
    return flag

# Explanation of the options showed in --help flag
exp_g = 'Path of .git folder.        => Default: .'
exp_f = 'Path of staging file(s).    => Default: .'
exp_b = 'Commiting branch.           => Default: master'
exp_p = 'Push or not. Flag.          => Default: False'
exp_d = 'Detailed diff. Flag.        => Default: False'
exp_l = 'Git log with option.        => Default: False'
exp_c = 'Commit or not.              => Default: False'

@click.command()
@click.option('-g', '--gitpath', default='.', type=click.Path(exists=True), help=exp_g)
@click.option('-f', '--filepath', default='.', type=click.Path(exists=True), help=exp_f)
@click.option('-b', '--branch', default='master', type=str, help=exp_b)
@click.option('-p', '--push', is_flag='False', help=exp_p)
@click.option('-d', '--detail', is_flag='False', help=exp_d)
@click.option('-l', '--log', is_flag='False', help=exp_l)
@click.option('-c', '--commit', is_flag='False', help=exp_c)
def cmd(gitpath, filepath, branch, push, detail, log, commit):

    #conversion to absolute path
    gitpath = os.path.abspath(gitpath)
    filepath = os.path.abspath(filepath)

    os.chdir(gitpath)
    if log:
        issues.EXECUTE('git log --stat --oneline --graph --decorate', run=True)
        sys.exit()

    if not isGitExist(gitpath):
        issues.WARNING()
        print(f'It seems path:`{gitpath}` does not have `.git` folder')
        answer = getAnswer([f'Initialize `.git` folder'])
        issues.EXECUTE('git init', run=True)

    if isExist('git branch'):
        current_branch = getCurrentBranch()
        if current_branch != branch:
            issues.BRANCH()
            branch = setBranch(branch, filepath, detail)
        
    # Commit or not
    if not isStatusClean():
        issues.EXECUTE(f'git diff --stat', run=True)
        issues.EXECUTE(f'git add {filepath}', run=True)
        if detail:
            issues.EXECUTE(f'git diff --cached --ignore-all-space --ignore-blank-lines', run=True)
        if commit:
            Commit()
    else:
        print('Clean State')

    # Push or not
    if not push:
        print('** no push **')
    elif not isExist(f'git remote -v'):
        print('** no remote repository **')
    else:
        issues.EXECUTE(f'git push -u origin {branch}', run=True)


def main():
    # Title string 
    title =    ' ╔═╗┬┌┬┐  ╔═╗┌─┐┌┬┐┌┬┐┬┌┬┐  ╦ ╦┌─┐┌┐┌┌┬┐┬  ┌─┐┬─┐'
    title += '\n ║ ╦│ │   ║  │ ││││││││ │   ╠═╣├─┤│││ │││  ├┤ ├┬┘'
    title += '\n ╚═╝┴ ┴   ╚═╝└─┘┴ ┴┴ ┴┴ ┴   ╩ ╩┴ ┴┘└┘─┴┘┴─┘└─┘┴└─'

    print(title)
    cmd()


if __name__ == "__main__":
    main()
