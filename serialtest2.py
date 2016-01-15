import serial
import imuValueExtractors
import math
import time
import config

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
    count = 0
    reads = 0
    prevacc = [0, 0, 0]

    accelList = []
    dataForML = []
    data = [0]
    while(1):
        reads += 1

        line = ser.readline()
        if(reads < 6):
            print 6 - reads
            continue # thro:w the first few lines to be safe

        acc = IM.getAcceleration(line)
        #alt = IM.getAltitude(line)
        #ang = IM.getAngles(line)
        accMag = ((acc[0]-prevacc[0])**2 + (acc[1]-prevacc[1])**2 +
                                                (acc[2]-prevacc[2])**2)**.5
        #print "AccelMag ", accMag, "\t", len(accelList)
        prevacc = acc
        alt = 0
	#print accelList
        #print config.collectingData
        if accMag == 0: #or (not config.collectingData):
            continue
        #print acc[0], " ", acc[1], " ", acc[2]
        if(accMag > 1.5):
            count+=1
            data.append([accMag, acc[0], acc[1], acc[2], alt, time.time()])
            dataForML.append((alt, accMag))
            accelList.append(accMag)
	elif len(accelList) > 0 and accelList[0] > 1.5 and count < 4:
            data.append([accMag, acc[0], acc[1], acc[2], alt, time.time()])
            dataForML.append((alt, accMag))
            accelList.append(accMag)
            count+=1
        else:
            if len(accelList) > 4:
	    #print "accel time sustain satisfied"
                if max(accelList) > 4:
                #print "min accel reached"
                    if True:#total1<total2 and total2>total3:
                        #print "bell curve satisfied"
                        baseAlt = data[0][4]
                        maxAlt = baseAlt
                        minAlt = baseAlt
                        for i in range(0, len(data)):
                            if(maxAlt < data[i][4]):
                                maxAlt = data[i][4]
                            if(minAlt > data[i][4]):
                                minAlt = data[i][4]
                        #print "maxalt ", maxAlt, " minalt ", minAlt
                        deltaAlt = maxAlt - baseAlt

                        if baseAlt-minAlt > deltaAlt:
                            deltaAlt = baseAlt - minAlt
                        #print "deltaAlt ", deltaAlt
                        deltaTotalTime = data[len(data)-1][5] - data[0][5]
                        deltaT = data[2][5] - data[1][5]
                        deltaA1 = abs(data[1][1] - acc[0])
                        deltaA2 = abs(data[1][2] - acc[1])
                        deltaA3 = abs(data[1][3] - acc[2])
                        deltaA4 = abs(data[1][0])
                        deltaA6 = (deltaA1**2 + deltaA3**2)**.5
                        deltaA7 = (deltaA1**2 + deltaA2**2 + deltaA3**2)**.5
                        #print "got to hangtime: ", deltaTotalTime
                        if(deltaTotalTime > 0.3):#deltaAlt > 0):
                            print "BALL WAS THROWN"
                            #print "Altitude Change: ", deltaAlt
                            print "Power of throw (0-100): ", int(max(accelList)*9)
                            print "Hang time: ", deltaTotalTime
                            print "Distance: ", max(accelList)*deltaT * deltaTotalTime * 32.2
                            print "Distance: ", deltaA6*deltaT * deltaTotalTime * 32.2
                            print "Distance: ", deltaA7*deltaT * deltaTotalTime * 32.2
                            #print "list lenL ", len(accelList)
                            #print "accelList ", accelList
			    #onePersonData = list(dataForML)
                            #if(config.new):
                            #    config.dataset.append( (config.PersonName, onePersonData) )
                            #    #Add a record of person's data to set
                            #else:
                            #    config.PersonName = analyze(onePersonData)
                            #config.completed = True
                        #print data
            accelList = []
            data = []
            dataForML = []
            count = 0
            #print "accelList", accelList
            #print "data", data



                


#
def analyze(oneset):

    difference = 0.0
    result = (config.dataset[0][0], 99999999999.9)

    for Person in config.dataset:

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


