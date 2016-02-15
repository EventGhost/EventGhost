# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from os.path import join, exists
import eg


class RegisterPluginException(Exception):
    """
    RegisterPlugin will raise this exception to interrupt the loading
    of the plugin module file.
    """
    pass



class PluginModuleInfo(object):
    """
    Holds information of a plugin module.

    The main purpose of this class is to get the information from the
    eg.RegisterPlugin call inside the plugin module. So it imports the main
    module, but stops the import immediately after the eg.RegisterPlugin call.
    """
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
    hardwareId = ""


    def __init__(self, path):
        self.path = path
        self.pluginName = os.path.basename(path)
        originalRegisterPlugin = eg.RegisterPlugin
        eg.RegisterPlugin = self.RegisterPlugin
        sys.path.insert(0, self.path)
        try:
            if self.path.startswith(eg.corePluginDir):
                moduleName = "eg.CorePluginModule." + self.pluginName
            else:
                moduleName = "eg.UserPluginModule." + self.pluginName
            if moduleName in sys.modules:
                del sys.modules[moduleName]
            __import__(moduleName, None, None, [''])
        except RegisterPluginException:
            # It is expected that the loading will raise
            # RegisterPluginException because eg.RegisterPlugin() is called
            # inside the module
            pass
        except:
            eg.PrintTraceback(eg.text.Error.pluginLoadError % self.path)
        finally:
            del sys.path[0]
            eg.RegisterPlugin = originalRegisterPlugin


    if eg.debugLevel:
        def __setattr__(self, name, value):
            if not hasattr(self.__class__, name):
                raise AttributeError(
                    "%s has no attribute %s" % (self.__class__.__name__, name)
                )
            object.__setattr__(self, name, value)


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
        hardwareId = "",
        **kwargs
    ):
        if name is None:
            name = self.pluginName
        if description is None:
            description = name
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
        self.url = unicode(url) if url else url # Added by Pako # ??? by topic2k
        self.guid = guid.upper()
        if not guid:
            eg.PrintDebugNotice("missing guid in plugin: %s" % self.path)
            self.guid = self.pluginName
        self.hardwareId = hardwareId.upper()
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

