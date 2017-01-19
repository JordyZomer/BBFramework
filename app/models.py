from app import BBFrameworkDB



class Users(BBFrameworkDB.Model):
	__tablename__ = 'users'

	user_id = BBFrameworkDB.Column(BBFrameworkDB.Integer, primary_key=True)
	username = BBFrameworkDB.Column(BBFrameworkDB.String(64), index=True, unique=True)
	password = BBFrameworkDB.Column(BBFrameworkDB.String(100), index=True)
	engagements = BBFrameworkDB.relationship('Engagements', backref='user_engagements', lazy='dynamic')
	modules     = BBFrameworkDB.relationship('Modules', backref='user_modules', lazy='dynamic')

	def __repr__(self):
		return "<User: %r>" % (self.username)



class Engagements(BBFrameworkDB.Model):
	__tablename__ = 'engagements'

	eng_id = BBFrameworkDB.Column(BBFrameworkDB.Integer, primary_key=True)
	eng_name = BBFrameworkDB.Column(BBFrameworkDB.String(250), index=True, unique=True)
	eng_desc = BBFrameworkDB.Column(BBFrameworkDB.String(500), index=True, unique=True)
	eng_user_id = BBFrameworkDB.Column(BBFrameworkDB.Integer, BBFrameworkDB.ForeignKey('users.user_id'))
	modules = BBFrameworkDB.relationship('Modules', backref='engagement_modules', lazy='dynamic')

	def __repr__(self):
		return "<Engagements: %r>" % self.eng_name

class Modules(BBFrameworkDB.Model):
	__tablename__ = 'modules'

	eng_id = BBFrameworkDB.Column(BBFrameworkDB.Integer, BBFrameworkDB.ForeignKey('engagements.eng_id'))
	module_id = BBFrameworkDB.Column(BBFrameworkDB.Integer, primary_key=True)
	module_name = BBFrameworkDB.Column(BBFrameworkDB.String(250), index=True)
	module_desc = BBFrameworkDB.Column(BBFrameworkDB.String(500), index=True)
	module_args = BBFrameworkDB.Column(BBFrameworkDB.String(1000), index=True)
	module_user_id = BBFrameworkDB.Column(BBFrameworkDB.Integer, BBFrameworkDB.ForeignKey('users.user_id'))
	
	def __repr__(self):	
		return "<Modules: %r>" % self.module_name


