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

import sys
import tempfile
import atexit
import shutil
from os.path import abspath, dirname, join
from builder.Utils import DecodePath

class Task(object):
    value = None
    visible = True
    enabled = True
    activated = True

    def __init__(self, buildSetup):
        self.buildSetup = buildSetup


    def Setup(self):
        pass

    @classmethod
    def GetId(cls):
        return cls.__module__ + "." + cls.__name__

    def DoTask(self):
        raise NotImplementedError



class Builder(object):

    def __init__(self):
        from CheckDependencies import CheckDependencies
        global buildSetup
        Task.buildSetup = self
        buildSetup = self
        baseDir = dirname(DecodePath(__file__))
        self.sourceDir = abspath(join(baseDir, "../.."))
        self.websiteDir = join(self.sourceDir, "website")
        self.dataDir = abspath(join(baseDir, "Data"))
        self.pyVersionStr = "%d%d" % sys.version_info[:2]
        self.pyVersionDir = join(self.dataDir, "Python%s" % self.pyVersionStr)
        self.libraryName = "lib%s" % self.pyVersionStr
        self.libraryDir = join(self.sourceDir, self.libraryName)
        self.outDir = abspath(join(self.sourceDir, ".."))
        if not CheckDependencies(self):
            sys.exit(1)
        self.tmpDir = tempfile.mkdtemp()
        #atexit.register(shutil.rmtree, self.tmpDir)
        self.appName = self.name


    def RunGui(self):
        from builder.Tasks import TASKS
        self.tasks = [task(self) for task in TASKS]
        from builder.Config import Config
        self.config = Config(self, join(self.dataDir, "Build.ini"))
        for task in self.tasks:
            task.Setup()
        import builder.Gui
        builder.Gui.Main(self)

