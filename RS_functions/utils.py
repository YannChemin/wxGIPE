
# DATE2DOY AND DOY2DATE FUNCTIONS

def date2doy( day, month, year):
	"""
	/*********************************************/
	/*This program converts day/month/year to doy*/
	/*********************************************/
	date2doy( day, month, year)
	"""
	leap = 0
	day_month_tot = 0
	doy = 0

#/*printf("Date is %i/%i/%i\n", day, month, year)*/

	if (month == 1):
		day_month_tot = 0
	elif (month == 2):
		day_month_tot = 31
	elif (month == 3):
		day_month_tot = 59
	elif (month == 4):
		day_month_tot = 90
	elif (month == 5):
		day_month_tot = 120
	elif (month == 6):
		day_month_tot = 151
	elif (month == 7):
		day_month_tot = 181
	elif (month == 8):
		day_month_tot = 212
	elif (month == 9):
		day_month_tot = 243
	elif (month == 10):
		day_month_tot = 273
	elif (month == 11):
		day_month_tot = 304
	elif (month == 12):
		day_month_tot = 334
	
	#/* Leap year if dividing by 4 leads % 0.0*/
	if (year/4*4 == year):
		leap = 1
	
	doy = day_month_tot + day
	if( doy > 59 ):
		doy = day_month_tot + day + leap
	return doy

# END OF DATE2DOY AND DOY2DATE FUNCTIONS 
