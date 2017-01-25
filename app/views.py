from app import BBFrameworkAPP, BBFrameworkAPI, BBFrameworkDB, Resource, reqparse, models, marshal, fields, datastructures, exc, pwd_context,abort, auth, g, jsonify

## BBFrameworkAPP Classes

## Engagements:
class Engagements(Resource):
	## Parse any parameters we require:
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('eng_name', type=str, required=True, help="eng_name missing", location='json')
		self.reqparse.add_argument('eng_desc', type=str, required=True, help="eng_desc missing", location='json')
		self.reqparse.add_argument('eng_user_id', type=str, required=True, help="eng_user_id missing", location='json')
		super(Engagements, self).__init__()

	## Get the complete list of enagements:
        @auth.login_required
	def get(self):
		engs = models.Engagements.query.all()
		if engs:
			return jsonify({ "Engagements: " : marshal(engs, datastructures.engagement_fields) })
		else:	
			return jsonif({ "Engagements: " : False })

	## Create an engagement:
	@auth.login_required
	def post(self):
		try:
	                args = self.reqparse.parse_args()
		except:
			return jsonify({"Error: " : "Invalid JSON data sent"})
		
		e_name = args['eng_name']
		e_desc = args['eng_desc']
		e_u_id = args['eng_user_id']
		
		if not e_name or not e_desc or not e_u_id:
                        #return {"Error: " : "Either of e_name, e_desc or e_u_id values is missing"}
			abort(400)
	
		if models.Engagements.query.filter_by(eng_name = e_name).first():
			abort(400)
	
		new_engagement = models.Engagements(eng_name = args['eng_name'], eng_desc = args['eng_desc'], eng_user_id = args['eng_user_id'])

		try:
			BBFrameworkDB.session.add(new_engagement)
			BBFrameworkDB.session.commit()
			return jsonify({'Engagement Added: ' : marshal(new_engagement, datastructures.engagement_fields)})
		except exc.IntegrityError as e:
			BBFrameworkDB.session.rollback()
			err = {'err_type' : type(e), 'err_desc' : e.args}
			return jsonify({"Error: " : marshal(err, datastructures.error_fields)})
		except exc.OperationalError as e:
			BBFrameworkDB.session.rollback()
                        err = {'err_type' : type(e), 'err_desc' : e.args}
                        return jsonify({"Error: " : marshal(err, datastructures.error_fields)})
		
## Specific Engagement:
class Engagement(Resource):
        ## Parse any parameters we require:
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('eng_name', type=str, required=True, help="eng_name missing", location='json')
                self.reqparse.add_argument('eng_desc', type=str, required=True, help="eng_desc missing", location='json')
                self.reqparse.add_argument('eng_user_id', type=str, required=True, help="eng_user_id missing", location='json')
                super(Engagement, self).__init__()

	## Request a specific engagement:
	@auth.login_required
	def get(self, eng_id):
		s_eng = models.Engagements.query.get(eng_id)
		if s_eng:
			return jsonify({("Engagement: %s" % eng_id) : marshal(s_eng, datastructures.engagement_fields)})
		else:
			return jsonify({ "Engagement: " : False })

	## Update engagement details:
	@auth.login_required
	def put(self, eng_id):	
		## Check JSON data sent by client is correct.
		try:
			args = self.reqparse.parse_args()
		except:
			return jsonify({"Error: " : "Invalid JSON data sent."})
		
		## Check the values are not empty:
                e_name = args['eng_name']
                e_desc = args['eng_desc']
                e_u_id = args['eng_user_id']

                if not e_name or not e_desc or not e_u_id:
                        return jsonif({"Error: " : "One of (e_name, e_desc or e_u_id values is missing"})

		## Update engagement:
		tmp_engagement = models.Engagements.query.get(eng_id)
		tmp_engagement.eng_name 	= e_name
		tmp_engagement.eng_desc 	= e_desc
		tmp_engagement.eng_user_id   	= e_u_id
		BBFrameworkDB.session.commit()

		return jsonify({"Updated Engagement: " : marshal(tmp_engagement, datastructures.engagement_fields)})

	## Delete an engagement:
        @auth.login_required	
	def delete(self, eng_id):	
		if (models.Engagements.query.filter_by(eng_id = eng_id).delete()):
			BBFrameworkDB.session.commit()
			return jsonify({"Deleted: " : True })
		else:
			return jsonify({"Deleted: " : False })

## Modules:
class Modules(Resource):
        def get(self, eng_id):
                return "Lists all modules assigned to an engagement: %s<BR />" % eng_id
        def post(self, eng_id):
                return "Creates a new module assigned to an engagement: %s<BR />" % eng_id

## Specific Module
class Module(Resource):
	def get(self, eng_id, module_id):
		return "List specific engagement: %s, specific module: %s" % (eng_id, module_id)
	def put(self, eng_id, module_id):
		return "Update a speific engagement: %s, specific module: %s" % (eng_id, module_id)
	def delete(self, eng_id, module_id):
		return "Delete a specific engagement: %s, specific module: %s" % (eng_id, module_id)

## Users:
class Users(Resource):
        def __init__(self):
	        self.reqparse = reqparse.RequestParser()
                self.reqparse.add_argument('username', type=str, required=True, help="username missing", location='json')
                self.reqparse.add_argument('password', type=str, required=True, help="password missing", location='json')
                super(Users, self).__init__()

	## Get a complete list of users:
	@auth.login_required
        def get(self):
		users = models.Users.query.all()
		if users:
	                return jsonify({"Users: " : marshal(users, datastructures.user_fields)})
		else:
			return jsonify({"Users: " : False })

		
	@auth.login_required
	def post(self):
		try:
                       	args = self.reqparse.parse_args()
	        except:
                        return jsonify({"Error: " : "Invalid JSON data sent"})

               	username = args['username']
               	password = args['password']
	
		if username is None or password is None:
			abort(400) # missing parameters

		if models.Users.query.filter_by(username = username).first() is not None:
			abort(400) # user exists
			
		new_user = models.Users(username = username)
		new_user.hash_password(password)

		try:
	                BBFrameworkDB.session.add(new_user)
                        BBFrameworkDB.session.commit()
                        return jsonify({'User Added: ' : marshal(new_user, datastructures.user_fields)}, 201)

                except exc.IntegrityError as e:
                        BBFrameworkDB.session.rollback()
                        err = {'err_type' : type(e), 'err_desc' : e.args}
                        return jsonify({"Error: " : marshal(err, datastructures.error_fields)})

                except exc.OperationalError as e:
                        BBFrameworkDB.session.rollback()
                        err = {'err_type' : type(e), 'err_desc' : e.args}
                        return jsonify({"Error: " : marshal(err, datastructures.error_fields)})

			 	
	
class User(Resource):
	def __init__(self):
                self.reqparse = reqparse.RequestParser()
                self.reqparse.add_argument('username', type=str, required=True, help="username missing", location='json')
                self.reqparse.add_argument('password', type=str, required=True, help="password missing", location='json')
                super(User, self).__init__()

	## List a specifc user:
	@auth.login_required	
	def get(self, user_id):
		user = models.Users.query.get(user_id)
		if user:
			return jsonify({"User: " : marshal(user, datastructures.user_fields)})
		else:
			return jsonify({"User: " : False })

	## Update user record:
	@auth.login_required
	def put(self, user_id):
		try:
			args = self.reqparse.parse_args()
		except:
			return {"Error: " : "Invalid JSON data sent."}

		## check the values are not empty:
		username = args['username']
		password = args['password']

		if not username or not password or not user_id:
			return jsonify({"Error: " : "Either the username, password or user_id value is missing."})

		## Update user:
		tmp_user = models.Users.query.get(user_id)
		tmp_user.username = username
		tmp_user.password = password
		tmp_user.user_id  = user_id
		BBFrameworkDB.session.commit()

		return jsonify({"Updated User: " : marshal(tmp_user, datastructures.user_fields)})

	## Delete a specific user:
	@auth.login_required
	def delete(self, user_id):
		if (models.Users.query.filter_by(user_id = user_id).delete()):
			BBFrameworkDB.session.commit()
			return jsonify({"Deleted: " : True })
		else:	
			return jsonify({"Deleted: " : False })

class Token(Resource):
	@auth.login_required
	def get(self):
		token = g.user.generate_auth_token()
		return jsonify({"Token: " : token.decode('ascii')})

@auth.verify_password
def verify_password(username_or_token, password):
	# first try to auth by token
	user = models.Users.verify_auth_token(username_or_token)
	if not user:
		# try to auth wit username/password:
		user = models.Users.query.filter_by(username = username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True


## Register routes
ROOT_URL = BBFrameworkAPP.config['API_ROOT_URL']

## Engagements route:
BBFrameworkAPI.add_resource(Engagements, ROOT_URL + 'engagements', endpoint='engagements')
## Specific Engagement route:
BBFrameworkAPI.add_resource(Engagement, ROOT_URL + 'engagement/<int:eng_id>', endpoint='engagement')
## Engagements Modules route:
BBFrameworkAPI.add_resource(Modules, ROOT_URL + 'engagement/<int:eng_id>/modules', endpoint='modules')
## Specific Engagements Modules route:
BBFrameworkAPI.add_resource(Module, ROOT_URL + 'engagement/<int:eng_id>/module/<int:module_id>', endpoint='module')
## Users route:
BBFrameworkAPI.add_resource(Users, ROOT_URL + 'users', endpoint='users')
## Specific User Route:
BBFrameworkAPI.add_resource(User, ROOT_URL + 'user/<int:user_id>', endpoint='user')
## Token Route
BBFrameworkAPI.add_resource(Token, ROOT_URL + 'token', endpoint='token')


