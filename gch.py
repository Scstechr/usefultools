#!/usr/bin/env python

title =    ' ╔═╗┬┌┬┐  ╔═╗┌─┐┌┬┐┌┬┐┬┌┬┐  ╦ ╦┌─┐┌┐┌┌┬┐┬  ┌─┐┬─┐'
title += '\n ║ ╦│ │   ║  │ ││││││││ │   ╠═╣├─┤│││ │││  ├┤ ├┬┘'
title += '\n ╚═╝┴ ┴   ╚═╝└─┘┴ ┴┴ ┴┴ ┴   ╩ ╩┴ ┴┘└┘─┴┘┴─┘└─┘┴└─'

import os, sys, subprocess as sp

class issues:
    def BRANCH():
        print(f'\n\033[93m>> BRANCH ISSUE!\033[0m')
    def ABORT():
        print(f'\n\033[91m>> ABORT!\033[0m')
    def WARNING():
        print(f'\n\033[91m>> WARNING!\033[0m')
    def EXECUTE(command, run=False):
        print(f'\033[94m>> EXECUTE: {command}\033[0m')
        if run:
            sp.call(command, shell=True)

try:
    import click
except ImportError:
    answer = input('package `click` needs to be installed...install? [y/N]:')
    while(1):
        if answer=='y':
            pythonver = sp.getoutput(f'python --version ')
            if pythonver.find('Anaconda') > 0:
                issues.EXECUTE('conda install click', run=True)
            else:
                issues.EXECUTE('pip install click', run=True)
            import click
            break;
        elif answer == 'N':
            print('Aborting process...')
            sys.exit()
        else:
            issues.WARNING()
            answer = input('Please choose y or N: ')

def getAnswer(lst):
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

# Explanation of the options
exp_gp = 'Path of .git folder.     => Default: .'
exp_fp = 'Path of staging file(s). => Default: .'
exp_br = 'Commiting branch.        => Default: master'
exp_pu = 'Push or not. Flag.       => Default: False'
exp_de = 'Detailed diff. Flag.     => Default: False'

def Commit(detail):
    if detail:
        issues.EXECUTE(f'git diff --cached --ignore-all-space --ignore-blank-lines', run=True)
    commit_message = input('Commit Message: ')
    issues.EXECUTE(f'git commit -m "{commit_message}"', run=True)

def isStatusClean():
    ''' Checks for any modified/new/deleted files since last commit '''
    status_list = sp.getoutput(f'git status').split('\n')
    status_list = [status for status in status_list if status[0:1] =='\t']
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
        selection = [f'Commit changes of `{current_branch}`', \
                     f'Stash changes of `{current_branch}`', \
                     f'Force Checkout to `{branch}`', ]
        answer_2 = getAnswer(selection)
        if answer_2 == 1:
            issues.EXECUTE(f'git add {filepath}', run=True)
            Commit(detail)
            issues.EXECUTE(f'git checkout {branch}', run=True)
        elif answer_2 == 2:
            issues.EXECUTE(f'git stash', run=True)
            issues.EXECUTE(f'git checkout {branch}', run=True)
        else:
            issues.EXECUTE(f'git checkout -f {branch}', run=True)

def setBranch(branch, filepath):
    current_branch, branch_list = getCurrentBranch(lst=True)
    if branch not in branch_list:
        print(f'Branch `{branch}` not found.')
        option = [f'Make new branch `{branch}`', f'Stay on current branch `{current_branch}`']
        answer = getAnswer(option)
        if answer == 1:
            issues.EXECUTE(f'git checkout -b {branch}', run=True)
        else:
            print(f'commiting branch set to {current_branch}')
            branch = current_branch
    else:
        print(f'Currently on branch `{current_branch}`', end=' ')
        print(f'but commiting branch is set to `{branch}`.')
        selection = [f'Merge branch `{current_branch}` -> `{branch}`', \
                     f'Stay on branch `{current_branch}`']
        answer = getAnswer(selection)
        if answer == 1:
            setCheckout(branch, current_branch, filepath)
            issues.EXECUTE(f'git merge {current_branch}', run=True)
        else:
            print(f'commiting branch set to {current_branch}')
            branch = current_branch
    return branch

def isGitExist(gitpath):
    gitfolder = os.path.join(gitpath, '.git')
    flag = True if os.path.exists(gitfolder) else False
    return flag

def isRemoteExist():
    git = sp.getoutput('git remote -v')
    flag = False if len(git) == 0 else True
    return flag

def isBranchExist():
    git = sp.getoutput('git branch')
    flag = False if len(git) == 0 else True
    return flag

@click.command()
@click.option('--gitpath', default='.', type=click.Path(exists=True), help=exp_gp)
@click.option('--filepath', default='.', type=click.Path(exists=True), help=exp_fp)
@click.option('--branch', default='master', type=str, help=exp_br)
@click.option('--push', is_flag='False', help=exp_pu)
@click.option('--detail', is_flag='False', help=exp_de)
def cmd(gitpath, filepath, branch, push, detail):

    #conversion to absolute path
    gitpath = os.path.abspath(gitpath)
    filepath = os.path.abspath(filepath)

    os.chdir(gitpath)

    if not isGitExist(gitpath):
        issues.WARNING()
        print(f'It seems path:`{gitpath}` does not have `.git` folder')
        answer = getAnswer([f'Initialize `.git` folder'])
        issues.EXECUTE('git init', run=True)

    if isRemoteExist():
        issues.EXECUTE(f'git fetch origin', run=True)

    if isBranchExist():
        current_branch = getCurrentBranch()
        if current_branch != branch:
            issues.BRANCH()
            branch = setBranch(branch, filepath)
        
    # Commit or not
    if not isStatusClean():
        issues.EXECUTE(f'git diff --stat', run=True)
        issues.EXECUTE(f'git add {filepath}', run=True)
        Commit(detail)
    else:
        print('Clean State')

    # Push or not
    if not push:
        print('** no push **')
    elif not isRemoteExist():
        print('** no remote repository **')
    else:
        issues.EXECUTE(f'git push -u origin {branch}', run=True)


def main():
    print(title)
    cmd()


if __name__ == "__main__":
    main()
