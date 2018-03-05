# Git Commit Handler

# from standard library
import os, sys, subprocess as sp
# from outside and own library
import click, bcolors as bc

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

def getAnswer(lst):
    print('Choose from below:')
    while(1):
        [print(f'{idx+1}: {option}') for idx, option in enumerate(lst)]
        answer = input('Answer: ')
        if answer.isdigit():
            answer = int(answer)
            if answer > 0 and answer <= len(lst):
                break;
            else:
                issues.WARNING()
                print('Please choose right answer from below:')
        else:
            issues.WARNING()
            print('Please choose right answer from below:')
    
    return answer

def isStatusClean():
    status_list = sp.getoutput(f'git status').split('\n')
    os.system('git status')
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

def setBranch(branch):
    current_branch, branch_list = getCurrentBranch(lst=True)
    print('clean') if isStatusClean() else print('dirty')
        
    
    if branch not in branch_list:
        print(f'Branch `{branch}` not found.')
    else:
        selection = ['Merge branches', 'Stash changes and exit', 'Force Checkout to branch', 'Stay on branch']
        answer = getAnswer(selection)
        print(f'Currently on branch `{current_branch}`', end=' ')
        print(f'but commiting branch is set to `{branch}`.')

def Commit():
    issues.EXECUTE(f'git status', run=True)
    commit_message = input('Commit Message: ')
    issues.EXECUTE(f'git commit -m "{commit_message}"', run=True)

    
    pass

exp_gp = 'Path of .git folder.     => Default: .'
exp_fp = 'Path of staging file(s). => Default: .'
exp_br = 'Commiting branch.        => Default: master'

@click.command()
@click.option('--gitpath', default='.', type=click.Path(exists=True), help=exp_gp)
@click.option('--filepath', default='.', type=click.Path(exists=True), help=exp_fp)
@click.option('--branch', default='master', type=str, help=exp_br)
def cmd(gitpath, filepath, branch):
    current_branch = getCurrentBranch()
    if current_branch != branch:
        issues.BRANCH()
        setBranch(branch)
        sys.exit(0)
    issues.EXECUTE(f'git add {filepath}', run=True)
    Commit()
    if not click.confirm(f'Push?'):
        print('** no push **')
    else:
        issues.EXECUTE(f'git push origin {branch}', run=True)

def main():
    cmd()

if __name__ == "__main__":
    main()

