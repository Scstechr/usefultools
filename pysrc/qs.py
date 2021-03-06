import subprocess as sp
import click
from . import issues

def getAnswer(lst):
    ''' Generates selection list and answering sequence '''
    while(1):
        [click.echo(f'{idx+1}: {option}') for idx, option in enumerate(lst)]
        answer = click.prompt('Answer',type=int)
        if answer > 0 and answer <= len(lst):
            break
        issues.warning('Please choose right answer from below:')
    return answer

def isExist(command):
    output = sp.getoutput(command)
    flag = False if len(output) == 0 else True
    return flag
