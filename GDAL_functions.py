#For BitmapFromBuffer
import wx
# For Image Processing
import numpy
#Use gdal 1.5.x
from osgeo import gdalnumeric
from osgeo import gdal_array
from osgeo import gdal
from osgeo.gdalconst import *

import gdal_merge as g_m

# SaveArrayWithGeo(): Saves an Array (array) with Georeferencing from another file (src_flnm), save it in file (dst_flnm) with format (format)

def SaveArrayWithGeo( array, src_filename, dst_filename, format ):
	"""
	SaveArrayWithGeo(): Saves an Array (array) with Georeferencing from another file (src_flnm), save it in file (dst_flnm) with format (format)
	SaveArrayWithGeo( self, array, src_filename, dst_filename, format )
	"""
	#From warmerdam at p...  Thu May  3 09:36:03 2001
	#From: warmerdam at p... (Frank Warmerdam)
	#Date: Wed Nov 21 11:49:13 2007
	#Subject: [gdal-dev] python bindings
	#References: <Pine.OSF.4.20.0105030806190.4482-100000@e...>
	#Message-ID: <3AF15EC3.FFD4AACF@p...>
	# Read information from source file.
	src_ds = gdal.Open(str(src_filename))
	gt = src_ds.GetGeoTransform()
	pj = src_ds.GetProjection()
	src_ds = None
	
	# Create GDAL dataset for array, and set georeferencing.
	src_ds = gdal_array.OpenArray( array )
	src_ds.SetGeoTransform( gt )
	src_ds.SetProjection( pj )
	
	# Write array dataset to new file. 
	driver = gdal.GetDriverByName( format )
	if driver is None:
		raise ValueError, "SaveArrayWithGeo: Can't find driver "+format
	
	return driver.CreateCopy( dst_filename, src_ds )

# CrAr(): Create Array with Georeferencing from another file (src_flnm), save it in file (dst_flnm) with format (format)

def CrAr( src_flnm, dst_flnm, format ):
	"""
	CrAr(): Create Array with Georeferencing from another file (src_flnm), save it in file (dst_flnm) with format (format)
	CrAr( self, src_flnm, dst_flnm, format )
	"""
	cr_opts=[]
	# Read information from source file.
	src_ds = gdal.Open(str(src_flnm[0]))
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
	out_fh.GetRasterBand(1).SetRasterColorTable(flinfos[0].ct)
	nodata = None
	iband = 1
	for fi in flinfos:
		fi.copy_into( out_fh, 1, iband, nodata )
		iband=iband+1
	iband = 0 
	
def file_ext_type(gdal_format):
	"""
For each output format of GDAL, returns the file extension.
  VRT (rw+): Virtual Raster
  GTiff (rw+): GeoTIFF
  NITF (rw+): National Imagery Transmission Format
  HFA (rw+): Erdas Imagine Images (.img)
  ELAS (rw+): ELAS
  AAIGrid (rw): Arc/Info ASCII Grid
  DTED (rw): DTED Elevation Raster
  PNG (rw): Portable Network Graphics
  JPEG (rw): JPEG JFIF
  MEM (rw+): In Memory Raster
  GIF (rw): Graphics Interchange Format (.gif)
  XPM (rw): X11 PixMap Format
  BMP (rw+): MS Windows Device Independent Bitmap
  PCIDSK (rw+): PCIDSK Database File
  PCRaster (rw): PCRaster Raster File
  ILWIS (rw+): ILWIS Raster Map
  GMT (rw): GMT NetCDF Grid Format
  netCDF (rw): Network Common Data Format
  HDF4Image (rw+): HDF4 Dataset
  PNM (rw+): Portable Pixmap Format (netpbm)
  ENVI (rw+): ENVI .hdr Labelled
  EHdr (rw+): ESRI .hdr Labelled
  PAux (rw+): PCI .aux Labelled
  MFF (rw+): Vexcel MFF Raster
  MFF2 (rw+): Vexcel MFF2 (HKV) Raster
  BT (rw+): VTP .bt (Binary Terrain) 1.3 Format
  IDA (rw+): Image Data and Analysis
  FIT (rw): FIT Image
  RMF (rw+): Raster Matrix Format
  JPEG2000 (rw): JPEG-2000 part 1 (ISO/IEC 15444-1)
  RST (rw+): Idrisi Raster A.1
  USGSDEM (rw): USGS Optional ASCII DEM (and CDED)
	"""
	if(gdal_format == "VRT"):
		extension = '.vrt'
	if(gdal_format == "GTiff"):
		extension = '.tif'
	if(gdal_format == "NITF"):
		extension = ''
	if(gdal_format == "HFA"):
		extension = '.img'
	if(gdal_format == "ELAS"):
		extension = ''
	if(gdal_format == "AAIGrid"):
		extension = ''
	if(gdal_format == "DTED"):
		extension = ''
	if(gdal_format == "PNG"):
		extension = '.png'
	if(gdal_format == "JPEG"):
		extension = 'jpg'
	if(gdal_format == "MEM"):
		extension = ''
	if(gdal_format == "GIF"):
		extension = '.gif'
	if(gdal_format == "XPM"):
		extension = '.xpm'
	if(gdal_format == "BMP"):
		extension = '.bmp'
	if(gdal_format == "PCIDSK"):
		extension = ''
	if(gdal_format == "PCRaster"):
		extension = ''
	if(gdal_format == "ILWIS"):
		extension = ''
	if(gdal_format == "GMT"):
		extension = ''
	if(gdal_format == "netCDF"):
		extension = ''
	if(gdal_format == "HDF4Image"):
		extension = '.hdf'
	if(gdal_format == "PNM"):
		extension = '.pnm'
	if(gdal_format == "ENVI"):
		extension = ''
	if(gdal_format == "EHdr"):
		extension = '.hdr'
	if(gdal_format == "PAux"):
		extension = '.aux'
	if(gdal_format == "MFF"):
		extension = '.mff'
	if(gdal_format == "MFF2"):
		extension = '.hkv'
	if(gdal_format == "BT"):
		extension = '.bt'
	if(gdal_format == "IDA"):
		extension = ''
	if(gdal_format == "FIT"):
		extension = '.fit'
	if(gdal_format == "RMF"):
		extension = '.rmf'
	if(gdal_format == "JPEG2000"):
		extension = '.jpg'
	if(gdal_format == "RST"):
		extension = '.rst'
	if(gdal_format == "USGSDEM"):
		extension = '.dem'

	return extension

def BmpFromBuffer(filename, band_number1, band_number2, band_number3, alpha_val):
	print "Draw ",filename
	Img2D = gdal.Open(str(filename), GA_ReadOnly)
	x_max = Img2D.RasterXSize
	y_max = Img2D.RasterYSize
	imgH = y_max
	imgW = x_max
	#prepare buffer
	rgba = numpy.ndarray(shape=(imgH,imgW,4), dtype=numpy.uint8)
	#fill with colour
	band1=10 	#red
	band2=200 	#green
	band3=0 	#blue
	if (alpha_val == None or alpha_val < 0):
		alpha_val=255
	else: pass
	rgba[:,:,0].fill(band1)
	rgba[:,:,1].fill(band2)
	rgba[:,:,2].fill(band3)
	rgba[:,:,3].fill(alpha_val) #alpha
	print "X= ",imgW, "Y= ",imgH
	for iBand in range(1, Img2D.RasterCount + 1):
		if(band_number1==band_number2 and band_number1==band_number3):
			inband = Img2D.GetRasterBand(iBand)
			for x in range(0, inband.XSize -1, 1):
				#print "X= ",x
				scanline = inband.ReadAsArray(x, 0, 1, inband.YSize, 1, inband.YSize)
				#print scanline[x]
				for y in range(inband.YSize - 1, -1, -1):
					pixel = scanline[y][0]
					rgba[y,x,0]= pixel
					rgba[y,x,1]= pixel
					rgba[y,x,2]= pixel
					#print scanline[y][0], pixel, rgba[y,x,0]
		else:
			# Start Thread Number 1
			inband1 = Img2D.GetRasterBand(band_number1)
			for x1 in range(0, inband1.XSize -1, 1):
				scanline1 = inband1.ReadAsArray(x1, 0, 1, inband1.YSize, 1, inband1.YSize)
				for y1 in range(inband1.YSize - 1, -1, -1):
					pixel1 = scanline[y1][0]
					rgba[y1,x1,0]= pixel1
			del inband1
			# End of Thread Number 1
			# Start Thread Number 2
			inband2 = Img2D.GetRasterBand(band_number2)
			for x2 in range(0, inband2.XSize -1, 1):
				scanline2 = inband2.ReadAsArray(x2, 0, 1, inband2.YSize, 1, inband2.YSize)
				for y2 in range(inband2.YSize - 1, -1, -1):
					pixel2 = scanline[y2][0]
					rgba[y2,x2,1]= pixel2
			del inband2
			# End of Thread Number 2
			# Start Thread Number 3
			inband3 = Img2D.GetRasterBand(band_number3)
			for x3 in range(0, inband3.XSize -1, 1):
				scanline3 = inband3.ReadAsArray(x3, 0, 1, inband3.YSize, 1, inband3.YSize)
				for y3 in range(inband3.YSize - 1, -1, -1):
					pixel3 = scanline[y3][0]
					rgba[y3,x3,2]= pixel3
			del inband3
			# End of Thread Number 3
	
	bmp = wx.BitmapFromBufferRGBA(imgW, imgH, rgba) #wxPython 2.8
	return bmp

def BmpSmallFromBuffer(filename, band_number1, band_number2, band_number3, alpha_val):
	"""
	Reads a file with GDAL, then creates a small Bitmap from buffer to display on screen
	Right now, it should be about max screen size (1000 pixels max)
	It is skipping pixels to load only smaller version of the file into buffer.
	This is experimental...
	"""
	print "Draw ",filename
	Img2D = gdal.Open(str(filename), GA_ReadOnly)
	x_max = Img2D.RasterXSize
	y_max = Img2D.RasterYSize
	imgH = y_max
	imgW = x_max
	# How many skips to read pixel
	skip = 1
	if(y_max>2000 or x_max>2000):
		if(y_max>x_max):
			factor = int(y_max/1000)
		else:
			factor = int(x_max/1000)
	if(factor>=2):
		skip = factor
	#prepare buffer
	rgba = numpy.ndarray(shape=(int(imgH/skip),int(imgW/skip),4), dtype=numpy.uint8)
	#fill with colour
	band1=10 	#red
	band2=200 	#green
	band3=0 	#blue
	if (alpha_val == None or alpha_val < 0):
		alpha_val=255
	else: pass
	rgba[:,:,0].fill(band1)
	rgba[:,:,1].fill(band2)
	rgba[:,:,2].fill(band3)
	rgba[:,:,3].fill(alpha_val) #alpha
	print "X= ",imgW, "Y= ",imgH
	print "Xskipped= ",int(imgW/skip), "Yskipped= ",int(imgH/skip)
	xskippedmax=int(imgW/skip)-1
	yskippedmax=int(imgH/skip)-1
	xskipped = 0
	yskipped = yskippedmax
	for iBand in range(1, Img2D.RasterCount + 1):
		if(band_number1==band_number2 and band_number1==band_number3):
			inband = Img2D.GetRasterBand(iBand)
			xskipped=0
			for x in range(0, inband.XSize -1, skip):
				#print "X= ",x
				scanline = inband.ReadAsArray(x, 0, 1, inband.YSize, 1, inband.YSize)
				#print scanline[x]
				yskipped=yskippedmax
				for y in range(inband.YSize - 1, -1, (-1*skip)):
					pixel = scanline[y][0]
					rgba[yskipped,xskipped,0]= pixel
					rgba[yskipped,xskipped,1]= pixel
					rgba[yskipped,xskipped,2]= pixel
					#print scanline[y][0], pixel, rgba[y,x,0]
					yskipped=yskipped-1
				xskipped=xskipped+1
		else:
			# Start Thread Number 1
			inband1 = Img2D.GetRasterBand(band_number1)
			for x1 in range(0, inband1.XSize -1, 1):
				scanline1 = inband1.ReadAsArray(x1, 0, 1, inband1.YSize, 1, inband1.YSize)
				for y1 in range(inband1.YSize - 1, -1, -1):
					pixel1 = scanline[y1][0]
					rgba[y1,x1,0]= pixel1
			del inband1
			# End of Thread Number 1
			# Start Thread Number 2
			inband2 = Img2D.GetRasterBand(band_number2)
			for x2 in range(0, inband2.XSize -1, 1):
				scanline2 = inband2.ReadAsArray(x2, 0, 1, inband2.YSize, 1, inband2.YSize)
				for y2 in range(inband2.YSize - 1, -1, -1):
					pixel2 = scanline[y2][0]
					rgba[y2,x2,1]= pixel2
			del inband2
			# End of Thread Number 2
			# Start Thread Number 3
			inband3 = Img2D.GetRasterBand(band_number3)
			for x3 in range(0, inband3.XSize -1, 1):
				scanline3 = inband3.ReadAsArray(x3, 0, 1, inband3.YSize, 1, inband3.YSize)
				for y3 in range(inband3.YSize - 1, -1, -1):
					pixel3 = scanline[y3][0]
					rgba[y3,x3,2]= pixel3
			del inband3
			# End of Thread Number 3
	
	bmp = wx.BitmapFromBufferRGBA(int(imgW/skip), int(imgH/skip), rgba) #wxPython 2.8
	return (bmp,skip)