#
# File:    physics.py
#
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     August 2012
#
# Summary of File:
#
#   Library of functions doing physical calculations.
#

def calcSQLDist(ra1, dec1, ra2, dec2):
	from sqlalchemy import func
	from math import pi
	return func.acos(func.sin(dec1*pi/180.0)*func.sin(dec2*pi/180.0) + func.cos(dec1*pi/180.0)*func.cos(dec2*pi/180.0)*func.cos((ra1-ra2)*pi/180.0))

def calcAngularSeparation(ra1, dec1, ra2, dec2):
	from math import pi, cos, sin, acos
	if (ra1 == ra2 and dec1 == dec2):
		return 0.0
	try:
		return acos(sin(dec1*pi/180.0)*sin(dec2*pi/180.0) + cos(dec1*pi/180.0)*cos(dec2*pi/180.0)*cos((ra1-ra2)*pi/180.0))
	except ValueError:
		return 0.0

def calcSQLSumDist(ra1, dec1, ra2, dec2):
	from sqlalchemy import func
	return func.abs(dec1 - dec2) + func.abs(ra1 - ra2)

def calcVrel(z1, z2):
	SPEED_OF_LIGHT = 299792.0 # km/s
	return SPEED_OF_LIGHT * ((1. + z1) / (1. + z2) - 1.)

def calcPositionAngleCartesianApproximation(ra1, dec1, ra2, dec2):
	return -1.0

def calc_angular_diameter_distance_noradiation(z):
	# Function to calculate the proper distance (in Mpc) in a concordance cosmology
	# using numerical integration
	from scipy.integrate import quad
	c = 299792.458 # km/s
	H0 = 70.0 # km/s/Mpc
	Omega_m = 0.3
	proper_distance = quad(lambda x: Omega_m**-0.5 / ((1+x)**3.0 - 1.0 + Omega_m**-1.0)**0.5, 0.0, float(z))
	angular_diameter_distance = [c/H0 * distance / (1.0+z) for distance in proper_distance]
	return angular_diameter_distance

def cosmocalc_angular_diameter_distance(z):
	# Function to calculate the proper distance (in Mpc) in a concordance cosmology
	# using numerical integration
	from math import sqrt, sin, exp

	H0 = 70                         # Hubble constant
	WM = 0.3                        # Omega(matter)
	WV = 1.0 - WM - 0.4165/(H0*H0)  # Omega(vacuum) or lambda

	# initialize constants
	WR = 0.        # Omega(radiation)
	WK = 0.        # Omega curvaturve = 1-Omega(total)
	c = 299792.458 # velocity of light in km/sec
	DTT = 0.5      # time from z to now in units of 1/H0
	age = 0.5      # age of Universe in units of 1/H0
	zage = 0.1     # age of Universe at redshift z in units of 1/H0
	DCMR = 0.0     # comoving radial distance in units of c/H0
	DA = 0.0       # angular size distance
	DA_Mpc = 0.0
	a = 1.0        # 1/(1+z), the scale factor of the Universe
	az = 0.5       # 1/(1+z(object))

	h = H0/100.
	WR = 4.165E-5/(h*h)   # includes 3 massless neutrino species, T0 = 2.72528
	WK = 1-WM-WR-WV
	az = 1.0/(1+1.0*z)
	age = 0.
	n =1000         # number of points in integrals

	for i in range(n):
		a = az*(i+0.5)/n
		adot = sqrt(WK+(WM/a)+(WR/(a*a))+(WV*a*a))
		age = age + 1./adot

	zage = az*age/n
	DTT = 0.0
	DCMR = 0.0

	# do integral over a=1/(1+z) from az to 1 in n steps, midpoint rule
	for i in range(n):
		a = az+(1-az)*(i+0.5)/n
		adot = sqrt(WK+(WM/a)+(WR/(a*a))+(WV*a*a))
		DTT = DTT + 1./adot
		DCMR = DCMR + 1./(a*adot)

	DTT = (1.-az)*DTT/n
	DCMR = (1.-az)*DCMR/n
	age = DTT+zage

	# tangential comoving distance
	ratio = 1.00
	x = sqrt(abs(WK))*DCMR
	if x > 0.1:
		if WK > 0:
			ratio =  0.5*(exp(x)-exp(-x))/x

		else:
			ratio = sin(x)/x

	else:
		y = x*x
		if WK < 0: y = -y
		ratio = 1. + y/6. + y*y/120.

	DCMT = ratio*DCMR
	DA = az*DCMT
	DA_Mpc = (c/H0)*DA

	return DA_Mpc

def calcAngleToBCGMajorAxis():
	return -1.0