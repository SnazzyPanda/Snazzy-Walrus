'''

@author: Snazzy Panda
'''
import os
import errno
from snazzy.helpers.IOHelper import IOHelper

class IOInitializer(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.ioHelper = IOHelper()
    # end constructor
    
    def initializeAllDirectories(self):
        self.initResDir()
        self.initWindowDir()
        self.initSaveDir()
        self.initPreviewDir()
        self.initConfigDir()
    # end initializeAllDirectories
    
    def initResDir(self):
        self.ioHelper.createDir(self.ioHelper.FULL_RESOURCE_PATH)
    # end initResDir
    
    def initSaveDir(self):
        self.ioHelper.createDir(self.ioHelper.FULL_SAVE_PATH)
    # end initSavePath
    
    def initPreviewDir(self):
        self.ioHelper.createDir(self.ioHelper.FULL_PREVIEW_PATH)
    # end initPreviewPath
    
    def initWindowDir(self):
        self.ioHelper.createDir(self.ioHelper.FULL_WINDOW_UI_PATH)
    # end initWindowDir
    
    def initTmpDir(self):
        self.ioHelper.createDir(self.ioHelper.FULL_TMP_PATH)
    # end initTmpDir
    
    def initConfigDir(self):
        self.ioHelper.createDir(self.ioHelper.getConfigDir())
    # end initConfigDir
    
        
