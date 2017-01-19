## Various Imports:
from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

## Create a Flask instance called BBFrameworkAPP:
BBFrameworkAPP = Flask(__name__)
## Create an API instance called BBFrameworkAPI:
BBFrameworkAPI = Api(BBFrameworkAPP)
## Load the config file:
BBFrameworkAPP.config.from_object('config')
## Create an SQLAlchemy instance called BBFrameworkDB:
BBFrameworkDB = SQLAlchemy(BBFrameworkAPP)

# At the bottom to avoid circular import errors.
from app import views, models
