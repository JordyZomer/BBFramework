import os

basedir = os.path.abspath(os.path.dirname(__file__))

DBSERVER	= '127.0.0.1'
DBUSER  	= 'bbframeworkdbuser'
DBPASSWD	= 'password123'
DBNAME 		= 'BBFrameworkAPI'
DBCONN 		= "mysql://"+DBUSER+":"+DBPASSWD+"@"+DBSERVER+"/"+DBNAME

API_ROOT_URL 	= "/bbframework/api/v0.1/"

SQLALCHEMY_DATABASE_URI = DBCONN
SQLALCHEMY_TRACK_MODIFICATIONS = True
