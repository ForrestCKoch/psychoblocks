# -*- coding: utf-8 -*-
###############################################################################
# Written by:       Forrest Koch (forrest.koch@unsw.edu.au)
# Organization:     Centre for Healthy Brain Ageing (UNSW)
# PyschoPy Version: 1.85.3
# Python Version:   2.7.5
###############################################################################
from psychopy import core, visual, event, logging
from abc import ABCMeta, abstractmethod
import const
from abstracts import *

class TimedLoop(AbstractLoop):
    """
    This will run the contained features for the specified amount of time, refreshing the
    screen with each pass.
    """
    def __init__(self, origin, duration, experiment = None):
        """
        Initialize an instance of TimedLoop.

        Parameters
        ----------
        duration : float
            Time in seconds.
        origin : AbstractFeature
            Feature being decorated.  None if this is the base.
        experiment : Experiment
            Experiment to which this belongs.  Not necessary if this is not the base.
        """
        super(TimedLoop,self).__init__(origin, experiment = experiment)

        self._framesToShow = int(self.experiment.participantFrameRate * duration)

        self._status = False

    @property
    def status(self):
        """
        Boolean : Execution status of the loop.
        """
        return self._status

    def initializeLoop(self):
        """
        Initializes the framesShown and status.
        """
        self._framesShown = 0
        self._status = True

    def updateStatus(self):
        """
        Check whether the correct number of frames have been shown for the requested duration.
        """
        self.experiment.participantWindow.flip()
        self._framesShown += 1
        if self._framesShown >= self._framesToShow:
            self._status = False

    def destroyLoop(self):
        """
        Does nothing.
        """
        pass

class SpacebarLoop(AbstractLoop):
    """
    Prevents experiment from progessing until the spacebar has been pressed.
    """

    def __init__(self, origin, experiment = None, updateExaminer=False):
        """
        Initialize an instance of TimedLoop.

        Parameters
        ----------
        origin : AbstractFeature
            Feature being decorated.  None if this is the base.
        experiment : Experiment
            Experiment to which this belongs.  Not necessary if this is not the base.
        """
        super(SpacebarLoop,self).__init__(origin, experiment = experiment)
        self._status = False
        self._updateExaminer = updateExaminer

    @property
    def status(self):
        """
        Boolean : Execution status of the loop.
        """
        return self._status

    def initializeLoop(self):
        """
        Initialize status.
        """
        self._status = True

    def updateStatus(self):
        """
        Check for spacebar keypress.
        """
        self.experiment.participantWindow.flip()
        if self._updateExaminer:
            self.experiment.examinerWindow.flip()
        if 'space' in event.getKeys(keyList = ['space']):
            self._status = False

    def destroyLoop(self):
        """
        Does nothing.
        """
        pass

class MRISync(AbstractFeature):
    """
    Waits for TLL pulse from the response box before continuing
    """
    
    def __init__(self, origin, experiment = None):
        """
        Initialize an instance of TimedLoop.

        Parameters
        ----------
        origin : AbstractFeature
            Feature being decorated.  None if this is the base.
        experiment : Experiment
            Experiment to which this belongs.  Not necessary if this is not the base.
        """
        super(MRISync,self).__init__(origin,experiment = experiment)

    def run(self):
        """
        Halt execution until TLL pulse is read
        """
        # run the origin features first
        super(MRISync,self).run() 
        # only execute if we have a response box
        if self.experiment.responseBox:
            # wait for TLL pulse until being allowed to continue
            self.experiment.responseBox.reset_input_buffer()
            pulseSeen = False

            startTime = self.experiment.clock.getTime()
            print(self.experiment.mode)

            while(not pulseSeen):
                data = self.experiment.responseBox.read()
                currTime = self.experiment.clock.getTime()
                if self.experiment.mode == 'practice':
                    if currTime-startTime > 10.0:
                        break
                if data and ord(data) == const.TLL_PULSE:
                    timestamp = str(currTime)
                    self.experiment.experimentHandler.nextEntry()
                    self.experiment.experimentHandler.addData('syncPulse',timestamp)
                    logging.info('Synced with pulse at '+str(self.experiment.clock.getTime()))
                    pulseSeen = True
                if 'escape' in event.getKeys(keyList = ['escape']):
                    logging.warn('escape button pressed ... aborting experiment')
                    core.quit()

class ResponseBox(AbstractFeature):
    """
    Checks the response box for the first reponse.
    """

    def __init__(self, origin, correctResponse, experiment = None):
        """
        Initialize an instance of ResponseBox.

        Parameters
        ----------
        origin : AbstractFeature
            Feature being decorated.  None if this is the base.
        experiment : Experiment
            Experiment to which this belongs.  Not necessary if this is not the base.
        correctResponse : str
            The value for the correct response so that it can be recorded
        """
        super(ResponseBox,self).__init__(origin,experiment = experiment)

        self._correctResponse = correctResponse
        self._flag = True

    @property
    def startTime(self):
        return self._startTime
        
    def start(self):
        """
        Set flags and clear the input buffer
        """
        self._responseRead = False
        # clear the buffer
        if(self.experiment.responseBox):
            self.experiment.responseBox.reset_input_buffer()
        # call origin feature
        super(ResponseBox,self).start()
        # record the starting time of this response
        self._startTime = self.experiment.clock.getTime()
        self.experiment.responsesExpected += 1

    def run(self):
        """
        Check for a response from the response box
        """
        # capture starting time
        if self._flag:
            self._startTime = self.experiment.clock.getTime()
            self._flag = False
            logging.info('starting routine timer from '+str(self._startTime))

        if self.experiment.responseBox:
            data = self.experiment.responseBox.read(size=1)
            while(data and ord(data) == const.TLL_PULSE):
                data = self.experiment.responseBox.read(size=1)
            if data and not self._responseRead:
                self._responseRead = True
                rt = self.experiment.clock.getTime()-self.startTime
                correct = data == self._correctResponse
                self.experiment.experimentHandler.addData('response',data)
                self.experiment.experimentHandler.addData('response time', str(rt))
                self.experiment.experimentHandler.addData('correct',correct)
                logging.data('Response Box: '+data)
                logging.data('ResponseTime: '+str(rt))
                if rt < 0.2:
                    self.experiment.responsesUnder200ms += 1
                self.experiment.responseTotal += 1
                
            # call origin feature
            super(ResponseBox,self).run()

class EscapeCheck(AbstractFeature):
    """
    Checks whether the escape button has been pressed to abort the experiment
    """

    def __init__(self, origin, experiment = None):
        """
        Initialize an instance of EscapeCheck.

        Parameters
        ----------
        origin : AbstractFeature
            Feature being decorated.  None if this is the base.
        experiment : Experiment
            Experiment to which this belongs.  Not necessary if this is not the base.
        """
        super(EscapeCheck,self).__init__(origin,experiment = experiment)

    def run(self):
        if 'escape' in event.getKeys(keyList = ['escape']):
            logging.warn('escape button pressed ... aborting experiment')
            core.quit()
        super(EscapeCheck,self).run()

class TextFeature(AbstractFeature):
    """
    Wrapper around psychopy.TextStim
    """
    
    def __init__(self, origin, experiment = None, text='Hello World', font=const.DEFAULT_FONT, 
                    pos=(0.0, 0.0), depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', 
                    opacity=1.0, contrast=1.0, units='', ori=0.0, height=0.2, antialias=True, 
                    bold=False, italic=False, alignHoriz='center', alignVert='center', 
                    fontFiles=(), wrapWidth=1, flipHoriz=False, flipVert=False, 
                    name=None, autoLog=True):
        """
        Initialize an instance of TextFeature.

        Note
        ----
        For undocumented parameters, refer to the psychopy documentaion for TextStim

        Parameters
        ----------
        origin : AbstractFeature
            Feature being decorated.  None if this is the base.
        experiment : Experiment
            Experiment to which this belongs.  Not necessary if this is not the base.
        """

        super(TextFeature,self).__init__(origin, experiment = experiment)
        self._textStim = visual.TextStim(self.experiment.participantWindow, text=text, 
                                font=font, pos=pos, depth=depth, rgb=rgb, color=color, 
                                colorSpace=colorSpace, opacity=opacity, contrast=contrast, 
                                units=units, ori=ori, height=height, antialias=antialias, 
                                bold=bold, italic=italic, alignHoriz=alignHoriz, 
                                alignVert=alignVert, fontFiles=fontFiles, wrapWidth=wrapWidth, 
                                flipHoriz=flipHoriz, flipVert=flipVert, name=name, autoLog=autoLog)

    def start(self):
        """
        Enable Auto Draw for the TextStim
        """
        self._textStim.setAutoDraw(True)
        super(TextFeature,self).start()

    def end(self):
        """
        Disable Auto Draw for the TextStim
        """
        self._textStim.setAutoDraw(False)
        super(TextFeature,self).end()

class ImageFeature(AbstractFeature):
    """
    Wrapper around psychopy.ImageStim
    """

    def __init__(self, origin, experiment = None, image=None, mask=None, units='', pos=(0.0, 0.0), 
                    size=None, ori=0.0, color=(1.0, 1.0, 1.0), colorSpace='rgb', contrast=1.0, 
                    opacity=1.0, depth=0, interpolate=False, flipHoriz=False, flipVert=False, 
                    texRes=128, name=None, autoLog=True, maskParams=None):
        """
        Initialize an instance of TextFeature.

        Note
        ----
        For undocumented parameters, refer to the psychopy documentaion for ImageStim

        Parameters
        ----------
        origin : AbstractFeature
            Feature being decorated.  None if this is the base.
        experiment : Experiment
            Experiment to which this belongs.  Not necessary if this is not the base.
        """
        super(ImageFeature,self).__init__(origin, experiment = experiment)
        self._imageStim = visual.ImageStim(self.experiment.participantWindow, image=image, 
                    mask=mask, units=units, pos=pos, size=size, ori=ori, color=color, 
                    colorSpace=colorSpace, contrast=contrast, opacity=opacity, depth=depth, 
                    interpolate=interpolate, flipHoriz=flipHoriz, flipVert=flipVert, 
                    texRes=texRes, name=name, autoLog=autoLog, maskParams=maskParams)

        #scale the image to screen
        screenHeight = self.experiment.screenHeight
        imageHeight = 400 # the images are 400px
        self._imageStim.size *= (screenHeight)/(imageHeight*2.0)


    def start(self):
        """
        enable AutoDraw for the ImageStim
        """
        self._imageStim.setAutoDraw(True)
        super(ImageFeature,self).start()

    def end(self):
        """
        disable AutoDraw for the ImageStim
        """
        self._imageStim.setAutoDraw(False)
        super(ImageFeature,self).end()

class ExaminerTextFeature(AbstractFeature):
    """
    Wrapper around psychopy.TextStim
    """
    
    def __init__(self, origin, experiment = None, text='Hello World', font=const.DEFAULT_FONT, 
                    pos=(0.0, 0.0), depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', 
                    opacity=1.0, contrast=1.0, units='', ori=0.0, height=None, antialias=True, 
                    bold=False, italic=False, alignHoriz='center', alignVert='center', 
                    fontFiles=(), wrapWidth=1.75, flipHoriz=False, flipVert=False, 
                    name=None, autoLog=True):
        """
        Initialize an instance of TextFeature.

        Note
        ----
        For undocumented parameters, refer to the psychopy documentaion for TextStim

        Parameters
        ----------
        origin : AbstractFeature
            Feature being decorated.  None if this is the base.
        experiment : Experiment
            Experiment to which this belongs.  Not necessary if this is not the base.
        """

        super(ExaminerTextFeature,self).__init__(origin, experiment = experiment)
        self._textStim = visual.TextStim(self.experiment.examinerWindow, text=text, 
                                font=font, pos=pos, depth=depth, rgb=rgb, color=color, 
                                colorSpace=colorSpace, opacity=opacity, contrast=contrast, 
                                units=units, ori=ori, height=height, antialias=antialias, 
                                bold=bold, italic=italic, alignHoriz=alignHoriz, 
                                alignVert=alignVert, fontFiles=fontFiles, wrapWidth=wrapWidth, 
                                flipHoriz=flipHoriz, flipVert=flipVert, name=name, autoLog=autoLog)

    def start(self):
        """
        Enable Auto Draw for the TextStim
        """
        self._textStim.setAutoDraw(True)
        super(ExaminerTextFeature,self).start()

    def end(self):
        """
        Disable Auto Draw for the TextStim
        """
        self._textStim.setAutoDraw(False)
        super(ExaminerTextFeature,self).end()

    
class WaitForResponse(AbstractLoop):
    """
    Apply this directly on top of a ResponseBox feature to make the program halt
    until a response is registered
    """
    def __init__(self, responseFeature, experiment = None):
        """
        Initialization

        Parameters
        ----------
        responseFeature : ResponseBox
            The ReponseBox feature being expanded on
        Experiment : Experiment
            The experiment to which this feature belongs.
        """
        super(WaitForResponse,self).__init__(responseFeature,experiment = experiment)
        self.responseFeature = responseFeature
        self._status = False

    @property
    def status(self):
        """
        Boolean : Execution status of the loop.
        """
        return not self.responseFeature._responseRead

    def initializeLoop(self):
        self._status = True

    def updateStatus(self):
        self.experiment.participantWindow.flip()
        pass

    def destroyLoop(self):
        pass
