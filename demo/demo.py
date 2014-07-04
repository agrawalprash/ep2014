from jigna.api import Template, WebApp


template = Template(html_file='demo.html')

app = WebApp(template=template, context={}, port=8000)
app.start()
