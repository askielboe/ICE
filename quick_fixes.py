#--------------------------------------------------------------------------------
# Create a session
#--------------------------------------------------------------------------------
from database_operations import create_session
session = create_session()

from classes import Association, SDSSGalaxy, Redmapper

q = session.query(Redmapper, SDSSGalaxy.deVPhi_r).join(SDSSGalaxy)

counter = 0
for bcg, angle in q.all():
	bcg.deVPhi_r = angle
	counter += 1
	if (counter % 1000 == 0):
		print counter , " # - quick fixing..."
		session.commit()

session.commit()
