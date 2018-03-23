# GCH: Git Commit Handler
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

Official document of __GCH__ (Git Commit Handler).
Recommended to use with `alias`, such as `alias gch='gch.py'`. after exporting PATH of the cloned folder.
Every command used in this script are visible as such:
```bash
>> EXECUTE: git status --short
```
### Options:

#### `-g` or `--gitpath`

The capability of this tag is that of `git --git-dir=<path>`.
With this tag, user can specify which `.git` folder to use for commit etc.
Default is set to `.`, which will be selected if `-g` was abridged.

##### Example of File Tree
```bash
-- Main <- A
     |--.git/
     |--tests/ <-B
     |    |--.git/  
     |    |--.gitignore  
     |    |--README.md  
     |    +--test.c
     |--.gitignore  
     |--README.md  
     +--main.c  
```

If user was in ...
- `Main`:
  1. If `-g` was abridged, it selects `Main/.git` as a target `.git` folder.
- `Main/tests`:
  1. If `-g` was abridged, it selects `Main/test/.git` as a target `.git` folder.
  2. If `-g` was set to `..` i.e. `-g ..`, it selects `Main/.git` as a target `.git` folder.

#### `-f` or `--filepath`

If user wants to `git add` only specific file, then please declare it with `-f <FILE>`. Otherwise, `git add .` will be executed by default.

#### `-b` or `--branch`

If user wants to specify committing branch, then please declare it with `-b <BRANCH>`. Otherwise, `master` branch will be used.

##### Example of Branch list
```bash
$ git branch
* master
  test
```
In the situation like above, where current branch was `master`:
- `-b master` or abridging `-b` does not make any change.
- `-b test` raises `BranchIssue` with number of choices.

```bash
>> BRANCH ISSUE!
Currently on branch `master` but tried to commit to branch `test`.
1: Merge branch `master` => branch `test`
2: Stay on branch `master`                   
3: Checkout to branch `test`  
Answer:
```
If you want to abort process, use `Ctrl-C`.
__Merge option (1) is not recommended, because it does not take merge conflict in count__. If there are changes to commit and you choose option (3), there will be three choices to pick next.
```bash
>> BRANCH ISSUE!
Answer: 3

Theres some changes in branch `master`.
>> EXECUTE: git diff --stat
 doc/gch_doc.md | 51 ++++++++++++++++++++++++++++++++++++++++++---------
 1 file changed, 42 insertions(+), 9 deletions(-)
1: Commit changes of branch `master`
2: Stash changes of branch `master`
3: Force Checkout to branch `test`
Answer:
```
`git diff --stat` will be executed automatically.

 If you pick...
- 1, 2: `commit`/`stash` changes and `checkout`.
- 3: Execute `git checkout -f test`, ignoring all changes.

#### `-d` or `--detail`

Option for detailed `git diff`.

#### `-l` or `--log`

Display `git log` with some options.

<!--##### `-p` or `--gitpath`
- __Default:__  `.`
- __Argument (Option):__ `<PATH>`

##### `-d` or `--gitpath`
- __Default:__  `.`
- __Argument (Option):__ `<PATH>`

##### `-l` or `--gitpath`
- __Default:__  `.`
- __Argument (Option):__ `<PATH>`

##### `-c` or `--gitpath`
- __Default:__  `.`
- __Argument (Option):__ `<PATH>`

##### `-u` or `--gitpath`
- __Default:__  `.`
- __Argument (Option):__ `<PATH>` -->