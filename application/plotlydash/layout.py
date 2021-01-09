"""Plotly Dash HTML layout override."""

import dash
with open("application/templates/includes/nav.html", 'r') as temp:
    nav_html = temp.read().replace('\n', '')

with open("application/templates/includes/footer.html", 'r') as temp:
    footer_html = temp.read().replace('\n', '')

dash_tags = '''
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

dash_string = '''
    <section id="temp-1" class="dash-section">
        <div class="dash-container">
            <div id="temp-row-1" class="dash-row">
            {%app_entry%}            
            </div>
        </div>
    </section>
    {%config%}
    {%scripts%}
    {%renderer%}
'''

html_layout = dash_tags + nav_html + dash_string + footer_html
