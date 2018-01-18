'''

@author: Snazzy Panda
'''

import signal

class GracefulKiller:
    '''
    basic usage:
    with yourGracefulKillerInstance:
        threadOfConcern.start()
    '''
    #TODO: make this work for system shutdowns/logouts/etc
    def __enter__(self):
        signal.signal(signal.SIGINT, self.exitGracefully)
        signal.signal(signal.SIGTERM, self.exitGracefully)
        
        #signal.signal(signal.SIGALRM, self.exitGracefully)
        #signal.signal(signal.SIGHUP, self.signal.SIG_IGN)
    # end __enter__
    
    def __exit__(self, type, value, traceback):
        return
    # end __exit__
    
    
    def __init__(self, threadsToKill = None, additionalCleanup = None):
        '''
        threadsToKill should be a list of threads using an Event object, accessible from threadReference.event
        additionalCleanup should be a function that runs any needed cleanup (such as saving files, etc) you need to be sure is done
        '''
        # TODO: see if we need to store these, or use these
        self.origSigint = signal.getsignal(signal.SIGINT)
        self.origSigterm = signal.getsignal(signal.SIGTERM)
        
        self.threadsToKill = threadsToKill
        self.additionalCleanup = additionalCleanup
    # end constructor

    def exitGracefully(self, signum, frame):
        print("DEBUG: exiting gracefully I guess...")
        
        if(self.threadsToKill is not None):
            for threadToKill in self.threadsToKill:
                threadToKill.event.set()
            # end for each thread to kill
        # end if we have been given threads to kill
        
        if(self.additionalCleanup is not None):
            self.additionalCleanup()
        # end if we were given a function of additional cleanup
    # end exitGracefully

        
