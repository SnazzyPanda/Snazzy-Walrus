'''

@author: Snazzy Panda
'''
from os import system

class WallpaperHelperOSX(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    def changeWallpaper(self, absPath):
        system(('osascript -e \'tell application "Finder" to set desktop picture to POSIX file "{0}"\''.format(absPath)))
    # end changeWallpaper
        
        