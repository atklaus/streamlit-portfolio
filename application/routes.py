
from flask import render_template
from flask import current_app as app
from flask import Flask, request
import flask
import git
import dash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/interests')
def interests():
    return render_template('interests.html')

@app.route('/version')
def version():
    return '2.1.1'

@app.route('/plotly_dashboard') 
def render_dashboard():
    return flask.redirect('/project1/')


