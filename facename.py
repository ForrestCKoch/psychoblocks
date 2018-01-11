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
    app = experiment.Experiment('facename')

    # add routines to the app
    app.addRoutine(FacenameInstructions(app))
    app.addRoutine(CountdownSequence(app))

    # build the trial sequence and add to the app
    runCSV = data.importConditions('facename/runs/run1.csv')
    
    firstBlock = True
    for line in runCSV:

        if firstBlock: 
            firstBlock = False
        else:
            # after each block there should be a rest block
            app.addRoutine(RestBlock(app))

        blockCSV = data.importConditions(line['blockFile'])
        # discriminate between known and novel trials
        if (int(line['isKnown']) == 1):
            isKnown = True
            app.addRoutine(KnownCue(app))
        else:
            isKnown = False
            app.addRoutine(NovelCue(app))
        firstTrial = True

        for trial in blockCSV:
            image = os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['image'])
            if isKnown:
                trialRoutine = KnownTrial(app, image, trial['name1'], trial['name2'], None)
            else:
                trialRoutine = NovelTrial(app, image, trial['name'])

            # after each trial there should be a brief fixation
            if firstTrial:
                firstTrial = False
            else: 
                app.addRoutine(Fixation(app))

            app.addRoutine(trialRoutine)

    
    # ready freddy go!
    app.run()
    print('hello')
    # write out the logfile
    logging.flush()
