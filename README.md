# Pokemon Proxying

This is a script I made which uses the [Pokemon TCG API](https://pokemontcg.io/) to grab high quality card scans and arranges them in the correct size to print.

## Usage
- **(Step 0)** Get a free API key by verifying your email at [https://pokemontcg.io/](https://pokemontcg.io/) and copy it into a .env file. An example file is included in this repo, just rename it to ".env" after pasting the key. This is not strictly required, but reduces rate limiting and speeds up API calls. Also make sure you have the latest version of Python installed.
- **(Step 1)** Copy and paste your decklist into the decklist.txt file. I personally use the [MyLimitless](https://my.limitlesstcg.com/) deckbuilder, so that is the only decklist format that has been tested. I believe my querying supports other decklist formats, but have not confirmed this.
- **(Step 2)** Run the ProxiesFromDeck.exe. A python terminal will open. It will show the current settings and give you an option to edit them. Target DPI is the max DPI the code attempts to scale the images to. The output file and decklists paths are just there if you want to make separate files instead of overwriting the same one each time. Drawing grid lines draws lines to help you cut out the proxies. If no edits are needed, you can press enter.
- **(Step 3)** The program will read the decklist and collect the image URLs from the API. It will then tell you if it was unable to find any cards and give you the number of cards found. If it is missing cards, you can exit here without generating a PDF. Otherwise, you can press enter and it will generate a PDF at the desired path which will try to automatically open in the default program (if your system allows it).

## Known Issues
- Sometimes promo cards aren't found correctly. This is mainly an API issue exacerbated by my crappy code, so check their documentation for how to find that specific card by editing your decklist.
- Finding images and generating the PDF are slow. Don't worry, it's not your computer. The API is not super fast and my code is not at all optimized to reduce API calls because I'm lazy. Reportlab is also not very fast, so if you are generating 30+ proxies it can take up to a minute to make the PDF.
- The API doesn't always have the highest quality scans, especially for older cards. As such, not all images can be properly scaled to the target DPI.

## History
Version .01 (2026-5-7) Initial Release with barebones functionality

## License
The MIT License (MIT)

Copyright (c) 2026 Kale Stahl

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
