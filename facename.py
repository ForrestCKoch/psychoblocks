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

import const
import routines
import experiment

if (__name__ == '__main__'):
    app = experiment.Experiment('facename')

    # initialize the constant routines
    instructions = routines.FacenameInstructions(app.clock,
                                        app.participantWindow,
                                        app.participantFrameRate,
                                        app.expHandler)
    countdown = routines.CountdownScreen(app.clock,
                                        app.participantWindow,
                                        app.participantFrameRate,
                                        app.expHandler)
    fixation = routines.Fixation(app.clock,
                                app.participantWindow,
                                app.participantFrameRate,
                                app.expHandler)
    restblock = routines.RestBlock(app.clock,
                                app.participantWindow,
                                app.participantFrameRate,
                                app.expHandler,
                                duration=20.0) 
    syncRoutine = routines.MRISync(app.clock,
                                app.participantWindow,
                                app.expHandler,
                                app.responseBox)

    # add routines to the app
    app.addRoutine(instructions)
    app.addRoutine(syncRoutine)
    app.addRoutine(countdown)

    # build the trial sequence and add to the app
    runCSV = data.importConditions('facename/runs/run1.csv')
    
    firstBlock = True
    for line in runCSV:

        if firstBlock: 
            firstBlock = False
        else:
            # after each block there should be a rest block
            app.addRoutine(restblock)
            # and sync
            app.addRoutine(syncRoutine)

        blockCSV = data.importConditions(line['blockFile'])
        # discriminate between known and novel trials
        if (int(line['isKnown']) == 1):
            isKnown = True
            app.addRoutine(routines.KnownCue(app.clock,
                                                app.participantWindow,
                                                app.participantFrameRate,
                                                app.expHandler))
        else:
            isKnown = False
            app.addRoutine(routines.NovelCue(app.clock,
                                                app.participantWindow,
                                                app.participantFrameRate,
                                                app.expHandler))
        firstTrial = True

        for trial in blockCSV:
            imageStim = visual.ImageStim(app.participantWindow,image=os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['image']),autoLog=True)
            if isKnown:
                trialRoutine = routines.KnownTrial(app.clock,
                                                app.participantWindow,
                                                app.participantFrameRate,
                                                app.expHandler,
                                                app.responseBox,
                                                imageStim,
                                                trial['name1'],
                                                trial['name2'])
            else:
                trialRoutine = routines.NovelTrial(app.clock,
                                                app.participantWindow,
                                                app.participantFrameRate,
                                                app.expHandler,
                                                app.responseBox,
                                                imageStim,
                                                trial['name'])
            # after each trial there should be a brief fixation
            if firstTrial:
                firstTrial = False
            else: 
                app.addRoutine(fixation)

            app.addRoutine(trialRoutine)

    
    # ready freddy go!
    app.run()
    print('hello')
    # write out the logfile
    logging.flush()
