# PRE-PROCESSING FUNCTIONS

def read_met_file_landsat7(metfName):
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


def dn2rad_landsat7( Lmin, LMax, QCalMax, QCalmin, DN ):
	"""
	Conversion of DN to Radiance for Landsat 7ETM+
	http://ltpwww.gsfc.nasa.gov/IAS/handbook/handbook_htmls/chapter11/chapter11.html#section11.3 
	dn2rad_landsat7( Lmin, LMax, QCalMax, QCalmin, DN )
	"""
	gain 	= (LMax-Lmin)/(QCalMax-QCalmin)
	offset 	= Lmin
	result 	= gain * (1.0*DN - QCalmin) + offset
	return result

def rad2ref_landsat7( radiance, doy, sun_elevation, k_exo ):
	"""
	Conversion of Radiance to Reflectance Top Of Atmosphere for Landsat 7ETM+
	rad2ref_landsat7( radiance, doy, sun_elevation, k_exo )
	"""
	PI = 3.1415927
	ds = ( 1.0 + 0.01672 * sin( 2 * PI * ( doy - 93.5 ) / 365 ) )
	result = (radiance/((cos((90-sun_elevation)*PI/180)/(PI*ds*ds))*k_exo))
	return result

def tempk_landsat7( l6 ):
	"""
	Surface temperature for Landsat 7ETM+
	tempk_landsat7( l6 )
	"""
	result = 1282.71 / (log ((666.09 / (l6)) + 1.0))
	return result

def dn2rad_aster( Lgain, Loffset, DN ):
	"""
	Conversion of DN to Radiance for Aster
	rad2ref_aster(  Lgain, Loffset, DN  )
	"""
	result = Lgain * DN + Loffset
	return result

def rad2ref_aster( radiance, doy, sun_elevation, k_exo ):
	"""
	Conversion of Radiance to Reflectance for ASTER
	rad2ref_aster( radiance, doy, sun_elevation, k_exo )
	"""
	PI = 3.1415927
	ds = ( 1.0 + 0.01672 * sin( 2 * PI * ( doy - 93.5 ) / 365 ) )
	result = radiance / ( ( cos ( ( 90.0 - sun_elevation ) * PI / 180.0 ) / ( PI * ds * ds ) ) * k_exo )
	return result

def Lgain(spacecraft_id, sensor_id, band_id):
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

def Loffset(spacecraft_id, sensor_id, band_id):
	"""Offset for Dn to Rad conversion
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

def kexo(spacecraft_id, sensor_id, band_id):
	"""Sun exo-atmospheric irridiance [W/m2/sr]
	This is used for processing surface reflectance.
	Spacecraft_id: Landsat7
		Sensor_id: ETM+
			band_id: band1, band2, band3, band4, band5, band7, band8
	Spacecraft_id: Terra
		Sensor_id: Aster
			band_id: band1, band2, band3, band4, band5, band7, band8, band9
	kexo(spacecraft_id, sensor_id, band_id)
	"""
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

