'''

@author: Snazzy Panda
'''
from snazzy.settings.ImageSettings import ImageSettings

class Image(object):
    '''
    classdocs
    '''
    KEY_SRC = "key_src"
    KEY_SETTINGS = "key_image_settings"


    def __init__(self, fileAbsPath = None):
        '''
        Constructor
        '''
        self.settings = ImageSettings()
        self.src = fileAbsPath
    # end constructor

    def getAsDict(self):
        outputDict = dict()
        outputDict[self.KEY_SRC] = self.src
        outputDict[self.KEY_SETTINGS] = self.settings.getAsDict()
        return outputDict
    # end getAsDict

    def loadFromDict(self, inputDict):
        self.src = inputDict[self.KEY_SRC]
        self.settings = ImageSettings()
        self.settings.loadFromDict(inputDict[self.KEY_SETTINGS])
    # end loadFromDict

    def equals(self, other):
        '''
        Returns true if objects refer to same source image
        '''
        return self.src is other.src
    # end equals

    def trueEquals(self, other):
        '''
        Returns true if objects are completely equal
        '''
        return (self.src is other.src) and self.settings.hasSameSettingsAs(other.settings)
    # end trueEquals
    
    def __eq__(self, other):
        return self.src == other.src
    # end __eq__
