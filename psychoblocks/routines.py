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

    def __init__(self, experiment):
        super(CountdownSequence,self).__init__(None, experiment = experiment)
        featureList = list()
        for i in range(5,0,-1):
            feature = EscapeCheck(None,experiment = experiment)
            feature = TextFeature(feature, text = str(i), name = 'Countdown '+str(i))
            feature = TimedLoop(feature, 1.0)
            featureList.append(feature)
        self._feature = IteratingFeature(featureList, experiment)
    
    @property
    def feature(self):
        return self._feature

    

class Fixation(AbstractCollection):

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
    
    def __init__(self, experiment):
        super(FNInstructions,self).__init__(None, experiment = experiment)
        textlist = ['You will be shown a series of face name pairs.'
                    'We will test your memory of these pairs after the scan.'
                    'During the task, please press with you RIGHT INDEX finger'
                    'if you the the name is a good fit for the face.'
                    'otherwise press with your RIGHT MIDDLE finger.']
                
        featureList = list()
        count = 1

        for text in textlist:
            feature = EscapeCheck(None, experiment = experiment)
            feature = TextFeature(feature, text = text, name = 'Instructions '+str(count))
            feature = SpacebarLoop(feature)
            featureList.append(feature)
            count += 1

        self._feature = IteratingFeature(featureList,experiment)
    
    @property
    def feature(self):
        return self._feature

class FacenameTrial(AbstractCollection):
    
    def __init__(self, experiment, image, name, duration = 5.0):
        super(FacenameTrial,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = ResponseBox(feature, None)
        feature = ImageFeature(feature, image = image, name = 'Trial Image: ' + image, units='pix',size=(569,400))
        feature = TextFeature(feature, text = "Is this name a good fit for the face?", 
                                       pos=(0,.8), name = 'Trial Prompt')
        feature = TextFeature(feature, text= name+'?', pos= (0,.6), name= 'Trial Name: '+name)
        feature = TextFeature(feature, text = 'YES', name = 'Yes Prompt', pos = (-.33, -.66))
        feature = TextFeature(feature, text = 'NO', name = 'No Prompt', pos = (.33,-.66))
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
    
    def __init__(self, experiment, image, rname, lname, correct):
        super(RecallTrial,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = ImageFeature(feature, image = image, name = 'Trial Image: ' + image, units='pix',size=(569,400))
        feature = TextFeature(feature, text = "Who is this?", 
                                       pos=(0,.8), name = 'Trial Prompt')
        feature = TextFeature(feature, text = lname, name = 'Yes Prompt', pos = (-.33, -.66))
        feature = TextFeature(feature, text = rname, name = 'No Prompt', pos = (.33,-.66))

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
