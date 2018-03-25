### Requirements
Please install all the packages listed in `requirements.txt`.

```bash
git clone https://github.com/Scstechr/usefultools ~/.useful
cd ~/.useful
pip install -r requirements.txt
```
Also, be sure you have `Python 3.6.x` executable in any way.

### List of tools

| name | filename | description |
|:-----|:---------|:------------|
| Git Commit Handler |`gch.py` | Handles git commands |
| Auto-Executor | `ae.py` | Automatically executes given command |
| Color Check | `colors.py` | Displays list of colors to pick |

#### Git Commit Handler
```bash
$ gch --help
Usage: gch.py [OPTIONS]

Options:
  -g, --gitpath PATH   Path of dir that contains `.git`. > Default: .
  -f, --filepath PATH  Path of staging file/diry.        > Default: .
  -b, --branch TEXT    Commiting branch.                 > Default: master
  -p, --push           Push or not.                      > Default: False
  -d, --detail         Detailed diff.                    > Default: False
  -l, --log            Git log with option.              > Default: False
  -c, --commit         Commit or not.                    > Default: False
  -u, --unstage        Unstage all files.                > Default: False
  --help               Show this message and exit.
```
- Executes `git` related commands as such:
	- `git init`, `git commit`, `git diff`, `git add`, `git push`
- Some issues with `merge` still exists (when conflict happens).
	- Attempts to avoid conflict before merge with applying patch.
- Document available: :us: [English](doc/gch_doc_en.md) / :jp: [Japanese](doc/gch_doc_jp.md)

#### Auto-Executor
```bash
$ ./ae.py --help
Usage: ae.py [OPTIONS] EXECUTE SLEEP

Options:
  -r, --rep INTEGER  Maximum Repetition. Default set to Infinit.
  --help             Show this message and exit.
```
- Automatically executes the command with some time gap in between.
- Able to set number of repetition.

```bash
$ ./ae.py 'ls' 2

1st 2018-03-09 22:50:49 >> EXECUTE: ls

LICENSE			ae.py			requirements.txt
README.md		colors.py
__pycache__		gch.py

2nd 2018-03-09 22:50:51 >> EXECUTE: ls

LICENSE			ae.py			requirements.txt
README.md		colors.py
__pycache__		gch.py

3rd 2018-03-09 22:50:53 >> EXECUTE: ls

LICENSE			ae.py			requirements.txt
README.md		colors.py
__pycache__		gch.py

...(Ctrl-C to stop)
```

### Recommended settings:
Add these lines in `.bash_profile` and `source` it afterwards.

```bash:.bash_profile
export "PATH=${HOME}/.useful:$PATH"
alias gch='gch.py'
alias ae='ae.py'
alias col='colors.py'
```



