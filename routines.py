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

class Routine:
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
    def __init__(self, clock, win, frameRate, expHandle, responseBox, imageStim, name):
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

        print("Novel Trial started at "+str(self.clock.getTime()))

        for i in range(0, int(self.frameRate * 5.0)):
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
                    print("\tResponse: "+data+" received at "+str(self.clock.getTime()))
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

    def __init__(self, clock, win, frameRate, expHandle, responseBox, imageStim, name1, name2):
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

        print("Known Trial started at "+str(self.clock.getTime()))

        for i in range(0, int(self.frameRate * 5.0)):
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
                    print("\tResponse: "+data+" received at "+str(self.clock.getTime()))
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
        self.text = visual.TextStim(win = self.win,
                                   text = '+',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white')

    def run(self):
        # make things visible
        self.text.setAutoDraw(True)
        # display for 0.8 seconds
        framesToShow = int(self.frameRate * 0.8)
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
        self.text = visual.TextStim(win = self.win,
                                   text = '+',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white')

    def run(self):
        self.text.setAutoDraw(True)
        # display for 20 seconds
        framesToShow = int(self.frameRate * 20)
        for i in range(0,framesToShow):
            if 'escape' in event.getKeys():
                print("Goodbye!")
                core.quit()
            self.win.flip() 
        self.text.setAutoDraw(False)

class InstructScreen(Routine):
    """
    Routine used to display instructions

    Note
    ----
    ....
    """

    def __init__(self, clock, win, frameRate, expHandle):
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
                                   text = 'INSTRUCTIONS',
                                   font = const.DEFAULT_FONT,
                                   pos = (0, 0),
                                   color = 'white')
                                   

    def run(self):
        self.text.setAutoDraw(True)
        # display for 10 seconds
        framesToShow = int(self.frameRate * 3)
        for i in range(0,framesToShow):
            if 'escape' in event.getKeys():
                print("Goodbye!")
                core.quit() 
            self.win.flip() 
        self.text.setAutoDraw(False)

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
                    print("Synced with pulse at "+str(self.clock.getTime()))
                    pulseSeen = True
            
