#!/usr/bin/env python
'''
==================
Git Commit Handler
==================
'''

import sys, subprocess as sp
from os import path, chdir, getcwd
import six
if not six.PY3:
    sp.call('echo "VERSION ERROR! PLEASE USE PYTHON 3.6.X"', shell=True)
    sys.exit()
try:
    import click
except ImportError:
    sp.call('echo "execute `pip install -r requirements.txt`"', shell=True)

from pysrc import issues
from pysrc.qs import getAnswer, isExist

def b(string):
    ''' String Format for Branch Name '''
    return f'\033[3m\033[33m{string}\033[0m'

def Commit():
    ''' Commit '''
    commit_message = click.prompt("Commit Message", type=str)
    issues.execute([f'git commit -m "{commit_message}"'])

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
        issues.warning(f'Branch `{b(branch)}` not found.')
        qs =     [f'Make new branch `{b(branch)}`               ']
        qs.append(f'Stay on current branch `{b(current_branch)}`')
        answer = getAnswer(qs)
        if answer == 1:
            issues.execute([f'git checkout -b {branch}'])
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
            click.echo(f'Commiting branch is now set to `{b(current_branch)}`')
            branch = current_branch
        else:
            if not isExist(f'git status --short'):
                issues.execute([f'git checkout {branch}'])
            else:
                click.echo(f'\nTheres some changes in branch `{b(current_branch)}`.')
                issues.execute([f'git diff --stat'])
                qs =     [f'Commit changes of branch `{b(current_branch)}`']
                qs.append(f'Stash changes of branch `{b(current_branch)}` ')
                qs.append(f'Force Checkout to branch `{b(branch)}`        ')
                answer_2 = getAnswer(qs)
                if answer_2 == 1:
                    issues.execute([f'git add .',f'git diff --stat'])
                    Commit()
                    issues.execute([f'git checkout {branch}'])
                elif answer_2 == 2:
                    issues.execute([f'git stash',f'git checkout {branch}'])
                else:
                    issues.execute([f'git checkout -f {branch}'])
            if answer == 1:
                issues.execute([f'git format-patch {branch}..{current_branch} --stdout | git apply --check'])
                if isExist('git format-patch {branch}..{current_branch} --stdout | git apply --check'):
                    issues.execute([f'git merge {current_branch}'])
                else:
                    issues.warning("Aborting Merge because conflict is likely to occur.")
                    issues.abort()
    return branch

def globalsetting():
    click.echo("** Configureation of global settings **")
    issues.execute(['git config --global credential.helper osxkeychain',\
                    'git config --global core.excludesfile ~/.gitignore_global'])
    name, email = click.prompt("name", type=str), click.prompt("email", type=str)
    issues.execute([f'git config --global user.name "{name}"',\
                    f'git config --global user.email {email}'])

    if click.confirm('Do you want to use emacs instead of vim as an editor?'):
        issues.execute([f'git config --global core.editor emacs'])
    else:
        issues.execute([f'git config --global core.editor vim'])
        
    if click.confirm('Do you want to use ediff instead of vimdiff?'):
        issues.execute([f'git config --global {x}.tool ediff' for x in ['diff', 'merge']])
    else:
        issues.execute([f'git config --global {x}.tool vimdff' for x in ['diff', 'merge']])
    issues.execute([f'cat ~/.gitconfig'])

def initialize(flag=False):
    if flag:
        issues.execute([f'cat ~/.gitconfig'])
        globalsetting()
        sys.exit()
    else:
        # git confi
        gitconfigpath = path.join(path.expanduser('~'), '.gitconfig')
        if not path.exists(gitconfigpath):
            click.echo("~/.gitconfig file does not exist. => Start Initialization!")
            globalsetting()
        readmepath = path.join(getcwd(), 'README.md')
        if not path.exists(readmepath):
            title = click.prompt('Title of this repository(project)').upper()
            issues.execute(['git init', 'touch .gitignore', 'touch README.md',\
                            'echo ".*" >> .gitignore', f'echo ".*" >> ~/.gitignore_global',\
                            'echo "# {title}" >> README.md'])

defaults = {}
if path.exists("./defaults.txt"):
    with open("./defaults.txt", 'r') as readfile:
        for line in readfile:
            k, v = line.replace('\n','').split(":")
            defaults[str(k)] = str(v)
else:
    defaults['init'] = 'False'
    defaults['gitpath'] = '.'
    defaults['filepath'] = '.'
    defaults['branch'] = 'master'
    defaults['detail'] = 'False'
    defaults['log'] = 'False'
    defaults['commit'] = 'False'
    defaults['reset'] = 'False'
    defaults['push'] = 'False'
    defaults['remote'] = 'origin'

# Explanation of the options showed in --help flag
exp_i = f'Run initializer or not.             > Default: {defaults["init"]}'
exp_g = f'Path of dir that contains `.git`.   > Default: {defaults["gitpath"]}'
exp_f = f'Path/Regex of staging file/dir.     > Default: {defaults["filepath"]}'
exp_b = f'Commiting branch.                   > Default: {defaults["branch"]}'
exp_d = f'Detailed diff.                      > Default: {defaults["detail"]}'
exp_l = f'Git log with option.                > Default: {defaults["log"]}'
exp_c = f'Commit or not.                      > Default: {defaults["commit"]}'
exp_r = f'Reset (remove all add).             > Default: {defaults["reset"]}'
exp_p = f'Push or not.                        > Default: {defaults["push"]}'
exp_e = f'Choose which remote repo. to push.  > Default: {defaults["remote"]}'
exp_s = f'Save settings                       > Default: False'

@click.command()
@click.option('-i', '--init',     is_flag=defaults['init'],   help=exp_i)
@click.option('-d', '--detail',   is_flag=defaults['detail'],   help=exp_d)
@click.option('-l', '--log',      is_flag=defaults['log'],   help=exp_l)
@click.option('-c', '--commit',   is_flag=defaults['commit'],   help=exp_c)
@click.option('-r', '--reset',    is_flag=defaults['reset'],   help=exp_r)
@click.option('-p', '--push',     is_flag=defaults['push'],   help=exp_p)
@click.option('-s', '--save',     is_flag='False', help=exp_s)
@click.option('-g', '--gitpath',  default=defaults['gitpath'],  type=click.Path(exists=True), help=exp_g)
@click.option('-f', '--filepath', default=defaults['filepath'], type=str, help=exp_f)
@click.option('-b', '--branch',   default=defaults['branch'],   type=str, help=exp_b)
@click.option('--remote',         default=defaults['remote'],   type=str, help=exp_e)
def main(init, detail, log, commit, reset, push, save, gitpath, filepath, branch, remote):

    defaults['init'] = init
    defaults['gitpath'] = gitpath
    defaults['filepath'] = filepath
    defaults['branch'] = branch
    defaults['detail'] = detail 
    defaults['log'] = log
    defaults['commit'] = commit
    defaults['reset'] = reset
    defaults['push'] = push
    defaults['remote'] = remote

    if save:
        issues.execute(['rm defaults.txt'])
        for k, v in defaults.items():
            issues.execute([f'echo "{str(k)}:{str(v)}" >> defaults.txt'])

    if init:
        initialize(flag=True)
    #conversion to absolute path
    gitpath = path.abspath(gitpath)
    filepath = path.abspath(filepath)

    chdir(gitpath)

    gitfolder = path.join(gitpath, '.git')
    if not path.exists(gitfolder):
        issues.warning(f'It seems path:`{gitpath}` does not have `.git` folder.')
        if click.confirm(f'Initialize?'):
            initialize()
        else:
            issues.abort()

    if reset:
        issues.execute(['git reset'])
    issues.execute(['git status --short'])

    if log:
        issues.execute(['git log --stat --oneline --graph --decorate'])
    # Commit or not

    if isExist(f'git status --short'):
        issues.execute([f'git diff --stat'])
        if detail:
            issues.execute([f'git add .',\
                            f'git diff --cached --ignore-all-space --ignore-blank-lines',\
                            f'git reset'])
        if commit:
            issues.execute([f'git add {filepath}'])
            Commit()
    else:
        click.echo('Clean State')


    if isExist('git branch'):
        current_branch = getCurrentBranch()
        if current_branch != branch:
            issues.branch()
            branch = setBranch(branch, filepath)
        

    # Push or not
    if not push:
        pass
        #click.echo('** no push **')
    elif not isExist(f'git remote -v'):
        click.echo('** no remote repository **')
    else:
        issues.execute([f'git push -u {remote} {branch}'])

if __name__ == "__main__":
    main()
