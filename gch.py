#!/usr/bin/env python
'''
==================
Git Commit Handler
==================
'''

import sys, subprocess as sp
from os import path, chdir
try:
    import click
except ImportError:
    print('execute `pip install -r requirements.txt`')

class issues:
    ''' String Format with color change '''
    def BRANCH():
        print(f'\n\033[93m>> BRANCH ISSUE!\033[0m')
    def ABORT():
        print(f'\n\033[91m>> ABORT!\033[0m')
        sys.exit()
    def WARNING(string=None):
        print(f'\n\033[91m>> WARNING!: {string}\033[0m')
    def EXECUTE(command_list, run=True):
        ''' Execute bash commands through shell '''
        for command in command_list:
            print(f'\033[94m>> EXECUTE: {command}\033[0m')
            if run == True:
                sp.call(command, shell=True)

def b(string):
    ''' String Format for Branch Name '''
    return f'\033[3m\033[33m{string}\033[0m'

def getAnswer(lst):
    ''' Generates selection list and answering sequence '''
    while(1):
        [print(f'{idx+1}: {option}') for idx, option in enumerate(lst)]
        answer = input('Answer: ')
        if answer.isdigit():
            if int(answer) > 0 and int(answer) <= len(lst):
                break
        issues.WARNING('Please choose right answer from below:')
    return int(answer)

def Commit():
    ''' Commit '''
    commit_message = click.prompt("Commit Message", type=str)
    issues.EXECUTE([f'git commit -m "{commit_message}"'])

def getCurrentBranch(lst=False):
    ''' Returns current branch name w or w/o branch list '''
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
        issues.WARNING(f'Branch `{b(branch)}` not found.')
        qs =     [f'Make new branch `{b(branch)}`               ']
        qs.append(f'Stay on current branch `{b(current_branch)}`')
        answer = getAnswer(qs)
        if answer == 1:
            issues.EXECUTE([f'git checkout -b {branch}'])
        else:
            click.echo(f'Commiting branch set to {b(current_branch)}')
            branch = current_branch
    else:
        click.echo(f'Currently on branch `{b(current_branch)}` but tried to commit to branch `{b(branch)}`.')
        qs =     [f'Merge branch `{b(current_branch)}` => branch `{b(branch)}`']
        qs.append(f'Stay on branch `{b(current_branch)}`                   ')
        qs.append(f'Checkout to branch `{b(branch)}`                       ')
        answer = getAnswer(qs)
        if answer == 2:
            print(f'Commiting branch is now set to `{b(current_branch)}`')
            branch = current_branch
        else:
            if not isExist(f'git status --short'):
                issues.EXECUTE([f'git checkout {branch}'])
            else:
                print(f'\nTheres some changes in branch `{b(current_branch)}`.')
                issues.EXECUTE([f'git diff --stat'])
                qs =     [f'Commit changes of branch `{b(current_branch)}`']
                qs.append(f'Stash changes of branch `{b(current_branch)}` ')
                qs.append(f'Force Checkout to branch `{b(branch)}`        ')
                answer_2 = getAnswer(qs)
                if answer_2 == 1:
                    issues.EXECUTE([f'git add .',f'git diff --stat'])
                    Commit()
                    issues.EXECUTE([f'git checkout {branch}'])
                elif answer_2 == 2:
                    issues.EXECUTE([f'git stash',f'git checkout {branch}'])
                else:
                    issues.EXECUTE([f'git checkout -f {branch}'])
            if answer == 1:
                issues.EXECUTE([f'git merge {current_branch}'])
    return branch

def isExist(command):
    output = sp.getoutput(command)
    flag = False if len(output) == 0 else True
    return flag

def initialize(flag=False):
    # git confi
    if not path.exists("~/.gitconfig") and flag:
        click.echo("~/.gitconfig file does not exist. => Start Initialization!")
        username = click.prompt("username", type=str)
        email = click.prompt("email", type=str)
        issues.EXECUTE([f'git config --global user.name "{username}"',\
                        f'git config --global user.email {email}'])

        if click.confirm('Do you want to use emacs instead of vim as an editor?'):
            issues.EXECUTE([f'git config --global core.editor emacs'])
        click.echo("# using vimdiff as a merge tool")
        issues.EXECUTE([f'git config --global merge.tool vimdiff',\
                         'git config --list'])
    title = input('Title of this repository(project): ').upper()
    issues.EXECUTE(['git init', 'touch .gitignore', 'touch README.md'])
    issues.EXECUTE(['echo ".*" >> .gitignore', f'echo "# {title}" >> README.md'])

# Explanation of the options showed in --help flag
exp_g = 'Path of dir that contains `.git`. > Default: .'
exp_f = 'Path of staging file/diry.        > Default: .'
exp_b = 'Commiting branch.                 > Default: master'
exp_p = 'Push or not.                      > Default: False'
exp_d = 'Detailed diff.                    > Default: False'
exp_l = 'Git log with option.              > Default: False'
exp_c = 'Commit or not.                    > Default: False'
exp_u = 'Unstage all files.                > Default: False'

@click.command()
@click.option('-g', '--gitpath', default='.', type=click.Path(exists=True), help=exp_g)
@click.option('-f', '--filepath', default='.', type=click.Path(exists=True), help=exp_f)
@click.option('-b', '--branch', default='master', type=str, help=exp_b)
@click.option('-p', '--push', is_flag='False', help=exp_p)
@click.option('-d', '--detail', is_flag='False', help=exp_d)
@click.option('-l', '--log', is_flag='False', help=exp_l)
@click.option('-c', '--commit', is_flag='False', help=exp_c)
@click.option('-u', '--unstage', is_flag='False', help=exp_u)
def main(gitpath, filepath, branch, push, detail, log, commit, unstage):

    #conversion to absolute path
    gitpath = path.abspath(gitpath)
    filepath = path.abspath(filepath)

    chdir(gitpath)

    gitfolder = path.join(gitpath, '.git')
    if not path.exists(gitfolder):
        issues.WARNING(f'It seems path:`{gitpath}` does not have `.git` folder.')
        if click.confirm(f'Initialize?'):
            initialize(True)
        else:
            issues.ABORT()

    if unstage:
        issues.EXECUTE(['git rm -r --cached .'])
    issues.EXECUTE(['git status --short'])

    if log:
        issues.EXECUTE(['git log --stat --oneline --graph --decorate'])

    if isExist('git branch'):
        current_branch = getCurrentBranch()
        if current_branch != branch:
            issues.BRANCH()
            branch = setBranch(branch, filepath)
        
    # Commit or not
    if isExist(f'git status --short'):
        issues.EXECUTE([f'git diff --stat'])
        if detail:
            issues.EXECUTE([f'git diff --cached --ignore-all-space --ignore-blank-lines'])
        if commit:
            issues.EXECUTE([f'git add {filepath}'])
            Commit()
    else:
        print('Clean State')

    # Push or not
    if not push:
        print('** no push **')
    elif not isExist(f'git remote -v'):
        print('** no remote repository **')
    else:
        issues.EXECUTE([f'git push -u origin {branch}'])


if __name__ == "__main__":
    main()
