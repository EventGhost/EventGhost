class Text:
    class General:
        configTree = "Configuration Tree"
        deleteQuestion = \
            "Are you sure you want to delete this item?"
        deleteManyQuestion = \
            "This element has %s subelements.\n"\
            "Are you sure you want to delete them all?"
        deletePlugin = \
            "This plugin is used by actions in your configuration.\n"\
            "You cannot remove it before all actions that are using this plugin "\
            "have been removed."
        deleteLinkedItems = (
            "At least one item outside your selection refers to an "
            "item inside your selection. If you continue to delete "
            "this selection, the referring item won't properly work "
            "anymore.\n\n"
            "Are you sure you want to delete the selection?")
        ok = "OK"
        cancel = "Cancel"
        help = "&Help"
        choose = "Choose"
        browse = "Browse..."
        pluginLabel = "Plugin: %s"
        autostartItem = "Autostart"
        unnamedFolder = "<unnamed folder>"
        unnamedMacro = "<unnamed macro>"
        unnamedEvent = "<unnamed event>"
        unnamedFile = "<unnamed file>"
        moreHelp = "More help"
        noOptionsAction = "This action has no options to configure."
        noOptionsPlugin = "This plugin has no options to configure."

    class Error:
        FileNotFound = "File \"%s\" couldn't be found."
        InAction = 'Error in Action: "%s"'
        InScript = 'Error in Script: "%s"'
        pluginNotActivated = 'Plugin "%s" is not activated'
        pluginStartError = "Error starting plugin: %s"
        
    class Plugin:
        pass

    
    class MainFrame:
        onlyLogAssigned = "Log only assigned and activated events"
        
        class TaskBarMenu:
            Show = "Show EventGhost"
            Hide = "Hide EventGhost"
            Exit = "Exit"
            
        class Menu:
            FileMenu = "&File"
            Apply = "&Apply Changes"
            New = "&New"
            Open = "&Open..."
            Save = "&Save"
            SaveAs = "Save &As..."
            Export = "Export..."
            Import = "Import..."
            Close = "&Close"
            Options = "&Options..."
            Exit = "E&xit"
            
            EditMenu = "&Edit"
            Undo = "&Undo"
            Redo = "&Redo"
            Cut = "Cu&t"
            Copy = "&Copy"
            Paste = "&Paste"
            Delete = "&Delete"
            ClearAll = "Clear All"
            SelectAll = "Select &All"
            AddPlugin = "Add Plugin"
            NewFolder = "Add Folder"
            NewMacro = "Add Macro"
            NewEvent = "Add Event"
            NewAction = "Add Action"
            Edit = "Configure Item"
            Rename = "Rename Item"
            Disabled = "Disable Item"
            Execute = "Execute Item"
            Find = "&Find..."
            FindNext = "Find &Next"

            ViewMenu = "View"
            HideShowToolbar = "Toolbar"
            CollapseAll = "&Collapse All"
            ExpandAll = "&Expand All"
            ExpandOnEvents = "Autom. highlight on event"
            ExpandTillMacro = "Autom. expand only till macro"
            LogActions = "Log Actions"
            LogTime = "Log Times"
            
            ConfigurationMenu = "&Configuration"
            
            HelpMenu = "&Help"
            About = "&About EventGhost..."
            WebHomepage = "EventGhost Homepage"
            WebForum = "Support Forum"
            WebWiki = "Wiki"
            CheckUpdate = "Check for newest version..."
            Reset = "Reset"
            
        class SaveChanges:
            title = "Save changes?"
            mesg = "The file was altered.\n\nDo you want to save the changes?\n"

        class Logger:
            caption = "Log"
            timeHeader = "Time"
            descriptionHeader = "Description"
            welcomeText = "---> Welcome to EventGhost <---"
            
        class Tree:
            caption = "Configuration"
            