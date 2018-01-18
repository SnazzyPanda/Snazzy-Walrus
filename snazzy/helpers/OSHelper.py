'''

@author: Snazzy Panda
'''
import os
import sys
from snazzy.helpers.IOHelper import IOHelper

class OSHelper(object):
    
    PLATFORM_LINUX = "linux"
    PLATFORM_WINDOWS = "win"
    #PLATFORM_LINUX2 = "linux2"
    #PLATFORM_WINDOWS = "win32"
    PLATFORM_OSX = "darwin"
    
    
    LINUX_ID = "linux"
    WINDOWS_ID = "windows"
    OSX_ID = "osx"
    
    UNKNOWN_ID = "unsupported"
    

    def __init__(self):
        '''
        Constructor
        '''

        self.platform = self.getPlatform()
        
        if not self.havePlatform():
            self.getPlatform()
        # end if
        
        # determine which platform we are on, and load and set the WallpaperHelper related to the platform
        if self.platform == self.WINDOWS_ID:
            from snazzy.helpers.windows.WallpaperHelperWin import WallpaperHelperWin
            self.wallhelper = WallpaperHelperWin()
        elif self.platform == self.LINUX_ID:
            from snazzy.helpers.linux.WallpaperHelperLinux import WallpaperHelperLinux
            self.wallhelper = WallpaperHelperLinux()
        elif self.platform == self.OSX_ID:
            from snazzy.helpers.osx.WallpaperHelperOSX import WallpaperHelperOSX
            self.wallhelper = WallpaperHelperOSX()
        else:
            print("No support " + self.platform)
            self.wallhelper = None
    # end constructor

    def getPlatform(self):
        platform = sys.platform

        if platform.startswith(self.PLATFORM_LINUX):
            # linux
            self.platform = self.LINUX_ID
        elif platform.startswith(self.PLATFORM_WINDOWS):
            # Windows...
            self.platform = self.WINDOWS_ID
        elif platform.startswith(self.PLATFORM_OSX):
            # OS X
            self.platform = self.OSX_ID
        else:
            print("unknown id: " + platform)
            self.platform = self.UNKNOWN_ID
    # end getPlatform
    
    def havePlatform(self):
        if self.platform is not None:
            return True
        else:
            return False
    # end havePlatform
    
    def setWallpaper(self, relPath):
        # if this is an unsupported platform, just leave since we cannot handle it
        if(self.platform is self.UNKNOWN_ID or self.wallhelper is None):
            print("platform not supported!")
            return
        
        absPath = IOHelper().getAbsPath(relPath)
        
        # change wallpaper with related wallpaper helper
        self.wallhelper.changeWallpaper(absPath)
    # end setWallpaper
