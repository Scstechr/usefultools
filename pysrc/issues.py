##ISSUES
import sys, subprocess as sp
import click

''' String Format with color change '''
def branch():
    click.echo(f'\n\033[93m>> branch ISSUE!\033[0m')
def abort():
    click.echo(f'\n\033[91m>> abort!\033[0m')
    sys.exit()
def warning(string=None):
    click.echo(f'\n\033[91m>> warning!: {string}\033[0m')
def execute(command_list, run=True):
    ''' Execute bash commands through shell '''
    for command in command_list:
        click.echo(f'\033[94m>> execute: {command}\033[0m')
        if run == True:
            sp.call(command, shell=True)
