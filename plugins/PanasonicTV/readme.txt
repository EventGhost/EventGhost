PanasonicTV 
===========

PanasonicTV is a plug-in for EventGhost (http://eventghost.org/)
This plug-in will allow you to control your Panasonic TV over ethernet with EventGhost.

With this plug-in you can:
- emulate remote control buttons 
- query basic information from your TV 
- set absolute volume levels or mute state

Installation
============

Download the .zip file from https://github.com/EssKaa/PanasonicTV
Unzip it into the EventGhost plug-in directory

Requirements
============

On your TV: 
    Go to: Menu -> Setup -> Network Setup -> Network Link Settings -> 
    
    Make sure that the following options are set:
    DLNA Remote Control -> On
    DLNA Remote Volume -> On
    Network Remote Control -> On
    
In EventGhost:
    Configure the TV's device IP address or hostname, preferably the FQDN (mytv.mydomain.local). 
    The port should not need any configuration.

Compatibility
=============

Check https://github.com/EssKaa/PanasonicTV/wiki/Compatibility for the most recent compatibility list.

It should work with most Panasonic TVs, if you don't find your model on the list give it a try.
The following devices were TESTED:

TX-P50VT30E
TX-P55ST50Y
TC-L55ET5

Version history
===============

1.3     fixed Set Mute on / off
        added Smart Mute functionality

1.2     Added direct input keys for:
        HDMI1
        HDMI2
        HDMI3
        HDMI4
        AV1
        AV2

1.1     Fixed settings dialog

1.0     Initial release

Known issues
============

If you set the volume to "0" using the "Set Volume" action and change it with the IR control of the TV, 
you cannot change it back to "0" using "Set Volume" unless you set it to another value before.
This strange behaviour seems to come from the TV itself.

Credits
=======

+ Sascha Killeweit (EssKaa)
+ Jingo

Thank you Jingo for helping me and being a good friend!