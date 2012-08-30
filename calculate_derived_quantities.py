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
from classes import Bcg

for bcg in session.query(Bcg):
	bcg.da = cosmocalc_angular_diameter_distance(bcg.z)

session.commit()