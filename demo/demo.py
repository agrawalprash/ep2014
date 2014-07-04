from jigna.api import Template, WebApp


template = Template(html_file='demo.html', recommended_size=(1400, 800))

app = WebApp(template=template, context={}, port=8000)
app.start()
