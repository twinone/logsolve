import sys

from comm import PrintComm

# left, right, cy, up
calib = (65, 144, 110, 16)

CLICK_DST = 4


# tested on a 8x8 grid
# percentage of the screen the game actually occupies
PCT_W = 1

INV_X = 1
INV_Y = -1




class Sender:
    def __init__(self, pc, calib, gs):
        self.pc = pc
        self.calib = calib
        self.gs = gs

        self.width = abs(self.calib[1] - self.calib[0])

        self.cx = self.calib[0] + self.width / 2
        self.cy = self.calib[2]

        self.up = self.calib[3]

        cols, rows = self.gs
        self.cellsize = self.width * PCT_W / cols
        self.left = self.cx - cols / 2 * self.cellsize*INV_X
        self.top = self.cy - rows / 2 * self.cellsize*INV_Y


    # goto (row,col) (starting at 0)
    def goto(self, row, col):

        x = self.pc.x if not col else self.left + ((col+0.5)*self.cellsize)*INV_X
        y = self.pc.y if not row else self.top + ((row+0.5)*self.cellsize)*INV_Y
        self.pc.set_xy(x, y)


    def click(self):
        self.pc.click(CLICK_DST)

    def center(self):
        self.pc.set_xy(self.cx, self.cy)


    def cli(self):
        while True:
            try:
                line = input('> ')
            except EOFError:
                break

            split = line.split(' ')
            cmd = split[0]
            if (cmd == 'click'):
                self.click()
            if (cmd == 'dclick'):
                self.click()
                self.click()
            if (cmd == 'row'):
                row = int(split[1])
                self.goto(row, None)
            if (cmd == 'col'):
                col = int(split[1])
                self.goto(None, col)
            if (cmd == 'goto'):
                row = int(split[1])
                col = int(split[2])
                self.goto(row, col)
            if (cmd == ''):
                self.click()
            else:
                self.pc.write(line)






def main():
    # go to 0, 0
    print('Establishing connection to printer')
    fname = sys.argv[1]
    pc = PrintComm(fname)

    # start the calibration process by homing all
    print('Home all (G28)')
    pc.write('G28')

    pc.offset_z(calib[3]+CLICK_DST)

    s = Sender(pc, calib, (8,8))

    s.center()
    s.cli()





if __name__ == '__main__':
    main()
