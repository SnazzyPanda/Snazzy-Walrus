'''

@author: Snazzy Panda
'''
#import tkinter as tk
from snazzy.helpers.IOHelper import IOHelper
import sys
import gi
gi.require_version("Gtk", '3.0')
from gi.repository import Gtk


class MainWindow():
    '''
    classdocs
    '''

    def createGtkWindow(self):
        win = Gtk.Window()
        builder = Gtk.Builder()
        builder.add_from_file(IOHelper.FULL_WINDOW_UI_PATH + "SnazzyWalrus.glade")
        win = builder.get_object("SnazzyWalrusWindowMain")
        win.connect("delete-event", Gtk.main_quit)
#        win.connect("delete-event", self.closeWindowAndExit)
        win.show_all()
        Gtk.main()

#        win = Gtk.Window()
#        win.connect("delete-event", Gtk.main_quit)
#        win.show_all()
#        Gtk.main()

#    def createWidgets(self):
#        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
#        self.quitButton.grid()

    def __init__(self, master=None):
        self.createGtkWindow()
#        tk.Frame.__init__(self, master)
#        self.grid()
#        self.createWidgets()
        '''
        Constructor
        '''
        
    def closeWindowAndExit(self):
        print("")
#        Gtk.main_quit()
        sys.exit(0)
    # end closeWindowAndExit
