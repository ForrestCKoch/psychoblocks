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
from fw import *
from new_routines import *

class CountdownSequence(AbstractCollection):

    def __init__(self, experiment):
        featureList = list()
        for i in range(5,0,-1):
            feature = EscapeCheck(None,experiment = experiment)
            feature = TextStim(feature, text=str(i))
            feature = TimedLoop(1.0, feature)
            featureList.append(feature)
        self._feature = IteratingFeature(featureList, experiment)
    
    @property
    def feature(self):
        return self._feature

    

class Fixation(AbstractCollection):

    def __init__(self, duration, experiment):
        feature = EscapeCheck(None, experiment = experiment)
        feature = TextStim(feature, text = '+')
        feature = TimedLoop(duration, feature)
         
    @property
    def feature(self):
        return self._feature

class RestBlock(AbstractCollection):
    
    def __init__(self, duration, experiment):
        feature = EscapeCheck(None, experiment = experiment)
        feature = TextStim(feature, text = '+')
        feature = TimedLoop(duration, feature)
    
    @property
    def feature(self):
        return self._feature

###############################################################################
# Facename Collections
###############################################################################
class FacenameInstructions(AbstractCollection):
    
    def __init__(self, experiment):
        textlist = ['In this experiment you will complete '
                    'two types of tasks.',
                    'During the novel tasks, you will be '
                    'shown a series of faces that you have '
                    'NOT seen before alongside a name.\n\n'
                    'Try to memorize this name and face.\n\n'
                    'Press with your INDEX finger if you think '
                    'the name goes well with the face.  Otherwise '
                    'press with your MIDDLE finger.',
                    'During the known tasks, you wil be '
                    'shown a series of faces that you have '
                    'seen before alongside one name to the left '
                    'and one name to the right.\n\nPress with your '
                    'INDEX finger if the name on the left matches '
                    'the face, and press with your MIDDLE finger if '
                    'the name on the right matches the face.',
                    'Are you ready?']
        featureList = list()
        for text in textlist:
            feature = EscapeCheck(None, experiment = experiment)
            feature = TextStim(feature, text = text)
            feature = SpacebarLoop(feature)
            featureList.append(feature)
        self._feature = IteratingFeature(featureList,experiment)
    
    @property
    def feature(self):
        return self._feature

class NovelTrial(AbstractCollection):
    
    def __init__(self, experiment):
        pass
     
    @property
    def feature(self):
        return self._feature

class KnownTrial(AbstractCollection):
    
    def __init__(self, experiment):
        pass
    @property
    def feature(self):
        return self._feature

class NovelCue(AbstractCollection):
    
    def __init__(self, experiment):
        pass
    @property
    def feature(self):
        return self._feature

class KnownCue(AbstractCollection):
    
    def __init__(self, experiment):
        pass
    @property
    def feature(self):
        return self._feature
###############################################################################
# NBack Collections
###############################################################################
class OneBackInstructions(AbstractCollection):
    
    def __init__(self, experiment):
        pass
    @property
    def feature(self):
        return self._feature

class TwoBackInstructions(AbstractCollection):
    
    def __init__(self, experiment):
        pass
    @property
    def feature(self):
        return self._feature

class NBackTrial(AbstractCollection):
    
    def __init__(self, experiment):
        pass
    @property
    def feature(self):
        return self._feature

class ZeroBackCue(AbstractCollection):
    
    def __init__(self, experiment):
        pass
    @property
    def feature(self):
        return self._feature

class OneBackCue(AbstractCollection):
    
    def __init__(self, experiment):
        pass
    @property
    def feature(self):
        return self._feature

class TwoBackCue(AbstractCollection):
    
    def __init__(self, experiment):
        pass
    @property
    def feature(self):
        return self._feature

                                   

