
import sys
import serial
import time

SPEED_XY = 2000  # mm/min
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
        z = int(z)
        cmd = 'G1 Z{0} F{1}'.format(z, SPEED_Z)
        self.z = z
        self.write(cmd)

    def set_xy(self, x, y):
        x, y = int(x), int(y)
        cmd = 'G1 X{0} Y{1} F{2}'.format(x, y, SPEED_XY)
        self.x, self.y = x, y
        self.write(cmd)

    def offset_z(self, z):
        self.set_z(self.z+z)

    def offset_xy(self, x, y):
        self.set_xy(self.x+x, self.y+y)


    def click(self, z):
        self.offset_z(-z)
        self.offset_z(z)


    def swipe(self, z, x, y):
        self.offset_z(-z)
        self.offset_xy(x, y)
        self.offset_z(z)

    def swipe_to(self, z, x, y):
        self.offset_z(-z)
        self.set_xy(x, y)
        self.offset_z(z)





    def write(self, cmd):
        #print("CMD: ", cmd)
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
            #print(line)

    def close(self):
        self.port.close()

    def cli(self):
        while True:
            try:
                line = input('> ')
            except EOFError:
                break
            self.write(line)




def main():
    fname = sys.argv[1]
    pc = PrintComm(fname)
    pc.cli()

if __name__ == '__main__':
    main()
