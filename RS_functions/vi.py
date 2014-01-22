
# VI FUNCTIONS
def arvi( redchan, nirchan, bluechan ):
	"""
	Atmospheric Resistant Vegetation Index: ARVI is resistant to atmospheric effects (in comparison to the NDVI) and is accomplished by a self correcting process for the atmospheric effect in the red channel, using the difference in the radiance between the blue and the red channels.(Kaufman and Tanre 1996).
	arvi( redchan, nirchan, bluechan )
	"""
	redchan = 1.0*redchan
	nirchan = 1.0*nirchan
	bluechan = 1.0*bluechan
	result = (nirchan - (2.0*redchan - bluechan)) / ( nirchan + (2.0*redchan - bluechan))
	return result

def dvi( redchan, nirchan ):
	"""
	DVI: Difference Vegetation Index
	dvi( redchan, nirchan )
	"""
	redchan = 1.0*redchan
	nirchan = 1.0*nirchan
	result = ( nirchan - redchan )
	return result

def gari( redchan, nirchan, bluechan, greenchan ):
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

def gemi( redchan, nirchan ):
	"""
	GEMI: Global Environmental Monitoring Index
	gemi( redchan, nirchan )
	"""
	redchan = 1.0*redchan
	nirchan = 1.0*nirchan
	result = (( (2*((nirchan * nirchan)-(redchan * redchan))+1.5*nirchan+0.5*redchan) /(nirchan + redchan + 0.5)) * (1 - 0.25 * (2*((nirchan * nirchan)-(redchan * redchan))+1.5*nirchan+0.5*redchan) /(nirchan + redchan + 0.5))) -( (redchan - 0.125) / (1 - redchan))
	return result

def gvi( bluechan, greenchan, redchan, nirchan, chan5chan, chan7chan):
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

def ipvi( redchan, nirchan ):
	"""
	IPVI: Infrared Percentage Vegetation Index 
			NIR	
		IPVI = --------
			NIR+red
	ipvi( redchan, nirchan )
	"""
	redchan = 1.0*redchan
	nirchan = 1.0*nirchan
	if( ( nirchan + redchan ) ==  0.0 ):
		result = -1.0
	else:
		result = ( nirchan ) / ( nirchan + redchan )
	return result

def msavi2( redchan, nirchan ):
	"""
	MSAVI2: second Modified Soil Adjusted Vegetation Index
	MSAVI2 = (1/2)*(2(NIR+1)-sqrt((2*NIR+1)^2-8(NIR-red)))
	msavi2( redchan, nirchan )
	"""
	redchan = 1.0*redchan
	nirchan = 1.0*nirchan
	result =( 1.0 / 2.0 ) * ( 2.0 * ( nirchan + 1.0 ) - sqrt ( ( 2 * nirchan + 1.0 ) * ( 2.0 * nirchan + 1.0 ) ) - ( 8.0 * ( nirchan - redchan ) ) )
	return result

def msavi( redchan, nirchan ):
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

def ndvi( redchan, nirchan ):
	"""
	Normalized Difference Vegetation Index
	ndvi( redchan, nirchan )
	"""
	redchan = 1.0*redchan
	nirchan = 1.0*nirchan
	if( ( nirchan + redchan ) ==  0.0 ):
		result = -1.0
	else:
		result = ( nirchan - redchan ) / ( nirchan + redchan )
	return result

def pvi( redchan, nirchan ):
	"""
	PVI: Perpendicular Vegetation Index
	PVI = sin(a)NIR-cos(a)red for a  isovegetation lines (lines of equal vegetation) would all be parallel to the soil line therefore a=1
	pvi( redchan, nirchan )
	"""

	redchan = 1.0*redchan
	nirchan = 1.0*nirchan
	result = (sin(1.0) * nirchan ) / ( cos(1.0) * redchan )
	return result

def savi( redchan, nirchan ):
	"""
	Soil Adjusted Vegetation Index
	savi( redchan, nirchan )
	"""
	redchan = 1.0*redchan
	nirchan = 1.0*nirchan
	if( ( nirchan + redchan + 0.5 ) ==  0.0 ):
		result = -1.0
	else:
		result = ((1.0+0.5)*( nirchan - redchan )) / ( nirchan + redchan +0.5)
	return result

def sr( redchan, nirchan ):
	"""
	Simple Vegetation ratio
	sr( redchan, nirchan )
	"""
	redchan = 1.0*redchan
	nirchan = 1.0*nirchan
	result =(nirchan/redchan)
	return result

def wdvi( redchan, nirchan, soil_line_weight ):
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