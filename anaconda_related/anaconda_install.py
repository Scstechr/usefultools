#!/usr/bin/env python
import sys, subprocess as sp

# installing brew
if not os.path.exists('/usr/local/bin/brew'):
    sp.call('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"', shell = True)

if sys.version.find('Anaconda') < 0:
    sp.call('brew install Caskroom/cask/miniconda', shell=True)
    sp.call('echo export PATH="/usr/local/miniconda3/bin:$PATH" >> ~/.bash_profile', shell=True)
    sp.call('source ~/.bash_profile', shell=True)
else:
    sp.call("echo 'Anaconda already installed'", shell=True)
