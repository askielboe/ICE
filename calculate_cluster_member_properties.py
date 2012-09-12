# 
# File:    calculate_cluster_member_properties.py
# 
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     September 2012
# 
# Summary of File: 
# 
#   Calculates quantities which require full association and BCG match information
# 

#--------------------------------------------------------------------------------
# Create a session
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

from classes import Association
from functions import calcSmallestAngleBetweenBCGAndAgalaxy

q = session.query(Association).filter(Association.positionAngle > -1)

counter = 0
for association in q.all():
	association.angleToBCGMajorAxis = calcSmallestAngleBetweenBCGAndAgalaxy(association.positionAngle,association.bcg.deVPhi_r)
	counter += 1
	if (counter % 1000 == 0):
		print counter , " # - calculating cluster member properties..."
		session.commit()

session.commit()
