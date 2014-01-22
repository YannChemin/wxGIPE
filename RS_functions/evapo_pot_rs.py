"""
Generic remote sensing based ET potential using radiation
"""
def solarday(latitude, doy, tsw ):
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

def solarday3d( latitude, doy, tsw, slope, aspect ):
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

def rnetday( albedo, solarday, tsw ):
	"""
	Average Diurnal Net Radiation after Bastiaanssen (1995)
	tsw = 0.7 generally clear-sky Single-way transmissivity of the atmosphere [0.0-1.0]
	output in W/m2
	rnetday( albedo, solarday, tsw )
	"""
	result = ((1.0 - albedo)*solar)-(110.0*tsw)
	return result

def etpotday( albedo, solarday, temperature, tsw, roh_water ):
	"""
	Average Diurnal Potential ET after Bastiaanssen (1995) in mm/day
	tsw = 0.7 generally clear-sky Single-way transmissivity of the atmosphere [0.0-1.0]
	roh_water = 1005 generally for non muddy Density of water (~1000 g/m3)
	etpotday( albedo, solarday, temperature, tsw, roh_water )
	"""
	latent=(2.501-(0.002361*(temperature-273.15)))*1000000.0;
	result = ((((1.0 - albedo)*solarday)-(110.0*tsw))*86400.0*1000.0)/(latent*roh_water);
	return result