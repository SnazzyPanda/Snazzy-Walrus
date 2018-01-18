'''

@author: Snazzy Panda
'''
from snazzy.settings.ImageListSettings import ImageListSettings
from snazzy.objs.Image import Image
from snazzy.objs.ListParams import ListParams

class ImageList(list):
    '''
    classdocs
    '''

    KEY_ID = "key_id"
    KEY_NAME = "key_list_name"
    KEY_ACTIVE = "key_list_active"
    KEY_LIST_SETTINGS = "key_list_settings"
    KEY_LIST_CONTENTS = "key_list_contents"
    KEY_PARAM_LIST_PARAMS = "key_param_list_params"
    PLACEHOLDER_ID = -1

    def __init__(self, name = None):
        '''
        Constructor for ImageList
        '''
        list.__init__(self)
        self.settings = ImageListSettings()
        self.id = self.PLACEHOLDER_ID
        self.name = ""
        if name is not None:
            self.name = name
        self.active = False
        self.listOfListParams = []
    # end constructor

    def addParamList(self, parmList, duplicateAllowed = False):
        if(duplicateAllowed or (parmList not in self.listOfListParams)):
            self.listOfListParams.append(parmList)
        else:
            print("ParamList already in list!")
    # end addParamList
    
    def removeParamList(self, parmList):
        #TODO: test this!
        print("Removal of param list not tested!")
        print(str(parmList))
        self.listOfListParams.remove(parmList)
    # end removeParamList
    

    def getAsDict(self):
        outputDict = dict()
        outputDict[self.KEY_ID] = self.id
        outputDict[self.KEY_NAME] = self.name
        outputDict[self.KEY_ACTIVE] = self.active
        outputDict[self.KEY_LIST_SETTINGS] = self.settings.getAsDict()
        outputDict[self.KEY_LIST_CONTENTS] = []
        outputDict[self.KEY_PARAM_LIST_PARAMS] = []
        
        for img in self:
            outputDict[self.KEY_LIST_CONTENTS].append(img.getAsDict())
        
        for param in self.listOfListParams:
            outputDict[self.KEY_PARAM_LIST_PARAMS].append(param.getAsDict())
        
        return outputDict
    # end getAsDict

    def loadFromDict(self, inputDict):
        self.id = inputDict[self.KEY_ID]
        self.name = inputDict[self.KEY_NAME]
        self.active = inputDict[self.KEY_ACTIVE]
        self.settings = ImageListSettings()
        self.settings.loadFromDict(inputDict[self.KEY_LIST_SETTINGS])
        
        for img in inputDict[self.KEY_LIST_CONTENTS]:
            imgObj = Image()
            imgObj.loadFromDict(img)
            self.append(imgObj)
        
        for param in inputDict[self.KEY_PARAM_LIST_PARAMS]:
            parmList = ListParams()
            parmList.loadFromDict(param)
            self.listOfListParams.append(parmList)
        
    # end loadFromDict
    
    def loadAndOverwriteFromList(self, listToLoadFrom):
        self.clear()
        self.loadFromList(listToLoadFrom, False)
    # end loadAndOverwriteFromList
    
    def loadFromList(self, listToLoadFrom, allowDuplicates = False):
        '''
        quick n dirty conversion to load a list of stuff into this ImageList object
        '''
        for item in listToLoadFrom:
            if(allowDuplicates or (item not in self)):
                self.append(item)
        
    # end loadFromList

    def equals(self, other):
        '''
        Returns true if the id of the objects match
        '''
        return self.id is other.id
    # end equals

    def deepEquals(self, other):
        '''
        Returns true if id, name, and settings of both objects match
        '''
        return ((self.id is other.id) and (self.name is other.name)
                and (self.settings.hasSameSettingsAs(other.settings)))
    # end deepEquals
    
    def __eq__(self, other):
        return self.id == other.id
    # end __eq__
