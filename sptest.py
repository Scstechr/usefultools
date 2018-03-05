import subprocess as sp

sp.call('git config --list', shell=True)
sp.call('git push -u origin master', shell=True)
