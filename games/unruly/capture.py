import logsolve as ls

def main():
    ls.log('Undistorting')
    im = ls.undistort_from_arg()
    ls.log('Calculating grid size...')
    gs = ls.gridsize(im)
    ls.log('Grid size: ', gs)
    ls.log('Calculating cell colors')
    colors = ls.thresh_local_mean(im, gs)
    out = ls.printmat(colors)
    print(out)


if __name__ == '__main__':
    main()
