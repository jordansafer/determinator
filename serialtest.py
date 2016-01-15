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

#function which gathers data over one throw
#This function returns a list of readings over one throw
# [(Alt1, Acc1), (Alt2, Acc2), ... ]
def gatherData():
    thrown = True
    oneset = []

    while(thrown):
        line = ser.readline()
        
        acc = IM.getAcceleration(line) #[acc1, acc2, acc3]
        alt = IM.getAltitude(line)     #alt
        
        oneset.append((alt,acc))

        #See if ball stops
        delalt = abs(heights.avgQ() - alt)
        delta = 0

        heights.pushQ(alt)
        for i in xrange(3):
            dif = abs(accels[i].avgQ() - acc[i])
            delta += dif
            accels[i].pushQ(acc[i])
        if delta > 2.5:
            print "Delta:", delta
            if delta > 4:
                print "Alt:", delalt
                if delalt > 1.5:
                   thrown = False
    
    return oneset

# function to make the readings
#This function returns another tuple
# ( PersonName, [ [ (Alt1, Acc1), (Alt2, Acc2), ... ],
#                  Readings from second set          ,
#                  Readings from third set           ,
#                               .....                  ]  )
#
#
def makeReadings(memory): 
    # open a serial connection
    ser = serial.Serial('/dev/tty.usbserial-DA01P1HX')
    IM = imuValueExtractors

    accels = []
    for i in xrange(3):
        accels.append(niceQ(memory))
    heights = niceQ(memory)

    reads = 0
    thrown = False

    onePersonData = []

    while(1): #Need some way of terminating this loop using collectingData
        reads += 1
        
        line = ser.readline()
        if(reads < 6):
            print 6 - reads
            continue # throw the first few lines to be safe
        
        acc = IM.getAcceleration(line) #[acc1, acc2, acc3]
        alt = IM.getAltitude(line)     #alt
        
        delalt = abs(heights.avgQ() - alt)
        delta = 0

        heights.pushQ(alt)
        for i in xrange(3):
            if(reads > memory + 5):
                dif = abs(accels[i].avgQ() - acc[i])
                delta += dif
            accels[i].pushQ(acc[i])
        if delta > 2.5:
            print "Delta:", delta
            if delta > 4:
                print "Alt:", delalt
                if delalt > 1.5:
                   thrown = True

        if thrown:
            oneset = gatherData()
            onePersonData.append(oneset)
            thrown = False
                
     dataset.append( (PersonName, onePersonData) ) #Add a record of person's data to set

#
def analyze(oneset):

    difference = 0.0
    result = (dataset[0][0], 99999999999.9)

    for Person in dataset:

        bestmatch = Person[1][0] #The closest matching data set
        
        #find the data set with closest length
        for reading in Person[1]:
            if (abs(len(reading) - len(oneset))) < (abs(len(bestmatch) - len(oneset))):
                bestmatch = reading

        #calculate the difference in altitudes and accelerations
        for i in range(min(len(bestmatch), len(oneset))):
            altdiff = abs(bestmatch[i][0] - oneset[i][0])
            accdiff = abs(bestmatch[i][1] - oneset[i][1])
            difference += altdiff
            difference += accdiff
        
        if (difference < result[1]):
            result = (Person[0], difference) #Update as a tuple of new name, and new difference

     return result[0]

#This function takes readings for a plain throw, no data collection occurs
#It then compares the readings to our global data set, and tries to match up the
#readings to the closest one.
def plainThrow:
    # open a serial connection
    ser = serial.Serial('/dev/tty.usbserial-DA01P1HX')
    IM = imuValueExtractors

    accels = []
    for i in xrange(3):
        accels.append(niceQ(memory))
    heights = niceQ(memory)

    reads = 0
    thrown = False

    while(1): #Need some way of terminating this loop using collectingData
        reads += 1
        
        line = ser.readline()
        if(reads < 6):
            print 6 - reads
            continue # throw the first few lines to be safe
        
        acc = IM.getAcceleration(line) #[acc1, acc2, acc3]
        alt = IM.getAltitude(line)     #alt
        
        delalt = abs(heights.avgQ() - alt)
        delta = 0

        heights.pushQ(alt)
        for i in xrange(3):
            if(reads > memory + 5):
                dif = abs(accels[i].avgQ() - acc[i])
                delta += dif
            accels[i].pushQ(acc[i])
        if delta > 2.5:
            print "Delta:", delta
            if delta > 4:
                print "Alt:", delalt
                if delalt > 1.5:
                   thrown = True

        if thrown:
            oneset = gatherData()
            PersonName = analyze(oneset)
            return PersonName


