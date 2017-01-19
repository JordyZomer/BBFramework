Bug Bounty Framework API
------------------------

Engagements / Modules / User
---------------------------------------

Engagements table:

	eng_id		
	eng_name     
	eng_desc
	eng_user
	
Modules table:

	eng_id
	module_id
	module_name
	module_desc
	module_user
	module_execution = True/False??
	
Users table:

	user_id
	username
	password
	
	
Relationships:
--------------

1) Engagement can have one user
Users can have many engagements

2) Modules can have one engagement
Engagements can have many modules

3) Users can have multiple engagements
engagements can have one user
	
---------------------------------------
</nocode>
Engagements:

List engagements				- GET      /engagements
List specific engagements		- GET	   /engagements/0
Add engagement					- POST     /engagements
delete engagement				- Delete   /engagements/0
Update engagement				- PUT	   /engagements/0

Modules:

List modules for an engagement 	- GET		/engagements/0/modules
add module to an engagement		- POST		/engagements/0/modules
delete module from engagement 	- Delete	/engagements/0/modules/0
Update module					- PUT		/engagements/0/modules/0

Users: 

List users						- GET		/users
Add User						- POST		/users
Delete User						- DELETE 	/users/0
Update User						- PUT		/users/0
</nocode>

-----------------------------------------------------------------------------

curl  -X GET    http://localhost:8080/bbframework/api/v0.1/engagements
curl  -X GET    http://localhost:8181/bbframework/api/v0.1/engagements
curl  -X GET    http://localhost:8181/bbframework/api/v0.1/engagement/1
curl  -X DELETE http://localhost:8181/bbframework/api/v0.1/engagement/1
curl  -X GET    http://localhost:8181/bbframework/api/v0.1/engagement/1/modules

