# -*- coding: utf-8 -*-
###############################################################################
# Written by:       Forrest Koch (forrest.koch@unsw.edu.au)
# Organization:     Centre for Healthy Brain Ageing (UNSW)
# PyschoPy Version: 1.85.3
# Python Version:   2.7.5
###############################################################################
from psychopy import core, visual, event
from abc import ABCMeta, abstractmethod
import const

"""
This module contains the classes that outline the facename routines.  Each class is a child of
the Routine abstract class, and so to one should just call the run method to run the routine.
"""

class Routine(object):
    """
    Base class for routines to derive from
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def run(self):
        """
        Call this function to run the routine specified by this instance
        """

class NovelTrial(Routine):
    """
    Routine used for the novel face-name exposures

    Note
    ----
    This trial lasts for approx 5 seconds.  The provided ImageStim is shown in the middle of
    the screen.  Assuming an image of approx 600x400px, the name is shown in the center 
    directly beneath the image.  Below this is a line asking "Does this face 'fit' this name?".

    Participants are expected to respond with their index finger (const.RIGHT_INDEX or 
    const.LEFT_INDEX) for 'yes' and with their middle finger (const.RIGHT_MIDDLE or 
    const.LEFT_MIDDLE) for no.
    """
    def __init__(self, clock, win, frameRate, expHandle, responseBox, 
                 imageStim, name, duration = 5.0):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box

        imageStim : psychopy.visual.ImageStim
            The ImageStim of the face to be used for this trial

        name : str
            The name associated with the provided face   
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.responseBox = responseBox
        self.duration = duration
        
        # stimulus stuff...
        self.image = imageStim
        self.name = visual.TextStim(win = self.win,
                                   text = name,
                                   font = const.DEFAULT_FONT,
                                   pos = (0, -.6),
                                   color = 'white')
        self.prompt = visual.TextStim(win = self.win,
                                   text = 'Does this face \'fit\' this name?',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, -.8),
                                   color = 'white')

    def run(self):
        
        # make things visible
        self.image.setAutoDraw(True)
        self.name.setAutoDraw(True)
        self.prompt.setAutoDraw(True)

        # flush the serial device
        if self.responseBox:
            self.responseBox.reset_input_buffer() 
        responseRead = False
        # reset the event buffer
        event.clearEvents() 

        # start new line for data output
        self.expHandle.nextEntry()
        self.expHandle.addData('trialStart',str(self.clock.getTime()))

        for i in range(0, int(self.frameRate * self.duration)):
            # refresh the screen
            self.win.flip()
            # check for response
            if not responseRead:
                # try to read data
                if self.responseBox:
                    data = self.responseBox.read(size=1)
                else:
                    data = None
                # make sure we're not reading a TLL Pulse
                while(data and ord(data) == const.TLL_PULSE):
                    data = self.responseBox.read(size=1)
                if data:
                    responseRead = True
                    self.expHandle.addData('response',data)
                    self.expHandle.addData('responseStamp',str(self.clock.getTime()))
            # check for abort signal
            if 'escape' in event.getKeys():
                print('Goodbye!')
                core.quit()

        # make things invisible
        self.image.setAutoDraw(False)
        self.name.setAutoDraw(False)
        self.prompt.setAutoDraw(False)

class KnownTrial(Routine):
    """
    Routine used for the known face-name exposures

    Note
    ----
    Participants are expected to be trained/familiar with the faces displayed in the trial.

    This trial lasts for approx 5 seconds.  The provided ImageStim is shown in the middle of
    the screen.  Assuming an image of approx 600x400px, name1 will be shown underneath the image
    to the left, and name2 will be shown underneath the image to the right.

    Participants are expected to response with their index finger (const.RIGHT_INDEX or 
    const.LEFT_INDEX) if the left name is correct and with their middle finger (const.RIGHT_MIDDLE 
    or const.LEFT_MIDDLE) if the right name is correct.
    """

    def __init__(self, clock, win, frameRate, expHandle, responseBox, 
                imageStim, name1, name2, duration = 5.0):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box

        imageStim : psychopy.visual.ImageStim
            The ImageStim of the face to be used for this trial

        name1 : str
            The name to be shown on the left

        name2 : str
            The name to be shown on the right

        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.responseBox = responseBox
        
        # stimulus stuff...
        self.image = imageStim
        self.name1 = visual.TextStim(win = self.win,
                                   text = name1,
                                   font = const.DEFAULT_FONT,
                                   pos = (-.3,-.6),
                                   color = 'white')
        self.name2 = visual.TextStim(win = self.win,
                                   text = name2,
                                   font = const.DEFAULT_FONT,
                                   pos = (.3, -.6),
                                   color = 'white')
        self.duration = duration

    def run(self):
        # make things visible
        self.image.setAutoDraw(True)
        self.name1.setAutoDraw(True)
        self.name2.setAutoDraw(True)

        # flush the serial device
        if self.responseBox:
            self.responseBox.reset_input_buffer() 
        responseRead = False

        # clear the event buffer
        event.clearEvents()

        # start new line for data output
        self.expHandle.nextEntry()
        self.expHandle.addData('trialStart',str(self.clock.getTime()))

        for i in range(0, int(self.frameRate * self.duration)):
            # refresh the screen
            self.win.flip()
            # check for response
            if not responseRead:
                # try to read data
                if self.responseBox:
                    data = self.responseBox.read(size=1)
                else:
                    data = None
                # make sure we're not reading a TLL Pulse
                while(data and ord(data) == const.TLL_PULSE):
                    data = self.responseBox.read(size=1)
                if data:
                    responseRead = True
                    self.expHandle.addData('response',data)
                    self.expHandle.addData('responseStamp',str(self.clock.getTime()))
            # check for abort signal
            if 'escape' in event.getKeys():
                print('Goodbye!')
                core.quit()
                
        # make things invisible
        self.image.setAutoDraw(False)
        self.name1.setAutoDraw(False)
        self.name2.setAutoDraw(False)

class Fixation(Routine):
    """
    Routine used for the inter-trial fixation
    """

    def __init__(self,clock,win,frameRate,expHandle,duration = 0.8):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.text = visual.TextStim(win = self.win,
                                   text = '+',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white')
        self.duration = duration

    def run(self):
        # make things visible
        self.text.setAutoDraw(True)
        # display for 0.8 seconds
        framesToShow = int(self.frameRate * self.duration)
        for i in range(0,framesToShow):
            self.win.flip() 
            if 'escape' in event.getKeys():
                print("Goodbye!")
                core.quit()
        # make things invisible
        self.text.setAutoDraw(False)

class RestBlock(Routine):
    """
    Routine used for the inter-block fixation

    Note
    ----
    During this routine, a white '+' is shown at the center of the screen for a duration
    of 20 seconds.
    """
    def __init__(self,clock,win,frameRate,expHandle, duration = 20.0):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.text = visual.TextStim(win = self.win,
                                   text = '+',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white')
        self.duration = duration

    def run(self):
        self.text.setAutoDraw(True)
        # display for 20 seconds
        framesToShow = int(self.frameRate * self.duration)
        for i in range(0,framesToShow):
            if 'escape' in event.getKeys():
                print("Goodbye!")
                core.quit()
            self.win.flip() 
        self.text.setAutoDraw(False)

class FacenameInstructions(Routine):
    """
    Routine used to display instructions for the nback task

    Note
    ----
    ....
    """

    def __init__(self, clock, win, frameRate, expHandle):
        """
        Initialize an instance of NBackInstructions

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.instructions = list()
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'In this experiment you will complete '
                                            'two types of tasks.',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'During the novel tasks, you will be '
                                            'shown a series of faces that you have '
                                            'NOT seen before alongside a name.\n\n'
                                            'Try to memorize this name and face.\n\n'
                                            'Press with your INDEX finger if you think '
                                            'the name goes well with the face.  Otherwise '
                                            'press with your MIDDLE finger.',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'During the known tasks, you wil be '
                                            'shown a series of faces that you have '
                                            'seen before alongside one name to the left '
                                            'and one name to the right.\n\nPress with your '
                                            'INDEX finger if the name on the left matches '
                                            'the face, and press with your MIDDLE finger if '
                                            'the name on the right matches the face.',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'Are you ready?',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
                                   

    def run(self):
        # display for 10 seconds
        for screen in self.instructions:
            # make text visible
            screen.setAutoDraw(True)
            # clear any remaining keypresses 
            event.clearEvents()    
            # display to screen
            self.win.flip() 
            # loop until spacebar is pressed
            while 'space' not in event.getKeys():
                pass
            screen.setAutoDraw(False)

class CountdownScreen(Routine):
    """
    Count down to the start of experiment

    Note
    ----
    Each 'count' lasts for approx 1 second
    """
    
    def __init__(self,clock,win,frameRate,expHandle):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.counts = list()
        
        # generate text stimuli for each value
        # NOTE: I'm not 100% sure this is any faster
        # than actually just changing the text.
        # is is possible that it is actually slower,
        # so it may be worth looking into
        for i in range(5,0,-1):
            self.counts.append(visual.TextStim(win = self.win,
                                   text = str(i),
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white'))

    def run(self):
        # cycle through each of the count downs...
        for count in self.counts:
            count.setAutoDraw(True)
            for i in range(0, int(self.frameRate)):
                if 'escape' in event.getKeys():
                    print("Goodbye")
                    core.quit()
                self.win.flip()
            count.setAutoDraw(False)

class MRISync(Routine):
    """
    Routine for waiting for the MRI TLL Pulse
    
    Note
    ----
    Can be included within other routines without altering the screen state
    """

    def __init__(self, clock, win, expHandle, responseBox):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.expHandle = expHandle
        self.responseBox = responseBox
    
    def run(self):
        if self.responseBox:
            # make sure we're not reading any old signals
            self.responseBox.reset_input_buffer()
            pulseSeen = False
            while(not pulseSeen):
                data = self.responseBox.read()
                if data and ord(data) == const.TLL_PULSE:
                    self.expHandle.addData('syncPulse',str(self.clock.getTime()))   
                    pulseSeen = True

class NovelCue(Routine):
    """
    Routine used to display instructions

    Note
    ----
    ....
    """

    def __init__(self, clock, win, frameRate, expHandle, duration = 2.0):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.text = visual.TextStim(win = self.win,
                                   text = 'NOVEL task',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white')
                                   
        self.duration = duration

    def run(self):
        self.text.setAutoDraw(True)
        # display for 10 seconds
        framesToShow = int(self.frameRate * self.duration)
        for i in range(0,framesToShow):
            if 'escape' in event.getKeys():
                print('Goodbye!')
                core.quit()
            self.win.flip() 
        self.text.setAutoDraw(False)

class KnownCue(Routine):
    """
    Routine used to display instructions

    Note
    ----
    ....
    """

    def __init__(self, clock, win, frameRate, expHandle, duration = 2.0):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.text = visual.TextStim(win = self.win,
                                   text = 'KNOWN task',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white')
        self.duration = duration                           

    def run(self):
        self.text.setAutoDraw(True)
        # display for 10 seconds
        framesToShow = int(self.frameRate * self.duration)
        for i in range(0,framesToShow):
            if 'escape' in event.getKeys():
                print('Goodbye!')
                core.quit()
            self.win.flip() 
        self.text.setAutoDraw(False)

########################################################################################
# N-Back routines
########################################################################################
class NBackTrial(Routine):
    """
    Routine used for n-back trial

    Note
    ----
    This trial lasts for approx 2 seconds.  The provided ImageStim is shown in the middle of
    the screen.  Assuming an image of approx 600x400px, the name is shown in the center 
    directly beneath the image.  

    Participants are expected to respond with their index finger (const.RIGHT_INDEX or 
    const.LEFT_INDEX) for 'yes' and with their middle finger (const.RIGHT_MIDDLE or 
    const.LEFT_MIDDLE) for no.
    """
    def __init__(self, clock, win, frameRate, expHandle, responseBox, imageStim, duration = 2.0):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box

        imageStim : psychopy.visual.ImageStim
            The ImageStim of the face to be used for this trial

        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.responseBox = responseBox
        
        # stimulus stuff...
        self.image = imageStim
    
        self.duration = duration

        self.matchtext = visual.TextStim(win = self.win,
                                   text = 'MATCH',
                                   font = const.DEFAULT_FONT,
                                   pos = (-.33, -.66),
                                   color = 'white')
        self.nomatchtext = visual.TextStim(win = self.win,
                                   text = 'NO MATCH',
                                   font = const.DEFAULT_FONT,
                                   pos = (.33, -.66),
                                   color = 'white')

    def run(self):
        
        # make things visible
        self.image.setAutoDraw(True)
        self.matchtext.setAutoDraw(True)
        self.nomatchtext.setAutoDraw(True)

        # flush the serial device
        if self.responseBox:
            self.responseBox.reset_input_buffer() 
        responseRead = False
        # reset the event buffer
        event.clearEvents() 

        # start new line for data output
        self.expHandle.nextEntry()
        self.expHandle.addData('trialStart',str(self.clock.getTime()))

        for i in range(0, int(self.frameRate * self.duration)):
            # refresh the screen
            self.win.flip()
            # check for response
            if not responseRead:
                # try to read data
                if self.responseBox:
                    data = self.responseBox.read(size=1)
                else:
                    data = None
                # make sure we're not reading a TLL Pulse
                while(data and ord(data) == const.TLL_PULSE):
                    data = self.responseBox.read(size=1)
                if data:
                    responseRead = True
                    self.expHandle.addData('response',data)
                    self.expHandle.addData('responseStamp',str(self.clock.getTime()))
            # check for abort signal
            if 'escape' in event.getKeys():
                print('Goodbye!')
                core.quit()

        # make things invisible
        self.image.setAutoDraw(False)
        self.matchtext.setAutoDraw(False)
        self.nomatchtext.setAutoDraw(False)

class TwoBackInstructions(Routine):
    """
    Routine used to display instructions for the nback task

    Note
    ----
    ....
    """

    def __init__(self, clock, win, frameRate, expHandle):
        """
        Initialize an instance of NBackInstructions

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.instructions = list()
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'In this experiment you will complete '
                                            'two types of tasks.',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'In the 0-back task, you will first be '
                                            'shown a target image.\n\nFor each of the '
                                            'images to follow, press your INDEX finger '
                                            'if the image MATCHES the target.\n\nOtherwise, '
                                            'press with your MIDDLE finger.',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'In the 2-back task, you will just be '
                                            'shown a series of images.\n\nFor each image '
                                            'press with your INDEX finger if the image '
                                            'MATCHES the image two previous.\n\nOtherwise, '
                                            'press with your MIDDLE finger.',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'Are you ready?',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
                                   

    def run(self):
        # display for 10 seconds
        for screen in self.instructions:
            # make text visible
            screen.setAutoDraw(True)
            # clear any remaining keypresses 
            event.clearEvents()    
            # display to screen
            self.win.flip() 
            # loop until spacebar is pressed
            while 'space' not in event.getKeys():
                pass
            screen.setAutoDraw(False)
class NBackInstructions(Routine):
    """
    Routine used to display instructions for the nback task

    Note
    ----
    ....
    """

    def __init__(self, clock, win, frameRate, expHandle):
        """
        Initialize an instance of NBackInstructions

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.instructions = list()
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'In this experiment you will complete '
                                            'two types of tasks.',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'In the 0-back task, you will first be '
                                            'shown a target image.\n\nFor each of the '
                                            'images to follow, press your INDEX finger '
                                            'if the image MATCHES the target.\n\nOtherwise, '
                                            'press with your MIDDLE finger.',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'In the 1-back task, you will just be '
                                            'shown a series of images.\n\nFor each image '
                                            'press with your INDEX finger if the image '
                                            'MATCHES the previous image.\n\nOtherwise, '
                                            'press with your MIDDLE finger.',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
        self.instructions.append(  visual.TextStim(win = self.win,
                                   text =   'Are you ready?',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white',
                                   wrapWidth=1.75))
                                   

    def run(self):
        # display for 10 seconds
        for screen in self.instructions:
            # make text visible
            screen.setAutoDraw(True)
            # clear any remaining keypresses 
            event.clearEvents()    
            # display to screen
            self.win.flip() 
            # loop until spacebar is pressed
            while 'space' not in event.getKeys():
                pass
            screen.setAutoDraw(False)

class TwoBackCue(Routine):
    """
    Routine used to display instructions

    Note
    ----
    ....
    """

    def __init__(self, clock, win, frameRate, expHandle, duration = 2.0):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.text = visual.TextStim(win = self.win,
                                   text = '1 - BACK',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white')

        self.duration = duration
                                   

    def run(self):
        self.text.setAutoDraw(True)
        # display for 10 seconds
        framesToShow = int(self.frameRate * self.duration)
        for i in range(0,framesToShow):
            if 'escape' in event.getKeys():
                print('Goodbye!')
                core.quit()
            self.win.flip() 
        self.text.setAutoDraw(False)
class OneBackCue(Routine):
    """
    Routine used to display instructions

    Note
    ----
    ....
    """

    def __init__(self, clock, win, frameRate, expHandle, duration = 2.0):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.text = visual.TextStim(win = self.win,
                                   text = '2 - BACK',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white')

        self.duration = duration
                                   

    def run(self):
        self.text.setAutoDraw(True)
        # display for 10 seconds
        framesToShow = int(self.frameRate * self.duration)
        for i in range(0,framesToShow):
            if 'escape' in event.getKeys():
                print('Goodbye!')
                core.quit()
            self.win.flip() 
        self.text.setAutoDraw(False)

class ZeroBackCue(Routine):
    """
    Routine used to display instructions

    Note
    ----
    ....
    """

    def __init__(self, clock, win, frameRate, expHandle, targetStim, duration = 2.0):
        """
        Initialize an instance of NovelTrial

        Parameters
        ----------
        clock : psychopy.clock.Clock
            The clock used for timing by this experiment
     
        win : psychopy.visual.Window
            The window to which this routine should be displayed to

        frameRate : int
            The refresh rate of win (obtained from getActualFrameRate)

        expHandle : psychopy.data.ExperimentHandler
            The ExperimentHandler being used for this experiment

        responseBox : serial.Serial
            The serial object used for the response box
        """
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        self.text = visual.TextStim(win = self.win,
                                   text = '0 - BACK',
                                   font = const.DEFAULT_FONT,
                                   pos = (-.5, 0),
                                   color = 'white')
        self.target = targetStim
        self.duration = duration
                                   

    def run(self):
        self.text.setAutoDraw(True)
        self.target.setAutoDraw(True)
        # display for 10 seconds
        framesToShow = int(self.frameRate * self.duration)
        for i in range(0,framesToShow):
            if 'escape' in event.getKeys():
                print('Goodbye!')
                core.quit()
            self.win.flip() 
        self.target.setAutoDraw(False)
        self.text.setAutoDraw(False)
