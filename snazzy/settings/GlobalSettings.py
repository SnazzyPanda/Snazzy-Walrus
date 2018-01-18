'''

@author: Snazzy Panda
'''

from .ImageListSettings import ImageListSettings

class GlobalSettings(ImageListSettings):
    '''
    classdocs
    '''
    
    ''' ImageSettings '''
    # boolean
    DEFAULT_USE_RESIZE = True
    # boolean
    DEFAULT_RESIZE_HEIGHT = True
    # int amount to resize to
    DEFAULT_RESIZE_HEIGHT_AMT = 1920
    # boolean
    DEFAULT_RESIZE_WIDTH = False
    # int amount to resize to
    DEFAULT_RESIZE_WIDTH_AMT = 0 # TODO: find a number to use here!!!!!!!!!!!!!!!!!!
    # boolean
    DEFAULT_USE_CROP = True
    # boolean
    DEFAULT_CROP_HORIZONTAL_DIR = True
    # int identifier
    '''
    0 - random
    1 - center
    2 - right/top
    3 - left/bottom
    '''
    DEFAULT_CROP_POS = 0
    
    ''' ImageListSettings '''
    # int time in minutes?
    DEFAULT_INTERVAL = 5
    # boolean
    DEFAULT_DISPLAY_PREVIEW = True
    # boolean
    DEFAULT_RANDOM_NEXT = True
    
    
    ''' General Settings '''
    DEFAULT_THEME = 0 # TODO: implement themes?
    ''' Advanced Settings '''
    DEFAULT_FORCE_GLOBAL_SETTINGS = False
    DEFAULT_INCLUDE_SUBDIRS = False
    DEFAULT_ALLOW_DUPLICATES = False
    
    ''' KEYS '''
    KEY_THEME = "key_theme"
    KEY_FORCE_GLOBAL_SETTINGS = "key_force_default_settings"
    KEY_INCLUDE_SUBDIRS = "key_include_subdirs"
    KEY_ALLOW_DUPLICATES = "key_allow_duplicates"

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.theme = self.DEFAULT_THEME
        self.forceGlobalSettings = self.DEFAULT_FORCE_GLOBAL_SETTINGS
        self.includeSubdirs = self.DEFAULT_INCLUDE_SUBDIRS
        self.allowDuplicates = self.DEFAULT_ALLOW_DUPLICATES
    # end constructor
    
    def isThemeDefault(self):
        return self.theme is self.DEFAULT_THEME
    
    def isForceGlobalSettingsDefault(self):
        return self.forceGlobalSettings is self.DEFAULT_FORCE_GLOBAL_SETTINGS
    
    def isIncludeSubdirsDefault(self):
        return self.includeSubdirs is self.DEFAULT_INCLUDE_SUBDIRS
    
    def isAllowDuplicatesDefault(self):
        return self.allowDuplicates is self.DEFAULT_ALLOW_DUPLICATES
    
    def resetToDefaults(self):
        ImageListSettings.resetToDefaults(self)
        self.theme = self.DEFAULT_THEME
        self.forceGlobalSettings = self.DEFAULT_FORCE_GLOBAL_SETTINGS
        self.includeSubdirs = self.DEFAULT_INCLUDE_SUBDIRS
        self.allowDuplicates = self.DEFAULT_ALLOW_DUPLICATES
    # end resetToDefaults
    
    def isEdited(self):
        return (ImageListSettings.isEdited(self) or not self.isThemeDefault()
                or not self.isForceGlobalSettingsDefault() or self.isIncludeSubdirsDefault()
                or not self.isAllowDuplicatesDefault())
    # end isEdited
    
    def hasSameSettingsAs(self, other):
        return (ImageListSettings.hasSameSettingsAs(self, other) and (self.theme is other.theme)
                and (self.forceGlobalSettings is other.forceGlobalSettings) and (self.includeSubdirs is other.includeSubdirs)
                and (self.allowDuplicates is other.allowDuplicates))
    # end hasSameSettingsAs
    
    def copyAllSettingsFrom(self, other):
        ImageListSettings.copyAllSettingsFrom(self, other)
        self.theme = other.theme
        self.forceGlobalSettings = other.forceGlobalSettings
        self.includeSubdirs = other.includeSubdirs
        self.allowDuplicates = other.allowDuplicates
    # end copyAllSettingsFrom
    
    def getAsDict(self):
        dictSet = ImageListSettings.getAsDict(self)
        dictSet[self.KEY_THEME] = self.theme
        dictSet[self.KEY_FORCE_GLOBAL_SETTINGS] = self.forceGlobalSettings
        dictSet[self.KEY_INCLUDE_SUBDIRS] = self.includeSubdirs
        dictSet[self.KEY_ALLOW_DUPLICATES] = self.allowDuplicates
        return dictSet
    # end getAsDict
    
    def loadFromDict(self, dictSet):
        ImageListSettings.loadFromDict(self, dictSet)
        self.theme = dictSet[self.KEY_THEME]
        self.forceGlobalSettings = dictSet[self.KEY_FORCE_GLOBAL_SETTINGS]
        self.includeSubdirs = dictSet[self.KEY_INCLUDE_SUBDIRS]
        self.allowDuplicates = dictSet[self.KEY_ALLOW_DUPLICATES]
    # end loadFromDict
    
    