;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; Version 1.0
; Author: Walter Krämbring
; Date: 18.04.2008
; 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 

 This plugin for EG is intended too be used as a scheduler for planned controls.

 All credits to Bartman, I have based it on code and structure from his Timer plugin.


 You could for instance feed your fishes in the pond automatically (provided you
 have the machine for that purpose) or control automatically the motor heater of your car.

 If you use radio controlled outlet switches, you could start to save all that standby
 energi your stuff is consuming today. Fantasy is free....

 Some words about the settings as seen in the picture:

 The first 3 fields for scheduler and event names are rather obvious.

 For each daytype you have 3 on and 3 off time settings. Write them in format "hhmm" like 1830.
 There are some error controls built in but if its 100% failsafe is left to be seen.

 Then there are public holidays. You have fixed ones and you have variable ones (that changes
 every year). So this you need to maintain yearly.

 The logic in handling holidays is as follows
  - if today is a normal weekday and tomorrow is a holiday, use time settings for Friday
  - if today and tomorrow are holidays, use time settings for Saturday
  - if today is a holiday and tomorrow normal weekday, use time settings for Sunday

 There is also a special Vacation daytype that you can use when the family is on vacation and
 the house is empty anyway. If you check the checkbox for this alternative, every day will
 use the settings for "vacation" until you uncheck it again.

 Some devices, especially radio controlled, needs sometimes the command to be repeated.
 The setting for this is called bursts, here you define how many "copies" of the event
 you like to create when turning on or off.

 Some transmission devices also need a short delay between the transmissions. So there is
 also a setting for that.

 Finally, you can decide if you like to have an entry printed in the log window for each
 loop execution.

 Talking about log, in a separate directory, "Log", you find a logfile in html-format holding
 the on off actions 

 To make things happen, just do as normal, finalize your settings, create an event with the
 same name in any macro together with actions.
