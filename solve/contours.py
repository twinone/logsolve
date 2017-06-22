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





import numpy as np
import matplotlib.pyplot as plt

from skimage import measure
from skimage.io import imread, imsave



r = imread('../capture/test/galaxies0-out.jpg')

# edge detection
r = sobel(r)
# blurring
r = filters.gaussian(r, sigma=3)
# thresholding: convert to binary rage
loc = threshold_local(r, 501)
r = r > loc

# Find contours at a constant value of 0.8
contours = measure.find_contours(r, 1.0)

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(r, interpolation='nearest', cmap=plt.cm.gray)

for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()
