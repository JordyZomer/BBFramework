from app import BBFrameworkAPP, BBFrameworkDB, pwd_context, Serializer, BadSignature, SignatureExpired, auth, jsonify, g



class Users(BBFrameworkDB.Model):
	__tablename__ = 'users'

	user_id = BBFrameworkDB.Column(BBFrameworkDB.Integer, primary_key=True)
	username = BBFrameworkDB.Column(BBFrameworkDB.String(64), index=True, unique=True)
	password_hash = BBFrameworkDB.Column(BBFrameworkDB.String(128))
	engagements = BBFrameworkDB.relationship('Engagements', backref='user_engagements', lazy='dynamic')
	modules     = BBFrameworkDB.relationship('Modules', backref='user_modules', lazy='dynamic')
	
	
	def generate_auth_token(self, expiration = 600):
		s = Serializer(BBFrameworkAPP.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({'user_id' : self.user_id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(BBFrameworkAPP.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired.
		except BadSignature:
			return None # Invalid token
		user = Users.query.get(data['user_id'])
		return user
	
	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)
		
	def verify_password_only(self, password):
		return pwd_context.verify(password, self.password_hash)

	@auth.error_handler
	def unauthorized():
        	return jsonify({"Message: " : "Unauthorized Access, please authenticate!"}), 403

	@auth.verify_password # verify_password
	def verify_password(username_or_token, password):
	       	# first try to auth by token
	        user = Users.verify_auth_token(username_or_token)
	        if not user:
	                # try to auth wit username/password:
	                user = Users.query.filter_by(username = username_or_token).first()
	                if not user or not user.verify_password_only(password):
	                        return False
        	g.user = user
	        return True

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


