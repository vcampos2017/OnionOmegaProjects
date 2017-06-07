#https://www.controleverything.com/content/Humidity
from OmegaExpansion import onionI2C
# MiniWeather tests running two ControlEverything Sensors from One Board
# Results are printed to the screen
import os
import time
import datetime
import sys
import requests

while True:
        # Get I2C bus
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
        # LPS25HB address, 0x5C(92)
        # Select Control register, 0x20(32)
        # 0x90(144)	Active mode, Continous update
        i2c.writeByte(0x5C, 0x20, 0x90)
        time.sleep(0.1)
        # LPS25HB address, 0x5C(92)
        # Read data back from 0x28(40), with Command register, 0x80(128)
        # 3 bytes, Pressure LSB first
        data =i2c.readBytes(0x5C, 0x28 | 0x80, 3)
        # Convert the data to hPa
        pressure = (data[2] * 65536 + data[1] * 256 + data[0]) / 4096.0
        #Convert data to inHg
        inHgPressure = pressure * 0.0295300
        # Output data to screen with pause between in print/write
        print time.strftime("%H:%M:%S")
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        time.sleep(3)
        print "Relative Humidity : %.2f %%" %humidity
        time.sleep(3)
        print "Temperature in Celsius : %.2f C" %cTemp
        time.sleep(3)
        print "Barometric Pressure is : %.2f hPa" %pressure
        print "Barometric Pressure is : %.2f inHg" %inHgPressure
        print "Temperature in Fahrenheit : %.2f F" %fTemp
        time.sleep(3)
        #Send Data to Ubidots
        payload = {'temperature': fTemp, 'humidity': humidity, 'barometricpressure':pressure, 'inHgPressure': inHgPressure, 'celTemperature': cTemp }
        r = requests.post('http://things.ubidots.com/api/v1.6/devices/YOUR-DEVICE-NAME-Here/?token=YOUR-TOKEN-HERE', data=payload)
        print "Sent data to Ubidots"
        print data
        break
