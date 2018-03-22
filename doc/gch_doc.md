# GCH: Git Commit Handler

Official document of __GCH__ (Git Commit Handler).
Recommended to use with `alias`, such as `alias gch='gch.py'`. after exporting PATH of the cloned folder.
Every command used in this script is visible as such:
```bash
>> EXECUTE: git status --short
```
### Options:

##### `-g` or `--gitpath`

The capability of this tag is that of `git --git-dir=<path>`.
With this tag, user can select which `.git` folder to use for commit etc.
Default is set to `.`, which will be selected if `-g` was abridged.

##### Example
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

<!-- ##### `-f` or `--fipath`
- __Default:__  `.`
- __Argument (Option):__ `<PATH>`

##### `-b` or `--gitpath`
- __Default:__  `.`
- __Argument (Option):__ `<PATH>`

##### `-p` or `--gitpath`
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