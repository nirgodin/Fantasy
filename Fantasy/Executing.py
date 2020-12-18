# FIRST, YOU NEED TO DEFINE YOUR DATABASE INFORMATION AND PASSWORD AS ENVIRONMENT VARIABLES!
# SECOND, MAKE SURE YOU UPDATE THE SEASON AND GAMEWEEK VARIABLES IN THE FILES BEFORE EXECUTING THE CODE
import os
from Credentials import os.environ['hostname'], os.environ['user'], os.environ['password'], os.environ['database']
import Scraping
import Merging
import Uploading
