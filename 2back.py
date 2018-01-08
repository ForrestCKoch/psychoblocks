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
    app = experiment.Experiment('2back')

    # initialize the constant routines
    instructions = routines.TwoBackInstructions(app.clock,
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
    runCSV = data.importConditions('2back/runs/run1.csv')
    for line in runCSV:
        blockCSV = data.importConditions(line['blockFile'])
        # discriminate between 0 and 1 back
        if (int(line['is0back']) == 1):
            is0 = True
            # a silly way to find the target image
            targetStim = None
            for trial in blockCSV:
                if trial['TargetType'] == 'target':
                    targetStim = visual.ImageStim(app.participantWindow,image=os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['Stimulus']),autoLog=True,pos=(0.33,0))
                    break
            app.addRoutine(routines.ZeroBackCue(app.clock,
                                                app.participantWindow,
                                                app.participantFrameRate,
                                                app.expHandler,
                                                targetStim))
        else:
            is0 = False
            app.addRoutine(routines.TwoBackCue(app.clock,
                                               app.participantWindow,
                                               app.participantFrameRate,
                                               app.expHandler))
        firstTrial = True 

        for trial in blockCSV:
            imageStim = visual.ImageStim(app.participantWindow,image=os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['Stimulus']),autoLog=True)
            trialRoutine = routines.NBackTrial(app.clock,
                                               app.participantWindow,
                                               app.participantFrameRate,
                                               app.expHandler,
                                               app.responseBox,
                                               imageStim)
            # after each trial there should be a brief fixation
            if firstTrial:
                firstTrial = False
            else:
                app.addRoutine(fixation)

            app.addRoutine(trialRoutine)

        # after each block there should be a rest block
        app.addRoutine(restblock)
        # and sync
        app.addRoutine(syncRoutine)
    
    # ready freddy go!
    app.run()
    # write out the logfile
    logging.flush()
