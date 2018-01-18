'''

@author: Snazzy Panda
'''

class StaticConfig(object):
    '''
    classdocs
    '''
    INPUT_MIME_TYPES = ["image/jpeg", "image/png", "image/bmp", "image/tiff"]
    
    INPUT_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    #INPUT_EXTS = ["*.webp"]
    
    WINDOW_MASTER_FILE = "SnazzyWalrus.glade"

    def __init__(self):
        '''
        Constructor
        '''
        
