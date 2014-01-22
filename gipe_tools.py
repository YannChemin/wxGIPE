# -*- coding: utf-8 -*-
import wx, os
path= os.getcwd()+"/" 

#----------------------------------------------------------
# Tools modules
#----------------------------------------------------------
def OnConvert(event):
	path_temp=''
	path_temp='python '+path+'proc_gdal_convert.py'
	wx.Execute(path_temp, False)
	
def OnLayerStackRGB(event):
	path_temp=''
	path_temp='python '+path+'proc_layer_stack_RGB.py'
	wx.Execute(path_temp, False)

def OnLayerStack(event):
	path_temp=''
	path_temp='python '+path+'proc_layer_stack.py'
	wx.Execute(path_temp, False)

#----------------------------------------------------------
# Import modules
#----------------------------------------------------------
def OnImportHdf(event):
	path_temp=''
	path_temp='python '+path+'proc_hdf_in.py'
	wx.Execute(path_temp, False)

def OnProcAsterIn(event):
	path_temp=''
	path_temp='python '+path+'proc_aster_in.py'
	wx.Execute(path_temp, False)

def OnProcLandsatIn(event):
	path_temp=''
	path_temp='python '+path+'proc_landsat_in.py'
	wx.Execute(path_temp, False)

def OnProcModisQc(event):
	path_temp=''
	path_temp='python '+path+'proc_modis_qc.py'
	wx.Execute(path_temp, False)

def OnProcModisQa(event):
	path_temp=''
	path_temp='python '+path+'proc_modis_stateqa.py'
	wx.Execute(path_temp, False)

#----------------------------------------------------------
# Processing Modules
#----------------------------------------------------------
def OnProcNdvi(event):
	path_temp=''
	path_temp='python '+path+'proc_ndvi.py'
	wx.Execute(path_temp, False)

def OnProcAlbedo(event):
	path_temp=''
	path_temp='python '+path+'proc_albedo.py'
	wx.Execute(path_temp, False)

#----------------------------------------------------------
# Auto-Processing Modules
#----------------------------------------------------------
def OnProcLandsatEtpotrs(event):
	path_temp=''
	path_temp='python '+path+'proc_landsat_etpotrs.py'
	wx.Execute(path_temp, False)

def OnProcLandsatEtasenay(event):
	path_temp=''
	path_temp='python '+path+'proc_landsat_etasenay.py'
	wx.Execute(path_temp, False)
