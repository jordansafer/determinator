import string

# get the altitude
def getAltitude(line):
    altLen = 14  # length of Altitude(ft): is 13
    altI = string.find(line, "A") # the first letter in altitude
    start = altI + altLen
    finish = string.find(line, " ", start)
    if (start == -1): return 0
    return float(line[start:finish])


# get the acceleration
def getAcceleration(line):
    # get the first acceleration value
    accLen = 10  # length of Q values: is 10
    accI = string.find(line, "Q") # the first letter in Q values
    start = accI + accLen
    finish = string.find(line, " ", start)
    if (start == -1): return [0,0,0,0]
    result = [float(line[start:finish])]
    # get the remaining accleration values
    for i in xrange(3): # number of other values
        current = finish
        bar = string.find(line, "|", current)
        barlen = 2 # length of bar and space
        start = bar + barlen
        finish = finish = string.find(line, " ", start)
        if (start == -1): return [0,0,0,0]
        result.append(float(line[start:finish]))
    return result  


# get the Euler angles
def getAngles(line):
    # get the first angle
    angLen = 14  # length of Euler angles: is 14
    angI = string.find(line, "E") # the first letter in Euler
    start = angI + angLen
    finish = string.find(line, " ", start)
    if (start == -1): return [0,0,0]
    result = [float(line[start:finish])]
    # get the remaining accleration values
    for i in xrange(2): # number of other values
        current = finish
        bar = string.find(line, "|", current)
        barlen = 2 # length of bar and space
        start = bar + barlen
        finish = finish = string.find(line, " ", start)
        if (start == -1): return [0,0,0]
        result.append(float(line[start:finish]))
    return result  




