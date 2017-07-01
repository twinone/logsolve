import logsolve as ls

def main():
    print('Undistorting')
    im = ls.undistort_from_arg()
    print('Calculating grid size...')
    gs = ls.gridsize(im)
    print('Grid size: ', gs)
    print('Calculating cell colors')
    colors = ls.thresh_local_mean(im, gs)
    out = ls.printmat(colors)
    print(out)


if __name__ == '__main__':
    main()
