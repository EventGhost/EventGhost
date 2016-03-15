Ping Plugin for eventghost
author : miljbee+egPing@gmail.com
rev 0.0.2

rev History :
0.0.2 : 
	- The plugin now uses a pure python ping implementation. the windows ping.exe isn't used anymore
		- All the threads can now be interrupted immediately (in 0.0.1, the code should wait for running ping.exe to end).
		- The plugin should consume far less cpu time.
		- The plugin param is no more needed ... unfortunatly, this breaks compatibility, with 0.0.1. :
			- if you upgrade, please remove all plugin actions, remove the plugin, then re add ...
	- The OnePing action now returns the response time in ms in eg.result
	- The GetHostsStatus action now returns the last response time in ms (if the host has ever responded to the pings !)
	- Small changes and clean up on the messages sent to the console
	
0.0.1 :
	- Initial release, based on the windows ping.exe program.

usual warning :
This plugin is provided as is, it is not sure it will work, perhaps it will destroy your computer, or even your house, but I can not be held responsible for this.
You are supposed to be clever enougth to fully understand what this code do before using it.
You have been warned !

sharing, modifying, distributing this code ...
You can do whatever you want with this code, but please, be kind enough to remember that I am the author of it. I would be very happy to know what you are doing with it.

What is it for ?

This plugin is to get events when a host become available or unavailable on the network.
You can use it for many things, here are a few exemples :

Get an event when you loose your internet connection
Get an event when you turn on or off your TV (if it has TCP/IP connectivity of course)
Get an event when you arrive at home (yes you can do this ! if you have a wifi smartphone in your pocket that automatically connects to your wlan)
Get an event when someone connects to you wlan (if you know his ip adress, which may be the case, if you know the first available address of your dhcp)

How does it work ?
1 - Add the plugin in you eg tree
2 - Add a new action in a macro : Ping\AddHost
2a - Fill in the params, the only important one is the hostname. It can be an ip, or anything that windows can resolve into an ip address.
	valid exemples are 192.168.0.62, www.google.com
3 - Run this macro
4 - If the host respond to ping, you will immediately get the Alive Event, else the Dead Event.
5 - let's say your host is alive, let eg run
6 - turn off your host
7 - it won't last long before you get the dead event for this host
8 - Add the other hosts you wish to manage

How does it work internally ?
When you add a host, the plugin creates a host object. the host object has a thread. The thread is started as soon as you add the host.
The thread performs ping commands. it's a full ping python implementation.

What can I do with the "number of successive successfull/unsuccessfull ping to fire event" ?
This param is usefull for me, I hope it will be for you ! Here is how I use it :
I have an iPhone which automatically connects to my wlan to retrieve my mails every 15 Minutes.
When it connects, it lasts just a few seconds, and I don't wan't to get event alive/dead each time.
I just want to know if my iPhone is in my house (so if I am in my house ...)
So I set up the host to : 
ping every 5s
wait 1000ms for the ping response
fire the alive event after the first successfull ping
fire the dead event, only after 90 unsuccessfull ping (180*5=900s=15min).

This way, I get an alive event 15min max after I arrives at home (it's the max time needed for the iphone to wake up), and a dead event 15min max after I left my house (it's the delay implemented in the ping plugin) ...
And thus can automatically turn off my heaters after the dead event...

You said that the only important param is the hostname, what about the others ?
the friendlyName is used to compute the events names if you don't set them. 
If friendly name and events names are not set, the events names are built from the host name !
The ping delay is the time the ping command will wait for the host to respond (equivalent to the -w param of the windows ping.exe)
The delay between pings is the time the host thread will wait between two ping commands (end of ping command and start of new one. That's not the delay between 2 starts !).
Other params have already been explained !


Feel free to contact me if you need to make a donation ... paypal account : miljbee at gmail dot com


