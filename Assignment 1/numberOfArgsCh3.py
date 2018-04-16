#!/usr/bin/python3

import sys

print('The number of command line arguments is: %s arguments.' % len(sys.argv))

if len(sys.argv) >= 3:
    print('There are 3 or more arguments')
else:
    print('There are less than 3 arguments')
