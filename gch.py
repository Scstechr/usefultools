#!/usr/bin/env python
# Git Commit Handler

# from standard library
import os, sys, subprocess as sp
# from outside and own library
import bcolors as bc

class issues:
    def BRANCH():
        print(f'\n{bc.WARNING}>> BRANCH ISSUE!{bc.ENDC}')
    def ABORT():
        print(f'\n{bc.FAIL}>> ABORT!{bc.ENDC}')
    def WARNING():
        print(f'\n{bc.FAIL}>> WARNING!{bc.ENDC}')
    def EXECUTE(command, run=False):
        print(f'{bc.OKBLUE}>> EXECUTE: {command}{bc.ENDC}')
        if run:
            os.system(command)

title =    ' ╔═╗┬┌┬┐  ╔═╗┌─┐┌┬┐┌┬┐┬┌┬┐  ╦ ╦┌─┐┌┐┌┌┬┐┬  ┌─┐┬─┐'
title += '\n ║ ╦│ │   ║  │ ││││││││ │   ╠═╣├─┤│││ │││  ├┤ ├┬┘'
title += '\n ╚═╝┴ ┴   ╚═╝└─┘┴ ┴┴ ┴┴ ┴   ╩ ╩┴ ┴┘└┘─┴┘┴─┘└─┘┴└─'

print(title)

try:
    import click
except:
    issues.WARNING()
    print('This command needs package: click')
    print('Please execute `conda install click` or `pip install click`')
    sys.exit()

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

def Commit():
    issues.EXECUTE(f'git status', run=True)
    commit_message = input('Commit Message: ')
    issues.EXECUTE(f'git commit -m "{commit_message}"', run=True)

def isStatusClean():
    status_list = sp.getoutput(f'git status').split('\n')
    status_list = [status for status in status_list if status[0:1] =='\t']
    print(status_list)

    sys.exit(0)
    status = True if status_list[2][0] != 'C' and status_list[3][0] != 'C' else False
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

def setBranch(branch, filepath):
    current_branch, branch_list = getCurrentBranch(lst=True)
    if branch not in branch_list:
        print(f'Branch `{branch}` not found.')
        option = [f'Make new branch `{branch}`', f'Stay on current branch `{current_branch}`']
        answer = getAnswer(option)
        if answer == 1:
            issues.EXECUTE(f'git checkout -b {branch}', run=True)
        return current_branch
    else:
        print(f'Currently on branch `{current_branch}`', end=' ')
        print(f'but commiting branch is set to `{branch}`.')
        selection = [f'Merge branch `{current_branch}` -> `{branch}`', \
                     f'Stash changes and checkout to branch `{branch}`', \
                     f'Force Checkout to `{branch}`', \
                     f'Stay on branch `{current_branch}`']
        answer = getAnswer(selection)
        if answer == 1:
            if isStatusClean():
                issues.EXECUTE(f'git checkout {branch}')
            else:
                print(f'Theres some changes in {current_branch}')
                selection = [f'Commit changes of `{current_branch}`', \
                             f'Stash changes of `{current_branch}`', \
                             f'Force Checkout to `{branch}`', ]
                answer_2 = getAnswer(selection)
                if answer_2 == 1:
                    issues.EXECUTE(f'git add {filepath}', run=True)
                    Commit()
                    issues.EXECUTE(f'git checkout {branch}')
                elif answer_2 == 2:
                    issues.EXECUTE(f'git stash')
                    issues.EXECUTE(f'git checkout {branch}')
                else:
                    issues.EXECUTE(f'git checkout -f {branch}')
            issues.EXECUTE(f'git merge {current_branch}')
        elif answer == 2:
            issues.EXECUTE(f'git stash')
            issues.EXECUTE(f'git checkout {branch}')
        elif answer == 3:
            issues.EXECUTE(f'git checkout -f {branch}')
        else:
            print(f'commiting branch set to {current_branch}')
            branch = current_branch
        return branch


@click.command()
@click.option('--gitpath', default='.', type=click.Path(exists=True), help=exp_gp)
@click.option('--filepath', default='.', type=click.Path(exists=True), help=exp_fp)
@click.option('--branch', default='master', type=str, help=exp_br)
@click.option('--push', is_flag='False', help=exp_pu)
def cmd(gitpath, filepath, branch, push):
    current_branch = getCurrentBranch()
    issues.EXECUTE(f'git fetch origin {branch}', run=True)
    if current_branch != branch:
        issues.BRANCH()
        branch = setBranch(branch)
        
    # Commit or not
    if not isStatusClean():
        issues.EXECUTE(f'git add {filepath}', run=True)
        Commit()

    # Push or not
    if not push:
        print('** no push **')
    else:
        issues.EXECUTE(f'git push origin {branch}', run=True)

def main():
    cmd()

if __name__ == "__main__":
    main()


