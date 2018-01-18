'''

@author: Snazzy Panda
'''
from threading import Thread
from snazzy.helpers.IOHelper import IOHelper

class SavingService(Thread):
    '''
    example use:
    ss = SavingService()
    ss.fullPath = "output.txt"
    ss.output = "This is my output!"
    ss.start()
    '''
    
    PATH_SEPARATOR = IOHelper.PATH_SEPARATOR

    def __init__(self, fullPath = None, output = ""):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.fullPath = fullPath
        self.output = output
    # end constructor
    
    def run(self):
        if(not self.fullPath.strip()):
            print("[WARN] invalid file: " + self.fullPath + " || stripped: " + self.fullPath.strip())
            return
        
        helper = IOHelper()
        # output has path and filename, so grab filename
        filename = helper.getFileFromPath(self.fullPath)
        
        # get the directory without a file on the end...
        filedir = helper.getDirFromFilePath(self.fullPath)
        # write out the file
        helper.writeFileWithPath(filedir, filename, self.output)
    # end run
    
    
    
