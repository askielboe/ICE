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
from physics import calcSQLSumDist, calcSQLDist, calcVrel, calcAngularSeparation
from classes import Redmapper, SDSSGalaxy, Association
import math
from sqlalchemy import func

#queryBcgDa = session.query(Bcg.id, Galaxy.da).filter(Bcg.sdss_galaxy_id == Galaxy.id).subquery('queryBcgDa')
#queryGalaxyNotBcg = session.query(Galaxy).join(Bcg).filter(Galaxy.id != Bcg.sdss_galaxy_id).subquery('queryGalaxyNotBcg')

counter = 0
q = session.query(SDSSGalaxy, Redmapper)

# Do rough cut on position
q = q.filter(calcSQLSumDist(SDSSGalaxy.ra, SDSSGalaxy.dec, Redmapper.ra, Redmapper.dec) < 1.135)

# Do cut on relative velocity
q = q.filter(func.abs(calcVrel(Redmapper.z, SDSSGalaxy.z)) < maxVrel)

# Do cut on projected separation
q = q.filter(calcSQLDist(Redmapper.ra, Redmapper.dec, SDSSGalaxy.ra, SDSSGalaxy.dec) < func.asin( maxComovingDistance / Redmapper.da ))

for galaxy, bcg in q.all():
	# If the BCG-galaxy pair passes selection apertures then we add an association
	vrel = calcVrel(bcg.z, galaxy.z)
	sep = calcAngularSeparation(bcg.ra, bcg.dec, galaxy.ra, galaxy.dec)
	dist = math.tan(sep) * bcg.da

	association = Association(dist=dist, vrel=vrel)
	association.galaxy = galaxy
	from functions import calcPositionAngleEofNRelativeToCenterInDegreesSpherical
	association.positionAngle = calcPositionAngleEofNRelativeToCenterInDegreesSpherical([galaxy.ra,galaxy.dec],[bcg.ra,bcg.dec])
	bcg.associated_sdss_galaxies.append(association)

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
