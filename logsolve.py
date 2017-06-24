#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from capture.undistort import undistort
from solve.gridsize import gridsize
from solve.cell import CellProcessor
from skimage.io import imread, imsave
from skimage.color import grey2rgb, rgb2grey
from skimage import img_as_ubyte
from skimage.filters import threshold_local, threshold_mean
import numpy as np

import sys


import matplotlib.pyplot as plt


def main():
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], '<input-image>')
        exit(1)

    #[infile, outfile] = sys.argv[1:3]
    infile = sys.argv[1]
    im = imread(infile, flatten=True)

    print('Undistorting')
    im = undistort(im)
    print('Calculating grid size...')
    x, y = gridsize(im)

    # for each im, inv, we want to do local thresholding
    # we need a big block size in order to get a good mean value
    # to compare to, but if it gets too big it's just like a global
    # thresholding

    thresh = threshold_local(im, 501, method='mean')
    #b = threshold_local(im, 501, method='mean', offset=0.1)

    offset = 0.1
    black, white = im > thresh-offset, im < thresh+offset

    print('Grid size: ', x, y)

    print('Calculating cell colors')
    cpwhite = CellProcessor(white, x, y)
    cpblack = CellProcessor(black, x, y)

    areas = grey2rgb(img_as_ubyte(im.copy()))
    colors = grey2rgb(img_as_ubyte(im.copy()))
    # grey out the images
    for yy in range(y):
        for xx in range(x):
            rr, cc = cpwhite.cell_ellipse(xx, yy)
            areas[rr, cc] = np.array([255,255,255])
            iswhite = cpwhite.get_color(xx, yy) < 127-offset
            isblack = cpblack.get_color(xx, yy) < 127-offset
            rr, cc = cpwhite.cell_rect(xx, yy)
            if isblack:
                colors[rr, cc] = np.array([0,0,0])
            elif iswhite:
                colors[rr, cc] = np.array([255,255,255])
            else:
                colors[rr, cc] = np.array([127,127,127])


    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(10, 3))
    ax = axes.ravel()
    plt.gray()

    ax[0].imshow(im)
    ax[0].set_title('Original Image')
    ax[1].imshow(areas)
    ax[1].set_title('Detection areas')
    ax[2].imshow(colors)
    ax[2].set_title('Detected colors')


    for a in ax:
        a.axis('off')
    plt.show()






if __name__ == '__main__':
    main()
