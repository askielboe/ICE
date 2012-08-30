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
# Assign galaxies to clusters
#--------------------------------------------------------------------------------
from physics import calcSQLSumDist, calcSQLDist, calcVrel, calcDist
from classes import Bcg, Galaxy, Association
import math
from sqlalchemy import func

#queryBcgDa = session.query(Bcg.id, Galaxy.da).filter(Bcg.sdss_galaxy_id == Galaxy.id).subquery('queryBcgDa')
#queryGalaxyNotBcg = session.query(Galaxy).join(Bcg).filter(Galaxy.id != Bcg.sdss_galaxy_id).subquery('queryGalaxyNotBcg')

counter = 0
q = session.query(Galaxy, Bcg)

# Don't add BCGs to BCGs
#q = q.filter(Galaxy.id != Bcg.sdss_galaxy_id)

# Do rough cut on position
q = q.filter(calcSQLSumDist(Galaxy.ra, Galaxy.dec, Bcg.ra, Bcg.dec) < 1.135)

# Do cut on relative velocity
q = q.filter(func.abs(calcVrel(Bcg.z, Galaxy.z)) < maxVrel)

# Do cut on projected separation
q = q.filter(calcSQLDist(Bcg.ra, Bcg.dec, Galaxy.ra, Galaxy.dec) < func.asin( maxComovingDistance / Bcg.da ))

for galaxy, bcg in q.all():
	# If the BCG-galaxy pair passes selection apertures then we add an association
	vrel = calcVrel(bcg.z, galaxy.z)
	sep = calcDist(bcg.ra, bcg.dec, galaxy.ra, galaxy.dec)
	dist = math.tan(sep) * bcg.da
	
	association = Association(dist=dist, vrel=vrel)
	association.galaxy = galaxy
	#association.positionAngle = 
	bcg.associated_galaxies.append(association)
	
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
