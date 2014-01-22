
# ALBEDO FUNCTIONS


def aster( greenchan, redchan, nirchan, swirchan1, swirchan2, swirchan3, swirchan4, swirchan5, swirchan6 ):
	"""
	Broadband albedo Aster (Careful the DN multiplier! Here it is 1000.0, output range should be [0.0-1.0])
	albedo_aster( greenchan, redchan, nirchan, swirchan1, swirchan2, swirchan3, swirchan4, swirchan5, swirchan6 )
	"""
	if( greenchan < 0 or redchan < 0 or nirchan < 0 or swirchan1 < 0 or swirchan2 < 0 or swirchan3 < 0 or swirchan4 < 0 or swirchan5 < 0 or swirchan6 < 0 ):
		result = -1.0
	else:
		result = ( 0.09*greenchan + 0.06*redchan + 0.1*nirchan + 0.092*swirchan1 + 0.035*swirchan2 + 0.04*swirchan3 + 0.047*swirchan4 + 0.07*swirchan5 + 0.068*swirchan6 ) / ((0.09+0.06+0.1+0.092+0.035+0.04+0.047+0.07+0.068)*1000.0)
	return result

def landsat( bluechan, greenchan, redchan, nirchan, chan5, chan7 ):
	"""
	Broadband albedo Landsat 5TM and 7ETM+ (maybe others too but not sure)
	albedo_landsat( bluechan, greenchan, redchan, nirchan, chan5, chan7 )
	"""
	if( bluechan < 0 or greenchan < 0 or redchan < 0 or nirchan < 0 or chan5 < 0 or chan7 < 0):
		result = -1.0
	else:
		result = ( 0.293*bluechan + 0.274*greenchan + 0.233*redchan + 0.156*nirchan + 0.033*chan5 + 0.011*chan7 )
	return result

def modis( redchan, nirchan, chan3, chan4, chan5, chan6, chan7 ):
	"""
	Broadband albedo MODIS (Careful the DN multiplier! Here it is 10000.0, output range should be [0.0-1.0])
	albedo_modis( redchan, nirchan, chan3, chan4, chan5, chan6, chan7 )
	"""
	if( nirchan < 0 or redchan < 0 or chan3 < 0 or chan4 < 0 or chan5 < 0 or chan6 < 0 or chan7 < 0):
		result = -1.0
	else:
		result = ((0.22831*redchan + 0.15982*nirchan + 0.09132*(chan3+chan4+chan5) + 0.10959*chan6 + 0.22831*chan7 ) / 10000.0 )
	return result
	
def avhrr( redchan, nirchan ):
	"""
	Broadband albedo NOAA AVHRR 14 (maybe others too but not sure). Careful the DN multiplier! Here it is 10000.0, output range should be [0.0-1.0]
	albedo_avhrr( redchan, nirchan )
	"""
	if( nirchan < 0 or redchan < 0 ):
		result = -1.0
	else:
		result = (( 0.035+ 0.545*nirchan - 0.32*redchan) / 10000.0 )
	return result

# END OF ALBEDO FUNCTIONS
