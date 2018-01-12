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

        if firstBlock: 
            firstBlock = False
        else:
            # after each block there should be a rest block
            if app.examinerWindow:
                app.addRoutine(examinerUpdate) 
            app.addRoutine(routines.RestBlock(app))

        blockCSV = data.importConditions(line['blockFile'])
        # discriminate between known and novel trials
        if (int(line['isKnown']) == 1):
            isKnown = True
            app.addRoutine(routines.KnownCue(app))
        else:
            isKnown = False
            app.addRoutine(routines.NovelCue(app))
        firstTrial = True
        
        # sync before each block
        app.addRoutine(features.MRISync(None, experiment = app))

        for trial in blockCSV:
            image = os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['image'])
            if isKnown:
                trialRoutine = routines.KnownTrial(app, image, trial['name1'], trial['name2'], None)
            else:
                trialRoutine = routines.NovelTrial(app, image, trial['name'])

            # after each trial there should be a brief fixation
            if firstTrial:
                firstTrial = False
            else: 
                app.addRoutine(routines.Fixation(app))

            app.addRoutine(trialRoutine)

    
    # ready freddy go!
    app.run()
    # write out the logfile
    logging.flush()
