'''

@author: Snazzy Panda
'''

import random

from snazzy.helpers.OSHelper import OSHelper
from snazzy.io.SavingService import SavingService
from snazzy.objs.ActiveList import ActiveList
from snazzy.objs.ImageList import ImageList

from snazzy.image.ImageManipulator import ImageManipulator

class ScheduleReceiver(object):
    '''
    classdocs
    '''
    DEFAULT_INTERVAL = 300 #but, we kinda grab it from scheduler service before starting it...
    
    def __init__(self, imagelist, activeList = None, markActive = False):
        '''
        Constructor
        '''
        #self.imagelist = None
        self.oshelper = OSHelper()
        self.markActive = markActive
        self.activeList = ActiveList('', 0)
        
        if(activeList is not None):
            self.activeList = activeList
        
        if(self.markActive):
            self.activeList.active = True
            
            localList = ActiveList()
            localList.loadFromConfigFile()
            # temporarily store the interval to make sure it gets applied
            tmpInterval = self.activeList.interval
            # Keep list path, active status, and last postion (if we are not overwriting them)
            self.activeList.updateConfigFromConfig(localList)
            self.activeList.interval = tmpInterval
            # Update the saved file
            ss = SavingService(self.activeList.iohelper.getAbsPath(self.activeList.getConfigFilePath()), self.activeList.getAsJSONDump())
            ss.start()
        # end if self.markActive
    # end constructor
    
    def checkConfigFileForChanges(self):
        localList = ActiveList()
        # if config file is not present, we are free to write one out...
        if(not localList.isConfigFilePresent()):
            ss = SavingService(self.activeList.iohelper.getAbsPath(self.activeList.getConfigFilePath()), self.activeList.getAsJSONDump())
            ss.start()
        else:
            localList.loadFromConfigFile()
            #Local file shows that rotation is active
            if(localList.active):
                # list is still active, continue doing normal operations
                self.activeList.updateConfigFromConfig(localList)
                # update the working list from config as well
                self.activeList.listPath = localList.listPath
                # update interval in case the config file has changed. Enabled changing config without stopping script
                self.activeList.interval = localList.interval
            elif(not self.markActive):
                #touch nothing, should be single, forced run through
                self.activeList.updateConfigFromConfig(localList)
            else:
                # it appears we want to stop rotating, so exit program completely...
                # TODO: more elegant way of stopping the scheduler service
                # return false, signifying that we should stop
                return False
        return True
    # end checkConfigFileForChanges
    
    def updateConfigFile(self, lastindex):
        self.activeList.lastIndex = lastindex
        # save the file in a thread blocking manner to prevent crashes (presumably due to not finishing file write)
        helper = self.activeList.iohelper
        fullPath = helper.getAbsPath(self.activeList.getConfigFilePath())
        # output has path and filename, so grab filename
        filename = helper.getFileFromPath(fullPath)
        
        # get the directory without a file on the end...
        filedir = helper.getDirFromFilePath(fullPath)
        # write out the file
        helper.writeFileWithPath(filedir, filename, self.activeList.getAsJSONDump())
    # end updateConfigFile
    
    
    def handleTimerEvent(self):
        #TODO: handle sequential rotation?
        continueEvent = self.checkConfigFileForChanges()
        if(not continueEvent):
            # tell service we will no longer process events
            return False
        
        # re-read image list from active config image list, allowing list to be updated without restarting scheduler
        rawFile = self.activeList.iohelper.loadFileContents(self.activeList.listPath)

        if(rawFile is None):
            # exit with an error message
            print("[ERROR] Invalid list provided!")
            return True
        
        imagelist = ImageList()
        # try to load needed ddata from the rawFile contents
        # TODO: verify/sanity check this loading
        imagelist.loadFromDict(self.activeList.iohelper.loadJSONAsDict(rawFile))

        # grab a random index of an item from the list (this way we would be able to save it as last known item, which is useful for sequential rotation)
        indexChosen = random.choice(list(enumerate(imagelist)))[0]
        #randimg = random.choice(self.imagelist)
        randimg = imagelist[indexChosen]
        print("\n[DEBUG] Using list: " + str(self.activeList.listPath))
        print("[DEBUG] " + str(indexChosen) + ": " + str(randimg.src))
        
        iman = ImageManipulator()
        img = iman.loadImage(randimg.src)
        landscape = iman.isImageLandscape(img)

        #change the wallpaper
        self.oshelper.setWallpaper(randimg.src, landscape)
        
        # update config file with latest index used
        self.updateConfigFile(indexChosen)
        # tell service we will continue processing events
        return True
    # end handleTimerEvent
    
    def grabInterval(self):
        localList = ActiveList()
        # if config file is not present, we are free to write one out...
        if(not localList.isConfigFilePresent()):
            ss = SavingService(self.activeList.iohelper.getAbsPath(self.activeList.getConfigFilePath()), self.activeList.getAsJSONDump())
            ss.start()
        else:
            localList.loadFromConfigFile()
            if(localList.interval is not None):
                self.activeList.interval = localList.interval
        return self.activeList.interval
    # end grabInterval


    def unexpectedTerminationCleanup(self):
        # update the config file, saying that the program is no longer actively running
        localList = ActiveList()
        localList.loadFromConfigFile()
        localList.active = False
        # save the updated config
        ss = SavingService(localList.iohelper.getAbsPath(localList.getConfigFilePath()), localList.getAsJSONDump())
        ss.start()
    # end unexpectedTerminationCleanup
    
    
    
    
