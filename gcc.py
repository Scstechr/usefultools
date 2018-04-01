#!/usr/bin/env python
import os, sys, subprocess as sp
from pysrc import issues
import click

def f(string):
    return f'\033[4m`{string}`\033[0m'

@click.command()
@click.argument('filename')
@click.option('-d', '--debug', is_flag='False', help='LLDB MODE TRIGGER')
@click.option('-r', '--run', is_flag='False', help='RUN AFTER COMPILE')
def main(filename, debug, run):
  output = filename[:filename.find('.')] + '.out'
  gcc = '/usr/local/bin/gcc-7'
  if not os.path.exists(gcc):
    gcc = '/usr/bin/gcc'
  opt = f'-O4 -Wall -mtune=native -march=native -o {output}'
  debugstr = f'-pg -g -fprofile-arcs -ftest-coverage'
  if debug:
    issues.execute([f'{gcc} {opt} {debugstr} {filename} -lm'])
    issues.execute([f'lldb ./{output}'])
    if click.confirm(f"Remove {f(output)} & related directory?"):
      issues.execute([f'rm ./{output}', f'rm -r ./{output}.dSYM'])
  else:
    issues.execute([f'{gcc} {opt} {filename} -lm'])
    if run:
      issues.execute([f'./{output}'])

if __name__ == '__main__':
    main()
    
