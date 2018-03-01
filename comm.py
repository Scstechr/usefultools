from os import system
from sys import argv
import pathlib
from subprocess import checkout

def getCurrentBranch(gFolder):
    '''
    Returns current branch name
    '''
    s = checkout('git branch').decode('utf-8'). 
    
