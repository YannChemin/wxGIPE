# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  wxGIPE
# Purpose:  Satellite image [multi/hyper][spectral/temporal] pixel plotting
# Author:   Yann Chemin, <yann.chemin@gmail.com>
#
###############################################################################
# Copyright (c) 2008, Yann Chemin <yann.chemin@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

#!/usr/bin/python

import  wx
import  wx.lib.plot
import  numpy

class TestFrame(wx.Frame):
    def __init__(
            self, parent, ID, title, pos=wx.DefaultPosition,
            size=(600, 400), style=wx.DEFAULT_FRAME_STYLE
            ):

        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
 
    def OnCloseWindow(self, event):
        self.Destroy()
 
class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, size=(600, 400))

        self.client = wx.lib.plot.PlotCanvas(self)
	sizer = wx.BoxSizer()
        sizer.Add(self.client, 1, wx.EXPAND)
        self.SetSizer(sizer)
        data1 = 2.*numpy.pi*numpy.arange(2*100)/200.
        data1.shape = (100, 2)
        data1[:,1] = numpy.sin(data1[:,0])
        markers1 = wx.lib.plot.PolyMarker(data1, legend='Green Markers', colour='green', marker='circle',size=1)

    # 50 points cos function, plotted as red line
        data1 = 2.*numpy.pi*numpy.arange(2*100)/200.
        data1.shape = (100,2)
        data1[:,1] = numpy.cos(data1[:,0])
        lines = wx.lib.plot.PolyLine(data1, legend= 'Red Line', colour='red')
        a = wx.lib.plot.PlotGraphics([markers1, lines],"Graph Title", "X Axis", "Y Axis")
        self.client.Draw(a)



def __ptest():

    app = wx.PySimpleApp()
    win = TestFrame(None, -1, "Test FRAME")
    win2 = TestPanel(win)
    win.Show(True)
    app.MainLoop()



if __name__ == '__main__':
    __ptest()
