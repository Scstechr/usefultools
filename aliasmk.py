#!/usr/bin/env python
import sys, subprocess as sp
from os import path, chdir, getcwd
import click

from pysrc import issues
from pysrc.qs import getAnswer, isExist

def a(string):
    ''' String format for alias name '''
    return f'\033[3m\033[91m{string}\033[0m'

def c(string):
    ''' String format for alias name '''
    return f'\033[3m\033[96m{string}\033[0m'

@click.command()
@click.argument('new_alias', type=str)
@click.argument('command', type=str)
def main(new_alias, command):
    #issues.execute(['cat ~/.bash_profile | grep "alias"'])
    alias_list = sp.check_output('cat ~/.bash_profile | grep "alias"', shell=True).decode('utf-8')
    alias_dict = {alias[alias.find('alias ')+6:alias.find('=')]:\
                  alias[alias.find("'")+1:-1] for alias in alias_list.split('\n')}
    if new_alias in alias_dict.keys():
        issues.warning(f'`{new_alias}` already exists!')
        print(f'old: {a(new_alias)} : {c(alias_dict[new_alias])}')
        print(f'new: {a(new_alias)} : {c(command)}')
        qs = ['Rewrite existing alias', 'Delete existing alias', 'Abort']
        ans = getAnswer(qs)
        if ans == 1 or ans == 2:
            issues.warning(f'**not implemented! sorry **')
        sys.exit()
    else:
        statement = f"alias {new_alias}='{command}'"
        issues.execute([f'echo {statement} >> ~/.bash_profile'])
        print('please execute `source ~/.bash_profile` afterwards')

if __name__ == '__main__':
    main()
