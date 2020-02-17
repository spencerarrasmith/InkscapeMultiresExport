# Inkscape Multi-Resolution Export
This is a simple Python GUI which takes a number of user inputs to specify regions of an Inkscape canvas. First, the .svg file must be selected in the file browser, and its name will appear next to the "Select File" button if successful. Next, supply the following information:

* Name of object
* Lower Left X-Coord (px) (these appear in this order on the top bar in Inkscape)
* Lower Left Y-Coord (px)
* Region Width (px)
* Region Height (px)
* Export Resolutions (comma-separated)

From these inputs, the program executes shell commands to export these regions in all specified resolutions, and places them in a new subdirectory adjacent to the .svg file itself.

# Requirements
* Python 3.6+
* Inkscape
* Add Inkscape to PATH (Windows)

