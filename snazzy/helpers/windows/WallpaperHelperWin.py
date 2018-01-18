'''

@author: Snazzy Panda
'''


'''
    import ctypes
    import os
    drive = "C:\\"
    folder = "images"
    image = "test.jpg"
    image_path = os.path.join(drive, folder, image)
    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path, 3)
'''
import ctypes
import struct

from snazzy.image.ImageManipulator import ImageManipulator
from snazzy.helpers.IOHelper import IOHelper
from snazzy.io.IOInitializer import IOInitializer

class WallpaperHelperWin(object):
    
    SPI_SETDESKWALLPAPER = 20
    IncorrectTypes = ('.png')
    TEMP_FILE_TYPE = ".bmp"
    
    def __init__(self):
        '''
        Constructor
        '''
        self.thing = self.SPI_SETDESKWALLPAPER
        self.iohelper = IOHelper()
    # end constructor
    
    def is64BitWin(self):
        """Find out how many bits is OS. """
        return struct.calcsize('P') * 8 == 64
    # end is64BitWin
    
    def autoGetSysParamInfo(self):
        if self.is64BitWin():
            return ctypes.windll.user32.SystemParametersInfoW
        else:
            return ctypes.windll.user32.SystemParametersInfoA
    #end 
    
    def changeWallpaper(self, absPath):
        
        tFileCreated = False
        
        # NOTE: if 32-bit, ONLY accepts .bmp!!
        # 64-bit seems to accept .bmp and .jpg, but not .png (more it doesn't like to come?)
        
        if self.isIncorrectType(absPath) and self.iohelper.pathExists(absPath):
            #create tmp jpg to use
            absPath = self.iohelper.getAbsPath(self.genTempImage(absPath))
            tFileCreated = True
            
        status = self.autoGetSysParamInfo()(self.SPI_SETDESKWALLPAPER, 0, absPath, 3)
        
        if tFileCreated:
            self.cleanTempImage()
        
        return status
    #end changeWallpaper
    
    def isIncorrectType(self, filename):
        return filename.endswith(self.IncorrectTypes)
    # end isIncorrectType
    
    def genTempImage(self, filepath):
        iman = ImageManipulator()

        img = iman.loadImage(filepath)
        tmpfile = self.iohelper.getConfigDir() + "tmp" + self.TEMP_FILE_TYPE
        iman.saveImage(img, tmpfile)
        return tmpfile
        
    # end genTempImage
    
    def cleanTempImage(self):
        tmpfile = self.iohelper.getConfigDir() + "tmp" + self.TEMP_FILE_TYPE
        #self.iohelper.removeFile(self.iohelper.getAbsPath(tmpfile))
    # end cleanTempImage
    
