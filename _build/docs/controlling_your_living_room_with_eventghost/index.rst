.. _Controlling-your-living-room-with-EventGhost:

============================================
Controlling your living room with EventGhost
============================================

This article is a thank-worthy contribution by Benjamin Webb. 

Introduction
============

Yes, I've been there. You have your HTPC all set up to go. Then you realize 
that you have no way to seamlessly use your HTPC with your current living 
room set up. You may be sitting there with a wireless keyboard and mouse 
controlling it or you may be plopped down in front of your PC pressing return 
to select a different video to be displayed. There is still hope for you yet. 
There are many solutions today for giving you control of both your PC and the 
remaining elements of your living room. Currently, most universal IR remotes 
are up to the task of linking together most things in your living room except 
your PC. Many places offer niche products that are set up to control certain 
applications on a computer or record and emit a limited number of IR codes. 
I have long since searched for the ultimate of HTPC building: pressing a 
button and having it turn the TV on, and then go on to control your PC. There 
are many schools of thought as to how this should occur. This article teaches 
you one that involve an innovative, free program called EventGhost for Windows 
2000, XP or Vista. 

    
    
IR PC Control
=============
I love basic IR PC control. It is inexpensive and thanks to EventGhost, easy 
to set up. The downside is pretty obvious. You need line of sight. You cannot 
turn up the volume when someone wanders in front of the TV as a result. People 
in general are used to the basic concept of IR, just point and click. It is 
inexpensive since you can use whatever remote you have laying around. One 
piece of advice is to try to get a remote that sends the same signal every 
time you click the button. Some remotes have a rotation of signals that they 
send to the device they control. This can cause problems when programming such 
a device. You can still program remotes like this but it's annoying to put in 
all the other IR codes as actions that trigger events. There may even be some 
company out there that created a remote with a constantly changing IR signal 
that is interpreted by an algorithm on the device (I haven't found one yet but 
they may exist). The reason for not keeping IR signal constant is to prevent 
universal remote from doing their job and forcing the user to use the device 
creators remote. 

RF X10 PC Control
=================
The program comes with an X10 remote plugin. This plugin, in theory, allows 
you to use any X10 compatible remote. I will test a Snapstream Firefly X10 
remote in this article. I have tested this remote before and it will travel 
35 feet through just about any wall excluding the cinderblock walls at my 
dorm. The software for this remote was very resource heavy and the main reason 
I was searching for an alternative program. 


IR Device Control
=================
EventGhost can be used with devices such as the USB-UIRT to transmit IR 
signals to devices you use with or without line of sight or simply use 
devices your remote is not programmed for. The USB-UIRT can be connected to 
objects placed away from line of sight. You just attach IR emitters to reach 
up to 300' around your house. Without the emitters the device needs to be 
placed in front of the device it will control. In this review, I will test 
two IR emitters attached with a stereo splitter. The IR emitters I will test 
have a reach of 10 feet. 


Programming
===========
 
Basics
------

EventGhost is a very interesting program. You install plugins that enable 
different events to be displayed on the logger. Simply click the add plugin 
button to gain access to the plugin listing screen.

.. image:: CYLRWE_pluginlisting.png
    :align: center
  
As you can see the plugins give this program capability far beyond what this 
article covers but before you tackle network control or speech control you 
must learn the basics.
    
An event triggers a macro and a macro consists of one or more actions. For 
example, I set up the disc button on my remote to launch iTunes. First, I 
installed the USB-UIRT plugin. Then, when I pointed the remote toward the 
USB-UIRT and pressed the disc button on the remote the IR code was displayed 
in the logger. 

.. image:: CYLRWE_IR_event.png
    :align: center

Make a macro by right clicking on the configuration panel (the group of stuff 
on the right) and select :guilabel:`Add Macro`. You will now immediately 
get a dialog where you can choose your first action.

.. image:: CYLRWE_select_action.png
    :align: center

After you have open up the action selection menu you just select the action 
of your choice. In my case, I wanted to launch iTunes, so I opened up the 
system folder and selected start application. EventGhost will now ask for 
additional properties of the action. 

.. image:: CYLRWE_launch_program_action.png
    :align: center

Here is how you would configure the start program action to launch iTunes.
From there navigate the file path to the program you want to open. In my case, 
the path was :file:`C:\\Program Files\\iTunes\\iTunes.exe`. After you have 
pressed the Ok button, you will see your newly added macro with the action in 
your configuration. Then drag and drop the IR event code you want to use from 
the logger to the macro you just created.

.. image:: CYLRWE_launch_program_action.png
    :align: center

EventGhost names the macro automatically but you can also rename the item (for 
your sanity be sure the name makes sense to you) 

Program Control
---------------

Now that you have the program open, there are multiple programming choices you 
can make. To simplify things, first, make a folder from which you store all of 
the instructions for controlling the program. This folder can later be called 
by an exclusive. I usually keep mine in the context folder, but anywhere will 
work. You name the folder which I conveniently called iTunes, then you precede 
by creating a macro for each action(s) you want to perform for iTunes.


Enabling Exclusives
-------------------

One of the meanings of exclusive is to grant a privilege to a selected group 
or single person. The concept remains the same here. An exclusive grants a 
particular macro or folder exclusive rights to be currently in control or 
active. Enabling exclusive is that action you take to activate the commands 
listed in the folder that you have chosen. It can also be used to call macros 
but keeping all you commands in one folder makes trouble shooting easier. It 
is available if you right click and select add action. You then proceed to 
open up the EventGhost folder. You have to select the folder/macro to make 
active after adding the exclusive. 


.. figure:: CYLRWE_enable_exclusive_config.png
   :figwidth: 100%
   :align: center
   
   Just select the folder that you want to make active as a result of the 
   event in the macro.

The event you want to activate your folder with is a matter of choice. I 
installed the Task Create/Switch Events plugin to cause the folder to be 
enabled when iTunes is active. If you choose to activate the folder when you 
launch iTunes from the disc button this will also work fine. You can activate 
other folders when you close programs or press a different button also. The 
choices are all up to you. 

The program comes with examples from WinAmp and ZoomPlayer. If these are your 
media programs of choice then all you need to do is replace the events put 
there by default with the ones from your IR remote. I understand that this is 
a brief explanation but it should enable you to be able to perform most basic 
keyboard shortcuts with the program of your choice. EventGhost is mostly drag 
and drop or copy and paste. This EventGhost also includes an excellent mouse 
emulator that you can tweak to your satisfaction.



X10 Programming
---------------

IR remote and X10 remote instructions remain basically the same. The events 
are simply listed on the logger as with the IR. The mouse functionality was 
easily implemented by simply putting in the X10 event X10.MTVCR in the 
"switch to mode: Mouse Emulation macro" I then program in the directional 
keys. I was not able to completely fine tune the X10.xml to be activated by 
the opening of iTunes or GBPVR due to the death of my remote. Here is a 
perfect start for those willing to tweak some more. 

+-------------------------------------+-------------------------------------+
| This is a sample of some X10        | This is what I did to enable the    |
| events on the logger:               | mouse on the firefly:               |
+-------------------------------------+-------------------------------------+
| |LeftPic|                           | |RightPic|                          |
+-------------------------------------+-------------------------------------+


.. |LeftPic| image:: CYLRWE_X10_event.png
   :alt:

.. |RightPic| image:: CYLRWE_X10_mouse.png
   :alt:


IR Transmission Programming
---------------------------

This is basically more of the same. You simply create a macro with an event 
that triggers the IR transmitting action. This is available if you expand the 
USB-UIRT folder in the add actions menu.

After the action has been added you simply click on Transmit IR icon and 
select learn an IR code. Make sure that you position the remote closer than 
half of an inch of the USB-UIRT to learn the IR code. I found the code was not 
learned correctly otherwise.

If you are looking to control channel changing for your tuner, currently you 
have to rely on the software that does the recording to change the channel. 
With the USB-UIRT this is not usually a problem since most HTPC recording 
programs provide there own interfaces for programming this in. I'm sure with 
more advanced plugins and creative programming this may be possible.


Results
=======

I consider the mouse function of EventGhost to be far superior to the 
Firefly's original software. The speed of the cursor slowly ramps up the 
longer the button is pressed. One of the most refreshing things about this 
program is that it uses about 8 MB of RAM as compared to Snapstream's 108 MB. 
This significantly improved the reaction time of this computer. The USB-UIRT 
worked as a perfect substitute for a X10 remote. The IR transmitting also 
worked perfectly. I highly suggest the stick-on IR emitters I purchased from 
SMARTHOME. Both IR emitters were able to transmit perfectly to the VCR. You do 
not have to position your USB-UIRT directly in front of the device you wish to 
control this way. This also leaves the USB-UIRT to be positioned perfectly as 
a receiver. I have not found any pitfalls in the software besides having to 
restart the program once the USB-UIRT has been connected.


Conclusion
==========

I was able to adjust the software to my satisfaction.  This did take a few 
hours and a bit of trial and error to get the hardware working correctly.  I 
found this to be about the same as programming a universal remote once you got 
the hang of it but at least this way you don't loose your settings when the 
batteries are pulled out.  The main downfall of this software is that the 
users do not openly share the xml files that they have created.  Everything 
must be done by you excluding the examples put in the program by default.  
The forum is extremely helpful and also prompt with answers.  They are also 
adding new hardware support and plugins constantly.  I found the wiki created 
for this program is a very poor source for beginners but considering the 
usefulness of this program I was able to work my way through it.  This is 
intended to be a gateway article for those looking to enter the world remote 
PC control and the sky is the limit as to where you can go from here.  As 
usual in the free software HTPC world you have to become your own hardware 
expert to pull off what your striving to do.  This program cannot exceed 
beyond what the hardware is capable of.  

On a side note, I highly suggest :doc:`donating or contributing <../contributing>`
to this project to ensure its future success. If your 
device is not currently supported just check back at the :doc:`supported 
hardware <../supported_receivers>` page from time to time to see what they're 
working on.
