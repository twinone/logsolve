from skimage.color import grey2rgb, rgb2grey
from skimage import img_as_ubyte
from skimage.filters import threshold_local, threshold_mean
from .cell import CellProcessor
import numpy as np
import matplotlib.pyplot as plt



def thresh_local_mean(im, gridsize, **kwargs):
    # for each im, inv, we want to do local thresholding
    # we need a big block size in order to get a good mean value
    # to compare to, but if it gets too big it's just like a global
    # thresholding

    # process kwargs
    opts = { 'offset': 0.1, 'blocksize': 501, 'method': 'mean', 'debug': False }
    for k in kwargs: opts[k] = kwargs[k]

    x, y = gridsize

    thresh = threshold_local(im, opts['blocksize'], method=opts['method'])
    #b = threshold_local(im, 501, method='mean', offset=0.1)

    black, white = im > thresh-opts['offset'], im < thresh+opts['offset']

    cpwhite = CellProcessor(white, x, y)
    cpblack = CellProcessor(black, x, y)

    areas = grey2rgb(img_as_ubyte(im.copy()))
    colors = grey2rgb(img_as_ubyte(im.copy()))

    out = np.zeros((x, y))

    # grey out the images
    for yy in range(y):
        for xx in range(x):
            rr, cc = cpwhite.cell_ellipse(xx, yy)
            areas[rr, cc] = np.array([255,255,255])
            iswhite = cpwhite.get_color(xx, yy) < 30
            isblack = cpblack.get_color(xx, yy) < 30
            rr, cc = cpwhite.cell_rect(xx, yy)
            if isblack:
                colors[rr, cc] = np.array([0,0,0])
                out[yy, xx] = 0
            elif iswhite:
                colors[rr, cc] = np.array([255,255,255])
                out[yy, xx] = 1
            else:
                colors[rr, cc] = np.array([127,127,127])
                out[yy, xx] = -1

    if (opts['debug']):
        fig, axes = plt.subplots(ncols=4, nrows=1, figsize=(10, 3))
        ax = axes.ravel()
        plt.gray()

        ax[0].imshow(im)
        ax[0].set_title('Original Image')
        ax[1].imshow(white)
        ax[1].set_title('white')
        ax[2].imshow(black)
        ax[2].set_title('black')
        ax[3].imshow(colors)
        ax[3].set_title('Detected colors')
        for a in ax:
            a.axis('off')
        plt.show()
    return out.astype(int)
