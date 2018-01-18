'''

Provides storage and manipulation of individual image's settings.

@author: Snazzy Panda
'''

class ImageSettings(object):
    '''
    classdocs
    '''
    # boolean
    DEFAULT_USE_RESIZE = None
    # boolean
    DEFAULT_RESIZE_HEIGHT = None
    # int amount to resize to
    DEFAULT_RESIZE_HEIGHT_AMT = None
    # boolean
    DEFAULT_RESIZE_WIDTH = None
    # int amount to resize to
    DEFAULT_RESIZE_WIDTH_AMT = None
    # boolean
    DEFAULT_USE_CROP = None
    # boolean
    DEFAULT_CROP_HORIZONTAL_DIR = None
    # int identifier
    DEFAULT_CROP_POS = None


    KEY_USE_RESIZE = "key_resize"
    KEY_RESIZE_HEIGHT = "key_resize_height"
    KEY_RESIZE_HEIGHT_AMT = "key_resize_height_amount"
    KEY_RESIZE_WIDTH = "key_resize_width"
    KEY_RESIZE_WIDTH_AMT = "key_resize_width_amt"
    KEY_USE_CROP = "key_use_crop"
    KEY_CROP_HORIZONTALLY = "key_crop_horizontally"
    KEY_CROP_POSITION = "key_crop_pos"


    def __init__(self):
        '''
        Constructor
        '''
        # initialize settings to defaults
        self.useResize = self.DEFAULT_USE_RESIZE
        self.resizeHeight = self.DEFAULT_RESIZE_HEIGHT
        self.resizeHeightAmount = self.DEFAULT_RESIZE_HEIGHT_AMT
        self.resizeWidth = self.DEFAULT_RESIZE_WIDTH
        self.resizeWidthAmount = self.DEFAULT_RESIZE_WIDTH_AMT
        self.useCrop = self.DEFAULT_USE_CROP
        self.cropHorizontally = self.DEFAULT_CROP_HORIZONTAL_DIR
        self.cropPosition = self.DEFAULT_CROP_POS
    # End constructor


    def isUseResizeDefault(self):
        return self.useResize is self.DEFAULT_USE_RESIZE

    def isResizeHeightDefault(self):
        return self.resizeHeight is self.DEFAULT_RESIZE_HEIGHT

    def isResizeHeightAmtDefault(self):
        return self.resizeHeightAmount is self.DEFAULT_RESIZE_HEIGHT_AMT

    def isResizeWidthDefault(self):
        return self.resizeWidth is self.DEFAULT_RESIZE_WIDTH

    def isResizeWidthAmtDefault(self):
        return self.resizeWidthAmount is self.DEFAULT_RESIZE_WIDTH_AMT

    def isUseCropDefault(self):
        return self.useCrop is self.DEFAULT_USE_CROP

    def isCropHorizontallyDefault(self):
        return self.cropHorizontally is self.DEFAULT_CROP_HORIZONTAL_DIR

    def isCropPositionDefault(self):
        return self.cropPosition is self.DEFAULT_CROP_POS

    def resetToDefaults(self):
        '''
        Resets the setting values to their default values (probably None)
        '''
        self.useResize = self.DEFAULT_USE_RESIZE
        self.resizeHeight = self.DEFAULT_RESIZE_HEIGHT
        self.resizeHeightAmount = self.DEFAULT_RESIZE_HEIGHT_AMT
        self.resizeWidth = self.DEFAULT_RESIZE_WIDTH
        self.resizeWidthAmount = self.DEFAULT_RESIZE_WIDTH_AMT
        self.useCrop = self.DEFAULT_USE_CROP
        self.cropHorizontally = self.DEFAULT_CROP_HORIZONTAL_DIR
        self.cropPosition = self.DEFAULT_CROP_POS
    # end resetToDefaults

    def isEdited(self):
        return (not self.isUseResizeDefault() or not self.isResizeHeightDefault()
                or not self.isResizeHeightAmtDefault() or not self.isResizeWidthDefault()
                or not self.isResizeWidthAmtDefault() or not self.isUseCropDefault()
                or not self.isCropHorizontallyDefault() or not self.isCropPositionDefault())
    # end isEdited

    def hasSameSettingsAs(self, other):
        '''
        (Should) Returns true if the settings of current object match the given object
        '''
        return ((self.useResize is other.useResize) and (self.resizeHeight is other.resizeHeight)
                and (self.resizeHeightAmount is other.resizeHeightAmount) and (self.resizeWidth is other.resizeWidth)
                and (self.resizeWidthAmount is other.resizeWidthAmount) and (self.useCrop is other.useCrop)
                and (self.cropHorizontally is other.cropHorizontally) and (self.cropPosition is other.cropPosition)
                )
    # end hasSameSettingsAs

    def copyAllSettingsFrom(self, other):
        self.useResize = other.useResize
        self.resizeHeight = other.resizeHeight
        self.resizeHeightAmount = other.resizeHeightAmount
        self.resizeWidth = other.resizeWidth
        self.resizeWidthAmount = other.resizeWidthAmount
        self.useCrop = other.useCrop
        self.cropHorizontally = other.cropHorizontally
        self.cropPosition = other.cropPosition
    # end copyAllSettingsFrom

    def getAsDict(self):
        dictSet = {
            self.KEY_USE_RESIZE: self.useResize,
            self.KEY_RESIZE_HEIGHT: self.resizeHeight,
            self.KEY_RESIZE_HEIGHT_AMT: self.resizeHeightAmount,
            self.KEY_RESIZE_WIDTH: self.resizeWidth,
            self.KEY_RESIZE_WIDTH_AMT: self.resizeWidthAmount,
            self.KEY_USE_CROP: self.useCrop,
            self.KEY_CROP_HORIZONTALLY: self.cropHorizontally,
            self.KEY_CROP_POSITION: self.cropPosition
        }
        return dictSet
    # end getAsdictSet

    def loadFromDict(self, dictSet):
        self.useResize = dictSet[self.KEY_USE_RESIZE]
        self.resizeHeight = dictSet[self.KEY_RESIZE_HEIGHT]
        self.resizeHeightAmount = dictSet[self.KEY_RESIZE_HEIGHT_AMT]
        self.resizeWidth = dictSet[self.KEY_RESIZE_WIDTH]
        self.resizeWidthAmount = dictSet[self.KEY_RESIZE_WIDTH_AMT]
        self.useCrop = dictSet[self.KEY_USE_CROP]
        self.cropHorizontally = dictSet[self.KEY_CROP_HORIZONTALLY]
        self.cropPosition = dictSet[self.KEY_CROP_POSITION]
    # end loadFromDict
