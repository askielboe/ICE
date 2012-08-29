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
from classes import Bcg, Galaxy

# Remember: For some databases a max length is required for parameters!
Bcg.metadata.create_all(engine)
Galaxy.metadata.create_all(engine)
