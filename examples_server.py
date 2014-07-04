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

    #: Root of the examples directory
    root = Str

    #: Filename of the example
    filename = Str

    #: Human readable name of the example
    name = Property(Str, depends_on='filename')
    def _get_name(self):
        return self.filename[:-3].replace("_", " ").capitalize()

    def run(self):
        """
        Run the example
        """
        cmd = ['python', join(self.root, self.filename)]
        Popen(cmd, cwd=self.root)
        print "returning now"

class ExamplesServer(HasTraits):
    """
    A simple examples server which executes examples in the jigna examples
    directory based on the user's requests.
    """

    root = Str

    examples = List(Example)
    def _examples_default(self):
        examples = []
        example_names = [
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

        for example_name in example_names:
            examples.append(Example(root=self.root, filename=example_name+".py"))

        return examples

#### UI layer ####

template = Template(html_file='presentation/index.html', base_url='presentation')

if __name__ == "__main__":
    examples_server = ExamplesServer(root=expanduser('~/work/jigna/examples'))
    app = WebApp(
        template=template,
        context={'examples_server': examples_server},
    )

    app.start()
