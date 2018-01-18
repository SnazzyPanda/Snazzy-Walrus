'''

@author: Snazzy Panda
'''

class ListParams(object):

    KEY_START = "key_start"
    KEY_EXCLUDES = "key_excludes"
    KEY_INCLUDE_ONLY = "key_include_only"


    def __init__(self, startingPath = None, excludes = None, includeOnly = None):
        self.startingPath = startingPath
        self.excludes = excludes
        self.includeOnly = includeOnly
    # end constructor

    def getAsDict(self):
        outputDict = dict()
        outputDict[self.KEY_START] = self.startingPath
        outputDict[self.KEY_EXCLUDES] = self.excludes
        outputDict[self.KEY_INCLUDE_ONLY] = self.includeOnly
        
        return outputDict
    # end getAsDict
    
    def loadFromDict(self, inputDict):
        self.startingPath = inputDict[self.KEY_START]
        self.excludes = inputDict[self.KEY_EXCLUDES]
        self.includeOnly = inputDict[self.KEY_INCLUDE_ONLY]
    # end loadFromDict
    
    def __eq__(self, other):
       return (self.startingPath == other.startingPath and self.excludes == other.excludes and self.includeOnly == other.includeOnly)
    # end __eq__



