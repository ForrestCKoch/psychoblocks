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

class Experiment(object):
    """
    Class for running an experiment

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

    def __init__(self,name):
        """
        Initialization...
        """
        self._getInfo(name)
        self._setupResponseBox()
        self._setupLogfile()
        self._setupWindows()
        self._setupExperimentHandler()
        self._clock = clock.Clock()
        self._routines = list()

    def _getInfo(self,name):
        """
        Get the required information to initialize this task
        """
        # get some basic information for the experiment
        self._expName = name
        expInfo = {'participant'       : const.DEFAULT_PARTICIPANT,
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
        dlg = gui.DlgFromDict(dictionary = expInfo, title = self.expName)
        if dlg.OK == False:
            core.quit()

        self._date = data.getDateStr()

        self._participant    = expInfo['participant']
        self._session        = expInfo['session']
        self._run_file       = expInfo['run_file']
        self._mode           = expInfo['mode']
        self._port           = expInfo['port']
        self._baudrate       = int(expInfo['baudrate'])
        self._fullscreen     = expInfo['fullscreen']
        self._screen_height  = int(expInfo['screen_height'])
        self._screen_width   = int(expInfo['screen_width'])
        self._stimuli_folder = expInfo['stimuli_folder']
        self._results_folder = expInfo['results_folder']
        
    def _setupResponseBox(self):
        """
        Setup the response box if necessary

        Note
        ----
        self.responseBox = None if the experiment isn't using it
        """
        # setup the response box if there is one
        if (self.mode == 'serial'):
            self._responseBox = serial.Serial(port = self.port,
                                        baudrate = self.baudrate,
                                        timeout = 0)
        else:
            self._responseBox = None

    def _setupLogfile(self):
        """
        Setup the logfile
        """
        # setup logging -- do we need to hold onto the returns?
        datafile = self.expName+'/data/%s_%s_%s' %(self.participant,
                                     self.session,
                                     self.date)
        self._logfile = logging.LogFile(datafile+'.log', level = logging.EXP)
        logging.console.setLevel(logging.WARNING)

    def _setupWindows(self):
        """
        Setup the windows
        """
        # setup the participant's window
        if self.fullscreen == 'true':
            screenFlag = True
        else:
            screenFlag = False

        height = self.screen_height
        width  = self.screen_width

        self._participantWindow = visual.Window(size = [width,height],
                                              fullscr = screenFlag,
                                              screen = 1,
                                              allowGUI = True,
                                              allowStencil = False,
                                              monitor = 'particpant',
                                              color = [-1,-1,-1],
                                              colorSpace = 'rgb',
                                              blendMode = 'avg',
                                              useFBO = True)
        self._participantFrameRate = self.participantWindow.getActualFrameRate()

    def _setupExperimentHandler(self):
        """
        Setup the experiment handler
        """
        datafile = self.expName + '/data/%s_%s_%s' %(self.participant,
                                     self.session,
                                     self.date)
        self._expHandler = data.ExperimentHandler(name = self.expName, 
                                                 version = self.run_file,
                                                 #extraInfo = self.expInfo,
                                                 runtimeInfo = None,
                                                 originPath = None,
                                                 savePickle = False,
                                                 saveWideText = True,
                                                 dataFileName = datafile)
    
    def addRoutine(self,routine):
        self._routines.append(routine)

    def run(self):
        # reverse our list because I'm too lazy to use a proper queue
        self._routines.reverse()
        while(len(self._routines)):
            currRoutine = self._routines.pop()
            currRoutine.run()
    @property
    def expName(self):
        return self._expName 

    @property
    def participant(self):
        return self._participant 
   
    @property
    def session(self):
        return self._session 
       
    @property
    def run_file(self):
        return self._run_file 
      
    @property
    def mode(self):
        return self._mode 
          
    @property
    def port(self):
        return self._port 
          
    @property
    def baudrate(self):
        return self._baudrate 
      
    @property
    def fullscreen(self):
        return self._fullscreen 
    
    @property
    def screen_height(self):
        return self._screen_height 
 
    @property
    def screen_width(self):
        return self._screen_width 
  
    @property
    def stimuli_folder(self):
        return self._stimuli_folder 
 
    @property
    def results_folder(self):
        return self._results_folder 
 
    @property
    def date(self):
        return self._date
 
    @property
    def responseBox(self):
        return self._responseBox 
 
    @property
    def logfile(self):
        return self._logfile 
 
    @property
    def participantWindow(self):
        return self._participantWindow 
 
    @property
    def participantFrameRate(self):
        return self._participantFrameRate 
 
    @property
    def expHandler(self):
        return self._expHandler

    @property
    def clock(self):
        return self._clock
