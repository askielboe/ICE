# 
# File:    calculate_associations.py 
# 
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     August 2012
# 
# Summary of File: 
# 
#   Assigns galaxies to clusters using SQL joins
# 

#--------------------------------------------------------------------------------
# Settings
#--------------------------------------------------------------------------------
maxComovingDistance = 6.0
maxVrel = 4000.0

#--------------------------------------------------------------------------------
# Create a session
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

#--------------------------------------------------------------------------------
# Define (physics) functions (move to seperate file?)
#--------------------------------------------------------------------------------
def calcSQLDist(ra1, dec1, ra2, dec2):
	from sqlalchemy import func
	from math import pi
	return func.acos(func.sin(dec1*pi/180.0)*func.sin(dec2*pi/180.0) + func.cos(dec1*pi/180.0)*func.cos(dec2*pi/180.0)*func.cos((ra1-ra2)*pi/180.0))

def calcDist(ra1, dec1, ra2, dec2):
	from math import pi, cos, sin, acos
	try:
		return acos(sin(dec1*pi/180.0)*sin(dec2*pi/180.0) + cos(dec1*pi/180.0)*cos(dec2*pi/180.0)*cos((ra1-ra2)*pi/180.0))
	except ValueError:
		return -1.0

def calcSQLSimpleDist(ra1, dec1, ra2, dec2):
	from sqlalchemy import func
	return func.abs(dec1 - dec2) + func.abs(ra1 - ra2)

def calcVrel(z1, z2):
	SPEED_OF_LIGHT = 299792.0 # km/s
	return SPEED_OF_LIGHT * ((1. + z1) / (1. + z2) - 1.)

#--------------------------------------------------------------------------------
# Assign galaxies to clusters
#--------------------------------------------------------------------------------
from sqlalchemy import func
import math
from classes import Bcg, Galaxy, Association

counter = 0
for bcg, galaxy in session.query(Bcg,Galaxy).\
filter(calcSQLSimpleDist(Galaxy.ra, Galaxy.dec, Bcg.ra, Bcg.dec) < 1.135).\
filter(func.abs(calcVrel(Bcg.z, Galaxy.z)) < maxVrel).\
filter(calcSQLDist(Bcg.ra, Bcg.dec, Galaxy.ra, Galaxy.dec) < func.asin( maxComovingDistance / Bcg.da )).\
all():
	# If the BCG-galaxy pair passes selection apertures then we add an association
	vrel = calcVrel(bcg.z, galaxy.z)
	sep = calcDist(bcg.ra, bcg.dec, galaxy.ra, galaxy.dec)
	dist = math.tan(sep) * bcg.da
	
	association = Association(dist=dist, vrel=vrel)
	association.galaxy = galaxy
	bcg.galaxies.append(association)
	
	#print galaxy, " added to ", bcg
	
	counter += 1
	if (counter % 1000 == 0):
		print counter , " # - assigning galaxies to clusters..."
		session.commit()

print "Total number of galaxies assigned to clusters = ", counter

#--------------------------------------------------------------------------------
# Commit changes to database
#--------------------------------------------------------------------------------
session.commit()
