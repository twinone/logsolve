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

    print('Centering (50mm up for safety)')
    pc.offset_z(50)

    x, y = BED_SIZE
    bed_cx, bed_cy = x/2, y/2
    pc.set_xy(bed_cx, bed_cy)

    print('Align the touch tip to the current edge.')
    print('Enter mm to move in axis, 0 to end')

    print('Move Z down until it touches the screen')
    calib(lambda x: pc.offset_z(x))
    up = pc.z

    pc.offset_z(5)

    print('Center vertically on the game grid')
    calib(lambda x: pc.offset_xy(0, x))
    game_cy = pc.y

    print('Center on the LEFT edge of the grid')
    calib(lambda x: pc.offset_xy(x, 0))
    left = pc.x

    print('Center on the RIGHT edge of the grid')
    calib(lambda x: pc.offset_xy(x, 0))
    right = pc.x




    print('Calibrated:', (left, right, game_cy, up))
    game_cx = (left+right)/2
    pc.set_xy(game_cx, game_cy)




if __name__ == '__main__':
    main()
