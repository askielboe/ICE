# 
# File:    create_database.py 
# 
# Author1:  Andreas Skielboe (skielboe@dark-cosmology.dk)
# Date:     August 2012
# 
# Summary of File: 
# 
#   Loads classes and creates tables in the database
# 

#--------------------------------------------------------------------------------
# Define database
#--------------------------------------------------------------------------------
from sqlalchemy import create_engine
import MySQLdb as mysqldb
engine = create_engine('mysql+mysqldb://root@127.0.0.1/ice')

#--------------------------------------------------------------------------------
# Import classes and create tables in databse
#--------------------------------------------------------------------------------
from classes import Redmapper, SDSSGalaxy

# Remember: For some databases a max length is required for parameters!
Redmapper.metadata.create_all(engine)
SDSSGalaxy.metadata.create_all(engine)
