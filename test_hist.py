#!/usr/bin/env python

#--------------------------------------------------------------------------------
# Create a session
#--------------------------------------------------------------------------------
# from database_operations import create_session
# session = create_session()

# Relative velocities
# from classes import Association
#
# q = session.query(Association.vrel)
# q = q.filter(Association.vrel != 0.0)
# #q = q.filter(Association.vrel < 200.0)
# q = q.filter(Association.dist == 0.0)
# 
# vrels = [vrel[0] for vrel in q.all()]
# 
# import matplotlib.pyplot as plt
# 
# # Plot histogram
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.hist(vrels, 20, range=(-200,200))
# plt.show()

# # Position angles
# from classes import Association
# 
# q = session.query(Association.positionAngle)
# q = q.filter(Association.positionAngle != None)
# q = q.filter(Association.dist > 0.01)
# q = q.filter(Association.vrel > 200.0)
# 
# xes = [x[0] for x in q.all()]
# 
# import matplotlib.pyplot as plt
# 
# # Plot histogram
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.hist(xes, 20)
# plt.show()

# # ======== BCG position angles ========
# from classes import Redmapper
# 
# q = session.query(Redmapper.deVPhi_r)
# q = q.filter(Redmapper.deVPhi_r != None)
# 
# xes = [x[0] for x in q.all()]
# 
# import matplotlib.pyplot as plt
# 
# # Plot histogram
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.hist(xes, 20)
# plt.show()

# # ======== Galaxy position angles ========
# from classes import SDSSGalaxy
# 
# q = session.query(SDSSGalaxy.deVPhi_r)
# q = q.filter(SDSSGalaxy.lnLDeV_r > -5000.)
# 
# xes = [x[0] for x in q.all()]
# 
# import matplotlib.pyplot as plt
# 
# # Plot histogram
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.hist(xes, 20)
# plt.show()

# # ======== Galaxy position angles differences (relative to BCG) ========
# from classes import Association
# from sqlalchemy import func
# 
# q = session.query(Association)
# q = q.filter(Association.angleToBCGMajorAxis != None)
# q = q.filter(Association.angleToBCGMajorAxis > -1)
# q = q.filter(Association.dist < 1.0)
# q = q.filter(func.abs(Association.vrel) < 1000.0)
# 
# x = [a.angleToBCGMajorAxis for a in q.all()]
# 
# import matplotlib.pyplot as plt
# 
# # Plot histogram
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.hist(x, 20)
# plt.show()

# # ======== Relative angle to BCG vs distance ========
# from classes import Association
# 
# q = session.query(Association.dist, Association.angleToBCGMajorAxis)
# q = q.filter(Association.angleToBCGMajorAxis != None)
# q = q.filter(Association.angleToBCGMajorAxis > -1)
# 
# x = [val[0] for val in q.all()]
# y = [val[1] for val in q.all()]
# 
# import matplotlib.pyplot as plt
# 
# # Using hexbin
# import matplotlib.cm as cm
# 
# xmin = min(x)
# xmax = max(x)
# ymin = min(y)
# ymax = max(y)
# 
# plt.subplot(111)
# plt.hexbin(x,y, cmap=cm.jet)
# plt.axis([xmin, xmax, ymin, ymax])
# plt.title("Hexagon binning")
# cb = plt.colorbar()
# cb.set_label('counts')

# ======== Galaxy position angles relative to BCG vs galaxy intrinsic position angle relative to BCG ========
from database_operations import create_session
session = create_session()

from classes import Association, SDSSGalaxy, Redmapper
from sqlalchemy import func

### Mikes method
from sqlalchemy.orm import aliased
redmapper_sdssgalaxy_aliased = aliased(SDSSGalaxy)
q = session.query(Association.angleToBCGMajorAxis, func.abs(redmapper_sdssgalaxy_aliased.deVPhi_r - SDSSGalaxy.deVPhi_r))
q = q.join(Association.redmapper)
q = q.join(Association.galaxy).join(redmapper_sdssgalaxy_aliased, Redmapper.sdss_galaxy)

# Filter: Angle to major axis is non-negative
q = q.filter(Association.angleToBCGMajorAxis != None)
q = q.filter(Association.angleToBCGMajorAxis >= 0.)

# Filter: Position angles are non-negative
q = q.filter(redmapper_sdssgalaxy_aliased.deVPhi_r >= 0.)
q = q.filter(SDSSGalaxy.deVPhi_r >= 0.)

#q = q.filter(Redmapper.lambda_chisq > 20.0)
q = q.filter(Association.dist < 1.0)
q = q.filter(func.abs(Association.vrel) < 1000.0)

x = [angleToBCGMajorAxis for angleToBCGMajorAxis,angleDifference in q.all()]
y = [angleDifference for angleToBCGMajorAxis,angleDifference in q.all()]

# ======== Galaxy position angles relative to BCG vs u-r band magnitude ========
from database_operations import create_session
session = create_session()

from classes import Association, SDSSGalaxy
from sqlalchemy import func

### Mikes method
#from sqlalchemy.orm import aliased
#Redmapper_aliased = aliased(SDSSGalaxy)
q = session.query(Association.angleToBCGMajorAxis, SDSSGalaxy.deVMag_u - SDSSGalaxy.deVMag_r)
q = q.join(Association.redmapper).join(Association.galaxy)
#q = q.join(redmapper_sdssgalaxy_aliased, Redmapper.sdss_galaxy)

# Filter: Angle to major axis is non-negative
q = q.filter(Association.angleToBCGMajorAxis != None)
q = q.filter(Association.angleToBCGMajorAxis >= 0.)

q = q.filter(Association.dist < 1.0)
q = q.filter(func.abs(Association.vrel) < 1000.0)

x = [angleToBCGMajorAxis for angleToBCGMajorAxis,color in q.all()]
y = [color for angleToBCGMajorAxis,color in q.all()]

# ==== Plotting ====
import matplotlib.pyplot as plt
from numpy import histogram2d
from pylab import imshow, colorbar

# ==== Using histogram2d ====
hist,xedges,yedges = histogram2d(x,y,bins=20,range=[[0.,90.],[0.,90.]])
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1] ]
imshow(hist.T,extent=extent,interpolation='nearest',origin='lower')
colorbar()
plt.xlabel("angle to CG major axis")
plt.ylabel("difference in position angle")
plt.show()

# # ==== Using hexbin ====
# import matplotlib.cm as cm
# 
# xmin = min(x)
# xmax = max(x)
# ymin = min(y)
# ymax = max(y)
# 
# plt.subplot(111)
# plt.hexbin(x,y, cmap=cm.jet)
# plt.axis([xmin, xmax, ymin, ymax])
# plt.title("Hexagon binning")
# plt.xlabel("angle to CG major axis")
# plt.ylabel("difference in position angle")
# cb = plt.colorbar()
# cb.set_label('counts')
# plt.show()
