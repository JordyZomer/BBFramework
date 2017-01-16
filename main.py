#!/usr/bin/env python

import MySQLdb

from flask import Flask, jsonify, make_response, abort, request

BBFrameworkAPI = Flask(__name__)

## Config
#
# Database:
DBSERVER = '127.0.0.1'
DBUSER   = 'bbframeworkdbuser'
DBPASSWD = 'password123'
DBNAME   = 'BBFrameworkAPI'

# Root URL
ROOT_URL = "/bbframework/api/v0.1/"

engagements = []
tasks = []


# Perform MySQL query, created so that we don't have to
# repeat the same code for each route.
def db_query(DBSERVER, DBUSER, DBPASSWD, DBNAME, QUERY):
        db = MySQLdb.connect(host=DBSERVER, user=DBUSER, passwd=DBPASSWD, db=DBNAME)
        cur = db.cursor()
        cur.execute((QUERY))
        columns = cur.description
        result = []
        for value in cur.fetchall():
                tmp = {}
                for (index, column) in enumerate(value):
                        tmp[columns[index][0]] = column
                result.append(tmp)
        db.commit()
        db.close()
        return result

## Hacky way to get how many entries in the tables:
def db_query_size(DBSERVER, DBUSER, DBPASSWD, DBNAME, QUERY):
        db = MySQLdb.connect(host=DBSERVER, user=DBUSER, passwd=DBPASSWD, db=DBNAME)
        cur = db.cursor()
        size = cur.execute((QUERY))
        db.commit()
        db.close()
        return size


## Error handlers
@BBFrameworkAPI.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error' : "Resource not found!"}), 404)

## List engagements
@BBFrameworkAPI.route(ROOT_URL + "engagements", methods=['GET'])
def api_list_engagements():
        query = "SELECT * FROM engagements"
        return jsonify({"Engagements: " : db_query(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)})

## Return a specific engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>", methods=['GET'])
def api_get_engagement(engagement_id):
        query = "SELECT * from engagements where eng_id = %d" % engagement_id
        return jsonify({"Engagement: " : db_query(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)})

## Create an engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements", methods=['POST'])
def api_add_engagement():
        if not request.json or not 'engagement_name' in request.json:
                abort(400)
        query = "SELECT * FROM engagements"
        eng_id = db_query_size(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)
        if (eng_id) == 0:
                new_eng_id = 0
                eng_name = request.json.get('engagement_name', ""),
                eng_desc = request.json.get('engagement_desc', ""),
                eng_user = request.json.get('eng_user', "")
                query = "INSERT INTO engagements values (%d, '%s', '%s', '%s')" %  (new_eng_id, eng_name[0], eng_desc[0], eng_user)
                size = db_query_size(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)
        else:
                new_eng_id = (eng_id-1) + 1
                eng_name = request.json.get('engagement_name', ""),
                eng_desc = request.json.get('engagement_desc', ""),
                eng_user = request.json.get('eng_user', "")
                query = "INSERT INTO engagements values (%d, '%s', '%s', '%s')" %  (new_eng_id, eng_name[0], eng_desc[0], eng_user)
                size = db_query_size(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)

        query = "SELECT * from engagements where eng_id = %d" % new_eng_id
        return jsonify({"Engagement Added: " : db_query(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)})




## Delete an engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>", methods=['DELETE'])
def api_delete_engagement(engagement_id):
        query = "DELETE FROM engagements where eng_id=(%d)" % engagement_id
        size = db_query_size(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)
        if (size) == 0:
                return jsonify({"Result: " : False})
        else:
                return jsonify({"Result: " : True})


## GET a list of tasks for a specific engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>/tasks", methods=["GET"])
def api_list_engagement_tasks(engagement_id):
        query = "SELECT * from tasks where eng_id = (%d)" % engagement_id
        return jsonify({"Task: " : db_query(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)})


## Create a task for a specific engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>/tasks", methods=["POST"])
def api_add_engagement_task(engagement_id):
        if not request.json or not 'task_name' in request.json:
                abort(404)
        query = "SELECT task_id from tasks where eng_id = (%d)" % engagement_id
        task_id = db_query_size(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)
        eng_id = engagement_id
        if (task_id) == 0:
                new_task_id = 0
                task_name = request.json.get('task_name', ""),
                task_desc = request.json.get('task_desc', ""),
                task_args = request.json.get('task_args', ""),
                task_user = request.json.get('task_user', "")
                query = "INSERT INTO tasks VALUES (%d, %d, '%s', '%s', '%s', '%s')" % (eng_id, new_task_id, task_name[0], task_desc[0], task_args[0], task_user)
                size = db_query_size(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)

        else:
                new_task_id = (task_id-1) + 1
                task_name = request.json.get('task_name', ""),
                task_desc = request.json.get('task_desc', ""),
                task_args = request.json.get('task_args', ""),
                task_user = request.json.get('task_user', "")
                query = "INSERT INTO tasks VALUES (%d, %d, '%s', '%s', '%s', '%s')" % (eng_id, new_task_id, task_name[0], task_desc[0], task_args[0], task_user)
                size = db_query_size(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)

        query = "SELECT * from tasks where eng_id = %d and task_id = %d" % (eng_id, new_task_id)
        return jsonify({"Task Added: " : db_query(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)})




## Delete a specific engagements task
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>/tasks/<int:task_id>", methods=['DELETE'])
def api_delete_engement_task(engagement_id,task_id):
        query = "DELETE FROM tasks where eng_id=(%d) and task_id=(%d)" % (engagement_id, task_id)
        size = db_query_size(DBSERVER, DBUSER, DBPASSWD, DBNAME, query)
        if (size) == 0:
                return jsonify({"Result: " : False})
        else:
                return jsonify({"Result: " : True})




if __name__ == "__main__":
        BBFrameworkAPI.run(debug=True, host="0.0.0.0", port=8080)
