Command Line Options
====================

The EventGhost main executable accepts the following command line arguments: 

.. cmdoption:: -event <eventname> [<payload> ...]

    Issues the event <eventname> in the currently running EventGhost instance. 
    Optionally you can specify one or more <payload> strings, that will be 
    added to the event in the 
    :data:`eg.event.payload <eg.EventGhostEvent.payload>` field.

.. cmdoption:: -e <eventname> [<payload> ...]

    Shorter alias for the :option:`-event` option.


.. cmdoption:: -hide

    Starts EventGhost hidden in the system tray. Otherwise it would start in
    the state it had as it was closed.


.. cmdoption:: -h

    Shorter alias for the :option:`-hide` option.


.. cmdoption:: -file <filename>

    Opens the XML configuration file <filename> on start-up (instead of the 
    last loaded file). 


.. cmdoption:: -f <filename>

    Shorter alias for the :option:`-file` option.


.. cmdoption:: -n <host>:<port> <password> <eventname> [<payload> ...]

    This one is similar to the *-event* option, but sends the event <eventname> 
    through TCP/IP like the 'Network Event Sender' plugin does. It will not 
    start EventGhost, so it can be used as a little helper tool for other 
    applications or .BAT files to send events to a remote machine. <host> has 
    to be the IP or host name of the target machine. <port> and <password> 
    are the options that you have configured on the target machine's 'Network 
    Event Receiver' plugin. 


.. cmdoption:: -translate

    Starts EventGhost's translation editor. 
    

.. cmdoption:: -configdir <directory>

    Instructs EventGhost to use the directory <directory> to store and
    retrieve its settings. Without this option EventGhost uses a directory in
    the application data folder of your machine for storing its settings.
    Through this option you can change the folder to a location on an USB
    stick for example, to make EventGhost portable.


