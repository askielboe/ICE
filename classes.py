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
	
	bcg_id = Column(Integer, ForeignKey('bcgs.id'), primary_key=True)
	galaxy_id = Column(Integer, ForeignKey('galaxies.id'), primary_key=True)
	
	dist = Column(Float)		# Projected distance to BCG in Mpc
	vrel = Column(Float)		# Velocity relative to BCG in km/s
	positionAngle = Column(Float)		# Galaxy position angle in galaxy cluster
	
	galaxy = relationship("Galaxy")

class Bcg(Base):
	__tablename__ = 'bcgs'
	
	id = Column(Integer, primary_key=True)
	
	# SDSS Quantities
	galaxy_id     = Column(Integer, ForeignKey('galaxies.id'))		# Corresponding Galaxy ID
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
	
	# Cluster catalog quantities
	pBCG          = Column(Float)		# pBCG (redmapper: Rozo et. al. 2012)
	richness      = Column(Float)		# Richness
	
	galaxies = relationship("Association", backref='bcgs')
	
	def __init__(self, objID, ra, dec, z):
		self.objID = objID
		self.ra = ra
		self.dec = dec
		self.z = z
		
		self.zErr = -1.0
		self.deVAB_r = -1.0
		self.deVABErr_r = -1.0
		self.deVPhi_r = -1.0
		self.lnLDeV_r = -1.0
		
		self.pBCG = -1.0
		self.richness = -1.0
		
		self.da = -1.0

	def __repr__(self):
		return "<Bcg('%f','%f','%f')>" % (self.ra, self.dec, self.z)

class Galaxy(Base):
	__tablename__ = 'galaxies'
	
	id = Column(Integer, primary_key=True)
	
	# SDSS Quantities
	objID         = Column(BigInteger)	# SDSS Object ID
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
	
	def __init__(self, objID, ra, dec, z):
		self.objID = objID
		self.ra = ra
		self.dec = dec
		self.z = z
		
		self.zErr = -1.0
		self.deVAB_r = -1.0
		self.deVABErr_r = -1.0
		self.deVPhi_r = -1.0
		self.lnLDeV_r = -1.0
		
		self.da = -1.0
	
	def __repr__(self):
		return "<Galaxy('%f','%f','%f')>" % (self.ra, self.dec, self.z)

