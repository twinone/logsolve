import sys
import time

from core.comm import PrintComm

BED_SIZE = (220, 220)


def calib(f):
    line = ""
    while line != 0:
        try:
            line = int(input('> '))
        except EOFError:
            break
        except:
            print("Enter a valid number")
            continue
        f(line)

def main():
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], '<serial>')
        return


    print('Establishing connection to printer')
    fname = sys.argv[1]
    pc = PrintComm(fname)

    # start the calibration process by homing all
    print('Home all (G28)')
    pc.write('G28')

    print('Centering (20mm up for safety)')
    pc.offset_z(20)

    x, y = BED_SIZE
    bed_cx, bed_cy = x/2, y/2
    pc.set_xy(bed_cx, bed_cy)

    print('Align the touch tip to the current edge.')
    print('Enter mm to move in x axis, 0 to end')
    print('Calibrating LEFT edge')
    calib(lambda x: pc.offset_xy(x, 0))
    left = pc.x
    print('Calibrating RIGHT edge')
    calib(lambda x: pc.offset_xy(x, 0))
    right = pc.x

    # go to the center of the x axis
    cx = int((left+right)/2)
    pc.set_xy(cx, pc.y)

    print('Calibrating TOP edge')
    calib(lambda x: pc.offset_xy(0, x))
    top = pc.y
    print('Calibrating BOTTOM edge')
    calib(lambda x: pc.offset_xy(0, x))
    bottom = pc.y

    print('Now center vertically on the game grid')
    calib(lambda x: pc.offset_xy(0, x))
    game_cy = pc.y


    print('Calibrated:', (left, right, top, bottom, game_cy))
    cy = int((top+bottom)/2)
    pc.set_xy(cx, cy)




if __name__ == '__main__':
    main()
