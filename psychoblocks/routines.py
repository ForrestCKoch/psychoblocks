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
from abstracts import *
from features import *

class CountdownSequence(AbstractCollection):
    """
    This routine will display the digits 1-5 in decreasing order for 1s each.
    """
    
    def __init__(self, experiment, length=5,time=1.0):
        super(CountdownSequence,self).__init__(None, experiment = experiment)
        featureList = list()
        for i in range(length,0,-1):
            feature = EscapeCheck(None,experiment = experiment)
            feature = TextFeature(feature, text = str(i), name = 'Countdown '+str(i))
            feature = TimedLoop(feature, time)
            featureList.append(feature)
        self._feature = IteratingFeature(featureList, experiment)
    
    @property
    def feature(self):
        return self._feature

    

class Fixation(AbstractCollection):
    """
    This routine will display a fixation ("+") for the specified duration.
    """

    def __init__(self, experiment, duration = 0.8):
        super(Fixation,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = TextFeature(feature, text = '+', name = 'Fixation')
        feature = TimedLoop(feature, duration)
        self._feature = feature
         
    @property
    def feature(self):
        return self._feature

class RestBlock(AbstractCollection):
    """
    Effectively the same as Fixation... I'm not actually sure why we have this
    """
    
    def __init__(self, experiment, duration = 20.0):
        super(RestBlock,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = TextFeature(feature, text = '+', name = 'Rest Block')
        feature = TimedLoop(feature, duration)
        self._feature = feature
    
    @property
    def feature(self):
        return self._feature

class UpdateExaminerWindow(AbstractCollection):
    """
    Update the examiner window with patient response information.  This includes:
        - Number of responses under 200ms
        - Number of non-responses
        - Number of Total responses

    This routine should be called sparingly as it will introduce ~1 frame's worth
    of delay to be added to the experiment with each call.
    """

    def __init__(self,experiment):
        super(UpdateExaminerWindow,self).__init__(None,experiment = experiment)

        self._feature1 = ExaminerTextFeature(None, experiment = experiment, pos = (0,.5), name = 'Ex1')
        self._feature2 = ExaminerTextFeature(self._feature1,experiment=experiment,pos=(0,0),name='Ex2')
        self._feature3 = ExaminerTextFeature(self._feature2,experiment=experiment,pos=(0,-.5),name='Ex3')
        self._feature = self._feature3 

    def start(self):
        super(UpdateExaminerWindow,self).start()
        # update the features
        self._feature1._textStim.setText(text='Responses Under 200ms = '
                    +str(self.experiment.responsesUnder200ms))
        self._feature2._textStim.setText(text='Non - Reponses = '
                    +str(self.experiment.responsesExpected - self.experiment.responseTotal))
        self._feature3._textStim.setText(text='Total Responses = '
                    +str(self.experiment.responseTotal))
        self.feature.start()
        self.experiment.examinerWindow.flip()

    def run(self):
        pass
    
    def end(self):
        pass

    @property
    def feature(self):
        return self._feature

###############################################################################
# Facename Collections
###############################################################################
class FNInstructions(AbstractCollection):
    """
    This routine will display the instructions for the face name pair task.
    It will remain on the screen until the spacebar is pressed.
    """
    
    def __init__(self, experiment):
        super(FNInstructions,self).__init__(None, experiment = experiment)
        textlist = ['You will be shown faces and names.',
                    'Try and remember the face and name for each person.',
                    'Press the left button if the the name is a good fit.',
                    'Otherwise, press the right button.',
                    'Remember, there is no right or wrong answer.']
                
        featureList = list()
        count = 1

        for text in textlist:
            feature = EscapeCheck(None, experiment = experiment)
            feature = TextFeature(feature, text = text, name = 'Instructions '+str(count))
            if experiment.examinerScreen == 'yes':
                feature = ExaminerTextFeature(feature, text = text, name = 'Instructions '+str(count))
                feature = SpacebarLoop(feature,updateExaminer=True)
            else:
                feature = SpacebarLoop(feature,updateExaminer=False)
            featureList.append(feature)
            count += 1

        self._feature = IteratingFeature(featureList,experiment)
    
    @property
    def feature(self):
        return self._feature

class FacenameTrial(AbstractCollection):
    """
    This routine will run the face name trial.
    """
 
    def __init__(self, experiment, image, name, duration = 5.0):
        """
        Parameters
        ----------
        experiment : Experiment
            The experiment to which this routine belongs.
        image : Str
            The path of the image to be used for this trial.
        name : Str
            The name to be associated with this face.
        duration : float
            The number of seconds which this trial should run for
        """
        super(FacenameTrial,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = ResponseBox(feature, None)
        feature = ImageFeature(feature, image = image, name = 'Trial Image: ' + image, units='norm')
        feature = TextFeature(feature, text= name, pos= (0,.8), name= 'Trial Name: '+name)
        feature = TextFeature(feature, text = 'YES', name = 'Yes Prompt', pos = (-.33, -.8))
        feature = TextFeature(feature, text = 'NO', name = 'No Prompt', pos = (.33,-.8))
        feature = TimedLoop(feature, duration)
        self._feature = feature
     
    @property
    def feature(self):
        return self._feature

    def run(self):
        # advance the data entry to next
        self.feature.experiment.experimentHandler.nextEntry()
        super(FacenameTrial,self).run()

class RecallTrial(AbstractCollection):
    """
    This routine will run the recall trial used for post-scan testing
    """
    
    def __init__(self, experiment, image, lname, rname, correct):
        """
        Parameters
        ----------
        experiment : Experiment
            The experiment to which this routine belongs.
        image : Str
            The path of the image to be used for this trial.
        rname : Str
            The name to be displayed on the right of the screen.
        lname : Str
            The name to be displayed on the left of the screen.
        correct : Str
            'left' or 'right'.  Indicates which name is actually correct.
        """
        super(RecallTrial,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = ImageFeature(feature, image = image, name = 'Trial Image: ' + image, units='pix',size=(569,400))
        feature = TextFeature(feature, text = lname, name = 'Yes Prompt', pos = (-.5, -.8))
        feature = TextFeature(feature, text = rname, name = 'No Prompt', pos = (.5,-.8))

        if correct == 'left':
            corr_resp = const.RIGHT_INDEX
        else:
            corr_resp = const.RIGHT_MIDDLE

        feature = ResponseBox(feature, corr_resp)
        feature = WaitForResponse(feature, None)
        self._feature = feature
     
    @property
    def feature(self):
        return self._feature

    def run(self):
        # advance the data entry to next
        self.feature.experiment.experimentHandler.nextEntry()
        super(RecallTrial,self).run()

class ConfidenceTrial(AbstractCollection):
    """
    This routine is to follow RecalTrial, and is used to indicate how confident the 
    participant is in their previous answer.
    """

    def __init__(self, experiment):
        super(ConfidenceTrial,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = TextFeature(feature, text = "How confident are you?")
        feature = TextFeature(feature, text = "High", pos = (-.33,-.66))
        feature = TextFeature(feature, text = "Low", pos = (.33,-.66))
        feature = ResponseBox(feature, None)
        feature = WaitForResponse(feature)
        self._feature = feature

    @property
    def feature(self):
        return self._feature

    def run(self):
        # advance the data entry to next
        self.feature.experiment.experimentHandler.nextEntry()
        super(ConfidenceTrial,self).run()

class WaitForTLL(AbstractCollection):
    """
    This routine is used to sync with the MRI machine.  It will
    display a 'waiting for TLL pulse' message and hang until
    the pulse is recieved
    """

    def __init__(self, experiment):
        super(WaitForTLL,self).__init__(None, experiment = experiment)
        feature = TextFeature(None,experiment = experiment, text = "Get Ready.  Waiting for scanner.")
        if self.experiment.examinerScreen == 'yes':
            feature = ExaminerTextFeature(feature,text = "Waiting for TLL pulse")
        feature = MRISync(feature)
        self._feature = feature

    def run(self):
        self.feature.start()
        self.experiment.participantWindow.flip()
        if self.experiment.examinerScreen == 'yes':
            self.experiment.examinerWindow.flip()
        self.feature.run()
        self.feature.end()
        # need to clear the examinerScreen
        if self.experiment.examinerScreen == 'yes':
            self.experiment.examinerWindow.flip()

    @property
    def feature(self):
        return self._feature

class Calibration(AbstractCollection):
    """
    This routine will display a number in each corner for calibration purposes
    It will remain on the screen until the spacebar is pressed.
    """
    
    def __init__(self, experiment):
        super(Calibration,self).__init__(None, experiment = experiment)

        feature = TextFeature(None, experiment = experiment, text = '4', name = 'BR',pos=(0.6,-0.85))
        feature = TextFeature(feature, text = '2', name = 'TR',pos=(0.6,0.85))
        feature = TextFeature(feature, text = '3', name = 'BL',pos=(-0.6,-0.85))
        feature = TextFeature(feature, text = '1', name = 'TL',pos=(-0.6,0.85))
        self._feature = SpacebarLoop(feature,updateExaminer=False)
    
    @property
    def feature(self):
        return self._feature
