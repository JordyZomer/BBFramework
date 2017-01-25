## Various Imports:

from flask import Flask, abort, g, jsonify
from flask_restful import Resource, Api, reqparse, marshal, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

## Create a Flask instance called BBFrameworkAPP:
BBFrameworkAPP = Flask(__name__)
## Create an API instance called BBFrameworkAPI:
BBFrameworkAPI = Api(BBFrameworkAPP)
## Load the config file:
BBFrameworkAPP.config.from_object('config')
## Create an SQLAlchemy instance called BBFrameworkDB:
BBFrameworkDB = SQLAlchemy(BBFrameworkAPP)
## Create HTTPBasicAuth instance called auth:
auth = HTTPBasicAuth()

# At the bottom to avoid circular import errors.
from app import views, models
