#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.lib.filebrowsebutton as filebrowse
import os

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

# Get Remote Sensing functions
from RS import *

#Define metadata list
metadata = []

# Define satellite bands
inputFile = []

# Define output base file name
output = ''

# Define output format
out_format = 'GTiff'
gdal_in_format = ['AAIGrid', 'BMP', 'BT', 'DTED', 'EHdr', 'ELAS', 'ENVI', 'FIT', 'GIF', 'GMT', 'GTiff', 'HDF4Image', 'HFA', 'IDA', 'ILWIS', 'JPEG', 'JPEG2000', 'MEM', 'MFF', 'MFF2', 'NITF', 'netCDF', 'PAux', 'PCIDSK', 'PCRaster', 'PNG',  'PNM', 'RMF', 'RST', 'USGSDEM', 'VRT', 'XPM']

# Define Info Message
overview = """
Warps MODIS HDF to any format of GDAL writer and in latlong/wgs84/wgs84, inspired from Markus Neteler's shell script.
EPSG:4326: +proj=latlong +ellps=wgs84 +datum=wgs84 +no_defs
"""

class MyFrame(wx.Frame):
	def __init__(self,parent, id=-1, title='Import HDF into LatLong (+default to GeoTiff)',
			pos=(0,0),
			size=(450,500),
			style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		self.metadata = metadata
		# Input Filenames
		self.inputFile = inputFile
		self.output = output
		self.gdal_in_format = gdal_in_format
		self.out_format = out_format
		# Construct Interface
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
		self.mbox.Add((10,10))
		self.mbox.Add(self.rbox, 1, wx.EXPAND, 0)
		self.mbox.Add((10,200))
		self.mbox.Add(self.bbox, 1, wx.CENTER, 0)
		self.mbox.Add((10,10))
		self.SetSizer(self.mbox)
		self.bindEvents()
	
	# Process Equations, Handling and saving of output
	def OnOK(self,event):
		print "in: ", self.inputFile, " out:", self.output, " type:", self.out_format
		ext = file_ext_type(self.out_format)
		if(self.inputFile==''):
			self.OnFileInError()
		if(self.output==''):
			print "will take care of the output names then"
		else:
			pass
		img=gdal.Open(self.inputFile)
		infiles = img.GetMetadata("SUBDATASETS")
		for filename in infiles:
			system_cmd = "gdalwarp -of "+self.out_format+" -t_srs \"+proj=latlong +ellps=sphere\" "+filename+" "+filename+".tmp"+ext
			wx.Execute(system_cmd, True)
			system_cmd = "gdal_translate -of "+self.out_format+" -a_srs \"EPSG:4326\" -co COMPRESS=YES "+filename+".tmp"+ext+" "+filename+ext+" ; rm -f "+filename+".tmp"+ext
			wx.Execute(system_cmd, True)
			#imgAr = LoadFile(line)
			#img = gdal.Open(line)
			#gt = img.GetGeoTransform()
			#pj = img.GetProjection()
			#mtd = img.GetMetadata()
			#dsc = img.GetDescription()
			#print pj, "\n", gt, "\n", mtd, "\n", dsc
			#del img #Free Memory
			#src_ds = OpenArray( imgAr )
			#src_ds.SetGeoTransform( gt )
			#src_ds.SetProjection( pj )
			#src_ds.SetMetadata(mtd)
			#src_ds.SetDescription(dsc)
			#driver = gdal.GetDriverByName( self.out_format )
			#driver.CreateCopy( self.output, src_ds )
			#del src_ds #Free Memory
		self.Destroy()
	
	def OnFileInError(self):
		dlg = wx.MessageDialog(self, 
				'Minimum files to add:\n\n  Input file => .hdf\n  Empty Output file to be taken care of by the program',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		
	# Path+filename seek and set
	def make_fb(self):
		# get current working directory
		self.dirnm = os.getcwd()
		self.cc0 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='in File:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback0,
		    	)
		self.cc1 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='out File: ',
			startDirectory = self.dirnm,
			fileMask='*.tif',
			fileMode=wx.SAVE,
			changeCallback = self.fbbCallback1
		    	)
	# Collect path+filenames
	def fbbCallback0(self, evt):
		 self.inputFile = evt.GetString()
	
	def fbbCallback1(self, evt):
		 self.output = evt.GetString()
		# Front text
	def make_text(self):
		self.text = wx.StaticText(self, -1, "Convert HDF into another format using gdal and numeric")
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
