Command line reference
======================

The EventGhost main executable accepts the following command line arguments: 

.. cmdoption:: -event <eventname> [<payload> ...]

    Issues the event <eventname> in the currently running EventGhost instance. 


.. cmdoption:: -e <eventname> [<payload> ...]

    Same function as the *-event* option.


.. cmdoption:: -hide

    Starts EventGhost hidden in the system tray. 


.. cmdoption:: -h

    Same function as the *-hide* option.


.. cmdoption:: -f <filename>, -file <filename>

    Opens the XML file <filename> on start-up (instead of the last loaded 
    file). 


.. cmdoption:: -n <host>:<port> <password> <eventname> [<payload> ...]

    This one is similar to the *-event* option, but sends the event <eventname> 
    through TCP/IP like the 'Network Event Sender' plugin does. It will not 
    start EventGhost, so it can be used as a little helper tool for other 
    applications or .BAT files to send events to a remote machine. <host> has 
    to be the IP or host name of the target machine. <port> and <password> 
    are the options that you have configured on the target machine's 'Network 
    Event Receiver' plugin. 


.. cmdoption:: -translate

    Starts EventGhost's language editor. 
    

.. cmdoption:: -configdir <directory>

    Instructs EventGhost to use the directory <directory> to store and
    retrieve its settings. Without this option EventGhost uses a directory in
    the application data folder of your machine for storing its settings.
    Through this option you can change the folder to a location on an USB
    stick for example, to make EventGhost portable.


