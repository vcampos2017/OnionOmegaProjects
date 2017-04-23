from OmegaExpansion import oledExp
#https://www.controleverything.com/content/Humidity
from OmegaExpansion import onionI2C
 
import os
import time
import datetime
import sys

#Start OLED
oledExp.driverInit()

while True:
      
        i2c 	= onionI2C.OnionI2C(0)
        # set the verbosity
        i2c.setVerbosity(1)
        # HIH7130 address, 0x27(39)
        # Read data back from 0x00(00), 4 bytes
        # humidity MSB, humidity LSB, temp MSB, temp LSB
        data = i2c.readBytes(0x27, 0x00, 4)
        # Convert the data to 14-bits
        humidity = ((((data[0] & 0x3F) * 256) + data[1]) * 100.0) / 16383.0
        temp = (((data[2] & 0xFF) * 256) + (data[3] & 0xFC)) / 4
        cTemp = (temp / 16384.0) * 165.0 - 40.
        fTemp = cTemp * 1.8 + 32
        # Output data to screen with pause between in print/write
        oledExp.setCursor(0,0)
        oledExp.write(time.strftime("%H:%M:%S"))
        print time.strftime("%H:%M:%S")
        time.sleep(3)
        oledExp.setCursor(1,0)
        oledExp.write("Rel Humidity : %.2f %%" %humidity)
        print "Relative Humidity : %.2f %%" %humidity
        time.sleep(3)
        oledExp.setCursor(3,0)
        oledExp.write("Celsius : %.2f C" %cTemp)
        time.sleep(3)
        print "Temperature in Celsius : %.2f C" %cTemp
        oledExp.setCursor(4,0)
        oledExp.write("Fahrenheit : %.2f F" %fTemp)
        print "Temperature in Fahrenheit : %.2f F" %fTemp
        time.sleep(3)
        
