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
SEGMENT_DISTANCE = 20

# debugging
COLS = 8
SAVE_OUTPUTS = True
DEBUG = True




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
def process(infile, outfile):
    fname = infile.split('/')[-1].strip()
    print("Processing",fname)
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

    # draw the segments
    im[:] = 0 # set image to black

    # filter slopes
    #segs = [seg for seg in segs if hvslope(seg)]

    for seg in segs:
        ((x1, y1), (x2, y2)) = seg
        rr,cc = draw.line(y1,x1,y2,x2)
        im[rr, cc] = 1

    process_segments(segs)

    if (DEBUG): add_image('Hough Lines')
    im = morphology.opening(im)


    # finally save the result
    print("Saving to ", outfile)
    imsave(outfile, im)

    displ()

def process_segments(segs, dst=SEGMENT_DISTANCE):
    vsegs = [x for x in segs if vertical(x)]
    hsegs = [x for x in segs if horizontal(x)]

    h, v = [], []
    # vertical segments
    for seg in vsegs:
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
    for seg in hsegs:
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
    print("grid size:: ", len(v)-1, len(h)-1)
    print("h, v group sizes: ", hlen, vlen)


def horizontal(seg):
    return abs(slope(seg)) < 0.01

def vertical(seg):
    return abs(slope(seg)) > 100

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
    if len(sys.argv) == 2 and sys.argv[1].lower().strip('-') == 'test':
        exit(test())

    if len(sys.argv) < 3:
        print("Usage:", sys.argv[0], '<input-image> <output-image>')
        exit(1)
    [i, o] = sys.argv[1:3]
    process(i, o)

def test():
    files = os.listdir('test')
    try:
        os.mkdir(TEST_DIR + 'out')
    except:
        pass

    for f in files:
        split = f.split('.')
        if (len(split) == 1):
            continue
        of = ''.join(split[:-1]) + '-out.' + split[-1]
        try:
            inf = TEST_DIR + f
            outf = TEST_DIR + of
            process(inf, outf)
        except Exception as e:
            print("Exception processing file", f, e)




if __name__ == '__main__':
    main()
