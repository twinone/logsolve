#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from gridsize import gridsize

def usage():
    print("Usage:", sys.argv[0], '<input-image> <x> <y>')
    exit(1)
# Main
def main():
    if len(sys.argv) < 4:
        usage()

    fname, real_x, real_y = sys.argv[1:4]
    try:
        real = int(real_x), int(real_y)
    except:
        usage()

    detected = gridsize(fname)
    if real != detected:
        print('[FAIL]', fname+': expected', coords_str(real) + ', got', coords_str(detected))
        exit(1)
    else:
        print('[PASS]', fname+':', coords_str(detected))


def coords_str(c):
    x, y = c
    return str(x) + 'x' + str(y)



if __name__ == '__main__':
    main()
