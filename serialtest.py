import serial
import imuValueExtractors
import math

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

# function to make the readings
def makeReadings(): 
    # open a serial connection
    ser = serial.Serial('/dev/tty.usbserial-DA01P1HX')
    IM = imuValueExtractors

    accels = []
    for i in xrange(4):
        accels.append(niceQ(10))

    reads = 0

    while(1):
        reads += 1
        
        line = ser.readline()
        if(reads < 6):
            print 6 - reads
            continue # throw the first few lines to be safe
        
        acc = IM.getAcceleration(line)
        delta = 0
        for i in xrange(4):
            dif = abs(accels[i].avgQ() - acc[i])
            delta += dif
            accels[i].pushQ(acc[i])
        if delta > .6:
            print "Throw"
        print delta


makeReadings()


