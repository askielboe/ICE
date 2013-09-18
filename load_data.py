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
maxNumberOfBcgs = 100000000
maxNumberOfGalaxies = 100000000
nWorkers = 20

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

inFileRedmapper = pyfits.open('data/dr8_redmapper_v3.4_nordcenter_catalog.fit')
dataRedmapperCGs = inFileRedmapper[1].data

#--------------------------------------------------------------------------------
# Declare classes and commit them to database
#--------------------------------------------------------------------------------
from classes import Redmapper, SDSSGalaxy
counter = 0

# # Declare sessions
# sessions = []
# for i in range(nWorkers):
# 	session = create_session()
# 	sessions.append(session)
from classes import Redmapper
def appendToDatabase(data_in):
	for RA, DEC, BCG_SPEC_Z, P_BCG, LAMBDA_CHISQ in data_in:
		bcg = Redmapper(RA, DEC, BCG_SPEC_Z)
		bcg.pBCG = P_BCG
		bcg.lambda_chisq = LAMBDA_CHISQ
	session.add(bcg)

#import multiprocessing
#jobs = []
#from multiprocessing import Pool
#po = Pool(processes=nWorkers)

n = 0
data = []
for MEM_MATCH_ID,RA,DEC,MODEL_MAG,MODEL_MAGERR,IMAG,IMAG_ERR,ZRED,ZRED_E,BCG_SPEC_Z,Z_SPEC_INIT,Z_INIT,Z,LAMBDA_CHISQ,LAMBDA_CHISQ_E,SCALEVAL,MASKFRAC,C_LAMBDA,C_LAMBDA_ERR,Z_LAMBDA,Z_LAMBDA_E,LNLAMLIKE,LNBCGLIKE,LNLIKE,RA_ORIG,DEC_ORIG,P_BCG in dataRedmapperCGs:

	if (BCG_SPEC_Z == -1.): continue

	bcg = Redmapper(RA, DEC, BCG_SPEC_Z)
	bcg.mem_match_id = MEM_MATCH_ID
	bcg.pBCG = P_BCG
	bcg.lambda_chisq = LAMBDA_CHISQ
	session.add(bcg)

	#data.append([RA, DEC, BCG_SPEC_Z, P_BCG, LAMBDA_CHISQ])

	#po.apply_async(appendToDatabase, args=(RA, DEC, BCG_SPEC_Z, P_BCG, LAMBDA_CHISQ))

	#result = po.apply_async(appendToDatabase, args=(RA, DEC, BCG_SPEC_Z, P_BCG, LAMBDA_CHISQ))
	#bcg = result.get()
	#print bcg
	#session.add(bcg)



	# if n == nWorkers:
	# 	bcgs = po.starmap(appendToDatabase, data)
	# 	data = []
	# n += 1
	#import multiprocessing

	#p = multiprocessing.Process(target=appendToDatabase, args=(RA, DEC, BCG_SPEC_Z, P_BCG, LAMBDA_CHISQ))
	#p.start()

	#bcg = Redmapper(RA, DEC, BCG_SPEC_Z)
	#bcg.pBCG = P_BCG
	#bcg.lambda_chisq = LAMBDA_CHISQ

	#session.add(bcg)

	# if n == nWorkers:
	# 	n = 0
	# 	#print data
	# 	for i in range(nWorkers):
	# 		po.apply_async(appendToDatabase, args=(data[i]))
	# 	data = []

	counter += 1
	if (counter == maxNumberOfBcgs): break
	if (counter % 100 == 0):
		print(counter , " # - comitting bcgs to database...")
		session.commit()

inFileSDSS = pyfits.open('data/SDSS_DR8_galaxies.fit')
dataSDSSGalaxies = inFileSDSS[1].data

# inFileSDSSMags = pyfits.open('data/SDSS_DR8_galaxies_magnitudes.fit')
# dataSDSSGalaxiesMags = inFileSDSSMags[1].data

counter = 0
for objID, ra, dec, z, zErr, deVAB_r, deVABErr_r, deVPhi_r, lnLDeV_r in dataSDSSGalaxies:
	galaxy = SDSSGalaxy(ra, dec, z)
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
		print(counter , " # - comitting galaxies to database...")
		session.commit()

#--------------------------------------------------------------------------------
# Commit changes to database
#--------------------------------------------------------------------------------
session.commit()
