===============
Writing Plugins
===============

Introduction
------------

Plugins in EventGhost serve mostly two functionalities:

1. They can extend the list of actions EventGhost can handle.
2. They can generate events that EventGhost can process, like remote 
   receiver plugins.

And they can do both at the same time.

To write plugins you mostly need to know two classes EventGhost defines:

1. `eg.PluginBase` - This is the base class of all plugins and 
   therefore the most essential.
2. `eg.ActionBase` - This is the base class of all actions a plugin 
   might want to export to EventGhost. 

You will need some basic knowledge of Python to understand this, but you don't 
need to be a Python expert. Many plugin developers have never used Python 
before and have learned most of the basics in an afternoon. You also don't 
need any additional programs, except an text editor that is appropriate to 
edit Python scripts.

This tutorial uses the latest beta version of EventGhost as the basis, so if 
you haven't already, update to the latest beta. 

Creating your first plugin
--------------------------

I will now try to show you the first steps needed to create a new plugin.

First you have to create a new folder under 
"C:\\Program Files\\EventGhost\\plugins" with a name you like. The name of the 
folder doesn't matter but should be unique and descriptive.

The next step is to create a __init__.py file in your plugin folder. This 
will be the starting point of your plugin code. The first line should call 
`eg.RegisterPlugin()`. Here is a typical start of a __init__.py::

    import eg
    
    eg.RegisterPlugin(
        name = "My New Plugin",
        guid = "{9D499A2C-72B6-40B0-8C8C-995831B10BB4}",
        author = "Me",
        version = "0.0.1",
        kind = "other",
        description = "This is an example plugin."
    )

You should first note that we use the :mod:`eg` module to access a function. 
This is the same :mod:`eg` that is described by the page about scripting in 
EventGhost.

The `eg.RegisterPlugin()` function understands many parameters. Actually 
every parameter can be omitted, but you should fill out the parameters as 
completely as you can.

*name*
    This is the name the user will see for your plugin. If omitted, EventGhost 
    will use the name of the folder where your __init__.py is. 

*guid*
    This GUID will help EG to identify your plugin so there are no name
    clashes with other plugins that accidentally might have the same name and
    will later ease the update of plugins.
    
*author*
    As you can guess, this parameter lets you define yourself as the author of 
    the plugin. Otherwise it will default to ``"<unknown author>"``. 

*version*
    Here you can define a version number for your plugin. Otherwise it will 
    default to ``"<unknown version>"``. 

*kind*
    This parameter defines where EventGhost will insert your plugin in the 
    :guilabel:`Add Plugin` dialog. Possible values are currently 
    ``"receiver"`` (for remote receiver plugins), ``"program"`` (for program 
    control plugins), ``"external"`` (for plugins handling external hardware 
    equipment) and ``"other"`` (if none of the other categories match). 
    This parameter defaults to ``"other"``. 

*description*
    This value can be a HTML string and therefore include formatting, table, 
    image and URL tags. This 'description' will be shown on the right side of 
    the :guilabel:`Add Plugin` dialog and also in the :guilabel:`Plugin Item Settings` dialog. 


.. note::

    Don't do anything else before the call to `eg.RegisterPlugin()`. 
    It must be the first thing in your file. Do all additional imports and 
    initializations after this statement. The reason is that EventGhost will 
    import each and every plugin when the user wants to add a plugin, because 
    EventGhost has to show a list of all plugins. But to speed this up, 
    EventGhost will interrupt the loading of the __init__.py, after it has 
    got the needed information through `eg.RegisterPlugin()`.

.. note::

    To create a GUID for your plugin, open the :guilabel:`Python Shell` under
    the :guilabel:`Help` menu. Then type:
    
       >>> import pythoncom
       >>> pythoncom.CreateGuid()
       
    You will get something like: `IID('{DA3F5444-F359-4FEC-AF59-876BB152CC29}')`
    You need the string value, so copy it and paste it to your plugin source
    file, so it looks like this:

        .. code:: python
        
            eg.RegisterPlugin(
                name = "My Plugin",
                ...
                guid = '{DA3F5444-F359-4FEC-AF59-876BB152CC29}',
                ...
            )
            
For the rest of this tutorial I will use the call to `eg.RegisterPlugin()`
without any parameters to save some space in the source.

Now we can start with the most minimal source code of a complete plugin::

    import eg
    
    eg.RegisterPlugin()
    
    class MyNewPlugin(eg.PluginBase):
        pass

That's it. This plugin will do nothing, but it will now show in the Add Plugin 
dialog and you can add it to your tree. 


Creating and adding actions
---------------------------

Now we want to add an action to our plugin. Let's create a typical 'Hello 
World!' example::

    import eg
    
    eg.RegisterPlugin()
    
    
    class MyNewPlugin(eg.PluginBase):
    
        def __init__(self):
            self.AddAction(HelloWorld)
    
    
    class HelloWorld(eg.ActionBase):
    
        def __call__(self):
            print "Hello World!"

You might have noticed that we have extended our plugin class with a 
__init__() method. Inside you find the single call to 
:meth:`self.AddAction() <eg.PluginBase.AddAction>`, that 
will insert the action we defined to the list of actions this plugin has.

An action is again created by subclassing, but this time from eg.ActionBase. 
Inside this class we have to define a __call__() method, that represents the 
workhorse of the action. So every time a particular action is executed by 
EventGhost, actually the __call__() method is called.

For our simple example we just do a print-statement here with the well known 
string.

Now you can try if this really works. Start EventGhost, add your plugin to 
the tree and fire up the :guilabel:`Add Action` dialog. There you will now 
find a new group named "My New Plugin" and a single action named "HelloWorld" 
inside it. After you have added this action to your tree, you can execute it 
and you will then see the message "Hello World!" appearing in the logger.

You may have noticed that the action is listed as "HelloWorld" because 
EventGhost has simply used the name of the class, but you might prefer to 
show it with a space between words as "Hello World". You might also want to 
show some description to the user. This is easy. Just modify the source code 
of the action class this way::

    class HelloWorld(eg.ActionBase):
        name = "Hello World"
        description = "You won't guess what this action does."
    
        def __call__(self):
            print "Hello World!"

In the 'description' field you can again use HTML.

Accessing the plugin from an action
-----------------------------------

Now I want to show you how actions can access members of the plugin. In the 
moment you call self.AddAction() in the plugin's __init__() code, your 
action class will be instantiated and will get some additional members 
set. One of the most important ones is 'self.plugin'. Imagine you want to 
have a simple plugin that holds a counter variable and you want to access 
this counter from two actions. The source code might look like this::

    import eg
    
    eg.RegisterPlugin()
    
    class MyNewPlugin(eg.PluginBase):
    
        def __init__(self):
            self.counter = 0
            self.AddAction(IncrementCounter)
            self.AddAction(DecrementCounter)
    
    
    class IncrementCounter(eg.ActionBase):
    
        def __call__(self):
            self.plugin.counter += 1
            print self.plugin.counter
    
    
    class DecrementCounter(eg.ActionBase):
    
        def __call__(self):
            self.plugin.counter -= 1
            print self.plugin.counter
    
The plugin now defines a 'self.counter' member variable. Both actions want to 
access this variable and modify it. They can simply do it through using the 
'self.plugin' reference to the plugin they were added to. 


Grouping of actions
-------------------

Some plugins have so many actions that they prefer to group the actions 
inside folders in the :guilabel:`Add Action` dialog. Take a look at the 'Media 
Player Classic' plugin for an example, even if you don't have or use this 
media player. Such grouping is easily done. You only have to learn one new 
method of a plugin called :meth:`AddGroup() <eg.PluginBase.AddGroup>`. I will 
show you a small example with only three actions and two groups::
    
    import eg
    
    eg.RegisterPlugin()
    
    class MyNewPlugin(eg.PluginBase):
    
        def __init__(self):
            self.AddAction(Action1)
            group1 = self.AddGroup(
                "My first group", 
                "My first group description"
            )
            group1.AddAction(Action2)
            group2 = self.AddGroup(
                "My second group", 
                "My second group description"
            )
            group2.AddAction(Action3)
 
        
    class Action1(eg.ActionBase):
    
        def __call__(self):
            print "Action1 called"
    
    
    class Action2(eg.ActionBase):
    
        def __call__(self):
            print "Action2 called"
    
    
    class Action3(eg.ActionBase):
    
        def __call__(self):
            print "Action3 called"

So this should be easy to understand. Instead of calling self.AddAction(), we 
use self.AddGroup() here to create a new group and remember the returned 
object. We then call AddAction() on this returned object to add our actions 
to this group. You can even call AddGroup() on the object returned from 
AddGroup() to get even deeper nested groups. 


Making a plugin configurable
----------------------------

Till now we only have overwritten the __init__() method of a plugin. But if 
your plugin wants to have configuration options, your plugin needs parameters 
and you need to know some more methods. We will start with the 
:meth:`~eg.PluginBase.Configure` method.

To make a nice configuration dialog in Python, you have to use wxPython 
functions. wxPython is a great GUI toolkit but it is quite big and complex. 
But don't be afraid. You don't need to know it with all odds and ends. Most 
times you can simply use some code from another plugin that has similar 
configuration elements as you intend. If you get stuck, feel free to ask 
in the `EventGhost forum </forum/viewforum.php?f=10>`_ to get some help. 
People who are familiar with wxPython can construct a nice dialog in minutes.

So let me show you a small demo again of a plugin with a configuration dialog. 
This one is really simple, as it only has a single string option.
::

    import eg
    
    eg.RegisterPlugin()
    
    class MyNewPlugin(eg.PluginBase):
    
        def Configure(self, myString=""):
            panel = eg.ConfigPanel()
            textControl = wx.TextCtrl(panel, -1, myString)
            panel.sizer.Add(textControl, 1, wx.EXPAND)
            while panel.Affirmed():
                panel.SetResult(textControl.GetValue())

If you add this plugin, you will see that the user gets a dialog box with a 
single text box inside. It doesn't look nice, but this doesn't matter now 
since I only want to demonstrate how things work.

Nearly all configuration dialogs follow the same scheme.

#. Define a :meth:`~eg.PluginBase.Configure` method, that has as 
   many parameters as you need. All parameters must be default parameters, 
   because if the plugin is added freshly, EventGhost can't know what and how 
   many parameters you want.
#. Then let EventGhost pre-build a panel through the creation of a
   :class:`eg.ConfigPanel` instance.
#. Now you create as many wxPython controls as you need and set their initial
   value with the parameters you got through the 
   :meth:`~eg.PluginBase.Configure` method. In this case we only have 
   *myString* and use it as value to a :class:`wx.TextCtrl`.
#. You now have to add these controls to the wx.Sizer of the panel with 
   panel.sizer.Add(). (Or you have to create a new wx.Sizer and add this sizer 
   to panel.sizer, but therefore you need more knowledge of wx.Sizers.)
#. Then you call panel.Affirmed() in a loop. This method of the panel will 
   finish the setup of the dialog and display it to the user. If the user 
   dismisses the dialog with the :guilabel:`Cancel` button, this method will 
   return False and you are done.
#. If panel.Affirmed() returns True, you have to return the current settings 
   the user has made through panel.SetResult(...). In this case we get the 
   current setting of the text box by using GetValue() on it. 

If you now type something into this text box and press :guilabel:`OK`, you 
will find that if you reconfigure the plugin this text is already set. It will 
even survive if you save your EventGhost configuration and restart EventGhost.

It is needed to use panel.Affirmed() and panel.SetResult(...) in a loop, 
because the user might also use the :guilabel:`Apply` button and EventGhost 
needs to know the current settings from the panel without dismissing it 
completely.

Before I can show you how to actually use this parameter you have to learn 
some more methods of a plugin:


Other important methods of a plugin
-----------------------------------

:meth:`__start__([, *args]) <eg.PluginBase.__start__>`

    This method will be called when your plugin gets enabled.
    
:meth:`__stop__() <eg.PluginBase.__stop__>`

    This method will be called when your plugin gets disabled.
    
:meth:`__close__() <eg.PluginBase.__close__>`

    This method gets called when your plugin gets unloaded.


Lets make a simple example where you can explore this::

    import eg
    
    eg.RegisterPlugin()
    
    print "MyNewPlugin module code gets loaded."
    
    
    class MyNewPlugin(eg.PluginBase):
    
        def __init__(self):
            print "MyNewPlugin is inited."
    
        def __start__(self, myString):
            print "MyNewPlugin is started with parameter: " + myString
    
        def __stop__(self):
            print "MyNewPlugin is stopped."
    
        def __close__(self):
            print "MyNewPlugin is closed."
    
        def Configure(self, myString=""):
            panel = eg.ConfigPanel()
            textControl = wx.TextCtrl(panel, -1, myString)
            panel.sizer.Add(textControl, 1, wx.EXPAND)
            while panel.Affirmed():
                panel.SetResult(textControl.GetValue())

If the user adds this plugin to its configuration the call order is as follows:

1. The plugin module code (__init__.py) gets loaded, similar to an import
2. The plugin gets instantiated and its __init__() method gets called. The 
   plugin should add all actions it wants to publish through calls to 
   AddAction() in its __init__() method.
3. If the plugin has any parameters that need to be set up, the Configure() 
   method is called and the user has to make the appropriate settings. As 
   soon as the user presses the :guilabel:`OK` button, EventGhost will receive 
   the parameters and store them.
4. Now the :meth:`~eg.PluginBase.__start__` method is called 
   and the plugin will receive the stored parameters. So it will receive the 
   same parameters that Configure() has returned.
5. If EventGhost is about to quit or the plugin gets deleted by the user, the 
   :meth:`~eg.PluginBase.__stop__` method is called and then the 
   :meth:`~eg.PluginBase.__close__` method immediately after that. 

If the user now disables your running plugin in the tree, your 
:meth:`~eg.PluginBase.__stop__` method gets called. If he re-enables the 
plugin, the :meth:`~eg.PluginBase.__start__` method is called again.

If the plugin is already stored in the configuration of the user and 
EventGhost will load this configuration, the same will happen with the only 
difference that the Configure() method is not called again, as EventGhost 
already knows the parameters it should supply to the 
:meth:`~eg.PluginBase.__start__` method. If the configuration was saved with 
your plugin in disabled state, your plugin will not get a 
:meth:`~eg.PluginBase.__start__` call.

So the :meth:`~eg.PluginBase.__start__` and :meth:`~eg.PluginBase.__stop__` 
methods are always called in a pair. If the plugins 
:meth:`~eg.PluginBase.__start__` method was called, the plugin 
can be sure its :meth:`~eg.PluginBase.__stop__` method will also 
be called at some time.

If the user wants to change some parameters of the plugin, the following will 
happen:

1. Configure() is called (with the old parameters).
2. If the user presses the :guilabel:`Cancel` button inside the configuration 
   dialog, nothing more will happen.
3. If the user presses the :guilabel:`OK` button the Configure() method has to 
   return the new parameters. If the plugin is enabled already, the plugin's 
   :meth:`~eg.PluginBase.__stop__` method will be called and 
   immediately after that the :meth:`~eg.PluginBase.__start__` 
   method with the new parameters. 

So what is important to know is that the plugin will get its parameters 
through the :meth:`~eg.PluginBase.__start__` method and not, as 
you might have expected, through the __init__() method.


Making actions configurable
---------------------------

To make actions configurable you basically do the same as for the plugin 
configuration. Again you have to define a Configure() method, but this time 
for the eg.ActionBase. Instead of a special method like :meth:`~eg.PluginBase.__start__`, an 
action will receive the parameters directly through the __call__() method.
::

    import eg
    
    eg.RegisterPlugin()
    
    class MyNewPlugin(eg.PluginBase):
    
        def __init__(self):
            self.AddAction(PrintString)
    
    
    class PrintString(eg.ActionBase):
    
        def __call__(self, myString):
            print myString
            
        def Configure(self, myString=""):
            panel = eg.ConfigPanel()
            textControl = wx.TextCtrl(panel, -1, myString)
            panel.sizer.Add(textControl, 1, wx.EXPAND)
            while panel.Affirmed():
                panel.SetResult(textControl.GetValue())

As you can see, the Configure() method is absolutely identical to the one we 
used above for the plugin. 
  
Generating events
-----------------

As said in the introduction, one purpose of some plugins is to generate 
events. EventGhost's architecture has special support for "enduring" events. 
Imagine you press and hold a button on your remote, EventGhost might 
have to do some actions dependent on the duration of the press, like 
AutoRepeat. Therefore you have to generate an enduring event and end this 
event later if the button is released.

Other plugins only generate "short-term" events that indicate a change on 
something, but don't have a duration.

Short-term events
^^^^^^^^^^^^^^^^^

The last mentioned type of events is simply generated. You just have to call 
the plugin's method :meth:`self.TriggerEvent() <eg.PluginBase.TriggerEvent>` 
with an appropriate event string.

Typically, a plugin that is generating events has to monitor some state and 
then fires the event if some condition is met. Therefore in most cases it has 
to create a thread that runs independent from EventGhost's processing. Here I 
will show you the source of a simple plugin that fires an event every 10 
seconds to EventGhost::

    import eg
    
    eg.RegisterPlugin()
    
    from threading import Event, Thread
    
    class MyPlugin(eg.PluginBase):
    
        def __start__(self):
            self.stopThreadEvent = Event()
            thread = Thread(
                target=self.ThreadLoop, 
                args=(self.stopThreadEvent, )
            )
            thread.start()
            
        def __stop__(self):
            self.stopThreadEvent.set()
            
        def ThreadLoop(self, stopThreadEvent):
            while not stopThreadEvent.isSet():
                self.TriggerEvent("MyTimerEvent")
                stopThreadEvent.wait(10.0)

One important thing you should notice, is the starting of the thread in the 
:meth:`~eg.PluginBase.__start__` method of the plugin and stopping it in the 
:meth:`~eg.PluginBase.__stop__` method. A plugin should only generate events 
if its :meth:`~eg.PluginBase.__start__` method was called, so it will not 
generate events if the plugin was disabled by the user. Please follow this 
convention, to only generate events after :meth:`~eg.PluginBase.__start__` is 
called and stop event generation if :meth:`~eg.PluginBase.__stop__` is called.


Enduring events
^^^^^^^^^^^^^^^

[more to come...]


Further reading
---------------

You should now have the basic knowledge to understand some already written 
plugins. A recommended start is the source code of the Winamp plugin, as it 
has some comments and is relative simple. The next one could be the 
Foobar2000 plugin, as it shows how to create many similar actions from a list 
of data. This technique is even more used in the "Media Player Classic" 
plugin. Then you should take a look at the definition of 
:class:`eg.PluginBase` and :class:`eg.ActionBase` in the 
`EventGhost API Documentation <eg/index.html>`_. There you can see which 
members of the classes are defined, so you won't accidentally overwrite them 
in your own plugin. 
