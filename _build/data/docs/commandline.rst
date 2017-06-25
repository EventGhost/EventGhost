Command Line Options
====================

The EventGhost main executable accepts the following command line arguments: 


.. cmdoption:: -configdir <directory>

    Instructs EventGhost to use the directory <directory> to store and
    retrieve its settings. Without this option EventGhost uses a directory in
    the application data folder of your machine for storing its settings.
    For example, through this option you can change the folder to a location
    on a USB stick to allow EventGhost to be used in a portable manner.


.. cmdoption:: -debug

    Start EventGhost in verbose mode and log to a file located in the
    %AppData%\\EventGhost folder.


.. cmdoption:: -d

    Shorter alias for the :option:`-debug` option.


.. cmdoption:: -event <eventname> [<payload> ...]

    Issues the event <eventname> in the currently running EventGhost instance.
    Optionally you can specify one or more <payload> strings, that will be
    added to the event in the
    :data:`eg.event.payload <eg.EventGhostEvent.payload>` field.


.. cmdoption:: -e <eventname> [<payload> ...]

    Shorter alias for the :option:`-event` option.


.. cmdoption:: -file <filename>

    Opens the configuration file <filename>. The :option:`-file` is not
    required, EventGhost will open any file with the .egtree or .xml extension
    passed as a command line argument.


.. cmdoption:: -f <filename>

    Shorter alias for the :option:`-file` option.


.. cmdoption:: -hide

    Starts EventGhost hidden in the system tray or minimized, depending on your
    setting in
    :menuselection:`File --> Options --> Display EventGhost icon in system tray`.
    Otherwise it would start in the state it had when it was closed.


.. cmdoption:: -h

    Shorter alias for the :option:`-hide` option.


.. cmdoption:: -multiload

    Allow multiple sessions of EventGhost on the same computer.


.. cmdoption:: -m

    Shorter alias for the :option:`-multiload` option.


.. cmdoption:: -netsend <host>:<port> <password> <eventname> [<payload> ...]

    This one is similar to the :option:`-event` option, but sends the event
    <eventname> through TCP/IP like the 'Network Event Sender' plugin does. It
    will not start EventGhost, so it can be used as a little helper tool for
    other applications or .BAT files to send events to a remote machine.
    <host> has to be the IP or host name of the target machine. <port> and
    <password> are the options that you have configured on the target
    machine's 'Network Event Receiver' plugin.


.. cmdoption:: -n <host>:<port> <password> <eventname> [<payload> ...]

    Shorter alias for the :option:`-netsend` option.


.. cmdoption:: -plugin <egplugin>

    Opens the plugin archive file <egplugin> for installation in EventGhost.
    Plugins installed through a <egplugin> plugin archive file are stored in the
    %AppData%\\EventGhost\\plugins folder and take precedence over plugins in the
    %ProgramFiles%\\EventGhost\\plugins folder. The :option:`-plugin` is not
    required, EventGhost will open any file with the .egplugin extension passed
    as a command line argument.


.. cmdoption:: -p <egplugin>

    Shorter alias for the :option:`-plugin` option.


.. cmdoption:: -plugindir <directory>

    Instructs EventGhost to use the directory <directory> to load additional
    plugins.


.. cmdoption:: -restart

    Restart EventGhost.

    .. note::

        If you started EventGhost with full elevation you must also run
        this commands with full elevation.


.. cmdoption:: -translate

    Starts EventGhost's translation editor.
