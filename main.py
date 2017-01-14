#!/usr/bin/env python

## To do:
#
# 1) Add database support and remove the enagements/tasks data structures
# 2) Implement a module (nmap) to get that working
# 3) Make sure that the tasks get added to the queue (celery/rabbitmq)
# 		a) add to queue
#		  b) check queue
#			c) return it from queue
#	4) once all the above work, all complete error checking, and create more modules..
# 5) Create a command line client, and web gui
#
#
#
#  Any other ideas whilst in this development stage?

from flask import Flask, jsonify, make_response, abort, request

BBFrameworkAPI = Flask(__name__)

ROOT_URL = "/bbframework/api/v0.1/"

engagements = [
        {'eng_id' : 0,
        'eng_name' : 'Ebay.com - NMap IP Block',
        'eng_desc' : "Scanning ebay.com ip block",
        'eng_user' : "dusty"},

        {'eng_id' : 1,
        'eng_name' : 'Amazon.co.uk',
        'eng_desc' : "Scanning amazon.co.uk ip block",
        'eng_user' : "dusty"}
]

tasks = [
        {'eng_id' : 0,
         'task_id' : 0,
         'task_name' : "nmap",
         'task_desc' : "nmap scan of ip block",
         'task_args' : [],
         'task_user' : "dusty"},

        {'eng_id' : 1,
         'task_id' : 1,
         'task_name' : "dnsrecon",
         'task_desc' : "dns enumeration",
         'task_args' : ["-d", "127.0.0.1"],
         'task_user' : "dusty"},
]

## Error handlers
@BBFrameworkAPI.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error' : "Resource not found!"}), 404)

## GET a list of engagements
@BBFrameworkAPI.route(ROOT_URL + "engagements", methods=['GET'])
def api_list_engagements():
        return jsonify({'engagements' : engagements})

## Return a specific engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>", methods=['GET'])
def api_get_engagement(engagement_id):
        engagement = [engagement for engagement in engagements if engagement['eng_id'] == engagement_id]
        if len(engagement) == 0:
                abort(404)
        return jsonify({'engagements' : engagement[0]})

## Create an engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements", methods=['POST'])
def api_add_engagement():
        if not request.json or not 'engagement_name' in request.json:
                abort(400)
        if len(engagements) == 0:
                new_engagement = {
                'eng_id' : 0,
                'eng_name' : request.json.get('engagement_name', ""),
                'eng_desc' : request.json.get('engagement_desc', ""),
                'eng_user' : request.json.get('eng_user', "")
                }
        else:
                new_engagement = {
                        'eng_id' : engagements[-1]['eng_id'] + 1,
                        'eng_name' : request.json.get('engagement_name', ""),
                        'eng_desc' : request.json.get('engagement_desc', ""),
                        'eng_user' : request.json.get('eng_user', "")
                }
        engagements.append(new_engagement)
        return jsonify({'engagement' : new_engagement}), 201

## Delete an engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>", methods=['DELETE'])
def api_delete_engagement(engagement_id):
        engagement = [engagement for engagement in engagements if engagement['eng_id'] == engagement_id]
        if len(engagement) == 0:
                abort(404)
        engagements.remove(engagement[0])
        return jsonify({'result' : True})


## GET a list of tasks for a specific engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>/tasks", methods=["GET"])
def api_list_engagement_tasks(engagement_id):
        rtask = [t for t in tasks if t['eng_id'] == engagement_id]
        if len(rtask) == 0:
                abort(404)
        else:
                return jsonify(rtask)

## Create a task for a specific engagement
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>/tasks", methods=["POST"])
def api_add_engagement_task(engagement_id):
        if not request.json or not 'task_name' in request.json:
                abort(404)
        if len(tasks) == 0:
                new_task =  {
                        'eng_id' : engagement_id,
                        'task_id' : 0,
                        'task_name' : request.json.get("task_name", ""),
                        'task_desc' : request.json.get("task_desc", ""),
                        'task_args' : request.json.get("task_args", ""),
                        'task_user' : request.json.get("task_user", "")
                }
        else:
                new_task =  {
                        'eng_id' : engagement_id,
                        'task_id' : tasks[-1]['task_id'] + 1,
                        'task_name' : request.json.get("task_name", ""),
                        'task_desc' : request.json.get("task_desc", ""),
                        'task_args' : request.json.get("task_args", ""),
                        'task_user' : request.json.get("task_user", "")
                }
        tasks.append(new_task)
        return jsonify({'task' : new_task}), 201

## Delete a specific engagements task
@BBFrameworkAPI.route(ROOT_URL + "engagements/<int:engagement_id>/tasks/<int:task_id>", methods=['DELETE'])
def api_delete_engement_task(engagement_id,task_id):
        t = [t for t in tasks if t['task_id'] == task_id]
        if len(tasks) == 0:
                abort(404)
        tasks.remove(t[0])
        return jsonify({'result' : True})

if __name__ == "__main__":
        BBFrameworkAPI.run(debug=True, host="0.0.0.0", port=8080)
