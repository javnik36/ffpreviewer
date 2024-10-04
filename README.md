# ffpreviewer
This small program allows you to do 4 main things:
  * generates .png files for each glyph in your font,
  * generates .pdf file containing all kern pairings found in your font,
  * generates .pdf file containing all glyph pairs between all glyphs in your font,
  * generates .pdf file containing all glyph pairs for selected character.

## Prerequisites
You will need to have [FontForge](https://fontforge.org/en-US/) installed.
  * FontForge supposedly installs python module required by *ffpreviewer*, but I am not able to confirm that without reinstallation. How to run section below, assumes that you don't have it installed, so you will need to provide full path to **ffpython.exe** executable - it is inside *\bin* folder of FontForge installation.

## man - How to run
```cmd
F:/FontForge/bin/ffpython.exe .\ffpreviewer.py -h
usage: ffpreviewer [-h] [-i [DIR]] [-k] [-a] [-s GLYPH] FONT_PATH

Simple script to generate font preview files.

positional arguments:
  FONT_PATH   Path to font.

options:
  -h, --help  show this help message and exit
  -i [DIR]    Generates png file for each glyph in a font to specified DIRectory (uses default folder 'glyphs' if not provided).
  -k          Generates pdf file containing all kern pairings found in a font.
  -a          Generates pdf file containing all glyph pairs between all glyphs in a font.
  -s GLYPH    Generates pdf file containing all glyph pairs for selected character. GLYPH = ascii encoded decimal number of selected glyph.
```

For *-s* flag you will need to supply decimal number of glyph (in ascii encoding) you want to have in your .pdf. E.g. it will be 43 (so `ffpreviewer -s 43 font.ttf`) for "+" character.

## License
Licensed under MIT License. 
Copyright (c) 2024 [Javnik](https://github.com/javnik36/).