#!/usr/bin/env python
import sys, subprocess as sp

if sys.version.find('Anaconda') < 0:
    sp.call("echo 'Anaconda (or any other variation of it) is not installed'", shell=True)
    answer = raw_input("Install Anaconda (Miniconda)?[y/N] ")
    if answer == 'y':
        sp.call('brew install Caskroom/cask/miniconda', shell=True)
        sp.call('echo export PATH="/usr/local/miniconda3/bin:$PATH" >> .bash_profile', shell=True)
        sp.call('source ~/.bash_profile', shell=True)
    else:
        sp.call("echo 'Aborting Process'", shell=True)
else:
    sp.call("echo 'Anaconda already installed'", shell=True)
