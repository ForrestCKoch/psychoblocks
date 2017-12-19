from psychopy import core, visual
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
    """
    def __init__(self, clock, win, frameRate, expHandle, imageStim, name):
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        
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
        self.image.setAutoDraw(True)
        self.name.setAutoDraw(True)
        self.prompt.setAutoDraw(True)
        for i in range(0, int(self.frameRate * 5.0)):
            self.win.flip()
        self.image.setAutoDraw(False)
        self.name.setAutoDraw(False)
        self.prompt.setAutoDraw(False)

class KnownTrial(Routine):
    """
    Routine used for the known face-name exposures
    """

    def __init__(self, clock, win, frameRate, expHandle, imageStim, name1, name2):
        self.clock = clock
        self.win = win
        self.frameRate = frameRate
        self.expHandle = expHandle
        
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
        self.image.setAutoDraw(True)
        self.name1.setAutoDraw(True)
        self.name2.setAutoDraw(True)
        for i in range(0, int(self.frameRate * 5.0)):
            self.win.flip()
        self.image.setAutoDraw(False)
        self.name1.setAutoDraw(False)
        self.name2.setAutoDraw(False)

class Fixation(Routine):
    """
    Routine used for the inter-trial fixation
    """

    def __init__(self,clock,win,frameRate,expHandle):
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
        # display for 0.8 seconds
        framesToShow = int(self.frameRate * 0.8)
        for i in range(0,framesToShow):
           self.win.flip() 
        self.text.setAutoDraw(False)

class RestBlock(Routine):
    """
    Routine used for the inter-block fixation
    """
    def __init__(self,clock,win,frameRate,expHandle):
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
        # display for 25 seconds
        framesToShow = int(self.frameRate * 25)
        for i in range(0,framesToShow):
           self.win.flip() 
        self.text.setAutoDraw(False)

class InstructScreen(Routine):
    """
    Routine used to display instructions
    """

    def __init__(self, clock, win, frameRate, expHandle):
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
           self.win.flip() 
        self.text.setAutoDraw(False)

class CountdownScreen(Routine):
    """
    Count down to the start of experiment
    """
    
    def __init__(self,clock,win,frameRate,expHandle):
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
                self.win.flip()
            count.setAutoDraw(False)

class MRISync(Routine):
    """
    Routine for waiting for the MRI TLL Pulse
    
    Note
    ----
    Can be included within other routines without altering the screen state
    """

    def __init__(self,clock,win,expHandle):
        pass
    
    def run(self):
        pass
