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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class issue:
    BRANCH = f'\n{bcolors.WARNING}>> BRANCH ISSUE!{bcolors.ENDC}'
    ABORT = f'\n{bcolors.FAIL}>> ABORT!{bcolors.ENDC}'
    WARNING = f'\n{bcolors.WARNING}>> WARNING!{bcolors.ENDC}'

def EXECUTE(command):
    print(f'{bcolors.OKBLUE}>> EXECUTE: {command}{bcolors.ENDC}')
    os.system(command)
    
def getModifiedList():
    status_list = sp.getoutput(f'git status').replace(' ','').split('\n')
    modified_list = set(filename for filename in status_list if filename.find('modified') > 0)
    new_file_list = set(filename for filename in status_list if filename.find('new file') > 0)
    delete_file_list = set(filename for filename in status_list if filename.find('delete file') > 0)
    modified_list = modified_list.union(new_file_list, delete_file_list)#
    return modified_list

def checkClean():
    status_list = sp.getoutput(f'git status').replace(' ','').split('\n')
    if len(status_list)==4:
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
        print(issue.BRANCH)
        if branch not in branch_list:
            print(f'You selected branch `{branch}` but it does not exist.\nExisting branch list:')
            [print(f'{idx+1}:', branch) for idx, branch in enumerate(branch_list)]
            if not click.confirm(f'Do you want to make new branch `{branch}`?'):
                print(f'{issue.ABORT}')
                sys.exit(0)
            else:
                EXECUTE(f'git checkout -b {branch}')
        else:
            print(f'Currently on branch `{current_branch}` but commiting branch is set to `{branch}`.\n')
            if checkClean():
                print(f'It seems branch `{current_branch}` has a clean state.')
                print(f'\t1. Checkout to branch `{branch}\n\t2. Stay on current branch `{current_branch}`')
                while(1):
                    print('Please choose your option:', end=" ")
                    option = f'{input()}'
                    if option == '1':
                        EXECUTE(f'git checkout {branch}')
                        break;
                    elif option == '2':
                        print(f'Branch unchanged')
                        break;
                    else:
                        print(f'{issue.WARNING}')
                        print(f'Please choose 1 or 2')
            else:
                print(f'It seems branch `{current_branch}` has a some modified/new/deleted files.')
                print(f'\t1. Discard changes and force checkout to branch `{branch}')
                print(f'\t2. Stash changes and checkout to branch `{branch}`')
                print(f'\t3. Try merging `{current_branch}` into `{branch}`')
                print(f'\t4. Stay on current branch `{current_branch}`')
                while(1):
                    print('Please choose your option:', end=" ")
                    option = f'{input()}'
                    if option == '1':
                        EXECUTE(f'git checkout {branch}')
                        break;
                    elif option == '2':
                        print(f'Branch unchanged')
                        break;
                    else:
                        print(f'{issue.WARNING}')
                        print(f'Please choose 1 or 2')
            #if not click.confirm(f'Do you want to merge `{current_branch}` into `{branch}`?'):
            #    if checkClean():
            #        print(f'> You have clean state. Checking out to branch `{branch}`')
            #        EXECUTE(f'git checkout {branch} >> .git_checkout_log')
            #    else:
            #        print('\nIt seems you have some files to commit.')
            #        if not click.confirm(f'Do you want to stash your changes and checkout to `{branch}`?'):
            #            print(f'\nCommiting branch is now set to `{current_branch}`')
            #            branch = current_branch
            #        else:
            #            EXECUTE('git stash')
            #            EXECUTE(f'git checkout {branch}')
            #            
            #else:
            #    if not checkClean():
            #        EXECUTE(f'git status')
            #        if not click.confirm(f'Do you want to stash your changes and checkout to `{branch}`?'):
            #            EXECUTE(f'git checkout --force {branch}') 
            #        else:
            #            EXECUTE('git stash')
            #            EXECUTE(f'git checkout {branch}')
            #    #EXECUTE(f'git format-patch master --stdout >| test.patch')
            #    print(f'Merge {current_branch} into {branch}\n')
            #    EXECUTE(f'git commit -m "merge: {current_branch} -> {branch}"')
            #    EXECUTE(f'git checkout {branch}')
            #    EXECUTE(f'git merge --no-ff {current_branch} --no-commit')
            #    if  click.confirm(f'CHECKOUT TO BRANCH `{current_branch}`?'):
            #        EXECUTE(f'git checkout {current_branch}')
            #    sys.exit()
    return branch

@click.command()
@click.option('--folder', default='.', type=click.Path(exists=True), help='Path of .git folder. Default: "."')
@click.option('--path', default='.', type=click.Path(exists=True), help='Path of staing file(s). Default: "."')
@click.option('--tag', default='NONE', help='What kind of commit. Default: "File Name"')
@click.option('--branch', default='master', type=str, help='Commiting branch. Default: "master"')
@click.option('--push', is_flag=True, help='Push or not')
@click.option('--commit', is_flag=True, help='Commit or not')
@click.option('--reset', is_flag=True, help='Reset or not')
def Commit(folder, path, branch, push, commit, tag, reset):
    git_folder = os.path.abspath(folder)
    commit_file = os.path.abspath(path)
    os.chdir(git_folder)

    commit_branch = setCommitBranch(branch)
    if reset:
        EXECUTE(f'git reset')
    if commit:
        if len(getModifiedList()) > 0:
            print('\n')
            EXECUTE(f'git add {commit_file}')
            EXECUTE(f'git status')
            print('Commit Message:', end=" ")
            if tag == 'NONE':
                tag = pathlib.PurePath(commit_file).stem
            else:
                tag = f'[{tag}]'
            commit_message = f'{tag}: {input()}'
            EXECUTE(f'git commit -m "{commit_message}"')
        else:
            print('Nothing to commit. Clean. ')


def main():
    Commit()

if __name__ == "__main__":
    main()
    
