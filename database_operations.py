#
# File:    database_operations.py
#
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     August 2012
#
# Summary of File:
#
#   Functions that connect to and modify the database at the lowest levels in SQLalchemy
#

def create_session():
	#--------------------------------------------------------------------------------
	# Define database
	#--------------------------------------------------------------------------------
	from sqlalchemy import create_engine
	import MySQLdb as mysqldb
	engine = create_engine('mysql+mysqldb://root@127.0.0.1/ice')

	#--------------------------------------------------------------------------------
	# Create a session to start talking to the database
	#--------------------------------------------------------------------------------
	from sqlalchemy.orm import sessionmaker
	# Since the engine is already created we can bind to it immediately
	Session = sessionmaker(bind=engine)
	return Session()
