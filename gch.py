#!/usr/bin/env python
"""
==================
Git Commit Handler
==================
"""

import sys, subprocess as sp
from os import path, chdir
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
    def WARNING(string=None):
        print(f'\n\033[91m>> WARNING!\033[0m\n{string}')
    def EXECUTE(command, run=False):
        print(f'\033[94m>> EXECUTE: {command}\033[0m')
        if run == True:
            sp.call(command, shell=True)

# Generates selection list and answering sequence
def getAnswer(lst):
    while(1):
        [print(f'{idx+1}: {option}') for idx, option in enumerate(lst)]
        answer = input('Answer: ')
        if answer.isdigit():
            if int(answer) > 0 and int(answer) <= len(lst):
                break
            else:
                issues.WARNING('Please choose right answer from below:')
        else:
            issues.WARNING('Please choose right answer from below:')
    return int(answer)

def Commit():
    ''' Commit '''
    commit_message = input('Commit Message: ')
    issues.EXECUTE(f'git commit -m "{commit_message}"', run=True)

def getCurrentBranch(lst=False):
    ''' Returns current branch name '''
    l = sp.getoutput('git branch').split('\n')
    current_branch = ''.join(branch[2:] for branch in l if branch[0]=='*')
    branch_list = [branch[2:] for branch in l]
    if lst:
        return current_branch, branch_list
    else:
        return current_branch

def setCheckout(branch, current_branch, filepath):
    ''' Handles Checkout Matters '''
    if not isExist(f'git status --short'):
        issues.EXECUTE(f'git checkout {branch}', run=True)
    else:
        print(f'Theres some changes in {current_branch}')
        qs =     [f'Commit changes of `{current_branch}`']
        qs.append(f'Stash changes of `{current_branch}`')
        qs.append(f'Force Checkout to `{branch}`')
        answer = getAnswer(qs)
        if answer == 1:
            issues.EXECUTE(f'git add {filepath}', run=True)
            Commit()
            issues.EXECUTE(f'git checkout {branch}', run=True)
        elif answer == 2:
            issues.EXECUTE(f'git stash', run=True)
            issues.EXECUTE(f'git checkout {branch}', run=True)
        else:
            issues.EXECUTE(f'git checkout -f {branch}', run=True)

def setBranch(branch, filepath):
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
        print(f'Currently on `{current_branch}` but tried to commit to `{branch}`.')
        qs =     [f'Merge `{current_branch}` => `{branch}`']
        qs.append(f'Stay on `{current_branch}`')
        qs.append(f'Checkout to `{branch}`')
        answer = getAnswer(qs)
        if answer == 1:
            setCheckout(branch, current_branch, filepath)
            issues.EXECUTE(f'git merge {current_branch}', run=True)
        elif answer == 2:
            print(f'commiting branch set to {current_branch}')
            branch = current_branch
        else:
            setCheckout(branch, current_branch, filepath)
    return branch

def isGitExist(gitpath):
    gitfolder = path.join(gitpath, '.git')
    flag = True if path.exists(gitfolder) else False
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
def main(gitpath, filepath, branch, push, detail, log, commit):

    #conversion to absolute path
    gitpath = path.abspath(gitpath)
    filepath = path.abspath(filepath)

    chdir(gitpath)

    if not isGitExist(gitpath):
        issues.WARNING()
        print(f'It seems path:`{gitpath}` does not have `.git` folder')
        answer = getAnswer([f'Initialize `.git` folder'])
        issues.EXECUTE('git init', run=True)

    issues.EXECUTE('git status --short', run=True)

    if log:
        issues.EXECUTE('git log --stat --oneline --graph --decorate', run=True)
        sys.exit()

    if isExist('git branch'):
        current_branch = getCurrentBranch()
        if current_branch != branch:
            issues.BRANCH()
            branch = setBranch(branch, filepath)
        
    # Commit or not
    if isExist(f'git status --short'):
        issues.EXECUTE(f'git diff --stat', run=True)
        issues.EXECUTE(f'git add -n {filepath}', run=True)
        if detail:
            issues.EXECUTE(f'git diff --cached --ignore-all-space --ignore-blank-lines', run=True)
        if commit:
            issues.EXECUTE(f'git add {filepath}', run=True)
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


if __name__ == "__main__":
    main()
