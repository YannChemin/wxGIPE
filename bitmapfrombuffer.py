#!/usr/bin/python

import wx
import numpy
#use gdal 1.5.x
from osgeo import gdalnumeric
from osgeo import gdal_array
from osgeo import gdal
from osgeo.gdalconst import *

class TestFrame(wx.Frame):
    def __init__(self, parent, id, title, pos, size):
        wx.Frame.__init__(self, parent, id, title, pos, size)
	
	Img = 'test_data/b5.tif'
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
	#prepare buffer
	rgba = numpy.ndarray(shape=(imgH,imgW,4), dtype=numpy.uint8)
	#fill with black
	band1=10 	#red
	band2=200 	#green
	band3=0 	#blue
	alpha=255
	rgba[:,:,0].fill(band1)
	rgba[:,:,1].fill(band2)
	rgba[:,:,2].fill(band3)
	rgba[:,:,3].fill(alpha) #alpha
	print "X= ",imgW, "Y= ",imgH
	for iBand in range(1, Img2D.RasterCount + 1):
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
	
	bmp = wx.BitmapFromBufferRGBA(imgW, imgH, rgba) #wxPython 2.8
	static_bmp = wx.StaticBitmap(self, -1, bmp)
        self.Show(True)

if __name__ == '__main__':
        app = wx.PySimpleApp()
        frame = TestFrame(None, wx.ID_ANY, 'test display', (200, 200), (600, 600))
        app.MainLoop()
