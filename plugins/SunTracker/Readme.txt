;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; Version 1.0
; Author: Walter Krämbring
; Date: 22.04.2008
; 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 

 This plugin for EG is intended to be used as a sunset/sunrise tracker for planned controls. I call it SunTracker.


 All credits to Bartman, I have based this one too on code and structure from his Timer plugin.

 I took it as a little challenge to re-work my script "SunRiseSet" into a plugin. 


 With this you could for instance fully automate your outdoor lights on your house, in your garden or park
 if you are lucky to have one. For sure its most useful for controlling lights and with the offset
 you can also control your indoor lights like I do myself. Maybe I should call the mayor, we could
 tune the whole downtown...and save some energy too...


 I use radio controlled (RF) outlet switches, but basically you can control anything that is supported by
 EG, just copy and paste the event name in a macro with actions.


 Some words about the settings as seen in the picture:

 The first 3 fields for tracker and event names are rather obvious.

 The longitude and latitude fields are needed to calculate the sunset/sunrise at your location.

 For each daytype you have 3 time settings. Write them in format "hhmm" like "1830".

 - "Night OFF" means any time between 0001-0559 when you want something to be turned OFF
 - "Morning ON" is the time in the morning from 0600-1759 (long morning, yes) when you want
    something to be turned ON
 - "Evening OFF" is the OFF time in the evening starting from 1800-2359


 A typical use-case could look like this

 During weekdays, Monday through Thursday, it would be that
	- the outdoor lamp is turned ON every morning at "0600"
	- it is then turned OFF at sunrise
	- it is turned ON again at sunset
	- finally, its turned OFF later in the evening, like "2300"

 On Friday evenings it would not be turned OFF, instead this happens Saturday night at "0200" (because
 the kids always arrives home much later during weekends)

 For Saturday we do not turn ON the light at all in the morning, everybody is sleeping anyway...
 Later in the evening, it is turned ON at sunset. The same procedure as for Friday, its turned OFF
 at "0200" Sunday night.

 ON Sundays, finally, the same morning and eveing procedure as during Saturdays wih the exception
 that the lights are turned OFF in the evening at "2300".

 During Vacation when the house is empty and you are dancing in Ibiza, another pattern could be 
 applicable...

 I hope you got the basic idea behind. The picture below is configured accordingly

 There is a checkbox where you can enable/disable the vacation override function. If checked,
 all days will follow the vacation schedule.


 Then there are public holidays. You have fixed ones and you have variable ones (that changes
 every year). So this you need to maintain yearly.

 The logic in handling holidays is as follows
  - if today is a normal weekday and tomorrow is a holiday, use time settings for Friday
  - if today and tomorrow are holidays, use time settings for Saturday
  - if today is a holiday and tomorrow normal weekday, use time settings for Sunday


 Some devices, especially radio controlled, needs sometimes the command to be repeated.
 The setting for this is called bursts, here you define how many "copies" of the event
 you like to create when turning ON or OFF.

 Some transmission devices also need a short delay between the transmissions. So there is
 also a setting for that.

 Also it makes no sense to turn on lights if they anyway are going to be turned OFF shortly.
 Here you have a setting where you define the minimum ON period left to be required.

 You can decide if you want the devices to be synchronized or not. This means that if by
 accident, someone turns a light OFF when its supposed to be ON, it will be turned ON again
 at the next synchronization. The interval is also configurable.

 If you like, you can specify an offset in minutes for ON/OFF events. A negative offset, as
 example -45, results in that the ON event is created the specified number of minutes
 (in this example 45 minutes) BEFORE the actual sunset happens.

 The OFF event will occur the same amount of minutes AFTER the actual sunrise. This function
 is much appreciated when you like to control indoor lights since it's normally getting a bit
 darker earlier inside than outside.

 A positive offset works the reverse way. It creates the ON event specified number of minutes
 AFTER the actual sunset. The OFF event will occur the same amount of minutes BEFORE the actual
 sunrise. This function can be used in cases where you think that there is still enough light
 from the sun also a period of time after the actual sunset and before the sunrise. It depends
 on your actual location.


 Finally, you can decide if you like to have an entry printed in the log window for each
 loop execution.

 Talking about log, in a separate directory, "Log", you find a logfile in html-format holding
 the on off actions 

 To make things happen, just do as normal, finalize your settings, create an event with the
 same name in any macro together with actions.
