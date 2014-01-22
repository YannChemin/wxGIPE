# PRESTLEY AND TAYLOR ETP
def daily_et( alpha_pt, delta_pt, ghamma_pt, rnet, g0 ):
	"""
	Calculates the diurnal evapotranspiration after Prestley and Taylor (1972) in mm/day.
	alpha_pt = 1.26 , this is the recommended Prestley-Taylor Coefficient
	PT_daily_et( alpha_pt, delta_pt, ghamma_pt, rnet, g0 )
	"""
	result = (alpha_pt/28.588) * ( delta_pt / ( delta_pt + ghamma_pt ) ) * ( rnet - g0 )
	return result

def delta( air_temperature ):
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

def ghamma( air_temperature, atmospheric_pressure ):
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
