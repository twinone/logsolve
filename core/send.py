import sys

from comm import PrintComm

# left, right, top, bottom, center_y, up
calib = (57, 146, 177, 22, 103, 13)


# tested on a 8x8 grid
# percentage of the screen the game actually occupies
PCT_W = 0.9

INV_X = 1
INV_Y = -1




class Sender:
    def __init__(self, pc, calib, gs):
        self.pc = pc
        self.calib = calib
        self.gs = gs

        self.width = abs(self.calib[1] - self.calib[0])
        self.height = abs(self.calib[3] - self.calib[2])

        self.cx = self.calib[0] + self.width / 2
        self.cy = self.calib[4]

        self.z_dst = self.calib[5]

        cols, rows = self.gs
        self.cellsize = self.width * PCT_W / cols
        self.left = self.cx - cols / 2 * self.cellsize*INV_X
        self.top = self.cy - rows / 2 * self.cellsize*INV_Y


    # goto (row,col) (starting at 0)
    def goto(self, row, col):
        x = self.left + ((col+0.5)*self.cellsize)*INV_X
        y = self.top + ((row+0.5)*self.cellsize)*INV_Y
        self.pc.set_xy(x, y)


    def click(self):
        self.pc.click(self.z_dst)





def main():
    # go to 0, 0
    print('Establishing connection to printer')
    fname = sys.argv[1]
    pc = PrintComm(fname)

    # start the calibration process by homing all
    print('Home all (G28)')
    pc.write('G28')

    pc.offset_z(20)

    s = Sender(pc, calib, (8,8))

    s.goto(1,3)
    s.click()




if __name__ == '__main__':
    main()
