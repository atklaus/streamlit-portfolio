"""Plotly Dash HTML layout override."""

import dash
with open("application/templates/includes/nav.html", 'r') as temp:
    NAV_HTML = temp.read().replace('\n', '')

with open("application/templates/includes/footer.html", 'r') as temp:
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

HTML_LAYOUT = DASH_HEADER + NAV_HTML + CUSTOM_STRING + DASH_FOOTER + FOOTER_HTML
