#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
###############################################################################
# Written by:       Forrest Koch (forrest.koch@unsw.edu.au)
# Organization:     Centre for Healthy Brain Ageing (UNSW)
# PyschoPy Version: 1.85.3
# Python Version:   2.7.5
###############################################################################
# This script implements the main task component of the face name pair task.
# Participants will be shown a series of face name pairs for which they will
# be asked to indicate whether they feel the face is a good fit for the name.
import os
import sys
import serial
from psychopy import core, gui, data, logging, visual, clock

from psychoblocks import const, experiment, routines, features

TRIAL_DURATION = 4.5
ISI = 0.5 # InterStimulus Interval
REST_DURATION = 16
TR=2.3

const.DEFAULT_EXAMINER_SCREEN = 'no'
const.DEFAULT_FULLSCREEN = 'yes'
const.DEFAULT_PORT = '/dev/tty.wchusbserial1420'
const.DEFAULT_RUN_FILE = 's1r1.csv'
const.DEFAULT_MODE = 'test'

if (__name__ == '__main__'):
    # make sure we start out in the right directory
    os.chdir(os.path.dirname(sys.argv[0]))

    app = experiment.Experiment('facename')
    app.addRoutine(routines.Calibration(app))
    app.addRoutine(routines.FNInstructions(app))
    # only try to update the examiner window if the user has requested one
    if app.examinerWindow:
        examinerUpdate = routines.UpdateExaminerWindow(app)
        #app.addRoutine(examinerUpdate) 
    #app.addRoutine(routines.CountdownSequence(app))


    # no need to sync if this is a practice run
    if app.mode != 'practice' or True:
        app.addRoutine(routines.WaitForTLL(app))
    app.addRoutine(routines.CountdownSequence(app,length=5, time=TR))


    # build the trial sequence and add to the app
    runCSV = data.importConditions(app.runfile)
    
    firstBlock = True
    for line in runCSV:

        blockCSV = data.importConditions(line['blockFile'])

        # Fixations will be placed BEFORE all trials except for the first
        # This means the last trial won't have a fixation following it
        firstTrial = True

        for trial in blockCSV:
            image = os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['image'])
            trialRoutine = routines.FacenameTrial(app, image, trial['name'],duration=TRIAL_DURATION)

            # see the above comment about firstTrial
            if firstTrial:
                firstTrial = False
            else:
                app.addRoutine(routines.Fixation(app,duration=ISI))

            app.addRoutine(trialRoutine)

        # only try to update the examiner window if the user has requested one
        if app.examinerWindow:
            app.addRoutine(examinerUpdate) 
        # after each block there should be a rest block
        app.addRoutine(routines.RestBlock(app,duration=REST_DURATION))

    
    # ready freddy go!
    app.run()
    # write out the logfile
    logging.flush()
