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
    app = experiment.Experiment('facename')

    if app.examinerWindow:
        examinerUpdate = routines.UpdateExaminerWindow(app)
        app.addRoutine(examinerUpdate) 

    app.addRoutine(routines.FacenameInstructions(app))
    # sync before instructions
    app.addRoutine(features.MRISync(None, experiment = app))
    app.addRoutine(routines.CountdownSequence(app))

    # build the trial sequence and add to the app
    runCSV = data.importConditions(app.runfile)
    
    firstBlock = True
    for line in runCSV:


        blockCSV = data.importConditions(line['blockFile'])
        # discriminate between known and novel trials
        if (int(line['isKnown']) == 1):
            isKnown = True
        else:
            isKnown = False
        firstTrial = True
        
        # sync before each block
        app.addRoutine(features.MRISync(None, experiment = app))

        firstTrial = True

        for trial in blockCSV:
            image = os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['image'])
            if isKnown:
                trialRoutine = routines.FacenameTrial(app, image, trial['name1'],duration=3.5)
            else:
                trialRoutine = routines.FacenameTrial(app, image, trial['name'],duration=3.5)

            if firstTrial:
                firstTrial = False
            else:
                app.addRoutine(routines.Fixation(app,duration=0.5))

            app.addRoutine(trialRoutine)

        # after each block there should be a rest block
        if app.examinerWindow:
            app.addRoutine(examinerUpdate) 
        app.addRoutine(routines.RestBlock(app,duration=16.0))

    
    # ready freddy go!
    app.run()
    # write out the logfile
    logging.flush()
