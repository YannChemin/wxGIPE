#!/usr/bin/python

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
# Based on Landsat channels
inputFile = []

# Define output base file name
output = ''

# Define vegetation indices types
proc_selected = 'ReflectanceTOA'
proc_type = ['Radiance','ReflectanceTOA']

# Define Info Message
overview = """This module is a full import module for Landsat 7. It corrects every band (1,2,3,4,5,6L,6H,7,8Pan) from DN to either reflectance at top of Atmosphere or Kinetic Temperature. 
It is useful after importing your Landsat 7 imagery from storage format that is generally in standard DN values range.

NOTES
Generally, after downloading L7ETM+, the bands are in gz format.

Run this shell command: "for file in *.gz; do gzip -d $file; done"

Finally run this GIPE module using metfile.met and base_ouput_name"""

class MyFrame(wx.Frame):
	def __init__(self,parent, id=-1, title='Pre-Processing Landsat image from .met metadata file',
			pos=(0,0),
			size=(300,300),
			style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		self.metadata = metadata
		# Input Filenames
		self.inputFile = inputFile
		self.output = output
		# Pre-Processing types
		self.proc_type = proc_type
		self.proc_selected = proc_selected
		# Construct Interface
		self.make_text()
		self.make_buttons()
		self.make_radiobuttons()
		self.make_fb()
		self.mbox = wx.BoxSizer(wx.VERTICAL)
		self.mbox.Add((10,20))
		self.mbox.Add(self.text, 1, wx.EXPAND|wx.CENTER, 10)
		self.mbox.Add((10,20))
		self.mbox.Add((10,10))
		self.mbox.Add(self.cc0, 1, wx.EXPAND, 10)
		self.mbox.Add(self.cc1, 1, wx.EXPAND, 10)
		self.mbox.Add((10,10))
		self.mbox.Add(self.rbox, 1, wx.EXPAND, 0)
		self.mbox.Add((10,20))
		self.mbox.Add((10,10))
		self.mbox.Add(self.bbox, 1, wx.CENTER, 10)
		self.mbox.Add((10,10))
		self.SetSizer(self.mbox)
		self.bindEvents()
	
	# Process Equations, Handling and saving of output
	def OnOK(self,event):
		print "in: ", self.inputFile, " out:", self.output
		if(self.inputFile==''):
			self.OnFileInError()
		else:
			self.metadata = read_met_file_landsat7(self.inputFile)
		
		# Process Thread 1
		self.band1 = LoadFile(self.metadata[0])
		self.Lmin = self.metadata[9]
		self.LMax = self.metadata[18]
		self.Qcalmin = self.metadata[27]
		self.QcalMax = self.metadata[36]
		self.result1 = dn2rad_landsat7( self.Lmin, self.LMax, QCalMax, QCalmin, self.band1 )
		del self.band1 #Free Memory
		if(self.proc_selected=='ReflectanceTOA'):
			self.doy = date2doy(self.metadata[50],self.metadata[49],self.metadata[48])
			self.kexo = kexo(self.metadata[52],self.metadata[51],"band1")
			self.result1 = rad2ref_landsat7( self.result1, self.doy, self.metadata[46], self.k_exo )
		self.out = self.output+"1"
		SaveArrayWithGeo(self.result1,self.band1,self.out,'GTiff')
		del self.result1 #Free Memory
		# End of Process Thread 1
		
		# Process Thread 2
		self.band2 = LoadFile(self.metadata[1])
		self.Lmin = self.metadata[10]
		self.LMax = self.metadata[19]
		self.Qcalmin = self.metadata[28]
		self.QcalMax = self.metadata[37]
		self.result2 = dn2rad_landsat7( self.Lmin, self.LMax, QCalMax, QCalmin, self.band2 )
		del self.band2 #Free Memory
		if(self.proc_selected=='ReflectanceTOA'):
			self.doy = date2doy(self.metadata[50],self.metadata[49],self.metadata[48])
			self.kexo = kexo(self.metadata[52],self.metadata[51],"band2")
			self.result2 = rad2ref_landsat7( self.result2, self.doy, self.metadata[46], self.k_exo )
		self.out = self.output+"2"
		SaveArrayWithGeo(self.result2,self.band2,self.out,'GTiff')
		del self.result2 #Free Memory
		# End of Process Thread 2
		
		# Process Thread 3
		self.band3 = LoadFile(self.metadata[2])
		self.Lmin = self.metadata[11]
		self.LMax = self.metadata[20]
		self.Qcalmin = self.metadata[29]
		self.QcalMax = self.metadata[38]
		self.result3 = dn2rad_landsat7( self.Lmin, self.LMax, QCalMax, QCalmin, self.band2 )
		del self.band3 #Free Memory
		if(self.proc_selected=='ReflectanceTOA'):
			self.doy = date2doy(self.metadata[50],self.metadata[49],self.metadata[48])
			self.kexo = kexo(self.metadata[52],self.metadata[51],"band3")
			self.result3 = rad2ref_landsat7( self.result3, self.doy, self.metadata[46], self.k_exo )
		self.out = self.output+"3"
		SaveArrayWithGeo(self.result3,self.band3,self.out,'GTiff')
		del self.result3 #Free Memory
		# End of Process Thread 3

		# Process Thread 4
		self.band4 = LoadFile(self.metadata[3])
		self.Lmin = self.metadata[12]
		self.LMax = self.metadata[21]
		self.Qcalmin = self.metadata[30]
		self.QcalMax = self.metadata[39]
		self.result4 = dn2rad_landsat7( self.Lmin, self.LMax, QCalMax, QCalmin, self.band4 )
		del self.band4 #Free Memory
		if(self.proc_selected=='ReflectanceTOA'):
			self.doy = date2doy(self.metadata[50],self.metadata[49],self.metadata[48])
			self.kexo = kexo(self.metadata[52],self.metadata[51],"band4")
			self.result4 = rad2ref_landsat7( self.result4, self.doy, self.metadata[46], self.k_exo )
		self.out = self.output+"4"
		SaveArrayWithGeo(self.result4,self.band4,self.out,'GTiff')
		del self.result4 #Free Memory
		# End of Process Thread 4

		# Process Thread 5
		self.band5 = LoadFile(self.metadata[4])
		self.Lmin = self.metadata[13]
		self.LMax = self.metadata[22]
		self.Qcalmin = self.metadata[31]
		self.QcalMax = self.metadata[40]
		self.result5 = dn2rad_landsat7( self.Lmin, self.LMax, QCalMax, QCalmin, self.band5 )
		del self.band5 #Free Memory
		if(self.proc_selected=='ReflectanceTOA'):
			self.doy = date2doy(self.metadata[50],self.metadata[49],self.metadata[48])
			self.kexo = kexo(self.metadata[52],self.metadata[51],"band5")
			self.result5 = rad2ref_landsat7( self.result5, self.doy, self.metadata[46], self.k_exo )
		self.out = self.output+"5"
		SaveArrayWithGeo(self.result5,self.band5,self.out,'GTiff')
		del self.result5 #Free Memory
		# End of Process Thread 5

		# Process Thread 6
		self.band61 = LoadFile(self.metadata[5])
		self.Lmin = self.metadata[14]
		self.LMax = self.metadata[23]
		self.Qcalmin = self.metadata[32]
		self.QcalMax = self.metadata[41]
		self.result61 = tempk_landsat7( self.band61 )
		del self.band61 #Free Memory
		self.out = self.output+"61"
		SaveArrayWithGeo(self.result61,self.band61,self.out,'GTiff')
		del self.result61 #Free Memory
		# End of Process Thread 6

		# Process Thread 7
		self.band62 = LoadFile(self.metadata[6])
		self.Lmin = self.metadata[15]
		self.LMax = self.metadata[24]
		self.Qcalmin = self.metadata[33]
		self.QcalMax = self.metadata[42]
		self.result62 = tempk_landsat7( self.band62 )
		del self.band62 #Free Memory
		self.out = self.output+"62"
		SaveArrayWithGeo(self.result62,self.band62,self.out,'GTiff')
		del self.result62 #Free Memory
		# End of Process Thread 7

		# Process Thread 8
		self.band7 = LoadFile(self.metadata[7])
		self.Lmin = self.metadata[16]
		self.LMax = self.metadata[25]
		self.Qcalmin = self.metadata[34]
		self.QcalMax = self.metadata[43]
		self.result7 = dn2rad_landsat7( self.Lmin, self.LMax, QCalMax, QCalmin, self.band7 )
		del self.band7 #Free Memory
		if(self.proc_selected=='ReflectanceTOA'):
			self.doy = date2doy(self.metadata[50],self.metadata[49],self.metadata[48])
			self.kexo = kexo(self.metadata[52],self.metadata[51],"band7")
			self.result7 = rad2ref_landsat7( self.result7, self.doy, self.metadata[46], self.k_exo )
		self.out = self.output+"7"
		SaveArrayWithGeo(self.result7,self.band7,self.out,'GTiff')
		del self.result7 #Free Memory
		# End of Process Thread 8
		
		# Process Thread 9
		self.band8 = LoadFile(self.metadata[8])
		self.Lmin = self.metadata[17]
		self.LMax = self.metadata[26]
		self.Qcalmin = self.metadata[35]
		self.QcalMax = self.metadata[44]
		self.result8 = dn2rad_landsat7( self.Lmin, self.LMax, QCalMax, QCalmin, self.band8 )
		del self.band8 #Free Memory
		if(self.proc_selected=='ReflectanceTOA'):
			self.doy = date2doy(self.metadata[50],self.metadata[49],self.metadata[48])
			self.kexo = kexo(self.metadata[52],self.metadata[51],"band8")
			self.result7 = rad2ref_landsat7( self.result8, self.doy, self.metadata[46], self.k_exo )
		self.out = self.output+"8"
		SaveArrayWithGeo(self.result8,self.band8,self.out,'GTiff')
		del self.result8 #Free Memory
		# End of Process Thread 8

		self.Destroy()
	
	def OnFileInError(self):
		dlg = wx.MessageDialog(self, 
				'Minimum files to add:\n\n  Input file => .met\n  One Output file',
				'Error',wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		
	# Path+filename seek and set
	def make_fb(self):
		# get current working directory
		self.dirnm = os.getcwd()
		self.cc0 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='.met File:',
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
		self.text = wx.StaticText(self, -1, "Pre-processing Landsat7ETM+ using gdal and numeric")
	# Output format radio buttons
	def make_radiobuttons(self):
		self.rbox = wx.BoxSizer(wx.HORIZONTAL)
		self.rb = wx.RadioBox(self, -1, "Select Pre-Processing Type", 
			wx.DefaultPosition, wx.DefaultSize,
			self.proc_type, 5, wx.RA_SPECIFY_COLS)
		self.rb.SetToolTip(wx.ToolTip("Select Pre-Processing Type"))
		self.rb.SetLabel("Output Type")
		self.rbox.Add(self.rb,1,wx.ALL,10)
		
	def EvtRadioBox(self, evt):
		self.nb = evt.GetInt()
		self.proc_selected = self.proc_type[self.nb]
		print self.proc_selected

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
