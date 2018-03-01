# comm.py
"""
This command handles `git commit` related commands.
"""

# from standard library
import os, sys, pathlib
import subprocess as sp
#from subprocess import check_output

# from libraries outside
# please install all the modules listed in requirements.txt
# pip install -r requrements.txt
import click

def ABORT():
    ABORT_MESSAGE = '\n>> ABORT COMMIT <<'
    print(ABORT_MESSAGE)
    click.Abort()

def EXECUTE(command):
    print('>> EXECUTE:', command)
    os.system(command)

def getCurrentBranch():
    ''' Returns current branch name '''

    l = sp.getoutput('git branch').split('\n')#check_output('ls', '-al')#.decode('utf-8').split('\n')
    current_branch = ''.join([branch[2:] for branch in l if branch[0]=='*'])
    branch_list = [branch[2:] for branch in l]
    return current_branch, branch_list

def setCommitBranch(branch):
    current_branch, branch_list = getCurrentBranch()
    if branch != current_branch:
        print(f'\n>> BRANCH ISSUE! <<')
        if branch not in branch_list:
            print(f'You selected branch `{branch}` but it does not exist.\nExisting branch list:')
            [print(f'{idx+1}:', branch) for idx, branch in enumerate(branch_list)]
            if not click.confirm(f'Do you want to make branch `{branch}`?'):
                ABORT()
            else:
                EXECUTE(f'git checkout -b {branch}')
        else:
            print(f'Currently on branch `{current_branch}` but commiting branch is `{branch}`.')
            if not click.confirm(f'Do you want to merge `{current_branch}` into `{branch}`?'):
                ABORT()
            else:
                print('\n')
                EXECUTE(f'git add .')
                EXECUTE(f'git commit -m "merge: {current_branch} -> {branch}"')
                EXECUTE(f'git checkout {branch}')
                EXECUTE(f'git merge {current_branch}')
                EXECUTE(f'git checkout {current_branch}')
    return branch

@click.command()
@click.option('--git_folder', default='.', type=click.Path(exists=True), help='Path of .git folder')
@click.option('--commit_file', default='.', type=click.Path(exists=True), help='Path of staing file(s)')
@click.option('--branch', default='master', type=str, help='Commiting branch. Default set to master')
@click.option('--p', is_flag=True)
def Commit(git_folder, commit_file, branch, p):
    git_folder = os.path.abspath(git_folder)
    commit_file = os.path.abspath(commit_file)
    os.chdir(git_folder)
    commit_branch = setCommitBranch(branch)

def main():
    Commit()

if __name__ == "__main__":
    main()
    
