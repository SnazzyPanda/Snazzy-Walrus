'''

@author: Snazzy Panda
'''

#import commands

import os
import shlex

'''
    linux/window:
    https://stackoverflow.com/questions/1977694/change-desktop-background

    gnome desktop:
    import commands
    command = "gconftool-2 --set /desktop/gnome/background/picture_filename --type string '/path/to/file.jpg'"
    status, output = commands.getstatusoutput(command)  # status=0 if success
'''

class WallpaperHelperLinux(object):
    '''
    classdocs
    '''

    SCHEMA = 'org.gnome.desktop.background'
    KEY = 'picture-uri'
    ENVIRONMENT = 'DESKTOP_SESSION'

    ENV_GNOME = "gnome"
    ENV_UNITY = "unity"
    ENV_CINNAMON = "cinnamon"
    ENV_MATE = "mate"
    ENV_XFCE4 = "xfce4"
    ENV_LXDE = "lxde"
    ENV_LXQT = "lxqt"

    DEWarningShown = False

    def __init__(self):
        '''
        Constructor
        '''

        #self.environment = self.getEnvironment()
        self.environment = self.getDesktopEnv()

    # end constructor

    #def getEnvironment(self):
    #    env = os.environ.get(self.ENVIRONMENT)
    #    print(env)
    #    return env
    # end getEnvironment

    def getDesktopEnv(self):
        '''
        taken from:
        https://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
        '''
        desktop_session = os.environ.get(self.ENVIRONMENT).lower()

        if desktop_session == "default":
            # TODO: make sure this does not mess up other things!!!
            # fix for Zorin environment
            desktop_session = os.environ.get("XDG_CURRENT_DESKTOP").lower()

        if desktop_session is not None: #easier to match if we doesn't have  to deal with caracter cases
            desktop_session = desktop_session.lower()
            if desktop_session in ["gnome","unity", "cinnamon", "mate", "xfce4", "lxde", "fluxbox",
                                   "blackbox", "openbox", "icewm", "jwm", "afterstep","trinity", "kde"]:
                return desktop_session
            # For some, desktop_session will be something like: /usr/share/xsessions/YOUR-DESKTOP-SESSSION, these are to catch those cases
            elif "gnome" in desktop_session:
                return "gnome"
            elif "cinnamon" in desktop_session:
                return "cinnamon"
            elif "lxqt" in desktop_session:
                if(not self.DEWarningShown):
                    print("\nNOTICE: LXQT desktop environment detected, the method for changing wallpapers may take 2 minutes to apply! It may also interrupt menus and other UI interactions on update.\n")
                    self.DEWarningShown = True
                return "lxqt"
            ## Special cases ##
            # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
            # There is no guarantee that they will not do the same with the other desktop environments.
            elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                return "xfce4"
            elif desktop_session.startswith("ubuntu"):
                return self.ENV_UNITY
            elif "lxde" in desktop_session or desktop_session.startswith("lubuntu"):
                return "lxde"
            elif desktop_session.startswith("kubuntu"):
                return "kde"
            elif desktop_session.startswith("razor"): # e.g. razorkwin
                return "razor-qt"
            elif desktop_session.startswith("wmaker"): # e.g. wmaker-common
                return "windowmaker"
        if os.environ.get('KDE_FULL_SESSION') == 'true':
            if(not self.DEWarningShown):
                print("\nNOTICE: Currently, KDE environments, such as Plasma, are not supported since I cannot figure out a way to change wallpapers.\n")
                self.DEWarningShown = True
            return "kde"
        elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            if not "deprecated" in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                return "gnome2"
            print("Unhandled thing in WallpaperHelperLinux.py getDesktopEnv!: " + str(os.environ.get('GNOME_DESKTOP_SESSION_ID')))
        #From http://ubuntuforums.org/showthread.php?t=652320
        elif os.environ.get('XDG_CURRENT_DESKTOP').tolower().startswith('xfce'):
            return "xfce4"
        elif self.is_running("ksmserver"):
            return "kde"
    # end getDesktopEnv



    def changeWallpaper(self, absPath, stretch = True):
        if self.environment is None:
            self.environment = self.getDesktopEnv()
        #

        #TODO: create methods for each to handle changing wallpaper type (aka stretched, fit, etc)

        if self.environment == self.ENV_UNITY:
            self.changeWallpaperGNOME(absPath, stretch)
        elif self.environment == self.ENV_GNOME or self.environment == "gnome2":
            self.changeWallpaperGNOME(absPath, stretch)
        elif self.environment == self.ENV_CINNAMON:
            self.changeWallpaperCinnamon(absPath, stretch)
        elif self.environment == self.ENV_MATE:
            self.changeWallpaperMATE(absPath, stretch) #needs testing!
        elif self.environment == self.ENV_XFCE4:
            self.changeWallpaperXFCE4(absPath, stretch)
        elif self.environment == self.ENV_LXDE:
            self.changeWallpaperLXDE(absPath, stretch)
        elif self.environment == self.ENV_LXQT:
            self.changeWallpaperLXQT(absPath, stretch)
        else:
            print("unknown or unsupported linux environment: " + str(self.environment))
        # end if elif else

    # end changeWallpaper

    def changeWallpaperCinnamon(self, absPath, stretched = True):
        # From: https://unix.stackexchange.com/questions/59653/change-desktop-wallpaper-from-terminal
        if(stretched):
            os.system('gsettings set org.cinnamon.desktop.background picture-options "stretched"')
        else:
            os.system('gsettings set org.cinnamon.desktop.background picture-options "scaled"')
        os.system('gsettings set org.cinnamon.desktop.background picture-uri file://' + shlex.quote(absPath))
    #end changeWallpaperCinnamon

    def changeWallpaperGNOME(self, absPath, stretched = True):
        #command = "gconftool-2 --set /desktop/gnome/background/picture_filename --type string '" + absPath + "'"
        #command = "gconftool-2 --set /desktop/gnome/background/picture_filename --type string '" + absPath + "'"
        #status = commands.getstatusoutput(command)  # status=0 if success

        #os.system("gsettings set org.gnome.desktop.background picture-uri file:///home/user/Pictures/wallpaper/Stairslwallpaper.png")

        #alternate:
        if(stretched):
            os.system('gsettings set org.gnome.desktop.background picture-options "stretched"')
        else:
            os.system('gsettings set org.gnome.desktop.background picture-options "scaled"')
        os.system("gsettings set org.gnome.desktop.background picture-uri file://" + shlex.quote(absPath))
    # end changeWallpaperGNOME

    def changeWallpaperUnity(self, absPath):
        #from gi.repository import Gio
        #gsettings = Gio.Settings.new(self.SCHEMA)
        #gsettings.set_string(self.KEY, "file://" + shlex.quote(absPath))
    # end changeWallpaperUnity

    def changeWallpaperKDE4(self, absPath):
        # TODO: find some way to successfully change wallpapers in KDE (any and all versions I can test, preferrably)
        # attempt to change the wallpaper?
        #dbus-send --session --dest=org.new_wallpaper.Plasmoid --type=method_call /org/new_wallpaper/Plasmoid/0 org.new_wallpaper.Plasmoid.SetWallpaper string:/path/to/your/wallpaper
        os.system('dbus-send --session --dest=org.new_wallpaper.Plasmoid --type=method_call /org/new_wallpaper/Plasmoid/0 org.new_wallpaper.Plasmoid.SetWallpaper string:' + shlex.quote(absPath))

    # end changeWallpaperKDE4

    def changeWallpaperMATE(self, absPath, stretched = True):
        import subprocess
        #TODO: see if we can actually detect MATE version to avoid possible ugly output from failure?
        #from: https://stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python
        try: # MATE >= 1.6
            # info from http://wiki.mate-desktop.org/docs:gsettings
            if(stretched):
                args = ["gsettings", "set", "org.mate.background", "picture-options", "stretched"]
            else:
                args = ["gsettings", "set", "org.mate.background", "picture-options", "scaled"]
            subprocess.Popen(args)
            args = ["gsettings", "set", "org.mate.background", "picture-filename", "'%s'" % absPath]
            subprocess.Popen(args)
        except: # MATE < 1.6
            # From https://bugs.launchpad.net/variety/+bug/1033918
            args = ["mateconftool-2","-t","string","--set","/desktop/mate/background/picture_filename",'"%s"' % absPath]
            subprocess.Popen(args)
        # end try MATE1.6 or greater/catch otherwise
    # end changeWallpaperMATE

    def changeWallpaperXFCE4(self, absPath, stretched = True):
        import subprocess
        #from:
        imageStyle = "3" #stretched by default
        if(not stretched):
            imageStyle = "4" #scaled
        # end if not stretched

        #From http://www.commandlinefu.com/commands/view/2055/change-wallpaper-for-xfce4-4.6.0
        #pretend conf does not already exist, because on some systems it might not (MX-17, possibly Manjaro?):
        useImageForBackground = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-show", "-n", "-t", "string", "-s", "true"]
        subprocess.Popen(useImageForBackground)
        # https://forum.xfce.org/viewtopic.php?id=10894
        # this is probably sufficient for xfce < 4.11
        primaryImage = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-path", "-s", absPath]
        subprocess.Popen(primaryImage)
        # this should get the main workspace for xfce > 4.11
        workspace0Image = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace0/last-image", "-s", absPath]
        subprocess.Popen(workspace0Image)

        styleArgs = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-style", "-s", imageStyle]
        subprocess.Popen(styleArgs)
        workStyleArgs = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace0/image-style", "-s", imageStyle]
        subprocess.Popen(workStyleArgs)

        reloadXfdesktop = ["xfdesktop","--reload"]
        subprocess.Popen(reloadXfdesktop)
    # end changeWallpaperXFCE4

    def changeWallpaperLXDE(self, absPath, stretched = True):
        #from: https://stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python
        #can force different size with: --wallpaper-mode=
        if(stretched):
            os.system("pcmanfm --wallpaper-mode=stretch")
        else:
            os.system("pcmanfm --wallpaper-mode=fit")
        # scaled, stretch, center, fit (none of these fills scales to screen size, so I dont apply any of them)
        os.system("pcmanfm --set-wallpaper " + shlex.quote(absPath))
    # end changeWallpaperLXDE

    def changeWallpaperLXQT(self, absPath, stretched = True):
        # This method of changing wallpapers seems to take a few seconds to apply...
        # may take up to 2 minutes to apply...?
        #can force different size with: --wallpaper-mode=
        # scaled, stretch, center, fit (none of these fills scales to screen size, so I dont apply any of them)
        if(stretched):
            os.system("pcmanfm-qt --wallpaper-mode=stretch")
        else:
            os.system("pcmanfm-qt --wallpaper-mode=fit")
        #NOTE: I have run into issues (in emulated environment) when screen does not properly refresh, desktop/computer becoming completely frozen and unusable, and possibly others I do not remember...
        os.system("pcmanfm-qt --set-wallpaper " + shlex.quote(absPath))
    # end changeWallpaperLXDE


