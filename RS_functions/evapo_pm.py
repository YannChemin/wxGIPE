# PENMAN MONTEITH ETP

def ETp(T, Z, u2, Rn, night, Rh, hc):
	"""
	Potential Evapotranspiration Calculation with hourly/daily Penman-Monteith
	T = Temperature raster map [°C]
	Z = DEM raster map [m a.s.l.]
	u2 = Wind Speed raster map [m/s]
	Rn = Net Solar Radiation raster map [MJ/m2/h]
	Rh = Relative Umidity raster map [%]
	hc = Crop height raster map [m]
	OUTPUT = output Reference Potential Evapotranspiration layer [mm/h]
	PM_ETp(T, Z, u2, Rn, night, Rh, hc)
	"""
	cp 	= 1.013		#[kj/kg*�c]	specific heat of moist air 
	epsilon = 0.622		#[-]			ratio of molecular weigth of water to dry air
	po 	= 101.3		#[kpa]			atmospheric pressure at sea level
	tko 	= 293.16	#[k]			reference temperature at sea level
	eta 	= 0.0065	#[k/m]			constant lapse rate
	ao 	= 0		#[m]			altitude at sea level
	g 	= 9.81		#[m/s]			gravitational accelleration
	r 	= 287		#[j/kg*k]		specific gas constant
	zw 	= 2		#[m]			height of  wind measurements
	zh 	= 2		#[m]			height of  humidity measurements
	k 	= 0.41		#[-]			von karman constant	
	#/* calculus: mean saturation vapoure pressure [KPa] */
	ea = 0.61078*exp((17.27*T)/(T+237.3))
	
	#/* calculus: slope of vapoure pressure curve [KPa/�C] */
	delta = (4098*ea)/pow((237.3+T),2)
		
	#/* calculus: latent heat vapourisation [MJ/kg]  */
	lambda = 2.501 - (0.002361*T)
	
	#/* calculus: atmospheric pressure [KPa] */
	P = Po * pow(((Tko-eta*(Z-Ao))/Tko),(g/(eta*R)))
	
	#/* calculus: psichiometric constant [kPa/�C] */
	gamma	= ((cp*P)/(epsilon*lambda))*0.001
	
	#/* calculus: aerodynamic resistance [s/m] */
	if ( hc < 2 ):
		d	= (2/3)*hc
		Zom	= 0.123*hc
		Zoh	= 0.1*Zom
		ra	= ( log((Zw-d)/Zom) * log((Zh-d)/Zoh) ) / (k*k*u2)
	else:
		u10	= u2*(log((67.8*10)-5.42))/4.87
		ra	= 94 / u10
	
	#/* calculus: surface resistance [s/m]  */
	rs = 100/(0.5*24*hc);
	
	#/*calculus: modified psichiometric constant [kPa/�C] */
	gstar = gamma*(1+(rs/ra));

	#/*calculus: net radiation [MJ/m2*d] */
	#/*Rn derived from r.sun */
	
	#/*calculus: soil heat flux [MJ/m2*d] */
	if (night==FALSE)
		G=0.1*Rn;
	else
		G=0.5*Rn;
	
	#/* calculus: radiation term [mm/h] */
	/* ETrad = (delta/(delta+gstar))*((Rn-G)/(lambda*1000000)); */
	ETrad = (delta/(delta+gstar))*((Rn-G)/lambda); /* torna da analisi dimensionale */
	
	#/* calculus: actual vapoure pressure [kPa] */
	ed = Rh*ea/100;
	
	#/* calculus: virtual temperature [�C] */
	Tkv = (T+273.15)/(1-(0.378*ed/P));
	
	#/* calculus: atmospheric density [Kg/m^3] */
	rho = P/(Tkv*R/100);
	
	/* calculus: aerodynamic term [mm/h] */
	/* ETaero = (0.001/lambda)*(1/(delta+gstar))*(rho*cp/ra)*(ea-ed); */
	ETaero = (3.6/lambda)*(1/(delta+gstar))*(rho*cp/ra)*(ea-ed); #/* torna da analisi dimensionale */
	#/* calculus: potential evapotranspiration [mm/h] */
	ETp = ETrad + ETaero
	return ETp

def openwaterETp( T, Z, u2, Rn, day, Rh, hc):
	"""
	Open Water Potential Evapotranspiration Calculation with hourly Penman-Monteith
	T = Temperature raster map [°C]
	Z = DEM raster map [m a.s.l.]
	u2 = Wind Speed raster map [m/s]
	Rn = Net Solar Radiation raster map [MJ/m2/h]
	Rh = Relative Umidity raster map [%]
	hc = Crop height raster map [m]
	OUTPUT = output Reference Potential Evapotranspiration layer [mm/h]
	PM_openwaterETp( T, Z, u2, Rn, day, Rh, hc)
	"""
	cp 	= 1.013		#[kj/kg*�c]	specific heat of moist air 
	epsilon = 0.622		#[-]			ratio of molecular weigth of water to dry air
	po 	= 101.3		#[kpa]			atmospheric pressure at sea level
	tko 	= 293.16	#[k]			reference temperature at sea level
	eta 	= 0.0065	#[k/m]			constant lapse rate
	ao 	= 0		#[m]			altitude at sea level
	g 	= 9.81		#[m/s]			gravitational accelleration
	r 	= 287		#[j/kg*k]		specific gas constant
	zw 	= 2		#[m]			height of  wind measurements
	zh 	= 2		#[m]			height of  humidity measurements
	k 	= 0.41		#[-]			von karman constant	
	cp 	= 1.013		#[kj/kg*�c]	specific heat of moist air 
	epsilon = 0.622		#[-]			ratio of molecular weigth of water to dry air
	po 	= 101.3		#[kpa]			atmospheric pressure at sea level
	tko 	= 293.16	#[k]			reference temperature at sea level
	eta 	= 0.0065	#[k/m]			constant lapse rate
	ao 	= 0		#[m]			altitude at sea level
	g 	= 9.81		#[m/s]			gravitational accelleration
	r 	= 287		#[j/kg*k]		specific gas constant
	zw 	= 2		#[m]			height of  wind measurements
	zh 	= 2		#[m]			height of  humidity measurements
	k 	= 0.41		#[-]			von karman constant
	#/* calculus: mean saturation vapoure pressure [KPa] */
	ea = 0.61078*exp((17.27*T)/(T+237.3))
	#/* calculus: slope of vapoure pressure curve [KPa/�C] */
	delta = (4098*ea)/pow((237.3+T),2)
	#/* calculus: latent heat vapourisation [MJ/kg]  */
	lambda = 2.501 - (0.002361*T)
	#/* calculus: atmospheric pressure [KPa] */
	P = Po * pow(((Tko-eta*(Z-Ao))/Tko),(g/(eta*R)))
	#/* calculus: di psichiometric constant [kPa/�C] */
	gamma	= ((cp*P)/(epsilon*lambda))*0.001
	#/*calculus: net radiation [MJ/m2*h] */
	#/*Rn derived from r.sun
	#/*calculus: actual vapoure pressure [kPa] */
	ed = Rh*ea/100
	#/*calculus: aerodynamic term [mm/d] */
	#ETaero = 0.35*(0.5+(0.621375*u2/100))*7.500638*(ea-ed)
	#/*to convert mm/d to mm/h it results: */
	ETaero = (0.35/24)*(0.5+(0.621375*u2/100))*7.500638*(ea-ed)
	#/*calculus: potential evapotranspiration [mm/h] */
	ETp = (((Rn*delta)/lambda)+(gamma*ETaero))/(delta+gamma)
	return ETp

# END OF PENMAN MONTEITH ETP
 
