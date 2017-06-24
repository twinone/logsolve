#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from skimage.draw import set_color, polygon, line, ellipse
import matplotlib.pyplot as plt
import numpy as np
from skimage import img_as_ubyte
from skimage.color import grey2rgb


class CellProcessor:
    def __init__(self, im, x, y):
        self.im = img_as_ubyte(im)
        self.imrgb = grey2rgb(self.im)
        self.w, self.h  = im.shape
        self.x, self.y = x, y
        self.cellw = self.w / x
        self.cellh = self.h / y
        self._cell_colors()


    def get_color(self, x, y):
        return self.colormap[y][x]

    def _cell_colors(self, areaf=0.8):
        """
        Calculates the average color of all cells,
        using the inner areaf [0-1] factor
        """
        self.colormap = [[0 for x in range(self.y)]
                            for y in range(self.x)]

        for row in range(self.y):
            for col in range(self.x):
                rr, cc = self.cell_ellipse(col, row)
                self.colormap[row][col] = self.pixel_avg_grey(rr, cc)
                #self.im[rr, cc] = self.colormap[row][col]


    def cell_center(self, x, y):
        xx = x * self.cellw + self.cellw/2
        yy = y * self.cellh + self.cellh/2
        return xx, yy

    def cell_rect(self, x, y, areaf=1):
        padx = self.cellw * areaf
        pady = self.cellh * areaf
        fromx = round(x * self.cellw + padx)
        fromy = round(y * self.cellh + pady)
        tox = round(fromx + self.cellw - 2*padx)
        toy = round(fromy + self.cellh - 2*pady)
        r = np.array([fromy, fromy, toy, toy])
        c = np.array([fromx, tox, tox, fromx])
        return polygon(r, c)


    def cell_ellipse(self, x, y, areaf=0.8):
        rx = self.cellw * areaf/2
        ry = self.cellh * areaf/2
        cx, cy = self.cell_center(x, y)
        return ellipse(cy, cx, ry, rx)

    def pixel_avg_grey(self, rr, cc):
        color = 0
        size = 0
        for px in self.im[rr, cc]:
            size += 1
            color += px
        color /= float(size)
        return color
