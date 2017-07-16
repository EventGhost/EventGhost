## [0.5.0-rc4](https://github.com/EventGhost/EventGhost/releases/tag/v0.5.0-rc4) (2017-07-16)

**Enhancements:**

* Changes XmlIdLink to eg.GUID \(see comment for more info\) [\#264](https://github.com/EventGhost/EventGhost/pull/264) ([kdschlosser](https://github.com/kdschlosser))
  
  The use of XmlId made it difficult to share code that used 'Enable/Disable Action' or 'Exlusive Enable' (and others). Now with the use of GUID's this hurdle is gone.

  To turn it on you would open the add plugin dialog and left click once in the upper right hand corner of the dialog (client area) and then click once in the lower left hand corner of the dialog (client area). There is a 20x20 pixel target for each of the spots so the chance of someone doing this accidentally is probably not going to happen. But in the event it does, a message box asking if you want to enable or disable it pops up.

  **Warning: This process cannot be undone, so make a backup copy of your config tree before enabling it.**

**Fixed bugs:**

* SoundMixer: Fixes traceback when using the Primary Sound Driver [\#255](https://github.com/EventGhost/EventGhost/pull/255) ([kdschlosser](https://github.com/kdschlosser))
* NamedPipe: Fixes traceback if returned item is not able to be evaluated [\#256](https://github.com/EventGhost/EventGhost/pull/256) ([kdschlosser](https://github.com/kdschlosser))
* Fixes restart not working from the file dropdown menu [\#257](https://github.com/EventGhost/EventGhost/pull/257) ([kdschlosser](https://github.com/kdschlosser))
* SoundMixer: Fixes lag when setting the relative volume [\#258](https://github.com/EventGhost/EventGhost/pull/258) ([kdschlosser](https://github.com/kdschlosser))
* EventThread: Fixes -event not working from cli if there is no EG running [\#261](https://github.com/EventGhost/EventGhost/pull/261) ([kdschlosser](https://github.com/kdschlosser))
* \[System\] Fix Monitor On action not functioning properly in Windows \> 8 [\#262](https://github.com/EventGhost/EventGhost/pull/262) ([kdschlosser](https://github.com/kdschlosser))
* CLI: fix bug when showing message on -netsend failure [\#263](https://github.com/EventGhost/EventGhost/pull/263) ([topic2k](https://github.com/topic2k))

**Other changes:**

* \[XBMC2\] update plugin to 0.6.33 [\#259](https://github.com/EventGhost/EventGhost/pull/259) ([topic2k](https://github.com/topic2k))


## [0.5.0-rc3](https://github.com/EventGhost/EventGhost/releases/tag/v0.5.0-rc3) (2017-07-03)

**Enhancements:**

* Document all command line options [\#235](https://github.com/EventGhost/EventGhost/pull/235) ([per1234](https://github.com/per1234))
* Add Named pipe support to solve the problem with elevations [\#240](https://github.com/EventGhost/EventGhost/pull/240) ([kdschlosser](https://github.com/kdschlosser))
* eg.WinApi: Functions to get information about logged in user [\#254](https://github.com/EventGhost/EventGhost/pull/254) ([kdschlosser](https://github.com/kdschlosser))

**Fixed bugs:**

* MainMessageReceiver: Fixes broken clipboard chain in windows 10 \(reported by saue0\) [\#227](https://github.com/EventGhost/EventGhost/pull/227) ([kdschlosser](https://github.com/kdschlosser))
* \[SchedulGhost\] update plugin to 0.1.18 [\#238](https://github.com/EventGhost/EventGhost/pull/238) ([topic2k](https://github.com/topic2k))
* Fixes incorrect checking of powerbroadcast notification message [\#241](https://github.com/EventGhost/EventGhost/pull/241) ([kdschlosser](https://github.com/kdschlosser))
* \[Broadcaster\] Fixes depreciation warning from asyncore.dispatcher [\#242](https://github.com/EventGhost/EventGhost/pull/242) ([kdschlosser](https://github.com/kdschlosser))
* \[USBUIRT\] Fixes learn ir dialog not closing [\#243](https://github.com/EventGhost/EventGhost/pull/243) ([kdschlosser](https://github.com/kdschlosser))
* \[MCERemoteVista\] Upgrades MCERemoteVista to version 1.4 [\#244](https://github.com/EventGhost/EventGhost/pull/244) ([kdschlosser](https://github.com/kdschlosser))
* \[System\] fix GetMasterVolume \(move use of VistaVolEvents to eg.WinApi.SoundMixer\) [\#246](https://github.com/EventGhost/EventGhost/pull/246) ([kdschlosser](https://github.com/kdschlosser))
* NamedPipe: Fixes possible endless loop if -restart is used at the CLI [\#247](https://github.com/EventGhost/EventGhost/pull/247) ([kdschlosser](https://github.com/kdschlosser))
* Typo - Text.py, Fixes typo in save dialog [\#250](https://github.com/EventGhost/EventGhost/pull/250) ([kdschlosser](https://github.com/kdschlosser))
* Moves initialization of python paths to the first thing that EG does [\#253](https://github.com/EventGhost/EventGhost/pull/253) ([kdschlosser](https://github.com/kdschlosser))

**Other changes:**

* Remove wiki content from documentation [\#234](https://github.com/EventGhost/EventGhost/pull/234) ([per1234](https://github.com/per1234))


## [0.5.0-rc2](https://github.com/EventGhost/EventGhost/releases/tag/v0.5.0-rc2) (2017-04-20)

**Fixed bugs:**

* Fixes incorrect replacement usage of IsVista\(\) and IsXP\(\) [\#221](https://github.com/EventGhost/EventGhost/pull/221) ([kdschlosser](https://github.com/kdschlosser))


## [0.5.0-rc1](https://github.com/EventGhost/EventGhost/releases/tag/v0.5.0-rc1) (2017-04-16)

**Important changes for plugin developers:**

* Add class for windows version checking [\#210](https://github.com/EventGhost/EventGhost/pull/210) ([topic2k](https://github.com/topic2k))

**Enhancements:**

* WindowsVersion, Fixes issue with help [\#215](https://github.com/EventGhost/EventGhost/pull/215) ([kdschlosser](https://github.com/kdschlosser))
* Add menu to restart EG with admin rights [\#218](https://github.com/EventGhost/EventGhost/pull/218) ([topic2k](https://github.com/topic2k))

**Fixed bugs:**

* Fixes log being scrolled to the top after restored from tray icon [\#199](https://github.com/EventGhost/EventGhost/pull/199) ([kdschlosser](https://github.com/kdschlosser))
* \[System\] Adds Windows XP support and moves the registering of the GUID's to the main thread [\#204](https://github.com/EventGhost/EventGhost/pull/204) ([kdschlosser](https://github.com/kdschlosser))
* Fixes exit not working from system tray icon when minimized [\#207](https://github.com/EventGhost/EventGhost/pull/207) ([kdschlosser](https://github.com/kdschlosser))
* Fixes incorrect reporting of windows version [\#211](https://github.com/EventGhost/EventGhost/pull/211) ([kdschlosser](https://github.com/kdschlosser))
* \[EventGhost\] \(PythonScript\) Fixes PrintError traceback [\#219](https://github.com/EventGhost/EventGhost/pull/219) ([kdschlosser](https://github.com/kdschlosser))
* \[ProcessWatcher\] Fixes thread not closing properly [\#220](https://github.com/EventGhost/EventGhost/pull/220) ([kdschlosser](https://github.com/kdschlosser))

**Other changes:**

* \[System\] Removes disabling of widgets if extension not in %PATHEXT% [\#189](https://github.com/EventGhost/EventGhost/pull/189) ([kdschlosser](https://github.com/kdschlosser))


## [0.5.0-beta6](https://github.com/EventGhost/EventGhost/releases/tag/v0.5.0-beta6) (2017-02-12)

**Enhancements:**

* PluginInstall: added backup, GUID check, better user notification, pretty print the info.py [\#137](https://github.com/EventGhost/EventGhost/pull/137) ([kdschlosser](https://github.com/kdschlosser))
* Ask to delete config data of plugin if uninstalled [\#140](https://github.com/EventGhost/EventGhost/pull/140) ([kdschlosser](https://github.com/kdschlosser))
* Add checking for hidden or system files on plugin import/export [\#146](https://github.com/EventGhost/EventGhost/pull/146) ([kdschlosser](https://github.com/kdschlosser))
* Add the Widget Inspection Tool to the Help menu. [\#153](https://github.com/EventGhost/EventGhost/pull/153) ([topic2k](https://github.com/topic2k))
* \[System\] PowerBroadcastNotifier, Adds additional notifications [\#175](https://github.com/EventGhost/EventGhost/pull/175) ([kdschlosser](https://github.com/kdschlosser))

**Fixed bugs:**

* Not being able to restore from a minimized state if tray icon is not shown and empty log [\#145](https://github.com/EventGhost/EventGhost/pull/145) ([kdschlosser](https://github.com/kdschlosser))
* Fix for empty Logctrl after restoring from tray \(fixes \#138\) [\#149](https://github.com/EventGhost/EventGhost/pull/149) ([topic2k](https://github.com/topic2k))
* \[Speech\] Fix wxGridSizer error when adding action [\#155](https://github.com/EventGhost/EventGhost/pull/155) ([per1234](https://github.com/per1234))
* Avoid duplicate GUIDs of tree Items on copy/paste [\#161](https://github.com/EventGhost/EventGhost/pull/161) ([kdschlosser](https://github.com/kdschlosser))
* Add six to included modules \(fixes \#169\) [\#171](https://github.com/EventGhost/EventGhost/pull/171) ([topic2k](https://github.com/topic2k))
* \[System\] MonitorPowerOn not working in Windows 8 & 10 [\#174](https://github.com/EventGhost/EventGhost/pull/174) ([kdschlosser](https://github.com/kdschlosser))
* Add module for patching pywin32 [\#177](https://github.com/EventGhost/EventGhost/pull/177) ([kdschlosser](https://github.com/kdschlosser))
* \[Speech\] nearly complete rewrite of the plugin [\#179](https://github.com/EventGhost/EventGhost/pull/179) ([topic2k](https://github.com/topic2k))
* Dialog gets stuck if a traceback occurs during it's creation. [\#184](https://github.com/EventGhost/EventGhost/pull/184) ([kdschlosser](https://github.com/kdschlosser))
* \[eg.SpinNumCtrl\] Re-add workaround for traceback if min value \> 0 [\#188](https://github.com/EventGhost/EventGhost/pull/188) ([kdschlosser](https://github.com/kdschlosser))
* Removes accidentally added SetMin\(\) from SpinNumCtrl [\#192](https://github.com/EventGhost/EventGhost/pull/192) ([kdschlosser](https://github.com/kdschlosser))
* WinUsbWrapper.dll broken in 0.5 builds [\#195](https://github.com/EventGhost/EventGhost/pull/195) ([kdschlosser](https://github.com/kdschlosser))

**Other changes:**

* \[System\] Allow multiple quoted arguments in calls to CMD via /S [\#150](https://github.com/EventGhost/EventGhost/pull/150) ([edemaine](https://github.com/edemaine))
* \[Remote Event Mapper\] Fix rendering of reStructuredText in description [\#170](https://github.com/EventGhost/EventGhost/pull/170) ([per1234](https://github.com/per1234))
* Change "Search our issue tracker" link to also show closed issues and PRs [\#173](https://github.com/EventGhost/EventGhost/pull/173) ([per1234](https://github.com/per1234))


## [0.5.0-beta5](https://github.com/EventGhost/EventGhost/releases/tag/v0.5.0-beta5) (2016-12-24)

**Enhancements:**

* Finish the new "Add Event..." dialog [\#110](https://github.com/EventGhost/EventGhost/pull/110) ([topic2k](https://github.com/topic2k))
* Documentation improvements [\#114](https://github.com/EventGhost/EventGhost/pull/114) ([per1234](https://github.com/per1234))
* Bring back the -debug command line argument [\#118](https://github.com/EventGhost/EventGhost/pull/118) ([topic2k](https://github.com/topic2k))
* Popup menu and hotkey for "Select All" in LogCtrl [\#124](https://github.com/EventGhost/EventGhost/pull/124) ([topic2k](https://github.com/topic2k))
* Adds GUID to treeItems [\#133](https://github.com/EventGhost/EventGhost/pull/133) ([kdschlosser](https://github.com/kdschlosser))
* \[Webserver\] plugin updates \(with commit for each version\) [\#134](https://github.com/EventGhost/EventGhost/pull/134) ([per1234](https://github.com/per1234))
* \[EventGhost\] add skin selection to ShowOSD [\#136](https://github.com/EventGhost/EventGhost/pull/136) ([topic2k](https://github.com/topic2k))

**Fixed bugs:**

* \[Broadcaster\] fix Unicode encoding and decoding [\#122](https://github.com/EventGhost/EventGhost/pull/122) ([david-mark](https://github.com/david-mark))
* Fix typo in build warning message [\#135](https://github.com/EventGhost/EventGhost/pull/135) ([per1234](https://github.com/per1234))


## [0.5.0-beta4](https://github.com/blackwind/EventGhost/releases/tag/v0.5.0-beta4) (2016-09-14)

**Enhancements:**

* Register restart handler for easy crash recovery [\#103](https://github.com/EventGhost/EventGhost/pull/103) ([blackwind](https://github.com/blackwind))

**Fixed bugs:**

* Make automatic log scrolling work at all window sizes [\#98](https://github.com/EventGhost/EventGhost/pull/98) ([blackwind](https://github.com/blackwind))
* Make plugin export work for non-English users [\#101](https://github.com/EventGhost/EventGhost/pull/101) ([blackwind](https://github.com/blackwind))
* Prevent traceback in PyCrust when a plugin imports its own modules [\#102](https://github.com/EventGhost/EventGhost/pull/102) ([blackwind](https://github.com/blackwind))
* Open plugin installer even if program isn't running [\#104](https://github.com/EventGhost/EventGhost/pull/104) ([blackwind](https://github.com/blackwind))
* \[Window\] Prevent random traceback on Grab Text Item\(s\) action [\#105](https://github.com/EventGhost/EventGhost/pull/105) ([blackwind](https://github.com/blackwind))


## [0.5.0-beta3](https://github.com/EventGhost/EventGhost/releases/tag/v0.5.0-beta3) (2016-08-16)

**Fixed bugs:**

* Catch errors when adding a plugin [\#92](https://github.com/EventGhost/EventGhost/pull/92) ([topic2k](https://github.com/topic2k))
* Gracefully handle all possible plugin load errors [\#94](https://github.com/EventGhost/EventGhost/pull/94) ([blackwind](https://github.com/blackwind))
* Continue setup only if user data can be backed up [\#95](https://github.com/EventGhost/EventGhost/pull/95) ([blackwind](https://github.com/blackwind))


## [0.5.0-beta2](https://github.com/EventGhost/EventGhost/releases/tag/v0.5.0-beta2) (2016-08-14)

**Fixed bugs:**

* Show update notification for new releases only [\#81](https://github.com/EventGhost/EventGhost/pull/81) ([blackwind](https://github.com/blackwind))
* Change directory to `eg.configDir` only if it exists [\#86](https://github.com/EventGhost/EventGhost/pull/86) ([blackwind](https://github.com/blackwind))
* Prevent hang on system resume when `eg.app.Restart()` is called [\#87](https://github.com/EventGhost/EventGhost/pull/87) ([blackwind](https://github.com/blackwind))


## [0.5.0-beta1](https://github.com/EventGhost/EventGhost/releases/tag/v0.5.0-beta1) (2016-08-12)

**Important changes for plugin developers:**

* Migrate from `PIL` to `Pillow` [\#27](https://github.com/EventGhost/EventGhost/pull/27) ([blackwind](https://github.com/blackwind))
* Upgrade to `wxPython` 3.0 [\#35](https://github.com/EventGhost/EventGhost/pull/35) ([topic2k](https://github.com/topic2k))
* Deprecate `eg.revision`, remove previously deprecated items [\#50](https://github.com/EventGhost/EventGhost/pull/50) ([blackwind](https://github.com/blackwind))
* Parse documents starting with "\<md\>" as Markdown [\#59](https://github.com/EventGhost/EventGhost/pull/59) ([blackwind](https://github.com/blackwind))

**Enhancements:**

* Upgrade to Python 2.7 [\#8](https://github.com/EventGhost/EventGhost/pull/8) ([topic2k](https://github.com/topic2k))
* Search for modules in `[python-install]\Lib\site-packages` and `%PYTHONPATH%` [\#20](https://github.com/EventGhost/EventGhost/pull/20) ([blackwind](https://github.com/blackwind))
* Preserve view settings when switching versions [\#21](https://github.com/EventGhost/EventGhost/pull/21) ([blackwind](https://github.com/blackwind))
* Restore changelog panel in about dialog [\#22](https://github.com/EventGhost/EventGhost/pull/22) ([blackwind](https://github.com/blackwind))
* Refresh environment variables automatically or via action [\#24](https://github.com/EventGhost/EventGhost/pull/24) ([blackwind](https://github.com/blackwind))
* Add File \> Restart menuitem [\#32](https://github.com/EventGhost/EventGhost/pull/32) ([blackwind](https://github.com/blackwind))
* Add hotkeys to most menuitems [\#33](https://github.com/EventGhost/EventGhost/pull/33) ([blackwind](https://github.com/blackwind))
* Support wildcard patterns in event bindings [\#46](https://github.com/EventGhost/EventGhost/pull/46) ([blackwind](https://github.com/blackwind))
* Calculate "Python Script" indent size from script [\#48](https://github.com/EventGhost/EventGhost/pull/48) ([blackwind](https://github.com/blackwind))
* Replay events via log control's context menu [\#49](https://github.com/EventGhost/EventGhost/pull/49) ([blackwind](https://github.com/blackwind))
* Restore automatic and manual update checking [\#51](https://github.com/EventGhost/EventGhost/pull/51) ([topic2k](https://github.com/topic2k))
* Add option to hide system tray icon [\#62](https://github.com/EventGhost/EventGhost/pull/62) ([blackwind](https://github.com/blackwind))
* Disable log scrolling automatically when not at bottom [\#64](https://github.com/EventGhost/EventGhost/pull/64) ([blackwind](https://github.com/blackwind))
* Integrate useful debug menu functionality into core [\#67](https://github.com/EventGhost/EventGhost/pull/67) ([blackwind](https://github.com/blackwind))

**Fixed bugs:**

* \[Lirc\] Prevent an exception if no device is connected [\#29](https://github.com/EventGhost/EventGhost/pull/29) ([topic2k](https://github.com/topic2k))
* \[MceRemote\_Vista\] Prevent an exception if no device is connected [\#30](https://github.com/EventGhost/EventGhost/pull/30) ([topic2k](https://github.com/topic2k))
* \[Speech\] Prevent an infinite loop on configuration reload [\#54](https://github.com/EventGhost/EventGhost/pull/54) ([blackwind](https://github.com/blackwind))
