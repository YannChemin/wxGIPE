#/usr/bin/python
"""
This is a way to save the startup time when running img2py on lots of
files...
"""
import sys
from wx.tools import img2py

command_lines = [
	"-i -a -u -n PngGipe gipe.png ../images.py",
	# Proc basic buttons
	"-i -a -u -n PngHelpAbout help-about.png ../images.py",
	"-i -a -u -n PngDialogOK dialog-ok-apply.png ../images.py",
	"-i -a -u -n PngDialogCancel dialog-cancel.png ../images.py",
	# wx_gipe basic buttons
	"-i -a -u -n PngDocOpen document-open.png ../images.py",
	"-i -a -u -n PngDocSaveAs document-save-as.png ../images.py",
	"-i -a -u -n PngDocSaveAs document-save-as.png ../images.py",
	"-i -a -u -n PngSnapShot ksnapshot.png ../images.py",
	"-i -a -u -n PngReload reload.png ../images.py",
	# Zoom
	"-i -a -u -n PngZoomFitBest zoom-fit-best.png ../images.py",
	"-i -a -u -n PngZoomIn zoom-in.png ../images.py",
	"-i -a -u -n PngZoomOriginal zoom-original.png ../images.py",
	"-i -a -u -n PngZoomOut zoom-out.png ../images.py",
	# Others
	"-i -a -u -n PngArrow arrow.png ../images.py",

	]

if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)
