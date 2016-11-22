:tocdepth: 2

=====================
Scripting with Python
=====================

Introduction
============

If you want to script with Python in EventGhost you first have to understand 
the difference between the environment of a 'PythonScript' and a 
'PythonCommand' action in EventGhost. 

PythonCommand
-------------

PythonCommands execute a single-line Python statement or expression. All 
PythonCommands share a single global namespace, so you can create a global 
variable with one PythonCommand and directly modify this variable with another 
PythonCommand later. The global namespace includes all Python built-in objects 
and the special object :mod:`eg`, that we will explain later.


PythonScript
------------

Every PythonScript in EventGhost has its own global namespace. The global 
namespace includes all Python built-in objects and the special object :mod:`eg`.


The one and all 'eg' object
===========================

Everything special that is needed from EventGhost for scripting and writing 
plugins is stuffed into the :mod:`eg` object. It includes many functions, 
variables, classes and objects. You could actually say :mod:`eg` is EventGhost 
itself.

So we will explain some of the members of :mod:`eg` here in more detail: 

Useful members
--------------

eg.globals
~~~~~~~~~~

As explained before, PythonCommands all share a single global namespace. This 
is actually eg.globals. Since every PythonScript has its own global namespace, 
you can't directly access a value defined with a PythonCommand from a 
PythonScript and vice versa, but you can access it through eg.globals.

If you made, for example, a PythonCommand like 'myVar = 123', you can later 
write in a PythonScript::

    print eg.globals.myVar

and you will get the value '123' printed to the logger. You can of course also 
create new named variables in this namespace from a PythonScript by simply 
writing::

    eg.globals.myOtherVar = "Hello World!"

and after that use the PythonCommand 'print myOtherVar' to get the value.

So eg.globals is the bridge between values defined with PythonCommands and 
values defined with PythonScripts and can also be used to transfer data 
between different PythonScripts. 


eg.plugins
~~~~~~~~~~

One neat feature of EventGhost is the ability to also use nearly every action 
of a plugin in a PythonScript. Every plugin creates a named member in 
eg.plugins, when it is loaded. And every action is a named member of a plugin. 
To find out the name of the action (and its plugin) you can simply create an 
action in EventGhost's tree, copy this action-item and paste it to a text 
editor like Notepad (or even EventGhost's built-in PythonScript editor). As an 
example, you will see something like this for 'System/Turn Mute Off'::

    <?xml version="1.0" encoding="UTF-8" ?>
    <EventGhost Version="532">
        <Action>
            System.MuteOff()
        </Action>
    </EventGhost>

If you look at the line between the <Action> tags, you will see the plugin is 
named 'System' and the action is named 'MuteOff'. Now you can write in a 
PythonScript::

    eg.plugins.System.MuteOff()

and it will exactly do the same as a 'System/Turn Mute Off' action.

Actions might also have parameters, so you will find that a 'Window/Resize' 
action, that should resize a window to 200 pixels width and 300 pixels height 
would be called from a PythonScript as::

    eg.plugins.Window.Resize(200, 300)

by simply configuring the action before you copy it and looking at the copied 
XML chunk in an editor. 


eg.event
~~~~~~~~

eg.event represents the event that is currently processed. Since your PythonScript or PythonCommand is most likely triggered by an event when it is executing, eg.event will give you information about this event. Most useful members of this object are:

eg.event.string
    This is the full qualified event string as you see it inside the logger, with the exception that if the eg.event.payload field (that is explained below) is not None the logger will also show it behind the event string, but this is not a part of the event string we are talking about here. 

eg.event.payload
    A plugin might publish additional data related to this event. Through eg.event.payload you can access this data. For example the 'Network Event Receiver' plugin returns also the IP of the client that has generated the event. If there is no data, this field is None. 

eg.event.prefix
    This is the first part of the event string till the first dot. This normally identifies the source of the event as a short string. 

eg.event.suffix
    This is the part of the event string behind the first dot. So you could say:
     
    eg.event.string = eg.event.prefix + '.' + eg.event.suffix 

eg.event.time
    The time the event was generated as a floating point number in seconds (as returned by the clock() function of Python's time module). Since most events are processed very quickly, this is most likely nearly the current time. But in some situations it might be more clever to use this time, instead of the current time, since even small differences might matter (for example if you want to determine a double-press). 

eg.event.source
    This is the object that has generated the event. For most events, the source is a plugin-object but for some built-in events and events generated through eg.TriggerEvent(), this will be our beloved :mod:`eg` object. 

eg.event.isEnded
    This boolean value indicates if the event is an enduring event and is still active. Some plugins (e.g. most of the remote receiver plugins) indicate if a button is pressed longer. As long as the button is pressed, this flag is 'False' and in the moment the user releases the button the flag turns to 'True'. So you can poll this flag to see if the button is still pressed. 

    
eg.result
~~~~~~~~~

Every action in EventGhost returns a result. For most actions this is simply 
Python's None, but some might return a result that is useful for later 
evaluation. For example, the 'Window/Find Window' action returns a list of the 
window-handles it has found (or an empty list if it hasn't found anything). So 
you can place a PythonScript directly after the 'Find Window' action and do 
something with this list.

The 'EventGhost/Jump' action also uses eg.result as the condition to decide 
what it has to do. If eg.result is determined as True by Python's standard 
truth testing procedure, the 'Jump' action will regard the result of the last
action as 'successful' and do a jump if configured so. So you can use this 
circumstance to control a 'Jump' from a PythonCommand or PythonScript, by 
assigning something to eg.result. For a PythonCommand you actually don't 
need to assign directly to eg.result, because the result of a Python 
evaluation is automatically assigned to eg.result. If you make a 
PythonCommand like 'myVar == 1', EventGhost will compute this to True if 
'myVar' is 1 or to False if 'myVar' is anything other and assign this 
True/False result to eg.result. 


Useful functions 
----------------

.. function:: eg.TriggerEvent(eventstring) 

To generate a new event in a PythonScript, you can use this function. Example 
usage::

    eg.TriggerEvent("MyEvent")

This will generate a "Main.MyEvent" event. Actually you could also use the 
'EventGhost/TriggerEvent' action with 
eg.plugins.EventGhost.TriggerEvent("MyEvent"), following the pattern described 
above, but for convenience this function is also exposed directly from :mod:`eg`. 


.. function:: eg.Exit()

Sometimes you want to quickly exit a PythonScript, because you don't want to 
build deeply nested if-structures for example. eg.Exit() will exit your 
PythonScript immediately.


.. function:: eg.StopMacro()

Instructs EventGhost to stop executing the current macro after the current 
action (thus the PythonScript or PythonCommand) has finished. 
