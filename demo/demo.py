import imp
import os
from bs4 import BeautifulSoup
from subprocess import Popen
from os.path import join, expanduser, abspath
from traits.api import HasTraits, Str, List, Property
from jigna.api import Template, WebApp

#### Domain model ####

class Example(HasTraits):
    """
    A class representing a jigna example. It contains the human readable name of
    the example, the filename of the example and the codestring that tells the
    domain model and the template used in that model.
    """

    #: Identifier of the example (eg. 'simple_view')
    ID = Str

    #: Root of the example directory
    root = Str

    #: Filename of the example
    filename = Property(Str, depends_on=['ID'])
    def _get_filename(self):
        return self.ID + '.py'

    name = Property(Str, depends_on='ID')
    def _get_name(self):
        return self.ID.replace("_", " ").capitalize()

    #: Code representation
    code = Property(Str, depends_on='filename')
    def _get_code(self):
        return open(join(self.root, self.filename), 'r').read()

    #: Domain model code representation
    domain_model_code = Property(Str, depends_on='code')
    def _get_domain_model_code(self):
        from_domain_model = self.code.split('#### Domain model ####\n')[1]
        return from_domain_model.split("\n#### UI layer ####")[0]

    #: UI layer code representation
    ui_layer_code = Property(Str, depends_on=['filename', 'root'])
    def _get_ui_layer_code(self):
        # change the directory temporarily to the examples root directory
        old_curdir = abspath(os.curdir)
        os.chdir(self.root)

        # load the template from the example
        example = imp.load_source(self.ID, self.filename)
        soup = BeautifulSoup(example.template.html)

        # change back the current directory
        os.chdir(old_curdir)

        return "".join([str(x) for x in soup.body.prettify()])

    def run(self):
        """
        Run the example
        """
        cmd = ['python', self.filename]
        Popen(cmd, cwd=self.root)

class ExamplesServer(HasTraits):
    """
    A simple examples server which executes examples in the jigna examples
    directory based on the user's requests.
    """

    root = Str

    examples = List(Example)
    def _examples_default(self):
        example_ids = [
            'simple_view',
            'model_updates',
            'method_call',
            'method_call_slow',
            'list_of_instances',
            'instance_trait',
            'event_trait',
            'success_error_callbacks',
            'simple_view_web',
            'embedding_chaco',
            'embedding_in_qt'
        ]

        examples = []
        for example_id in example_ids:
            examples.append(Example(root=self.root, ID=example_id))

        return examples

#### UI layer ####

template = Template(html_file='demo.html', recommended_size=(1400, 800))

#### Entry point ####

if __name__ == '__main__':
    examples_server = ExamplesServer(root=expanduser('~/work/jigna/examples'))

    examples_server.examples.extend([
        Example(root='examples', ID='employee_simple')
    ])

    app = WebApp(template=template, context={'server': examples_server}, port=8000)
    app.start()
