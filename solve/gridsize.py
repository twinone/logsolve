#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from skimage import util

from skimage.feature import canny, corner_harris, corner_subpix, corner_peaks
from skimage import img_as_ubyte

from skimage.data import camera
from skimage.filters import roberts, sobel, scharr, prewitt, threshold_local
import skimage.filters as filters
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.io import imread, imsave
from skimage import morphology
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage import draw

from scipy.spatial import ConvexHull
from skimage import transform as tf
import sys, os


# Distance in pixels to group same slope segments
SEGMENT_DISTANCE = 10

# debugging
COLS = 8
SAVE_OUTPUTS = False
DEBUG = False




im = None
steps = []
def add_image(tit):
    global im
    steps.append((tit, im.copy()))

## Displaying
def displ():
    rows = int((len(steps)-1)/COLS)+1
    fig, ax = plt.subplots(
        ncols=min(COLS,len(steps)),
        nrows=rows,
        sharex=True,
        sharey=True,
        squeeze=False,
        figsize=(12,7))


    for i, (tit, im) in enumerate(steps):
        r = int(i/COLS)
        c = i%COLS
        ax[r][c].imshow(im, cmap=plt.cm.gray)
        ax[r][c].set_title(tit)

        if (SAVE_OUTPUTS):
            imsave(tit+'-out.jpg', img_as_ubyte(im))



        ax[r][c].axis('off')
        ax[r][c].set_xticklabels([])
        ax[r][c].set_yticklabels([])
    plt.subplots_adjust(wspace=0, hspace=.1, left=0, bottom=0, right=1, top=.95)
    #plt.tight_layout()
    plt.show()

# Process an image
def grid_size(infile):
    fname = infile.split('/')[-1].strip()
    global im
    # read the image from disk
    original = imread(infile, flatten=True)
    im = original.copy()

    add_image(fname)

    # edge detection
    im = sobel(im)
    # blurring
    im = filters.gaussian(im, sigma=5)
    # thresholding: convert to binary rage
    loc = threshold_local(im, 31)
    im = im > loc

    if (DEBUG): add_image('Threshold')

    # detect straight lines longer than 150px
    segs = probabilistic_hough_line(
        im,
        threshold=30,
        line_length=200,
        line_gap=10)

    #segs = [seg for seg in segs if vertical(seg)]

    # draw the segments
    im[:] = 0 # set image to black
    for seg in segs:
        ((x1, y1), (x2, y2)) = seg
        rr,cc = draw.line(y1,x1,y2,x2)
        im[rr, cc] = 1

    if (DEBUG): add_image('Hough Lines')
    hh, vv = process_segments(segs)

    # draw the segments
    im[:] = 0 # set image to black

    num = 0
    for yy in hh:
        for yyy in yy:
            (_,y),_ = yyy
            rr,cc = draw.line(y,0,y,999)
            im[rr, cc] = 1
            num += 1
    for xx in vv:
        for xxx in xx:
            (x,_),_ = xxx
            rr,cc = draw.line(0,x,999,x)
            im[rr, cc] = 1
            num += 1

    if (DEBUG):
        add_image('Filtered Segs')
        # finally save the result
        displ()

    return len(vv)-1, len(hh)-1


def segcmp(seg):
    (a, b), (c, d) = seg
    if (vertical(seg)): return (a+c)/2
    else: return (b+d)/2


def process_segments(segs, dst=SEGMENT_DISTANCE):
    vsegs = [x for x in segs if vertical(x)]
    hsegs = [x for x in segs if horizontal(x)]

    vsegs = sorted(vsegs, key=segcmp)
    hsegs = sorted(hsegs, key=segcmp)
    h, v = [], []
    # vertical segments
    while vsegs:
        s = vsegs.pop()
        (a, _), _ = s
        found = False
        for cc in v:
            for (b, _), _ in cc:
                if abs(b-a) < SEGMENT_DISTANCE:
                    cc.append(s)
                    found = True
                    break
            if found: break
        if not found: v.append([s])

    # horizontal segments
    while hsegs:
        s = hsegs.pop()
        (_, a), _ = s
        found = False
        for cc in h:
            for (_, b), _ in cc:
                if abs(b-a) < SEGMENT_DISTANCE:
                    cc.append(s)
                    found = True
                    break
            if found: break
        if not found: h.append([s])
    hlen = [len(x) for x in h]
    vlen = [len(x) for x in v]
    return h, v


def horizontal(seg):
    return abs(slope(seg)) < 1/3

def vertical(seg):
    return abs(slope(seg)) > 3

def hvslope(seg):
    s = abs(slope(seg))
    return s > 100 or s < 0.01

def slope(seg):
    (x1, y1), (x2, y2) = seg
    dx, dy = x2-x1, y2-y1
    if (dx == 0):
        return float('inf')
    return dy/dx

def ccw(a,b,c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    return (cy-ay) * (bx-ax) > (by-ay) * (cx-ax)

# Return true if line segments AB and CD intersect
def intersect(s1,s2):
    a, b = s1
    c, d = s2
    return ccw(a,c,d) != ccw(b,c,d) and ccw(a,b,c) != ccw(a,b,d)



# Main
def main():
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], '<input-image>')
        exit(1)
    fname = infile.split('/')[-1].strip()
    print("Processing", fname)
    x, y = grid_size(sys.argv[1])
    print('Grid size (x,y): ' + str(x) + 'x' + str(y))



if __name__ == '__main__':
    main()
