'''

@author: Snazzy Panda
'''
import os
from os.path import expanduser
import errno
import json

class IOHelper(object):
    '''
    classdocs
    '''

    PATH_SEPARATOR = os.sep
    
    DISTANCE_FROM_PROJECT_ROOT = 3
    
    RESOURCE_PATH = "res"
    WINDOW_UI_PATH = "windows"
    REL_WINDOW_UI_PATH = RESOURCE_PATH + PATH_SEPARATOR + WINDOW_UI_PATH

    USER_PATH = "user"
    PREVIEW_PATH = "previews"
    REL_PREVIEW_PATH = USER_PATH + PATH_SEPARATOR + PREVIEW_PATH
    SAVE_PATH = "saves"
    REL_SAVE_PATH = USER_PATH + PATH_SEPARATOR + SAVE_PATH
    TMP_PATH = "tmp"
    REL_TMP_PATH = USER_PATH + PATH_SEPARATOR + TMP_PATH
    
    CONFIG_DIR_NAME = ".snazzywalrus"
    CONFIG_FILE_NAME = "activeconfig"
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.FULL_RESOURCE_PATH = self.getBaseProjectPath() + self.PATH_SEPARATOR + self.RESOURCE_PATH
        self.FULL_WINDOW_UI_PATH = self.getBaseProjectPath() + self.PATH_SEPARATOR + self.REL_WINDOW_UI_PATH
        self.FULL_PREVIEW_PATH = self.getBaseProjectPath() + self.PATH_SEPARATOR + self.REL_PREVIEW_PATH
        self.FULL_SAVE_PATH = self.getBaseProjectPath() + self.PATH_SEPARATOR + self.REL_SAVE_PATH
        self.FULL_TMP_PATH = self.getBaseProjectPath() + self.PATH_SEPARATOR + self.REL_TMP_PATH
    # end constructor
    
    def getConfigDir(self):
        homepath = expanduser("~")
        configBasePath = homepath + self.PATH_SEPARATOR + self.CONFIG_DIR_NAME + self.PATH_SEPARATOR
        return configBasePath
    # end getConfigDir
    
    def getConfigFilePath(self):
        configBasePath = self.getConfigDir()
        configPath = configBasePath + self.CONFIG_FILE_NAME
        return configPath
    # end getConfgiFilePath
    
    def getBaseProjectPath(self):
        return self.getXthParentDirPath(__file__, self.DISTANCE_FROM_PROJECT_ROOT)
    # end getBaseProjectPath

    def getAbsPath(self, filePath):
        return os.path.abspath(filePath)
    # end getAbsPath
    
    def getDirFromFilePath(self, inputPath):
        inputPath = os.path.abspath(inputPath)
        pos = inputPath.rfind(os.sep)
        if(pos is -1):
            outPath = None
        else:
            outPath = inputPath[:pos]
        return outPath
    # end getDirFromFilePath
    
    def getFileFromPath(self, inputPath):
        inputPath = os.path.abspath(inputPath)
        n = inputPath
        n = n[(n.rfind(os.sep) + 1):]
        fileName = n
        return fileName
    # end getFileFromPath
    
    def getRawFilesInPath(self, inputPath):
        inputPath = os.path.abspath(inputPath)
        lst = os.listdir(inputPath)
        fileList = []
        for i in lst:
            i = os.path.join(inputPath, i)
            if os.path.isfile(i):
                fileList += [i]
            # end if
        # end for
        return fileList
    # end getRawFilesInPath
    
    def getFilesInPath(self, inputPath, extList = []):
        if extList is None:
            extList = []
        
        lst = self.getRawFilesInPath(inputPath)
        
        # if no extensions were provided
        if len(extList) == 0:
            return lst
        
        fileList = []
        
        for i in lst:
            if str(i).lower().endswith(tuple(extList)):
                fileList += [i]
            # end if
        # end for
        return fileList
    # end getFilesInPath
    
    def getValidImagesInPath(self, inputPath):
        from snazzy.settings.StaticConfig import StaticConfig
        setting = StaticConfig()
        return self.getFilesInPath(inputPath, setting.INPUT_EXTS)
    # end getValidImagesInPath
    
    def getRawDirsInPath(self, inputPath):
        inputPath = os.path.abspath(inputPath)
        lst = os.listdir(inputPath)
        dirList = []
        for i in lst:
            i = os.path.join(inputPath, i)
            if os.path.isdir(i):
                dirList += [i]
            # end if
        # end for
        return dirList
    # end getRawDirsFromPath
    
    def getDirsInPath(self, inputPath, excludeList = [], includeOnlyList = []):
        if excludeList is None:
            excludeList = []
        if includeOnlyList is None:
            includeOnlyList = []
        
        '''
        WARNING:
        currently exclude/include need to be absolute paths to work!!
        
        NEEDS TESTING
        '''
        
        tList = self.getRawDirsInPath(inputPath)
        
        if len(excludeList) == 0 and len(includeOnlyList) == 0:
            return tList
        # end if
        
        dirList = []
        
        for i in tList:
            
            # gets the last current dir as non absolute path
            cmp = self.getFileFromPath(i)
            
            if cmp in excludeList:
                continue
            if cmp in includeOnlyList:
                dirList += [i]
            elif len(includeOnlyList) == 0:
                dirList += [i]
        # end for
        return dirList
    # end getDirsInPath
    
    def getDeepDirsInPath(self, inputPath, excludeList = [], includeOnlyList = []):
        '''
        Probably inefficient but seems to work at excluding the desired files and including only the includeonly files
        '''
        if excludeList is None:
            excludeList = []
        if includeOnlyList is None:
            includeOnlyList = []
        
        lst = []
        
        for root, subdirs, tfiles in os.walk(inputPath):
            # gets the last current dir as non absolute path
            cmp = self.getFileFromPath(root)
            if cmp in excludeList:
                print("ignoring: " + cmp)
                continue
            
            #remove any excluded folders from dir list
            for thedir in subdirs:
                if thedir in excludeList:
                    fp = root + os.sep + thedir
                    print("ignoring2: " + thedir + " [" + fp + "]")
                    subdirs.remove(thedir)
            
            for thedir in subdirs:
                if thedir in excludeList:
                    fp = root + os.sep + thedir
                    print("ignoring: " + thedir + " [" + fp + "]")
                    subdirs.remove(thedir)
                    continue
                if thedir in includeOnlyList:
                    #apparently will not grab the root directory, probably need to change this?
                    lst += self.getDeepDirsInPath(root + os.sep + thedir, excludeList)
                    #as such, add the root directory...
                    lst += [root + os.sep + thedir]
                elif len(includeOnlyList) == 0:
                    lst += [root + os.sep + thedir]
                print("added: " + thedir)
        # end for
        
        # if rootdir not in lst, add to lst
        if inputPath not in lst:
            lst += [inputPath]
        # end if root path given was not added to list
        return lst
    # end getDeepDirsInPath
    
    def getParentDirPath(self, childPath):
        #print(__file__)
        return os.path.dirname(childPath)
    # end getParentDirPath
    
    def getXthParentDirPath(self, childPath, x = 1):
        # invalid path given, must be positive integer
        if(x < 1):
            return childPath
        curpath = childPath
        for i in range(0, x):
            curpath = self.getParentDirPath(curpath)
        # end for loop
        return curpath
    # end getXthParentDirPath
    
    def createDir(self, directory):
        try:
            os.makedirs(directory)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    # end createDir
    
    def writePathlessFile(self, fileName, outputData = ""):
        with open(fileName, "w") as file:
            file.write(outputData)
    # end writePathlessFile
    
    def writeFileWithPath(self, filePath, fileName, outputData = ""):
        self.createDir(filePath)
        with open(os.path.join(filePath, fileName), "w") as file:
            file.write(outputData)
    # end writeFileWithPath
    
    def removeFile(self, filename):
        print("deleting: " + filename)
        os.remove(filename)
    # end removeFile
    
    def removeDir(self, folder):
        print("deleting: " + folder)
        os.rmdir(folder)
    # end removeDir
    
    def loadFileContents(self, filepath):
        content = None
        try:
            with open(filepath, 'r') as content_file:
                content = content_file.read()
        except FileNotFoundError as exception:
            content = None

        return content
    # end loadFileContents
    
    def pathExists(self, filepath):
        return os.path.exists(filepath)
    # end pathExists

    def getAsJSONDump(self, stuffToDump):
        #TODO: allow specifying non-pretty output to reduce file size and ???
        return json.dumps(stuffToDump, indent=4)
    # end getAsJSONDump
    
    def loadJSONAsDict(self, jsonInput):
        return json.loads(jsonInput)
    # end loadJSONAsDict
    
    def loadFromJSONFile(self, filepath):
        # get the raw file contents
        rawContents = self.loadFileContents(str(filepath))
        # return the json as a dict
        return self.loadJSONAsDict(rawContents)
    # end loadFromJSONFile
    
