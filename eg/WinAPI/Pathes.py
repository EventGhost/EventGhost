from win32com.shell import shell, shellcon
import win32api

def get_path (folder_id):
    location = shell.SHGetSpecialFolderLocation(0, folder_id)
    return shell.SHGetPathFromIDList(location)


def get_path2 (folderId):
    location = shell.SHGetFolderPath(0, folderId, None, 0)
    return location

APPDATA = get_path2(shellcon.CSIDL_APPDATA)
STARTUP = get_path2(shellcon.CSIDL_STARTUP)
PROGRAMFILES = get_path2(shellcon.CSIDL_PROGRAM_FILES)
TEMPDIR = win32api.GetTempPath()

