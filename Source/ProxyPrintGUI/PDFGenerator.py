'''
PDFGenerator.py
Created on 2026-08-24 by Kale Stahl
Last Updated on 2026-08-24 by Kale Stahl
'''

import os
import re
import unicodedata
import threading
from paperSize import PaperSizes
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
from pokemontcgsdk import Card, RestClient
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

### Set your API key (get one for free at https://pokemontcg.io/)
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")
RestClient.configure(api_key)

class PDFGenerator:
    '''
    Class to generate the proxy pdf from the GUI.
    '''

    _cards = None
    _ouputFile = None
    _cardsPerPage = None
    _pageHeight = None
    _pageWidth = None
    _cardWidth = None
    _cardHeight = None
    _orientation = None
    
    def __init__(self,
                card_list,
                output_file,
                cards_per_page = 9,
                paper = PaperSizes.Letter.value,
                card_width = 2.5 * inch,
                card_height = 3.5 * inch,
                orientation = 'portrait',

                ):
        self._cards = card_list
        self._output = output_file
        self._cardsPerPage = cards_per_page
        self._pageWidth, self._pageHeight = paper.width, paper.height
        self._cardWidth, self._cardHeight = card_width, card_height
        self._orientation = orientation
