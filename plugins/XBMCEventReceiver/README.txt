# This plugin is based on the Broadcaster plugin that was originally provided 
# by the good work from Kingtd.  I have used it as a basis for true 2-way control 
# too and from XBMC.  The following improvements have been made to v2.0:
#
#	- Enabled additional fields for configuration of HTTP.API destination in setup
#	- Enabled the invoking of XBMC Host Broadcast function with in the script
#	  (so it is not necessary to do it manually)
#	- Cleaned up some of the code.
#	- Fixed error when trying to reconfigure plugin
#
# Future enhancements to make for future ver. as time permits such as: 
#
#  - Extending response functionality as it applies to XBMC (once it is implemented @ the XBMC Host).
#  - Additional parsing of input from XBMC host
#  
#  If you have any additional comments or suggestions feel free to contact me at vortexrotor@vortexbb.com


XBMC Event Receiver Plugin for Eventghost - README





Use the following to control the broadcasting of events (assumes xbox is the address of your xbox 
running xbmc and xbmc has its web server turned on):

Turns on broadcasting at low level (just playing events)


http://xbox/xbmcCmds/xbmcHttp?command=SetBroadcast&parameter=1;8278



Turns on broadcasting at high level (includes button presses etc)

http://xbox/xbmcCmds/xbmcHttp?command=SetBroadcast&parameter=2;8278



Turns off broadcasting events

http://xbox/xbmcCmds/xbmcHttp?command=SetBroadcast&parameter=0




Note the 8278 parameter is the default value and is optional if the default value is to be used. 
Make sure it is the same value as used by XBMC Listener.



Provided you have xbmc running on the same lan segment as XBMC Listener you should not need to change the IP 
address used by XBMC Listener. 

If this is not the case - you are on your own!



Displays the current setting

http://xbox/xbmcCmds/xbmcHttp?command=GetBroadcast