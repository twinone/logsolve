import logsolve as ls

from subprocess import Popen, PIPE, STDOUT



OUT_FILE = './image.jpg'

def process(fname):
    ls.log('Reading image')
    im = ls.imread(fname, flatten=True)
    ls.log('Undistorting')
    im = ls.undistort(im)
    ls.log('Calculating grid size...')
    gs = ls.gridsize(im)
    ls.log('Grid size: ', gs)
    ls.log('Calculating cell colors')
    colors = ls.thresh_local_mean(im, gs, debug=True)
    mat = ls.printmat(colors)
    ls.log("Problem matrix:")
    ls.log(mat)

    ls.log("Calculating solution...")

    p = Popen(['./solve'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    sol = p.communicate(input=mat.encode())[0]
    ls.log("Solution:")
    ls.log(sol.decode())


def serve():
    srv = ls.Server(OUT_FILE)
    srv.set_handlerfunc(process)
    srv.run('0.0.0.0')


def main():
    #serve()
    process('./image.jpg')

if __name__ == '__main__':
    main()
