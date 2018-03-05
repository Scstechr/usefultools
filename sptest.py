import subprocess as sp

import os, sys

myenv = os.environ.copy()
for key in myenv.keys():
    print(key, '\t', myenv[key])
    
cmd = 'git push -u origin master'.split(' ')
print(cmd)
sp.run(cmd)
