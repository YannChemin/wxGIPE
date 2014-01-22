def g0(albedo, ndvi, temperature, r_net, time, roerink):
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
