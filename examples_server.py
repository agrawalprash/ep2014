from subprocess import Popen
from os.path import join, expanduser
from traits.api import HasTraits, Str, List
from jigna.api import Template, WebApp


#### Domain model ####

class ExamplesServer(HasTraits):
    """
    A simple examples server which executes examples in the jigna examples
    directory based on the user's requests.
    """

    root = Str
    def _root_default(self):
        return expanduser('~/work/jigna/examples/')

    selected_examples = List(Str)
    def _selected_examples_default(self):
        return ['simple_view', 'model_updates', 'method_call', 'method_call_slow',
            'list_of_instances', 'instance_trait', 'event_trait', 'success_error_callbacks',
            'simple_view_web', 'embedding_chaco', 'embedding_mayavi',
            'embedding_in_qt']

    def run_example(self, example_name):
        example_file = join(self.root, example_name + '.py')
        cmd = ['python', example_file]
        Popen(cmd, cwd=self.root)


#### UI layer ####

template = Template(html_file='presentation/index.html', base_url='presentation')

if __name__ == "__main__":
    examples_server = ExamplesServer()
    app = WebApp(
        template=template,
        context={'examples_server': examples_server},
        port=8000
    )

    app.start()
