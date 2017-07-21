
import sys
import serial
import time

UP_DST = 3  # mm
SPEED_XY = 1200  # mm/min
SPEED_Z = 1200  # mm/min

class PrintComm:
    def __init__(self, port):
        self.x = self.y = self.z = 0
        try:
            self.port = serial.Serial(port, 115200)
            time.sleep(5)
        except:
            print("Could not open port " + port)
            sys.exit(1)

    def set_z(self, z):
        cmd = 'G1 Z{0} F{1}'.format(z, SPEED_Z)
        self.z = z
        self.write(cmd)

    def set_xy(self, x, y):
        cmd = 'G1 X{0} Y{1} F{2}'.format(x, y, SPEED_XY)
        self.x, self.y = x, y
        self.write(cmd)

    def offset_z(self, z):
        self.set_z(self.z+z)

    def offset_xy(self, x, y):
        self.set_xy(self.x+x, self.y+y)


    def up(self):
        self.offset_z(UP_DST)
    def down(self):
        self.offset_z(-UP_DST)


    def write(self, cmd):
        try:
            command = (cmd + "\n").encode('utf-8')
            self.port.write(b"\n")
            self.port.write(command)
            self.port.flush()
            self.wait_for('ok')
        except Exception as e:
            print("Error", e)

    def wait_for(self, want):
        line = ""
        while line != (want+'\n').encode():
            line = self.port.readline()

    def close(self):
        self.port.close()


def main():
    fname = sys.argv[1]
    pc = PrintComm(fname)

    while True:
        try:
            line = input('> ')
        except EOFError:
            break
        pc.write(line)
    pc.close()

if __name__ == '__main__':
    main()
