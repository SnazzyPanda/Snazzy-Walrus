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
import winreg

from snazzy.image.ImageManipulator import ImageManipulator
from snazzy.helpers.IOHelper import IOHelper
from snazzy.io.IOInitializer import IOInitializer

class WallpaperHelperWin(object):
    
    SPI_SETDESKWALLPAPER = 20
    STYLE_REG_KEY_MAIN = winreg.HKEY_CURRENT_USER
    STYLE_REG_KEY_PATH = 'Control Panel\\Desktop'
    STYLE_REG_KEY_ID = 'WallpaperStyle'

    STYLE_REG_KEY_TYPE = winreg.REG_SZ

    STYLE_REG_KEY_CENTER = 0
    STYLE_REG_KEY_STRETCH = 2
    STYLE_REG_KEY_FIT = 6
    STYLE_REG_KEY_FILL = 10
    STYLE_REG_KEY_SPAN = 22
    VALID_STYLE_REG_VALUES = [0, 2, 6, 10, 22]

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
    
    def updateRegistryVal(self, stretch = True):
        # read the registry value to check if it even needs to be changed
        readOnlyKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.STYLE_REG_KEY_PATH, 0, winreg.KEY_READ)
        # get the values of the registry we want
        regValues = winreg.QueryValueEx(readOnlyKey, self.STYLE_REG_KEY_ID)
        # close this key, not needed anymore
        winreg.CloseKey(readOnlyKey)
        # put value in new var
        currentVal = regValues[0]
        #currentType = regValues[1]

        # start newVal at None
        newVal = None

        # if the preferred wallpaper type does not match the current type, update the newVal to the type we want
        if(stretch and str(currentVal) != str(self.STYLE_REG_KEY_STRETCH)):
            # if we do want stretched
            newVal = self.STYLE_REG_KEY_STRETCH
        elif(not stretch and (str(currentVal) != str(self.STYLE_REG_KEY_FIT))):
            # if we do not want stretch, we probabaly want fit
            newVal = self.STYLE_REG_KEY_FIT
        # end if/else values do not match

        # if we need to update the registry, and the new value is a valid value for the registry item
        if(newVal is not None and newVal in self.VALID_STYLE_REG_VALUES):
            # convert value to string to ensure it is the correct data type
            newVal = str(newVal)
            print("[DEBUG] Changing registry value to modify background type!")
            # open a writable key to the registry entry
            writeKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.STYLE_REG_KEY_PATH, 0, winreg.KEY_WRITE)
            # update the registry entry
            winreg.SetValueEx(writeKey, self.STYLE_REG_KEY_ID, 0, self.STYLE_REG_KEY_TYPE, newVal)
            # close the key
            winreg.CloseKey(writeKey)
        # end if registry needs updated
    #end updateRegistryVal

    def changeWallpaper(self, absPath, stretch = True):
        
        tFileCreated = False

        # NOTE: if 32-bit, ONLY accepts .bmp!!
        # 64-bit seems to accept .bmp and .jpg, but not .png (more it doesn't like to come?)
        
        if self.isIncorrectType(absPath) and self.iohelper.pathExists(absPath):
            #create tmp jpg to use
            absPath = self.iohelper.getAbsPath(self.genTempImage(absPath))
            tFileCreated = True
        
        # try to update the registry as needed for optimal display based on if we were told to use stretch or not
        self.updateRegistryVal(stretch)

        # Update the background to the new image. I don't even really know what is going on here, but it works
        status = self.autoGetSysParamInfo()(self.SPI_SETDESKWALLPAPER, 0, absPath, 3)
        
        # if we needed to create a temporary file (because Windows is retarded apparently), cleanup that image (aka delete it)
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
    
