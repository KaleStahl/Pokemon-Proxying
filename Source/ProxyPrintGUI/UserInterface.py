'''
UserInterface.py
Created on 2026-08-24 by Kale Stahl
Last Updated on 2026-08-24 by Kale Stahl
'''

from logging import root
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfilename
import math

class UserInterface:
    """Class to create the application GUI."""

    _root = None # Stores the tkinter root object for use in the class methods.
    _menuBar = None # Stores the menu bar object for use in the class methods.
    _fileMenu = None # Stores the file menu object for use in the class methods.
    _helpMenu = None # Stores the help menu object for use in the class methods.

    def __init__(self, root):
        self._root = root

    ### EVENT HANDLER FUNCTIONS ###
    def uxReadMe(self):
        """
        Event handler for README menu bar item.

        Returns
        -------
        None.

        """
        from os import startfile
        startfile("README.txt")
        return None
    
    def uxGithub(self):
        """
        Event handler for GitHub menu bar item.

        Returns
        ------
        None.

        """
        import webbrowser
        webbrowser.open_new("https://github.com/KaleStahl/Pokemon-Proxying")
        return None

    def onClose(self, window):
        window.destroy()
        return None

    def uxSetApiKey(self):
        """
        Event handler for Set API Key menu bar item.

        Returns
        -------
        None.

        """
        return None

    def uxSavePDF(self):
        """
        Event handler for Save PDF menu bar item.

        Returns
        -------
        None.

        """
        return None

    def uxSavePDFAs(self):    
        """
        Event handler for Save PDF As menu bar item.

        Returns
        -------
        None.

        """
        return None

    ### GUI INITIALIZATION FUNCTIONS ###
    def uxInitialize(self):
        """
        Initialize the application by calling the menu bar, layout, and mainloop functions.

        Returns
        -------
        None.

        """
        ### ADD MENU BAR AND PANELS FOR INITiALIZATION ###
        self.uxFileMenu()
        self.uxLayout()
        self._root.mainloop()
        return None

    def uxLayout(self):
        """
        Sets the layout for the application body.

        Returns
        -------
        None.

        """
        ## Configures column setup
        self._root.geometry("680x680")
        self._root.title("ProxyPrintGUI")
        self._root.update()
        self._root.protocol("WM_DELETE_WINDOW",lambda: self.onClose(self._root))
        self._root.columnconfigure(0, weight = 1, minsize = self._root.winfo_width()/2)
        self._root.columnconfigure(1, weight = 1, minsize = self._root.winfo_width()/2)
        self._root.rowconfigure(0, weight = 1, minsize = self._root.winfo_height())

  

        return None

    def uxFileMenu(self):
        """

        Generate the file menu at the top of the application.

        Returns
        -------
        None.

        """
    
        self._menuBar = tk.Menu(self._root)

        # Create file menu bar
        self._fileMenu = tk.Menu(self._menuBar, tearoff=0)
        self._fileMenu.add_command(label="Save PDF", command=self.uxSavePDF)
        self._fileMenu.add_command(label="Save PDF As", command=self.uxSavePDFAs)
        self._fileMenu.add_separator()
        self._fileMenu.add_command(label="Exit", command=lambda: self.onClose(self._root))
        self._menuBar.add_cascade(label="File", menu=self._fileMenu)

        # Initializes API Keysmenu bar
        self._helpMenu = tk.Menu(self._menuBar, tearoff=0)
        self._helpMenu.add_command(label="Set API Key", command=self.uxSetApiKey)
        self._menuBar.add_cascade(label="API Keys", menu=self._helpMenu)
        
        # Initializes help menu bar
        self._helpMenu = tk.Menu(self._menuBar, tearoff=0)
        self._helpMenu.add_command(label="README", command=self.uxReadMe)
        self._helpMenu.add_command(label="GitHub", command=self.uxGithub)
        self._menuBar.add_cascade(label="Help", menu=self._helpMenu)

        self._root.config(menu=self._menuBar)

        return None