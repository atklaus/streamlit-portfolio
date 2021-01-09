"""Plotly Dash HTML layout override."""

from ..config import BASE_DIR
import dash
import os

with open(os.path.join(BASE_DIR,'templates','includes','nav.html'), 'r') as temp:
    NAV_HTML = temp.read().replace('\n', '')

with open(os.path.join(BASE_DIR,'templates','includes','footer.html')) as temp:
    FOOTER_HTML = temp.read().replace('\n', '')

DASH_HEADER = '''
<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>{%title%}
    </title>
    {%favicon%}
    {%css%}
  </head>
  '''

CUSTOM_STRING = '''
    <section id="temp-1" class="dash-section">
        <div class="dash-container">

            {%app_entry%}            
        </div>
    </section>
'''

DASH_FOOTER = '''
{%config%}
{%scripts%}
{%renderer%}
'''


about = '''{{url_for(\'index\')}}'''
index = '''{{ url_for(\'about\') }}'''
about_new = r'''https://almostdatascience.com'''
index_new = r'''https://almostdatascience.com/about'''
# main = '''"almostdatascience.com"'''

NAV_HTML = NAV_HTML.replace(about,about_new)
NAV_HTML = NAV_HTML.replace(index,index_new)

# NAV_HTML = NAV_HTML.replace("{{url_for('about')}}",'''"https://almostdatascience.com/about"''')


HTML_LAYOUT = DASH_HEADER + NAV_HTML + CUSTOM_STRING + DASH_FOOTER + FOOTER_HTML
