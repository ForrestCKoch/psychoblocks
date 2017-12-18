import abc

class abstractClass:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        self.test = 1

    @abc.abstractmethod
    def getTest(self):
        return self.test

class concreteClass(abstractClass):

    def __init__(self, value):
        super(concreteClass,self).__init__()
        self.value=2

    def getTest(self):
        return self.test

    def getSuperTest(self):
        return super(concreteClass,self).getTest()

    def getValue(self):
        return self.value 
