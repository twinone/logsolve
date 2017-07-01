import sys

from skimage.io import imread, imsave
from .undistort import undistort


def undistort_from_arg():
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], '<input-image>')
        exit(1)

    infile = sys.argv[1]
    im = imread(infile, flatten=True)

    im = undistort(im)
    return im
