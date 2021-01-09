"""Plotly Dash HTML layout override."""

import dash

html_layout = '''
<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>{%title%}
    </title>
    {%favicon%}
    {%css%}
  </head>
  <div id="igeai" class="gpd-navbar main-nav-bar">
    <div id="i33xc" class="gpd-container">
      <div id="i54ff" class="gdp-row">
        <div id="iok7h" class="cell logo-box">
          <a id="ie6up" class="gpd-link-box main-logo-box">
            <img id="iockf" src="https://cdn.grapedrop.com/u0e8c2eda803f4757a1488f6bc8b68881/3523ba756d344863bb3b7e2fea8052dc_adc_logo.png"/>
          </a>
          <div id="i56s7" class="gpd-text">Almost
            <br>Data
            <br>​​​​​​​Science
            <br>
          </div>
        </div>
        <div id="ik0zo" class="cell gpd-navbar__menu">
          <a id="ikdod" href="" class="gpd-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M3 6h18v2H3V6m0 5h18v2H3v-2m0 5h18v2H3v-2z">
              </path>
            </svg>
          </a>
        </div>
        <div id="ij7oc" class="cell gpd-navbar__items">
          <div id="i4dfto">
            <a id="izkljc" href="{{url_for('index')}}" class="gpd-link-box nav-icon">
              <span id="i8thax" class="gpd-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8h5z">
                  </path>
                </svg>
              </span>
            </a>
            <a id="ixlf88" href="{{ url_for('about') }}" class="gpd-link-box nav-icon">
              <span id="iilevd" class="gpd-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M13 9h-2V7h2m0 10h-2v-6h2m-1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z">
                  </path>
                </svg>
              </span>
            </a>
            <a id="ipnudr" href="https://github.com/atklaus?tab=repositories" target="_blank" class="gpd-link-box nav-icon">
              <span id="iyoxl" class="gpd-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M5 3h14c1.1 0 2 .9 2 2v14c0 1.1-.9 2-2 2h-4.44c-.32-.07-.33-.68-.33-.89l.01-2.47c0-.84-.29-1.39-.61-1.67 2.01-.22 4.11-.97 4.11-4.44 0-.98-.35-1.79-.92-2.42.09-.22.4-1.14-.09-2.38 0 0-.76-.23-2.48.93-.72-.2-1.48-.3-2.25-.31-.76.01-1.54.11-2.25.31-1.72-1.16-2.48-.93-2.48-.93-.49 1.24-.18 2.16-.09 2.38-.57.63-.92 1.44-.92 2.42 0 3.47 2.1 4.22 4.1 4.47-.26.2-.49.6-.57 1.18-.52.23-1.82.63-2.62-.75 0 0-.48-.86-1.38-.93 0 0-.88 0-.06.55 0 0 .59.28 1 1.32 0 0 .52 1.75 3.03 1.21l.01 1.53c0 .21-.02.82-.34.89H5c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2z">
                  </path>
                </svg>
              </span>
            </a>
            <a id="inffs" href="https://www.linkedin.com/in/adam-klaus/" target="_blank" class="gpd-link-box nav-icon">
              <span id="i0x1a" class="gpd-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M19 3c1.1 0 2 .9 2 2v14c0 1.1-.9 2-2 2H5c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2h14m-.5 15.5v-5.3c0-1.8-1.46-3.26-3.26-3.26-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4.77 0 1.4.63 1.4 1.4v4.93h2.79M6.88 8.56a1.686 1.686 0 0 0 0-3.37c-.93 0-1.69.76-1.69 1.69 0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z">
                  </path>
                </svg>
              </span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
  <section id="itf5s" class="gpd-section">
  </section>
  <div id="i7qq5v" class="gpd-shape-divider gpd-shape-divider--fl-v-h" data-gjs-type="shape-divider" data-gjs-resizable="[object Object]" data-gjs-shape-divider="low-hills-split" data-gjs-flip-vert data-gjs-flip-horiz data-gjs-custom-name="Shape divider">
    <svg preserveAspectRatio="none" viewBox="0 0 240 24">
      <path fill-opacity=".3" d="M240 24V0c-51.8 0-69.9 13.2-94.7 15.6-24.7 2.4-43.9-1.2-63.8-1-19.1 0-31.2 3.6-51.3 6.5A126 126 0 010 22V24h240z"/>
      <path fill-opacity=".3" d="M240 24V2.2c-51.8 0-69.9 12-94.7 14.2-24.7 2.1-43.9-1.1-63.8-1-19.1 0-31.2 3.3-51.3 6-14.6 1.8-25.9 1.2-30.2.8V24h240z"/>
      <path d="M240 24V3.7c-51.8 0-69.9 11.7-94.7 14-24.7 2.4-43.9-3.2-63.8-3.1-19.1 0-31.2 3.6-51.3 6.5a128 128 0 01-30.2 1V24h240z"/>
    </svg>
  </div>


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
  <div id="i7r0vq" class="gpd-shape-divider gpd-shape-divider--fl-v-h">
    <svg class="gpd-shape-divider-inv" preserveAspectRatio="none" viewBox="0 0 240 24">
      <path fill-opacity=".3" d="M240 0H0v23.5c4.3.5 15.5 1.2 30.2-.9 20.1-2.8 32.1-6.2 51.3-6.3 20 0 39 3.4 63.8 1 24.8-2.2 42.9-15 94.7-15"/>
      <path fill-opacity=".3" d="M240 0H0v23.4c4.3.4 15.5 1.2 30.2-1 20.1-3.1 32.1-6.9 51.3-7 20 0 39 6 63.8 3.4C170 16.3 188.2 4 240 4"/>
      <path d="M0 23.3c4.3.5 15.5 1.3 30.2-1 20.1-3 32.1-6.8 51.3-7 20 0 39 3.8 63.8 1.2C170 14 188.2 0 240 0H0v23.3z"/>
    </svg>
  </div>
  <div class="gpd-container" id="itbqe" data-gjs-type="container">
    <div id="ivi361" data-gjs-type="divider" data-gjs-style="[object Object]">
    </div>
    <div id="infzsb" class="gdp-row" data-gjs-type="grid-row">
      <div class="cell" data-gjs-type="grid-item">
        <div id="itpjjh" class="gdp-row" data-gjs-type="grid-row">
          <div class="cell footer-column" data-gjs-type="grid-item">
            <h4 class="footer-title" data-gjs-type="header">Pages
            </h4>
            <a id="i104le" href="" class="gpd-link footer-link" data-gjs-type="link">About Me
            </a>
            <a id="iq460j" class="gpd-link footer-link" data-gjs-type="link" data-gjs-view="">Podcast Recs
            </a>
          </div>
          <div id="ikeiog" class="cell footer-column" data-gjs-type="grid-item" data-gjs-view="">
            <h4 class="footer-title" data-gjs-type="header" data-gjs-view="">Artist Credits
            </h4>
            <a id="ifmeek" class="gpd-link footer-link" data-gjs-type="link" data-gjs-view="">Main Logo:&nbsp;
            </a>
            <a id="i0a0b5" class="gpd-link footer-link" data-gjs-type="link" data-gjs-view="">Icons:
            </a>
          </div>
          <div id="i4a6eg" class="cell footer-column" data-gjs-type="grid-item" data-gjs-view="">
            <h4 class="footer-title" data-gjs-type="header" data-gjs-view="">Contact
            </h4>
            <a id="isxhjm" href="" class="gpd-link footer-link" data-gjs-type="link" data-gjs-view="">atklaus@wisc.edu
            </a>
            <a href="{{ url_for('static', filename='images/AdamKlaus.pdf') }}" target="_blank" id="isxhjm" href="" class="gpd-link footer-link" data-gjs-type="link" data-gjs-view="">Resume
            </a>
          </div>
          <div id="i4a6eg" class="cell footer-column" data-gjs-type="grid-item" data-gjs-view="">
            <h4 class="footer-title" data-gjs-type="header" data-gjs-view="">About This Page
            </h4>
            <a id="isxhjm" href="" class="gpd-link footer-link" data-gjs-type="link" data-gjs-view="">Website coded in HTML, CSS, JavaScript, template from GrapeDrop on Flask framework with embedded Plotly Dash visuals hosted on PythonAnywhere.com 
            </a>
          </div>
          <div id="i0bvnn" class="cell" data-gjs-type="grid-item">
            <div class="gdp-row" id="ii2har" data-gjs-type="grid-row">
              <div id="ivyzt7" class="cell" data-gjs-type="grid-item">
                <a id="ih74bg" href="" target="_blank" class="gpd-link-box footer-social-link" data-gjs-type="link-box">
                  <span id="iejtb" class="gpd-icon" data-gjs-type="icon-v2" data-gjs-view="">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" data-gjs-type="svg" data-gjs-view="">
                      <path d="M5 3h14c1.1 0 2 .9 2 2v14c0 1.1-.9 2-2 2h-4.44c-.32-.07-.33-.68-.33-.89l.01-2.47c0-.84-.29-1.39-.61-1.67 2.01-.22 4.11-.97 4.11-4.44 0-.98-.35-1.79-.92-2.42.09-.22.4-1.14-.09-2.38 0 0-.76-.23-2.48.93-.72-.2-1.48-.3-2.25-.31-.76.01-1.54.11-2.25.31-1.72-1.16-2.48-.93-2.48-.93-.49 1.24-.18 2.16-.09 2.38-.57.63-.92 1.44-.92 2.42 0 3.47 2.1 4.22 4.1 4.47-.26.2-.49.6-.57 1.18-.52.23-1.82.63-2.62-.75 0 0-.48-.86-1.38-.93 0 0-.88 0-.06.55 0 0 .59.28 1 1.32 0 0 .52 1.75 3.03 1.21l.01 1.53c0 .21-.02.82-.34.89H5c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2z" data-gjs-type="svg-in" data-gjs-view="">
                      </path>
                    </svg>
                  </span>
                </a>
              </div>
              <div id="i3s2ua" class="cell" data-gjs-type="grid-item" data-gjs-view="">
                <a href="" target="_blank" class="gpd-link-box footer-social-link" data-gjs-type="link-box" data-gjs-view="">
                  <span id="i35zto" class="gpd-icon" data-gjs-type="icon-v2" data-gjs-view="">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" data-gjs-type="svg">
                      <path d="M5 3h14c1.1 0 2 .9 2 2v14c0 1.1-.9 2-2 2H5c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2m12.71 6.33c.48-.4 1.04-.88 1.29-1.41-.41.21-.9.34-1.44.41.5-.36.91-.83 1.12-1.47-.52.28-1.05.52-1.71.64-1.55-1.87-5.26-.35-4.6 2.45-2.61-.16-4.2-1.34-5.52-2.79-.75 1.22-.1 3.07.79 3.58-.46-.03-.81-.17-1.14-.33.04 1.54.89 2.28 2.08 2.68-.36.07-.76.09-1.14.03.37 1.07 1.14 1.74 2.46 1.88-.9.76-2.56 1.29-3.9 1.08 1.15.73 2.46 1.31 4.28 1.23 4.41-.2 7.36-3.36 7.43-7.98z" data-gjs-type="svg-in">
                      </path>
                    </svg>
                  </span>
                </a>
              </div>
              <div id="i3im0b" class="cell" data-gjs-type="grid-item" data-gjs-view="">
                <a href="" target="_blank" class="gpd-link-box footer-social-link" data-gjs-type="link-box" data-gjs-view="">
                  <span id="i54mfi" class="gpd-icon" data-gjs-type="icon-v2" data-gjs-view="">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" data-gjs-type="svg">
                      <path d="M19 3c1.1 0 2 .9 2 2v14c0 1.1-.9 2-2 2H5c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2h14m-.5 15.5v-5.3c0-1.8-1.46-3.26-3.26-3.26-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4.77 0 1.4.63 1.4 1.4v4.93h2.79M6.88 8.56a1.686 1.686 0 0 0 0-3.37c-.93 0-1.69.76-1.69 1.69 0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z" data-gjs-type="svg-in">
                      </path>
                    </svg>
                  </span>
                </a>
              </div>
            </div>
            <div class="gdp-row" id="ivhu0g" data-gjs-type="grid-row" data-gjs-view="">
              <div class="cell" id="iw1ity" data-gjs-type="grid-item" data-gjs-view="">
                <div id="iexxr" class="gpd-text" data-gjs-type="text" data-gjs-view="">© 2020 Copyright, All Right Reserved. almostdatascience.com
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</html>
'''

# class CustomDash(dash.Dash):
#     def interpolate_index(self, **kwargs):
#         # Inspect the arguments by printing them
#         print(kwargs)
#         return '''
#         <!DOCTYPE html>
#         <html>
#             <head>
#                 <title>My App</title>
#             </head>
#             {nav}
#             <body>
#                 <div id="custom-header">My custom header</div>
#                 {app_entry}
#                 {config}
#                 {scripts}
#                 {renderer}
#                 <div id="custom-footer">My custom footer</div>
#             </body>
#         </html>
#         '''.format(
#             app_entry=kwargs['app_entry'],
#             config=kwargs['config'],
#             scripts=kwargs['scripts'],
#             renderer=kwargs['renderer'],
#             nav=kwargs['nav'])
