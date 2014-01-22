#!/usr/bin/python
# -*- coding: utf-8 -*-

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


global infiles
global output
global gdal_in_format
global out_format

infiles = []
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
		global infiles
		self.output = output
		global gdal_in_format
		self.out_format = out_format
		self.make_text()
		self.make_buttons()
		self.make_radiobuttons()
		self.make_fb()
		self.mbox = wx.BoxSizer(wx.VERTICAL)
		self.mbox.Add((10,10))
		self.mbox.Add(self.text, 1, wx.EXPAND|wx.CENTER, 10)
		self.mbox.Add((10,10))
		self.mbox1 = wx.BoxSizer(wx.HORIZONTAL)
		self.mbox1.Add(self.text1, 1, wx.CENTER, 10)
		self.mbox1.Add(self.cc0, 1, wx.CENTER, 10)
		self.mbox.Add(self.mbox1, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc1, 1, wx.EXPAND, 10)
		self.mbox.Add((10,10))
		self.mbox.Add(self.rbox, 1, wx.EXPAND, 0)
		self.mbox.Add((10,200))
		self.mbox.Add(self.bbox, 1, wx.CENTER, 0)
		self.SetSizer(self.mbox)
		self.bindEvents()
	
	# Process Equations, Handling and saving of output
	def OnOK(self,event):
		#print "*******: ",self.src_flnm, " ",self.output," ", self.out_format
		CrAr(self.src_flnm,self.output,self.out_format)
		self.Destroy()

	def OnSelectIn(self,event):
		dlg = wx.FileDialog(self, message="Select files to Stack",
					defaultDir=os.getcwd(),defaultFile="",
					wildcard="*.*",
					style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
					)
		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			infiles = paths
			#print paths
			self.src_flnm = []
			#for path in paths:
				#print path
			for infile in infiles:
				#print "infile:",infile
				self.src_flnm.append(infile)
				#print "src_flnm:",self.src_flnm
		dlg.Destroy()

	# Path+filename seek and set
	def make_fb(self):
		# get current working directory
		self.dirnm = os.getcwd()
		self.cc0 = wx.Button(self, -1, " Browse ", (50,50))
		self.cc1 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='OUT File: ',
			startDirectory = self.dirnm,
			fileMask=out_format,
			fileMode=wx.SAVE,
			changeCallback = self.fbbCallback1
			)
	# Collect path+filenames
	def fbbCallback1(self, evt):
		 self.output = evt.GetString()
		 #print "output: ", self.output
	
	# Front text
	def make_text(self):
		self.text = wx.StaticText(self, -1, "This is layer stack for 3 bands through the use of gdal and numeric")
		self.text1 = wx.StaticText(self, -1, " Select Input Files ")
	# Output format radio buttons
	def make_radiobuttons(self):
		self.rbox = wx.BoxSizer(wx.HORIZONTAL)
		self.rb = wx.RadioBox(self, -1, "Select Output Format", 
			wx.DefaultPosition, wx.DefaultSize,
			gdal_in_format, 4, wx.RA_SPECIFY_COLS)
		self.rb.SetToolTip(wx.ToolTip("Select Output Format"))
		self.rb.SetLabel("Output Format")
		self.rbox.Add(self.rb,1,wx.ALL,10)
		
	def EvtRadioBox(self, evt):
		self.nb = evt.GetInt()
		self.out_format = gdal_in_format[self.nb]
		print self.out_format

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
		self.Bind(wx.EVT_BUTTON, self.OnSelectIn, self.cc0)
		
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

	def CrAr( self, src_flnm, dst_flnm, format ):
		cr_opts=[]
		#print "dst_flnm = ",dst_flnm
		# Read information from source file.
		src_ds = gdal.Open(src_flnm[0])
		gt = src_ds.GetGeoTransform()
		pj = src_ds.GetProjection()
		src_ds = None
		# Standard checking on the GDAL driver
		Driver = gdal.GetDriverByName( format )
		if Driver is None:
			raise ValueError, "CrAr: No DriverFound "+format
		DriverMTD = Driver.GetMetadata()
		if not DriverMTD.has_key('DCAP_CREATE'):
			print 'Format Driver %s does not support creation and piecewise writing.\nPlease select a format that does, such as GTiff or HFA (Erdas/Imagine).' % format
			sys.exit( 1 )	
		# Set up the band number
		nbands = len(src_flnm)
		print "nbands =", nbands
		# Collect information on source files
		flinfos = g_m.names_to_fileinfos( src_flnm )
		ulx = flinfos[0].ulx
		uly = flinfos[0].uly
		lrx = flinfos[0].lrx
		lry = flinfos[0].lry
		# get largest extends
		for fi in flinfos:
			ulx = min(ulx, fi.ulx)
			uly = max(uly, fi.uly)
			lrx = max(lrx, fi.lrx)
			lry = min(lry, fi.lry)
		# Set other info
		psize_x = flinfos[0].geotransform[1]	
		psize_y = flinfos[0].geotransform[5]
		band_type = flinfos[0].band_type
		# Try opening as an existing file
		gdal.PushErrorHandler( 'CPLQuietErrorHandler' )
		out_fh = gdal.Open( dst_flnm, gdal.GA_Update )
		gdal.PopErrorHandler()
		# Otherwise create a new file
		if out_fh is None:
			geot = [ulx, psize_x, 0, uly, 0, psize_y]
			print geot[0], geot[1], geot[2], geot[3], geot[4]
			xsize = int((lrx-ulx)/geot[1]+0.5)
			ysize = int((lry-uly)/geot[5]+0.5)
			out_fh=Driver.Create(dst_flnm,xsize,ysize,nbands,band_type,cr_opts)
			if out_fh is None:
				print ValueError, "CrAr: Failed to create new file ",dst_flnm
				sys.exit( 1 )
		out_fh.SetGeoTransform( gt )
		out_fh.SetProjection( pj )
		out_fh.GetRasterBand(1).SetRasterColorTable(flinfos[0].ct)
		iband = 1
		for fi in flinfos:
			fi.copy_into( out_fh, 1, iband, nodata )
			iband=iband+1
		iband = 0

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
