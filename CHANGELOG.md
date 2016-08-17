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
