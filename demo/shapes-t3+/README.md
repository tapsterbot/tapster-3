# Setup
```
pip install svg-to-gcode
```

# Using the SVG Drawer
## For Shapes:
- Make your SVG in a program such as Inkscape, and save it to this directory.
- When you call the Draw.drawSVG() method, specify your corner points. This will scale any content in your SVG file to be between those two points automatically, while preserving the aspect ratio.

## For Drawing Text:
- Make your SVG file, and add your text.
- Select your text, and in Inkscape, go to Extensions >> Text >> Hershey Text. This will convert your text from a filled in font to a line font, which works better with the Tapster robot.
- Select your font, and then hit apply.
    - If you get an error message, you are trying to convert a piece of text that has already been converted. Rewrite the text in a new text box, and then reopen Hershey Text and retry.
- Save the SVG to this directory.
- Run the Draw.drawSVG() method as normal.

## Credits:
Thank you to PadLex on GitHub for making the SVG to Gcode converter used for this project, and the sample code used in svgToGcode.py. Check out his project [here](https://github.com/PadLex/SvgToGcode)