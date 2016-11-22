.. _internationalisation:

========================================
Internationalisation Support for Plugins
========================================

Giving your plugin internationalisation support is quite easy and 
straightforward.

Somewhere in your code (preferable at the beginning) you should create a class 
for all strings you need. You can use any attribute name freely inside this 
class except *name* and *description* as these attributes are used to set and 
translate the corresponding fields of your :class:`eg.PluginBase` and the 
:class:`eg.ActionBase` subclasses you might have. For every 
:class:`eg.ActionBase` you define, you can create a class inside your 'Text' 
class with the same name as the eg.ActionBase. Then set this class to the 
attribute *text* of the eg.PluginBase definition.

As an example look at this (quite useless) code::

    import eg
    
    class Text:
        text1 = "This is just a text"
        text2 = "This is just another text"
        class Message1:
            name = "Print first Message"
            description = (
                "This is a quite useless action that will print a message "
                "to the logger"
            )
            message = "This is just a message"
        class Message2:
            name = "Print second Message"
            description = (
                "This is another quite useless action that will print a "
                "message to the logger"
            )
            message = "This is another message"
    
    
    class MyPlugin(eg.PluginBase):
    
        text = Text # <- This is all you need to do
    
        def __init__(self):
            self.AddAction(Message1)
            self.AddAction(Message2)
            print self.text.text1
    
        def __close__(self):
            print self.text.text2
    
    
    class Message1(eg.ActionBase):
    
        def __call__(self):
            print self.text.message
    
    
    class Message2(eg.ActionBase):
    
        def __call__(self):
            print self.text.message

As you can see, inside your eg.PluginBase methods you can now access the 
strings through 'self.text'. Your action-classes will have a 'self.text' 
attribute of their own. The *name* and *description* fields of your actions 
have also been set up by EventGhost.

If you prefer, you can also use independent classes for the actions and assign 
them to the class-attribute *text* of the eg.ActionBase. This example will do 
the same as the above::

    import eg
    
    class PluginText:
        text1 = "This is just a text"
        text2 = "This is just another text"
    
    class MyPlugin(eg.PluginBase):
    
        text = PluginText # <- setting the 'text' attribute for the plugin
        
        def __init__(self):
            self.AddAction(Message1)
            self.AddAction(Message2)
            print self.text.text1
    
        def __close__(self):
            print self.text.text2
    
    # defining a 'text' class for the 'Message1' action.
    class Message1Text:
        message = "This is just a message"
    
    class Message1(eg.ActionBase):
        name = "Print first Message"
        description = (
            "This is a quite useless action that will print a message to "
            "the logger"
        )
        text = Message1Text # <- setting the 'text' attribute for the action
        
        def __call__(self):
            print self.text.message
    
    
    class Message2(eg.ActionBase):
        # You can also define directly a nested class if you name it 'text'.
        # If the action class has no attribute 'name' or 'description', 
        # EventGhost will look inside the 'text' class and use them if they 
        # are defined there. So you can piece together everything in the 
        # 'text' class.
        class text:
            name = "Print second Message" 
            description = (
                "This is another quite useless action that will print a "
                "message to the logger"
            )
            message = "This is another message"
    
        def __call__(self):
            print self.text.message

It is also important to note that your plugin should be able to get imported 
and the __init__() method should be able to be called under all circumstances. 
If a translator uses the translation editing tool of EventGhost, this tool 
will import every plugin and call the __init__() method of every plugin, to 
find out all actions the plugins have. So don't assume that the user might 
actually want to use your plugin and therefore assume some conditions can be 
presumed, like the existence of some DLL or registry key. Keep your __init__() 
fail-safe and add all your actions under all circumstances there. Your "hot 
code" should only be execute if the __start__() method gets called.
