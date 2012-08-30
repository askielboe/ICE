# 
# File:    match_objects.py 
# 
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     August 2012
# 
# Summary of File: 
# 
#   Matches astronomical objects across tables
# 

#--------------------------------------------------------------------------------
# Settings
#--------------------------------------------------------------------------------
maxSumDist = 0.00001
maxZDiff = 0.0001

#--------------------------------------------------------------------------------
# Create a session
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

#--------------------------------------------------------------------------------
# Match BCGs with galaxies from SDSS
#--------------------------------------------------------------------------------
from physics import calcSQLSumDist
from classes import Bcg, Galaxy
from sqlalchemy import func

counter = 0
q = session.query(Bcg, Galaxy)
# Do rough cut on position
q = q.filter(calcSQLSumDist(Galaxy.ra, Galaxy.dec, Bcg.ra, Bcg.dec) < maxSumDist)
# Do cut on redshift difference
q = q.filter(func.abs(Bcg.z - Galaxy.z) < maxZDiff)

# while (len(q.all()) > 1):
# 	print "WARNING: Found several matches! Trying with tighter cuts.."
# 	print "len(q.all()) = ", len(q.all())
# 	print "maxSumDist = ", maxSumDist, "maxZDiff = ", maxZDiff
# 	maxSumDist -= maxSumDist/10.
# 	maxZDiff -= maxZDiff/10.
# 	# Do rough cut on position
# 	q = q.filter(calcSQLSumDist(Galaxy.ra, Galaxy.dec, Bcg.ra, Bcg.dec) < maxSumDist)
# 	# Do cut on redshift difference
# 	q = q.filter(func.abs(Bcg.z - Galaxy.z) < maxZDiff)

for bcg, galaxy in q.all():	
	bcg.sdss_galaxy = galaxy
	counter += 1

session.commit()

print "Total number of BCGs matched to SDSS galaxies = ", counter
