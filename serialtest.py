import serial
import imuValueExtractors
import math

ser = serial.Serial('/dev/tty.usbserial-DA01P1HX')
IM = imuValueExtractors

class niceQ:
    def __init__(self, size):
        self.index = 0
        self.size = size
        self.vals = size*[0]

    def pushQ(self, val):
        self.vals[self.index] = val
        self.index = (self.index + 1) % self.size

    def avgQ(self):
        return sum(self.vals)/self.size


accels = niceQ(10)
reads = 0

while(1):
    line = ser.readline()
    acc = IM.getAcceleration(line)
    total = (acc[0]**2 + acc[1]**2 + acc[2]**2 + acc[3]**2)**.5
    delta = abs(accels.avgQ() - total)
    print total
    if (reads > 30) and delta > .4:
        pass#print "Throw!", delta
    accels.pushQ(total)
    reads += 1

        



