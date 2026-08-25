'''
UserInterface.py
Created on 2026-08-24 by Kale Stahl
Last Updated on 2026-08-24 by Kale Stahl
'''

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfilename
import math

class UserInterface:
    """Class to create the application GUI."""

    _root = None # Stores the tkinter root object for use in the class methods.

    def __init__(self, root):
        self._root = root

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

    def uxInitialize(self):
        """
        Initialize the application.

        Parameters
        ----------
        root : tkinter.tk
            Interface to initialize.

        Returns
        -------
        None.

        """
        ### ADD MENU BAR AND PANELS FOR INITiALIZATION ###
        self._root.mainloop()
        return None
