#!/usr/bin/python

import wx
import wx.lib.filebrowsebutton as filebrowse
import os, sys

# For Image Processing
import numpy
from osgeo import gdalnumeric
from osgeo import gdal
import gdal_merge as g_m
from GDAL_functions import *

# For icons, pngs, etc coming from images.py
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO
import images


infile1 = ''
infile2 = ''
infile3 = ''
output = ''
nodata = None
out_format = 'GTiff'
gdal_in_format = ['AAIGrid', 'BMP', 'BT', 'DTED', 'EHdr', 'ELAS', 'ENVI', 'FIT', 'GIF', 'GMT', 'GTiff', 'HDF4Image', 'HFA', 'IDA', 'ILWIS', 'JPEG', 'JPEG2000', 'MEM', 'MFF', 'MFF2', 'NITF', 'netCDF', 'PAux', 'PCIDSK', 'PCRaster', 'PNG',  'PNM', 'RMF', 'RST', 'USGSDEM', 'VRT', 'XPM']

overview = """<html><body>
<h2><center>Convert GeoImage</center></h2>

Layer Stack various GeoImage bands into one image file using GDAL 

</body></html>
"""

class MyFrame(wx.Frame):
	def __init__(self,parent, id=-1, title='Layer Stack: 3 Bands to RGB', pos=(0,0),
			size=(450,600),
			style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		self.infile1 = infile1
		self.infile2 = infile2
		self.infile3 = infile3
		self.output = output
		self.gdal_in_format = gdal_in_format
		self.out_format = out_format
		self.make_text()
		self.make_buttons()
		self.make_radiobuttons()
		self.make_fb()
		self.mbox = wx.BoxSizer(wx.VERTICAL)
		self.mbox.Add((10,10))
		self.mbox.Add(self.text, 1, wx.EXPAND|wx.CENTER, 10)
		self.mbox.Add((10,10))
		self.mbox.Add(self.cc0, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc1, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc2, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc3, 1, wx.EXPAND, 10)
		self.mbox.Add((10,10))
		self.mbox.Add(self.rbox, 1, wx.EXPAND, 0)
		self.mbox.Add((10,200))
		self.mbox.Add(self.bbox, 1, wx.CENTER, 0)
		self.SetSizer(self.mbox)
		self.bindEvents()
	
	# Process Equations, Handling and saving of output
	def OnOK(self,event):
		print self.infile1, "", self.infile2, "", self.infile3, "", self.output, "", self.out_format
		self.src_flnm = [self.infile1, self.infile2, self.infile3, ]
		CrAr(self.src_flnm,self.output,self.out_format)
		self.Destroy()

	# Path+filename seek and set
	def make_fb(self):
		# get current working directory
		self.dirnm = os.getcwd()
		self.cc0 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='IN File R: ',
			startDirectory = self.dirnm,
			changeCallback = self.fbbCallback0,
			fileMode = wx.MULTIPLE | wx.OPEN
			)
		self.cc1 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='IN File G: ',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback1
			)
		self.cc2 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='IN File B: ',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback2
			)
		self.cc3 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='OUT File: ',
			startDirectory = self.dirnm,
			fileMask='*.tif',
			fileMode=wx.SAVE,
			changeCallback = self.fbbCallback3
			)
	# Collect path+filenames
	def fbbCallback0(self, evt):
		 self.infile1 = evt.GetString()
		 print "infile1: ", self.infile1
	
	def fbbCallback1(self, evt):
		 self.infile2 = evt.GetString()
		 print "infile1: ", self.infile2
	
	def fbbCallback2(self, evt):
		 self.infile3 = evt.GetString()
		 print "infile2: ", self.infile3
	
	def fbbCallback3(self, evt):
		 self.output = evt.GetString()
		 print "outfile: ", self.output
	# Front text
	def make_text(self):
		self.text = wx.StaticText(self, -1, "This is layer stack for 3 bands through the use of gdal and numeric")
	# Output format radio buttons
	def make_radiobuttons(self):
		self.rbox = wx.BoxSizer(wx.HORIZONTAL)
		self.rb = wx.RadioBox(self, -1, "Select Output Format", 
			wx.DefaultPosition, wx.DefaultSize,
			self.gdal_in_format, 4, wx.RA_SPECIFY_COLS)
		self.rb.SetToolTip(wx.ToolTip("Select Output Format"))
		self.rb.SetLabel("Output Format")
		self.rbox.Add(self.rb,1,wx.ALL,10)
		
	def EvtRadioBox(self, evt):
		self.nb = evt.GetInt()
		out_format = gdal_in_format[self.nb]
		print out_format

	# Bottom buttons	
	def make_buttons(self):
		self.bbox = wx.BoxSizer(wx.HORIZONTAL)
		# OnOK
		bmp0 = wx.Bitmap("icons/dialog-ok-apply.png", wx.BITMAP_TYPE_PNG)
		self.b0 = wx.BitmapButton(self, 20, bmp0, (20, 20),
                       (bmp0.GetWidth()+50, bmp0.GetHeight()+10), style=wx.NO_BORDER)
        	self.b0.SetToolTipString("Process")
		self.bbox.Add(self.b0,1,wx.CENTER,10)
		# OnCancel
		bmp1 = wx.Bitmap("icons/dialog-cancel.png", wx.BITMAP_TYPE_PNG)
		self.b1 = wx.BitmapButton(self, 30, bmp1, (20, 20),
                       (bmp1.GetWidth()+50, bmp1.GetHeight()+10), style=wx.NO_BORDER)
		self.b1.SetToolTipString("Abort")
		self.bbox.Add(self.b1,1,wx.CENTER,10)
		# OnInfo 
		bmp2 = wx.Bitmap("icons/help-about.png", wx.BITMAP_TYPE_PNG)
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
