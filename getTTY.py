#!/usr/local/bin/python2.7
from glob import glob

if __name__ == '__main__':

    old = set(glob('/dev/tty*'))
    print('Please insert the device')
    new = set(glob('/dev/tty*'))
    while(len(new)==len(old)):
        new = set(glob('/dev/tty*'))
    print('The device is location: ' + list(new-old)[0])
        
