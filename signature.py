#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
# for plot
import  wx.lib.plot
import numpy

#use gdal 1.5.x and more
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
	    size=(600,400), style=wx.DEFAULT_FRAME_STYLE):

		wx.Frame.__init__(self, parent, id, title, pos, size)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		
	def OnCloseWindow(self, event):
		self.Destroy()
	
class TestPanel(wx.Panel):
	def __init__(self, parent):
        	wx.Panel.__init__(self, parent, -1, size=(600, 400))

		self.client = wx.lib.plot.PlotCanvas(self)
		sizer = wx.BoxSizer()
		sizer.Add(self.client, 1, wx.EXPAND)
		self.SetSizer(sizer)
	
		Img = 'test_data/data.bsq'
		pixel_y = 0
		pixel_x = 1
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
		data=numpy.zeros(rl)
		lines = wx.lib.plot.PolyLine(data1, legend= 'Profile 1', colour='Blue')
		markers1 = wx.lib.plot.PolyMarker(data1, legend='Img', colour='Navy Blue', marker='circle',size=1)
		graphic=wx.lib.plot.PlotGraphics([markers1,lines],"LMF Profile", "Temporal Axis", "Value Axis")
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
