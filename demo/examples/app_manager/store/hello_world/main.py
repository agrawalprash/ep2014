from jigna.api import Template, QtApp

body_html = """
   <h2>Hello World</h2>
"""
template = Template(body_html=body_html)
app = QtApp(template=template)
app.start()
