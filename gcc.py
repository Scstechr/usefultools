#!/usr/bin/env python
import os, sys

if len(sys.argv) == 2:
    output = sys.argv[1][:sys.argv[1].find('.')] + '.out'
    os.system(f'gcc -O3 -mtune=native -march=native {sys.argv[1]} -lm')
    os.system(f'mv ./a.out ./{output}')
    os.system(f'./{output}')
    
