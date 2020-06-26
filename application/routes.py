
from flask import render_template
from flask import current_app as app

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



