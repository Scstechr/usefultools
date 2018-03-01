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
    
def getModifiedList():
    status_list = sp.getoutput(f'git status').replace(' ','').split('\n')
    
    modified_list = set(filename for filename in status_list if filename.find('modified') > 0)
    new_file_list = set(filename for filename in status_list if filename.find('new file') > 0)
    delete_file_list = set(filename for filename in status_list if filename.find('delete file') > 0)
    return modified_list

def checkClean():
    status_list = sp.getoutput(f'git status').replace(' ','').split('\n')
    if len(status_list)==4:
        EXECUTE('git status')
        return True
    else:
        return False

def getCurrentBranch():
    ''' Returns current branch name '''

    l = sp.getoutput('git branch').split('\n')
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
            print(f'Currently on branch `{current_branch}` but commiting branch is `{branch}`.\n')
            if not click.confirm(f'Do you want to merge `{current_branch}` into `{branch}`?'):
                if checkClean():
                    print(f'You have clean state. Checking out to branch `{branch}`')
                    EXECUTE(f'git checkout {branch}')
                else:
                    print('These are the modified list:')
                    [print(filename) for filename in getModifiedList()]
                    if not click.confirm(f'Do you want to stash your changes and checkout to `{branch}`?'):
                        print(f'Staying on branch `{current_branch}`')
                        branch = current_branch
                    else:
                        EXECUTE('git stash')
                        EXECUTE(f'git checkout {branch}')
                        
            else:
                print(f'Merge {current_branch} into {branch}\n')
                EXECUTE(f'git add .')
                EXECUTE(f'git commit -m "merge: {current_branch} -> {branch}"')
                EXECUTE(f'git checkout {branch}')
                EXECUTE(f'git merge {current_branch}')
                EXECUTE(f'git checkout {current_branch}')
                click.end()
    return branch

@click.command()
@click.option('--git_folder', default='.', type=click.Path(exists=True), help='Path of .git folder')
@click.option('--commit_file', default='.', type=click.Path(exists=True), help='Path of staing file(s)')
@click.option('--branch', default='master', type=str, help='Commiting branch. Default set to master')
@click.option('--fetch', is_flag=True)
@click.option('--push', is_flag=True)
@click.option('--commit', is_flag=True)
@click.option('--rebase', is_flag=True)
def Commit(git_folder, commit_file, branch, fetch, push, commit, rebase):
    git_folder = os.path.abspath(git_folder)
    commit_file = os.path.abspath(commit_file)
    os.chdir(git_folder)

    if fetch:
        EXECUTE(f'git fetch')
    if rebase:
        EXECUTE(f'git rebase')
    if commit:
        commit_branch = setCommitBranch(branch)
        modified_list = getModifiedList()
        if len(modified_list) > 0:
            print('These are modified since last commit:')
            [print(filename) for filename in modified_list]
            EXECUTE(f'git add {commit_file}')
            print('Commit Message:', end=" ")
            commit_message = f'{pathlib.PurePath(commit_file).stem}: {input()}'
            EXECUTE(f'git commit -m {commit_message}')
        else:
            print('Nothing to commit. Clean. ')


def main():
    Commit()

if __name__ == "__main__":
    main()
    
