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

import argparse
import logging
import os
import sys
import tempfile
import threading
from os.path import abspath, dirname, exists, join

# Local imports
import builder
from builder import VirtualEnv
from builder.Logging import LogToFile
from builder.Utils import (
    GetGitHubConfig, GetVersion, Is64bitInterpreter, IsCIBuild
)


logger = logging.getLogger()


class Task(object):
    value = None
    visible = True
    enabled = True
    activated = True

    def __init__(self, buildSetup):
        self.buildSetup = buildSetup

    def Setup(self):
        pass

    def DoTask(self):
        raise NotImplementedError

    @classmethod
    def GetId(cls):
        return cls.__module__ + "." + cls.__name__

    def Print(self, *args):
        logger.log(22, " ".join(args))


class Builder(object):
    def __init__(self):
        if not VirtualEnv.Running() and VirtualEnv.Exists():
            VirtualEnv.Activate()

        global buildSetup
        Task.buildSetup = self
        buildSetup = self

        self.pyVersionStr = "%d%d" % sys.version_info[:2]
        self.buildDir = abspath(join(dirname(__file__), ".."))
        self.sourceDir = abspath(join(self.buildDir, ".."))
        self.libraryName = "lib%s" % self.pyVersionStr
        self.libraryDir = join(self.sourceDir, self.libraryName)
        self.dataDir = join(self.buildDir, "data")
        self.docsDir = join(self.dataDir, "docs")
        self.pyVersionDir = join(self.dataDir, "Python%s" % self.pyVersionStr)
        self.outputDir = join(self.buildDir, "output")
        self.websiteDir = join(self.outputDir, "website")

        if Is64bitInterpreter():
            print(
                "ERROR: Sorry, EventGhost can't be built with the 64-bit "
                "version of Python!"
            )
            sys.exit(1)
        elif not exists(self.pyVersionDir):
            print(
                "ERROR: Sorry, EventGhost can't be built with Python %d.%d!"
                % sys.version_info[:2]
            )
            sys.exit(1)

        sys.path.append(self.sourceDir)
        sys.path.append(join(self.libraryDir, "site-packages"))

        self.args = self.ParseArgs()
        self.showGui = not (
            self.args.build or
            self.args.check or
            self.args.package or
            self.args.release or
            self.args.sync
        )
        if os.environ.get(
                "APPVEYOR_REPO_COMMIT_MESSAGE", ""
        ).upper().startswith("VERBOSE:"):
            self.args.verbose = True

        os.chdir(self.buildDir)

        if not exists(self.outputDir):
            os.mkdir(self.outputDir)

        LogToFile(join(self.outputDir, "Build.log"), self.args.verbose)

        from CheckDependencies import CheckDependencies
        if not CheckDependencies(self):
            sys.exit(1)

        try:
            self.gitConfig = GetGitHubConfig()
        except Exception as e:
            msg = (
                "WARNING: To change version or release to GitHub, you must:\n"
                "    $ git config --global github.user <your github username>\n"
                "    $ git config --global github.token <your github token>\n"
                "To create a token, go to: https://github.com/settings/tokens\n"
            )
            if type(e) is ValueError:
                msg = "WARNING: Specified `github.token` is invalid!\n" + msg
            if not IsCIBuild():
                token = ""
                print msg
            else:
                token = os.environ["GITHUB_TOKEN"]
            self.gitConfig = {
                "all_repos": {
                    "EventGhost/EventGhost": {
                        "all_branches": ["master"],
                        "def_branch": "master",
                        "name": "EventGhost",
                    },
                },
                "branch": "master",
                "repo": "EventGhost",
                "repo_full": "EventGhost/EventGhost",
                "token": token,
                "user": "EventGhost",
            }

        self.appVersion = None
        self.appVersionInfo = None
        self.tmpDir = tempfile.mkdtemp()
        self.appName = self.name

    def ParseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-b", "--build",
            action="store_true",
            help="build imports, lib%s, and interpreters" % self.pyVersionStr,
        )
        parser.add_argument(
            "-c", "--check",
            action="store_true",
            help="check source code for issues",
        )
        parser.add_argument(
            "-m", "--make-env",
            action="store_true",
            help="auto-install dependencies into a virtualenv",
        )
        parser.add_argument(
            "-p", "--package",
            action="store_true",
            help="build changelog, docs, and setup.exe",
        )
        parser.add_argument(
            "-r", "--release",
            action="store_true",
            help="release to github and web if credentials available",
        )
        parser.add_argument(
            "-s", "--sync",
            action="store_true",
            help="build and synchronize website",
        )
        parser.add_argument(
            "-d", "--docs",
            action="store_true",
            help="build and synchronize usr and dev docs",
        )
        parser.add_argument(
            "-u", "--url",
            dest="websiteUrl",
            default='',
            type=str,
            help="sftp url for doc synchronizing",
        )
        parser.add_argument(
            "-vv", "--verbose",
            action="store_true",
            help="give a more verbose output",
        )
        parser.add_argument(
            "-v", "--version",
            action="store",
            help="package as the specified version",
        )
        return parser.parse_args()

    def Start(self):
        from Tasks import TASKS
        self.tasks = [task(self) for task in TASKS]
        from Config import Config
        self.config = Config(self, join(self.outputDir, "Build.ini"))
        for task in self.tasks:
            task.Setup()
        (self.appVersion, self.appVersionInfo) = GetVersion(self)
        if self.showGui:
            import Gui
            Gui.Main(self)
        else:
            thread = threading.Thread(target=builder.Tasks.Main, args=[self])
            thread.start()
