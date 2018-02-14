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
class FacenameInstructions(AbstractCollection):
    
    def __init__(self, experiment):
        super(FacenameInstructions,self).__init__(None, experiment = experiment)
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

class FNInstructions(AbstractCollection):
    
    def __init__(self, experiment):
        super(FNInstructions,self).__init__(None, experiment = experiment)
        textlist = ['You will be shown a series of face name pairs.\n\n'
                    'If you recognize the face, and the name is correct, '
                    'press YES.  Otherwise, press NO.']
                   
                  
                 
                
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

class NovelTrial(AbstractCollection):
    
    def __init__(self, experiment, image, name, duration = 5.0):
        super(NovelTrial,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = ResponseBox(feature, None)
        feature = ImageFeature(feature, image = image, name = 'Novel Trial Image: ' + image)
        feature = TextFeature(feature, text= name, pos= (0,-.6), name= 'Novel Trial Name: '+name)
        feature = TextFeature(feature, text = "Does this face 'fit' this name?", 
                                       pos=(0,-.8), name = 'Novel Trial Prompt')
        feature = TimedLoop(feature, duration)
        self._feature = feature
     
    @property
    def feature(self):
        return self._feature

    def run(self):
        # advance the data entry to next
        self.feature.experiment.experimentHandler.nextEntry()
        super(NovelTrial,self).run()

class KnownTrial(AbstractCollection):
    
    def __init__(self, experiment, image, name1, name2, correctResponse, duration = 5.0):
        super(KnownTrial,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = ResponseBox(feature, correctResponse)
        feature = ImageFeature(feature, image = image, name = 'Known Trial Image: ' + image)
        feature = TextFeature(feature, text=name1, pos=(-.3,-.6), name='Known Trial Name1: '+name1)
        feature = TextFeature(feature, text=name2, pos=(0.3,-.6), name='Known Trial Name2: '+name2)
        feature = TimedLoop(feature, duration)
        self._feature = feature
        

    @property
    def feature(self):
        return self._feature

    def run(self):
        # advance the data entry to next
        self.feature.experiment.experimentHandler.nextEntry()
        super(KnownTrial,self).run()
    
class NovelCue(AbstractCollection):
    
    def __init__(self, experiment, duration = 2.0):
        super(NovelCue,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = TextFeature(feature, text='NOVEL task', name = 'Known Cue')
        feature = TimedLoop(feature, duration)
        self._feature = feature

    @property
    def feature(self):
        return self._feature

class KnownCue(AbstractCollection):
    
    def __init__(self, experiment, duration = 2.0):
        super(KnownCue,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = TextFeature(feature, text='KNOWN task', name = 'Known Cue')
        feature = TimedLoop(feature, duration)
        self._feature = feature

    @property
    def feature(self):
        return self._feature
###############################################################################
# NBack Collections
###############################################################################
class OneBackInstructions(AbstractCollection):
    
    def __init__(self, experiment):
        super(OneBackInstructions,self).__init__(None, experiment = experiment)
        textlist = ['In this experiment you will complete '
                    'two types of tasks.',
                    'In the 0-back task, you will first be '
                    'shown a target image.\n\nFor each of the '
                    'images to follow, press your INDEX finger '
                    'if the image MATCHES the target.\n\nOtherwise, '
                    'press with your MIDDLE finger.',
                    'In the 1-back task, you will just be '
                    'shown a series of images.\n\nFor each image '
                    'press with your INDEX finger if the image '
                    'MATCHES the previous image.\n\nOtherwise, '
                    'press with your MIDDLE finger.',
                    'Are you ready?']
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

class TwoBackInstructions(AbstractCollection):
    
    def __init__(self, experiment):
        super(TwoBackInstructions,self).__init__(None, experiment = experiment)
        textlist = ['In this experiment you will complete '
                    'two types of tasks.',
                    'In the 0-back task, you will first be '
                    'shown a target image.\n\nFor each of the '
                    'images to follow, press your INDEX finger '
                    'if the image MATCHES the target.\n\nOtherwise, '
                    'press with your MIDDLE finger.',
                    'In the 2-back task, you will just be '
                    'shown a series of images.\n\nFor each image '
                    'press with your INDEX finger if the image '
                    'MATCHES the image two previous.\n\nOtherwise, '
                    'press with your MIDDLE finger.',
                    'Are you ready?']
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

class NBackTrial(AbstractCollection):
    
    def __init__(self, experiment, image, correctResponse, duration = 2.5):
        super(NBackTrial,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = ResponseBox(feature, correctResponse)
        feature = ImageFeature(feature, image = image, name = 'Trial: '+image)
        feature = TextFeature(feature, text = 'MATCH', name = 'Match Prompt', pos = (-.33, -.66))
        feature = TextFeature(feature, text = 'NO MATCH', name = 'Match Prompt', pos = (.33,-.66))
        feature = TimedLoop(feature, duration) 

        self._feature = feature

    @property
    def feature(self):
        return self._feature

    def run(self):
        # advance the data entry to next
        self.feature.experiment.experimentHandler.nextEntry()
        super(NBackTrial,self).run()

class ZeroBackCue(AbstractCollection):
    
    def __init__(self, experiment, image, duration = 2.5):
        super(ZeroBackCue,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = ImageFeature(feature,image=image,name='Zero Back Cue Image: '+image,pos=(0.33,0))
        feature = TextFeature(feature, text = '0 - BACK', name = 'Zero Back Cue Text',pos=(-.5,0))
        feature = TimedLoop(feature, duration) 
        
        self._feature = feature

    @property
    def feature(self):
        return self._feature

class OneBackCue(AbstractCollection):
    
    def __init__(self, experiment, duration = 2.5):
        super(OneBackCue,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = TextFeature(feature, text = '1 - BACK', name = 'One Back Cue Text')
        feature = TimedLoop(feature, duration)
        
        self._feature = feature

    @property
    def feature(self):
        return self._feature

class TwoBackCue(AbstractCollection):
    
    def __init__(self, experiment, duration = 2.5):
        super(TwoBackCue,self).__init__(None, experiment = experiment)
        feature = EscapeCheck(None, experiment = experiment)
        feature = TextFeature(feature, text = '2 - BACK', name = 'One Back Cue Text')
        feature = TimedLoop(feature, duration)
        
        self._feature = feature

    @property
    def feature(self):
        return self._feature
