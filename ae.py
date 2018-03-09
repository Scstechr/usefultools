#!/usr/bin/env python
"""
=============
Auto Executor
=============
"""
import subprocess as sp
import time
from datetime import datetime

try:
    import click
except ImportError:
    print('execute `pip install -r requirements.txt`')

class issues:
    def TIME():
        print(f'\033[93m{str(datetime.now())[:-7]}\033[0m', end=' ')
    def WARNING():
        print(f'\n\033[91m>> WARNING!\033[0m')
    def EXECUTE(command, run=False):
        print(f'\033[94m>> EXECUTE: \033[0m\033[91m{command}\033[0m\n')
        if run == True:
            sp.call(command, shell=True)

def strdth(digit):
    digit = str(digit)
    end = 'th'
    if digit[-1] == '1' and digit != '11':
        end = 'st'
    if digit[-1] == '2':
        end = 'nd'
    if digit[-1] == '3':
        end = 'rd'
    return digit + end

@click.command()
@click.argument('execute', type=str)
@click.argument('sleep', type=int)
@click.option('-r', '--rep', type=int, default=0, help='Maximum Repetition. Default set to Infinit.')
def cmmd(execute, sleep, rep):
    i = 1
    if rep < 0 or sleep < 0:
        issues.WARNING()
        sys.exit()
    while(1):
        print(f'\n{strdth(i)}', end=' ')
        issues.TIME()
        issues.EXECUTE(f'{execute}', run=True)
        if rep > 0 and i >= rep:
            break
        time.sleep(sleep)
        i += 1

def main():
    cmmd()

if __name__ == '__main__':
    main()
