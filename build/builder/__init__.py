# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import tempfile
import shutil
import stat
import pygit2
import sys
from os import chmod, mkdir
from os.path import abspath, dirname, join, exists, isdir
from Utils import GetRevision, DecodePath


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
        repoDir = pygit2.discover_repository(self.sourceDir)
        self.repo = pygit2.Repository(repoDir)
        self.branchFullname = self.repo.head.name
        #self.appRevision = None
        if not CheckDependencies(self):
            sys.exit(1)
        self.tmpDir = tempfile.mkdtemp()
        self.appName = self.name

    def RunGui(self):
        from Tasks import TASKS
        self.tasks = [task(self) for task in TASKS]
        from Config import Config
        self.config = Config(self, join(self.dataDir, "Build.ini"))
        for task in self.tasks:
            task.Setup()
        import Gui
        GetRevision(self)
        Gui.Main(self)

