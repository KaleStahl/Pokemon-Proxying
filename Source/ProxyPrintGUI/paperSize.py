'''
paperSize.py
Created on 2026-08-24 by Kale Stahl
Last Updated on 2026-08-24 by Kale Stahl
'''

class Paper:
    '''Class to store paper size information.'''

    def __init__(self, name, width, height):
        '''
        Initialize the Paper object with its name, dimensions.

        Parameters
        ----------
        name : str
            The name of the paper size (e.g., "A4", "Letter").  
        width : float
            The width of the paper in inches.
        height : float
            The height of the paper in inches.        
        '''
        self.name = name
        self.width = width
        self.height = height

from enum import Enum

class PaperSizes(Enum):
    '''
    Enum class to store paper sizes and their dimensions.
    '''
    A3 = Paper("A3", 11.69, 16.54)
    A4 = Paper("A4", 8.27, 11.69)
    A5 = Paper("A5", 5.83, 8.27)
    A7 = Paper("A7", 2.91, 4.13)
    Letter = Paper("Letter", 8.5, 11.0)
    Legal = Paper("Legal", 8.5, 14.0)
    Ledger = Paper("Ledger", 11.0, 17.0)