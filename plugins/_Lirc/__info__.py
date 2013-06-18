name = "LIRC Event Receiver"
kind = "remote"
version = "0.5.0"
author = "jinxdone"
description = """
This plugin reads Lirc eventstrings over a TCP-connection and generates EventGhost events accordingly.<p>

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
<LI><i>Ignoretime after first event</i><br>
You can specify a time during which after a first event any repeat-events are discarded. The value is in milliseconds, set to 0 to disable.
<br>
<LI><i>Use enduring-events</i><br>
Generate enduring events for EventGhost, this involves a workaround that will add 400ms of "lag" into your keypresses. <u>Overrides any other settings except the optional remote name.</u>
</UL>
"""