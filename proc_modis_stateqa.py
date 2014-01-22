###############################################################################
# $Id$
#
# Project:  Sub1 project of IRRI
# Purpose:  State Quality Assessment extraction from MODIS09A (500m)
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
import numpy as N
from osgeo import gdalnumeric
from osgeo import gdal
from osgeo import gdal_array
from osgeo.gdalconst import *

# For icons, pngs, etc coming from images.py
from wx import ImageFromStream, BitmapFromImage, EmptyIcon
import cStringIO
import images

# Define satellite bands
# Based on Landsat channels
qc = ''

# Define output file name
output = ''

# Define list of QA types
NameQC = ['cloud_state','cloud_shadow','land_water_flag','aerosol_quantity','cirrus_detected','internal_cloud_alg_flag','internal_fire_alg_flag','MOD35_snow_ice_flag','pixel_adjacent_to_cloud','brdf_correction','internal_snow_mask']


# Define Info Message
overview = """MODIS State Quality Assessment Extractor

Makes Human-readable images of State Quality Assessment binary bits from MOD09A 500m products (Vermote et al., 2008), this is the proper place to find cloud related information.
Vermote E.F., Kotchenova S.Y., Ray J.P. MODIS Surface Reflectance User's Guide. Version 1.2. June 2008. MODIS Land Surface Reflectance Science Computing Facility. Homepage

Cloud State unsigned int bits[0-1]
[00]= class 0: clear
[01]= class 1: cloudy
[10]= class 2: mixed
[11]= class 3: not set, assumed clear

Cloud shadow unsigned int bits[2]
[0]= class 0: yes
[1]= class 1: no

Land/Water Flag unsigned int bits[3-5]
[000]= class 0: Shallow ocean
[001]= class 1: Land
[010]= class 2: Ocean coastlines and lake shorelines
[011]= class 3: Shallow inland water
[100]= class 4: Ephemeral water
[101]= class 5: Deep inland water
[110]= class 6: Continental/moderate ocean
[111]= class 7: Deep ocean

Aerosol Quantity unsigned int bits[6-7]
[00]= class 0: Climatology
[01]= class 1: Low
[10]= class 2: Average
[11]= class 3: High

Cirrus detected unsigned int bits[8-9]
[00]= class 0: None
[01]= class 1: Small
[10]= class 2: Average
[11]= class 3: High

Internal Cloud Algorithm Flag unsigned int bits[10]
[0]= class 0: Cloud
[1]= class 1: No cloud

Internal Fire Algorithm Flag unsigned int bits[11]
[0]= class 0: Fire
[1]= class 1: No fire

MOD35 snow/ice flag unsigned int bits [12]
[0]= class 0: Yes
[1]= class 1: No

Pixel adjacent to cloud unsigned int bits[13]
[0]= class 0: Yes
[1]= class 1: No

BRDF correction performed unsigned int bits[14]
[0]= class 0: Yes
[1]= class 1: No

Internal Snow Mask unsigned int bits[15]
[0]= class 0: Snow
[1]= class 1: No snow

"""

class MyFrame(wx.Frame):
	def __init__(self,parent, id=-1, title='MODIS09A State Quality Bits Extractor',
			pos=(0,0),
			size=(500,650),
			style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		# Input Filenames
		self.qc = qc
		self.qc_type = 'cloud_state'
		self.NameQC = NameQC
		self.output = output
		# Construct Interface
		self.make_text()
		self.make_buttons()
		self.make_radiobuttons3()
		self.make_fb()
		self.mbox = wx.BoxSizer(wx.VERTICAL)
		self.mbox.Add(self.text, 1, wx.EXPAND|wx.CENTER, 0)
		self.mbox.Add(self.cc2, 1, wx.EXPAND, 0)
		self.mbox.Add(self.cc6, 1, wx.EXPAND, 0)
		self.mbox.Add(self.rbox3, 1, wx.EXPAND, 0)
		self.mbox.Add(self.bbox, 1, wx.CENTER|wx.BOTTOM, -50)
		self.SetSizer(self.mbox)
		self.bindEvents()

	# Process Equations, Handling and saving of output
	def OnOK(self,event):
		#print "qc: ", self.qc
		#print "out:", self.output
		if(self.qc==''):
			self.OnFileInError()
		else:
			self.qcF = gdal.Open(self.qc)
			self.bqc = self.qcF.GetRasterBand(1)
			self.test = gdal.Open(self.qc)
			self.CrAr( self.qc, self.output, 'GTiff' )
			self.result = gdal.Open(self.output, GA_Update)
			for self.y in range(self.bqc.YSize - 1, -1, -1):
				print self.y
				self.scanline1=self.bqc.ReadAsArray(0, self.y, self.bqc.XSize, 1, self.bqc.XSize, 1)
				for self.x in range(0, self.bqc.XSize - 1, 1):
					self.pix1 = self.scanline1[0][self.x]
					self.scanline1[0][self.x]=self.qcbits(self.pix1,self.qc_type)
				self.result.GetRasterBand(1).WriteArray(N.reshape(self.scanline1,(1,self.bqc.XSize)), 0, self.y)
		self.Destroy()
	
	#def bin(self,i):
		#"""
		#Convert Binary to Integer Bit Field
		#Manish Jethani (manish.j at gmx.net)
		#http://bytes.com/forum/thread20381.html
		#"""
		#b = ''
		#while i > 0:
			#j = i & 1
			#b = str(j) + b
			#i >>= 1
		#return b
	
	def qcbits(self,qcbit,qcflag):
		outclas = 0
		if (qcflag=="cloud_state"):
			#calculate cloud state
			outclas = self.stateqa500a(qcbit)
		elif (qcflag=="cloud_shadow"):
			#calculate cloud shadow 
			outclas = self.stateqa500b(qcbit)
		elif (qcflag=="land_water_flag"): 
			#calculate land/water flag 
			outclas = self.stateqa500c(qcbit)
		elif (qcflag, "aerosol_quantity"): 
			#calculate aerosol quantity
			outclas = self.stateqa500d(qcbit)
		elif (qcflag, "cirrus_detected"): 
			#calculate cirrus detected flag 
			outclas = self.stateqa500e(qcbit)
		elif (qcflag, "internal_cloud_alg_flag"):
			#calculate internal cloud algorithm flag 
			outclas = self.stateqa500f(qcbit)
		elif (qcflag, "internal_fire_alg_flag"):
			#calculate internal fire algorithm flag 
			outclas = self.stateqa500g(qcbit)
		elif (qcflag, "mod35_snow_ice_flag"):
			#calculate MOD35 snow/ice flag
			outclas = self.stateqa500h(qcbit)
		elif (qcflag, "pixel_adjacent_to_cloud"):
			#calculate pixel is adjacent to cloud flag 
			outclas = self.stateqa500i(qcbit)
		elif (qcflag=="brdf_correction"):
			#calculate BRDF correction performed flag 
			outclas = self.stateqa500j(qcbit)
		elif (qcflag=="internal_snow_mask"):
			#calculate internal snow mask flag 
			outclas = self.stateqa500k(qcbit)
		else:
			# Signal user that the flag name is badly written  
			# therefore not understood by the application  
			print "Unknown flag name, please check spelling"
			self.OnQCInError()
		return outclas
	
	def stateqa500a(self, pixel):
		"""
	Cloud State unsigned int bits[0-1]
00 -> class 0: clear
01 -> class 1: cloudy
10 -> class 2: mixed
11 -> class 3: not set, assumed clear
	"""
		pixel = pixel & 3
		return pixel
	
	def stateqa500b(self, pixel):
		"""
cloud shadow unsigned int bits[2]
0 -> class 0: yes
1 -> class 1: no
	"""
		pixel >> 2
		pixel = pixel & 1
		return pixel
	
	
	def stateqa500c(self,pixel):
		"""
		LAND/WATER FLAG unsigned int bits[3-5]
000 -> class 0: Shallow ocean
001 -> class 1: Land
010 -> class 2: Ocean coastlines and lake shorelines
011 -> class 3: Shallow inland water
100 -> class 4: Ephemeral water
101 -> class 5: Deep inland water
110 -> class 6: Continental/moderate ocean
111 -> class 7: Deep ocean
	"""
		pixel >> 3
		pixel = pixel & 7
		return pixel
	
	def stateqa500d(self, pixel):
		"""
		AEROSOL QUANTITY unsigned int bits[6-7]
00 -> class 0: Climatology
01 -> class 1: Low
10 -> class 2: Average
11 -> class 3: High
	"""
		pixel >> 6
		pixel = pixel & 3
		return pixel
	
	def stateqa500e(self,pixel):
		"""
	CIRRUS DETECTED unsigned int bits[8-9]
00 -> class 0: None
01 -> class 1: Small
10 -> class 2: Average
11 -> class 3: High
	"""
		pixel >> 8
		pixel = pixel & 3
		return pixel
	
	def stateqa500f(self,pixel):
		"""
		Internal Cloud Algorithm Flag unsigned int bits[10]
0 -> class 0: Cloud
1 -> class 1: No cloud
	"""
		pixel >> 10
		pixel = pixel & 1
		return pixel
	
	def stateqa500g(self,pixel):
		"""
		Internal Fire Algorithm Flag unsigned int bits[11]
0 -> class 0: Fire 
1 -> class 1: No fire
	"""
		pixel >> 11
		pixel = pixel & 1
		return pixel

	def stateqa500h(self,pixel,bandno):
		"""
		MOD35 snow/ice flag unsigned int bits [12]
0 -> class 0: Yes
1 -> class 1: No
	"""
		pixel >> 12
		pixel = pixel & 1
		return pixel
	
	def stateqa500i(self,pixel):
		"""
		Pixel adjacent to cloud unsigned int bits[13]
0 -> class 0: Yes
1 -> class 1: No
	"""
		pixel >> 13
		pixel = pixel & 1
		return pixel
	
	def stateqa500j(self,pixel):
		"""
		BRDF correction performed unsigned int bits[14]
0 -> class 0: Yes
1 -> class 1: No
	"""
		pixel >> 14
		pixel = pixel & 1
		return pixel
	
	def stateqa500k(self,pixel):
		"""
		Internal Snow Mask unsigned int bits[15]
0 -> class 0: Snow
1 -> class 1: No snow
 	"""
		pixel >> 15
		pixel = pixel & 1
		return pixel

	def CrAr(self, src_flnm, dst_flnm, format ):
		"""
		CrAr(): Create Array with Georeferencing from another file (src_flnm), save it in file (dst_flnm) with format (format)
		CrAr( self, src_flnm, dst_flnm, format )
		"""
		cr_opts=[]
		# Read information from source file.
		src_ds = gdal.Open(str(src_flnm))
		gt = src_ds.GetGeoTransform()
		pj = src_ds.GetProjection()
		src_ds = None
		# Standard checking on the GDAL driver
		Driver = gdal.GetDriverByName( str(format) )
		if Driver is None:
			raise ValueError, "CrAr: No DriverFound "+format
		DriverMTD = Driver.GetMetadata()
		if not DriverMTD.has_key('DCAP_CREATE'):
			print 'Format Driver %s does not support creation and piecewise writing.\nPlease select a format that does, such as GTiff or HFA (Erdas/Imagine).' % format
			sys.exit( 1 )	
		# Set up the band number
		nbands = 1
		#print "nbands =", nbands
		# Collect information on source files
		flinfos = self.names_to_fileinfos( str(src_flnm) )
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
		out_fh = gdal.Open( str(dst_flnm), gdal.GA_Update )
		gdal.PopErrorHandler()
		# Otherwise create a new file
		if out_fh is None:
			geot = [ulx, psize_x, 0, uly, 0, psize_y]
			print geot[0], geot[1], geot[2], geot[3], geot[4]
			xsize = int((lrx-ulx)/geot[1]+0.5)
			ysize = int((lry-uly)/geot[5]+0.5)
			out_fh=Driver.Create(str(dst_flnm),xsize,ysize,nbands,band_type,cr_opts)
			if out_fh is None:
				raise ValueError, "CrAr: Failed to create new file "+dst_flnm
				sys.exit( 1 )
		out_fh.SetGeoTransform( gt )
		out_fh.SetProjection( pj )
		#out_fh.GetRasterBand(1).SetRasterColorTable(flinfos[0].ct)
		nodata = None
		iband = 1
		for fi in flinfos:
			fi.copy_into( out_fh, 1, iband, nodata )
			iband=iband+1
		iband = 0 
		
	def names_to_fileinfos( self, name ):
		file_infos = []
		fi = file_info()
		if fi.init_from_name( name ) == 1:
			file_infos.append( fi )
		return file_infos

	def OnFileInError(self):
		dlg = wx.MessageDialog(self, 
				'Minimum files to add:\n\n  Input files => NDVI and Modis Band7\n  One Output file',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
	
	def OnQCInError(self):
		dlg = wx.MessageDialog(self, 
				'QC type error\n\n Please check your input',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

	# Path+filename seek and set
	def make_fb(self):
		# get current working directory
		self.dirnm = os.getcwd()
		self.cc2 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='QC File:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback2,
		    	)
		self.cc6 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='OUT File: ',
			startDirectory = self.dirnm,
			fileMask='*.tif',
			fileMode=wx.SAVE,
			changeCallback = self.fbbCallback6
		    	)
	# Collect path+filenames

	def fbbCallback2(self, evt):
		 self.qc = str(evt.GetString())
	
	def fbbCallback6(self, evt):
		 self.output = str(evt.GetString())
		# Front text
		
	def make_text(self):
		self.text = wx.StaticText(self, -1, "This is processing MODIS09A State Quality Assessment Bits through the use of gdal and numeric.")

	# QC type radio buttons
	def make_radiobuttons3(self):
		self.rbox3 = wx.BoxSizer(wx.HORIZONTAL)
		self.rb3 = wx.RadioBox(self, -1, "Select QC Type", 
			wx.DefaultPosition, wx.DefaultSize,
			self.NameQC, 2, wx.RA_SPECIFY_COLS)
		self.rb3.SetToolTip(wx.ToolTip("Select QC type"))
		self.rb3.SetLabel("QC Type")
		self.rbox3.Add(self.rb3,1,wx.ALL,0)
		
	def EvtRadioBox3(self, evt):
		self.nb = evt.GetInt()
		self.qc_type = NameQC[self.nb]
		#print self.qc_type

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
		self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox3, self.rb3)

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

class file_info:
	"""A class holding information about a GDAL file."""
	def init_from_name(self, filename):
		"""
		Initialize file_info from filename
		filename -- Name of file to read.
		Returns 1 on success or 0 if the file can't be opened.
		"""
		fh = gdal.Open( str(filename) )
		if fh is None:
			return 0	
		self.filename = filename
		self.bands = fh.RasterCount
		self.xsize = fh.RasterXSize
		self.ysize = fh.RasterYSize
		self.band_type = fh.GetRasterBand(1).DataType
		self.projection = fh.GetProjection()
		self.geotransform = fh.GetGeoTransform()
		self.ulx = self.geotransform[0]
		self.uly = self.geotransform[3]
		self.lrx = self.ulx + self.geotransform[1] * self.xsize
		self.lry = self.uly + self.geotransform[5] * self.ysize
		ct = fh.GetRasterBand(1).GetRasterColorTable()
		if ct is not None:
			self.ct = ct.Clone()
		else:
			self.ct = None
		return 1
	
	def copy_into( self, t_fh, s_band = 1, t_band = 1, nodata_arg=None ):
		"""
		Copy this files image into target file.
		"""
		t_geotransform = t_fh.GetGeoTransform()
		t_ulx = t_geotransform[0]
		t_uly = t_geotransform[3]
		t_lrx = t_geotransform[0] + t_fh.RasterXSize * t_geotransform[1]
		t_lry = t_geotransform[3] + t_fh.RasterYSize * t_geotransform[5]
	
		# figure out intersection region
		tgw_ulx = max(t_ulx,self.ulx)
		tgw_lrx = min(t_lrx,self.lrx)
		if t_geotransform[5] < 0:
			tgw_uly = min(t_uly,self.uly)
			tgw_lry = max(t_lry,self.lry)
		else:
			tgw_uly = max(t_uly,self.uly)
			tgw_lry = min(t_lry,self.lry)
		
		# do they even intersect?
		if tgw_ulx >= tgw_lrx:
			return 1
		if t_geotransform[5] < 0 and tgw_uly <= tgw_lry:
			return 1
		if t_geotransform[5] > 0 and tgw_uly >= tgw_lry:
			return 1
		
		# compute target window in pixel coordinates.
		tw_xoff = int((tgw_ulx - t_geotransform[0]) / t_geotransform[1] + 0.1)
		tw_yoff = int((tgw_uly - t_geotransform[3]) / t_geotransform[5] + 0.1)
		tw_xsize = int((tgw_lrx-t_geotransform[0])/t_geotransform[1] + 0.5) - tw_xoff
		tw_ysize = int((tgw_lry-t_geotransform[3])/t_geotransform[5] + 0.5) - tw_yoff
	
		if tw_xsize < 1 or tw_ysize < 1:
			return 1
	
		# Compute source window in pixel coordinates.
		sw_xoff = int((tgw_ulx - self.geotransform[0]) / self.geotransform[1])
		sw_yoff = int((tgw_uly - self.geotransform[3]) / self.geotransform[5])
		sw_xsize = int((tgw_lrx - self.geotransform[0]) / self.geotransform[1] + 0.5) - sw_xoff
		sw_ysize = int((tgw_lry - self.geotransform[3]) / self.geotransform[5] + 0.5) - sw_yoff
	
		if sw_xsize < 1 or sw_ysize < 1:
			return 1
	
		# Open the source file, and copy the selected region.
		s_fh = gdal.Open( str(self.filename) )
	
		return self.raster_copy( s_fh, sw_xoff, sw_yoff, sw_xsize, sw_ysize, s_band, t_fh, tw_xoff, tw_yoff, tw_xsize, tw_ysize, t_band, nodata_arg )

	def raster_copy( self, s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n, t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n, nodata=None ):
	
		if nodata is not None:
			return self.raster_copy_with_nodata(
			s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
			t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
			nodata )
		s_band = s_fh.GetRasterBand( s_band_n )
		t_band = t_fh.GetRasterBand( t_band_n )
		data = s_band.ReadRaster( s_xoff, s_yoff, s_xsize, s_ysize, t_xsize, t_ysize, t_band.DataType )
		t_band.WriteRaster( t_xoff, t_yoff, t_xsize, t_ysize, data, t_xsize, t_ysize, t_band.DataType )
		return 0

	def raster_copy_with_nodata( self, s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n, nodata ):
		import Numeric as Num
		s_band = s_fh.GetRasterBand( s_band_n )
		t_band = t_fh.GetRasterBand( t_band_n )
		data_src = s_band.ReadAsArray( s_xoff, s_yoff, s_xsize, s_ysize, t_xsize, t_ysize )
		data_dst = t_band.ReadAsArray( t_xoff, t_yoff, t_xsize, t_ysize )
		nodata_test = Num.equal(data_src,nodata)
		to_write = Num.choose(nodata_test, (data_src, data_dst))
		t_band.WriteArray( to_write, t_xoff, t_yoff )
		return 0


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
	
