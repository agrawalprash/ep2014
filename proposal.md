# Jigna: a seamless Python-JS bridge to create rich HTML UIs for Python apps

## Abstract 

Jigna aims to provide an HTML based solution for creating beautiful user 
interfaces for Python applications, as opposed to widget based toolkits like 
Qt/wx or native toolkits. It provides a seamless two-way data binding between 
the Python model and the HTML view by creating a Python-JS communication bridge. 
This ensures that the view is always live as it can automatically update itself 
when the model changes, and update the model when user actions take place on the 
UI. The Jigna view can be rendered in an in-process Qt widget or over the web in 
a browser.

## Description

Let us say we have a nice model written in Python (specifically, in [Traits][1]):

    from traits.api import HasTraits, Str, on_trait_change
    
    class Model(HasTraits):
        name = Str
        greeting = Str
    
        @on_trait_change('name')
        def update_greeting(self):
            self.greeting = "Hello " + self.name

        def clear(self):
            self.name = ""
    
    model = Model(name='Fred')

We would like to write simple HTML to visualize this and have the model and view 
be fully connected. Here is a sample HTML (an [AngularJS][2] template):

    body_html = """
        Name: <input ng-model="model.name"> <br>
        Greeting:
        <h1>{{model.greeting}}</h1> <br>

        <button ng-click="model.clear()">Clear</button>
    """

Notice how the HTML is directly referencing Python model attributes via 
`model.name` and `model.greeting`, and calling its method via `model.clear()`. 
Jigna binds this declarative view to the model and lets you create a Qt based UI:

    from jigna.api import View
    view = View(body_html=body_html)
    
    from PySide import QtGui
    app = QtGui.QApplication([])
    view.show(model=model)
    app.exec_()

This produces an HTML UI which responds automatically to any changes in the 
model and vice-versa. It can optionally be styled with CSS and made interactive 
with Javascript. Clearly the above example is a toy example, but this shows a 
nice way of easily building rich, live user interfaces for Python apps. 

This is nice for several reasons:

* The view code is declarative and hence easy to read.
* The binding between the model and the view is automatic.
* HTML/CSS/JS today is very powerful 
    * there are many JS libraries for a variety of tasks.
    * it is much easier to find people who know HTML/CSS/JS than Qt or a native 
    toolkit.
    * your development team doesn't have to worry about creating widgets or the 
    limitations in the toolkit's widget set as there are thousands of developers 
    worldwide creating awesome CSS/JS widgets for you.
* There is a complete separation of view from the model and this allows us to 
hand off the entire UI to an HTML/CSS/JS guru.

And if this were not enough, the view can also be easily served on a web browser 
if we just did the following:

    view.serve(model=model)

This starts up a web server to which one can connect multiple browsers to see 
and interact with the model.

### How is this different from existing options?

For a simple Python desktop application, it is relatively easy to create an HTML 
view using a webkit browser widget.  However, the connection between the model 
and the HTML UI can be tricky resulting in fairly complicated code.  Most web 
frameworks provide this functionality but are web-centric, and are centered 
around building web applications, not desktop applications. One of the 
implications of this is that the template is usually static and does not respond 
to changes on the server side immediately.

Our goal is to be able to build a desktop UI completely in HTML where the HTML 
template always remains live by referring directly to Python object attributes 
and methods. Changes in the Python side should update the UI and user inputs on 
the UI should be able to update the model.

### How it works

It turns out that Qt's [QtWebkit][3] browser has support for in-process 
communication between its Javascript engine and the running Python application. 
We use this communication channel to create a Javascript proxy for Python 
models.

The other nice piece in this story is [AngularJS][2], which provides good model 
view separation between its HTML template and the corresponding Javascript model. 
AngularJS has great support for two-way data binding between the template and 
the model, which keeps the template expressions always in sync with the JS 
model. This makes sure that the HTML you need to write is terse and simple.

We combine these two pieces to create a lightweight lazy-loaded Python-JS bridge 
which provides us the two-way data binding we needed between the Python model 
and the HTML view. We use Traits to write models in Python. Traits lets us define 
attributes of an object statically, and supports notifications when the 
attributes change. Jigna integrates well with traits so that these notifications
automatically update the UI. Similarly, user inputs on the UI change model 
attributes, call public methods on the model as well.

Note however that you don’t need traits to use Jigna as you can bind it to your 
plain old Python objects too - you would just need to add your own events *if* 
you want your models to be updated outside of the UI.

### More about the presentation

In the presentation, I will talk about the basic philosophy of Jigna and then 
move on to show some interesting demos. The demos will mostly include the 
following:

* Simple data binding between HTML and traits model
* A dummy app store UI created using Jigna - It demonstrates multiple 
capabilities of Jigna like: templating lists and objects, calling methods on the 
model, catching events fired on the Python side over in JS side etc.
* Embedding Qt widgets inside Jigna HTML - we embed [Chaco][4] and [Mayavi][5] 
widgets (Chaco and Mayavi are 2D and 3D visualization libraries respectively) 
which update live as we move HTML sliders.
* A demo of the web version of Jigna, in which you can view the HTML UI on a web 
browser and execute public methods of the model remotely.
* WebGL backend working with Jigna (embedding Mayavi in the web version via 
webgl)
* Embedding Jigna in an [IPython notebook][6] to have interactive plots in 
IPython notebooks.

[1]: http://code.enthought.com/projects/traits/ "Traits"
[2]: http://angularjs.org/ "AngularJS"
[3]: http://qt-project.org/wiki/QtWebKit "QtWebkit"
[4]: http://code.enthought.com/chaco/ "Chaco"
[5]: http://code.enthought.com/projects/mayavi/ "Mayavi"
[6]: http://ipython.org/notebook.html "IPython notebook"
