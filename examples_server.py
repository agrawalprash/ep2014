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
        return self.filename.replace("_", " ").capitalize()

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

    examples = Property(List(Example), depends_on='selected_examples')
    def _get_examples(self):
        examples = []
        for example_name in self.selected_examples:
            examples.append(Example(root=self.root, filename=example_name+".py"))

        return examples

    selected_examples = List(Str)
    def _selected_examples_default(self):
        return [
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

#### UI layer ####

template = Template(html_file='presentation/index.html', base_url='presentation')

if __name__ == "__main__":
    examples_server = ExamplesServer(root=expanduser('~/work/jigna/examples'))
    app = WebApp(
        template=template,
        context={'examples_server': examples_server},
    )

    app.start()
