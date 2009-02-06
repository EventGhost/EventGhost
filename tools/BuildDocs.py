import os
import sys
import re
import _winreg
import subprocess
import shutil
from os.path import join

MY_DIR = os.path.dirname(__file__)
MAIN_DIR = os.path.abspath(join(MY_DIR, ".."))
DOCS_MAIN_DIR = join(MAIN_DIR, "docs")
DOCS_SOURCE_DIR = join(DOCS_MAIN_DIR, "source")
DOCS_HTML_BUILD_DIR = join(DOCS_MAIN_DIR, "html")
DOCS_CHM_BUILD_DIR = join(DOCS_MAIN_DIR, "chm")


sys.path.append(MAIN_DIR)
STDERR = sys.stderr
STDOUT = sys.stdout
try:
    import eg
finally:
    sys.stderr = STDERR
    sys.stdout = STDOUT
from eg.Utils import GetFirstParagraph


def GetHtmlHelpCompilerPath():
    """ 
    Try to find the install location of the HTML Help command line compiler
    """
    subkey = r"Software\Microsoft\HTML Help Workshop"
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, subkey)
        path = _winreg.QueryValueEx(key, "InstallDir")[0]
    except WindowsError:
        path = join(os.environ["PROGRAMFILES"], "HTML Help Workshop")
    programPath = join(path, "hhc.exe")
    if not os.path.exists(programPath):
        return None
    return programPath
    
    
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
        if os.path.exists(info.path + "\\" + "noinclude"):
            continue
        if info.kind in groups:
            groups[info.kind].append(info)
        else:
            groups[info.kind] = [info]
        numPlugins += 1
    
    outfile = open(filepath, "wt")
    outfile.write(".. This file is automatically created. Don't edit it!\n\n")
    outfile.write(".. _pluginlist:\n\n")
    outfile.write("List of Plugins\n")
    outfile.write("===============\n\n")
    outfile.write("This is the list of the %d plugins " % numPlugins)
    outfile.write("currently distributed with EventGhost ")
    outfile.write("%s:\n\n" % eg.Version.string)
    replacementId = 1
    for kind, kindDesciption in kindList:
        outfile.write("%s\n" % kindDesciption)
        outfile.write(79 * "-" + "\n\n")
        groups[kind].sort(key=lambda x: x.name)
        for info in groups[kind]:
            description = GetFirstParagraph(info.description)
            description = re.sub(
                r'<a\s+.*href=["\']http://(.*?)["\']>\s*((\n|.)+?)\s*</a>',
                r'`\2 <http://\1>`_',
                description
            )
            if info.url:
                outfile.write("|%s Plugin|_\n" % info.name)
            else:
                outfile.write("**%s**\n" % info.name)
            outfile.write("   %s\n\n" % description)
            if info.url:
                outfile.write(".. |%s Plugin| replace:: **%s**\n" % 
                    (info.name, info.name)
                )
                outfile.write(".. _%s Plugin: %s\n\n" % 
                    (info.name, info.url)
                )
            replacementId += 1
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

def Main(buildHtml=True, buildChm=False):
    import sphinx
    WritePluginList(join(DOCS_SOURCE_DIR, "pluginlist.rst"))
    filepath = join(DOCS_SOURCE_DIR, "eg", "classes.txt")
    outfile = open(filepath, "wt")
    outfile.write(CreateClsDocs(MAIN_CLASSES))
    outfile.close()
    filepath = join(DOCS_SOURCE_DIR, "eg", "gui_classes.txt")
    outfile = open(filepath, "wt")
    outfile.write(CreateClsDocs(GUI_CLASSES))
    outfile.close()
    if buildHtml:
        sphinx.main([
            None,
            #"-a",
            "-b", "html",
            #"-E",
            "-D", "release=%s" % eg.Version.string,
            "-d", join(DOCS_MAIN_DIR, ".doctree"),
            DOCS_SOURCE_DIR,
            DOCS_HTML_BUILD_DIR,
        ])
    
    if buildChm:
        sphinx.main([
            None,
            #"-a",
            "-b", "htmlhelp",
            "-E",
            "-D", "release=%s" % eg.Version.string,
            "-d", join(DOCS_MAIN_DIR, ".doctree"),
            DOCS_SOURCE_DIR,
            DOCS_CHM_BUILD_DIR,
        ])
        
        htmlHelpCompilerPath = GetHtmlHelpCompilerPath()
        if htmlHelpCompilerPath is None:
            raise Exception(
                "HTML Help Workshop command line compiler not found"
            )
        hhpPath = join(DOCS_CHM_BUILD_DIR, "EventGhost.hhp")
        from InnoInstaller import StartProcess
        StartProcess(htmlHelpCompilerPath, hhpPath)
        shutil.copy(join(DOCS_CHM_BUILD_DIR, "EventGhost.chm"), MAIN_DIR)
    
    
def Cli(argv):
    buildHtml = False
    buildChm = False
    for arg in argv[1:]:
        if arg == "chm":
            buildChm = True
        elif arg == "html":
            buildHtml = True
    Main(buildHtml, buildChm)
    
    
if __name__ == "__main__":
    Cli(sys.argv)