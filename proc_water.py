###############################################################################
# $Id$
#
# Project:  Sub1 project of IRRI
# Purpose:  Satellite image processing of Water Mapping
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
ndvi = ''
band7 = ''

# Define output file name
output = ''

# Define Info Message
overview = """Water Mapping

Calculates Water ponding areas based on NDVI and Modis Band 7

Input of NDVI is a [-1.0;+1.0] range
Input of Band7 is original Modis storage band7=10000*band7

Returns 0 if no water is found and 1 if water is found

Xiao X., Boles S., Liu J., Zhuang D., Frokling S., Li C., Salas W., Moore III B. (2005). Mapping paddy rice agriculture in southern China using multi-temporal MODIS images. Remote Sensing of Environment 95:480-492.

Roy D.P., Jin Y., Lewis P.E., Justice C.O. (2005). Prototyping a global algorithm for systematic fire-affected area mapping using MODIS time series data. Remote Sensing of Environment 97:137-162.

"""



class MyFrame(wx.Frame):
	def __init__(self,parent, id=-1, title='Water Mapping',
			pos=(0,0),
			size=(400,500),
			style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		# Input Filenames
		self.ndvi = ndvi
		self.band7 = band7
		self.output = output
		# Construct Interface
		self.make_text()
		self.make_buttons()
		self.make_fb()
		self.mbox = wx.BoxSizer(wx.VERTICAL)
		self.mbox.Add((10,10))
		self.mbox.Add(self.text, 1, wx.EXPAND|wx.CENTER, 10)
		self.mbox.Add((10,10))
		self.mbox.Add((10,10))
		self.mbox.Add(self.cc2, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc3, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc6, 1, wx.EXPAND, 10)
		self.mbox.Add((10,10))
		self.mbox.Add(self.bbox, 1, wx.CENTER, 10)
		self.mbox.Add((10,10))
		self.SetSizer(self.mbox)
		self.bindEvents()
	
	# Process Equations, Handling and saving of output
	def OnOK(self,event):
		#print "ndvi: ", self.ndvi
		#print "band7:",self.band7
		#print "out:", self.output
		if(self.ndvi==''):
			self.OnFileInError()
		elif(self.band7==''):
			self.OnFileInError()
		else:
			self.ndviF = gdal.Open(self.ndvi)
			self.band7F = gdal.Open(self.band7)
			self.bndvi = self.ndviF.GetRasterBand(1)
			self.bb7 = self.band7F.GetRasterBand(1)
			self.test = gdal.Open(self.ndvi)
			self.CrAr( self.ndvi, self.output, 'GTiff' )
			self.result = gdal.Open(self.output, GA_Update)
			for self.y in range(self.bndvi.YSize - 1, -1, -1):
                                print (self.bndvi.YSize-self.y)
				#Fast way if same pixel sizes...
				#nxarray=array[j,:].astype(numpy.float32) 
				#nxarray=numpy.where(nxarray>0,self.water(self.scanline1, self.scanline2)
				self.scanline1=self.bndvi.ReadAsArray(0, self.y, self.bndvi.XSize, 1, self.bndvi.XSize, 1)
				self.scanline2=self.bb7.ReadAsArray(0, self.y/2, self.bb7.XSize, 1, self.bb7.XSize, 1)
				for self.x in range(0, self.bndvi.XSize - 1, 1):
					self.pix1 = self.scanline1[0][self.x]
					self.pix2 = self.scanline2[0][self.x/2]
					self.scanline1[0][self.x]=self.water(self.pix1, self.pix2)
				self.result.GetRasterBand(1).WriteArray(N.reshape(self.scanline1,(1,self.bndvi.XSize)), 0, self.y)
##		self.SaveArrayWithGeo(self.result,self.band7,self.output,'GTiff')
		self.Destroy()
		
##	def SaveArrayWithGeo( self, array, src_filename, dst_filename, format ):
##		"""
##		SaveArrayWithGeo(): Saves an Array (array) with Georeferencing from
##		another file (src_flnm), save it in file (dst_flnm) with format
##		(format)
##		SaveArrayWithGeo( self, array, src_filename, dst_filename, format )
##		"""
##		print src_filename
##                print str(src_filename)
##		src_ds1 = gdal.Open(str(src_filename))
##		gt = src_ds1.GetGeoTransform()
##		pj = src_ds1.GetProjection()
##		src_ds1 = None
##		
##		# Create GDAL dataset for array, and set georeferencing.
##		src_ds = gdal_array.OpenArray( array )
##		src_ds.SetGeoTransform( gt )
##		src_ds.SetProjection( pj )
##		
##		# Write array dataset to new file.
##		print 'there'
##		driver = gdal.GetDriverByName( format )
##		print 'there'
##		if driver is None:
##			raise ValueError, "SaveArrayWithGeo: Can't find driver "+format
##		
##		return driver.CreateCopy( dst_filename, src_ds )
	
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

	def water( self, ndvi, band7 ):
		"""
		Water Mapping
		water( ndvi, band7 )
		"""
		if ((ndvi<0.1)and(band7<400)):
			result=1
		else :
			result=0
		return result
	
	def OnFileInError(self):
		dlg = wx.MessageDialog(self, 
				'Minimum files to add:\n\n  Input files => NDVI and Modis Band7\n  One Output file',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

	# Path+filename seek and set
	def make_fb(self):
		# get current working directory
		self.dirnm = os.getcwd()
		self.cc2 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='NDVI:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback2,
		    	)
		self.cc3 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='Band7:',
			startDirectory = self.dirnm,
			fileMode=wx.OPEN,
			changeCallback = self.fbbCallback3
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
		 self.ndvi = str(evt.GetString())
	
	def fbbCallback3(self, evt):
		 self.band7 = str(evt.GetString())

	def fbbCallback6(self, evt):
		 self.output = str(evt.GetString())
		# Front text
		
	def make_text(self):
		self.text = wx.StaticText(self, -1, "This is processing water maps through the use of gdal and numeric. Water=1, non-water=0")

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

