#!/usr/bin/python2
# -*- coding: utf-8 -*-
###############################################################################
# Written by:       Forrest Koch (forrest.koch@unsw.edu.au)
# Organization:     Centre for Healthy Brain Ageing (UNSW)
# PyschoPy Version: 1.85.3
# Python Version:   2.7.5
###############################################################################

from abc import ABCMeta, abstractmethod, abstractproperty

class AbstractFeature(object):
    """
    Base class for deriving classes to be used by this framework.
    """    
    __metaclass__ = ABCMeta


    @property
    def origin(self):
        """
        AbstractFeature : This is the feature which has been decorated.

        If this value is None, the feature to which this property belongs is the base.
        """
        return self._origin

    @property
    def experiment(self):
        """
        Experiment : This is the experiment to which the feature belongs.
        """
        return self._experiment

    @abstractmethod
    def __init__(self, origin, experiment = None):
        """
        This method should be called by all deriving classes.

        Parameters
        ----------
        origin : AbstractFeature
            The feature which is being decorated.  None if this is the base.
        experiment : Experiment
            The experiment to which the feature belongs. Not necessary if this is not the base.
        """
        self._origin = origin
        
        if self.origin:
            self._experiment = origin.experiment
        else:
            if not experiment:
                raise TypeError('Experiment = None')
            self._experiment = experiment

    def start(self):
        """
        Calls the start methods of origin features to prepare them to be run.

        If extending this class, make sure you use super to call this function.
        """
        if self.origin:
            self.origin.start()

    def run(self):
        """
        Calls the run methods of origin features to execute them.

        If extending this class, make sure you use super to call this function.
        """
        if self.origin:
            self.origin.run()

    def end(self):
        """
        Calls the end methods of origin features to indicate they are done being run

        If extending this class, make sure you use super to call this function.
        """
        if self.origin:
            self.origin.end()

class AbstractCollection(AbstractFeature):
    """
    This class should be used to make declarations more legible and to abstract away
    the contents of the collection.

    It also serves as a barrier, preventing the contents from being started (and ended) until
    this collection is itself run.
    """
    
    __metaclass__ = ABCMeta

    @abstractproperty
    def feature(self):
        """
        AbstractFeature : The feature being decorated
        """
        return None

    @abstractmethod
    def __init__(self, origin, experiment = None):
        """
        This method should be called by all deriving classes.

        Parameters
        ----------
        origin : AbstractFeature
            The feature which is being decorated.  None if this is the base.
        experiment : Experiment
            The experiment to which the feature belongs. Not necessary if this is not the base
        """
        super(AbstractCollection,self).__init__(origin, experiment = experiment)

    def start(self):
        """
        Do nothing.  Contents will not be started until the collection is run.        
        """
        pass

    def run(self):
        """
        Run start, run, and end the contents
        """

        self.feature.start()
        self.feature.run()
        self.feature.end()

    def end(self):
        """
        Do nothing.  Contents will be ended when the collection is run.        
        """
        pass

class AbstractLoop(AbstractFeature):
    """
    This class is similar to a collection; however, it provides a mechanism
    for continuously running a feature dependent on some status criterea.
    """

    __metaclass__ = ABCMeta


    @abstractproperty
    def status(self):
        """
        Boolean : used to indicate whether the loop should continue 
        """
        return False 

    @abstractmethod
    def __init__(self, origin, experiment = None):
        """
        This method should be called by all deriving classes.

        Parameters
        ----------
        origin : AbstractFeature
            The feature which is being decorated.  None if this is the base.
        experiment : Experiment
            The experiment to which the feature belongs. Not neccesary if this is not the base.
        """
        super(AbstractLoop,self).__init__(origin, experiment = experiment)

    @abstractmethod
    def initializeLoop(self):
        """
        Should be used to set any conditions prior to execution of the loop (e.g status property)
        """
        pass

    @abstractmethod
    def updateStatus(self):
        """
        Should be used to update the status property accordingly
        """
        pass

    @abstractmethod
    def destroyLoop(self):
        """
        Should be used to take care of anything that needs to be done upon completion of the loop
        """
        pass


    def start(self):
        """
        Does nothing.  Origin feature will be started when this loop is run
        """
        pass

    def run(self):
        """
        Continuously runs the origin feature until stats = False
        """
        self.initializeLoop()
        self.origin.start()
        while(self.status):
            self.origin.run()
            self.updateStatus()
        self.origin.end()
        self.destroyLoop()

    def end(self):
        """
        Does nothing.  Origin feature will be ended when this loop is run
        """
        pass

class IteratingFeature(AbstractFeature):

    def __init__(self, featureList, experiment):
        super(IteratingFeature,self).__init__(None, experiment = experiment)
        self._featureList = list(featureList)

    def start(self):
        """
        Does nothing.  Origin feature will be started when this loop is run
        """
        pass

    def run(self):
        """
        Continuously runs the origin feature until stats = False
        """
        for f in self._featureList:
            f.start()
            f.run()
            f.end()

    def end(self):
        """
        Does nothing.  Origin feature will be ended when this loop is run
        """
        pass
    
