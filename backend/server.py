#!/usr/bin/env pythonn

from bottle import route, run, response
import simplejson as json
from gcfind import gcfind

@route('/gcfind/<query>')
def index(query=''):
	response.set_header('Access-Control-Allow-Origin', '*')
	response.content_type = "application/json; charset=UTF8"
	result = json.dumps([c for c in gcfind(query)])
	return result

run(host='0.0.0.0', port=52052)
#run(host='127.0.0.1', port=52052)
