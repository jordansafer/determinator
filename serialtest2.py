import serial
import imuValueExtractors
import math
import time
import config
import copy
from niceQ import *
import pymsgbox


def resetHighscores():
    config.power_highscore = 0
    config.distance_highscore = 0
    config.hangtime_highscore = 0


# function to make the readings
#This function returns another tuple
# ( PersonName, [ [ (Alt1, Acc1), (Alt2, Acc2), ... ],
#                  Readings from second set          ,
#                  Readings from third set           ,
#                               .....                  ]  )
def makeReadings(memory):
    # open a serial connection
    ser = serial.Serial('/dev/tty.usbserial-DA01QTU5')
    IM = imuValueExtractors

    resetHighscores()

    accels = []
    for i in xrange(3):
        accels.append(niceQ(memory))
    count = 0
    reads = 0
    prevacc = [0, 0, 0]


    config.power_current = 0
    config.distance_current = 0
    config.hangtime_current = 0

    accelList = []
    dataForML = []
    data = [0]
    while(1):
        reads += 1

        line = ser.readline()
        buffer = 6
        if(reads < buffer):
            print(buffer - reads)
            continue # throw the first few lines to be safe

        acc = IM.getAcceleration(line)
        #alt = IM.getAltitude(line)
        ang = IM.getAngles(line)
        accMag = ((acc[0]-prevacc[0])**2 + (acc[1]-prevacc[1])**2 +
                                                (acc[2]-prevacc[2])**2)**.5
        prevacc = acc
        if accMag == 0: #or (not config.collectingData):
            continue

        if(accMag > 1.5):
            count+=1
            data.append([accMag, acc[0], acc[1], acc[2], time.time()])
            dataForML.append((ang, accMag))
            accelList.append(accMag)
        elif len(accelList) > 0 and accelList[0] > 1.5 and count < 4:
            data.append([accMag, acc[0], acc[1], acc[2], time.time()])
            dataForML.append((ang, accMag)) #list of (altitudes, accelerations)
            accelList.append(accMag)
            count+=1
        else:
            if len(accelList) > 4:
                #print "accel time sustain satisfied"
                if max(accelList) > 4:
                    #print "min accel reached"
                    deltaTotalTime = data[len(data)-1][4] - data[0][4]
                    deltaT = data[2][4] - data[1][4]
                    #print "got to hangtime: ", deltaTotalTime
                    if(deltaTotalTime > 0.3):
                        #print "BALL WAS THROWN"
                        config.power_current = int(max(accelList)*9)
                        config.hangtime_current = deltaTotalTime
                        config.distance_current = max(accelList)*deltaT\
                                                  * deltaTotalTime * 32.2
                        #print "Power of throw (0-100): ",\
                        #                        config.power_current
                        #print "Hang time: ", config.hangtime_current
                        #print "Distance: ", config.distance_current

                        if(config.distance_current >
                                                config.distance_highscore):
                            config.distance_highscore = \
                                                config.distance_current
                        if(config.hangtime_current >
                                                config.hangtime_highscore):
                            config.hangtime_highscore = \
                                                config.hangtime_current
                        if(config.power_current >
                                                config.power_highscore):
                            config.power_highscore = \
                                                config.power_current

                        onePersonData = copy.deepcopy(dataForML)
                        if(config.new):
                            found = False
                            for i in xrange(len(config.dataset)):
                                if(config.dataset[i][0] == config.PersonName):
                                    config.dataset[i][1].append(onePersonData)
                                    found = True
                            if not found:
                                #Add a record of person's data to set
                                config.dataset.append((config.PersonName,
                                                            [onePersonData]))
                        else:
                            config.PersonName = analyze(onePersonData)
                        config.completed = True

                        time.sleep(1)

            #print data
            accelList = []
            data = []
            dataForML = []
            count = 0
            #print "accelList", accelList
            #print "data", data


# dataset contains people
# each person = (Name, data)
# data = [ (Persons Name, [ [ set1, set2, set3 ...  ] ] ) ,
# set = ([ang, ang, ang], acc)
def analyze(oneset):

    difference = 0.0
    result = (config.dataset[0][0], -1)

    for Person in config.dataset:

        for reading in Person[1]:
            readDif = 0.0
            #calculate the difference in altitudes and accelerations
            length = min(len(reading), len(oneset))
            for i in xrange(length):
                angdiff = 0
                for j in xrange(len(reading[i][0])):
                    angdiff += abs(reading[i][0][j] - oneset[i][0][j])
                accdiff = abs(reading[i][1] - oneset[i][1])
                readDif += angdiff + accdiff

            readDif /= length
            difference += readDif

        difference = difference / (len(Person))
        if (difference < result[1] or result[1] == -1):
            #Update as a tuple of new name, and new difference
            result = (Person[0], difference)
        difference = 0.0

    return result[0]


