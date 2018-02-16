#!/usr/bin/python2
# -*- coding: utf-8 -*-
###############################################################################
# Written by:       Forrest Koch (forrest.koch@unsw.edu.au)
# Organization:     Centre for Healthy Brain Ageing (UNSW)
# PyschoPy Version: 1.85.3
# Python Version:   2.7.5
###############################################################################
import os
import serial
from psychopy import core, gui, data, logging, visual, clock

from psychoblocks import const, experiment, routines, features

if (__name__ == '__main__'):
    app = experiment.Experiment('recall')

    # build the trial sequence and add to the app
    runCSV = data.importConditions(app.runfile)
    
    for line in runCSV:
        print(const.DEFAULT_STIMULI_FOLDER)
        print(line['image'])
        image = os.path.join(const.DEFAULT_STIMULI_FOLDER,line['image'])
        app.addRoutine(routines.RecallTrial(app,image,line['lname'],line['rname'],line['correct']))
        app.addRoutine(routines.ConfidenceTrial(app))

    # ready freddy go!
    app.run()
    # write out the logfile
    logging.flush()
