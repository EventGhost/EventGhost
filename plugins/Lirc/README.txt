26th July 2007 - v0.6.0

EventGhost plugin for receiving Lirc-style events written in python.

Extract into the EventGhost\Plugins directory, files should be as follows;
   EventGhost\Plugins\Lirc\__init__.py
   EventGhost\Plugins\Lirc\__info__.py
   EventGhost\Plugins\Lirc\icon.png



This has only been tested with WinLirc (http://winlirc.sourceforge.net/),
though it should also work with any version of Lirc (http://www.lirc.org/).


If you are using WinLirc I'd suggest setting it a higher priority than normal.
It's also a good idea to autorun it from somewhere, for example from
eventghost or automatically during windows startup etc.

Example of launching winlirc with higher priority:
cmd.exe /C "start /realtime /min /B /D C:\winlirc\ C:\winlirc\winlirc.exe"


Any questions? comments? 
Ask on the forum or email jinxdone@earthling.net


changelog:
V0.6.0 - Removed the internal enduring-event generation
       - Added adjustable enduring event timeout value
       - some other minor changes

v0.5.0 - First public version