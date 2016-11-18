========
Features
========

Other common things that can act as a trigger for an event are:

* key presses (hotkeys)
* joysticks/gamepads
* a program is starting or is switched to by the user
* another program like EventGhost (on another PC), Girder or NetRemote is 
  sending an event through TCP/IP
* a special HTTP request is made to the internal web server
* another program is sending an event through ActiveX 

and everything some code can catch, as events can also be generated through 
plugins.

EventGhost gives the user a GUI to configure macros that do all kind of things 
like:

* launching applications
* emulating keystrokes
* emulating mouse movements and clicks
* control the sound card
* move, resize, etc. windows on the desktop
* execute Python scripts (Python interpreter and editor is built-in)
* transmit IR-codes to external consumer equipment, if you have a supported 
  IR-transceiver.
* control external hardware devices like projectors and other media equipment 
  through RS232 communication
* extensive control of programs that have special communication interfaces, 
  such as some media players 

and everything some code can do, as these list of actions can also be extended 
through plugins.

You can take a look at the list of plugins to find out what has been 
implemented also.

The plugin system is the most integral part of the program. Actually EventGhost
is designed around the plugin idea from the beginning. Every action 
EventGhost does and every event it sees is implemented through a plugin, even 
the most basic ones. So every plugin has rights equal to the built-in 
functions, because they are actually the same. The user can configure and use 
them through a consistent and, hopefully, easy to learn interface.

EventGhost is written mostly in Python with some low-level parts in C. 
Plugins can be written in any language that can produce DLLs, such as C, C++, 
Delphi and Visual Basic. But of course they can be (and mostly are) written in 
Python. 
