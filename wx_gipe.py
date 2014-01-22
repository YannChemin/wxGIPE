#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  GDAL Image Processing Environment
# Purpose:  wxPython interface to GDAL image manipulation under georeferencing
#           constraints
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
import wx.aui

#Import canvas
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

# Console redirect
from console import *

# For icons, pngs, etc coming from images.py
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO
import images
import GipeIcon

#for OnAbout
from wx.lib.wordwrap import wordwrap

#for Canvas
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

# For Image Processing
#import Numeric #old
import numpy #new
from osgeo import gdalnumeric
from osgeo import gdal
from osgeo.gdalconst import *
import gdal_merge as g_m
# Saving arrays functions
from GDAL_functions import *

# Get Remote Sensing functions
#from RS import *

# Load Tools
from gipe_tools import *

#Useful stuff for later
#wxProgressDialog wait("Please Wait", "Saving image...", 3);
#// progress bar will show one third of the way along
#wait.Update(0);

global coordsys
global north
global south
global east
global west
global resolution_x
global resolution_y
global fullfilename
global zoom_x
global zoom_y
global zoom_scale
global maxWith
global maxHeight
global zoom_tool_on

#screen type or geo_image type
display_coordinate_type='screen'
coordsys = ''
north = 0.0
south = 0.0
east = 0.0
west = 0.0
resolution_x = 0.0
resolution_y = 0.0
projection = ''
fullfilename = ''
dirname = ''

#Set module path
import sys, os
sys.path.append( os.getcwd() )

class MyFrame(wx.Frame):
	def __init__(self, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)
		self.CreateStatusBar()
		self.SetSize((800,800))
		self.SetTitle("GDAL Image Processing Environment")
		ico = GipeIcon.getIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		self._mgr = wx.aui.AuiManager(self)
		Canvas = NavCanvas.NavCanvas(self,ProjectionFun = None,
					BackgroundColor = "DARK SLATE BLUE",
					).Canvas
		Canvas.MaxScale=4
		self.Canvas = Canvas
		FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove)
		self.createMenuBar()
		self.createToolBar()
		self.console = wxConsole(self, -1)
		self.bindEvents()
		self._mgr.AddPane(self.console, wx.BOTTOM, 'Python Command Line Interface')
		self._mgr.AddPane(self.Canvas, wx.CENTER, 'Image Processing')
		self._mgr.Update()
	
	def bindEvents(self):
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		
	def menuData(self):
		return (("&File ",
				(" &Open ", " Open file", self.OnOpen),
				(" Save &As ", " Change Image Format",OnConvert),
				("", "", ""),
				(" &Screenshot ", " Save display as PNG file", self.SaveToFile),
				("", "", ""),
				(" &Quit ", "Quit", self.OnCloseWindow)),
			("&Tools ",
				(" &Layer Stack Many ", "Layer Stack Many", OnLayerStack),
				(" &Layer Stack RGB ", "Layer Stack RGB", OnLayerStackRGB),
				("", "", ""),
				(" &Convert to any ", "Convert to any", OnLayerStackRGB),
				(" &Convert to LatLong ", "Convert to LatLong", OnLayerStackRGB),
				("", "", ""),
				(" &Options... ", "Options", self.OnOptions)),
			("&Import ",
				(" &HDF", "Import HDF", OnImportHdf),
				("", "", ""),
				(" &Aster ", "Aster DN to Rad to RefTOA", OnProcAsterIn),
				(" &Landsat ", "Landsat DN to Rad to RefTOA", OnProcLandsatIn),
				("", "", ""),
				(" Modis Q&A ", "MODIS09Q/A Quality Assessment", OnProcModisQc),
				(" Modis &State QA ", "MOD09A State QA", OnProcModisQa),
				("", "", "")),
			("&Process ",
				(" &Albedo ", "Albedo", OnProcAlbedo),
				(" &NDVI ", "NDVI", OnProcNdvi),
				("", "", ""),
				(" &ET... ", "Options", self.OnOptions)),
			("&Auto-Process ",
				(" &L7ETPOT RS ", "Landsat DN to ETPOT (RS)", OnProcLandsatEtpotrs),
				(" L7ETa &Senay ", "Landsat DN to ETa (Senay)", OnProcLandsatEtasenay)),
			("&Help ",
				(" &Manual ", "Manual", self.OnHelpManual),
				(" &About ", "About", self.OnAbout)))
		
	def createToolBar(self):
		toolbar = self.CreateToolBar()
		fileopen = images.getPngDocOpenBitmap()
		fopen = toolbar.AddSimpleTool(-1,fileopen,"Open","Display Image")
		self.Bind(wx.EVT_TOOL, self.OnOpen,fopen)
		filesaveas = images.getPngDocSaveAsBitmap()
		fsaveas = toolbar.AddSimpleTool(-1,filesaveas,"Save As...","Save Image As Another GDAL Format")
		self.Bind(wx.EVT_TOOL, OnConvert,fsaveas)
		snapshot = images.getPngSnapShotBitmap()
		snap = toolbar.AddSimpleTool(-1,snapshot,"Screenshot","Save a PNG of the Display Area")
		self.Bind(wx.EVT_TOOL, self.SaveToFile,snap)
		toolbar.AddSeparator()
		reloadoriginal = images.getPngReloadBitmap()
		roriginal = toolbar.AddSimpleTool(-1,reloadoriginal,"Reload Original Image","Reload original image")
		self.Bind(wx.EVT_TOOL, self.OnReloadImage, roriginal)
		toolbar.AddSeparator()
		#arrow = images.getPngArrowBitmap()
		#arro = toolbar.AddCheckLabelTool(-1, "Checkable", arrow, shortHelp="Toggle this")
		##zin = toolbar.AddSimpleTool(-1,zoomin,"Zoom In Once","Zoom In Once")
		#self.Bind(wx.EVT_TOOL, self.OnArrowEnable, arro)
		#zoomin = images.getPngZoomInBitmap()
		#zin = toolbar.AddCheckLabelTool(-1, "Checkable", zoomin, shortHelp="Toggle this")
		##zin = toolbar.AddSimpleTool(-1,zoomin,"Zoom In Once","Zoom In Once")
		#self.Bind(wx.EVT_TOOL, self.OnZoomEnable, zin)
		toolbar.Realize()
	
	def createMenuBar(self):
		menuBar = wx.MenuBar()
		for eachMenuData in self.menuData():
			menuLabel = eachMenuData[0]
			menuItems = eachMenuData[1:]
			menuBar.Append(self.createMenu(menuItems), menuLabel)
		self.SetMenuBar(menuBar)
	
	def createMenu(self, menuData):
		menu = wx.Menu()
		for eachLabel, eachStatus, eachHandler in menuData:
			if not eachLabel:
				menu.AppendSeparator()
				continue
			menuItem = menu.Append(-1, eachLabel, eachStatus)
			self.Bind(wx.EVT_MENU, eachHandler, menuItem)
		return menu

	def OnCloseWindow(self, event):
        	# deinitialize the frame manager
        	self._mgr.UnInit()
        	# delete the frame
        	self.Destroy()
	
	# Getting Mouse Position in the Panel 
	def OnMove(self, event):
		if(display_coordinate_type=='screen'):
			"""
			Updates the status bar with the world coordinates
			"""
			self.SetStatusText("screen %i, %i"%tuple(event.Coords))
			## Client coordinates
			#self.posCtrl.SetValue("x=%s, y=%s" % (pos.x, pos.y))
		elif(display_coordinate_type=='geo_image'):
			global north
			global west
			global resolution_x
			global resolution_y
			# Image internal geo coordinates
			(pos_x,pos_y)=tuple(event.Coords)
			y_geo = north - pos_y*resolution_y
			x_geo = west + pos_x*resolution_x
			#self.posCtrl.SetValue("x=%s, y=%s" % (x_geo, y_geo))
			self.SetStatusText("geo %i, %i"% (x_geo,y_geo))

	# Display an image in the Window
	def OnOpen(self, event):
		#global zoom_scale
		#zoom_scale = 0.0
		global fileindisplay
		global fullfilename
		global dirname
		if (dirname == ''):
			# get current working directory
			self.dirname = os.getcwd()
		dlg = wx.FileDialog(self, "Pick a file", self.dirname, "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.flnm = dlg.GetFilename()
			self.dirnm = dlg.GetDirectory()
			self.text = ""
			self.text = os.path.join(self.dirnm,self.flnm)
			self.SetTitle(self.text)
			fileindisplay = self.text
			self.OnCopyToClipboard(self.text)
			fullfilename = self.text
			dirname = self.dirnm
			image = wx.Image(fullfilename)
			img = self.Canvas.AddScaledBitmap( image,(0,0),Height=image.GetHeight(),Position = 'tl',)
			self.Canvas.ZoomToBB()
		dlg.Destroy()
	
	def OnReloadImage(self, event):
		global fileindisplay
		self.text = ""
		self.text = fileindisplay
		self.SetTitle(self.text)
		self.OnCopyToClipboard(self.text)
		image = wx.Image(fullfilename)
		img = self.Canvas.AddScaledBitmap( image,(0,0),Height=image.GetHeight(),Position = 'tl',)
		self.Canvas.ZoomToBB()
		
	def SaveToFile(self, event):
		dlg = wx.FileDialog(self, "PNG Screenshot save as...",
			defaultDir = "",
			defaultFile = "",
			wildcard = "*.png",
			style = wx.SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			self.Window.SaveToFile(dlg.GetPath(),wx.BITMAP_TYPE_PNG)
		dlg.Destroy()

	def OnCopyToClipboard( self, info ):
		wx.TheClipboard.Open()
		data = wx.TextDataObject(info)
		success = wx.TheClipboard.SetData(data)
		#print "In Clipboard"
		#if(success):
		#	print "Get"+data.GetText()
		#else:
			#print "Empty Clipboard"
		wx.TheClipboard.Close()
		wx.TheClipboard.Flush()
		
	#Just grouping the empty event handlers together
	def OnCopy(self, event): pass
	def OnCut(self, event): pass
	def OnPaste(self, event): pass
	def OnOptions(self, event): pass
		
	def OnHelpManual(self, event):
		wx.Execute('python Help.py', True)
	
	def OnAbout(self,event):
		# First we create and fill the info object
		info = wx.AboutDialogInfo()
		info.Name = "GIPE"
		info.Version = "0.0.2"
		info.Copyright = """Copyright (c) 2008, Yann Chemin.\n
"""
		info.Description = wordwrap(" ",350, wx.ClientDC(self))
		info.WebSite = ("http://www.osgeo.org/gdal", "GDAL home page")
		info.Developers = [ "Yann Chemin <yann.chemin@gmail.com>\nUsed code from:","Frank Warmerdam <warmerdam@pobox.com>","Andrey Kiselev <dron@remotesensing.org>","" ]
		overview = """<html><body>
			<h2><center>GDAL Image Processing Environment</center></h2>.</body></html>"""
		licenseText = """This library is free software; you can redistribute it and/or modify it under the terms of the GNU Library General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.\n
This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public License for more details.\n
You should have received a copy of the GNU Library General Public License along with this library; if not, write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
		"""
		info.License = wordwrap(licenseText, 500, wx.ClientDC(self))
		# Then we call wx.AboutBox giving it that info object
		wx.AboutBox(info)


#class DrawWindow(BufferedWindow):
	#def Draw(self, dc):
		#global resolution_x
		#global resolution_y
		#global north
		#global south
		#global east
		#global west
		#global fullfilename
		#global dirname
		#global zoom_scale
		#global memory
		#global maxWidth
		#global maxHeight
		#dc.SetBackground( wx.Brush("Tan") )
		#dc.Clear()
		#if(fullfilename!=''):
			#Img = fullfilename
			#print "Draw ",Img
			#Img2D = gdal.Open(str(Img))
			##nband = Img2D.RasterCount
			#x_max = Img2D.RasterXSize
			#y_max = Img2D.RasterYSize
			##geomatrix = Img2D.GetGeoTransform()
			##north = geomatrix[0]
			##resolution_y = abs(geomatrix[1])
			##print resolution_y
			##west = geomatrix[3]
			##resolution_x = abs(geomatrix[5])
			##print resolution_x
			##projection = Img2D.GetProjection()
			##print projection
			#x_min = y_min = 0
			#corners = [(x_min, y_min),
				#(x_min, y_max),
				#(x_max, y_min),
				#(x_max, y_max),]
			#south = north - y_max*resolution_y
			#east = west + x_max*resolution_x
			#img_h = y_max
			#img_w = x_max
			#maxHeight = y_max
			#maxWidth = x_max
			#img_area = img_h*img_w
			#img_ratio = float (img_h/img_w)
			#Size = self.GetClientSizeTuple()
			#(w_w, w_h) = Size
			#h_ratio = float (w_h)/ float (img_h)
			#w_ratio = float (w_w)/ float (img_w)
			#w_area = w_w*w_h
			#newWidth = 0
			#newHeight = 0
			#if(h_ratio < w_ratio):
				#newHeight = w_h
				#newWidth = img_w*h_ratio
			#if(h_ratio > w_ratio):
				#newHeight = img_h*w_ratio
				#newWidth = w_w
			#if(w_area >= img_area):
				#newHeight = img_h
				#newWidth = img_w
			#maxWidth = newWidth
			#maxHeight = newHeight
			##print "height",img_h, "width", img_w
			#Img2D.BuildOverviews(overviewlist=[2,4])
			#band0 = Img2D.GetRasterBand(1).GetOverview(1)
			#array0 = band0.ReadAsArray()
			##min1=array0.min()
			##max1=array0.max()
			##print "min=",min1,"max=",max1
			##print "ovr=",array0
			#array = numpy.array([array0]*3,numpy.uint8)
			##print array, array0.shape
			#(nbands,tmp_h,tmp_w)=array.shape
			#del array0
			#Img2D1 = wx.ImageFromBuffer(tmp_w, tmp_h, array)
			#del array, tmp_w, tmp_h
			##image = wx.EmptyImage(y_max,x_max)
			##image.InitAlpha()
			##image.SetData(array)
			##if nband <= 2 :
				##image.SetData(array0)
			##else :
				##image.SetData(array0,array1,array2)
			##Img2D1=wx.ImageFromDataWithAlpha(y_max, x_max, array, Aarray)
			##Img2D1 = BmpSmallFromBuffer(Img2D, 1, 1, 1, 255)
			## Load original image into a memory DC
			##memory.SelectObject(Img2D)
			## Continue default loading
			#wx.Image.Rescale(Img2D1,newWidth,newHeight)
			#Img2D2 = wx.BitmapFromImage(Img2D1)
			#dc.DrawBitmap(Img2D2,0,0,False)
			#if USE_BUFFERED_DC:
				#dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
				#self.Draw_Update(dc)
			#else:
				##update the buffer
				#dc = wx.MemoryDC()
				#dc.SelectObject(self._Buffer)
				#self.Draw_Update(dc)
				##update the screen
				#wx.ClientDC(self).DrawBitmap(self._Buffer,0,0)
		#else:
			#trying=1

class Log:
	def WriteText(self, text):
		if text[-1:] == '\n':
			text = text[:-1]
		wx.LogMessage(text)
	write = WriteText


class MainApp(wx.App):
	def OnInit(self):
		wx.Log_SetActiveTarget(wx.LogStderr())
		wx.InitAllImageHandlers()
		frame = MainFrame(None)
		frame.Show(True)
		self.SetTopWindow(frame)
		return True
	
if __name__ == '__main__':
	app = wx.App()
	frame = MyFrame(None)
	frame.Show()
	app.MainLoop() 
