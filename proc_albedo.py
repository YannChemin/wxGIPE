#!/usr/bin/python
# -*- coding: utf-8 -*-

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
swir1chan = ''
swir2chan = ''
swir3chan = ''
swir4chan = ''
swir5chan = ''
swir6chan = ''

# Define output file name
output = ''

# Define vegetation indices types
alb_selected = 'AVHRR'
alb_type = ['AVHRR','Aster','Landsat','Modis']

# Define Info Message
overview = """This calculates the Albedo, that is the Shortwave surface reflectance in the range of 0.3-3 micro-meters. It takes input of individual bands of surface reflectance from Modis, AVHRR, Landsat or Aster and calculates the Albedo for those. This is an precursor to r.sun and any Energy-Balance processing. 

NOTES: It assumes MODIS product surface reflectance in [0;10000]

Input files:
	AVHRR:	self.redband, self.nirband
		
	Aster:	self.greenband, self.redband, self.nirband, 
			self.swirchan1, self.swirchan2, self.swirchan3, 
			self.swirchan4, self.swirchan5, self.swirchan6
	
	Landsat:	self.blueband, self.greenband, self.redband, 
			self.nirband, self.swir1band, self.swir2band
		
	Modis:	self.redchan, self.nirchan, self.swir1band, 
			self.swir2band, self.swir3band, self.swir4band, 
			self.swir5band
	"""

class MyFrame(wx.Frame):
	def __init__(self,parent, id=-1, title='Albedo Processing',
			pos=(0,0),
			size=(400,650),
			style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		self.alb=rs.albedo()
		# Input Filenames
		self.bluechan = bluechan
		self.greenchan = greenchan
		self.redchan = redchan
		self.nirchan = nirchan
		self.swir1chan = swir1chan
		self.swir2chan = swir2chan
		self.swir3chan = swir3chan
		self.swir4chan = swir4chan
		self.swir5chan = swir5chan
		self.swir6chan = swir6chan
		self.output = output
		# Albedo equation types
		self.alb_type = alb_type
		self.alb_selected = alb_selected
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
		self.mbox.Add(self.cc7, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc8, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc9, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc10, 1, wx.EXPAND, 10)
		self.mbox.Add((10,10))
		self.mbox.Add(self.rbox, 1, wx.EXPAND, 0)
		self.mbox.Add((10,10))
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
		
		if(self.alb_selected=='AVHRR'):
			self.result=self.alb.avhrr(self.redband, self.nirband)
				
		if(self.alb_selected=='Aster'):
			if(self.greenchan==''):
				self.OnGreenFileInError()
			else:
				self.greenband = gdal_array.LoadFile(self.greenchan)
				self.result=self.alb.aster(self.greenband, self.redband, self.nirband, self.swirchan1, self.swirchan2, self.swirchan3, self.swirchan4, self.swirchan5, self.swirchan6)
			
		if(self.alb_selected=='Landsat'):
			if(self.bluechan==''):
				self.OnBlueFileInError()
			elif(self.greenchan==''):
				self.OnGreenFileInError()
			elif(self.swir1chan==''):
				self.OnSwir1FileInError()
			elif(self.swir2chan==''):
				self.OnSwir2FileInError()
			else:
				self.blueband = gdal_array.LoadFile(self.bluechan)
				self.greenband = gdal_array.LoadFile(self.greenchan)
				self.swir1band = gdal_array.LoadFile(self.swir1chan)
				self.swir2band = gdal_array.LoadFile(self.swir2chan)
				self.result=self.alb.landsat( self.blueband, self.greenband, self.redband, self.nirband, self.swir1band, self.swir2band )
				
		if(self.alb_selected=='Modis'):
			if(self.swir1chan==''):
				self.OnSwir1FileInError()
			elif(self.swir2chan==''):
				self.OnSwir2FileInError()
			elif(self.swir3chan==''):
				self.OnSwir3FileInError()
			elif(self.swir4chan==''):
				self.OnSwir4FileInError()
			elif(self.swir5chan==''):
				self.OnSwir5FileInError()
			else:
				self.swir1band = gdal_array.LoadFile(self.swir1chan)
				self.swir2band = gdal_array.LoadFile(self.swir2chan)
				self.swir3band = gdal_array.LoadFile(self.swir3chan)
				self.swir4band = gdal_array.LoadFile(self.swir4chan)
				self.swir5band = gdal_array.LoadFile(self.swir5chan)
				self.result=self.alb.modis(self.redchan, self.nirchan, self.swir1band, self.swir2band, self.swir3band, self.swir4band, self.swir5band)

		SaveArrayWithGeo(self.result,self.redchan,self.output,'GTiff')
		self.Destroy()
		
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
	
	def OnSwir1FileInError(self):
		dlg = wx.MessageDialog(self, 
				'Missing first SWIR/MIR Channel file !!!!!!\n (Modis and Aster)\n (Landsat Band 5)',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

	def OnSwir2FileInError(self):
		dlg = wx.MessageDialog(self, 
				'Missing second SWIR/MIR Channel file !!!!!!\n (Modis and Aster)\n (Landsat Band 7)',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
	
	def OnSwir3FileInError(self):
		dlg = wx.MessageDialog(self, 
				'Missing SWIR 3 Channel file !!!!!!\n (Modis and Aster)',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

	def OnSwir4FileInError(self):
		dlg = wx.MessageDialog(self, 
				'Missing SWIR 4 Channel file !!!!!!\n (Modis and Aster)',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
	
	def OnSwir5FileInError(self):
		dlg = wx.MessageDialog(self, 
				'Missing SWIR 5 Channel file !!!!!!\n (Modis and Aster)',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

	def OnSwir6FileInError(self):
		dlg = wx.MessageDialog(self, 
				'Missing SWIR 6 Channel file !!!!!!\n (Only Aster)',
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
			self, -1, size=(50, -1), labelText='SWIR1/chan5:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback4,
		    	)
		self.cc5 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='SWIR2/chan7:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback5
		    	)
		self.cc6 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='SWIR3:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback6
		    	)
		self.cc7 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='SWIR4:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback7
		    	)
		self.cc8 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='SWIR5:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback8
		    	)
		self.cc9 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='SWIR6:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback9
		    	)
		self.cc10 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='OUT File: ',
			startDirectory = self.dirnm,
			fileMask='*.tif',
			fileMode=wx.SAVE,
			changeCallback = self.fbbCallback10
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
		 self.swir1chan = str(evt.GetString())

	def fbbCallback5(self, evt):
		 self.swir2chan = str(evt.GetString())
	
	def fbbCallback6(self, evt):
		 self.swir3chan = str(evt.GetString())
	
	def fbbCallback7(self, evt):
		 self.swir4chan = str(evt.GetString())
	
	def fbbCallback8(self, evt):
		 self.swir5chan = str(evt.GetString())
	
	def fbbCallback9(self, evt):
		 self.swir6chan = str(evt.GetString())
	
	def fbbCallback10(self, evt):
		 self.output = str(evt.GetString())
	# Front text
	def make_text(self):
		self.text = wx.StaticText(self, -1, "This is processing Various Albedo through the use of gdal and numeric")
	# Output format radio buttons
	def make_radiobuttons(self):
		self.rbox = wx.BoxSizer(wx.HORIZONTAL)
		self.rb = wx.RadioBox(self, -1, "Select Output Albedo Type", 
			wx.DefaultPosition, wx.DefaultSize,
			self.alb_type, 4, wx.RA_SPECIFY_COLS)
		self.rb.SetToolTip(wx.ToolTip("Select Output Albedo Type"))
		self.rb.SetLabel("Output Albedo Type")
		self.rbox.Add(self.rb,1,wx.ALL,10)
		
	def EvtRadioBox(self, evt):
		self.nb = evt.GetInt()
		self.alb_selected = self.alb_type[self.nb]
		print self.alb_selected

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
