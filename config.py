import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


SQLALCHEMY_DATABASE_URI = 'postgresql://atta:passwordforatta@127.0.0.1:5432/fyyur2'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'akldadfg628e9t^*T68*y8YgG8YDNSAIhl'
DEBUG_TB_INTERCEPT_REDIRECTS = False