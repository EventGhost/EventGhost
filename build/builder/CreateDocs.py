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

import os
import sys
import re
import shutil
import codecs
import warnings
from os.path import join

import sphinx

import builder
from builder.Utils import StartProcess, GetHtmlHelpCompilerPath, EncodePath


MAIN_DIR = builder.buildSetup.sourceDir
DOCS_SOURCE_DIR = join(MAIN_DIR, "build", "docs")

sys.path.append(EncodePath(MAIN_DIR))
import eg
from eg.Utils import GetFirstParagraph



def WritePluginList(filepath):
    kindList = [
        ("core", "Essential (always loaded)"),
        ("remote",  "Remote Receiver"),
        ("program", "Program Control"),
        ("external", "External Hardware Equipment"),
        ("other", "Other"),
    ]
    numPlugins = 0
    groups = {}
    for info in eg.pluginManager.GetPluginInfoList():
        if os.path.exists(join(info.path, "noinclude")):
            continue
        if info.kind in groups:
            groups[info.kind].append(info)
        else:
            groups[info.kind] = [info]
        numPlugins += 1

    outfile = codecs.open(filepath, "w", "utf-8")
    outfile.write(".. This file is automatically created. Don't edit it!\n\n")
    outfile.write(".. _pluginlist:\n\n")
    outfile.write("List of Plugins\n")
    outfile.write("===============\n\n")
    outfile.write("This is the list of the %d plugins " % numPlugins)
    outfile.write("currently distributed with EventGhost ")
    outfile.write("%s:\n\n" % eg.Version.base)
    for kind, kindDesciption in kindList:
        outfile.write("%s\n" % kindDesciption)
        outfile.write(79 * "-" + "\n\n")
        groups[kind].sort(key=lambda x: x.name)
        for info in groups[kind]:
            description = GetFirstParagraph(info.description)
            description = re.sub(
                r'<a\s+.*?href=["\']http://(.*?)["\']>\s*((\n|.)+?)\s*</a>',
                r'`\2 <http://\1>`_',
                description
            )
            if info.url:
                outfile.write("|%s Plugin|_\n" % info.name)
            else:
                outfile.write("**%s**\n" % info.name)
            outfile.write(u"   %s\n\n" % description)
            if info.url:
                outfile.write(".. |%s Plugin| replace:: **%s**\n" %
                    (info.name, info.name)
                )
                outfile.write(".. _%s Plugin: %s\n\n" %
                    (info.name, info.url)
                )
    outfile.close()


def GetFirstTextParagraph(text):
    res = []
    for line in text.lstrip().splitlines():
        line = line.strip()
        if line == "":
            break
        res.append(line)
    return " ".join(res)


def CreateClsDocs(clsNames):
    res = []
    for clsName in clsNames:
        if clsName.startswith("-"):
            clsName = clsName[1:]
            addCls = False
        else:
            addCls = True
        fullClsName = "eg." + clsName
        cls = getattr(eg, clsName)
        if addCls:
            res.append("\nclass :class:`%s`" % fullClsName)
            if cls.__doc__:
                res.append("   %s" % GetFirstTextParagraph(cls.__doc__))
        filepath = join(DOCS_SOURCE_DIR, "eg", "%s.rst" % fullClsName)
        outfile = open(filepath, "wt")
        outfile.write("=" * len(fullClsName) + "\n")
        outfile.write(fullClsName + "\n")
        outfile.write("=" * len(fullClsName) + "\n")
        outfile.write("\n")
        outfile.write(".. currentmodule:: eg\n")
        outfile.write(".. autoclass:: %s\n" % fullClsName)
        outfile.write("   :members:\n")
        if hasattr(cls, "__docsort__"):
            outfile.write("      " + cls.__docsort__)
        outfile.write("\n")
    return "\n".join(res)


MAIN_CLASSES = [
    "PluginBase",
    "ActionBase",
    "SerialThread",
    "ThreadWorker",
    "ConfigPanel",
    "Bunch",
    "WindowMatcher",
    "-EventGhostEvent",
    "-Scheduler",
    "-ControlProviderMixin",
]

GUI_CLASSES = [
    "SpinIntCtrl",
    "SpinNumCtrl",
    "MessageDialog",
    "DisplayChoice",
    "SerialPortChoice",
    "FileBrowseButton",
    "DirBrowseButton",
    "FontSelectButton",
]


def Prepare():
    WritePluginList(join(DOCS_SOURCE_DIR, "pluginlist.rst"))

    filepath = join(DOCS_SOURCE_DIR, "eg", "classes.txt")
    outfile = open(filepath, "wt")
    outfile.write(CreateClsDocs(MAIN_CLASSES))
    outfile.close()

    filepath = join(DOCS_SOURCE_DIR, "eg", "gui_classes.txt")
    outfile = open(filepath, "wt")
    outfile.write(CreateClsDocs(GUI_CLASSES))
    outfile.close()



class CreateHtmlDocs(builder.Task):
    description = "Build HTML docs"
    activated = False

    def DoTask(self):
        Prepare()
        sphinx.build_main([
            None,
            "-a",
            "-b", "html",
            "-E",
            "-P",
            "-D", "release=%s" % self.buildSetup.appVersion,
            "-d", join(self.buildSetup.tmpDir, ".doctree"),
            DOCS_SOURCE_DIR,
            join(self.buildSetup.sourceDir, "website", "docs"),
        ])



class CreateChmDocs(builder.Task):
    description = "Build CHM docs"

    def Setup(self):
        if os.path.exists(
            join(self.buildSetup.sourceDir, "EventGhost.chm")
        ):
            self.activated = False


    def DoTask(self):
        tmpDir = join(self.buildSetup.tmpDir, "chm")
        Prepare()
        #warnings.simplefilter('ignore', DeprecationWarning)
        sphinx.build_main([
            None,
            "-a",  # always write all output files
            "-b", "htmlhelp",
            "-E",  # Don’t use a saved environment (the structure
                   # caching all cross-references),
            "-P",  # (Useful for debugging only.) Run the Python debugger,
                    # pdb, if an unhandled exception occurs while building.
            "-D", "release=%s" % self.buildSetup.appVersion,
            "-D", "templates_path=[]",
            "-d", EncodePath(join(self.buildSetup.tmpDir, ".doctree")),
            EncodePath(DOCS_SOURCE_DIR),
            tmpDir,
        ])

        print "calling HTML Help Workshop compiler"
        htmlHelpCompilerPath = GetHtmlHelpCompilerPath()
        if htmlHelpCompilerPath is None:
            raise Exception(
                "HTML Help Workshop command line compiler not found"
            )
        hhpPath = join(tmpDir, "EventGhost.hhp")
        StartProcess(htmlHelpCompilerPath, hhpPath)
        try:
            shutil.copy(join(tmpDir, "EventGhost.chm"),
                        self.buildSetup.sourceDir)
        except IOError:
            print("ERROR: 'EventGhost.chm' couldn't be copied from temporary "
                  "folder ({0} to '{1}'".format(tmpDir,
                                               self.buildSetup.sourceDir))

