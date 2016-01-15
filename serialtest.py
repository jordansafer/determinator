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
def makeReadings(memory): 
    # open a serial connection
    ser = serial.Serial('/dev/tty.usbserial-DA01P1HX')
    IM = imuValueExtractors


    accels = []
    for i in xrange(3):
        accels.append(niceQ(memory))
    heights = niceQ(memory)

    reads = 0

    while(1):
        reads += 1
        
        line = ser.readline()
        if(reads < 6):
            print 6 - reads
            continue # throw the first few lines to be safe
        
        acc = IM.getAcceleration(line)
        alt = IM.getAltitude(line)
        
        delalt = abs(heights.avgQ() - alt)
        delta = 0

        heights.pushQ(alt)
        for i in xrange(3):
            if(reads > 20):
                dif = abs(accels[i].avgQ() - acc[i])
                delta += dif
            accels[i].pushQ(acc[i])
        if delta > 5 and delalt > 1:
            print "Throw"
        print delta



