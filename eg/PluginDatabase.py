# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2007-05-30 08:12:13 +0200 (Mi, 30 Mai 2007) $
# $LastChangedRevision: 133 $
# $LastChangedBy: bitmonster $

import eg
import sys
import os
from os.path import isdir, join, exists, abspath
import cPickle as pickle
import imp

from PluginTools import _LoadPluginModule

class RegisterPluginDone(Exception):
    pass



class PluginFileInfo:

    def __init__(self, pluginDir):
        self.module = None
        self.dirname = pluginDir
        old = eg.RegisterPlugin
        eg.SetAttr("RegisterPlugin", self.RegisterPlugin)
        try:
            try:
                module = _LoadPluginModule(self.dirname)
            finally:
                eg.SetAttr("RegisterPlugin", old)
        except RegisterPluginDone:
            return
        except:
            eg.PrintTraceback(
                "Error while loading plugin-file %s." % self.dirname
            )
            return
        
        
    def RegisterPlugin(self, **kwargs):
        self.__dict__.update(kwargs)
        raise RegisterPluginDone
    
    
    def __getstate__(self):
        state = self.__dict__.copy()
        if "module" in state:
            del state["module"]
        return state
    
    
    def __repr__(self):
        return "\n".join(
            (
                "--------- PluginFileInfo --------",
                "Name: %r" % self.name,
                "PluginDir: %r" % self.dirname,
                "Author: %r" % self.author,
                "Version: %r" % self.version,
                "Kind: %r" % self.kind,
            )
        )
        
        
class PluginDatabase:
    
    @eg.TimeIt  
    def __init__(self, forceRebuild=False):
        """
        Scans the plugin directory to get all needed information for all 
        plugins.
        
        This will use a simple database file to avoid time consuming processing
        of unchanged plugins. If 'forceRebuild' is True, the old database file
        will be ignored and a new one completely rebuild.
        """
        
        # load the database file if exists
        databasePath = join(eg.APPDATA, eg.APP_NAME, "PluginDatabase")
        if not forceRebuild and exists(databasePath):
            databaseFile = open(databasePath, "rb")
            try:
                database = pickle.load(databaseFile)
            except:
                database = {}
            databaseFile.close()
        else:
            database = {}
            
        # a new database will be created at the end if a plugin has changed
        hasChanged = False
        newDatabase = {}
            
        # scan through all directories in the plugin directory
        for dirname in os.listdir(eg.PLUGIN_DIR):
            # filter out non-plugin names
            if dirname.startswith(".") or dirname.startswith("_"):
                continue
            pluginDir = join(eg.PLUGIN_DIR, dirname)
            if not isdir(pluginDir):
                continue
            
            # get the highest timestamp of all files in that directory
            highestTimestamp = 0
            for dirpath, dirnames, filenames in os.walk(pluginDir):
                for filename in filenames:
                    timestamp = os.stat(join(dirpath, filename)).st_mtime
                    highestTimestamp = max(highestTimestamp, timestamp)
                # little hack to avoid scanning of SVN directories
                for directory in dirnames[:]:
                    if directory.startswith(".svn"):
                        dirnames.remove(directory)
                    
            
            # if the highest timestamp doesn't differ from the database's one
            # we can skip further processing
            if dirname in database:
                if database[dirname].timestamp == highestTimestamp:
                    newDatabase[dirname] = database[dirname]
                    del database[dirname]
                    continue
            
            hasChanged = True
            pluginInfo = PluginFileInfo(dirname)
            pluginInfo.timestamp = highestTimestamp
            newDatabase[dirname] = pluginInfo
            #print repr(pluginInfo)
            
        # only save if something has changed
        if hasChanged or len(database):
            eg.Notice("writing new plugin database")
            databaseFile = open(databasePath, "wb")
            pickle.dump(newDatabase, databaseFile, -1)
            databaseFile.close()
        
        self.database = newDatabase
        
        
    def GetPluginInfo(self, pluginName):
        return self.database[pluginName]
