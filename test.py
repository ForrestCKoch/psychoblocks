#!/usr/bin/python2
from psychopy import core
from facename import Facename
from routines import InstructScreen

x = Facename()
y = InstructScreen(x.clock,x.participantWindow,x.expInfo['participantFrameRate'],x.expHandler)
y.run()
