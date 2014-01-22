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

# Define satellite bands
infiles = []
# Define output file name
output = ''

doy = 180
sun_elevation = 45.0

# Define processing types
proc_selected = 'ReflectanceTOA'
proc_type = ['Radiance','ReflectanceTOA']

# Define Info Message
overview = """Aster DN 2 Rad 2 Ref"""

class MyFrame(wx.Frame):
	def __init__(self,parent, id=-1, title='Aster DN2Rad2Ref',
			pos=(0,0),
			size=(400,500),
			style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, id, title, pos, size, style)
		ico = images.getPngGipeIcon()
		self.SetIcon(ico)
		self.lognull = wx.LogNull()
		# Input Filenames
		self.infiles = infiles
		self.output = output
		self.doy = doy
		self.sun_elevation = sun_elevation
		# Pre-Processing types
		self.proc_type = proc_type
		self.proc_selected = proc_selected
		# Construct Interface
		self.make_text()
		self.make_input_param()
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
		self.mbox.Add((10,10))
		self.mbox.Add(self.scbox, 1, wx.EXPAND, 10)
		self.mbox.Add(self.sc1box, 1, wx.EXPAND, 10)
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
		print "infiles: ", self.infiles, " out:", self.output
		self.spacecraft_id = "Terra"
		self.sensor_id = "Aster"
		self.band_no = 1
		for infile in self.infiles:
			self.band_id = "band"+self.band_no
			self.band = LoadFile(infile)
			self.Lgain = (self.spacecraft_id, self.sensor_id, self.band_id)
			self.Loffset = (self.spacecraft_id, self.sensor_id, self.band_id)
			self.result=dn2rad_aster( self.Lgain, self.Loffset, self.band )
			if(self.proc_selected=='Reflectance'):
				self.kexo = kexo(self.spacecraft_id, self.sensor_id, self.band_id)
				self.result=rad2ref_aster( self.result, self.doy, self.sun_elevation, self.kexo )
			SaveArrayWithGeo(self.result,self.infile,self.output,'GTiff')
			self.band_no = self.band_no + 1
		self.Destroy()
		
	def OnSelectIn(self,event):
		dlg = wx.FileDialog(self, message="Select files to Process",
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
	
	def make_input_param(self):
		sc_text = wx.StaticText(self, -1, "Input DOY:", (45, 15))
		sc = wx.SpinCtrl(self, -1, "", (30, 50))
		sc.SetRange(1,366)
		sc.SetValue(1)	
		self.scbox = wx.BoxSizer(wx.HORIZONTAL)
		self.scbox.Add(sc_text,1,wx.EXPAND,10)
		self.scbox.Add(sc,1,wx.EXPAND,10)
		sc1_text = wx.StaticText(self, -1, "Input sun_elevation:", (45, 15))
		sc1 = wx.SpinCtrl(self, -1, "", (30, 50))
		sc1.SetRange(1.0,90.0)
		sc1.SetValue(45.0)	
		self.sc1box = wx.BoxSizer(wx.HORIZONTAL)
		self.sc1box.Add(sc_text,1,wx.EXPAND,10)
		self.sc1box.Add(sc,1,wx.EXPAND,10)
		
		
		
	# Path+filename seek and set
	def make_fb(self):
		# get current working directory
		self.dirnm = os.getcwd()
		self.cc0 = wx.Button(self, -1, " Browse ", (50,50))
		self.cc1 = filebrowse.FileBrowseButton(
			self, -1, size=(50, -1), labelText='OUT File: ',
			startDirectory = self.dirnm,
			fileMask='*.tif',
			fileMode=wx.SAVE,
			changeCallback = self.fbbCallback1
		    	)
	# Collect path+filenames
	def fbbCallback1(self, evt):
		 self.output = evt.GetString()
		# Front text
	def make_text(self):
		self.text = wx.StaticText(self, -1, "This is processing DN2Rad2Ref for Aster through the use of gdal and numeric")
	# Output format radio buttons
	def make_radiobuttons(self):
		self.rbox = wx.BoxSizer(wx.HORIZONTAL)
		self.rb = wx.RadioBox(self, -1, "Select Output Type", 
			wx.DefaultPosition, wx.DefaultSize,
			self.proc_type, 5, wx.RA_SPECIFY_COLS)
		self.rb.SetToolTip(wx.ToolTip("Select Output Type"))
		self.rb.SetLabel("Output Type")
		self.rbox.Add(self.rb,1,wx.ALL,10)
		
	def EvtRadioBox(self, evt):
		self.nb = evt.GetInt()
		self.vi_selected = self.vi_type[self.nb]
		print self.vi_selected

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
