#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  GDAL Image Processing Environment
# Purpose:  wxPython interface to plotting multi-spectral pixel information
#		EXPERIMENTAL!
#
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

import wx
# for plot
import  wx.lib.plot
import numpy
#use gdal 1.5.x
from osgeo import gdalnumeric
from osgeo import gdal_array
from osgeo import gdal
from osgeo.gdalconst import *

# For icons, pngs, etc coming from images.py
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO
import images

class TestFrame(wx.Frame):
	def __init__(self, parent, id, title, pos=wx.DefaultPosition,
	    size=(300,200), style=wx.DEFAULT_FRAME_STYLE):

		wx.Frame.__init__(self, parent, id, title, pos, size)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		
	def OnCloseWindow(self, event):
		self.Destroy()
	
class TestPanel(wx.Panel):
	def __init__(self, parent):
        	wx.Panel.__init__(self, parent, -1, size=(300, 200))

		self.client = wx.lib.plot.PlotCanvas(self)
		sizer = wx.BoxSizer()
		sizer.Add(self.client, 1, wx.EXPAND)
		self.SetSizer(sizer)
		
		number = 2
		pix_x = 10
		pix_y = 20
		display = []
		Img = 'test_data/f.bsq'
		if(number==2):
			Img2 = 'test_data/data.bsq'
		pixel_y = pix_y
		pixel_x = pix_x
		
		print "Draw ",Img
		Img2D = gdal.Open(str(Img), GA_ReadOnly)
		#Imgarray = gdal_array.LoadFile(str(Img))
		#geomatrix = Img2D.GetGeoTransform()
		#north = geomatrix[0]
		#resolution_y = abs(geomatrix[1])
		##print resolution_y
		#west = geomatrix[3]
		#resolution_x = abs(geomatrix[5])
		##print resolution_x
		#projection = Img2D.GetProjection()
		##print projection
		#x_min = y_min = 0
		x_max = Img2D.RasterXSize
		y_max = Img2D.RasterYSize
		#corners = [(x_min, y_min),
			#(x_min, y_max),
			#(x_max, y_min),
			#(x_max, y_max),]
		#south = north - y_max*resolution_y
		#east = west + x_max*resolution_x
		imgH = y_max
		imgW = x_max
		print "X= ",imgW, "Y= ",imgH
		result = []
		for iBand in range(1, Img2D.RasterCount + 1):
			print "iBand = ", iBand
			inband = Img2D.GetRasterBand(iBand)
			scanline = inband.ReadAsArray(pixel_x, 0, 1, inband.YSize, 1, inband.YSize)
			pixel = scanline[pixel_y][0]
			print pixel
			result.append(pixel)
		
		print result
		rl = len(result)
		data1 = numpy.arange(2*rl)
		data1.shape = (rl, 2)
		data1[:,1] = result[:]
		lines1 = wx.lib.plot.PolyLine(data1, legend= 'Profile 1', colour='Blue')
		markers1 = wx.lib.plot.PolyMarker(data1, legend='Img', colour='Navy Blue', marker='circle',size=1)
		del result
		
		display.append(lines1)
		display.append(markers1)
		
		if(number==2):
			pixel_y = pix_y
			pixel_x = pix_x
			Img2D = gdal.Open(str(Img2), GA_ReadOnly)
			x_max = Img2D.RasterXSize
			y_max = Img2D.RasterYSize
			imgH = y_max
			imgW = x_max
			print "X= ",imgW, "Y= ",imgH
			result = []
			for iBand in range(1, Img2D.RasterCount + 1):
				print "iBand = ", iBand
				inband = Img2D.GetRasterBand(iBand)
				scanline = inband.ReadAsArray(pixel_x, 0, 1, inband.YSize, 1, inband.YSize)
				pixel = scanline[pixel_y][0]
				print pixel
				result.append(pixel)
			print result
			rl = len(result)
			data2 = numpy.arange(2*rl)
			data2.shape = (rl, 2)
			data2[:,1] = result[:]
			lines2 = wx.lib.plot.PolyLine(data2, legend= 'Profile 1', colour='Dark Green')
			markers2 = wx.lib.plot.PolyMarker(data2, legend='Img', colour='Dark Green', marker='cross',size=1)
			
			display.append(lines2)
			display.append(markers2)

		
		graphic=wx.lib.plot.PlotGraphics(display,"LMF Profile", "Temporal Axis", "Value Axis")
		self.client.Draw(graphic)

	def resetDefaults(self):
		"""Just to reset the fonts back to the PlotCanvas defaults"""
		self.client.SetFont(wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL))
		self.client.SetFontSizeAxis(10)
		self.client.SetFontSizeLegend(7)
		self.client.setLogScale((False,False))
		self.client.SetXSpec('auto')
		self.client.SetYSpec('auto')

if __name__ == '__main__':
        app = wx.PySimpleApp()
        frame = TestFrame(None, -1, 'Shamim\'s LMF curve')
	frame1 = TestPanel(frame)
	frame.Show(True)
        app.MainLoop()
