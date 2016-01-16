import string

############## IMU and Altimeter information access module #########
# This module defines functions to take advantage of data reaped by
# sensor on the ball and transmitted from the xBee.  The functions
# rely on a predetermined format. Each value is preceeded by an 
# appropriate label.
#
# The functions operate by finding the corresponding label for a value
# and adding the length of the label to find the value. In the case
# where there are multiple values, a loop is used to find additional
# following values and return them as well.
#####################################################################

# get the altitude
def getAltitude(line):
    altLen = 14  # length of Altitude(ft): is 13
    altI = string.find(line, "Al") # the first letters in altitude
    # throw a value if bad data is received
    if (altI == -1): return 0 
    
    start = altI + altLen
    finish = string.find(line, " ", start)
    return float(line[start:finish])


# get the acceleration
def getAcceleration(line):
    # get the first acceleration value
    accLen = 14  # length of acceleration is 14
    accI = string.find(line, "Ac") # the first letters in Acceleration
    start = accI + accLen
    finish = string.find(line, ".", start)+2
    try:
        result = [float(line[start:finish])]
    except: 
        return [0, 0, 0]
    # get the remaining accleration values
    for i in xrange(2): # number of other values
        current = finish
        space = string.find(line, " ", current)
        spacelen = 1 # length of space
        start = space + spacelen
        finish = string.find(line, ".", start) + 2
        try:
            result.append(float(line[start:finish]))
        except:
            return [0, 0, 0]
    return result

# Euler angles: -112.68 | -26.39 | 8.87
# get the Euler angles
def getAngles(line):
    # get the first angle
    angLen = 14 # length of Euler angles text
    angI = string.find(line, "Eu") # first letters in Euler
    start = angI + angLen
    finish = string.find(line, ".", start) + 2
    try:
        result = [float(line[start:finish])]
    except:
        return [0, 0, 0]

    # get remaining angles
    for i in xrange(2):
        current = finish
        space = string.find(line, " ", current)
        spacelen = 3 # length of " | "
        start = space + spacelen
        finish = string.find(line, ".", start) + 2
        try:
            result.append(float(line[start:finish]))
        except:
            return [0, 0, 0]
    return result

