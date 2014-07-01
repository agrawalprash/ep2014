import SimpleHTTPServer
import BaseHTTPServer
from subprocess import Popen
from os.path import join, expanduser

class ExamplesRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    A simple examples server which executes examples in the jigna examples
    directory based on the user's requests.
    """

    EXAMPLES_DIRECTORY = expanduser('~/work/jigna/examples/')

    def do_GET(self):
        # obtain the example file that needs to be executed
        example_file = join(self.EXAMPLES_DIRECTORY, self.path.lstrip('/')) + '.py'

        # execute it
        cmd = ['python', example_file]
        Popen(cmd, cwd=self.EXAMPLES_DIRECTORY).wait()

        # send an OK response
        self.send_response(200, 'OK')

PORT = 9000

httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', PORT), ExamplesRequestHandler)

print "serving at port", PORT
httpd.serve_forever()
