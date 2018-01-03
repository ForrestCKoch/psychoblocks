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
    app = experiment.Experiment('nback')

    # initialize the constant routines
    instructions = routines.InstructScreen(app.clock,
                                        app.participantWindow,
                                        app.expInfo['participantFrameRate'],
                                        app.expHandler)
    countdown = routines.CountdownScreen(app.clock,
                                        app.participantWindow,
                                        app.expInfo['participantFrameRate'],
                                        app.expHandler)
    fixation = routines.Fixation(app.clock,
                                app.participantWindow,
                                app.expInfo['participantFrameRate'],
                                app.expHandler)
    restblock = routines.RestBlock(app.clock,
                                app.participantWindow,
                                app.expInfo['participantFrameRate'],
                                app.expHandler)
    syncRoutine = routines.MRISync(app.clock,
                                app.participantWindow,
                                app.expHandler,
                                app.responseBox)

    # add routines to the app
    app.addRoutine(instructions)
    app.addRoutine(syncRoutine)
    app.addRoutine(countdown)

    # build the trial sequence and add to the app
    runCSV = data.importConditions('nback/runs/run1.csv')
    for line in runCSV:
        blockCSV = data.importConditions(line['blockFile'])
        # discriminate between 0 and 1 back
        if (int(line['is0back']) == 1):
            is0 = True
        else:
            is0 = False
        for trial in blockCSV:
            imageStim = visual.ImageStim(app.participantWindow,image=os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['Stimulus']),autoLog=True)
            trialRoutine = routines.NBackTrial(app.clock,
                                               app.participantWindow,
                                               app.expInfo['participantFrameRate'],
                                               app.expHandler,
                                               app.responseBox,
                                               imageStim)
            app.addRoutine(trialRoutine)
            # after each trial there should be a brief fixation
            app.addRoutine(fixation)

        # after each block there should be a rest block
        app.addRoutine(restblock)
        # and sync
        app.addRoutine(syncRoutine)
    
    # ready freddy go!
    app.run()
    # write out the logfile
    logging.flush()
