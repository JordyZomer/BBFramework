from app import fields 

engagement_fields = {
        'eng_id' : fields.String,
        'eng_name' : fields.String,
        'eng_desc' : fields.String,
        'eng_user_id' : fields.String
}
module_fields = {
        'eng_id' : fields.String,
        'module_id' : fields.String,
        'module_name' : fields.String,
        'module_desc' : fields.String,
        'module_args' : fields.String,
        'module_user_id' : fields.String,
}
user_fields = {
        'user_id' : fields.String,
        'username' : fields.String,
        'password' : fields.String,
}

error_fields = {
	'err_type' : fields.String, 
	'err_desc' : fields.String
}
