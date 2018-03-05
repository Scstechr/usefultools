import subprocess as sp

import os, sys

myenv = os.environ.copy()
for key in myenv.keys():
    print(key, '\t', myenv[key])
    
#sp.call('git config --list', shell=True)
sp.call('git push -u origin master', shell=True, env=myenv)
