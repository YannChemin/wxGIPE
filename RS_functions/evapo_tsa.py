# TWO-SOURCE ALGORITHM ETA

"""
Calculates the diurnal actual evapotranspiration after Chen et al. (2005)
//Chen et al., 2005. IJRS 26(8):1755-1762.
//Estimation of daily evapotranspiration using a two-layer remote sensing model.
The tsa_tempk C code is wrong, not working. the rest is apparently fine.
"""
def main(rnet,fv,tempk,alb,ndvi,disp,z0,z0s,hv,z,w,uz,tempka,time,sunh):
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
	if(disp<0.0&&z0<0.0&&hv<0.0):
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

def g0_g( rnet ):
	"""
	Chen et al., 2005. IJRS 26(8):1755-1762.
	Estimation of daily evapotranspiration using a two-layer remote sensing model.
	soil heat flux for bare soil
	TSA_g0_g( rnet )
	"""
	result = (rnet * 0.4)
	return result


def TSA_g0_v( albedo, ndvi, temperature_vegetation, rnet ):
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

def TSA_h_g( temperature_ground, temperature_vegetation, temperature_air, roughness_ground, roughness_vegetation, roughness_air ):
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

def TSA_h_v(temperature_ground, temperature_vegetation, temperature_air, roughness_ground, roughness_ground, roughness_air ):
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

def TSA_ra( displacement, surface_roughness, vegetation_height, reference_height, wind_speed_ref_h, temperature_air, temperature_vegetation):
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
	elif (d > 0.0 && z0 < 0.0):
		z0 = 0.13 * (d/0.63)
	#//Deal with input of surface roughness length
	elif (d < 0.0 && z0 > 0.0):
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

def TSA_rg(displacement, surface_roughness, surface_roughness_soil, vegetation_height, reference_height, leaf_weight, wind_speed_ref_h, temperature_air, temperature_vegetation):
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
	elif (d > 0.0 && z0 < 0.0):
		z0 = 0.13 * (d/0.63)
	#//Deal with input of surface roughness length
	elif (d < 0.0 && z0 > 0.0):
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

def TSA_rn_g( rnet, vegetation_fraction):
	"""
	//Chen et al., 2005. IJRS 26(8):1755-1762.
	//Estimation of daily evapotranspiration using a two-layer remote sensing model.
	Bare soil net radiation
	TSA_rn_g( rnet, vegetation_fraction)
	"""
	result = (1 - vegetation_fraction) * rnet
	return result

def TSA_rn_v( rnet, vegetation_fraction):
	"""
	//Chen et al., 2005. IJRS 26(8):1755-1762.
	//Estimation of daily evapotranspiration using a two-layer remote sensing model.
	Vegetation net radiation
	TSA_rn_v( rnet, vegetation_fraction)
	"""
	result = vegetation_fraction * rnet
	return result

def TSA_rv( displacement, surface_roughness, vegetation_height, reference_height, leaf_weight, wind_speed_ref_h, temperature_air, temperature_vegetation):
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
	elif (d > 0.0 && z0 < 0.0):
		z0 = 0.13 * (d/0.63)
	#//Deal with input of surface roughness length
	elif (d < 0.0 && z0 > 0.0):
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

def TSA_t_g( temperature, temperature_vegetation, vegetation_fraction):
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

def TSA_t_v( temperature, vegetation_fraction):
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

def TSA_daily_et( et_instantaneous, time, sunshine_hours ):
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
 
