from app import BBFrameworkAPP, BBFrameworkAPI, BBFrameworkDB, Resource, reqparse, models, marshal, fields, datastructures, exc 

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
	## Required to check if a new database entry is unique or not
	## to avoid duplicates within the database and the id's going out of sync.
	def is_unique(self, new_eng):
		is_unique = True
		current_engs = models.Engagements.query.all()
		for e in current_engs:
			if (new_eng.eng_name in e.eng_name) or (new_eng.eng_desc in e.eng_desc):
				is_unique = False
				break	
			else:
				is_unique = True
		return is_unique

	## Get the complete list of enagements:
	def get(self):
		engs = models.Engagements.query.all()
		return { 'Engagements: ' : marshal(engs, datastructures.engagement_fields) }

	## Create an engagement:
	def post(self):
		try:
	                args = self.reqparse.parse_args()
		except:
			return {"Error: " : "Invalid JSON data sent"}
		
		e_name = args['eng_name']
		e_desc = args['eng_desc']
		e_u_id = args['eng_user_id']
		
		if not e_name or not e_desc or not e_u_id:
                        return {"Error: " : "Either of e_name, e_desc or e_u_id values is missing"}
		
		new_engagement = models.Engagements(eng_name = args['eng_name'], eng_desc = args['eng_desc'], eng_user_id = args['eng_user_id'])

		if self.is_unique(new_engagement):
			try:
				BBFrameworkDB.session.add(new_engagement)
				BBFrameworkDB.session.commit()
				return {'Engagement Added: ' : marshal(new_engagement, datastructures.engagement_fields)}
			except exc.IntegrityError as e:
				BBFrameworkDB.session.rollback()
				err = {'err_type' : type(e), 'err_desc' : e.args}
				return {"Error: " : marshal(err, datastructures.error_fields)}
			except exc.OperationalError as e:
				BBFrameworkDB.session.rollback()
                                err = {'err_type' : type(e), 'err_desc' : e.args}
                                return {"Error: " : marshal(err, datastructures.error_fields)}
		else:
			return {"Error: " : "The new engagement is a duplicate, duplicates cannot exist!"}


## Specific Engagement:
class Specific_Engagement(Resource):
        ## Parse any parameters we require:
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('eng_name', type=str, required=True, help="eng_name missing", location='json')
                self.reqparse.add_argument('eng_desc', type=str, required=True, help="eng_desc missing", location='json')
                self.reqparse.add_argument('eng_user_id', type=str, required=True, help="eng_user_id missing", location='json')
                super(Specific_Engagement, self).__init__()

	## Request a specific engagement:
	def get(self, eng_id):
		s_eng = models.Engagements.query.get(eng_id)
		eng_string = "Engagement: %s" % eng_id
		return {eng_string : marshal(s_eng, datastructures.engagement_fields)}

	## Update engagement details:
	def put(self, eng_id):	
		## Check JSON data sent by client is correct.
		try:
			args = self.reqparse.parse_args()
		except:
			return {"Error: " : "Invalid JSON data sent."}
		
		## Check the values are not empty:
                e_name = args['eng_name']
                e_desc = args['eng_desc']
                e_u_id = args['eng_user_id']

                if not e_name or not e_desc or not e_u_id:
                        return {"Error: " : "One of (e_name, e_desc or e_u_id values is missing"}
		## Update engagement:
		tmp_engagement = models.Engagements.query.get(eng_id)
		tmp_engagement.eng_name 	= e_name
		tmp_engagement.eng_desc 	= e_desc
		tmp_engagement.eng_user_id   	= e_u_id
		BBFrameworkDB.session.commit()
		return {"Updated Engagement: " : marshal(tmp_engagement, datastructures.engagement_fields)}

	## Delete an engagement:
	def delete(self, eng_id):	
		if (models.Engagements.query.filter_by(eng_id = eng_id).delete()):
			BBFrameworkDB.session.commit()
			return {"Deleted: " : True }
		else:
			return {"Deleted: " : False }

## Modules:
class Modules(Resource):
        def get(self, eng_id):
                return "Lists all modules assigned to an engagement: %s<BR />" % eng_id
        def post(self, eng_id):
                return "Creates a new module assigned to an engagement: %s<BR />" % eng_id

## Specific Module
class Specific_Module(Resource):
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

	## Implement is_unique for users:
	def is_unique(self):
		pass
	
	## Get a complete list of users:
        def get(self):
		users = models.Users.query.all()
                return {"Users: " : marshal(users, datastructures.user_fields)}

	## Create a user:
        def post(self):
		try:	
			args = self.reqparse.parse_args()
		except:	
			return {"Error: " : "Invalid JSON data sent"}
			
		username = args['username']
		password = args['password']
		
		if not username or not password:
			return {"Error: " : "One of the username or password values is missing"}

		new_user = models.Users(username = username, password = password)

		try:
	                BBFrameworkDB.session.add(new_user)
                        BBFrameworkDB.session.commit()
                        return {'User Added: ' : marshal(new_user, datastructures.user_fields)}
                except exc.IntegrityError as e:
                        BBFrameworkDB.session.rollback()
                        err = {'err_type' : type(e), 'err_desc' : e.args}
                        return {"Error: " : marshal(err, datastructures.error_fields)}
                except exc.OperationalError as e:
                        BBFrameworkDB.session.rollback()
                        err = {'err_type' : type(e), 'err_desc' : e.args}
                        return {"Error: " : marshal(err, datastructures.error_fields)}


class Specific_User(Resource):
	def __init__(self):
                self.reqparse = reqparse.RequestParser()
                self.reqparse.add_argument('username', type=str, required=True, help="username missing", location='json')
                self.reqparse.add_argument('password', type=str, required=True, help="password missing", location='json')
                super(Specific_User, self).__init__()

	## List a specifc user:	
	def get(self, user_id):
		user = models.Users.query.get(user_id)
		return {"User: " : marshal(user, datastructures.user_fields)}

	## Update user record:
	def put(self, user_id):
		#try:
		args = self.reqparse.parse_args()
		#except:
		#	return {"Error: " : "Invalid JSON data sent."}
		print "debug: %r" % args
		## check the values are not empty:
		username = args['username']
		password = args['password']

		if not username or not password or not user_id:
			return {"Error: " : "Either the username, password or user_id value is missing."}	

		## Update user:
		tmp_user = models.Users.query.get(user_id)
		tmp_user.username = username
		tmp_user.password = password
		tmp_user.user_id  = user_id
		BBFrameworkDB.session.commit()
		return {"Updated User: " : marshal(tmp_user, datastructures.user_fields)}

	## Delete a specific user:
	def delete(self, user_id):
		if (models.Users.query.filter_by(user_id = user_id).delete()):
			BBFrameworkDB.session.commit()
			return {"Deleted: " : True }
		else:	
			return {"Deleted: " : False }

	


## Register routes
ROOT_URL = BBFrameworkAPP.config['API_ROOT_URL']

## Engagements route:
BBFrameworkAPI.add_resource(Engagements, ROOT_URL + 'engagements', endpoint='engagements')
## Specific Engagement route:
BBFrameworkAPI.add_resource(Specific_Engagement, ROOT_URL + 'engagement/<int:eng_id>', endpoint='engagement')
## Engagements Modules route:
BBFrameworkAPI.add_resource(Modules, ROOT_URL + 'engagement/<int:eng_id>/modules', endpoint='modules')
## Specific Engagements Modules route:
BBFrameworkAPI.add_resource(Specific_Module, ROOT_URL + 'engagement/<int:eng_id>/module/<int:module_id>', endpoint='module')
## Users route:
BBFrameworkAPI.add_resource(Users, ROOT_URL + 'users', endpoint='users')
## Specific User Route:
BBFrameworkAPI.add_resource(Specific_User, ROOT_URL + 'user/<int:user_id>', endpoint='user')


