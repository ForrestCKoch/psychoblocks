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
import experiment

from colls import *

if (__name__ == '__main__'):
    app = experiment.Experiment('2back')

    # add routines to the app
    app.addRoutine(TwoBackInstructions(app))
    app.addRoutine(CountdownSequence(app))

    # build the trial sequence and add to the app
    runCSV = data.importConditions('2back/runs/run1.csv')

    firstBlock = True

    for line in runCSV:
    
        if firstBlock:
            firstBlock = False
        else:
            # after each block there should be a rest block
            app.addRoutine(RestBlock(app, duration = 15.0))

        blockCSV = data.importConditions(line['blockFile'])
        # discriminate between 0 and 1 back
        if (int(line['is0back']) == 1):
            is0 = True
            # a silly way to find the target image
            targetStim = None
            for trial in blockCSV:
                if trial['TargetType'] == 'target':
                    target=os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['Stimulus'])
                    break
            app.addRoutine(ZeroBackCue(app,target))
        else:
            is0 = False
            app.addRoutine(TwoBackCue(app))
        firstTrial = True 

        for trial in blockCSV:
            image=os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['Stimulus'])
            trialRoutine = NBackTrial(app,image,None)
            # after each trial there should be a brief fixation
            if firstTrial:
                firstTrial = False
            else:
                app.addRoutine(Fixation(app,duration = 0.5))

            app.addRoutine(trialRoutine)

    
    # ready freddy go!
    app.run()
    # write out the logfile
    logging.flush()
