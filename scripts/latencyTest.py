#!/usr/bin/python

import serial
import time
import numpy

diffs = list()
count = 0
s = serial.Serial('/dev/ttyACM0',baudrate=57600, timeout=0)
s.reset_input_buffer()

prev = time.time()
while(count < 100):
    data = s.read()
    if data:
        curr = time.time()
        diffs.append(curr-prev)
        prev = curr
        count += 1

print("mean:",numpy.mean(diffs))
print("stdv:",numpy.std(diffs))
