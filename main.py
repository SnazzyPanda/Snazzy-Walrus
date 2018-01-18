'''

A command line version of the program.
For the near future, this will likely have more support due to the more immediate usability of it.

NOTE: For windows systems (specifically Windows 7, but most likely others as well), requires python 3.6 to not crash when outputting to console.

Program requires the following packages:
pillow
pygobject (for pygtk) gi?
pygtk

@author: Snazzy Panda
'''
import argparse
import os
import sys

#import time
#import random
#from PIL import Image
#import json

#from snazzy.ui.window import MainWindow
#from snazzy.settings.ImageSettings import ImageSettings
#from snazzy.settings.ImageListSettings import ImageListSettings
#from snazzy.settings.GlobalSettings import GlobalSettings
#from snazzy.image.ImageManipulator import ImageManipulator
#from snazzy.helpers.OSHelper import OSHelper
#from snazzy.ui.FileChooser import FileChooser


from snazzy.io.IOInitializer import IOInitializer
from snazzy.helpers.IOHelper import IOHelper
from snazzy.io.SavingService import SavingService
from snazzy.scheduler.GracefulKiller import GracefulKiller
from snazzy.scheduler.ScheduleReceiver import ScheduleReceiver
from snazzy.scheduler.SchedulerService import SchedulerService

from snazzy.util.ImageGrabber import ImageGrabber

from snazzy.objs.ImageList import ImageList
from snazzy.objs.ActiveList import ActiveList
from snazzy.objs.ListParams import ListParams









# Functions
def getActiveConfig():
    activeList = ActiveList()
    activeList.loadFromConfigFile()
    return activeList

def getListFromActiveConfig():
    activeList = getActiveConfig()
    # Put into this var so I can leave later setting activeList.listPath to it
    usedListPath = str(activeList.listPath)
    rawFile = iohelper.loadFileContents(usedListPath)
    
    if(rawFile is None):
        print("[WARN] Issue with active config!")
        return None
    else:
        return rawFile
# end getListFromActiveConfig
    
def getWorkingLists():
    #TODO: what is this? (probably remove)
    pass
# end getWorkingLists

def updateWallpaperList(foldersToDrawFrom, userSelectedExcludes, userSelectedIncludes, overwrite = False, allowDuplicates = False):
    
    #TODO: (not related to function) list the listparams (in specific order, and allow deletion of params from a list)
    #TODO: test adding single image file, test adding to multiple files, ????
    #TODO: try to simplify this? (what the fuck have I just written? I literally have no fucking clue and I wrote it like 30min ago...)
    #TODO: debug why having overwrite = True prevents updatin lists properly (main.py -u -o results in no scanning + updating...)

    # IOHelper for path/file processing
    iohelper = IOHelper()
    # ImageGrabber for logic specific to our handling of images
    igrab = ImageGrabber()
    # will be filled with Image objects for our ImageList (generated from given inputs)
    ilststuff = []
    
    # will be filled with valid directories that we are working with
    listOfDirsToGrabImagesFrom = []
    listParams = None
    
    listsToUpdate = userSelectedLists
    
    # if we were not supplied a file to update
    if(len(listsToUpdate) == 0):
        # use the list in the activeconfig file
        activeList = getActiveConfig()
        listsToUpdate = activeList.listPath
    # end if no list supplied
    if(listsToUpdate is not None and type(listsToUpdate) is not list):
        listsToUpdate = [listsToUpdate]
    
    newListOfImages = []
    # if user supplied folder to get images from (so we need to create new ListParams)
    if foldersToDrawFrom:
        # create a new ListParams based on user input, and grab all images found from it
        listParams = ListParams(foldersToDrawFrom, userSelectedExcludes, userSelectedIncludes)
        
        # get valid directories
        for userList in listParams.startingPath:
            listOfDirsToGrabImagesFrom += iohelper.getDeepDirsInPath(userList, listParams.excludes, listParams.includeOnly)
        
        #get all images in those directories
        for diritem in listOfDirsToGrabImagesFrom:
            # currently, the same as: iohelper.getValidImagesInPath(inpath)
            ilststuff += [igrab.getImagesFromDir(diritem)]
        # create a list of Image objects from those images
        print()
        tmpcount = sum(p == [] for p in ilststuff)
        #print(str(ilststuff))
        print()
        print("[DEBUG] " + str(tmpcount))
        print("[DEBUG] " + str(len(ilststuff)))
        print()
        #TODO: fix ilststuff getting duplicate images
        newListOfImages = igrab.genListImages(ilststuff)
    # end user supplied folders
    

    print("[DEBUG]: New list contains " + str(len(newListOfImages)) + " images.")
    
    for wallList in listsToUpdate:
        additionalImages = []
        #TODO: allow updating List name?
        imgList = ImageList('Names Not Supported Yet!')
        # if file already exists
        if(os.path.isfile(os.path.abspath(wallList))):
            #load from the file
            rawFile = iohelper.loadFileContents(wallList)
            imgList.loadFromDict(iohelper.loadJSONAsDict(rawFile))
            listParmLists = imgList.listOfListParams
            # update using other paramters used to build this list
            for parms in listParmLists:
                # if we are overwriting or the list is already one of the paramlists (and thus already handled)
                if(overwrite or (listParams is not None and parms is listParams)):
                    if(parms is None or parms is ListParams()):
                        # if parms is None or an empty ListParams object, remove it from the ImageList
                        imgList.removeParamList(parms)
                    continue
                else:
                    imgPathList = []
                    for userList in parms.startingPath:
                        listOfDirsToGrabImagesFrom += iohelper.getDeepDirsInPath(userList, parms.excludes, parms.includeOnly)
                    # end for each startinPath in parms
                    for diritem in listOfDirsToGrabImagesFrom:
                        # currently, the same as: iohelper.getValidImagesInPath(inpath)
                        imgPathList += igrab.getImagesFromDir(diritem)
                    # end foreach dir in the dirlist
                    
                    # Create list of Images
                    additionalImages += igrab.genListImages(imgPathList)
                # end else handle saved parms
            # end for each ListParams in this ImageList's list of ListParams
        # end if the given file already exists on disk
        
        #TODO: append using list (with allow duplicates option)
        #print("Need to add ability to append to list, with an allow duplicates option!")
        combinedList = []
        combinedList = additionalImages + newListOfImages
        print("[DEBUG] " + str(len(combinedList)) + " " + str(len(additionalImages)) + " " + str(len(newListOfImages)))
        print()
        print("[DEBUG] Prev list length: " + str(len(imgList)))
        # if we are overwriting, clear the list first
        if(overwrite):
            imgList.loadAndOverwriteFromList(combinedList)
        else:
            imgList.loadFromList(combinedList, allowDuplicates)
        
        print("[DEBUG] New list length: " + str(len(imgList)))
        print()

        if(listParams is not None):
            if(overwrite):
                imgList.listOfListParams = [listParams]
            else:
                imgList.addParamList(listParams)
        
        # Save this ImageList to given file
        ss = SavingService()
        ss.fullPath = iohelper.getAbsPath(wallList)
        ss.output = iohelper.getAsJSONDump(imgList.getAsDict())
        ss.start()
    # end for each list to update
# end if user wants to update a list






















if __name__ == '__main__':
    ioInit = IOInitializer()
    ioInit.initializeAllDirectories()
    
    iohelper = IOHelper()
    
    DEFAULT_INTERVAL = 300 # set default interval to 5 minutes
    
    #TODO: consider re-loading wallpaper save every switch
    # Pros: 
    # - This results in lower constant memory usage
    # - Allows "hot" updating of wallpapers
    # Cons:
    # - Higher CPU usage when changing wallpapers (have to re-process list)
    # - More disk reads (negligable)
    # - Larger delay before changing wallpaper (due to additional processing; may not be a big deal)

    # TODO: save list creation details within list?
    # Why?: This would allow simple -u for runnin all updates for list
    
    #TODO: test above functionality (should be mostly there)
    #TODO: enable sequential rotation?
    
    '''
    args I want:
    -h, --help
    
    -l, --list
    -a, --append
    -d, --delete
    
    -e, --exclude
    -i, --include-only
    
    -f, --folder
    
    
    add these:
    -v, --view
    -s, --simulate
    
    -w, --wallchange (run)
    -n, --next (next-wall)
    
    NOTE: may be very useful to allow loading folder and exclude lists from file?
    '''
    #TODO: make use of capital letters (-D for delete?)
    
    #TODO: find a way to edit settings of a list?
    
    parser = argparse.ArgumentParser(description='Add things')
    
    
    parser.add_argument('-l', '--list', action='append', nargs='*', default=[[]], help='Specify a list to work with(either full path or known lists only?)')
    
    parser.add_argument('-f', '--folder', action='append', nargs='*', help='Specify directory names to add images from. Can additionally specify -r/--recursive -e/--exclude -i/--include-only for more control')
    
    parser.add_argument('-r', '--recursive', action='store_true', help='[not needed as default action? - may still be helpful as an overwrite settings]NOT IMPLEMENTED Specify if specified input folders should be searched recurseively')
    
    parser.add_argument('-e', '--exclude', action='append', nargs='*', default=[[]], help='Specify directory names to exclude from adding to a list')
    
    parser.add_argument('-i', '--include-only', action='append', nargs='*', default=[[]], help='Specify the names of directories to include in a list, any directory (or its subdirectory) that is not specified will be ignored.')
    
    parser.add_argument('-o', '--overwrite', action='store_true', help='Specify to overwrite selected lists, rather than the default append.')
    
    parser.add_argument('--interval', action='store', default=None, help='Specify an override interval for the --wallchange option.')
    
    parser.add_argument('-D', '--delete', action='store_true', help='NOT IMPLEMENTED Specify to be prompted to delete selected lists')
    
    # TODO: make this an implied action? -> better shorthand the -w and --wallchange?
    parser.add_argument('-w', '--wallchange', action='store_true', help='Specify to be prompted to delete selected lists')
    
    parser.add_argument('-s', '--simulate', action='store_true', help='NOT IMPLEMENTED Specify to be prompted to delete selected lists')
    parser.add_argument('-n', '--next', action='store_true', help='Rotate wallpaper using selected list')
    parser.add_argument('--sequential', action='store_true', help='NOT IMPLEMENTED If list/rotation should be done sequentially')
    parser.add_argument('-v', '--view', action='store_true', help='NOT IMPLEMENTED Inspect contents of a saved list maybe?')
    
    parser.add_argument('-u', '--update', action='store_true', help='PARTIALLY IMPLEMENTED Updates (creates if it does not exist) a list using given inputs...I hope')
    
    parser.add_argument('--set-config', action='store_true', help='[Currently] Update the active config file with a list path so that it may be used implicitly by commands such as -n and -w. (Must specify list with -l)')
    parser.add_argument('--set-interval', action='store_true', help='[Currently] Update the active config file with a new interval so that active scheduler can be updated to use it. (must specify --interval as well)')
    parser.add_argument('--fix-config', action='store_true', help='[Currently] Should fix inconsistencies between a local config file and the expected format.')
    #TODO: find a way to be able to stop a running script immediately
    parser.add_argument('-T', '--terminate', '--stop', action="store_true", help='Try to stop rotation via the active config file. Due to the way this is set up, active script will not terminate until the next interval.')
    
    # -a = --append, -o = --overwrite (list name should likely be implied?)
    # 
    
    
    thelists = parser.parse_args()
    
    print(str(thelists) + "\n")
    
    doesUserWantToDelete = thelists.delete
    doesUserWantToView = thelists.view
    doesUserWantToWallpaper = thelists.wallchange
    doesUserWantNextWall = thelists.next
    doesuserWantSequential = thelists.sequential
    doesUserWantSimulate = thelists.simulate
    doesUserWantOverwrite = thelists.overwrite
    
    doesUserWantUpdateConfigList = thelists.set_config
    doesUserWantUpdateInterval = thelists.set_interval

    tryToFixConfigFile = thelists.fix_config
    doesUserWantTerminate = thelists.terminate
    
    doesUserWantUpdate = thelists.update
    
    userSpecifiedInterval = None
    if(thelists.interval is not None):
        userSpecifiedInterval = int(thelists.interval)
        if(userSpecifiedInterval < 10 and doesUserWantToWallpaper):
            userSpecifiedInterval = DEFAULT_INTERVAL
            print("[WARN] Invalid or no interval provided, defaulting to " + str(DEFAULT_INTERVAL) + " seconds. (Found: " + str(int(thelists.interval)) + ")")
    
    # this should be always result in a list, so loop over it to get to each specified item
    userSelectedLists = thelists.list
    if(userSelectedLists is None):
        userSelectedLists = []
    # should flatten the list of lists
    tmpList = [item for sublist in userSelectedLists for item in sublist]
    # shoudl remove all empty lists from the list
    userSelectedLists = [x for x in tmpList if x != []]
    
    print(str(userSelectedLists))
    
    #print(str(thelists.list[0]))
    foldersToDrawFrom = thelists.folder
    if(foldersToDrawFrom is None):
        foldersToDrawFrom = []
    # should flatten the list of lists
    tmpList = [item for sublist in foldersToDrawFrom for item in sublist]
    # shoudl remove all empty lists from the list
    foldersToDrawFrom = [x for x in tmpList if x != []]
    
    userSelectedExcludes = thelists.exclude
    if(userSelectedExcludes is None):
        userSelectedExcludes = []
    # should flatten the list of lists
    tmpList = [item for sublist in userSelectedExcludes for item in sublist]
    # shoudl remove all empty lists from the list
    userSelectedExcludes = [x for x in tmpList if x != []]
    
    userSelectedIncludes = thelists.include_only
    if(userSelectedIncludes is None):
        userSelectedIncludes = []
    # should flatten the list of lists
    tmpList = [item for sublist in userSelectedIncludes for item in sublist]
    # shoudl remove all empty lists from the list
    userSelectedIncludes = [x for x in tmpList if x != []]
    
    
    
    # START ACTUALLY HANDLING THINGS HERE!
    
    #TODO: check user lists here, if no valid try active config (otherwise None)
    '''
    listsToWorkWith = userSelectedLists
    
    # if we were not supplied a file to update
    if(len(listsToWorkWith) == 0):
        # use the list in the activeconfig file
        activeList = getActiveConfig()
        listsToWorkWith = activeList.listPath
    else:
        singleSelectedList = None
        for givenList in userSelectedLists:
            if(os.path.isfile(str(iohelper.getAbsPath(str(givenList))))):
                singleSelectedList = str(iohelper.getAbsPath(str(givenList)))
                break
            # end if given list is actually a file
        # end for each given list
        if(singleSelectedList is None):
            activeList = getActiveConfig()
            listsToWorkWith = activeList.listPath
        else:
            listsToWorkWith = singleSelectedList
    # end if no list supplied
    '''

    
    
    #TODO: move functionality to a function
    if(doesUserWantTerminate):
        localList = ActiveList()
        if(localList.isConfigFilePresent()):
            localList.loadFromConfigFile()
            localList.active = False
        # end there is config file already present
        
        # save the new config to file
        ss = SavingService(localList.iohelper.getAbsPath(localList.getConfigFilePath()), localList.getAsJSONDump())
        ss.start()
    # end if user wants to terminate rotation
    
    #TODO: verify that user is sure they want to do this...
    #TODO: verify that lists exist and are what we would consider valid lists
    #TODO: add soemthing like "isValidImageListThing"
    if(doesUserWantToDelete):
        for listToDelete in userSelectedLists:
            userDecision = input("Are you sure you want to delete " + listToDelete + "? This action cannot be undone! (y/N)")
            if(userDecision.toLower().startsWith('y')):
                print("[DEBUG] Would delete: " + str(listToDelete))
            #print("Would delete: " + str(listToDelete))
        # end for
        # Do no other action since we are deleting
        sys.exit()
    # end if doesUserWantToDelete
    
    if(tryToFixConfigFile):
        activeList = ActiveList()
        activeList.loadFixConfig()
        ss = SavingService(activeList.iohelper.getAbsPath(activeList.getConfigFilePath()), activeList.getAsJSONDump())
        ss.start()
    # end if tryToFixConfigFile

    #TODO: handle appends/overwrites as appropriate (CURRENTLY: append should be implied, overwrite should be implemented)
    # I think above TODO have been taken care of?
    if(doesUserWantUpdate):
        #TODO: allow user to specify that they want to allow duplicate images in a list (may be handy to have this on a ParamList level?)
        updateWallpaperList(foldersToDrawFrom, userSelectedExcludes, userSelectedIncludes, doesUserWantOverwrite)
    # end if user wants to update a list
    
    if(doesUserWantUpdateConfigList):
        
        chosenList = None
        for givenList in userSelectedLists:
            if(os.path.isfile(str(iohelper.getAbsPath(str(givenList))))):
                chosenList = str(iohelper.getAbsPath(str(givenList)))
                break
            # end if given list is actually a file
        # end for each givenlist
        
        if(chosenList is not None):
            activeList = ActiveList(chosenList)
            localList = ActiveList()
            if(localList.isConfigFilePresent()):
                localList.loadFromConfigFile()
                activeList.updateConfigFromConfig(localList)
            # end there is config file already present
            
            # save the new config to file
            ss = SavingService(activeList.iohelper.getAbsPath(activeList.getConfigFilePath()), activeList.getAsJSONDump())
            ss.start()
        # end if we have a chosenList
    # end if doesUserWantUpdateConfigList
    


    if(doesUserWantUpdateInterval):
        
        chosenList = None
        #for givenList in userSelectedLists:
        #    if(os.path.isfile(str(iohelper.getAbsPath(str(givenList))))):
        #        chosenList = str(iohelper.getAbsPath(str(givenList)))
        #        break
            # end if given list is actually a file
        # end for each givenlist
        
        activeList = ActiveList()
        if(activeList.isConfigFilePresent()):
            activeList.loadFromConfigFile()
            #activeList.updateConfigFromConfig(localList)


        if(userSpecifiedInterval is not None):
            activeList.interval = userSpecifiedInterval
            print("[DEBUG]: Interval updating to: " + str(userSpecifiedInterval))
        #if(chosenList is not None):
        #    activeList = ActiveList(chosenList)
        #    localList = ActiveList()
        #    if(localList.isConfigFilePresent()):
        #        localList.loadFromConfigFile()
        #        activeList.updateConfigFromConfig(localList)
            # end there is config file already present
            
        # save the new config to file
        ss = SavingService(activeList.iohelper.getAbsPath(activeList.getConfigFilePath()), activeList.getAsJSONDump())
        ss.start()
        # end if we have a chosenList
    # end if doesUserWantUpdateInterval



    # if user wants to change wallpapers (either through changer or just for next)
    if(doesUserWantToWallpaper or doesUserWantNextWall):
        iohelper = IOHelper()
        rawFile = None
        usedListPath = ''
        activeList = ActiveList()

        for givenList in userSelectedLists:
            # if givenList is a file
            if (os.path.isfile(str(givenList))):
                # try to load its contents into rawFile
                rawFile = iohelper.loadFileContents(str(givenList))
                usedListPath = str(givenList)
                #escape the for loop
                #TODO: see if theres any way to handle multiple list inputs?
                break
            # end if givenList
        # end for each given list
        
        # if no file was actually loaded
        if(rawFile is None):
            # try to load from active list
            activeList.loadFromConfigFile()
            # Put into this var so I can leave later setting activeList.listPath to it
            usedListPath = str(activeList.listPath)
            rawFile = iohelper.loadFileContents(usedListPath)
            
            # if no valid file loaded, and no valid file loaded from config
            if(rawFile is None):
                # exit with an error message
                sys.exit("Invalid list provided!")
        # end usable list was not provided
        
        newIList = ImageList()
        # try to load needed ddata from the rawFile contents
        # TODO: verify/sanity check this loading
        newIList.loadFromDict(iohelper.loadJSONAsDict(rawFile))
        
        print("[DEBUG] Loaded image objects. " + str(len(newIList)) + " images found.")
        
        # START DEBUG PARAM OUTPUT
        print("\n[DEBUG] paramlist:\n")
        tmpcount = 0
        for parm in newIList.listOfListParams:
            tmpdict = parm.getAsDict()
            print(str(tmpcount) + ": ")
            print("[DEBUG] folders: " + str(tmpdict[parm.KEY_START]))
            print("[DEBUG] includes" + str(tmpdict[parm.KEY_INCLUDE_ONLY]))
            print("[DEBUG] excludes: " + str(tmpdict[parm.KEY_EXCLUDES]))
            print("\n")
            tmpcount += 1
        
        # END DEBUG PARAM OUTPUT

        print("[DEBUG] Starting the scheduler")
        
        activeList.listPath = usedListPath
        
        newIList = None
        # if elseif block, since we only want 1 to apply, prefer next over full run!
        if(doesUserWantNextWall):
            sr = ScheduleReceiver(newIList, activeList, False)
            # setting 1 starts instantly, if you then specify interval it will apply to next switch...
            x = SchedulerService(1)
            # ensure we grab a default interval, just in case
            sr.DEFAULT_INTERVAL = x.DEFAULT_INTERVAL
            x.function = sr.handleTimerEvent
            print("\n")
            x.start()
            # we just wanted the next wallpaper, so stop
            x.stop()
        # end if doesUserWantNextWall
        elif(doesUserWantToWallpaper):
            if(userSpecifiedInterval is not None):
                activeList.interval = userSpecifiedInterval
            sr = ScheduleReceiver(newIList, activeList, True)
            # setting 1 starts instantly, if you then specify interval it will apply to next switch...
            x = SchedulerService(1)
            # ensure we grab a default interval, just in case
            sr.DEFAULT_INTERVAL = x.DEFAULT_INTERVAL
            # define an alternative method of grabbing interval, this method will handle reading the interval from file allowing interval to update mid schduler (after next interval is reached)
            x.getInterval = sr.grabInterval

            x.function = sr.handleTimerEvent
            print("\n")
            
            gracefulKiller = GracefulKiller([x], sr.unexpectedTerminationCleanup)
            with gracefulKiller:
                x.start()
                # we want to continue rotating, so properly set given interval
                #TODO: if none specified, use the settings!
                if(userSpecifiedInterval is not None):
                    x.interval = userSpecifiedInterval
            # end with gracefulKiller (attempt to gracefully handle interrupts such as ctrl+c)
        # end if doesUserWantToWallpaper
    # end if user wants to start wallpaper changer
        
    # end if

    
    #sys.exit()
    #pass
# end if __name__ == '__main__':



