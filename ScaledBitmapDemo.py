#!/usr/bin/env python

## Set a path to an Image file here:
#ImageFile = "/home/yann/Greek_EXP/SRTM_u03_p183r032.tif" 
ImageFile = "/home/yann/Desktop/Work/wx_gipe/test_data/b321.tif" 
import wx
## import the installed version
from wx.lib.floatcanvas import NavCanvas, FloatCanvas
## import a local version
#import sys
#sys.path.append("../")
#from floatcanvas import NavCanvas, FloatCanvas
class DrawFrame(wx.Frame):
    """
    A frame used for the FloatCanvas Demo
    """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.CreateStatusBar()
        # Add the Canvas
        Canvas = NavCanvas.NavCanvas(self,ProjectionFun = None,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ).Canvas
        Canvas.MaxScale=8
        self.Canvas = Canvas
        FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove )
        # create the image:
        image = wx.Image(ImageFile)
        img = Canvas.AddScaledBitmap( image,(0,0),Height=image.GetHeight(),
                                      Position = 'tl',)
        #Box.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.Binding)
        self.Show()
        Canvas.ZoomToBB()
    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%i, %i"%tuple(event.Coords))
    def Binding(self, event):
        print "Writing a png file:"
        self.Canvas.SaveAsImage("junk.png")
        print "Writing a jpeg file:"
        self.Canvas.SaveAsImage("junk.jpg",wx.BITMAP_TYPE_JPEG)
app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(1024,800) )
app.MainLoop()
    
    
    
    









