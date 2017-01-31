import sys

sys.path.append('..')

from app import models

users = models.Users.query.all()

print "Users: %r" % users

for i in users:
	print i.username
	print i.password_hash
