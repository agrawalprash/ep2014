from subprocess import Popen
from os.path import join, expanduser
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

    #: Root of the examples directory
    root = Str

    #: Filename of the example
    filename = Property(Str, depends_on=['root', 'ID'])
    def _get_filename(self):
        return join(self.root, self.ID + '.py')

    name = Property(Str, depends_on='ID')
    def _get_name(self):
        return self.ID.replace("_", " ").capitalize()

    #: Code representation
    code = Property(Str, depends_on='filename')
    def _get_code(self):
        return open(self.filename, 'r').read()

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

    app = WebApp(template=template, context={'server': examples_server}, port=8000)
    app.start()
