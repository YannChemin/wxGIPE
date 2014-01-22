#Last updated 22 March 2008
from math import *

global	pre		#pre-processing
global	albedo		#albedo
global	emissivity	#emissivity
global	vi		#vegetation indices
global	wi		#water indices
global	eb		#energy balance
global	et_pot_rs	#ET potential by RS
global	et_ref_hg	#ET reference Hargreaves
global	et_pot_pm	#ET potential Penman-Monteith
global	et_a_tsa	#ET actual Two Sources Algorithm
global	utils		#Utilities, conversions

class rs( object ):
	"""
###############################################################################
# $Id$
#
# Project:  Remote Sensing Image Processing functions
# Purpose:  Satellite image processing
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
	"""
	def initialize( self ):
		"""
		Instantiate classes
		"""
		pre=self.pre() 				#preprocessing
		albedo=self.albedo()			#albedo
		emissivity=self.emissivity()		#emissivity
		vi=self.vi()				#vegetation indices
		wi=self.wi()				#vegetation indices
		eb=self.eb()				#energy balance
		et_pot_rs=self.et_pot_rs()		#ET potential by RS
		et_ref_hg=self.et_ref_hg()		#ET reference Hargreaves
		et_pot_pm=self.et_pot_pm()		#ET potential Penman-Monteith
		et_a_tsa=self.et_a_tsa()		#ET actual Two Sources Algorithm
		utils=self.utils()			#Utilities, conversions
	
	class pre( object ):
		# PRE-PROCESSING FUNCTIONS
		def read_met_file_landsat7(self, metfName):
			"""
			Utility to parse Metadata .met XML file for extracting Landsat 7 satellite and sensor informations
			read_met_file_landsat7(metfName)
			"""
			metadata = [] # This will be returned
			bandFlnm = [] #names of the different Landsat band files
			lmin = [] # min radiance
			lmax = [] # max radiance
			qcalmin = [] # min pixel value
			qcalmax = [] # max pixel value
			
			full_metadata = {} # Holds the full file elements (no real use now)
			wordList = [] # To extract info from the .met file
			wordTuple = () # To extract info from the .met file
			wordCount = 0 # To extract info from the .met file
			lineCount = 0 # To extract info from the .met file
			
			dateList = [] # For date elements separation
			dateCount = 0 # For date elements separation
			
			file = open(metfName,'rU')
			for line in file:
				wordList.append(lineCount)
				for word in line.split():
					wordList.append(word)
					wordCount += 1
				if (wordList[1]=="ACQUISITION_DATE"):
					acquisition_date = wordList[3]
					for date in acquisition_date.split('-'):
						dateList.append(date)
						dateCount += 1
					print dateList[0], dateList[1], dateList[2]
				if (wordList[1]=="BAND1_FILE_NAME"):
					bandFlnm.insert(0,wordList[3].strip('"'))
					print bandFlnm[0]
				if (wordList[1]=="BAND2_FILE_NAME"):
					bandFlnm.insert(1,wordList[3].strip('"'))
					print bandFlnm[1]
				if (wordList[1]=="BAND3_FILE_NAME"):
					bandFlnm.insert(2,wordList[3].strip('"'))
					print bandFlnm[2]
				if (wordList[1]=="BAND4_FILE_NAME"):
					bandFlnm.insert(3,wordList[3].strip('"'))
					print bandFlnm[3]
				if (wordList[1]=="BAND5_FILE_NAME"):
					bandFlnm.insert(4,wordList[3].strip('"'))
					print bandFlnm[4]
				if (wordList[1]=="BAND61_FILE_NAME"):
					bandFlnm.insert(5,wordList[3].strip('"'))
					print bandFlnm[5]
				if (wordList[1]=="BAND62_FILE_NAME"):
					bandFlnm.insert(6,wordList[3].strip('"'))
					print bandFlnm[6]
				if (wordList[1]=="BAND7_FILE_NAME"):
					bandFlnm.insert(7,wordList[3].strip('"'))
					print bandFlnm[7]
				if (wordList[1]=="BAND8_FILE_NAME"):
					bandFlnm.insert(8,wordList[3].strip('"'))
					print bandFlnm[8]
				if (wordList[1]=="SUN_AZIMUTH"):
					sun_azimuth = float(wordList[3])
					print sun_azimuth
				if (wordList[1]=="SUN_ELEVATION"):
					sun_elevation = float(wordList[3])
					print sun_elevation
				if (wordList[1]=="LMAX_BAND1"):
					lmax.insert(0,float(wordList[3]))
					print lmax[0]
				if (wordList[1]=="LMAX_BAND2"):
					lmax.insert(1,float(wordList[3]))
					print lmax[1]
				if (wordList[1]=="LMAX_BAND3"):
					lmax.insert(2,float(wordList[3]))
					print lmax[2]
				if (wordList[1]=="LMAX_BAND4"):
					lmax.insert(3,float(wordList[3]))
					print lmax[3]
				if (wordList[1]=="LMAX_BAND5"):
					lmax.insert(4,float(wordList[3]))
					print lmax[4]
				if (wordList[1]=="LMAX_BAND61"):
					lmax.insert(5,float(wordList[3]))
					print lmax[5]
				if (wordList[1]=="LMAX_BAND62"):
					lmax.insert(6,float(wordList[3]))
					print lmax[6]
				if (wordList[1]=="LMAX_BAND7"):
					lmax.insert(7,float(wordList[3]))
					print lmax[7]
				if (wordList[1]=="LMAX_BAND8"):
					lmax.insert(8,float(wordList[3]))
					print lmax[8]
				if (wordList[1]=="LMIN_BAND1"):
					lmin.insert(0,float(wordList[3]))
					print lmin[0]
				if (wordList[1]=="LMIN_BAND2"):
					lmin.insert(1,float(wordList[3]))
					print lmin[1]
				if (wordList[1]=="LMIN_BAND3"):
					lmin.insert(2,float(wordList[3]))
					print lmin[2]
				if (wordList[1]=="LMIN_BAND4"):
					lmin.insert(3,float(wordList[3]))
					print lmin[3]
				if (wordList[1]=="LMIN_BAND5"):
					lmin.insert(4,float(wordList[3]))
					print lmin[4]
				if (wordList[1]=="LMIN_BAND61"):
					lmin.insert(5,float(wordList[3]))
					print lmin[5]
				if (wordList[1]=="LMIN_BAND62"):
					lmin.insert(6,float(wordList[3]))
					print lmin[6]
				if (wordList[1]=="LMIN_BAND7"):
					lmin.insert(7,float(wordList[3]))
					print lmin[7]
				if (wordList[1]=="LMIN_BAND8"):
					lmin.insert(8,float(wordList[3]))
					print lmin[8]
				if (wordList[1]=="QCALMAX_BAND1"):
					qcalmax.insert(0,float(wordList[3]))
					print qcalmax[0]
				if (wordList[1]=="QCALMAX_BAND2"):
					qcalmax.insert(1,float(wordList[3]))
					print qcalmax[1]
				if (wordList[1]=="QCALMAX_BAND3"):
					qcalmax.insert(2,float(wordList[3]))
					print qcalmax[2]
				if (wordList[1]=="QCALMAX_BAND4"):
					qcalmax.insert(3,float(wordList[3]))
					print qcalmax[3]
				if (wordList[1]=="QCALMAX_BAND5"):
					qcalmax.insert(4,float(wordList[3]))
					print qcalmax[4]
				if (wordList[1]=="QCALMAX_BAND61"):
					qcalmax.insert(5,float(wordList[3]))
					print qcalmax[5]
				if (wordList[1]=="QCALMAX_BAND62"):
					qcalmax.insert(6,float(wordList[3]))
					print qcalmax[6]
				if (wordList[1]=="QCALMAX_BAND7"):
					qcalmax.insert(7,float(wordList[3]))
					print qcalmax[7]
				if (wordList[1]=="QCALMAX_BAND8"):
					qcalmax.insert(8,float(wordList[3]))
					print qcalmax[8]
				if (wordList[1]=="QCALMIN_BAND1"):
					qcalmin.insert(0,float(wordList[3]))
					print qcalmin[0]
				if (wordList[1]=="QCALMIN_BAND2"):
					qcalmin.insert(1,float(wordList[3]))
					print qcalmin[1]
				if (wordList[1]=="QCALMIN_BAND3"):
					qcalmin.insert(2,float(wordList[3]))
					print qcalmin[2]
				if (wordList[1]=="QCALMIN_BAND4"):
					qcalmin.insert(3,float(wordList[3]))
					print qcalmin[3]
				if (wordList[1]=="QCALMIN_BAND5"):
					qcalmin.insert(4,float(wordList[3]))
					print qcalmin[4]
				if (wordList[1]=="QCALMIN_BAND61"):
					qcalmin.insert(5,float(wordList[3]))
					print qcalmin[5]
				if (wordList[1]=="QCALMIN_BAND62"):
					qcalmin.insert(6,float(wordList[3]))
					print qcalmin[6]
				if (wordList[1]=="QCALMIN_BAND7"):
					qcalmin.insert(7,float(wordList[3]))
					print qcalmin[7]
				if (wordList[1]=="QCALMIN_BAND8"):
					qcalmin.insert(8,float(wordList[3]))
					print qcalmin[8]
				if (wordList[1]=="SPACECRAFT_ID"):
					spacecraft_id = wordList[3].strip('"')
					print spacecraft_id
				if (wordList[1]=="SENSOR_ID"):
					sensor_id = wordList[3].strip('"')
					print sensor_id
				if(wordList[1]!='END'):
					wordTuple = (wordList[1],wordList[3])
					full_metadata[lineCount]= wordTuple
					print full_metadata[lineCount]
					wordList = []
					lineCount += 1
				else:
					break
		
			metadata.extend(bandFlnm) # Add file names to metadata [0-8]
			metadata.extend(lmin) # Min Radiance value [9-17]
			metadata.extend(lmax) # Max Radiance value [18-26]
			metadata.extend(qcalmin) # Min pixel value [27-35]
			metadata.extend(qcalmax) # Max pixel value [36-44]
			metadata.append(sun_azimuth) # Sun azimuth angle [45]
			metadata.append(sun_elevation) # Sun elevation angle [46]
			metadata.append(acquisition_date) # human readable date [47]
			metadata.extend(dateList) # separated [year, month, day] [48-50]
			metadata.append(spacecraft_id) # Landsat7 [51]
			metadata.append(sensor_id) # ETM+ [52]
			
			return metadata

		def dn2rad_landsat5(self,c_year,c_month,c_day,year,month,day,band,DN):
			"""
			Conversion of DN to Radiance for Landsat 5TM
			c_year, c_month, c_day are from the NLAPS report of processing completion.
			year, month and day are the satellite overpass characteristics
			dn2rad_landsat5(self,c_year,c_month,c_day,year,month,day,band,DN)
			"""
			if(c_year<2003):
				gain_mode=1
			elif(c_year==2003):
				if(c_month<5):
					gain_mode=1
				elif(c_month==5):
					if(c_day<5):
						gain_mode=1
					else:
						gain_mode=2
				else:
					gain_mode=2
			elif (c_year>2003 and c_year<2007):
				gain_mode=2
			elif (c_year==2007):
				if(c_month<5):
					gain_mode=2
				elif(year<1992):
					gain_mode=3
				else:
					gain_mode=4
			if (gain_mode==1):
				if (band==1):
					gain = 0.602431
					bias = -1.52
				if (band==2):
					gain = 1.175100
					bias = -2.84
				if (band==3):
					gain = 0.805765
					bias = -1.17
				if (band==4):
					gain = 0.814549
					bias = -1.51
				if (band==5):
					gain = 0.108078
					bias = -0.37
				if (band==6):
					gain = 0.055158
					bias = 1.2378
				if (band==7):
					gain = 0.056980
					bias = -0.15
			if (gain_mode==2):
				if (band==1):
					gain = 0.762824
					bias = -1.52
				if (band==2):
					gain = 1.442510
					bias = -2.84
				if (band==3):
					gain = 1.039880
					bias = -1.17
				if (band==4):
					gain = 0.872588
					bias = -1.51
				if (band==5):
					gain = 0.119882
					bias = -0.37
				if (band==6):
					gain = 0.055158
					bias = 1.2378
				if (band==7):
					gain = 0.065294
					bias = -0.15
			if (gain_mode==3):
				if (band==1):
					gain = 0.668706
					bias = -1.52
				if (band==2):
					gain = 1.317020
					bias = -2.84
				if (band==3):
					gain = 1.039880
					bias = -1.17
				if (band==4):
					gain = 0.872588
					bias = -1.51
				if (band==5):
					gain = 0.119882
					bias = -0.37
				if (band==6):
					gain = 0.055158
					bias = 1.2378
				if (band==7):
					gain = 0.065294
					bias = -0.15
			if (gain_mode==4):
				if (band==1):
					gain = 0.762824
					bias = -1.52
				if (band==2):
					gain = 1.442510
					bias = -2.84
				if (band==3):
					gain = 1.039880
					bias = -1.17
				if (band==4):
					gain = 0.872588
					bias = -1.51
				if (band==5):
					gain = 0.119882
					bias = -0.37
				if (band==6):
					gain = 0.055158
					bias = 1.2378
				if (band==7):
					gain = 0.065294
					bias = -0.15
			result=gain*DN+bias
			return result

		def dn2rad_landsat7(self, Lmin, LMax, QCalMax, QCalmin, DN ):
			"""
			Conversion of DN to Radiance for Landsat 7ETM+
			http://ltpwww.gsfc.nasa.gov/IAS/handbook/handbook_htmls/chapter11/chapter11.html#section11.3 
			dn2rad_landsat7( Lmin, LMax, QCalMax, QCalmin, DN )
			"""
			gain 	= (LMax-Lmin)/(QCalMax-QCalmin)
			offset 	= Lmin
			result 	= gain * (1.0*DN - QCalmin) + offset
			return result
		
		def rad2ref_landsat7(self, radiance, doy, sun_elevation, k_exo ):
			"""
			Conversion of Radiance to Reflectance Top Of Atmosphere for Landsat 7ETM+
			rad2ref_landsat7( radiance, doy, sun_elevation, k_exo )
			"""
			PI = 3.1415927
			ds = ( 1.0 + 0.01672 * sin( 2 * PI * ( doy - 93.5 ) / 365 ) )
			result = (radiance/((cos((90-sun_elevation)*PI/180)/(PI*ds*ds))*k_exo))
			return result
		
		def tempk_landsat7(self, l6 ):
			"""
			Surface temperature for Landsat 7ETM+
			tempk_landsat7( l6 )
			"""
			result = 1282.71 / (log ((666.09 / l6) + 1.0))
			return result

		def tempk_landsat5(self, l6 ):
			"""
			Surface temperature for Landsat 5TM
			tempk_landsat5( l6 )
			"""
			result = 1260.56 / (log ((607.76 / l6) + 1.0))
			return result
		
		def tempk_landsat4(self, l6 ):
			"""
			Surface temperature for Landsat 5TM
			tempk_landsat4( l6 )
			"""
			result = 1284.30 / (log ((671.62 / l6) + 1.0))
			return result
		
		def dn2rad_aster(self, Lgain, Loffset, DN ):
			"""
			Conversion of DN to Radiance for Aster
			rad2ref_aster(  Lgain, Loffset, DN  )
			"""
			result = Lgain * DN + Loffset
			return result
		
		def rad2ref_aster(self, radiance, doy, sun_elevation, k_exo ):
			"""
			Conversion of Radiance to Reflectance for ASTER
			rad2ref_aster( radiance, doy, sun_elevation, k_exo )
			"""
			PI = 3.1415927
			ds = ( 1.0 + 0.01672 * sin( 2 * PI * ( doy - 93.5 ) / 365 ) )
			result = radiance / ( ( cos ( ( 90.0 - sun_elevation ) * PI / 180.0 ) / ( PI * ds * ds ) ) * k_exo )
			return result
		
		def Lgain(self, spacecraft_id, sensor_id, band_id):
			"""Gain for Dn to Rad conversion
			This is used for processing radiance of Terra Aster images.
			Spacecraft_id: Terra
				Sensor_id: Aster
					band_id: band1, band2, band3, band4, band5, band7, band8, band9
			Lgain(spacecraft_id, sensor_id, band_id):
			"""
			if(spacecraft_id == "Terra"):
				if (sensor_id == "Aster"):
					if(band_id == "band1"):
						Lgain = 0.676
					if(band_id == "band2"):
						Lgain = 0.862
					if(band_id == "band3"):
						Lgain = 0.217
					if(band_id == "band4"):
						Lgain = 0.0696
					if(band_id == "band5"):
						Lgain = 0.0696
					if(band_id == "band7"):
						Lgain = 0.0696
					if(band_id == "band8"):
						Lgain = 0.0696
					if(band_id == "band9"):
						Lgain = 0.0318
					else:
						Lgain = 0.0
				else:
					Lgain = 0.0
		
		def Loffset(self, spacecraft_id, sensor_id, band_id):
			"""
			Offset for Dn to Rad conversion
			This is used for processing radiance of Terra Aster images.
			Spacecraft_id: Terra
				Sensor_id: Aster
					band_id: band1, band2, band3, band4, band5, band7, band8, band9
			Lgain(spacecraft_id, sensor_id, band_id):
			"""
			if(spacecraft_id == "Terra"):
				if (sensor_id == "Aster"):
					if(band_id == "band1"):
						Loffset = -0.676
					if(band_id == "band2"):
						Loffset = -0.862
					if(band_id == "band3"):
						Loffset = -0.217
					if(band_id == "band4"):
						Loffset = -0.0696
					if(band_id == "band5"):
						Loffset = -0.0696
					if(band_id == "band7"):
						Loffset = -0.0696
					if(band_id == "band8"):
						Loffset = -0.0696
					if(band_id == "band9"):
						Loffset = -0.0318
					else:
						Loffset = 0.0
				else:
					Loffset = 0.0
		
		def kexo(self, spacecraft_id, sensor_id, band_id):
			"""Sun exo-atmospheric irridiance [W/m2/sr]
			This is used for processing surface reflectance.
			Spacecraft_id: Landsat4
				Sensor_id: TM
					band_id: band1, band2, band3, band4, band5, band7
			Spacecraft_id: Landsat5
				Sensor_id: TM
					band_id: band1, band2, band3, band4, band5, band7
			Spacecraft_id: Landsat7
				Sensor_id: ETM+
					band_id: band1, band2, band3, band4, band5, band7, band8
			Spacecraft_id: Terra
				Sensor_id: Aster
					band_id: band1, band2, band3, band4, band5, band7, band8, band9
			kexo(spacecraft_id, sensor_id, band_id)
			"""
			if(spacecraft_id == "Landsat4"):
				if (sensor_id == "TM"):
					if(band_id == "band1"):
						kexo = 1957.0
					if(band_id == "band2"):
						kexo = 1825.0
					if(band_id == "band3"):
						kexo = 1557.0
					if(band_id == "band4"):
						kexo = 1033.0
					if(band_id == "band5"):
						kexo = 214.9
					if(band_id == "band7"):
						kexo = 80.72
					else:
						kexo = 0.0
			if(spacecraft_id == "Landsat5"):
				if (sensor_id == "TM"):
					if(band_id == "band1"):
						kexo = 1957.0
					if(band_id == "band2"):
						kexo = 1826.0
					if(band_id == "band3"):
						kexo = 1554.0
					if(band_id == "band4"):
						kexo = 1036.0
					if(band_id == "band5"):
						kexo = 215.0
					if(band_id == "band7"):
						kexo = 80.67
					else:
						kexo = 0.0
			if(spacecraft_id == "Landsat7"):
				if (sensor_id == "ETM+"):
					if(band_id == "band1"):
						kexo = 1969.0
					if(band_id == "band2"):
						kexo = 1840.0
					if(band_id == "band3"):
						kexo = 1551.0
					if(band_id == "band4"):
						kexo = 1044.0
					if(band_id == "band5"):
						kexo = 225.7
					if(band_id == "band7"):
						kexo = 82.07
					if(band_id == "band8"):
						kexo = 1385.64 # Self calculated value...
					else:
						kexo = 0.0
			if(spacecraft_id == "Terra"):
				if (sensor_id == "Aster"):
					if(band_id == "band1"):
						kexo = 1828.0
					if(band_id == "band2"):
						kexo = 1559.0
					if(band_id == "band3"):
						kexo = 1045.0
					if(band_id == "band4"):
						kexo = 226.73
					if(band_id == "band5"):
						kexo = 86.50
					if(band_id == "band7"):
						kexo = 74.72
					if(band_id == "band8"):
						kexo = 66.41
					if(band_id == "band9"):
						kexo = 59.83
					else:
						kexo = 0.0
				else:
					kexo = 0.0
			else:
				kexo = 0.0
			return kexo
	# END OF PRE_PROCESSING FUNCTIONS
	
	# ALBEDO FUNCTIONS
	
	class albedo( object ):
		"""
		Albedo calculations for Aster, Landsat, AVHRR, MODIS
		"""
		def aster( self, greenchan, redchan, nirchan, swirchan1, swirchan2, swirchan3, swirchan4, swirchan5, swirchan6 ):
			"""
			Broadband albedo Aster (Careful the DN multiplier! Here it is 1000.0, output range should be [0.0-1.0])
			albedo_aster( greenchan, redchan, nirchan, swirchan1, swirchan2, swirchan3, swirchan4, swirchan5, swirchan6 )
			"""
			result = ( 0.09*greenchan + 0.06*redchan + 0.1*nirchan + 0.092*swirchan1 + 0.035*swirchan2 + 0.04*swirchan3 + 0.047*swirchan4 + 0.07*swirchan5 + 0.068*swirchan6 ) / ((0.09+0.06+0.1+0.092+0.035+0.04+0.047+0.07+0.068)*1000.0)
			return result
		
		def landsat( self, bluechan, greenchan, redchan, nirchan, chan5, chan7 ):
			"""
			Broadband albedo Landsat 5TM and 7ETM+ (maybe others too but not sure)
			albedo_landsat( bluechan, greenchan, redchan, nirchan, chan5, chan7 )
			"""
			result = ( 0.293*bluechan + 0.274*greenchan + 0.233*redchan + 0.156*nirchan + 0.033*chan5 + 0.011*chan7 )
			return result
		
		def modis( self, redchan, nirchan, chan3, chan4, chan5, chan6, chan7 ):
			"""
			Broadband albedo MODIS (Careful the DN multiplier! Here it is 10000.0, output range should be [0.0-1.0])
			albedo_modis( redchan, nirchan, chan3, chan4, chan5, chan6, chan7 )
			"""
			result = ((0.22831*redchan + 0.15982*nirchan + 0.09132*(chan3+chan4+chan5) + 0.10959*chan6 + 0.22831*chan7 ) / 10000.0 )
			return result
			
		def avhrr( self, redchan, nirchan ):
			"""
			Broadband albedo NOAA AVHRR 14 (maybe others too but not sure). Careful the DN multiplier! Here it is 10000.0, output range should be [0.0-1.0]
			albedo_avhrr( redchan, nirchan )
			"""
			result = (( 0.035+ 0.545*nirchan - 0.32*redchan) / 10000.0 )
			return result
	
	# END OF ALBEDO FUNCTIONS
	
	class emissivity( object ):
		"""
		Emissivity Calculations
		"""
		def generic( self, ndvi ):
			"""
			Emissivity Generic mode (Reads directly from NDVI)
			Estimation in the 8-14 micrometers range for sparse canopy
			emissivity_generic( ndvi )
			"""
			if(ndvi < 0.16):
				result = 1.0
			elif(ndvi > 0.74):
				result = 0.9
			else:
				result = 1.009 + 0.047*log(ndvi)
			return result
	
	# VI FUNCTIONS
	class vi( object ):
		"""
		Various Vegetation Indices functions:
		ARVI, DVI, EVI, GARI, GEMI, GVI, IPVI, MSAVI, MSAVI2,NDVI, PVI, SAVI, SR, WDVI
		"""
		def arvi( self, redchan, nirchan, bluechan ):
			"""
			Atmospheric Resistant Vegetation Index: ARVI is resistant to atmospheric effects (in comparison to the NDVI) and is accomplished by a self correcting process for the atmospheric effect in the red channel, using the difference in the radiance between the blue and the red channels.(Kaufman and Tanre 1996).
			arvi( redchan, nirchan, bluechan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			bluechan = 1.0*bluechan
			result = (nirchan - (2.0*redchan - bluechan)) / ( nirchan + (2.0*redchan - bluechan))
			return result
		
		def dvi( self, redchan, nirchan ):
			"""
			DVI: Difference Vegetation Index
			dvi( redchan, nirchan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result = ( nirchan - redchan )
			return result
		
		def evi( self, bluechan, redchan, nirchan ):
			"""
			EVI: Enhanced Vegetation Index
			evi( bluechan, redchan, nirchan )
			Huete A.R., Liu H.Q., Batchily K., vanLeeuwen W. (1997). A comparison of vegetation indices global set of TM images for EOS-MODIS. Remote Sensing of Environment, 59:440-451.
			"""
			bluechan = 1.0*bluechan
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result = 2.5 * ( nirchan - redchan ) / ( nirchan + 6.0 * redchan - 7.5 * bluechan + 1.0 )
			return result
		
		def gari( self, redchan, nirchan, bluechan, greenchan ):
			"""
			GARI: green atmospherically resistant vegetation index
			gari( redchan, nirchan, bluechan, greenchan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			bluechan = 1.0*bluechan
			greenchan = 1.0*greenchan
			result = ( nirchan - (greenchan-(bluechan - redchan))) / ( nirchan- (greenchan-(bluechan - redchan)))
			return result
		
		def gemi( self, redchan, nirchan ):
			"""
			GEMI: Global Environmental Monitoring Index
			gemi( redchan, nirchan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result = (( (2*((nirchan * nirchan)-(redchan * redchan))+1.5*nirchan+0.5*redchan) /(nirchan + redchan + 0.5)) * (1 - 0.25 * (2*((nirchan * nirchan)-(redchan * redchan))+1.5*nirchan+0.5*redchan) /(nirchan + redchan + 0.5))) -( (redchan - 0.125) / (1 - redchan))
			return result
		
		def gvi( self, bluechan, greenchan, redchan, nirchan, chan5chan, chan7chan):
			"""
			Green Vegetation Index
			gvi( bluechan, greenchan, redchan, nirchan, chan5chan, chan7chan)
			"""
			bluechan = 1.0*bluechan
			greenchan = 1.0*greenchan
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			chan5chan = 1.0*chan5chan
			chan7chan = 1.0*chan7chan
			result = ( -0.2848 * bluechan - 0.2435 * greenchan - 0.5436 * redchan + 0.7243 * nirchan + 0.0840 * chan5chan - 0.1800 * chan7chan)
			return result
		
		def ipvi( self, redchan, nirchan ):
			"""
			IPVI: Infrared Percentage Vegetation Index 
					NIR	
				IPVI = --------
					NIR+red
			ipvi( redchan, nirchan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result = ( nirchan ) / ( nirchan + redchan )
			return result
		
		def msavi2( self, redchan, nirchan ):
			"""
			MSAVI2: second Modified Soil Adjusted Vegetation Index
			MSAVI2 = (1/2)*(2(NIR+1)-sqrt((2*NIR+1)^2-8(NIR-red)))
			msavi2( redchan, nirchan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result =( 1.0 / 2.0 ) * ( 2.0 * ( nirchan + 1.0 ) - sqrt ( ( 2 * nirchan + 1.0 ) * ( 2.0 * nirchan + 1.0 ) ) - ( 8.0 * ( nirchan - redchan ) ) )
			return result
		
		def msavi( self, redchan, nirchan ):
			"""
			// MSAVI: Modified Soil Adjusted Vegetation Index//
			//							//
			//			 s(NIR-s*red-a)			//
			//		  MSAVI = ---------------------------	//
			//			  (a*NIR+red-a*s+X*(1+s*s))	//
			//	where a is the soil line intercept, s is the 	//
			//	soil line slope, and X 	is an adjustment factor //
			//	which is set to minimize soil noise (0.08 in 	//
			//	original papers).				//
			msavi( redchan, nirchan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result = ( 1.0 / 2.0 ) * ( 2.0 * ( nirchan + 1.0 ) - sqrt ( ( 2.0 * nirchan + 1.0 ) * ( 2.0 * nirchan + 1.0 ) ) - ( 8.0 * ( nirchan - redchan ) ) )
			return result
		
		def ndvi( self, redchan, nirchan ):
			"""
			Normalized Difference Vegetation Index
			ndvi( redchan, nirchan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result = ( nirchan - redchan ) / ( nirchan + redchan )
			return result
		
		def pvi( self, redchan, nirchan ):
			"""
			PVI: Perpendicular Vegetation Index
			PVI = sin(a)NIR-cos(a)red for a  isovegetation lines (lines of equal vegetation) would all be parallel to the soil line therefore a=1
			pvi( redchan, nirchan )
			"""
		
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result = (sin(1.0) * nirchan ) / ( cos(1.0) * redchan )
			return result
		
		def savi( self, redchan, nirchan ):
			"""
			Soil Adjusted Vegetation Index
			savi( redchan, nirchan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result = ((1.0+0.5)*( nirchan - redchan )) / ( nirchan + redchan +0.5)
			return result
		
		def sr( self, redchan, nirchan ):
			"""
			Simple Vegetation ratio
			sr( redchan, nirchan )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			result =(nirchan/redchan)
			return result
		
		def wdvi( self, redchan, nirchan, soil_line_weight ):
			"""
			Weighted Difference Vegetation Index
			if(soil_weight_line == None):
				a = 1.0 #slope of soil line
			wdvi( redchan, nirchan, soil_line_weight )
			"""
			redchan = 1.0*redchan
			nirchan = 1.0*nirchan
			if(soil_weight_line == None):
				a = 1.0 #slope of soil line
			else:
				a = soil_line_weight
				result = nirchan - a * redchan
			return result
	
	# END OF VI FUNCTIONS
	
	# WI FUNCTIONS
	class wi( object ):
		"""
		Various Water Indices functions:
		LSWI
		"""
		def lswi( self, nirchan, swirchan ):
			"""
			Land Surface Water Index
			lswi( nirchan, swirchan )
			"""
			nirchan = 1.0*nirchan
			swirchan = 1.0*swirchan
			result =(nirchan - swirchan)/(nirchan + swirchan)
			return result
		
	# END OF WI FUNCTIONS
	
	# ENERGY BALANCE EQUTATIONS
	class eb(object):
		"""
		Energy balance functions:
		ETA, EVAPFR, EVAPFR_SENAY, SOILMOISTURE, G0, H0, RAH_FIXED_DT, H0_SEBAL, Z0M, U_STAR, U_BLEND, ROH_AIR, MINMAX, MINMAX_TEMPERATURE, 
		"""
		def eta( self, r_net_day, evaporative_fraction, temperature):
			"""
			eta( r_net_day, evaporative_fraction, temperature)
			"""
			t_celsius = temperature - 273.15
			latent 	  = 86400.0/((2.501-0.002361*t_celsius)*pow(10,6))
			result 	  = r_net_day * evaporative_fraction * latent
			return result
		
		def evapfr( self, r_net, g0, h0 ):
			"""
			calculates the evaporative fraction after bastiaanssen (1995).
			It takes input of Net Radiation (see r.sun,r.eb.netrad), soil heat flux (see r.eb.g0) and sensible heat flux (see r.eb.h0). 
			evaporative fraction
			evapfr( r_net, g0, h0 )
			"""
			result = (r_net - g0 - h0) / (r_net - g0)
			return result
		
		def evapfr_senay( self, temperature, temperature_hot, temperature_cold ):
			"""
			calculates the evaporative fraction after Senay (Sensors, 2007).
			evapfr_senay( temperature )
			"""
			result = (temperature_hot - temperature) / (temperature_hot - temperature_cold)
			return result
		
		def soilmoisture( self, evaporative_fraction ):
			"""
			soil moisture in the root zone
			Makin, Molden and Bastiaanssen, 2001
			soilmoisture( evaporative_fraction )
			"""
			result = (exp((evaporative_fraction-1.2836)/0.4213))/0.511
			return result
		
		def g0( self, albedo, ndvi, temperature, r_net, time, roerink ):
			"""
			Calculates the soil heat flux approximation (g0) after bastiaanssen (1995).
			It takes input of Albedo, NDVI, Surface Skin temperature, Net Radiation (see r.sun), time of satellite overpass, and a flag for the Roerink empirical modification from the HAPEX-Sahel experiment. 
			Soil heat flux
			g0(albedo, ndvi, temperature, r_net, time, roerink)
			"""
			if (time<=9.0 or time>15.0):
				r0_coef = 1.1
			elif (time>9.0 and time<=11.0):
				r0_coef = 1.0
			elif (time>11.0 and time<=13.0):
				r0_coef = 0.9
			elif (time>13.0 and time<=15.0):
				r0_coef = 1.0
			else: pass
			a = (0.0032 * (albedo/r0_coef) + 0.0062 * (albedo/r0_coef) * (albedo/r0_coef))
			b = (1 - 0.978 * ndvi)
			#// Spain (Bastiaanssen, 1995)
			result = (r_net * (temperature-273.15) / albedo) * a * b
			#// HAPEX-Sahel (Roerink, 1995)
			if(roerink):
				result = result * 1.430 - 0.0845
			return result
		
		def h0( self, air_density, air_specific_heat, heat_aerodynamic_resistance, temperature_difference ):
			"""
			calculates the sensible heat flux approximation (h0), a flag allows the use of an affine transform from surface temperature after bastiaanssen (1995).
			It takes input of air density, air specific heat, difference of temperature between surface skin and a height of about 2m above, and the aerodynamic resistance to heat transport. 
			"""
			result = air_density * air_specific_heat * temperature_difference / heat_aerodynamic_resistance
			return result
		
		def rah_fixed_dt( self, u2m, roh_air, cp, dt, disp, z0m, z0h, tempk ):
			"""
			It takes input of air density, air specific heat, difference of temperature between surface skin and a height of about 2m above, and the aerodynamic resistance to heat transport.  This version runs an iteration loop to stabilize psychrometric data for the aerodynamic resistance to heat flux.
			Fixed temperature difference correction of aerodynamic roughness for heat transport
			"""
			PI = 3.14159265358979323846 
			ublend=u2m*(log(100-disp)-log(z0m))/(log(2-disp)-log(z0m))	
			for i in range(10):
				ustar = 0.41*ublend/(log((100-disp)/z0m)-psim)
				rah   = (log((2-disp)/z0h)-psih)/(0.41*ustar)
				h_in  = roh_air * cp * dt / rah
				length= -roh_air*cp*pow(ustar,3)*tempk/(0.41*9.81*h_in)
				xm    = pow(1.0-16.0*((100-disp)/length),0.25)
				xh    = pow(1.0-16.0*((2-disp)/length),0.25)
				psim  = 2.0*log((1.0+xm)/2.0)+log((1+xm*xm)-2*atan(xm)+0.5*PI)
				psih  = 2.0*log((1.0+xh*xh)/2.0)
			return rah
		
		def h0_SEBAL( self, tempk_water, tempk_desert, t0_dem, tempk, ndvi, ndvi_max, dem, rnet_desert, g0_desert,  t0_dem_desert, u2m, dem_desert):
			"""
			SEBAL Loop
			"""
			ITER_MAX = 10
			debug = 0
			if debug :
				print "*****************************\n"
				print "t0_dem = ",t0_dem
				print "ndvi = ", ndvi, "ndvimax = ",ndvi_max
				print "*****************************\n"
			#//	dtair[0] 	= dt_air_0(t0_dem, tempk_water, tempk_desert);
			dtair[0] = 5.0;
			#// 	printf("*****************************dtair = %5.3f\n",dtair[0]);
			roh_air[0] 	= roh_air_0(tempk);
			#// 	printf("*****************************rohair=%5.3f\n",roh_air[0]);
			roh_air_desert 	= roh_air_0(tempk_desert);
			#// 	printf("**rohairdesert = %5.3f\n",roh_air_desert);
			zom0 		= zom_0(ndvi, ndvi_max);
			#// 	printf("*****************************zom = %5.3f\n",zom0);
			u_0 		= U_0(zom0, u2m);
			#// 	printf("*****************************u0\n");
			rah[0] 		= rah_0(zom0, u_0);
			#// 	printf("*****************************rah = %5.3f\n",rah[0]);
			h[0] 		= h_0(roh_air[0], rah[0], dtair[0]);
			#// 	printf("*****************************h\n");
			if debug:
				print "dtair[0]	= ", dtair[0], "K"
				print "roh_air[0] 	= ", roh_air[0], "kg/m3"
				print "roh_air_desert0 = ", roh_air_desert, "kg/m3"
				print "zom_0 		= ", zom0
				print "u_0 		= ", u_0
				print "rah[0] 		= ", rah[0], "s/m"
				print "h[0] 		= ", h[0], "W/m2"
			#/*----------------------------------------------------------------*/
			#/*Main iteration loop of SEBAL*/
			zom[0] = zom0
			for ic in range (ITER_MAX):
				if debug :
					print "\n ******** ITERATION ",ic,"*********"
				#/* Where is roh_air[i]? */
				psih = psi_h(t0_dem,h[ic-1],u_0,roh_air[ic-1])
				ustar[ic] = u_star(t0_dem,h[ic-1],u_0,roh_air[ic-1],zom[0],u2m)
				rah[ic] = rah1(psih, ustar[ic])
				#/* get desert point values from maps */
				if ic == 1:
					h_desert	= rnet_desert - g0_desert
					zom_desert	= 0.002
					psih_desert 	= psi_h(t0_dem_desert,h_desert,u_0,roh_air_desert)
					ustar_desert	= u_star(t0_dem_desert,h_desert,u_0,roh_air_desert,zom_desert,u2m)
				else:
					roh_air_desert	= rohair(dem_desert,tempk_desert,dtair_desert)
					h_desert	= h1(roh_air_desert,rah_desert,dtair_desert)
					ustar_desertold = ustar_desert
					psih_desert 	= psi_h(t0_dem_desert,h_desert,ustar_desertold,roh_air_desert)
					ustar_desert	= u_star(t0_dem_desert,h_desert,ustar_desertold,roh_air_desert,zom_desert,u2m)
				rah_desert	= rah1(psih_desert,ustar_desert)
				dtair_desert 	= dt_air_desert(h_desert, roh_air_desert, rah_desert)
				#/* This should find the new dtair from inversed h equation...*/
				dtair[ic] 	= dt_air(t0_dem, tempk_water, tempk_desert, dtair_desert)
				#/* This produces h[ic] and roh_air[ic+1] */
				roh_air[ic] 	= rohair(dem, tempk, dtair[ic])
				h[ic] 		= h1(roh_air[ic], rah[ic], dtair[ic])
				#/* Output values of the iteration parameters */
				if debug:
					print "psih[", ic,"] 	= ", psih
					print "ustar[", ic,"] 	= ", ustar[ic]
					print "rah[", ic,"] 	= ", rah[ic], "s/m"
					print "h_desert 	= ", h_desert
					print "rohair_desert	= ", roh_air_desert
					print "psih_desert 	= ", psih_desert, "ustar_desert = ", ustar_desert, "rah_desert = ", rah_desert
					print "dtair_desert 	= \n", dtair_desert
					print "dtair[", ic,"] 	= ", dtair[ic], "K"
					print "roh_air[", ic, "] = ", roh_air[ic], "kg/m3"
					print "h[",ic,"]	= ", h[ic], "W/m2"
			return h[ITER_MAX]
		
		def z0m( self, savi ):
			"""
			calculates the momentum roughness length (z0m) and optionally the surface roughness for heat transport (z0h) as per SEBAL requirements from bastiaanssen (1995).
			This version is calculating from a SAVI with an empirical equation, as seen in Pawan (2004).
			This is a typical input to sensible heat flux computations of any energy balance modeling.
			// Momentum roughness length (z0m) as seen in Pawan (2004)
			z0m( savi )
			"""
			result = exp(-5.809+5.62*savi)
			return result
		
		def u_star( self, ublend, hblend, disp, z0m, psi_m):
			"""
			calculates the nominal wind speed
			u_star( ublend, hblend, disp, z0m, psi_m)
			"""
			ustar = 0.41*ublend/(log((hblend-disp)/z0m)-psi_m)
			return ustar
		
		def u_blend( self, u_hmoment, disp, hblend, z0m, hmoment):
			"""
			calculates the wind speed at blending height
			u_blend( self, u_hmoment, disp, hblend, z0m, hmoment)
			"""
			ublend=u_hmoment*(log(hblend-disp)-log(z0m))/(log(hmoment-disp)-log(z0m))
			return ublend
		
		def U_0(self, z0m, u, height_of_u):
			"""
			calculates the wind speed at 0 m height
			U_0(self, z0m, u, height_of_u)
			"""
			grass_height=0.15
			hu = height_of_u
			hg = grass_height
			u_0 = u2m*0.41*log(200/(hg/7))/(log(hu/(hg/7))*log(200/z0m))
			return u_0
		
		def roh_air( self, dem, tempka):
			"""
			calculates the Atmospheric Air Density.
			This is found in Bastiaanssen (1995).
			/* Atmospheric Air Density 
			* Requires Air Temperature and DEM*/
			"""
			b = (( tempka - (0.00627 * dem )) / tempka )
			result = 349.467 * pow( b , 5.26 ) / tempka
			if (result > 1.5):
				result = -999.99
			elif (result < 0.0):
				result = -999.99
			return result 
	
		def minmax( self, indataset ):
			#set up iteration variables
			tmin=400.0
			tmax=200.0
			#indataset = gdal.Open( infile, GA_ReadOnly )
			inband = indataset.GetRasterBand(1)
			for i in range(inband.YSize - 1, -1, -1):
				scanline = inband.ReadAsArray(0,i,inband.XSize,1,inband.XSize,1)
				for j in range(0, inband.XSize -1, 1):
					pixel = scanline[0][j]
					if(pixel<tmin):
						tmin=pixel
					elif(pixel>tmax):
						tmax=pixel
					else: pass
			#print "tmin =", tmin, "tmax =", tmax
			return (tmin,tmax)
	
		def minmax_temperature( self, temperature_array, elevation_array ):
			"""
			Looks for minimum maximum temperature in an image, needs altitude map for correction
			"""
			#set up iteration variables
			tmin=400.0
			tmax=200.0
			t0dem_min=400.0
			t0dem_max=200.0
			#set up altitude adjusted temperature
			t0dem=0.0016*elevation+temperature
			#start search for min max
			if(t0dem>273.15 and t0dem<t0dem_min):
				t0dem_min=t0dem
				tmin=temperature
			elif(t0dem>t0dem_max):
				t0dem_max=t0dem
				tmax=temperature
			return (tmin, tmax)
	
	
	# END OF ENERGY BALANCE EQUTATIONS
	
	# ETPOT FROM RS
	class et_pot_rs( object ):
		"""
		Generic remote sensing based ET potential using radiation:
		SOLARDAY, SOLARDAY3D, RNETDAY, ETPOTDAY
		"""
		def solarday( self, latitude, doy, tsw ):
			"""
			Average Solar Diurnal Radiation after Bastiaanssen (1995)
			tsw = 0.7 generally clear-sky Single-way transmissivity of the atmosphere [0.0-1.0]
			solarday(latitude, doy, tsw )
			"""
			PI=3.1415927
			ds = 1.0 + 0.01672 * sin(2*PI*(doy-93.5)/365.0)
			delta = 0.4093*sin((2*PI*doy/365)-1.39)
			
			temp =  lat * PI / 180.0
			ws = acos(-tan(temp)*tan(delta*PI/180.0))
			cosun = ws*sin(delta*PI/180.0)*sin(temp)+cos(delta*PI/180.0)*cos(temp)*sin(ws)
			result = ( cosun * 1367 * tsw ) / ( PI * ds * ds )
			return result
		
		def solarday3d( self, latitude, doy, tsw, slope, aspect ):
			"""
			// Average Solar Diurnal Radiation after Bastiaanssen (1995)
			// Includes Slope and aspect correction
			"""
			PI = 3.1415927
			ds = 1.0 + 0.01672 * sin(2 * PI * (doy - 93.5) / 365.0)
			delta = 0.4093 * sin((2 * PI * doy / 365) - 1.39)
			deltarad  = delta * PI / 180.0
			latrad 	  = latitude * PI / 180.0
			slrad  = slope * PI / 180.0
			asprad = aspect * PI / 180.0
			ws = acos(-tan(latrad)*tan(deltarad))
			temp1 = sin(deltarad) * sin(latrad) * cos(slrad)
			temp2 = sin(deltarad) * cos(latrad) * sin(slrad) * cos(asprad)
			temp3 = cos(deltarad) * cos(latrad) * cos(slrad) * cos(ws*PI/180.0)
			temp4 = cos(deltarad) * sin(slrad) * cos(asprad) * cos(ws*PI/180.0)
			temp5 = cos(deltarad) * sin(slrad) * sin(asprad) * sin(ws*PI/180.0)
			costheta = (temp1 - temp2 + temp3 + temp4 + temp5) / cos(slrad)
			result = ( costheta * 1367 * tsw ) / ( PI * ds * ds )
			return result
		
		def rnetday( self, albedo, solarday, tsw ):
			"""
			Average Diurnal Net Radiation after Bastiaanssen (1995)
			tsw = 0.7 generally clear-sky Single-way transmissivity of the atmosphere [0.0-1.0]
			output in W/m2
			rnetday( albedo, solarday, tsw )
			"""
			result = ((1.0 - albedo)*solar)-(110.0*tsw)
			return result
		
		def etpotday( self, albedo, solarday, temperature, tsw, roh_water ):
			"""
			Average Diurnal Potential ET after Bastiaanssen (1995) in mm/day
			tsw = 0.7 generally clear-sky Single-way transmissivity of the atmosphere [0.0-1.0]
			roh_water = 1005 generally for non muddy Density of water (~1000 g/m3)
			etpotday( albedo, solarday, temperature, tsw, roh_water )
			"""
			latent=(2.501-(0.002361*(temperature-273.15)))*1000000.0;
			result = ((((1.0 - albedo)*solarday)-(110.0*tsw))*86400.0*1000.0)/(latent*roh_water);
			return result
		
	# END OF ETPOT FROM RS
	
	# HARGREAVES ETo
	class et_ref_hg( object ):
		"""
		Hargreaves ET reference equations and modified ones:
		ORIGINAL, MH, SAMANI
		"""
		def original( self, rnet, temperature_avg, temperature_max, temperature_min, precipitation ):
			"""
			//Hargreaves et al, 1985.
			temperature_avg = average temperature [C]
			temperature_min = min temperature [C]
			temperature_max = max temperature [C]
			p = precipitation [mm/month]
			rnet = net radiation [W/m2]
			original( rnet, temperature_avg, temperature_max, temperature_min, precipitation )
			"""
			p = precipitation
			tavg = temperature_average
			tmin = temperature_min
			tmax = temperature_max
			td = tmax - tmin
			if (tavg > 100.0):
				tavg=tavg-273.15 #// in case Temperature is in Kelvin
			rnet = rnet * (84600.0 * 1000.0) #// convert W -> MJ/d
			result = 0.0023 * 0.408 * rnet * ( tavg + 17.8 ) * pow(td,0.5)
			return result
		
		def mh( self, rnet, temperature_avg, temperature_max, temperature_min, precipitation ):
			"""
			//Droogers and Allen, 2001.
			temperature_avg = average temperature [C]
			temperature_min = min temperature [C]
			temperature_max = max temperature [C]
			p = precipitation [mm/month]
			rnet = net radiation [W/m2]
			mh( rnet, temperature_avg, temperature_max, temperature_min, precipitation )
			"""
			p = precipitation
			tavg = temperature_average
			tmin = temperature_min
			tmax = temperature_max
			td = tmax - tmin
			if (tavg > 100.0):
				tavg=tavg-273.15	#//in case temperature is in Kelvin
			rnet = rnet * (84600.0 * 1000.0)	#// convert W -> MJ/d
			result = 0.0013 * 0.408 * rnet * ( tavg + 17.0 ) * pow((td - 0.0123*p),0.76)
			return result
		
		def samani( self, rnet, temperature_average, temperature_max, temperature_min ):
			"""
			Hargreaves-Samani, 1985. 
			temperature_avg = average temperature [C]
			temperature_min = min temperature [C]
			temperature_max = max temperature [C]
			rnet = net radiation [W/m2]
			samani(rnet,temperature_average,temperature_max,temperature_min)
			"""
			td = tmax - tmin
			if (tavg > 100.0):
				tavg=tavg-273.15 #// in case Temperature is in Kelvin
			rnet = rnet * (84600.0 * 1000.0) #// convert W -> MJ/d
			result = 0.0023 * 0.408 * rnet * pow(td,0.5) * ((tmax+tmin)/2+17.8)/2.45
			return result
	
	# END OF HARGREAVES ETo 
	
	# PENMAN MONTEITH ETP
	class et_pot_pm( object ):
		"""
		Potential Evapotranspiration Calculation with hourly/daily Penman-Monteith:
		ETP, OPENWATERETP, 
		"""
		def ETp(self, T, Z, u2, Rn, night, Rh, hc):
			"""
			Potential Evapotranspiration Calculation with hourly/daily Penman-Monteith
			T = Temperature raster map [C]
			u2 = Wind Speed raster map [ m/s ]
			Z = DEM raster map [m.a.s.l.]
			Rn = Net Solar Radiation raster map [MJ/m2/h]
			Rh = Relative Humidity raster map [%]
			hc = Crop height raster map [m]
			OUTPUT = output Reference Potential Evapotranspiration layer [mm/h]
			PM_ETp(T, Z, u2, Rn, night, Rh, hc)
			"""
			cp 	= 1.013		#[kj/kg*c]	specific heat of moist air 
			epsilon = 0.622		#[-]			ratio of molecular weigth of water to dry air
			po 	= 101.3		#[kpa]			atmospheric pressure at sea level
			tko 	= 293.16	#[k]			reference temperature at sea level
			eta 	= 0.0065	#[k/m]			constant lapse rate
			ao 	= 0		#[m]			altitude at sea level
			g 	= 9.81		#[m/s]			gravitational accelleration
			r 	= 287		#[j/kg*k]		specific gas constant
			zw 	= 2		#[m]			height of  wind measurements
			zh 	= 2		#[m]			height of  humidity measurements
			k 	= 0.41		#[-]			von karman constant	
			#/* calculus: mean saturation vapoure pressure [KPa] */
			ea = 0.61078*exp((17.27*T)/(T+237.3))
			
			#/* calculus: slope of vapoure pressure curve [KPa/C] */
			delta = (4098*ea)/pow((237.3+T),2)
				
			#/* calculus: latent heat vapourisation [MJ/kg]  */
			lmbda = 2.501 - (0.002361*T)
			
			#/* calculus: atmospheric pressure [KPa] */
			P = Po * pow(((Tko-eta*(Z-Ao))/Tko),(g/(eta*R)))
			
			#/* calculus: psichiometric constant [kPa/C] */
			gamma	= ((cp*P)/(epsilon*lmbda))*0.001
			
			#/* calculus: aerodynamic resistance [s/m] */
			if ( hc < 2 ):
				d	= (2/3)*hc
				Zom	= 0.123*hc
				Zoh	= 0.1*Zom
				ra	= ( log((Zw-d)/Zom) * log((Zh-d)/Zoh) ) / (k*k*u2)
			else:
				u10	= u2*(log((67.8*10)-5.42))/4.87
				ra	= 94 / u10
			#/* calculus: surface resistance [s/m]  */
			rs = 100/(0.5*24*hc)
			#/*calculus: modified psichiometric constant [kPa/C] */
			gstar = gamma*(1+(rs/ra))
			#/*calculus: net radiation [MJ/m2*d] */
			#/*Rn derived from r.sun */
			#/*calculus: soil heat flux [MJ/m2*d] */
			if (night==False):
				G=0.1*Rn
			else:
				G=0.5*Rn
			
			#/* calculus: radiation term [mm/h] */
			# ETrad = (delta/(delta+gstar))*((Rn-G)/(lmbda*1000000))
			ETrad = (delta/(delta+gstar))*((Rn-G)/lmbda) #/* torna da analisi dimensionale */
			
			#/* calculus: actual vapoure pressure [kPa] */
			ed = Rh*ea/100
			
			#/* calculus: virtual temperature [C] */
			Tkv = (T+273.15)/(1-(0.378*ed/P))
			
			#/* calculus: atmospheric density [Kg/m^3] */
			rho = P/(Tkv*R/100)
			
			#/* calculus: aerodynamic term [mm/h] */
			#/* ETaero = (0.001/lmbda)*(1/(delta+gstar))*(rho*cp/ra)*(ea-ed); */
			ETaero = (3.6/lmbda)*(1/(delta+gstar))*(rho*cp/ra)*(ea-ed); #/* torna da analisi dimensionale */
			#/* calculus: potential evapotranspiration [mm/h] */
			ETp = ETrad + ETaero
			return ETp
		
		def openwaterETp(self,  T, Z, u2, Rn, day, Rh, hc):
			"""
			Open Water Potential Evapotranspiration Calculation with hourly Penman-Monteith
			T = Temperature raster map [C]
			Z = DEM raster map [m a.s.l.]
			u2 = Wind Speed raster map [m/s]
			Rn = Net Solar Radiation raster map [MJ/m2/h]
			Rh = Relative Umidity raster map [%]
			hc = Crop height raster map [m]
			OUTPUT = output Reference Potential Evapotranspiration layer [mm/h]
			PM_openwaterETp( T, Z, u2, Rn, day, Rh, hc)
			"""
			cp 	= 1.013		#[kj/kg*C]	specific heat of moist air 
			epsilon = 0.622		#[-]			ratio of molecular weigth of water to dry air
			po 	= 101.3		#[kpa]			atmospheric pressure at sea level
			tko 	= 293.16	#[k]			reference temperature at sea level
			eta 	= 0.0065	#[k/m]			constant lapse rate
			ao 	= 0		#[m]			altitude at sea level
			g 	= 9.81		#[m/s]			gravitational accelleration
			r 	= 287		#[j/kg*k]		specific gas constant
			zw 	= 2		#[m]			height of  wind measurements
			zh 	= 2		#[m]			height of  humidity measurements
			k 	= 0.41		#[-]			von karman constant	
			cp 	= 1.013		#[kj/kg*C]	specific heat of moist air 
			epsilon = 0.622		#[-]			ratio of molecular weigth of water to dry air
			po 	= 101.3		#[kpa]			atmospheric pressure at sea level
			tko 	= 293.16	#[k]			reference temperature at sea level
			eta 	= 0.0065	#[k/m]			constant lapse rate
			ao 	= 0		#[m]			altitude at sea level
			g 	= 9.81		#[m/s]			gravitational accelleration
			r 	= 287		#[j/kg*K]		specific gas constant
			zw 	= 2		#[m]			height of  wind measurements
			zh 	= 2		#[m]			height of  humidity measurements
			k 	= 0.41		#[-]			von karman constant
			#/* calculus: mean saturation vapoure pressure [KPa] */
			ea = 0.61078*exp((17.27*T)/(T+237.3))
			#/* calculus: slope of vapour pressure curve [KPa/C] */
			delta = (4098*ea)/pow((237.3+T),2)
			#/* calculus: latent heat vapourisation [MJ/kg]  */
			lmbda = 2.501 - (0.002361*T)
			#/* calculus: atmospheric pressure [KPa] */
			P = Po * pow(((Tko-eta*(Z-Ao))/Tko),(g/(eta*R)))
			#/* calculus: di psichiometric constant [kPa/C] */
			gamma	= ((cp*P)/(epsilon*lmbda))*0.001
			#/*calculus: net radiation [MJ/m2*h] */
			#/*Rn derived from r.sun
			#/*calculus: actual vapour pressure [kPa] */
			ed = Rh*ea/100
			#/*calculus: aerodynamic term [mm/d] */
			#ETaero = 0.35*(0.5+(0.621375*u2/100))*7.500638*(ea-ed)
			#/*to convert mm/d to mm/h it results: */
			ETaero = (0.35/24)*(0.5+(0.621375*u2/100))*7.500638*(ea-ed)
			#/*calculus: potential evapotranspiration [mm/h] */
			ETp = (((Rn*delta)/lmbda)+(gamma*ETaero))/(delta+gamma)
			return ETp
	
	# END OF PENMAN MONTEITH ETP
	
	# PRESTLEY AND TAYLOR ETP
	class et_pot_pt( object ):
		"""
		diurnal evapotranspiration after Prestley and Taylor (1972) in mm/day:
		DAILY_ET, DELTA, GHAMMA, 
		Alpha = 1.26 for humid climate (relative humidity > 60%
		Alpha = 1.74 for semi-arid and arid climates especially and other areas
		After Shuttleworth, W.J., Evaporation, in Handbook of Hydrology, edited
		by D.R. Maidment, pp 4.1-4.53, McGraw-Hill, New York, 1993.
		"""
		def daily_et( self, alpha_pt, delta_pt, ghamma_pt, rnet, g0 ):
			"""
			Calculates the diurnal evapotranspiration after Prestley and Taylor (1972) in mm/day.
			alpha_pt = 1.26 , this is the recommended Prestley-Taylor Coefficient
			PT_daily_et( alpha_pt, delta_pt, ghamma_pt, rnet, g0 )
			"""
			result = (alpha_pt/28.588) * ( delta_pt / ( delta_pt + ghamma_pt ) ) * ( rnet - g0 )
			return result
		
		def delta( self, air_temperature ):
			"""
			Prestely and Taylor, 1972.
			PT_delta( air_temperature )
			"""
			if (air_temperature > 250.0):
				air_temperature = air_temperature - 273.15
			a = ( 17.27 * air_temperature ) / ( 237.3 + air_temperature )
			b = air_temperature + 237.3
			result = 2504.0 * exp(a) / pow(b,2)
			return result
		
		def ghamma( self, air_temperature, atmospheric_pressure ):
			"""
			Prestely and Taylor, 1972. 
			PT_ghamma( air_temperature, atmospheric_pressure )
			"""
			Cp = 1004.16
			if (air_temperature > 250.0):
				air_temperature = air_temperature - 273.15
			a = 0.622 * pow(10,7) * (2.501 - (2.361 * pow(10,-3) * air_temperature))
			result = Cp * atmospheric_pressure / a
			return result
	
	# END OF PRESTLEY AND TAYLOR ETP 
	
	# TWO-SOURCE ALGORITHM ETA
	class et_a_tsa( object ):
		"""
		Calculates the diurnal actual evapotranspiration after Chen et al. (2005)
		//Chen et al., 2005. IJRS 26(8):1755-1762.
		//Estimation of daily evapotranspiration using a two-layer remote sensing model.
		The tsa_tempk C code is wrong, not working. the rest is apparently fine.
		"""
		def main(self, rnet,fv,tempk,alb,ndvi,disp,z0,z0s,hv,z,w,uz,tempka,time,sunh):
			"""
			Calculates the diurnal actual evapotranspiration after Chen et al. (2005)
			//Chen et al., 2005. IJRS 26(8):1755-1762.
			//Estimation of daily evapotranspiration using a two-layer remote sensing model.
			The tsa_tempk C code is wrong, not working. the rest is apparently fine.
			"""
			#//Calculate Net radiation fractions
			rn_g 		= rn_g( rnet, fv)
			rn_v 		= rn_v( rnet, fv)
			#//Calculate temperature fractions
			tempk_v 	= tempk_v( tempk, fv)
			tempk_g 	= tempk_g( tempk, tempk_v, fv)
			#//Calculate soil heat flux fractions
			g0_g 		= g_0g( rnet)
			g0_v 		= g_0v( alb, ndvi, tempk_v, rnet)
			#//Data necessary for sensible heat flux calculations
			if(disp<0.0 and z0<0.0 and hv<0.0):
				ra 	= 0.0
				rg 	= 0.0
				rv 	= 0.0
			else:
				ra	= ra( disp, z0, hv, z, uz, tempka, tempk_v)
				rg	= rg( disp, z0, z0s, hv, z, w, uz, tempka, tempk_v)
				rv	= rv( disp, z0, hv, z, w, uz, tempka, tempk_v)
				
			#//Calculate sensible heat flux fractions
			h_g 		= h_g( tempk_g, tempk_v, tempka, rg, rv, ra )
			h_v 		= h_v( tempk_g, tempk_v, tempka, rg, rv, ra )
			#//Calculate LE
			le_inst_v	= rn_v - g0_v - h_v
			le_inst_g	= rn_g - g0_g - h_g
			le_inst		= le_inst_v + le_inst_g
			#//Calculate ET
			daily_et	= daily_et( le_inst, time, sunh)
		
		def g0_g( self, rnet ):
			"""
			Chen et al., 2005. IJRS 26(8):1755-1762.
			Estimation of daily evapotranspiration using a two-layer remote sensing model.
			soil heat flux for bare soil
			TSA_g0_g( rnet )
			"""
			result = (rnet * 0.4)
			return result
		
		
		def TSA_g0_v( self, albedo, ndvi, temperature_vegetation, rnet ):
			"""
			Chen et al., 2005. IJRS 26(8):1755-1762.
			Estimation of daily evapotranspiration using a two-layer remote sensing model.
			soil heat flux for vegetation
			TSA_g0_v( albedo, ndvi, temperature_vegetation, rnet )
			"""
			a = (0.0032 * albedo) + (albedo * albedo)
			b = (1 - 0.978 * pow(ndvi,4))
			result = (rnet * (temperature_vegetation-273.15) / albedo) * a * b
			return result
		
		def TSA_h_g( self, temperature_ground, temperature_vegetation, temperature_air, roughness_ground, roughness_vegetation, roughness_air ):
			"""
			Chen et al., 2005. IJRS 26(8):1755-1762.
			Estimation of daily evapotranspiration using a two-layer remote sensing model.
			Sensible heat flux for ground
			TSA_h_g( temperature_ground, temperature_vegetation, temperature_air, roughness_ground, roughness_vegetation, roughness_air )
			"""
			r_g = roughness_ground
			r_v = roughness_vegetation
			r_a = roughness_air
			tempk_v = temperature_vegetation
			tempk_g = temperature_ground
			tempk_a = temperature_air
			a = r_g * tempk_v - r_g * tempk_a + r_v * tempk_g - r_v * tempk_a
			b = r_v * r_g + r_g * r_a + r_v * r_a
			c = r_a * ( a / b )
			result = (tempk_g - c - tempk_a) / r_g
			return result
		
		def TSA_h_v( self, temperature_ground, temperature_vegetation, temperature_air, roughness_ground, roughness_vegetation, roughness_air ):
			"""
			Chen et al., 2005. IJRS 26(8):1755-1762.
			Estimation of daily evapotranspiration using a two-layer remote sensing model.
			Sensible heat flux for vegetation
			TSA_h_v(temperature_ground, temperature_vegetation, temperature_air, roughness_ground, roughness_ground, roughness_air )
			"""
			r_g = roughness_ground
			r_v = roughness_vegetation
			r_a = roughness_air
			tempk_v = temperature_vegetation
			tempk_g = temperature_ground
			tempk_a = temperature_air
			a = r_g * tempk_v - r_g * tempk_a + r_v * tempk_g - r_v * tempk_a
			b = r_v * r_g + r_g * r_a + r_v * r_a
			c = r_a * ( a / b )
			result = (tempk_v - c - tempk_a) / r_v 
			return result	
		
		def TSA_ra( self, displacement, surface_roughness, vegetation_height, reference_height, wind_speed_ref_h, temperature_air, temperature_vegetation):
			"""
			//Chen et al., 2005. IJRS 26(8):1755-1762.
			//Estimation of daily evapotranspiration using a two-layer remote sensing model.
			
			// d = zero plane displacement (m)
			// z0 = surface roughness length gouverning heat and vapour transfers (m)
			// h = vegetation height (m)
			// z = reference height of air temperature and humidity measurements (m)
			// u_z = wind speed at reference height z (m/s)
			// tempk_a = air temperature (at reference height z?) (K)
			// tempk_v = surface temperature of vegetation (K)
			
			//If h (vegetation height) is given then d and z0 will be:
			//d = 0.63h
			//z0 = 0.13h
			//If d OR z0 are positive a relationship will find the second one
			//based on the equations above
			//If d AND z0 are positive they are used regardless of h values
			Roughness air
			TSA_ra( displacement, surface_roughness, vegetation_height, reference_height, wind_speed_ref_h, temperature_air, temperature_vegetation)
			"""
			u_z = wind_speed_ref_h
			z0 = surface_roughness
			z = reference_height
			h = vegetation_height
			d = displacement
			tempk_v = temperature_vegetation
			tempk_a = temperature_air
			vonKarman = 0.41 #// von Karman constant
			g = 9.81  #// gravitational acceleration (m/s)
			#//Deal with input of vegetation height
			if ( h > 0.0 ):
				d = 0.63*h
				z0 = 0.13*h
			#//Deal with input of displacement height
			elif (d > 0.0 and z0 < 0.0):
				z0 = 0.13 * (d/0.63)
			#//Deal with input of surface roughness length
			elif (d < 0.0 and z0 > 0.0):
				d = 0.63 * (z0/0.13)
			else: pass
			ra_0 = pow(log ((z-d)/z0),2) / ( pow(vonKarman,2)* u_z )
			#//psi, molength, u_star: Ambast S.K., Keshari A.K., Gosain A.K. 2002.
			#//An operational model for estimating evapotranspiration 
			#//through Surface Energy Partitioning (RESEP).
			#//International Journal of Remote Sensing, 23, pp. 4917-4930.
			u_star = vonKarman * u_z / log((z-d)/z0)
			molength = u_star*((tempk_v+tempk_a)/2)/(vonKarman*g*(tempk_a-tempk_v)/u_z)
			
			if( ((z-d)/molength) < -0.03 ):
				psi = pow((1-16*((z-d)/molength)),0.5)
			else:
				psi = (1+5*((z-d)/molength))
			#//psi & ra: Wang, C.Y., Niu Z., Tang H.J. 2002. 
			#//Technology of Earth Observation and Precision agriculture
			#//(Beijing: Science Press)
			result = ra_0 * ( 1 + (psi*(z-d)/z0) )
			return result
		
		def TSA_rg( self, displacement, surface_roughness, surface_roughness_soil, vegetation_height, reference_height, leaf_weight, wind_speed_ref_h, temperature_air, temperature_vegetation ):
			"""
			//Chen et al., 2005. IJRS 26(8):1755-1762.
			//Estimation of daily evapotranspiration using a two-layer remote sensing model.
			// d = zero plane displacement (m)
			// z0 = surface roughness length gouverning heat and vapour transfers (m)
			// z0s = bare soil surface roughness length (m)
			// h = vegetation height (m)
			// w = weight of leaf (g)
			// z = reference height of air temperature and humidity measurements (m)
			// u_z = wind speed at reference height (m/s)
			// u_h = wind speed at plant height (m/s)
			// tempk_a = air temperature (at reference height z?) (K)
			// tempk_v = surface temperature of vegetation (K)
			//If h (vegetation height) is given then d and z0 will be:
			//d = 0.63h
			//z0 = 0.13h
			//If d OR z0 are positive a relationship will find the second one
			//based on the equations above
			//If d AND z0 are positive they are used regardless of h values
			Resistance of bare soil
			TSA_rg(displacement, surface_roughness, surface_roughness_soil, vegetation_height, reference_height, leaf_weight, wind_speed_ref_h, temperature_air, temperature_vegetation)
			"""
			z0s = surface_roughness_soil
			w = leaf_weight
			u_z = wind_speed_ref_h
			z0 = surface_roughness
			z = reference_height
			h = vegetation_height
			d = displacement
			tempk_v = temperature_vegetation
			tempk_a = temperature_air
			vonKarman = 0.41 #// von Karman constant
			g = 9.81 #// gravitational acceleration (m/s)
			#//Deal with input of vegetation height
			if ( h > 0.0 ):
				d = 0.63*h
				z0 = 0.13*h
			#//Deal with input of displacement height
			elif (d > 0.0 and z0 < 0.0):
				z0 = 0.13 * (d/0.63)
			#//Deal with input of surface roughness length
			elif (d < 0.0 and z0 > 0.0):
				d = 0.63 * (z0/0.13)
			else: pass
			if ( h < 0.0 ):
				h = d / 0.63
			#//molength, u_star: Ambast S.K., Keshari A.K., Gosain A.K. 2002.
			#//An operational model for estimating evapotranspiration 
			#//through Surface Energy Partitioning (RESEP).
			#//International Journal of Remote Sensing, 23, pp. 4917-4930.
			u_star = vonKarman * u_z / log((z-d)/z0)
			molength = u_star*((tempk_v+tempk_a)/2)/(vonKarman*g*(tempk_a-tempk_v)/u_z)
			#//rv: Choudhury B.J. and Monteith J.L. 1988. 
			#//A four-layer model for the heat budget of homogeneous land surfaces.
			#//Quarterly Journal of the Royal Meteorological Society,114,pp.373-398.
			k_h = 1.5*pow(vonKarman,2)*(h-d)*u_z/(log((z-d)/z0))
			alpha = 1.0 / ((d/h)*log((h-d)/z0))
			temp = h*exp(alpha)/(alpha*k_h)
			result = temp*(exp(-alpha*z0s/h)-exp(-alpha*(d+z0)/h))
			return result
		
		def TSA_rn_g( self, rnet, vegetation_fraction):
			"""
			//Chen et al., 2005. IJRS 26(8):1755-1762.
			//Estimation of daily evapotranspiration using a two-layer remote sensing model.
			Bare soil net radiation
			TSA_rn_g( rnet, vegetation_fraction)
			"""
			result = (1 - vegetation_fraction) * rnet
			return result
		
		def TSA_rn_v( self, rnet, vegetation_fraction):
			"""
			//Chen et al., 2005. IJRS 26(8):1755-1762.
			//Estimation of daily evapotranspiration using a two-layer remote sensing model.
			Vegetation net radiation
			TSA_rn_v( rnet, vegetation_fraction)
			"""
			result = vegetation_fraction * rnet
			return result
		
		def TSA_rv( self, displacement, surface_roughness, vegetation_height, reference_height, leaf_weight, wind_speed_ref_h, temperature_air, temperature_vegetation):
			"""
			//Chen et al., 2005. IJRS 26(8):1755-1762.
			//Estimation of daily evapotranspiration using a two-layer remote sensing model.
			// d = zero plane displacement (m)
			// z0 = surface roughness length gouverning heat and vapour transfers (m)
			// h = vegetation height (m)
			// w = weight of leaf (g)
			// z = reference height of air temperature and humidity measurements (m)
			// u_z = wind speed at reference height (m/s)
			// u_h = wind speed at plant height (m/s)
			// tempk_a = air temperature (at reference height z?) (K)
			// tempk_v = surface temperature of vegetation (K)
			//If h (vegetation height) is given then d and z0 will be:
			//d = 0.63h
			//z0 = 0.13h
			//If d OR z0 are positive a relationship will find the second one
			//based on the equations above
			//If d AND z0 are positive they are used regardless of h values
			vegetation roughness
			TSA_rv( displacement, surface_roughness, vegetation_height, reference_height, leaf_weight, wind_speed_ref_h, temperature_air, temperature_vegetation)
			"""
			w = leaf_weight
			u_z = wind_speed_ref_h
			z0 = surface_roughness
			z = reference_height
			h = vegetation_height
			d = displacement
			tempk_v = temperature_vegetation
			tempk_a = temperature_air
			vonKarman = 0.41; #// von Karman constant
			g = 9.81 ; #// gravitational acceleration (m/s)
			#//Deal with input of vegetation height
			if ( h > 0.0 ):
				d = 0.63*h
				z0 = 0.13*h
			#//Deal with input of displacement height
			elif (d > 0.0 and z0 < 0.0):
				z0 = 0.13 * (d/0.63)
			#//Deal with input of surface roughness length
			elif (d < 0.0 and z0 > 0.0):
				d = 0.63 * (z0/0.13)
			#//molength, u_star: Ambast S.K., Keshari A.K., Gosain A.K. 2002.
			#//An operational model for estimating evapotranspiration 
			#//through Surface Energy Partitioning (RESEP).
			#//International Journal of Remote Sensing, 23, pp. 4917-4930.
			u_star = vonKarman * u_z / log((z-d)/z0)
			molength = u_star*((tempk_v+tempk_a)/2)/(vonKarman*g*(tempk_a-tempk_v)/u_z)
			#//rv: Choudhury B.J. and Monteith J.L. 1988. 
			#//A four-layer model for the heat budget of homogeneous land surfaces.
			#//Quarterly Journal of the Royal Meteorological Society,114,pp.373-398.
			u_h = 1.5*u_z*log((h-d)/z0)/(log((z-d)/z0))
			alpha = 1.0 / ((d/h)*log((h-d)/z0))
			result = 50.0*alpha*pow(abs(w/u_h),0.5) / (molength*(1-exp(-alpha/2)))
			return result
		
		def TSA_t_g( self, temperature, temperature_vegetation, vegetation_fraction):
			"""
			//Temperature of ground from Tvegetation
			//Based on two sources pixel split
			//Chen et al., 2005. IJRS 26(8):1755-1762.
			//Estimation of daily evapotranspiration using a two-layer remote sensing model.
			Ground temperature, bare soil
			TSA_t_g( temperature, temperature_vegetation, vegetation_fraction)
			"""
			result = (temperature - (vegetation_fraction*temperature_vegetation)) / (1 - vegetation_fraction)
			return result
		
		def TSA_t_v( self, temperature, vegetation_fraction):
			"""
			//Temperature of vegetation
			//Based on two sources pixel split
			//Chen et al., 2005. IJRS 26(8):1755-1762.
			//Estimation of daily evapotranspiration using a two-layer remote sensing model.
			Vegetation temperature
			TSA_t_v( temperature, vegetation_fraction)
			"""
			fv = vegetation_fraction
			a = (fv-(pow(fv,0.5)*pow(0.97,0.25)))/((pow((1-fv),0.5)*pow(0.93,0.25))-1-fv)
			result = temperature / ( fv - (1 - fv) * a )
			return result
		
		def TSA_daily_et( self, et_instantaneous, time, sunshine_hours ):
			"""
			Xie, X.Q., 1991: Estimation of daily evapo-transpiration (ET) from one time-of-day remotely sensed canopy temperature. Remote Sensing of Environment China, 6, pp.253-259. 
			Transforms instantaneous ET into daily ET
			TSA_daily_et( et_instantaneous, time, sunshine_hours )
			"""
			PI = 3.1415927
			# Daily ET hours
			n_e = sunshine_hours - 2.0
			result = et_instantaneous * (2 * n_e) / (PI * sin(PI*time/n_e))
			return result
	
	# END OF TWO-SOURCE ALGORITHM ETA
	
	
	class utils( object ):
		"""
		Various Utilities:
		DATE2DOY,
		"""
		# DATE2DOY AND DOY2DATE FUNCTIONS
		def date2doy( day, month, year):
			"""
			/*********************************************/
			/*This program converts day/month/year to doy*/
			/*********************************************/
			date2doy( day, month, year)
			"""
			leap = 0
			day_month_tot = 0
			doy = 0
			year=int(year)
			month=int(month)
			day=int(day)
			#/*printf("Date is %i/%i/%i\n", day, month, year)*/
		
			if (month == 1):
				day_month_tot = 0
			elif (month == 2):
				day_month_tot = 31
			elif (month == 3):
				day_month_tot = 59
			elif (month == 4):
				day_month_tot = 90
			elif (month == 5):
				day_month_tot = 120
			elif (month == 6):
				day_month_tot = 151
			elif (month == 7):
				day_month_tot = 181
			elif (month == 8):
				day_month_tot = 212
			elif (month == 9):
				day_month_tot = 243
			elif (month == 10):
				day_month_tot = 273
			elif (month == 11):
				day_month_tot = 304
			elif (month == 12):
				day_month_tot = 334
			
			#/* Leap year if dividing by 4 leads % 0.0*/
			if (year/4*4 == year):
				leap = 1
			
			doy = day_month_tot + day
			if( doy > 59 ):
				doy = day_month_tot + day + leap
			return doy
		
		# END OF DATE2DOY AND DOY2DATE FUNCTIONS 
