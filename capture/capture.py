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



COLS = 8
SAVE_OUTPUTS = True




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
            imsave('out/'+tit+'.jpg', img_as_ubyte(im))



        ax[r][c].axis('off')
        ax[r][c].set_xticklabels([])
        ax[r][c].set_yticklabels([])
    plt.subplots_adjust(wspace=0, hspace=.1, left=0, bottom=0, right=1, top=.95)
    #plt.tight_layout()
    plt.show()





# Process an image
def process(fname):
    global im
    # read the image from disk
    im = imread('test/'+fname+'.jpg', flatten=True)
    add_image(fname)

    # edge detection
    im = sobel(im)
    # blurring
    im = filters.gaussian(im, sigma=1)
    # thresholding: convert to binary image
    loc = threshold_local(im, 57)
    im = im > loc
    add_image('Threshold')

    # detect straight lines longer than 150px
    segs = probabilistic_hough_line(
        im,
        threshold=10,
        line_length=150,
        line_gap=5)

    # draw the segments
    im[:] = 0 # set image to black
    for seg in segs:
        ((x1, y1), (x2, y2)) = seg
        rr,cc = draw.line(y1,x1,y2,x2)
        im[rr, cc] = 1
    add_image('Hough Lines')

    # Calculate the connected components (intersecting groups)
    ccs = []
    while segs:
        s = segs.pop()
        found = False
        for cc in ccs:
            for ss in cc:
                if intersect(s, ss):
                    cc.append(s)
                    found = True
                    break
            if found: break
        if not found: ccs.append([s])

    # get the one with most segments (the one with the grid)
    ccs.sort(key=len)
    ccs = ccs[::-1]

    # get coordinates for each segment
    coords = []
    for seg in ccs[0]:
        (x1, y1), (x2,y2) = seg
        coords.append([x1, y1])
        coords.append([x2, y2])

    # calculate the convex hull or 'envelope' surrounding segments
    hull = ConvexHull(np.array(coords))
    indices = hull.vertices
    im[:] = 0
    for i in indices:
        x, y = coords[i]
        rr, cc = draw.circle(y,x,1)
        im[rr, cc] = 1
    im = morphology.convex_hull_image(im)
    print(fname + ":", "number of hull vertices:", len(indices))

    hullcoords = [coords[i] for i in indices]
    # calculate the 4 vertices of the trapezoid
    # these are the vertices that are most top-left, top-right,
    # bottom-left and bottom-right
    # we can easily calculate them maximizing (+,-)(x,y)
    # for example: the top left corner will be the vertex
    # whose -x-y is maximum
    def findmax(fx, fy):
        maximum = None
        res = None
        for (x,y) in hullcoords:
            if maximum == None or x*fx + y*fy > maximum:
                maximum = x*fx+y*fy
                res = x, y
        return res
    verts = [
        findmax(-1,-1),
        findmax(-1, 1),
        findmax( 1,-1),
        findmax( 1, 1),
    ]

    # display the actual vertices a bit bigger
    for (x, y) in verts:
        rr, cc = draw.circle(y,x,10)
        im[rr, cc] = 1
    add_image('Hull')




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
    #names = ['pearl', 'range', 'tents', 'unruly']
    names = ['fifteen', 'galaxies', 'keen', 'loopy']
    for name in names:
        process(name+'0')
    #process('test/1.jpg')
    #process('test/test3.jpg')
    #process('test/test6.jpg')

    displ()



if __name__ == '__main__':
    main()
