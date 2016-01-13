# 'pip install serial' before running this

import serial

ser = serial.Serial('/dev/tty.usbserial-DA01P1HX')

while(1):
      line = ser.readline()
      print(line)


