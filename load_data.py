# 
# File:    load_data.py 
# 
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     August 2012
# 
# Summary of File: 
# 
#   Loads raw data from SDSS and Redmapepr into classes
#   and writes the classes to the database.
# 

#--------------------------------------------------------------------------------
# Settings
#--------------------------------------------------------------------------------
maxNumberOfBcgs = 100
maxNumberOfGalaxies = 10000

#--------------------------------------------------------------------------------
# Create a session
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

#--------------------------------------------------------------------------------
# Read in physics data from txt files
#--------------------------------------------------------------------------------
# from numpy import loadtxt
# bcgtxt = loadtxt('data/bcg.txt', usecols=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
# galaxytxt = loadtxt('data/galaxy.txt', usecols=(1, 2, 3, 4, 5))
# # objID, ra, dec, deVAB_r, deVABErr_r, deVPhi_r, lnLDeV_r
# photoObjdeV = loadtxt('data/SDSS_DR8_galaxy_shapes_devphi.txt', usecols=(0, 1, 2, 5, 10, 15, 20))

#--------------------------------------------------------------------------------
# Read in physics data from FITS files
#--------------------------------------------------------------------------------
import pyfits
inFileSDSS = pyfits.open('data/SDSS_DR8_galaxies.fit')
dataSDSSGalaxies = inFileSDSS[1].data

inFileRedmapper = pyfits.open('data/dr8_redmapper_v3.4_nordcenter_catalog.fit')
dataRedmapperCGs = inFileRedmapper[1].data

#--------------------------------------------------------------------------------
# Declare classes and commit them to database
#--------------------------------------------------------------------------------
from classes import Bcg, Galaxy
counter = 0
for MEM_MATCH_ID,RA,DEC,MODEL_MAG,MODEL_MAGERR,IMAG,IMAG_ERR,ZRED,ZRED_E,BCG_SPEC_Z,Z_SPEC_INIT,Z_INIT,Z,LAMBDA_CHISQ,LAMBDA_CHISQ_E,SCALEVAL,MASKFRAC,C_LAMBDA,C_LAMBDA_ERR,Z_LAMBDA,Z_LAMBDA_E,LNLAMLIKE,LNBCGLIKE,LNLIKE,RA_ORIG,DEC_ORIG,P_BCG in dataRedmapperCGs:
	
	if (BCG_SPEC_Z == -1.): break
	
	bcg = Bcg(RA, DEC, BCG_SPEC_Z)
	bcg.pBCG = P_BCG
	bcg.richness = Z_LAMBDA_E
	
	session.add(bcg)
	
	counter += 1
	if (counter == maxNumberOfBcgs): break
	if (counter % 100 == 0):
		print counter , " # - comitting bcgs to database..."
		session.commit()

counter = 0

for objID, ra, dec, z, zErr, deVAB_r, deVABErr_r, deVPhi_r, lnLDeV_r in dataSDSSGalaxies:
	galaxy = Galaxy(ra, dec, z)
	galaxy.objID = objID
	galaxy.zErr = zErr
	galaxy.deVAB_r = deVAB_r
	galaxy.deVABErr_r = deVABErr_r
	galaxy.deVPhi_r = deVPhi_r
	galaxy.lnLDeV_r = lnLDeV_r
	
	session.add(galaxy)
	
	counter += 1
	if (counter == maxNumberOfGalaxies): break
	if (counter % 1000 == 0):
		print counter , " # - comitting galaxies to database..."
		session.commit()

#--------------------------------------------------------------------------------
# Commit changes to database
#--------------------------------------------------------------------------------
session.commit()
