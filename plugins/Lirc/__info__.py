name = "LIRC Event Receiver"
kind = "remote"
version = "0.6.0"
author = "jinxdone"
description = """
Plugin for receiving Lirc eventstrings and generating EventGhost events accordingly.

<br>
<br>
The configurable options are:
<UL>
<LI><i>Target Host</i><br>
The target host and port of the lirc server. For WinLirc running on localhost the default settings should be fine (127.0.0.1:8765)
<br>
<LI><i>Only use the first event</i><br>
Only one event per keypress is generated, all subsequent events will be discarded.
<LI><i>Add remote-name</i><br>
Adds the remote-name into the eventstring, use it if you want to distinguish between multiple remotes.
<LI><i>Add repeat-tag</i><br>
Adds "++" into the eventstring when the event in question is a repeating event.
<br>
<LI><i>Ignoretime after first event</i><br>
You can specify a time during which after a first event any repeat-events are discarded. The value is in milliseconds, set to 0 to disable.
 (Useful if you have problems with buttons you want only to "tap" and not have multiple events by accident)
<br>
<LI><i>Timeout for enduring events</i><br>
Sets the timeout value for enduring events. If you increase it it will work more reliably, but it adds 'lag' to the end of each event, if you set it too low your events may sometimes be interrupted abrubtly.
 (default = 200, recommended between 150-400, depending on your setup)
</UL>
"""