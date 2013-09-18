#
# File:    calculate_derived_quantities.py
#
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     August 2012
#
# Summary of File:
#
#   Calculates physically derived quantities. Often requires to assume a given cosmology.
#

#--------------------------------------------------------------------------------
# Create a session
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

#--------------------------------------------------------------------------------
# Calculate angular diameter distances for all SDSS galaxies
#--------------------------------------------------------------------------------
from physics import cosmocalc_angular_diameter_distance

# # ===== Da for SDSS Galaxies =====
# from classes import SDSSGalaxy
# counter = 0
# for galaxy in session.query(SDSSGalaxy).all():
# 	galaxy.da = cosmocalc_angular_diameter_distance(galaxy.z)
# 	counter += 1
# 	if (counter % 1000 == 0):
# 		print counter , " # - calculating derived quantities..."
# 		session.commit()
#
# session.commit()

# ===== Da for Redmapper =====
from classes import Redmapper
counter = 0
for cg in session.query(Redmapper).all():
	cg.da = cosmocalc_angular_diameter_distance(cg.z)
	counter += 1
	if (counter % 1000 == 0):
		print counter , " # - calculating derived quantities..."
		session.commit()

session.commit()