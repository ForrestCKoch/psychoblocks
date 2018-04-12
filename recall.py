#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
###############################################################################
# Written by:       Forrest Koch (forrest.koch@unsw.edu.au)
# Organization:     Centre for Healthy Brain Ageing (UNSW)
# PyschoPy Version: 1.85.3
# Python Version:   2.7.5
###############################################################################
# This script runs the recall task component of the facename pair task.
# For each face, the participant will be prompted to select the correct choice between
# two names, and to rate their confidence 'high/low'.
# There is no enforced time limit.  The program will wait for input from the response box
import os
import sys
import serial
from psychopy import core, gui, data, logging, visual, clock

from psychoblocks import const, experiment, routines, features

if (__name__ == '__main__'):

    os.chdir(os.path.dirname(sys.argv[0]))

    app = experiment.Experiment('recall')

    # build the trial sequence and add to the app
    runCSV = data.importConditions(app.runfile)
    
    for line in runCSV:
        image = os.path.join(const.DEFAULT_STIMULI_FOLDER,line['image'])
        app.addRoutine(routines.RecallTrial(app,image,line['lname'],line['rname'],line['correct']))
        app.addRoutine(routines.ConfidenceTrial(app))

    # ready freddy go!
    app.run()
    # write out the logfile
    logging.flush()
