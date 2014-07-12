#### Imports ####
import time
import os
import math
import shutil
from os.path import join, getsize, dirname, exists, isfile
from traits.api import HasTraits, Str, Bool, Int, List, Instance, Dict, Property
from jigna.api import Template, QtApp

#### Exceptions ####

class AppNotInstalledException(Exception):
    pass

class AppNotAvailableException(Exception):
    pass

#### App ####

class App(HasTraits):

    name = Str
    version = Str
    id = Str
    author = Str

    status = Str('none')

    url = Property(Str, depends_on='id')
    def _get_url(self):
        return join(self.id, 'main.py')

#### App Actions ####

class AppAction(HasTraits):

    app = Instance(App)

    store_url = Str

    local_url = Str

    progress = Int

    def execute(self):
        raise NotImplementedError

class FetchAction(AppAction):

    def execute(self):
        self.app.status = 'fetching'
        app_filename = join(self.store_url, self.app.url)

        filesize = getsize(app_filename)
        chunk_size = int(math.ceil(filesize/100.0))

        with open(app_filename, 'r') as fr:
            while True:
                data = fr.read(chunk_size)
                if not data:
                    break
                else:
                    local_filename = join(self.local_url, self.app.url)
                    if not exists(dirname(local_filename)):
                        os.makedirs(dirname(local_filename))
                    with open(local_filename, 'a') as fw:
                        fw.write(data)
                    time.sleep(0.1)
                    self.progress += int(float(chunk_size) / filesize * 100)
                    print "written", getsize(local_filename), "bytes"
        self.app.status = 'fetched'

class InstallAction(AppAction):

    def execute(self):
        self.app.status = 'installing'
        self.app.installed = True
        time.sleep(2)
        self.app.status = 'installed'

class RemoveAction(AppAction):

    def execute(self):
        self.app.status = 'removing'
        time.sleep(2)
        shutil.rmtree(join(self.local_url, self.app.id))
        self.app.status = 'none'

class StartAction(AppAction):

    def execute(self):
        if not self.installed:
            raise AppNotInstalledException("The app %s does not exist" % self.id)

        print 'Starting app', self.app.name

#### App Manager ####

class AppManager(HasTraits):

    connected = Bool(False)

    STORE_URL = Str

    LOCAL_URL = Str

    available_apps = List(App)

    installed_apps = List(App)

    actions = Dict(Str, AppAction)

    def connect(self):
        if self.connected:
            print "Connected already"
            return

        print "Trying to connect to the remote store..."
        time.sleep(4)
        if exists(self.STORE_URL):
            self.connected = True
            for f in os.listdir(self.STORE_URL):
                if not isfile(f):
                    app = App(id=f, name=self._prettify(f), author='Enthought')
                    self.available_apps.append(app)
            print "Connected"

        else:
            print "Failed"

    def install_app(self, app):
        # fetch
        self._perform_action(FetchAction(
            app=app, store_url=self.STORE_URL, local_url=self.LOCAL_URL
        ))

        # install
        self._perform_action(InstallAction(
            app=app, store_url=self.STORE_URL, local_url=self.LOCAL_URL
        ))

        self.installed_apps.append(app)

    def remove_app(self, app):
        self._perform_action(RemoveAction(
            app=app, store_url=self.STORE_URL, local_url=self.LOCAL_URL
        ))

        self.installed_apps.remove(app)

    def start_app(self, app):
        self._perform_action(StartAction(
            app=app, store_url=self.STORE_URL, local_url=self.LOCAL_URL
        ))

    #### Private protocol #####################################################

    def _perform_action(self, action):
        self.actions[action.app.id] = action
        action.execute()

    def _prettify(self, str):
        str = str.replace("_", " ")
        return str.capitalize()

def main():
    app_manager = AppManager(STORE_URL='store', LOCAL_URL='local')
    template = Template(html_file=join('gui', 'app_manager.html'), base_url='gui')

    app = QtApp(template=template, context={'app_manager': app_manager})
    app.start()

if __name__ == '__main__':
    main()


