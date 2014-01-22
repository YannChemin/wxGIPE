
# HARGREAVES ETo

"""
Hargreaves ET reference equations and modified ones.
"""
def original( rnet, temperature_avg, temperature_max, temperature_min, precipitation ):
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

def mh( rnet, temperature_avg, temperature_max, temperature_min, precipitation ):
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

def samani( rnet, temperature_average, temperature_max, temperature_min ):
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
