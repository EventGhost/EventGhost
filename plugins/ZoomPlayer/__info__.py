name = "Zoom Player"
author = "Bitmonster"
version = "1.0.0"
kind = "program"
description = """
Adds support functions to control the famous Zoom Player.

<p>
<b>Notice:</b><br>
To make it work, you have to enable TCP control in Zoom Player. Either enable it
in the options of Zoom Player under:
<p>
<i>Option/Setup => Values & Tools => Interface => Enable External TCP Control</i>
<P>
or call the executable with the option <i>/TCP:[port]</i>
<p>
<b>Hint:</b><br>
Disable scroll acceleration in Zoom Player. Otherweise scrolling in navigators 
might be jumpy if you use autorepeat in EventGhost (which has a more 
sophisticated scroll acceleration). You find the setting in Zoom Player under:<br>
<i>Option/Setup => OSD => Navigators => Settings => Disable Scroll Acceleration</i>
"""