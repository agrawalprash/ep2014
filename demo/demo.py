import imp
import os
from textwrap import dedent
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

    #: Python side code representation
    python_code = Str
    def _python_code_default(self):
        from_domain_model = self.code.split('#### Domain model ####\n')[1]
        return from_domain_model.split("\n#### UI layer ####")[0]

    #: The command to run the example.
    command = Str
    def _command_default(self):
        return 'python %s' % self.filename

    #: HTML side code representation
    html_code = Str
    def _html_code_default(self):
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
        cmd = self.command.split()
        Popen(cmd, cwd=self.root)

class ExamplesServer(HasTraits):
    """
    A simple examples server which executes examples in the jigna examples
    directory based on the user's requests.
    """

    root = Str

    examples = List(Example)
    def _examples_default(self):

        examples = [
            Example(
                root=self.root,
                ID='simple_view',
                python_code=dedent("""
                    class Person(HasTraits):
                        name = Str
                        age = Int

                    person = Person(...)

                    app = QtApp(template=template,
                                context={'person': person})
                    app.start()
                """),
                html_code=dedent("""
                    Name: <input ng-model="person.name">
                    Age: <input ng-model="person.age">
                """)
            ),

            Example(
                root=self.root,
                ID='model_updates',
                python_code=dedent("""
                    class MOTD(HasTraits):
                        message = Str

                        def update_message(self, message):
                            self.message = message

                    ...

                    do_after(2500, motd.update_message,
                             'Flat is better than nested')
                """),
                html_code=dedent("""
                    Message of the day: {{motd.message}}
                """)
            ),

            Example(
                root=self.root,
                ID='instance_trait',
                python_code=dedent("""
                    class Person(HasTraits):
                        name = Str
                        spouse = Instance(Person)
                """),
                html_code=dedent("""
                    Person: {{person.name}}
                    Spouse: {{person.spouse.name}}
                """)
            ),

            Example(
                root=self.root,
                ID='list_of_instances',
                python_code=dedent("""
                    class Person(HasTraits):
                        name = Str
                        friends = List(Person)
                """),
                html_code=dedent("""
                    <div ng-repeat='friend in person.friends'>
                        {{friend.name}}
                    </div>
                """)
            ),

            Example(
                root=self.root,
                ID='method_call',
                python_code=dedent("""
                    class Person(HasTraits):
                        name = Str
                        spouse = Instance(Person)

                        def greet(self):
                            print "Hello " + self.name

                        def marry(self, person):
                            self.spouse = person
                """),
                html_code=dedent("""
                    <button ng-click='person.greet()'>
                        Greet
                    </button>

                    <button ng-click='person.marry(wilma)'>
                        Marry
                    </button>
                """)
            ),

            Example(
                root=self.root,
                ID='method_call_slow',
                python_code=dedent("""
                    class Installer(HasTraits):
                        progress = Int

                        def install(self, package):
                            while self.progress < 100:
                                time.sleep(0.5)
                                self.progress += 10
                """),
                html_code=dedent("""
                    <button ng-click='jigna.threaded(installer, "install", pandas)'>
                        Install Pandas
                    </button>
                """)
            ),

            Example(
                root=self.root,
                ID='event_trait',
                python_code=dedent("""
                    class Downloader(HasTraits):
                        files = List

                        file_downloaded = Event

                        def download_all(self):
                            for file in self.files:
                                self.download_file(file)

                                # Fire the `file_downloaded` event
                                self.file_downloaded = file
                """),
                html_code=dedent("""
                    <button ng-click='jigna.threaded(downloader, "download_all")'>
                        Download files
                    </button>

                    <script>
                        jigna.add_listener(downloader, 'file_downloaded', function(){
                            ...
                        })
                    </script>
                """)
            ),

            Example(
                root=self.root,
                ID='success_error_callbacks',
                python_code=dedent("""
                    class Worker(HasTraits):

                        def do_work(self):
                            time.sleep(5)

                        def do_illegal_work(self):
                            raise Exception
                """),
                html_code=dedent("""
                    <script>
                        jigna.threaded(worker, 'do_work').done(function(){
                            $scope.status = "Done"
                        })

                        jigna.threaded(worker, 'do_illegal_work').error(function(traceback){
                            $scope.status = "Error " + traceback
                        })
                    </script>
                """)
            ),

            Example(
                root=self.root,
                ID='simple_view_web',
                python_code=dedent("""
                    class Person(HasTraits):
                        name = Str
                        age = Int

                    person = Person(...)

                    app = WebApp(template=template,
                                 context={'person': person}, port=8000)
                    app.start()
                """),
                html_code=dedent("""
                    Name: <input ng-model="person.name">
                    Age: <input ng-model="person.age">
                """)
            ),

            Example(
                root=self.root,
                ID='embedding_mayavi',
                python_code=dedent("""
                    class SceneController(HasTraits):
                        n_longitudinal = Int
                        n_meridional = Int

                        def create_scene_widget(self):
                            ...
                            return QWidget(...)

                """),
                html_code=dedent("""
                    Plot:
                    <object widget-factory='scene.create_scene_widget'
                            type='application/x-qwidget'>
                    </object>
                """)
            ),

            Example(
                root=self.root,
                ID='embedding_in_qt',
                python_code=dedent("""
                    class Person(HasTraits):
                        name = Str
                        age = Int

                    person = Person(...)

                    app = QtApp(template=template,
                                context={'person': person})
                    qwidget = app.create_widget()

                    # Do whatever you like with this qwidget

                """),
                html_code=dedent("""
                    Name: <input ng-model="person.name">
                    Age: <input ng-model="person.age">
                """)
            ),

            Example(
                root='examples',
                ID='employee_simple',
                python_code=dedent("""
                    class Employee(HasTraits):
                        name = Str
                        salary = Int

                        def update_salary(self):
                            self.salary += int(0.2*self.salary)
                """),
                html_code=dedent("""
                    Employee name is {{employee.name}}
                    Salary is ${{employee.salary}}

                    <button ng-click='employee.update_salary()'>
                        Update salary
                    </button>
                """)
            ),

            Example(
                root='examples/app_manager/',
                ID='app_manager',
                python_code=dedent("""
                    class App(HasTraits):
                        name = Str
                        url = Str
                        icon_url = Str
                        status = Str('none')



                    class AppManager(HasTraits):

                        ### Dashboard protocol ###

                        def start_app(self, app):
                            # Start app
                            subprocess.Popen(app.command, ...)

                        ### AppStore protocol ###

                        connected = Bool(False)
                        available_apps = List(App)
                        installed_apps = List(App)

                        def connect(self):
                            # Some slow operation
                            time.sleep(4)

                            self.connected = True

                        def install_app(self, app):
                            # Fetch app from the store
                            FetchAction(app=app).execute()

                            # Install app

                        def remove_app(self, app):
                            # Remove app







                    class AppAction(HasTraits):
                        app = Instance(App)
                        progress = Int

                        def execute(self):
                            # implement this method in subclasses
                            pass

                    class FetchAction(AppAction):
                        ...

                    ...

                """),
                html_code=dedent("""
                    <!-- Dashboard view -->
                    <div ng-repeat='app in app_manager.installed_apps'>
                        <img ng-src='app.icon_url'/><br>

                        {{app.name}}

                        <button ng-click='app_manager.start_app(app)'>
                            Start
                        </button>
                        ...
                    </div>










                    <!-- AppStore view -->
                    <div ng-repeat='app in app_manager.available_apps'>
                        <img ng-src='app.icon_url'/><br>

                        {{app.name}}

                        <button ng-click='jigna.threaded(app_manager, "install_app", app)'>
                            Install
                        </button>

                        <div ng-show='app.status == "installing"'
                             ng-init='action = app_manager.actions[app.id]'>
                            Installing...

                            <!-- Progress bar -->
                            <div class='progress-bar-container'>
                                <div class='progress-bar' color='green'
                                     style='width: {{action.progress}}%'>
                                </div>
                            </div>
                        </div>
                        ...
                    </div>
                """)
            ),

            Example(
                root=self.root,
                ID='ipython_notebook',
                python_code=dedent("""
                    from jigna.utils.notebook import display_jigna

                    display_jigna(context={'person': person}, template=template)
                """),
                html_code=dedent("""
                    Name: {{person.name}}
                    Age: {{person.age}}
                """),
                command='ipython notebook examples_notebook.ipynb'
            ),
        ]

        return examples

    def get_example(self, ID):
        ''' Return the example with the given ID.'''

        example = None
        for example in self.examples:
            if example.ID == ID:
                return example

        return None

#### UI layer ####

template = Template(html_file='demo.html', recommended_size=(1400, 800))

#### Entry point ####

if __name__ == '__main__':
    examples_server = ExamplesServer(root=expanduser('~/work/jigna/examples'))

    app = WebApp(template=template, context={'server': examples_server}, port=8001)
    app.start()
