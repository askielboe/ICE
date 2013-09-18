#!/usr/bin/env python

#--------------------------------------------------------------------------------
# Create a session
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

#--------------------------------------------------------------------------------
# Plot relative velocities
#--------------------------------------------------------------------------------
from classes import Association

q = session.query(Association.vrel)
q = q.filter(Association.vrel != 0.0)
q = q.filter(Association.dist == 0.0)

vrels = [vrel[0] for vrel in q.all()]

# Plot histogram
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(vrels, 20, range=(-200,200))
plt.show()

#--------------------------------------------------------------------------------
# Plot position angles
#--------------------------------------------------------------------------------
from classes import Association

q = session.query(Association.positionAngle)
q = q.filter(Association.positionAngle != None)
q = q.filter(Association.dist > 0.01)
q = q.filter(Association.vrel > 200.0)

xes = [x[0] for x in q.all()]

# Plot histogram
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(xes, 20)
plt.show()

#--------------------------------------------------------------------------------
# Plot BCG position angles
#--------------------------------------------------------------------------------
# NOTE: This is using the column in the Redmapper table,
# which is copied from SDSSgalaxies

from classes import Redmapper

q = session.query(Redmapper.deVPhi_r)
q = q.filter(Redmapper.deVPhi_r != None)

xes = [x[0] for x in q.all()]

import matplotlib.pyplot as plt

# Plot histogram
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(xes, 20)
plt.show()

#--------------------------------------------------------------------------------
# Plot galaxy position angles
#--------------------------------------------------------------------------------
from classes import SDSSGalaxy

q = session.query(SDSSGalaxy.deVPhi_r)
q = q.filter(SDSSGalaxy.lnLDeV_r > -5000.)

xes = [x[0] for x in q.all()]

import matplotlib.pyplot as plt

# Plot histogram
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(xes, 20)
plt.show()

#--------------------------------------------------------------------------------
# Plot galaxy position angles differences (relative to BCG)
#--------------------------------------------------------------------------------
from classes import Association
from sqlalchemy import func

q = session.query(Association)
q = q.filter(Association.angleToBCGMajorAxis != None)
q = q.filter(Association.angleToBCGMajorAxis > -1)
q = q.filter(Association.dist < 1.0)
q = q.filter(func.abs(Association.vrel) < 1000.0)

x = [a.angleToBCGMajorAxis for a in q.all()]

import matplotlib.pyplot as plt

# Plot histogram
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(x, 20)
plt.show()

#--------------------------------------------------------------------------------
# Plot relative angle to BCG vs distance
#--------------------------------------------------------------------------------
from classes import Association

q = session.query(Association.dist, Association.angleToBCGMajorAxis)
q = q.filter(Association.angleToBCGMajorAxis != None)
q = q.filter(Association.angleToBCGMajorAxis > -1)

x = [val[0] for val in q.all()]
y = [val[1] for val in q.all()]

import matplotlib.pyplot as plt

# Using hexbin
import matplotlib.cm as cm

xmin = min(x)
xmax = max(x)
ymin = min(y)
ymax = max(y)

plt.subplot(111)
plt.hexbin(x,y, cmap=cm.jet)
plt.axis([xmin, xmax, ymin, ymax])
plt.title("Hexagon binning")
cb = plt.colorbar()
cb.set_label('counts')
plt.show()
