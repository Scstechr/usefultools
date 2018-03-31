#!/usr/bin/env python
import os, sys

if len(sys.argv) == 2:
    output = sys.argv[1][:sys.argv[1].find('.')] + '.out'
    gcc = b'/usr/local/bin/gcc-7'
    os.system(f'{gcc} -O3 -mtune=native -march=native {sys.argv[1]} -lm')
    #os.system(f'clang {sys.argv[1]}')
    os.system(f'mv ./a.out ./{output}')
    os.system(f'./{output}')
    
