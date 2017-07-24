import sys

from skimage.io import imread, imsave


def from_arg():
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], '<input-image>')
        exit(1)

    infile = sys.argv[1]
    im = imread(infile, flatten=True)

    return im
