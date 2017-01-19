#!/usr/bin/env python

from config import SQLALCHEMY_DATABASE_URI
from app import BBFrameworkDB

BBFrameworkDB.create_all()

