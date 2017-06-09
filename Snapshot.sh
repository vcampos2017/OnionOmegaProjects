#!/bin/sh
import os
import datetime
import time
now = time.strftime("%c")
## date and time representation for debugging
print "Current date & time " + time.strftime("%c")
camOutput = "fswebcam --no-banner --device /dev/video0 --jpeg 95 -r 1280x720 /root/grs/capture/" + str(time.time()) + ".jpg"
response = os.system(camOutput)
