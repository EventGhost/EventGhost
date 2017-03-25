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
