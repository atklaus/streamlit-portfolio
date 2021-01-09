

with open("application/templates/includes/nav.html", 'r') as temp:
    nav_html = temp.read().replace('\n', '')


with open("application/templates/includes/footer.html", 'r') as temp:
    footer_html = temp.read().replace('\n', '')

nav_html + footer_html



nav_html.read()

