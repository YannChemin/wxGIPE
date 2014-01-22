"""
Energy balance functions
"""
def eta( r_net_day, evaporative_fraction, temperature):
	"""
	eta( r_net_day, evaporative_fraction, temperature)
	"""
	t_celsius = temperature - 273.15
	latent 	  = 86400.0/((2.501-0.002361*t_celsius)*pow(10,6))
	result 	  = r_net_day * evaporative_fraction * latent
	return result

def evapfr( r_net, g0, h0 ):
	"""
	calculates the evaporative fraction after bastiaanssen (1995).
	It takes input of Net Radiation (see r.sun,r.eb.netrad), soil heat flux (see r.eb.g0) and sensible heat flux (see r.eb.h0). 
	evaporative fraction
	evapfr( r_net, g0, h0 )
	"""
	result = (r_net - g0 - h0) / (r_net - g0)
	return result

def soilmoisture( evaporative_fraction ):
	"""
	soil moisture in the root zone
	Makin, Molden and Bastiaanssen, 2001
	soilmoisture( evaporative_fraction )
	"""
	result = (exp((evaporative_fraction-1.2836)/0.4213))/0.511
	return result

def g0(albedo, ndvi, temperature, r_net, time, roerink):
	"""
	Calculates the soil heat flux approximation (g0) after bastiaanssen (1995).
	It takes input of Albedo, NDVI, Surface Skin temperature, Net Radiation (see r.sun), time of satellite overpass, and a flag for the Roerink empirical modification from the HAPEX-Sahel experiment. 
	Soil heat flux
	g0(albedo, ndvi, temperature, r_net, time, roerink)
	"""
	if (time<=9.0||time>15.0):
		r0_coef = 1.1
	elif (time>9.0&&time<=11.0):
		r0_coef = 1.0
	elif (time>11.0&&time<=13.0):
		r0_coef = 0.9
	elif (time>13.0&&time<=15.0):
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

def h0( air_density, air_specific_heat, heat_aerodynamic_resistance, temperature_difference):
	"""
	calculates the sensible heat flux approximation (h0), a flag allows the use of an affine transform from surface temperature after bastiaanssen (1995).
	It takes input of air density, air specific heat, difference of temperature between surface skin and a height of about 2m above, and the aerodynamic resistance to heat transport. 
	"""
	result = air_density * air_specific_heat * temperature_difference / heat_aerodynamic_resistance
	return result

def rah_fixed_dt( u2m, roh_air, cp, dt, disp, z0m, z0h, tempk):
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

def h0_SEBAL( tempk_water, tempk_desert, t0_dem, tempk, ndvi, ndvi_max, dem, rnet_desert, g0_desert,  t0_dem_desert, u2m, dem_desert):
	"""
	SEBAL Loop
	"""
	ITER_MAX = 10
	debug = 0
	if debug :
		print "*****************************\n")
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
		print "u_0 		= ", u_0);
		print "rah[0] 		= ", rah[0], "s/m"
		print "h[0] 		= ", h[0], "W/m2"
	#/*----------------------------------------------------------------*/
	#/*Main iteration loop of SEBAL*/
	zom[0] = zom0
	for ic in range (ITER_MAX):
		if debug :
			printf("\n ******** ITERATION ",ic,"*********"
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

def z0m( savi ):
	"""
	calculates the momentum roughness length (z0m) and optionally the surface roughness for heat transport (z0h) as per SEBAL requirements from bastiaanssen (1995).
	This version is calculating from a SAVI with an empirical equation, as seen in Pawan (2004).
	This is a typical input to sensible heat flux computations of any energy balance modeling.
	// Momentum roughness length (z0m) as seen in Pawan (2004)
	z0m( savi )
	"""
	result = exp(-5.809+5.62*savi)
	return result

def u_star( ublend, hblend, disp, z0m, psi_m):
	"""
	calculates the nominal wind speed
	u_star( ublend, hblend, disp, z0m, psi_m)
	"""
	ustar = 0.41*ublend/(log((hblend-disp)/z0m)-psi_m)
	return ustar

def u_blend( u_hmoment, disp, hblend, z0m, hmoment):
	"""
	calculates the wind speed at blending height
	//Wind speed at blending height
	"""
	ublend=u_hmoment*(log(hblend-disp)-log(z0m))/(log(hmoment-disp)-log(z0m))
	return ublend


def roh_air( dem, tempka):
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
