#!/usr/bin/env python
import os, sys, subprocess as sp
from pysrc import issues
import click

def f(string):
    return f'\033[4m`{string}`\033[0m'

@click.command()
@click.argument('filename')
@click.option('-d', '--debug', is_flag='False', help='LLDB MODE TRIGGER')
def main(filename, debug):
        output = filename[:filename.find('.')] + '.out'
        print("filename:", filename);
        gcc = '/usr/local/bin/gcc-7'
        if debug:
            issues.execute([f'{gcc} {filename} -g -O0 -m32'])
            issues.execute([f'lldb ./a.out'])
            if click.confirm(f"Remove {f('a.out')} & related directory?"):
                issues.execute([f'rm ./a.out', f'rm -r ./a.out.dSYM'])
        else:
            issues.execute([f'{gcc} -o3 -mtune=native -march=native {filename} -lm'])
            issues.execute([f'./{output}'])

if __name__ == '__main__':
    main()
    
