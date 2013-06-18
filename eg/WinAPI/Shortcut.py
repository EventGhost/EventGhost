import pythoncom
from win32com.shell import shell, shellcon

def CreateShortcut(
    path, 
    target, 
    arguments="", 
    startIn="",
    icon=("", 0), 
    description=""
):
    """Create a Windows shortcut:
    
    path - As what file should the shortcut be created?
    target - What command should the desktop use?
    arguments - What arguments should be supplied to the command?
    startIn - What folder should the command start in?
    icon - (filename, index) What icon should be used for the shortcut?
    description - What description should the shortcut be given?
    
    eg
    CreateShortcut(
        path=os.path.join (desktop (), "PythonI.lnk"),
        target=r"c:\python\python.exe",
        icon=(r"c:\python\python.exe", 0),
        description="Python Interpreter"
    )
    """
    sh = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IShellLink
    )
    sh.SetPath(target)
    sh.SetDescription(description)
    sh.SetArguments(arguments)
    sh.SetWorkingDirectory(startIn)
    sh.SetIconLocation(icon[0], icon[1])
    persist = sh.QueryInterface(pythoncom.IID_IPersistFile)
    persist.Save(path, 1)


def GetShortcutInfo(filename):
    sh = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IShellLink
    )
    persist = sh.QueryInterface(pythoncom.IID_IPersistFile).Load(filename)
    class ShortcutInfo:
        pass
    shortcutInfo = ShortcutInfo()
    shortcutInfo.path = filename
    shortcutInfo.target = sh.GetPath(shell.SLGP_SHORTPATH)[0]
    shortcutInfo.description = sh.GetDescription()
    shortcutInfo.arguments = sh.GetArguments()
    shortcutInfo.startIn = sh.GetWorkingDirectory()
    shortcutInfo.icons = sh.GetIconLocation()
    return shortcutInfo
