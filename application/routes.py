
from flask import render_template
from flask import current_app as app
from flask import Flask, request
import git
import time
import re
import os
import requests

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/soon')
def soon():
    return render_template('soon.html')


@app.route('/version')
def version():
    return '1.1.1'


@app.route('/dash')
def testdash():
    """Landing page."""
    return render_template(
        'index.jinja2',
        title='Plotly Dash Flask Tutorial',
        description='Embed Plotly Dash into your Flask applications.',
        template='home-template',
        body="This is a homepage served with Flask."
    )

@app.route('/update_server', methods=['GET','POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/var/www/')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400



# @app.route('/update_server', methods=['POST'])
# def webhook():
#     if request.method != 'POST':
#         return 'OK'
#     else:
#         abort_code = 418
#         # Do initial validations on required headers
#         if 'X-Github-Event' not in request.headers:
#             abort(abort_code)
#         if 'X-Github-Delivery' not in request.headers:
#             abort(abort_code)
#         if 'X-Hub-Signature' not in request.headers:
#             abort(abort_code)
#         if not request.is_json:
#             abort(abort_code)
#         if 'User-Agent' not in request.headers:
#             abort(abort_code)
#         ua = request.headers.get('User-Agent')
#         if not ua.startswith('GitHub-Hookshot/'):
#             abort(abort_code)

#         event = request.headers.get('X-GitHub-Event')
#         if event == "ping":
#             return json.dumps({'msg': 'Hi!'})
#         if event != "push":
#             return json.dumps({'msg': "Wrong event type"})

#         x_hub_signature = request.headers.get('X-Hub-Signature')
#         # webhook content type should be application/json for request.data to have the payload
#         # request.data is empty in case of x-www-form-urlencoded
#         if not is_valid_signature(x_hub_signature, request.data, w_secret):
#             print('Deploy signature failed: {sig}'.format(sig=x_hub_signature))
#             abort(abort_code)

#         payload = request.get_json()
#         if payload is None:
#             print('Deploy payload is empty: {payload}'.format(
#                 payload=payload))
#             abort(abort_code)

#         if payload['ref'] != 'refs/heads/master':
#             return json.dumps({'msg': 'Not master; ignoring'})

#         repo = git.Repo('/var/www/sites/mysite')
#         origin = repo.remotes.origin

#         pull_info = origin.pull()

#         if len(pull_info) == 0:
#             return json.dumps({'msg': "Didn't pull any information from remote!"})
#         if pull_info[0].flags > 128:
#             return json.dumps({'msg': "Didn't pull any information from remote!"})

#         commit_hash = pull_info[0].commit.hexsha
#         build_commit = f'build_commit = "{commit_hash}"'
#         print(f'{build_commit}')
#         return 'Updated PythonAnywhere server to commit {commit}'.format(commit=commit_hash)




