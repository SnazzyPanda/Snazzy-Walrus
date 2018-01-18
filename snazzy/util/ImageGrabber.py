'''

@author: Snazzy Panda
'''

'''

Should handle crawling folders/possible creation of custom Image object
for crawling:
    should handle crawl folder x, skip folders named y, search ONLY in folders named z
    get ONLY images meeting specific requirements (this would be slow -> load each image and examine its dimensions)
may want to support threading -> each thread builds its list (announces to a parent that it is scanning folder?)
    returns list when finished
    for now, will not do this...
'''

import os
from snazzy.helpers.IOHelper import IOHelper
from snazzy.objs.Image import Image

class ImageGrabber(object):
    
    def __init__(self):
        '''
        Constructor
        '''
        self.iohelper = IOHelper()
    # end constructor
    
    def metaScan(self, scanDir, subDirs = True, restrictDirs = [], excludeDirs = [], restrict = None):
        '''
        
        '''
        
        # get initial information for scan, probably only needed for threading (give threads subfolders, etc)
        print("metascan: " + scanDir + " | " + str(subDirs) + " | " + str(restrictDirs) + " | " + str(excludeDirs) + " | " + str(restrict))
        # if subdirs is false, return number of entries? otherwise the scandDir
        if not subDirs:
            return scanDir
        # for each valid folder, get list of folders that need scanned
    # end metaScan
    
    def grabImages(self, imageList = []):
        # TODO: take list of folders and grab images within?
        for img in imageList:
            print(img)
        # end for each image
    # end grabImages
    
    def getImagesFromDir(self, inpath):
        print(inpath) #TODO: get list of files in dir and try to make sure they are images or have file extension or whatever
        
        return self.iohelper.getValidImagesInPath(inpath)
    # end getImagesFromDir
    
    def genListImages(self, imglist = []):
        imageList = []
        
        for item in imglist:
            if(type(item) is list):
                for img in item:
                    if os.path.exists(img) and os.path.isfile(img):
                        imageList += [Image(img)]
            else:
                if os.path.exists(item) and os.path.isfile(item):
                    imageList += [Image(item)]
            # end if
        # end for
        return imageList
    # end genListImages
    
# end class
