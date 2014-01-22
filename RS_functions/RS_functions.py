
def emissivity_generic( ndvi ):
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
