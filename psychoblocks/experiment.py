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
        The name of this experiment
    participant : str
        The participant id
    session : str
        The session id
    runfile : str
        The path of the run file to be used
    mode : str
        The type of experiment being run (serial/test).
    port : str
        The port which the serial device is connected to (for serial mode).
    baudrate : int
        The baudrate of the serial device (for serial mode).
    fullscreen : str
        String indicating fullscreen status. ('yes'/'no')
    screenHeight : int
        If fullscreen = 'no', this indicates the screen height in pixels.
    screenWidth : int
        If fullscreen = 'no', this indicates the screen width in pixels.
    stimuliFolder : str
        Path of the stimuli folder.
    resultsFolder : str
        Path of the results folder.
    date : str
        Current date.
    responseBox : serial.Serial
        The serial device being used.  None if the experiment is not run in serial mode.
    responsesUnder200ms : int
        Keep track of the number of responses under 200ms
    responsesTotal : int
        Keep track of the total number of responses
    responsesExpected:
        Keep track of the total number of expected responses
    logfile : psychopy.LogFile
        The logfile. 
    participantWindow : psychopy.visual.Window
        The window for the participant screen.
    participantFrameRate : float
        The frame rate (hz) for the participant screen.
    experimentHandler : psychopy.data.ExperimentHandler
        The ExperimentHandler being used for this experiment.
    clock : psychopy.clock.Clock
        The clock used by this experiment
    examinerScreen : str
        String indicating status of examiner screen. ('yes'/'no')
    examinerWindow : psychopy.visual.Window
        The window for the examiner.  None if not being used
    examinerFullscreen : str
        String indicating fullscreen status of examiner screen. ('yes'/'no')
    examinerScreenHeight : int
        If examinerFullscreen = 'no', this indicates the screen height in pixels
    examinerScreenWidth : int
        If examinerFullscreen = 'no', this indicates the screen width in pixels
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

        self._responsesUnder200ms = 0
        self._responseTotal = 0
        self._responsesExpected = 0

    def _getInfo(self,name):
        """
        Get the required information to initialize this task
        """
        # get some basic information for the experiment
        self._expName = name
        expInfo={   'participant':const.DEFAULT_PARTICIPANT,
                    'run session':const.DEFAULT_SESSION,
                    'run file':os.path.join('data','runs',const.DEFAULT_RUN_FILE),
                    'run mode':const.DEFAULT_MODE,
                    'serial port':const.DEFAULT_PORT,
                    'serial baudrate':const.DEFAULT_BAUDRATE,
                    'participant fullscreen':const.DEFAULT_FULLSCREEN,
                    'participant screen height':const.DEFAULT_SCREEN_HEIGHT,
                    'participant screen width':const.DEFAULT_SCREEN_WIDTH,
                    'path to stimuli folder':const.DEFAULT_STIMULI_FOLDER,
                    'path to results folder':os.path.join('data',const.DEFAULT_RESULTS_FOLDER),
                    'examiner fullscreen':const.DEFAULT_FULLSCREEN,
                    'examiner screen height':const.DEFAULT_SCREEN_HEIGHT,
                    'examiner screen width':const.DEFAULT_SCREEN_WIDTH,
                    'examiner screen':'yes'}

        dlg = gui.DlgFromDict(dictionary = expInfo, title = self.expName)
        if dlg.OK == False:
            logging.error("Couldn't establish experiment parameters")
            core.quit()

        self._date = data.getDateStr()

        self._participant = expInfo['participant']
        self._session = expInfo['run session']
        self._port = expInfo['serial port']
        
        # check that the run file exists
        self._runfile = expInfo['run file']
        if not os.path.exists(self.runfile):
            logging.error("Couldn't find runfile ("+self.runfile+")")
            core.quit() 

        # check for results folder and create if necessary
        self._resultsFolder = os.path.join(expInfo['path to results folder'],self.participant)
        if not os.path.exists(self.resultsFolder):
            logging.warn(self.resultsFolder+' does not exist ... creating folder')
            try:
                os.makedirs(self.resultsFolder)
            except OSError:
                logging.error("Couldn't create results folder ("+self.resultsFolder+")")
                core.quit()
        

        # check for stimuli folder
        self._stimuliFolder = expInfo['path to stimuli folder']
        if not os.path.exists(self.stimuliFolder):
            logging.error('Could not find '+self.stimuliFolder)
            core.quit()

        # fullscreen should be 'yes' or 'no'
        self._fullscreen = expInfo['participant fullscreen']
        if self.fullscreen != 'yes' and self.fullscreen != 'no':
            logging.warn('fullscreen should either be yes or no ... defaulting to false')
            self._fullscreen = 'no'

        # examiner fullscreen should be 'yes' or 'no'
        self._examinerScreen = expInfo['examiner screen']
        if self.examinerScreen != 'yes' and self.examinerScreen != 'no':
            logging.warn('examiner screen should either be yes or no ... defaulting to false')
            self._examinerScreen = 'no'

        # examiner fullscreen should be 'yes' or 'no'
        self._examinerFullscreen = expInfo['examiner fullscreen']
        if self.examinerFullscreen != 'yes' and self.examinerFullscreen != 'no':
            logging.warn('examiner fullscreen should either be yes or no ... defaulting to false')
            self._examinerFullscreen = 'no'

        # mode should be 'serial' or 'test'
        self._mode = expInfo['run mode']
        if self.mode != 'serial' and self.mode != 'test':
            logging.warn('unrecognized mode ... defaulting to no'+self.mode)
            self._mode = 'test'

        # baudrate should be an integer
        try:
            self._baudrate = int(expInfo['serial baudrate'])
        except ValueError:
            if self.mode == 'serial':
                logging.error('baudrate is not an integer ('+expInfo['serial baudrate']+')')
                core.quit()
            else:
                logging.warn('baudrate is not an integer ('+expInfo['serial baudrate']+')')

        # screen height should be an integer
        try:
            self._screenHeight = int(expInfo['participant screen height'])
        except ValueError:
            if self.fullscreen == 'no':
                logging.error('screen height is not an integer ('+expInfo['participant screen height']+')')
                core.quit()
            else:
                logging.warn('screen height is not an integer ('+expInfo['participant screen height']+')')

        # screen width should be an integer
        try:
            self._screenWidth = int(expInfo['participant screen width'])
        except ValueError:
            if self.fullscreen == 'no':
                logging.error('screen width is not an integer ('+expInfo['participant screen width']+')')
                core.quit()
            else:
                logging.warn('screen width is not an integer ('+expInfo['participant screen width']+')')

        # examiner screen height should be an integer
        try:
            self._examinerScreenHeight = int(expInfo['examiner screen height'])
        except ValueError:
            if self.examinerFullscreen == 'no':
                logging.error('examiner screen height is not an integer ('+expInfo['examiner screen height']+')')
                core.quit()
            else:
                logging.warn('examiner screen height is not an integer ('+expInfo['examiner screen height']+')')

        # examiner screen width should be an integer
        try:
            self._examinerScreenWidth = int(expInfo['examiner screen width'])
        except ValueError:
            if self.examinerFullscreen == 'no':
                logging.error('examiner screen width is not an integer ('+expInfo['examiner screen width']+')')
                core.quit()
            else:
                logging.warn('examiner screen width is not an integer ('+expInfo['examiner screen width']+')')
        
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

        # setup logging -- do we need to hold onto the returns?
        datafile = os.path.join(self.resultsFolder,'%s_%s_%s_%s' %
                               (self.expName,self.participant, self.session, self.date))

        self._logfile = logging.LogFile(datafile+'.log', level = logging.INFO)
        logging.console.setLevel(logging.WARNING)

    def _setupWindows(self):
        """
        Setup the windows
        """
        # setup the participant's window
        if self.fullscreen == 'yes':
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
        if self.examinerScreen == 'yes':
            # setup the participant's window
            if self.examinerFullscreen == 'yes':
                screenFlag = True
            else:
                screenFlag = False

            height = self.examinerScreenHeight
            width  = self.examinerScreenWidth

            self._examinerWindow = visual.Window(size = [width,height],
                                              fullscr = screenFlag,
                                              screen = 0,
                                              allowGUI = True,
                                              allowStencil = False,
                                              monitor = 'examiner',
                                              color = [-1,-1,-1],
                                              colorSpace = 'rgb',
                                              blendMode = 'avg',
                                              useFBO = False,
                                              waitBlanking = True)
        else:
            self._examinerWindow = None 

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

        datafile = os.path.join(self.resultsFolder, '%s_%s_%s' %
                               (self.participant, self.session, self.date))

        self._expHandler = data.ExperimentHandler(name = self.expName, 
                                                 version = self.runfile,
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
            logging.info('starting routine '+type(currRoutine).__name__+' ...')
            currRoutine.start()
            currRoutine.run()
            currRoutine.end()
            logging.info('finished routine '+type(currRoutine).__name__+' ...')

    @property
    def responsesUnder200ms(self):
        return self._responsesUnder200ms

    @property
    def responseTotal(self):
        return self._responseTotal

    @property
    def responsesExpected(self):
        return self._responsesExpected 

    @responsesUnder200ms.setter
    def responsesUnder200ms(self,value):
        self._responsesUnder200ms = value

    @responseTotal.setter
    def responseTotal(self,value):
        self._responseTotal = value

    @responsesExpected.setter
    def responsesExpected(self,value):
        self._responsesExpected = value

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
    def runfile(self):
        return self._runfile 
      
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
    def experimentHandler(self):
        return self._expHandler

    @property
    def clock(self):
        return self._clock

    @property
    def examinerWindow(self):
        return self._examinerWindow

    @property
    def examinerFullscreen(self):
        return self._examinerFullscreen

    @property
    def examinerScreenHeight(self):
        return self._examinerScreenHeight

    @property
    def examinerScreenWidth(self):
        return self._examinerScreenWidth

    @property
    def examinerScreen(self):
        return self._examinerScreen
