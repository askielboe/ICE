#
# File:    functions.py
#
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     September 2012
#
# Summary of File:
#
#   Simple mathematical functions for speedy execution
#

def vecSub(vec1,vec2):
	# Subtracts two vectors
	if len(vec1) != len(vec2):
		print "ERROR in vecSub: Vectors are not of equal dimensions!"
		return
	vecSub = [0 for i in range(len(vec1))]
	try:
		for i in range(len(vec1)):
			vecSub[i] = vec1[i] - vec2[i]
		return vecSub
	except TypeError:
		print "ERROR in vecSub: Type error!"
		return

def calcShortestAngleToYAxisInRadiansCartesian(vec):
	from math import sqrt,pow,acos
	if len(vec) != 2:
		print "ERROR in calcShortestAngleToYAxisInRadians: Vector not of dimension 2!"
		return
	try:
		vecLength = sqrt(pow(vec[0],2.) + pow(vec[1],2.))
		angle = acos(vec[1] / vecLength)
		return angle
	except ValueError:
		print "ERROR in calcShortestAngleToYAxisInRadians: Type error!"
		return

def calcPositionAngleEofNRelativeToCenterInDegreesCartesian(vec,center):
	###### BROKEN ######
	from math import pi
	if len(vec) != 2:
		print "ERROR in calcPositionAngleEofNRelativeToCenterInDegrees: Vector not of dimension 2!"
		return
	try:
		relativeVec = vecSub(vec,center)
		if relativeVec[0] == relativeVec[1] == 0.:
			return -1.
		shortestAngleToY = calcShortestAngleToYAxisInRadiansCartesian(relativeVec)
		# If vector is in 1st or 4th quadrant
		if relativeVec[0] > 0.:
			shortestAngleToY = 2. * pi - shortestAngleToY
		return shortestAngleToY / 2. / pi * 360.
	except ValueError:
		print "ERROR in calcPositionAngleEofNRelativeToCenterInDegrees: Type error!"
		return

def calcPositionAngleEofNRelativeToCenterInDegreesSpherical(vec,center):
	from math import pi, cos, sin, acos
	from physics import calcAngularSeparation
	if len(vec) != 2:
		print "ERROR in calcPositionAngleEofNRelativeToCenterInDegrees: Vector not of dimension 2!"
		return
	try:
		if (vec == center):
			return None

		if (vec[0] == center[0]):
			return 90.0

		if (vec[1] == center[1]):
			return 0.0

		# Convert coordinates to radians and calculate relative to equator
		a = (90.0 - vec[1]) * pi/180.
		b = (90.0 - center[1]) * pi/180.

		c = calcAngularSeparation(vec[0],vec[1],center[0],center[1])

		# Using spherical law of cosines to calculate the angle A
		cosAngleA = ( cos(a) - cos(c)*cos(b) ) / ( sin(c)*sin(b) )

		angleA = acos(cosAngleA)
		positionAngle = angleA * 180./pi

		return positionAngle
	except ValueError:
		print "ERROR in calcPositionAngleEofNRelativeToCenterInDegrees: Type error!"
		print "BCG position = ", center
		print "Galaxy position = ", vec
		print "Position difference = [", center[0]-vec[0], ", ", center[1]-vec[1], "]"
		return

def calcSmallestAngleBetweenBCGAndAgalaxy(positionAngleBCG,positionAngleGalaxy):
	try:
		angleDifference = abs(positionAngleBCG-positionAngleGalaxy)
		if angleDifference > 90.:
			angleDifference = 180. - angleDifference
		return angleDifference
	except ValueError:
		print "ERROR in calcSmallestAngleBetweenVectorAndLine: Type error!"
		return
