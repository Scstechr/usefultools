#!/usr/bin/env python
# colors
for i in range(110):
    print(f'\033[{i}m' + '{0:3d}'.format(i) + '\033[0m', end = ' ')
    if str(i)[-1] == '9':
        print('\n')
