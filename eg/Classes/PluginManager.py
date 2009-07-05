# This file is part of EventGhost.
# Copyright (C) 2007 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

from __future__ import with_statement
import eg
import os
import sys
import cPickle as pickle
from os import stat
from os.path import isdir, join, exists
from types import ClassType



class RegisterPluginException(Exception):
    """
    RegisterPlugin will raise this exception to interrupt the loading
    of the plugin module file.
    """
    pass



class PluginModuleInfo(object):
    name = "unknown"
    description = ""
    author = "unknown author"
    version = "unknow version"
    kind = "other"
    canMultiLoad = False
    createMacrosOnAdd = False
    icon = eg.Icons.PLUGIN_ICON
    url = None
    englishName = None
    englishDescription = None
    path = None
    timestamp = None
    

    def __init__(self, path):
        self.path = path
        originalRegisterPlugin = eg.RegisterPlugin
        eg.RegisterPlugin = self.RegisterPlugin
        try:
            self.Import()
        except RegisterPluginException:
            # It is expected that the loading will raise RegisterPluginException
            # because RegisterPlugin is called inside the module
            pass
        except:
            eg.PrintTraceback(eg.text.Error.pluginLoadError % self.path)
        finally:
            eg.RegisterPlugin = originalRegisterPlugin
    
    
    if eg.debugLevel:
        def __setattr__(self, name, value):
            if not hasattr(self.__class__, name):
                raise AttributeError("PluginModuleInfo has no attribute %s" % name)
            object.__setattr__(self, name, value)


    def Import(self):
        dirname = os.path.basename(self.path)
        moduleName = "eg.PluginModule." + dirname
        if moduleName in sys.modules:
            return sys.modules[moduleName]
        sys.path.insert(0, self.path)
        try:
            module = __import__(moduleName, None, None, [''])
        finally:
            del sys.path[0]
        return module


    def RegisterPlugin(
        self,
        name = None,
        description = None,
        kind = "other",
        author = "unknown author",
        version = "unknown version",
        icon = None,
        canMultiLoad = False,
        createMacrosOnAdd = False,
        url = None,
        help = None,
        guid = None,
        #**kwargs
    ):
        """
        Registers information about a plugin to EventGhost.

        :param name: should be a short descriptive string with the name of the
           plugin.
        :param description: the description of the plugin.
        :param kind: gives a hint about the category the plugin belongs to. It
           should be a string with a value out of "remote" (for remote receiver
           plugins), "program" (for program control plugins), "external" (for
           plugins that control external hardware) or "other" (if none of the
           other categories match).
        :param author: can be set to the name of the developer of the plugin.
        :param version: can be set to a version string.
        :param canMultiLoad: set this to ``True``, if a configuration can have
           more than one instance of this plugin.
        :param \*\*kwargs: just to consume unknown parameters, to make the call
           backward compatible.
        """
        if name is None:
            name = info.dirname
        if description is None:
            description = name
        if help is not None:
            help = "\n".join([s.strip() for s in help.splitlines()])
            help = help.replace("\n\n", "<p>")
            description += "\n\n<p>" + help
        if guid:
            guid = guid.upper()
        self.name = self.englishName = name
        self.description = self.englishDescription = description
        self.kind = kind
        self.author = author
        self.version = version
        self.canMultiLoad = canMultiLoad
        self.url = url

        # get the icon if any
        if icon is not None:
            self.icon = eg.Icons.StringIcon(icon)
        else:
            iconPath = join(self.path, "icon.png")
            if exists(iconPath):
                self.icon = eg.Icons.PathIcon(iconPath)
                
        # try to translate name and description
        pluginName = os.path.basename(self.path)
        textCls = getattr(eg.text.Plugin, pluginName, None)
        if textCls is not None:
            self.name = getattr(textCls, "name", name)
            self.description = getattr(textCls, "description", description)

        # we are done with this plugin module, so we can interrupt further
        # processing by raising RegisterPluginException
        raise RegisterPluginException



class PluginClsInfo(PluginModuleInfo):
    cls = None
    
    @classmethod
    def FromModuleInfo(cls, moduleInfo):
        self = cls()
        self.__dict__.update(moduleInfo.__dict__)
        
        
    def ImportCls(self):
        pathname = join(self.path, "__init__.py")
        if not exists(pathname):
            eg.PrintError("File %s does not exist" % pathname)
            return False
        try:
            module = self.Import()
        except:
            eg.PrintTraceback(
                "Error while loading plugin-file %s." % self.path,
                1
            )
            return False
        cls = module.__pluginCls__
        self.module = module
        self.cls = cls
        defaultText = cls.text
        if defaultText is None:
            class defaultText:
                pass
        defaultText.name = self.englishName
        defaultText.description = self.englishDescription
        translationText = getattr(eg.text.Plugin, cls.__name__, None)
        if translationText is not None:
            SetDefault(translationText, defaultText)
            text = translationText
        else:
            setattr(eg.text.Plugin, cls.__name__, defaultText)
            text = defaultText

        cls.text = text
        cls.name = text.name
        cls.description = text.description
        eg.pluginClassInfo[cls.pluginName] = self
        return True



class PluginInstanceInfo(PluginClsInfo):
    pass


        
class PluginManager:

    # the PluginInfo currently been processed
    currentInfo = None

    def __init__(self):
        if not exists(eg.userPluginDir):
            os.mkdir(eg.userPluginDir)
        self.databasePath = join(eg.configDir, "pluginManager")
        self.Refresh()


    @eg.TimeIt
    def Refresh(self, forceRebuild=(eg.debugLevel > 0)):
        """
        Scans the plugin directory to get all needed information for all
        plugins.

        This will use a simple database file to avoid time consuming processing
        of unchanged plugins. If 'forceRebuild' is True, the old database file
        will be ignored and a new one completely rebuild.
        """

        # load the database file if exists
        self.database = {}
        if not forceRebuild:
            self.Load()
        database = self.database

        # a new database will be created at the end if a plugin has changed
        hasChanged = False
        newDatabase = {}

        root = eg.PLUGIN_DIR
        # scan through all directories in the plugin directory
        for dirname in os.listdir(root):
            # filter out non-plugin names
            if dirname.startswith(".") or dirname.startswith("_"):
                continue
            pluginDir = join(root, dirname)
            if not isdir(pluginDir):
                continue
            if not exists(join(pluginDir, "__init__.py")):
                continue

            # get the highest timestamp of all files in that directory
            highestTimestamp = 0
            for dirpath, dirnames, filenames in os.walk(pluginDir):
                for filename in filenames:
                    timestamp = stat(join(dirpath, filename)).st_mtime
                    if timestamp > highestTimestamp:
                        highestTimestamp = timestamp
                # little hack to avoid scanning of unrelated directories
                for directory in dirnames[:]:
                    if directory.startswith("."):
                        dirnames.remove(directory)


            # if the highest timestamp doesn't differ from the database's one
            # we can use the old entry and skip further processing
            if dirname in database:
                if database[dirname].timestamp == highestTimestamp:
                    newDatabase[dirname] = database[dirname]
                    del database[dirname]
                    continue

            hasChanged = True
            pluginInfo = PluginClsInfo(pluginDir)
            if pluginInfo is None:
                print dirname
            else:
                pluginInfo.timestamp = highestTimestamp
                newDatabase[dirname] = pluginInfo
            #print repr(pluginInfo)

        # only save if something has changed
        needsSave = hasChanged or len(database)
        self.database = newDatabase
        if needsSave:
            self.Save()


    @eg.LogIt
    def Save(self):
        """
        Save the database to disc.
        """
        with file(self.databasePath, "wb") as databaseFile:
            pickle.dump(eg.Version.string, databaseFile, -1)
            pickle.dump(self.database, databaseFile, -1)


    def Load(self):
        """
        Load the database from disc.
        """
        if not exists(self.databasePath):
            return
        with file(self.databasePath, "rb") as databaseFile:
            try:
                version = pickle.load(databaseFile)
                if version != eg.Version.string:
                    eg.PrintDebugNotice("pluginManager version mismatch")
                    return
                self.database = pickle.load(databaseFile)
            except:
                eg.PrintTraceback()


    def GetPluginInfo(self, pluginName):
        # first look, if we already have cached this plugin class
        cachedInfo = eg.pluginClassInfo.get(pluginName, None)
        if cachedInfo:
            return cachedInfo

        if pluginName not in self.database:
            return None

        moduleInfo = self.database[pluginName]
        Info = ClassType("Info", (eg.PluginInfo,), moduleInfo.__dict__.copy())
        Info.baseInfo = moduleInfo
        Info.actionClassList = []
        Info.pluginName = pluginName
        return Info


    def GetPluginInfoList(self):
        """
        Get a list of all PluginInfo for all plugins in the plugin directory
        """
        infoList = self.database.values()
        infoList.sort(key=lambda x: x.name.lower())
        return infoList

