import sys
import subprocess as sp

def AbortProcess():
    sp.call('echo "Aborting process..."', shell=True)
    sys.exit()

if sys.version[0] == '2':
    sp.call('echo "You seem to have Python 2.x in your machine."', shell=True)
    answer = input('echo "Install Python 3.x via miniconda?[y/N]')
    print answer
    sys.exit()
    if not answer == 'y':
        AbortProcess()
    else:
        brew = sp.getoutput('brew')
        if brew.find('not found') > 0:
            sp.call('echo "You seem to not have `brew` installed in your machine."', shell=True)
            answer_2 = input('echo "Install `brew`?[y/N]')
            if not answer == 'y':
                AbortProcess()
            else:
                sp.call('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"', shell=True)
        sp.call('brew install Caskroom/cask/miniconda', shell=True)
        sp.call('echo "Exporting path to ~/.bash_profile"', shell=True)
        sp.call('echo "export PATH="/usr/local/miniconda3/bin:$PATH" >> ~/.bash_profile', shell=True)
        sp.call('source ~/.bash_profile', shell=True)
else:
    sp.call('echo "You already have Python 3.x installed."', shell=True)
