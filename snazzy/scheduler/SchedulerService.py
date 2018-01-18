'''

@author: Snazzy Panda
'''

from threading import Thread, Event, Condition, Lock

class SchedulerService(Thread):
    '''
    classdocs
    
    A new object needs to be created when one is stopped, since it is a thread
    '''

    DEFAULT_INTERVAL_IN_MINUTES = 5
    SECONDS_PER_MINUTE = 60
    MILLISECONDS_PER_MINUTE = 1000 * SECONDS_PER_MINUTE # do not need milliseconds?
    
    DEFAULT_INTERVAL = DEFAULT_INTERVAL_IN_MINUTES * SECONDS_PER_MINUTE
    

    def __init__(self, interval = DEFAULT_INTERVAL, func = None, paused = False, getInterval = None):
        '''
        Constructor
        '''
        self.stopped = False
        self.function = self.handleEvent
        if(func is not None):
            self.function = func
        self.getInterval = self.grabInterval
        if(getInterval is not None):
            self.getInterval = getInterval
        self.interval = interval
        self.paused = paused
        self.pause_cond = Condition(Lock())
        self.event = Event()
        Thread.__init__(self)
    # end constructor
    
    def run(self):
        while not self.stopped:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                # end while paused
            # end with paused condition
            cont = self.function()
            if(not cont):
                break
            # wait for the specified interval before running again, unless the event is triggered, in which case we will terminate the thread
            # get updated interval, doing this inside the wait() causes issues!
            theinterval = self.getInterval()
            # delay action until the specified interval has passed
            interrupted = self.event.wait(theinterval)
            if(interrupted):
                self.stop()
                break
        # end while not stopped
        print("[DEBUG] out of thread loop")
    # end run
    
    def handleEvent(self):
        return
    # end handleEvent
    
    def forceEventImmediate(self):
        # This funciton is unused due to the way I made this program work...
        self.function()
    # end forceEventImmediate

    def grabInterval(self):
        return self.interval
    
    def pause(self):
        self.paused = True
        # If in sleep, we acquire immediately, otherwise we wait for thread
        # to release condition. In race, worker will still see self.paused
        # and begin waiting until it's set back to False
        self.pause_cond.acquire()
    # end pause
    
    def resume(self):
        self.paused = False
        # Notify so thread will wake after lock released
        self.pause_cond.notify()
        # Now release the lock
        self.pause_cond.release()
    # end resume
    
    def stop(self):
        print("DEBUG: stopping")
        self.stopped = True
    # end stop
    
    def reset(self):
        # does not work
        self = SchedulerService(self.interval, self.function)
    # end reset

        
