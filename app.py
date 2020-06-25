from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import git

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/blog/blog.db'


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/update_server', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            repo = git.Repo('path/to/git_repo')
            origin = repo.remotes.origin


origin.pull()
return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400

@app.route('/version')
def version():
    return '0.2.7'


if __name__ == '__main__':
    app.run(debug=True)

