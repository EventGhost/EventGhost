import os
import sys
import re
import _winreg

MY_DIR = os.path.dirname(__file__)
MAIN_DIR = os.path.abspath(os.path.join(MY_DIR, ".."))
DOCS_MAIN_DIR = os.path.join(MAIN_DIR, "docs")
DOCS_SOURCE_DIR = os.path.join(DOCS_MAIN_DIR, "source")
DOCS_HTML_BUILD_DIR = os.path.join(DOCS_MAIN_DIR, "html")
DOCS_CHM_BUILD_DIR = os.path.join(DOCS_MAIN_DIR, "chm")


def ImportEg():
    sys.path.append(MAIN_DIR)
    stderr = sys.stderr
    stdout = sys.stdout
    try:
        import eg
    finally:
        sys.stderr = stderr
        sys.stdout = stdout
    return eg


def GetHtmlHelpCompilerPath():
    """ 
    Try to find the install location of the HTML Help command line compiler
    """
    subkey = r"Software\Microsoft\HTML Help Workshop"
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, subkey)
        path = _winreg.QueryValueEx(key, "InstallDir")[0]
    except WindowsError:
        path = os.path.join(os.environ["PROGRAMFILES"], "HTML Help Workshop")
    programPath = os.path.join(path, "hhc.exe")
    if not os.path.exists(programPath):
        return None
    return programPath
    
    
def WritePluginList(eg, filepath):
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
    outfile.write(".. _PluginList:\n\n")
    outfile.write("List of plugins\n")
    outfile.write("===============\n\n")
    outfile.write("This is the list of the %d plugins " % numPlugins)
    outfile.write("currently distributed with EventGhost beta ")
    outfile.write("%s:\n\n" % eg.Version.string)
    replacementId = 1
    for kind, kindDesciption in kindList:
        outfile.write("%s\n" % kindDesciption)
        outfile.write(79 * "-" + "\n\n")
        groups[kind].sort(key=lambda x: x.name)
        for info in groups[kind]:
            try:
                description = info.description.splitlines()[0]
            except:
                description = info.description
            description = re.sub(
                r'<a\s+href=["\']http://(.*?)["\']>\s*((\n|.)+?)\s*</a>',
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
    

def Main():
    import sphinx
    eg = ImportEg()
    WritePluginList(eg, os.path.join(DOCS_SOURCE_DIR, "PluginList.rst"))
    
    sphinx.main([
        None,
        "-a",
        "-b", "html",
        #"-E",
        "-d", os.path.join(DOCS_MAIN_DIR, ".doctree"),
        DOCS_SOURCE_DIR,
        DOCS_HTML_BUILD_DIR,
    ])
    
    sphinx.main([
        None,
        "-a",
        "-b", "htmlhelp",
        #"-E",
        "-d", os.path.join(DOCS_MAIN_DIR, ".doctree"),
        DOCS_SOURCE_DIR,
        DOCS_CHM_BUILD_DIR,
    ])
    
    htmlHelpCompilerPath = GetHtmlHelpCompilerPath()
    if htmlHelpCompilerPath is None:
        raise Exception("HTML Help Workshop command line compiler not found")
    import subprocess
    hhpPath = os.path.join(DOCS_CHM_BUILD_DIR, "EventGhost.hhp")
    subprocess.call([htmlHelpCompilerPath, hhpPath])
    import shutil
    shutil.copy(os.path.join(DOCS_CHM_BUILD_DIR, "EventGhost.chm"), MAIN_DIR)
    
    
if __name__ == "__main__":
    Main()
