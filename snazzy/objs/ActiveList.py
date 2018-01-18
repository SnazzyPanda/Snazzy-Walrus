'''

@author: Snazzy Panda
'''

from snazzy.helpers.IOHelper import IOHelper

class ActiveList(object):
    
    #TODO: change this to not use json, but rather just lines in the file/user friendly format
    KEY_PATH = "list_path"
    KEY_INDEX = "last_index"
    KEY_ACTIVE = "active"
    KEY_INTERVAL = "scheduler_interval"
    
    def __init__(self, listPath = None, lastIndex = 0, active = None, interval = None):
        self.iohelper = IOHelper()
        self.configDirPath = self.iohelper.getConfigDir()
        
        self.listPath = listPath
        self.lastIndex = lastIndex
        self.active = active
        self.interval = interval
    # end constructor
    
    def clearConfig(self):
        self.iohelper.writeFileWithPath(self.configDirPath, self.iohelper.CONFIG_FILE_NAME, "")
    # end clearConfig
    
    def getConfigDir(self):
        return self.iohelper.getConfigDir()
    # end getConfigDir
    
    def getConfigFilePath(self):
        return self.iohelper.getConfigFilePath()
    # end getConfgiFilePath
    
    def isConfigFilePresent(self):
        cont = self.iohelper.loadFileContents(self.iohelper.getConfigFilePath())
        if(cont is None or cont.strip() is ''):
            return False
        else:
            return True
    # end isConfigFilePresent
    
    def getConfigFileContents(self):
        return self.iohelper.loadFileContents(self.iohelper.getConfigFilePath())
    # end getConfigFileContents
    
    def updateConfigFromConfig(self, activeConfig):
        #updates only variables that are None with non-none values passed in
        if(self.listPath is None and activeConfig.listPath is not None):
            self.listPath = activeConfig.listPath
        if(self.lastIndex is None and activeConfig.lastIndex is not None):
            self.lastIndex = activeConfig.lastIndex
        if(self.active is None and activeConfig.active is not None):
            self.active = activeConfig.active
        if(self.interval is None and activeConfig.interval is not None):
            self.interval = activeConfig.interval
    # end updateConfigFromConfig
    
    def updateConfig(self, listPath = None, lastIndex = None, active = None, interval = None):
        if(listPath is not None):
            self.listPath == listPath
        if(lastIndex is not None):
            self.lastIndex = lastIndex
        if(active is not None):
            self.active = active
        if(interval is not None):
            self.interval = interval
        #TODO: write to file?
    # end updateConfig
    
    def loadFromConfigFile(self):
        self.loadFromDict(self.iohelper.loadFromJSONFile(self.iohelper.getConfigFilePath()))
    # end loadFromConfigFile
    
    def loadSafeFromConfigFile(self):
        return self.iohelper.loadFromJSONFile(self.iohelper.getConfigFilePath())
    # end loadSafeFromConfigFile

    def loadFixConfig(self):
        self.loadConfigSafe(self.loadSafeFromConfigFile())
        #TODO: save out config?
    # end loadFixConfig

    def updateStopConfig(self, configuration = None):
        #TODO: if no configuration given, load existing
        cfg = ActiveList()
        cfg.loadFromDict(self.getConfigFileContents())
        cfg.active = False
        
    # end updateStopConfiguration
    
    def getAsDict(self):
        outputDict = dict()
        outputDict[self.KEY_PATH] = self.listPath
        outputDict[self.KEY_INDEX] = self.lastIndex
        outputDict[self.KEY_ACTIVE] = self.active
        outputDict[self.KEY_INTERVAL] = self.interval
        
        return outputDict
    # end getAsDict

    def loadFromDict(self, inputDict):
        self.listPath = inputDict[self.KEY_PATH]
        self.lastIndex = inputDict[self.KEY_INDEX]
        self.active = inputDict[self.KEY_ACTIVE]
        self.interval = inputDict[self.KEY_INTERVAL]
    # end loadFromDict

    def loadConfigSafe(self, inputDict):
        try:
            self.listPath = inputDict[self.KEY_PATH]
        except KeyError:
            pass
        try:
            self.lastIndex = inputDict[self.KEY_INDEX]
        except KeyError:
            pass
        try:
            self.active = inputDict[self.KEY_ACTIVE]
        except KeyError:
            pass
        try:
            self.interval = inputDict[self.KEY_INTERVAL]
        except KeyError:
            pass
    # end loadConfigSafe
    
    def getAsJSONDump(self):
        return self.iohelper.getAsJSONDump(self.getAsDict())
    # end getAsJSONDump
    

