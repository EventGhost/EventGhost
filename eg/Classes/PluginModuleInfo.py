# This file is part of EventGhost.
# Copyright (C) 2009 Lars-Peter Voss <bitmonster@eventghost.org>
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

import os
import sys
from os.path import join, exists
import eg
from eg.Utils import DecodeReST


class RegisterPluginException(Exception):
    """
    RegisterPlugin will raise this exception to interrupt the loading
    of the plugin module file.
    """
    pass



class PluginModuleInfo(object):
    _guids = {}
    
    name = u"unknown"
    description = u""
    author = u"unknown author"
    version = u"unknown version"
    kind = u"other"
    guid = ""
    canMultiLoad = False
    createMacrosOnAdd = False
    icon = eg.Icons.PLUGIN_ICON
    url = None
    englishName = None
    englishDescription = None
    path = None
    pluginName = None
    

    def __init__(self, path):
        self.path = path
        self.pluginName = os.path.basename(path)
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
                raise AttributeError(
                    "PluginModuleInfo has no attribute %s" % name
                )
            object.__setattr__(self, name, value)


    def Import(self):
        if self.path.startswith(eg.PLUGIN_DIR):
            moduleName = "eg.PluginModule." + self.pluginName
        else:
            moduleName = "eg.UserPluginModule." + self.pluginName
        if moduleName in sys.modules:
            return sys.modules[moduleName]
        module = __import__(moduleName, None, None, [''])
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
        guid = "",
        **kwargs
    ):
        if name is None:
            name = self.pluginName
        if description is None:
            description = name
#        else:
#            pos = description.find("<rst>")
#            if pos != -1:
#                description = DecodeReST(description[pos+5:])
        if help is not None:
            help = "\n".join([s.strip() for s in help.splitlines()])
            help = help.replace("\n\n", "<p>")
            description += "\n\n<p>" + help
        self.name = self.englishName = unicode(name)
        self.description = self.englishDescription = unicode(description)
        self.kind = unicode(kind)
        self.author = unicode(author)
        self.version = unicode(version)
        self.canMultiLoad = canMultiLoad
        self.createMacrosOnAdd = createMacrosOnAdd
        self.url = unicode(url)
        self.guid = guid.upper()
        if not guid:
            print "missing guid", self.path
        else:
            if guid in self._guids:
                print "duplicate guid", self.path
            else:
                self._guids[guid] = self
        # get the icon if any
        if icon is not None:
            self.icon = eg.Icons.StringIcon(icon)
        else:
            iconPath = join(self.path, "icon.png")
            if exists(iconPath):
                self.icon = eg.Icons.PathIcon(iconPath)
                
        # try to translate name and description
        textCls = getattr(eg.text.Plugin, self.pluginName, None)
        if textCls is not None:
            self.name = getattr(textCls, "name", name)
            self.description = getattr(textCls, "description", description)

        # we are done with this plugin module, so we can interrupt further
        # processing by raising RegisterPluginException
        raise RegisterPluginException

