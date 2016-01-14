import serial
import string
import imuValueExtractors


ser = serial.Serial('/dev/tty.usbserial-DA01P1HX')
IM = imuValueExtractors

while(1):
    line = ser.readline()
    print line, IM.getAltitude(line), IM.getAcceleration(line), IM.getAngles(line)



