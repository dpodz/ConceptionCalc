from flask import Flask, jsonify, render_template, request
import histopy
import datetime
import random
app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=str)
    b = request.args.get('b', 0, type=int)
    print (a)
    today = datetime.datetime.strptime(a, '%Y-%m-%d')
    today_in_history = histopy.load_history(today)
    events = histopy.load_events(today_in_history)
    random_year = random.randint(0, (len(events)-1))
    resp = events[random_year]
    return jsonify(year=resp[0],desc = resp[1], wiki = resp[2])

@app.route('/')
def index():
    return "Hello"

app.run()

##from flask import Flask
##from flask import jsonify
##from flask import render_template
### -*- coding: utf-8 -*-
##from datetime import timedelta
##from flask import make_response, request, current_app
##from functools import update_wrapper
##
##
##def crossdomain(origin=None, methods=None, headers=None,
##                max_age=21600, attach_to_all=True,
##                automatic_options=True):
##    if methods is not None:
##        methods = ', '.join(sorted(x.upper() for x in methods))
##    if headers is not None and not isinstance(headers, basestring):
##        headers = ', '.join(x.upper() for x in headers)
##    if not isinstance(origin, basestring):
##        origin = ', '.join(origin)
##    if isinstance(max_age, timedelta):
##        max_age = max_age.total_seconds()
##
##    def get_methods():
##        if methods is not None:
##            return methods
##
##        options_resp = current_app.make_default_options_response()
##        return options_resp.headers['allow']
##
##    def decorator(f):
##        def wrapped_function(*args, **kwargs):
##            if automatic_options and request.method == 'OPTIONS':
##                resp = current_app.make_default_options_response()
##            else:
##                resp = make_response(f(*args, **kwargs))
##            if not attach_to_all and request.method != 'OPTIONS':
##                return resp
##
##            h = resp.headers
##            h['Access-Control-Allow-Origin'] = origin
##            h['Access-Control-Allow-Methods'] = get_methods()
##            h['Access-Control-Max-Age'] = str(max_age)
##            h['Access-Control-Allow-Credentials'] = 'true'
##            h['Access-Control-Allow-Headers'] = \
##                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
##            if headers is not None:
##                h['Access-Control-Allow-Headers'] = headers
##            return resp
##
##        f.provide_automatic_options = False
##        return update_wrapper(wrapped_function, f)
##    return decorator
##
##
##app = Flask(__name__)
##
##@app.after_request
##def after_request(response):
##  response.headers.add('Access-Control-Allow-Origin', '*')
##  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
##  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
##  return response
##
##@app.route("/")
##def index():
##    resp = ["1997", "Daniels Bday", "WOW!"]
##    return jsonify(array=resp)
##
##@app.route('/signUp')
##def signUp():
##    return render_template('signUp.html')
##
##@app.route('/signUpUser', methods=['POST'])
##@crossdomain(origin='*')
##def signUpUser():
##    user =  request.form['username'];
##    password = request.form['password'];
##    return json.dumps({'status':'OK','user':user,'pass':password});
##app.run()
