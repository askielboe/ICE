# 
# File:    classes.py 
# 
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     August 2012
# 
# Summary of File: 
# 
#   Declares classes
# 

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, BigInteger, Float
from sqlalchemy.orm import relationship #, backref

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Association(Base):
	__tablename__ = 'associations'
	
	redmapper_id = Column(Integer, ForeignKey('redmapper.mem_match_id'), primary_key=True)
	sdss_galaxy_id = Column(BigInteger, ForeignKey('sdss_galaxies.objID'), primary_key=True)
	
	dist = Column(Float)		# Projected distance to BCG in Mpc
	vrel = Column(Float)		# Velocity relative to BCG in km/s
	positionAngle = Column(Float)		# Galaxy position angle East of North with respect to the BCG position
	angleToBCGMajorAxis = Column(Float)
	
	galaxy = relationship("SDSSGalaxy")

class SDSSGalaxy(Base):
	__tablename__ = 'sdss_galaxies'
	
	#id = Column(Integer, primary_key=True)
	
	# SDSS Quantities
	objID         = Column(BigInteger, primary_key=True)	# SDSS Object ID
	ra            = Column(Float)		# Right ascension
	dec           = Column(Float)		# Declination
	z             = Column(Float)		# Redshift
	zErr          = Column(Float)		# Redshift Error
	deVAB_r       = Column(Float)		# Axis Ratio (de Vaucouleurs fit)
	deVABErr_r    = Column(Float)		# Axis Ratio Error (de Vaucouleurs fit)
	deVPhi_r      = Column(Float)		# Position Angle (de Vaucouleurs fit)
	lnLDeV_r      = Column(Float)		# de Vaucouleurs fit likelihood
	
	# Derived quantities
	da            = Column(Float)		# Angular Diameter Distance
	
	def __init__(self, ra, dec, z):
		self.ra = ra
		self.dec = dec
		self.z = z
		
		self.objID = -1.0
		
		self.zErr = -1.0
		self.deVAB_r = -1.0
		self.deVABErr_r = -1.0
		self.deVPhi_r = -1.0
		self.lnLDeV_r = -1.0
		
		self.da = -1.0
	
	def __repr__(self):
		return "<SDSS Galaxy('%f','%f','%f')>" % (self.ra, self.dec, self.z)

class Redmapper(Base):
	from sqlalchemy.ext.associationproxy import association_proxy
	
	__tablename__ = 'redmapper'
	
	#id = Column(Integer, primary_key=True)
	mem_match_id  = Column(Integer, primary_key=True)
	
	sdss_galaxy_id = Column(BigInteger, ForeignKey('sdss_galaxies.objID')) # Corresponding Galaxy ID
	sdss_galaxy = relationship("SDSSGalaxy", uselist=False, backref="matched_redmapper", lazy="joined", join_depth=2)
	
	# Redmapper Quantities
	ra            = Column(Float)		# Right ascension
	dec           = Column(Float)		# Declination
	z             = Column(Float)		# Redshift
	pBCG          = Column(Float)		# pBCG (redmapper: Rozo et. al. 2012)
	lambda_chisq  = Column(Float)		# Richness
	
	# # SDSS Quantities
	# objID         = Column(BigInteger)	# SDSS Object ID
	# deVAB_r       = Column(Float)		# Axis Ratio (de Vaucouleurs fit)
	# deVABErr_r    = Column(Float)		# Axis Ratio Error (de Vaucouleurs fit)
	
	# lnLDeV_r      = Column(Float)		# de Vaucouleurs fit likelihood
	
	# Derived quantities
	da            = Column(Float)		# Angular Diameter Distance
	
	deVPhi_r      = Column(Float)		# Position Angle (de Vaucouleurs fit)
	
	#def _get_deVPhi_r(self):
	#	return object_session(self).query(SDSSGalaxy.deVPhi_r).with_parent(self).all()
	
	#deVPhi_rProperty = property(_get_deVPhi_r)
	
	deVPhi_rProxy = association_proxy('sdss_galaxy', 'deVPhi_r')
	
	#from sqlalchemy.orm import column_property
	#from sqlalchemy import select, and_
	
	# deVPhi_r_fromsdss = column_property(
	# 	select(
	# 		[SDSSGalaxy.deVPhi_r],
	# 		and_(sdss_galaxy_id == SDSSGalaxy.objID),
	# 	).correlate(None),
	# 	deferred=True,
	# )
	
	# deVPhi_r_fromsdss = column_property(
	# 	select(
	# 		[SDSSGalaxy.deVPhi_r],
	# 		sdss_galaxy_id == SDSSGalaxy.objID)\
	# 		.as_scalar() \
	# 		.label('deVPhi_r_fromsdss'))
	
	
	#deVPhi_r_fromsdss = column_property(select([SDSSGalaxy.deVPhi_r]).where(sdss_galaxy_id == SDSSGalaxy.objID).correlate(None), deferred=True)
	
	associated_sdss_galaxies = relationship("Association", backref='redmapper')
	
	def __init__(self, ra, dec, z):
		self.ra = ra
		self.dec = dec
		self.z = z
	
		self.pBCG = -1.0
		self.lambda_chisq = -1.0
	
	def __repr__(self):
		return "<Bcg('%f','%f','%f')>" % (self.ra, self.dec, self.z)

