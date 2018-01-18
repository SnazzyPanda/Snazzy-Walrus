'''

@author: Snazzy Panda
'''
from .ImageSettings import ImageSettings

class ImageListSettings(ImageSettings):
    '''
    classdocs
    '''

    # int time in minutes?
    DEFAULT_INTERVAL = None
    # boolean
    DEFAULT_DISPLAY_PREVIEW = None
    # boolean
    DEFAULT_RANDOM_NEXT = None
    
    KEY_INTERVAL = "key_interval"
    KEY_DISPLAY_PREVIEW = "key_display_preview"
    KEY_RANDOM_NEXT = "key_random_next"

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.interval = self.DEFAULT_INTERVAL
        self.displayPreview = self.DEFAULT_DISPLAY_PREVIEW
        self.randomNext = self.DEFAULT_RANDOM_NEXT
        #additionally need: interval, display preview, randomnext, more?
    # end constructor
    
    def isIntervalDefault(self):
        return self.interval is self.DEFAULT_INTERVAL
    
    def isDisplayPreviewDefault(self):
        return self.displayPreview is self.DEFAULT_DISPLAY_PREVIEW
    
    def isRandomNextDefault(self):
        return self.randomNext is self.DEFAULT_RANDOM_NEXT
    
    def resetToDefaults(self):
        ImageSettings.resetToDefaults(self)
        self.interval = self.DEFAULT_INTERVAL
        self.displayPreview = self.DEFAULT_DISPLAY_PREVIEW
        self.randomNext = self.DEFAULT_RANDOM_NEX
    # end resetToDefaults
    
    def isEdited(self):
        return (ImageSettings.isEdited(self) or not self.isIntervalDefault()
                or not self.isDisplayPreviewDefault() or not self.isRandomNextDefault())
    # end isEdited
    
    def hasSameSettingsAs(self, other):
        return (ImageSettings.hasSameSettingsAs(self, other) and (self.interval is other.interval)
                and (self.displayPreview is other.displayPreview) and (self.randomNext is other.randomNext))
    # end hasSameSettingsAs
    
    def copyAllSettingsFrom(self, other):
        ImageSettings.copyAllSettingsFrom(self, other)
        self.interval = other.interval
        self.displayPreview = other.displayPreview
        self.randomNext = other.randomNext
    # end copyAllSettingsFrom
    
    def getAsDict(self):
        dictObj = ImageSettings.getAsDict(self)
        dictObj[self.KEY_INTERVAL] = self.interval
        dictObj[self.KEY_DISPLAY_PREVIEW] = self.displayPreview
        dictObj[self.KEY_RANDOM_NEXT] = self.randomNext
        return dictObj
    # end getAsDict
    
    def loadFromDict(self, dictSet):
        ImageSettings.loadFromDict(self, dictSet)
        self.interval = dictSet[self.KEY_INTERVAL]
        self.displayPreview = dictSet[self.KEY_DISPLAY_PREVIEW]
        self.randomNext = dictSet[self.KEY_RANDOM_NEXT]
    # end loadFromDict
    
    