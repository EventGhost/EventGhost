Command Line Options
====================

Usage:
    eventghost [.egtree/.egplugin file]
               [-?, /?, -help, --help] [-h, /h, -hide, --hide]
               [-i, /i, -install, --install] [-u, /u, -uninstall, --uninstall]
               [-m, /m, -multiload, --multiload] [-t, /t, -translate, --translate]
               [-r, /r, -restart, --restart]
               [-n, /n, -netsend, --netsend <host>:<port> <password> <eventname> [<payload>]]
               [-d, /d, -debug, --debug <modules>]
               [-e, /e, -event, --event <event> [<payload>]
               [-c, /c, -configdir, --configdir <config path>]
               [-f, /f, -file, --file <.egtree file>]
               [-p, /p, -pluginFile, --pluginfile <.egplugin file>]

The EventGhost main executable accepts the following command line arguments:

.. cmdoption:: .egtree/.egplugin file
    Will load a save file or install a plugin
    eventghost Saved_Data.egtree

.. cmdoption:: -?, /?, -help, --help
    Show this help message and exit.

.. cmdoption:: -h, /h, -hide, --hide
    Start EventGhost minimized.

.. cmdoption:: -i, /i, -install, --install
    Compile all EventGhost files.

.. cmdoption:: -u, /u, -uninstall, --uninstall
    Remove all .pyc (python compiled) files.

.. cmdoption:: -m, /m, -multiload, --multiload
    Open multiple instances of EventGhost.

.. cmdoption:: -t, /t, -translate, --translate
    Starts EventGhost's translation editor.

.. cmdoption:: -r, /r, -restart, --restart
    Restart EventGhost.

.. cmdoption:: -d, /d, -debug, --debug <module names>
    Enable debugging. Optionally you can specify module names to enable verbose
    debugging. If the module supports verbose debugging.

    To enable verbose debugging globally.
    --debug eg

    Enable debugging for all core plugins.
    --debug eg.CorePluginModule

    Enable debugging for a specific core plugin.
    --debug eg.CorePluginModule.EventGhost

    Enable debugging for a specific module in a core plugin.
    --debug eg.CorePluginModule.Window.SendKeys

    You can also specify more then one module to set to verbose debugging just
    put a space between them. Because this feature uses a "Bottom Up" means to
    set the verbose debugging.

    Doing the following is pointless.
    --debug eg.CorePluginModule eg

    This is because eg is the bottom most module and everything on top of it
    also has verbose debugging set.

.. cmdoption:: -e, /e, -event, --event <eventname> [<payload>]
    Trigger an event with optional payload.

    Issues the event <eventname> in the currently running EventGhost instance.
    Optionally you can specify one or more <payload> strings, that will be
    added to the event in the :data:`eg.event.payload <eg.EventGhostEvent.payload>`
    field.

.. cmdoption:: -n, /n, -netsend, --netsend <host>:<port> <password> <eventname> [<payload>]
    Send an event and an optional payload to another computer running
    EventGhost.

    This one is similar to the :option:`-event` option, but sends the event
    <eventname> through TCP/IP like the 'Network Event Sender' plugin does. It
    will not start EventGhost, so it can be used as a little helper tool for
    other applications or .BAT files to send events to a remote machine.
    <host> has to be the IP or host name of the target machine. <port> and
    <password> are the options that you have configured on the target
    machine's 'Network Event Receiver' plugin.

.. cmdoption:: -c, /c, -configdir, --configdir <directory>
    Specify what config file to use.

    Instructs EventGhost to use the directory <directory> to store and
    retrieve its settings. Without this option EventGhost uses a directory in
    the application data folder of your machine for storing its settings.
    For example, through this option you can change the folder to a location
    on a USB stick to make EventGhost portable.

.. cmdoption:: -p, /p, -pluginfile, --pluginfile <.egplugin file>
    Install a plugin.

.. cmdoption:: -f, /f, -file, --file  <.egtree file>
    Specify save file to load.

** Now don't forget if you want an optional argument that has spaces in it
to be treated as a single statement, you will need to wrap the statement in
"double quotes"
