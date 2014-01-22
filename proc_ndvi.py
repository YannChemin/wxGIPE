# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Vegetation Indices Image Processing functions for wxGIPE
# Purpose:  Satellite image processing of Vegetation Indices
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

import wx
import wx.lib.filebrowsebutton as filebrowse
import os

# For Image Processing
import numpy
from osgeo import gdalnumeric
from osgeo import gdal
from osgeo import gdal_array
import gdal_merge as g_m
from GDAL_functions import *

# For icons, pngs, etc coming from images.py
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO
import images

# Get Remote Sensing functions
from RS import *

# Define satellite bands
# Based on Landsat channels
bluechan = ''
greenchan = ''
redchan = ''
nirchan = ''
chan5chan = ''
chan7chan = ''

# Define output file name
output = ''

# Define vegetation indices types
vi_selected = 'NDVI'
vi_type = ['ARVI','DVI','GARI','GEMI','GVI','IPVI','MSAVI','MSAVI2','NDVI','PVI','RVI','SAVI','WDVI']

# Define input var for WDVI
soil_line_slope = 1.0

# Define Info Message
overview = """Vegetation Index Processing.

Calculates vegetation indices based on biophysical parameters. 
1. ARVI: atmospherically resistant vegetation indices
2. DVI: Difference Vegetation Index
3: GARI: Green atmospherically resistant vegetation index
4: GEMI: Global Environmental Monitoring Index
5: GVI: Green Vegetation Index
6: IPVI: Infrared Percentage Vegetation Index
7: MSAVI: Modified Soil Adjusted Vegetation Index
8: MSAVI2: second Modified Soil Adjusted Vegetation Index
9: NDVI: Normalized Difference Vegetation Index
10:PVI: Perpendicular Vegetation Index
11:RVI: ratio vegetation index:
12:SAVI: Soil Adjusted Vegetation Index  
13:WDVI: Weighted Difference Vegetation Index

NDVI 
Data Type Band Numbers ([IR, Red]) 
TM Bands= [4, 3] 
MSS Bands = [7, 5] 
AVHRR Bands = [2, 1] 
SPOT XS Bands = [3, 2] 
AVIRIS Bands = [51, 29] 

(AVHRR) NDVI = (channel 2 - channel 1) / (channel 2 + channel 1)

Originally from kepler.gps.caltech.edu
A FAQ on Vegetation in Remote Sensing 
Written by Terrill W. Ray
	   Div. of Geological and Planetary Sciences
	   California Institute of Technology
email: terrill@mars1.gps.caltech.edu"""

class MyFrame(wx.Frame):
	def __init__(self,parent, id=-1, title='Vegetation Indices Processing',
			pos=(0,0),
			size=(400,500),
			style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		self.vi=rs.vi()
		# Input Filenames
		self.bluechan = bluechan
		self.greenchan = greenchan
		self.redchan = redchan
		self.nirchan = nirchan
		self.chan5chan = chan5chan
		self.chan7chan = chan7chan
		self.output = output
		# VI types
		self.vi_type = vi_type
		self.vi_selected = vi_selected
		# WDVI input var
		self.soil_line_slope=soil_line_slope
		# Construct Interface
		self.make_text()
		self.make_buttons()
		self.make_radiobuttons()
		self.make_fb()
		self.mbox = wx.BoxSizer(wx.VERTICAL)
		self.mbox.Add((10,10))
		self.mbox.Add(self.text, 1, wx.EXPAND|wx.CENTER, 10)
		self.mbox.Add((10,10))
		self.mbox.Add((10,10))
		self.mbox.Add(self.cc0, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc1, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc2, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc3, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc4, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc5, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc6, 1, wx.EXPAND, 10)
		self.mbox.Add((10,10))
		self.mbox.Add(self.rbox, 1, wx.EXPAND, 0)
		self.mbox.Add((10,80))
		self.mbox.Add((10,10))
		self.mbox.Add(self.bbox, 1, wx.CENTER, 10)
		self.mbox.Add((10,10))
		self.SetSizer(self.mbox)
		self.bindEvents()
	
	# Process Equations, Handling and saving of output
	def OnOK(self,event):
		print "red: ", self.redchan, " nir:",self.nirchan, " out:", self.output
		if(self.redchan==''):
			self.OnFileInError()
		elif(self.nirchan==''):
			self.OnFileInError()
		else:
			self.redband = gdal_array.LoadFile(self.redchan)
			self.nirband = gdal_array.LoadFile(self.nirchan)
		# ARVI
		if(self.vi_selected=='ARVI'):
			if(self.bluechan==''):
				self.OnBlueFileInError()
			else:
				self.blueband = gdal_array.LoadFile(self.bluechan)
				self.result=self.vi.arvi(self.redband, self.nirband, self.blueband)
		# DVI	
		if(self.vi_selected=='DVI'):
			self.result=self.vi.dvi(self.redband, self.nirband)
		# GARI
		if(self.vi_selected=='GARI'):
			if(self.bluechan==''):
				self.OnBlueFileInError()
			elif(self.greenchan==''):
				self.OnGreenFileInError()
			else:
				self.blueband = gdal_array.LoadFile(self.bluechan)
				self.greenband = gdal_array.LoadFile(self.greenchan)
				self.result=self.vi.gari(self.redband, self.nirband, self.blueband, self.greenband)
		# GEMI	
		if(self.vi_selected=='GEMI'):
			self.result=self.vi.gemi(self.redband, self.nirband)
		# GVI
		if(self.vi_selected=='GVI'):
			if(self.bluechan==''):
				self.OnBlueFileInError()
			elif(self.greenchan==''):
				self.OnGreenFileInError()
			elif(self.chan5chan==''):
				self.OnChan5FileInError()
			elif(self.chan7chan==''):
				self.OnChan7FileInError()
			else:
				self.blueband = gdal_array.LoadFile(self.bluechan)
				self.greenband = gdal_array.LoadFile(self.greenchan)
				self.chan5band = gdal_array.LoadFile(self.chan5chan)
				self.chan7band = gdal_array.LoadFile(self.chan7chan)
				self.result=self.vi.gvi(self.blueband,self.greenband,self.redband, self.nirband,self.chan5band,self.chan7band)
		# IPVI
		if(self.vi_selected=='IPVI'):
			self.result=self.vi.ipvi(self.redband, self.nirband)
		# MSAVI
		if(self.vi_selected=='MSAVI'):
			self.result=self.vi.msavi(self.redband, self.nirband)
		# MSAVI2
		if(self.vi_selected=='MSAVI2'):
			self.result=self.vi.msavi2(self.redband, self.nirband)
		# NDVI
		if(self.vi_selected=='NDVI'):
			self.result=self.vi.ndvi(self.redband, self.nirband)
		# PVI
		if(self.vi_selected=='PVI'):
			self.result=self.vi.pvi(self.redband, self.nirband)
		# RVI
		if(self.vi_selected=='RVI'):
			self.result=self.vi.rvi(self.redband, self.nirband)
		# SAVI
		if(self.vi_selected=='SAVI'):
			self.result=self.vi.savi(self.redband, self.nirband)
		# WDVI
		if(self.vi_selected=='WDVI'):
			self.OnSelectSoilLineSlope()
			self.result=self.vi.wdvi(self.redband, self.nirband, self.soil_line_slope)

		SaveArrayWithGeo(self.result,self.redchan,self.output,'GTiff')
		self.Destroy()
	
	def OnSelectSoilLineSlope(self):
		dlg = wx.SingleChoiceDialog(
			self, 'Soil Line Slope Choice', 'Choose Soil Line Slope for WDVI', [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 3.0, 4.0, 5.0],wx.CHOICEDLG_STYLE)
		if dlg.ShowModal() == wx.ID_OK:
			self.soil_line_slope = dlg.GetStringSelection()
		dlg.Destroy()
	
	def OnFileInError(self):
		dlg = wx.MessageDialog(self, 
				'Minimum files to add:\n\n  Input files => Red and NIR\n  One Output file',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		
	def OnBlueFileInError(self):
		dlg = wx.MessageDialog(self, 
				'Missing Blue Channel file !!!!!!',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

	def OnGreenFileInError(self):
		dlg = wx.MessageDialog(self, 
				'Missing Green Channel file !!!!!!',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

	# Path+filename seek and set
	def make_fb(self):
		# get current working directory
		self.dirnm = os.getcwd()
		self.cc0 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='Blue:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback0,
		    	)
		self.cc1 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='Green:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback1
		    	)
		self.cc2 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='RED:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback2,
		    	)
		self.cc3 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='NIR:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback3
		    	)
		self.cc4 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='chan5:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback4,
		    	)
		self.cc5 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='chan7:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback5
		    	)
		self.cc6 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='OUT File: ',
			startDirectory = self.dirnm,
			fileMask='*.tif',
			fileMode=wx.SAVE,
			changeCallback = self.fbbCallback6
		    	)
	# Collect path+filenames
	def fbbCallback0(self, evt):
		 self.bluechan = str(evt.GetString())
	
	def fbbCallback1(self, evt):
		 self.greenchan = str(evt.GetString())

	def fbbCallback2(self, evt):
		 self.redchan = str(evt.GetString())
	
	def fbbCallback3(self, evt):
		 self.nirchan = str(evt.GetString())
	
	def fbbCallback4(self, evt):
		 self.chan5chan = str(evt.GetString())

	def fbbCallback5(self, evt):
		 self.chan7chan = str(evt.GetString())
	
	def fbbCallback6(self, evt):
		 self.output = str(evt.GetString())
		# Front text
	def make_text(self):
		self.text = wx.StaticText(self, -1, "This is processing Various VI through the use of gdal and numeric")
	# Output format radio buttons
	def make_radiobuttons(self):
		self.rbox = wx.BoxSizer(wx.HORIZONTAL)
		self.rb = wx.RadioBox(self, -1, "Select Output VI Type", 
			wx.DefaultPosition, wx.DefaultSize,
			self.vi_type, 5, wx.RA_SPECIFY_COLS)
		self.rb.SetToolTip(wx.ToolTip("Select Output VI Type"))
		self.rb.SetLabel("Output VI Type")
		self.rbox.Add(self.rb,1,wx.ALL,10)
		
	def EvtRadioBox(self, evt):
		self.nb = evt.GetInt()
		self.vi_selected = self.vi_type[self.nb]
		print self.vi_selected

	# Bottom buttons	
	def make_buttons(self):
		self.bbox = wx.BoxSizer(wx.HORIZONTAL)
		# OnOK
		bmp0 = images.getPngDialogOKBitmap()
		self.b0 = wx.BitmapButton(self, 20, bmp0, (20, 20),
                       (bmp0.GetWidth()+50, bmp0.GetHeight()+10), style=wx.NO_BORDER)
        	self.b0.SetToolTipString("Process")
		self.bbox.Add(self.b0,1,wx.CENTER,10)
		# OnCancel
		bmp1 = images.getPngDialogCancelBitmap()
		self.b1 = wx.BitmapButton(self, 30, bmp1, (20, 20),
                       (bmp1.GetWidth()+50, bmp1.GetHeight()+10), style=wx.NO_BORDER)
		self.b1.SetToolTipString("Abort")
		self.bbox.Add(self.b1,1,wx.CENTER,10)
		# OnInfo 
		bmp2 = images.getPngHelpAboutBitmap()
		self.b2 = wx.BitmapButton(self, 40, bmp2, (20, 20),
                       (bmp2.GetWidth()+50, bmp2.GetHeight()+10), style=wx.NO_BORDER)
        	self.b2.SetToolTipString("Help/Info.")
		self.bbox.Add(self.b2,1,wx.CENTER,10)

	def bindEvents(self):
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        	self.Bind(wx.EVT_BUTTON, self.OnOK, self.b0)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.b1)
		self.Bind(wx.EVT_BUTTON, self.OnInfo, self.b2)
		self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.rb)
		
	def OnCloseWindow(self, event):
		self.Destroy()

	def OnCancel(self, event):
		self.Destroy()
	
	def OnInfo(self,event):
		dlg = wx.MessageDialog(self, overview,
			'Help', wx.OK | wx.ICON_INFORMATION
			)
		dlg.ShowModal()
		dlg.Destroy()

class MainApp(wx.App):
	def OnInit(self):
		frame = MainFrame(None)
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

if __name__ == '__main__':
	app = wx.App()
	frame = MyFrame(None)
	frame.Show()
	app.MainLoop()
