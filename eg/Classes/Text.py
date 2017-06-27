# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import os

# Local imports
import eg
from eg.Utils import SetDefault

class Default:
    class General:
        configTree = "Configuration Tree"
        deleteQuestion = "Are you sure you want to delete this item?"
        deleteManyQuestion = (
            "This element has %s subelements.\n\n"
            "Are you sure you want to delete them all?"
        )
        deletePlugin = (
            "This plugin is used by actions in your configuration. You "
            "cannot remove it before all actions that are using this plugin "
            "have been removed."
        )
        deleteLinkedItems = (
            "At least one item outside your selection refers to an "
            "item inside your selection. If you continue to delete "
            "this selection, the referring item won't work properly "
            "anymore.\n\n"
            "Are you sure you want to delete the selection?"
        )
        ok = "OK"
        cancel = "Cancel"
        apply = "&Apply"
        yes = "&Yes"
        no = "&No"
        help = "&Help"
        choose = "Choose"
        browse = "Browse..."
        test = "&Test"
        pluginLabel = "Plugin: %s"
        autostartItem = "Autostart"
        unnamedFolder = "<unnamed folder>"
        unnamedMacro = "<unnamed macro>"
        unnamedEvent = "<unnamed event>"
        unnamedFile = "<unnamed file>"
        #moreTag = "more..."
        supportSentence = "Support for this plugin can be found"
        supportLink = "here"
        settingsPluginCaption = "Plugin Item Settings"
        settingsActionCaption = "Action Item Settings"
        settingsEventCaption = "Event Item Settings"
        noOptionsAction = "This action has no options to configure."
        noOptionsPlugin = "This plugin has no options to configure."
        monitorsLabel = "Identified monitors:"
        monitorsHeader = (
            "Monitor nr.",
            "X coordinate",
            "Y coordinate",
            "Width",
            "Height",
        )

        smartSpinMenu = (
            'Change control to "Spin Num"',
            'Change control to "Text" with {eg.result}',
            'Change control to "Text" with {eg.event.payload}',
            'Change control to (empty) "Text"'
        )
        smartSpinTooltip = (
            "Use the right mouse button\n"
            "to open the context menu!"
        )

    class Error:
        FileNotFound = "File \"%s\" couldn't be found."
        InAction = 'Error in Action: "%s"'
        pluginNotActivated = 'Plugin "%s" is not activated'
        pluginStartError = "Error starting plugin: %s"
        pluginLoadError = "Error loading plugin file: %s"
        configureError = "Error while configuring: %s"

    class Plugin:
        pass

    class MainFrame:
        onlyLogAssigned = "&Log only assigned and activated events"
        onlyLogAssignedToolTip = (
            "If checked, the log will only show events that would actually\n"
            "execute in the current configuration, so you should uncheck\n"
            "this when you want to assign new events."
        )

        class TaskBarMenu:
            Show = "&Show EventGhost"
            Hide = "&Hide EventGhost"
            Exit = "E&xit"

        class Menu:
            FileMenu = "&File"
            New = "&New"
            Open = "&Open..."
            Save = "&Save"
            SaveAs = "Save &As..."
            Options = "O&ptions..."
            Restart = "&Restart"
            RestartAsAdmin = "Restart as Administrator"
            Exit = "E&xit"

            EditMenu = "&Edit"
            Undo = "&Undo"
            Redo = "&Redo"
            Cut = "Cu&t"
            Copy = "&Copy"
            Python = "Copy as P&ython"
            Paste = "&Paste"
            Delete = "&Delete"
            SelectAll = "Select &All"
            Find = "&Find..."
            FindNext = "Find &Next"

            ViewMenu = "&View"
            HideShowToolbar = "&Toolbar"
            ExpandAll = "&Expand All"
            CollapseAll = "&Collapse All"
            ExpandOnEvents = "Select on E&xecution"
            LogMacros = "Log &Macros"
            LogActions = "Log &Actions"
            LogDebug = "Log &Debug Info"
            IndentLog = "&Indent Log"
            LogTime = "Time&stamp Log"
            ClearLog = "Clear &Log"

            ConfigurationMenu = "&Configuration"
            AddPlugin = "Add Plugin..."
            AddFolder = "Add Folder"
            AddMacro = "Add Macro..."
            AddEvent = "Add Event..."
            AddAction = "Add Action..."
            Configure = "Configure Item"
            Rename = "Rename Item"
            Execute = "Execute Item"
            Disabled = "Disable Item"

            HelpMenu = "&Help"
            HelpContents = "&Help Contents"
            WebHomepage = "Home &Page"
            WebForum = "Support &Forums"
            WebWiki = "&Wiki"
            PythonShell = "P&ython Shell"
            WIT = "Widget Inspection Tool"
            CheckUpdate = "Check for &Updates..."
            About = "&About EventGhost..."

            Apply = "&Apply Changes"
            Close = "&Close"
            Export = "&Export..."
            Import = "&Import..."
            Replay = "&Replay"
            Reset = "&Reset"

        class SaveChanges:
            mesg = (
                "Configuration contains unsaved changes.\n\n"
                "Do you want to save before continuing?"
            )
            saveButton = "&Save"
            dontSaveButton = "Do&n't Save"

        class Logger:
            caption = "Log"
            welcomeText = "---> Welcome to EventGhost <---"

        class Tree:
            caption = "Configuration"

        class Messages:
            cantAddEvent = (
                "Events can only be added to macros."
            )
            cantAddAction = (
                "Actions can only be added to macros and Autostart."
            )
            cantDisable = (
                "The root item and Autostart can't be disabled."
            )
            cantRename = (
                "The root item, Autostart, and plugins can't be renamed."
            )
            cantExecute = (
                "The root item, folders, and events can't be executed."
            )
            cantConfigure = (
                "Only plugins, events, and actions can be configured."
            )


def Text(language):
    class Translation(Default):
        pass
    languagePath = os.path.join(eg.languagesDir, "%s.py" % language)
    try:
        eg.ExecFile(languagePath, {}, Translation.__dict__)
    except IOError:
        pass
    SetDefault(Translation, Default)
    return Translation
