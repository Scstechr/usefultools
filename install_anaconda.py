import os, sys, subprocess as sp

if not sys.version.find('Anaconda'):
    sp.call("echo 'Anaconda (or any other variation of it) is not installed'", shell=True)
    answer = input("Install Anaconda (Miniconda)?[y/N]")
else:
    sp.call("echo 'Anaconda already installed'", shell=True)
