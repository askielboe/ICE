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

def calcShortestAngleToYAxisInRadians(vec):
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

def calcPositionAngleEofNRelativeToCenterInDegrees(vec,center):
	from math import pi
	if len(vec) != 2:
		print "ERROR in calcPositionAngleEofNRelativeToCenterInDegrees: Vector not of dimension 2!"
		return
	try:
		relativeVec = vecSub(vec,center)
		if relativeVec[0] == relativeVec[1] == 0.:
			return -1.
		shortestAngleToY = calcShortestAngleToYAxisInRadians(relativeVec)
		# If vector is in 1st or 4th quadrant
		if relativeVec[0] > 0.:
			shortestAngleToY = 2. * pi - shortestAngleToY
		return shortestAngleToY / 2. / pi * 360.
	except ValueError:
		print "ERROR in calcPositionAngleEofNRelativeToCenterInDegrees: Type error!"
		return

def calcSmallestAngleBetweenBCGAndAgalaxy(positionAngleBCG,positionAngleGalaxy):
	try:
		angleDifference = abs(positionAngleBCG-positionAngleGalaxy)
		if angleDifference > 180.:
			angleDifference -= 180.
		if angleDifference > 90.:
			angleDifference -= 90.
		return angleDifference
	except ValueError:
		print "ERROR in calcSmallestAngleBetweenVectorAndLine: Type error!"
		return
