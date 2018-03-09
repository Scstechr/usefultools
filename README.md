### List of tools
Some tools are still __unstable__, so please use it at your own risk.

| name | filename | description |
|:-----|:---------|:------------|
| Git Commit Handler |`gch.py` | Handles git commands |
| Auto-Executor | `ae.py` | Automatically executes given command |
| Color Check | `colors.py` | Displays list of colors to pick |
### Requirements
Please install all the packages listed in `requirements.txt`.

```bash
git clone https://github.com/Scstechr/usefultools ~/.useful
cd ~/.useful
pip install -r requirements.txt
```
Also, be sure you have `Python 3.6.x` executable in any way.
### Recommended settings:
Add these lines in `.bash_profile` and `source` it afterwards.

```bash:.bash_profile
export "PATH=${HOME}/.useful:$PATH"
alias gch='gch.py'
alias ae='ae.py'
alias col='colors.py'
```

