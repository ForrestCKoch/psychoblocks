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
        self._clock = clock.Clock()
        self._setupLogfile()
        self._setupWindows()
        self._setupResponseBox()
        self._setupExperimentHandler()
        self._routines = list()

    def _getInfo(self,name):
        """
        Get the required information to initialize this task
        """
        # get some basic information for the experiment
        self._expName = name
        expInfo = {'participant'       : const.DEFAULT_PARTICIPANT,
                        'session'           : const.DEFAULT_SESSION,
                        'run file'          : os.path.join(name,'runs',const.DEFAULT_RUN_FILE),
                        'mode'              : const.DEFAULT_MODE,
                        'port'              : const.DEFAULT_PORT,
                        'baudrate'          : const.DEFAULT_BAUDRATE,
                        'fullscreen'        : const.DEFAULT_FULLSCREEN,
                        'screen height'     : const.DEFAULT_SCREEN_HEIGHT,
                        'screen width'      : const.DEFAULT_SCREEN_WIDTH,
                        'stimuli folder'    : const.DEFAULT_STIMULI_FOLDER,
                        'results folder'    : os.path.join(name,const.DEFAULT_RESULTS_FOLDER)} 
        dlg = gui.DlgFromDict(dictionary = expInfo, title = self.expName)
        if dlg.OK == False:
            logging.error("Couldn't establish experiment parameters")
            core.quit()

        self._date = data.getDateStr()

        self._participant = expInfo['participant']
        self._session = expInfo['session']
        self._port = expInfo['port']
        
        # check that the run file exists
        self._runFile = expInfo['run file']
        if not os.path.exists(self.runFile):
            logging.error("Couldn't find runfile ("+self.runFile+")")
            core.quit() 

        # check for results folder and create if necessary
        self._resultsFolder = expInfo['results folder']
        if not os.path.exists(self.resultsFolder):
            logging.warn(self.resultsFolder+' does not exist ... creating folder')
            try:
                os.makedirs(self.resultsFolder)
            except OSError:
                logging.error("Couldn't create results folder ("+self.resultsFolder+")")
                core.quit()
        

        # check for stimuli folder
        self._stimuliFolder = expInfo['stimuli folder']
        if not os.path.exists(self.stimuliFolder):
            logging.error('Could not find '+self.stimuliFolder)
            core.quit()

        # fullscreen should be 'true' or 'false'
        self._fullscreen = expInfo['fullscreen']
        if self.fullscreen != 'true' and self.fullscreen != 'false':
            logging.warn('fullscreen should either be true or false ... defaulting to false')
            self._fullscreen = 'false'

        # mode should be 'serial' or 'test'
        self._mode = expInfo['mode']
        if self.mode != 'serial' and self.mode != 'test':
            logging.warn('unrecognized mode ... defaulting to false'+self.mode)
            self._mode = 'test'

        # baudrate should be an integer
        try:
            self._baudrate = int(expInfo['baudrate'])
        except ValueError:
            if self.mode == 'serial':
                logging.error('baudrate is not an integer ('+expInfo['baudrate']+')')
                core.quit()
            else:
                logging.warn('baudrate is not an integer ('+expInfo['baudrate']+')')

        # screen height should be an integer
        try:
            self._screenHeight = int(expInfo['screen height'])
        except ValueError:
            if self.fullscreen == 'false':
                logging.error('screen height is not an integer ('+expInfo['screen height']+')')
                core.quit()
            else:
                logging.warn('screen height is not an integer ('+expInfo['screen height']+')')

        # screen width should be an integer
        try:
            self._screenWidth = int(expInfo['screen width'])
        except ValueError:
            if self.fullscreen == 'false':
                logging.error('screen width is not an integer ('+expInfo['screen width']+')')
                core.quit()
            else:
                logging.warn('screen width is not an integer ('+expInfo['screen width']+')')
        
    def _setupResponseBox(self):
        """
        Setup the response box if necessary

        Note
        ----
        self.responseBox = None if the experiment isn't using it
        """
        # setup the response box if there is one
        if (self.mode == 'serial'):
            try:
                self._responseBox = serial.Serial(port = self.port,
                                        baudrate = self.baudrate,
                                        timeout = 0)
            except serial.SerialException:
                logging.error("Couldn't connect to responsebox at "+self.port)
                core.quit()
        else:
            self._responseBox = None

    def _setupLogfile(self):
        """
        Setup the logfile
        """
        # make sure we have a data folder
        if not os.path.exists(os.path.join(self.expName,'data')):
            os.makedirs(os.path.join(self.expName,'data'))

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

        height = self.screenHeight
        width  = self.screenWidth

        self._participantWindow = visual.Window(size = [width,height],
                                              fullscr = screenFlag,
                                              screen = 1,
                                              allowGUI = True,
                                              allowStencil = False,
                                              monitor = 'particpant',
                                              color = [-1,-1,-1],
                                              colorSpace = 'rgb',
                                              blendMode = 'avg',
                                              useFBO = False,
                                              waitBlanking = True)

        self._participantFrameRate = self.participantWindow.getActualFrameRate(nIdentical=100,nMaxFrames=1000,nWarmUpFrames=100)
        if self.participantFrameRate:
            logging.info('Particpant screen has a framerate of '+str(self.participantFrameRate)+" hz")
        else:
            logging.error("Couldn't establish a stable frame rate for particpant screen")
            core.quit()

    def _setupExperimentHandler(self):
        """
        Setup the experiment handler
        """
        # make sure we have a data folder
        if not os.path.exists(os.path.join(self.expName,'data')):
            os.makedirs(os.path.join(self.expName,'data'))

        datafile = self.expName + '/data/%s_%s_%s' %(self.participant,
                                     self.session,
                                     self.date)
        self._expHandler = data.ExperimentHandler(name = self.expName, 
                                                 version = self.runFile,
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
    def runFile(self):
        return self._runFile 
      
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
    def screenHeight(self):
        return self._screenHeight 
 
    @property
    def screenWidth(self):
        return self._screenWidth 
  
    @property
    def stimuliFolder(self):
        return self._stimuliFolder 
 
    @property
    def resultsFolder(self):
        return self._resultsFolder 
 
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
