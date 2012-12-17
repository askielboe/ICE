# 
# File:    create_database.py 
# 
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     August 2012
# 
# Summary of File: 
# 
#   Routines for matching obejcts for adding information from various catalogs
# 	

# from classes import *
# 
# def is_same_object():
# 	# Add photometric de Vaucouleurs fit information (r band only)
# 	for objID, ra, dec, z, zErr, deVAB_r, deVABErr_r, deVPhi_r, lnLDeV_r in dataSDSSGalaxies:
# 		if (bcg.ra == ra and bcg.dec == dec):
# 			bcg.objID = objID
# 			bcg.deVAB_r = deVAB_r
# 			bcg.deVABErr_r = deVABErr_r
# 			bcg.deVPhi_r = deVPhi_r
# 			bcg.lnLDeV_r = lnLDeV_r
# 			break
# 	if (bcg.objID == -1):
# 		print "ERROR: No photometric object found for ", bcg

from classes import SDSSGalaxy, importClass

# Create session
from database_operations import create_session
session = create_session()

# Put import data in import table using the import class
import pyfits
inFileSDSSMags = pyfits.open('data/SDSS_DR8_galaxies_magnitudes.fit')
dataSDSSGalaxiesMags = inFileSDSSMags[1].data

counter = 0
for objID, deVMag_u, deVMag_r in dataSDSSGalaxiesMags:
	importInstance = importClass(objID, deVMag_u, deVMag_r)
	session.add(importInstance)
	counter += 1
	if (counter % 1000 == 0):
		print(counter , " # - comitting import objects to database...")
		session.commit()

session.commit()

# Match import objects with current objects
counter = 0
q = session.query(SDSSGalaxy, importClass.float1, importClass.float2)
q = q.join(importClass, SDSSGalaxy.objID == importClass.id)

for (galaxy,float1,float2)  in q.yield_per(5):
	galaxy.deVMag_u = float1
	galaxy.deVMag_r = float2
	counter += 1
	if (counter % 1000 == 0):
		print(counter , " # - comitting galaxies to database...")
		session.commit()

session.commit()

print(counter, " galaxies updated with new data")
print("Total galaxies = ", len(q.all()))