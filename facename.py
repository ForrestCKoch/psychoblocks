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

class Facename():
    """
    Class for running an instance of facename task

    Note
    ----
    There should only be one instance of this class initialized at any one time
    results are undefined otherwise.

    Attributes
    ----------
    expName : str
        Name of this experiment task
    expInfo : dict
        Dictionary containing information required to
        setup the experiment
    participantWindow : visual.Window
        The window displayed to the participant during the experiment 
    expHandler : data.ExperimentHandler
        Experiment Handler uesd to write the data file for this experiment
    responseBox: serial.Serial
        Serial object used for reading data from the response box
    clock: clock.Clock
        clock from the core module used for keeping track of time
    routines: list
        list of Routine objects to be called over the course of the experiment
    """

    def __init__(self):
        """
        Initialization...
        """
        self._getInfo()
        self._setupResponseBox()
        self._setupLogfile()
        self._setupWindows()
        self._setupExperimentHandler()
        self.clock = clock.Clock()
        self.routines = list()

    def _getInfo(self):
        """
        Get the required information to initialize this task
        """
        # get some basic information for the experiment
        self.expName = 'facename'
        self.expInfo = {'participant'       : const.DEFAULT_PARTICIPANT,
                        'session'           : const.DEFAULT_SESSION,
                        'run_file'          : const.DEFAULT_RUN_FILE,
                        'mode'              : const.DEFAULT_MODE,
                        'port'              : const.DEFAULT_PORT,
                        'baudrate'          : const.DEFAULT_BAUDRATE,
                        'fullscreen'        : const.DEFAULT_FULLSCREEN,
                        'screen_height'     : const.DEFAULT_SCREEN_HEIGHT,
                        'screen_width'      : const.DEFAULT_SCREEN_WIDTH,
                        'stimuli_folder'    : const.DEFAULT_STIMULI_FOLDER,
                        'results_folder'    : const.DEFAULT_RESULTS_FOLDER} 
        dlg = gui.DlgFromDict(dictionary = self.expInfo, title = self.expName)
        if dlg.OK == False:
            core.quit()
        self.expInfo['date'] = data.getDateStr()
        
    def _setupResponseBox(self):
        """
        Setup the response box if necessary

        Note
        ----
        self.responseBox = None if the experiment isn't using it
        """
        # setup the response box if there is one
        if (self.expInfo['mode'] == 'serial'):
            self.responseBox = serial.Serial(port = self.expInfo['port'],
                                        baudrate = int(self.expInfo['baudrate']),
                                        timeout = 0)
        else:
            self.responseBox = None

    def _setupLogfile(self):
        """
        Setup the logfile
        """
        # setup logging -- do we need to hold onto the returns?
        datafile = 'data/%s_%s_%s' %(self.expInfo['participant'],
                                     self.expInfo['session'],
                                     self.expInfo['date'])
        self.expInfo['logifle'] = logging.LogFile(datafile+'.log', level = logging.EXP)
        logging.console.setLevel(logging.WARNING)

    def _setupWindows(self):
        """
        Setup the windows
        """
        # setup the participant's window
        if self.expInfo['fullscreen'] == 'true':
            screenFlag = True
        else:
            screenFlag = False

        height = int(self.expInfo['screen_height'])
        width  = int(self.expInfo['screen_width'])

        self.participantWindow = visual.Window(size = [width,height],
                                              fullscr = screenFlag,
                                              screen = 1,
                                              allowGUI = True,
                                              allowStencil = False,
                                              monitor = 'particpant',
                                              color = [-1,-1,-1],
                                              colorSpace = 'rgb',
                                              blendMode = 'avg',
                                              useFBO = True)
        self.expInfo['participantFrameRate'] = self.participantWindow.getActualFrameRate()

    def _setupExperimentHandler(self):
        """
        Setup the experiment handler
        """
        datafile = 'data/%s_%s_%s' %(self.expInfo['participant'],
                                     self.expInfo['session'],
                                     self.expInfo['date'])
        self.expHandler = data.ExperimentHandler(name = self.expName, 
                                                 version = self.expInfo['run_file'],
                                                 extraInfo = self.expInfo,
                                                 runtimeInfo = None,
                                                 originPath = None,
                                                 savePickle = False,
                                                 saveWideText = True,
                                                 dataFileName = datafile)
    
    def addRoutine(self,routine):
        self.routines.append(routine)

    def run(self):
        # reverse our list because I'm too lazy to use a proper queue
        self.routines.reverse()
        while(len(self.routines)):
            currRoutine = self.routines.pop()
            currRoutine.run()
        

if (__name__ == '__main__'):
    app = Facename()

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

    # add routines to the app
    app.addRoutine(instructions)
    app.addRoutine(countdown)

    # build the trial sequence and add to the app
    runCSV = data.importConditions('run.csv')
    for line in runCSV:
        blockCSV = data.importConditions(line['blockFile'])
        # discriminate between known and novel trials
        if (int(line['isKnown']) == 1):
            isKnown = True
        else:
            isKnown = False
        for trial in blockCSV:
            imageStim = visual.ImageStim(app.participantWindow,image=os.path.join(const.DEFAULT_STIMULI_FOLDER,trial['image']))
            if isKnown:
                trialRoutine = routines.KnownTrial(app.clock,
                                                app.participantWindow,
                                                app.expInfo['participantFrameRate'],
                                                app.expHandler,
                                                app.responseBox,
                                                imageStim,
                                                trial['name1'],
                                                trial['name2'])
            else:
                trialRoutine = routines.NovelTrial(app.clock,
                                                app.participantWindow,
                                                app.expInfo['participantFrameRate'],
                                                app.expHandler,
                                                app.responseBox,
                                                imageStim,
                                                trial['name'])
            app.addRoutine(trialRoutine)
            # after each trial there should be a brief fixation
            app.addRoutine(fixation)

        # after each block there should be a rest block
        app.addRoutine(restblock)
    
    # ready freddy go!
    app.run()
