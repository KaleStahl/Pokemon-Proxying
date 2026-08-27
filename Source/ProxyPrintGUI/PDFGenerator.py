'''
PDFGenerator.py
Created on 2026-08-24 by Kale Stahl
Last Updated on 2026-08-26 by Kale Stahl
'''

import os
import re
import unicodedata
import threading
from Source.ProxyPrintGUI import PDFOptions
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

class PDFGenerator:
    '''
    Class to generate the proxy pdf from the GUI.
    '''    

    image_cache = {}
    image_cache_lock = threading.Lock()
    image_reader_cache = {}
    image_reader_cache_lock = threading.Lock()
    image_session = requests.Session()
    CARD_QUERY_PAGE_SIZE = 100
    card_lookup_cache = {}
    card_lookup_cache_lock = threading.Lock()


    def __init__(self,
                card_list,
                output_file,
                APIKey,
                PDFOptions = PDFOptions.PDFOptions()
                ):
        '''
        Constructor for the PDFGenerator class.

        Parameters:
        ----------
        card_list : list
            A list of card images to be included in the PDF.
        output_file : str
            The path to the output PDF file.
        APIKey : str
            The API key for the Pokémon TCG SDK.
        PDFOptions : PDFOptions
            An instance of the PDFOptions class containing user-defined settings for the PDF generation.
        '''
        self._cards = card_list
        self._outputPath = output_file
        self._options = PDFOptions
        self._cardsPerPage = PDFOptions.cards_per_page
        self._pageWidth, self._pageHeight = PDFOptions.page_width, PDFOptions.page_height
        self._cardWidth, self._cardHeight = PDFOptions.card_width, PDFOptions.card_height
        self._orientation = PDFOptions.orientation
        self._saturation = PDFOptions.saturation
        self._brightness = PDFOptions.brightness
        self._contrast = PDFOptions.contrast
        self._red = PDFOptions.red
        self._green = PDFOptions.green
        self._blue = PDFOptions.blue
        self._cardBacks = PDFOptions.cardBacks
        self._cardBackText = PDFOptions.cardBackText
        self._proxyText = PDFOptions.proxyText
        self._horizontal_margin = PDFOptions.horizontal_margin
        self._vertical_margin = PDFOptions.vertical_margin
        self._horizontal_spacing = PDFOptions.horizontal_spacing
        self._vertical_spacing = PDFOptions.vertical_spacing
        self._targetDPI = PDFOptions.TargetDPI

        # Initialize the RestClient with the provided API key for the Pokémon TCG SDK
        RestClient.configure(APIKey)

    def get_image(self, url):
        '''
        Fetches an image from a URL, applies color adjustments, and caches the result.
        
        Parameters
        ----------      
        url : str
            The URL of the image to fetch.
        
        Returns
        -------
        PIL.Image.Image
            The fetched and adjusted image.
        '''
        TARGET_W = int(self._cardWidth * self._targetDPI)  
        TARGET_H = int(self._cardHeight * self._targetDPI)  
        with self.image_cache_lock:
            cached = self.image_cache.get(url)
        if cached is not None:
            return cached
        r = self.image_session.get(url, timeout=20)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        # Upscale to target print resolution
        img = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)

        # Apply color adjustments
        img = ImageEnhance.Color(img).enhance(self._saturation)
        img = ImageEnhance.Brightness(img).enhance(self._brightness)
        img = ImageEnhance.Contrast(img).enhance(self._contrast)

        img = img.filter(
            ImageFilter.UnsharpMask(
                radius=0.5,
                percent=120,
                threshold=2
            )
        )
        with self.image_cache_lock:
            self.image_cache[url] = img
        return img

    def get_image_reader(self, url):
        '''
        Fetches an image from a URL, applies color adjustments, and returns an ImageReader object for use in ReportLab.
        
        Parameters
        ----------
        url : str
            The URL of the image to fetch.

        Returns
        -------
        ReportLab.lib.utils.ImageReader
            An ImageReader object for use in ReportLab.
        '''
        with self.image_reader_cache_lock:
            cached = self.image_reader_cache.get(url)
        if cached is not None:
            return cached
        img = self.get_image(url)
        reader = ImageReader(img)
        with self.image_reader_cache_lock:
            self.image_reader_cache[url] = reader
        return reader

    def prefetch_images(self, max_workers=12):
        '''
        Prefetches images from the provided URLs using a thread pool to improve performance.
        
        Parameters
        ----------
        max_workers : int, optional
            The maximum number of worker threads to use (default is 12).
        '''
        unique_urls = list(dict.fromkeys(self._cards))  # Remove duplicates while preserving order)
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(self.get_image, url) for url in unique_urls]
            for f in as_completed(futures):
                try:
                    f.result()
                except:
                    pass

    def get_page_setup(self):
        '''
        Calculates the number of columns and rows of cards that can fit on a page based on the current PDF options.
        '''
        cols = int((self._pageWidth - 2 * self._horizontal_margin + self._horizontal_spacing) / (self._cardWidth + self._horizontal_spacing))
        rows = int((self._pageHeight - 2 * self._vertical_margin + self._vertical_spacing) / (self._cardHeight + self._vertical_spacing))
        return cols, rows
    
    def create_pdf(self):
        '''
        Creates a PDF file with the specified card images and options.

        Returns
        -------
        canvas.Canvas
            The ReportLab canvas object for the created PDF.
        '''
        self.prefetch_images(self._cards)
        numcols, numrows = self.get_page_setup()
        c = canvas.Canvas(
            self._outputPath,
            pagesize=(self._pageWidth, self._pageHeight),
            pageCompression=0
            )
        x0, y0 = 0, 0
        c.setFillColor(colors.gray)

        for page_start in range(0, len(self._cards), self._cardsPerPage):
            c.setFont("Helvetica", 3)
            page_urls = self._cards[page_start:page_start + self._cardsPerPage]
            for offset, url in enumerate(page_urls):
                row = (offset // numcols) % numrows
                col = offset % numcols
                reader = self.get_image_reader(url)

                x = col * (self._cardWidth + self._horizontal_spacing)
                y = (numrows - 1 - row) * (self._cardHeight + self._vertical_spacing)

                c.drawImage(
                    reader,
                    x, y,
                    width=self._cardWidth,
                    height=self._cardHeight,
                    preserveAspectRatio=True,
                    mask='auto'
                )
                c.setFont("Helvetica", 3)
                c.drawCentredString(
                    x + 3 * self._cardWidth / 4,
                    y + 1,
                    self._proxyText
                )
            if page_start + self._cardsPerPage < len(self._cards):
                c.showPage()
        c.save()
        return c