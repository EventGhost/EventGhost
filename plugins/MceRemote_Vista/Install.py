import sys
from os.path import dirname, join, abspath
from eg.WinApi.Service import Service
import _winreg as reg
import shutil, os

ServiceKey = "SYSTEM\\CurrentControlSet\\Services\\EventLog\\Application"

def Is64BitOS():
    from os import environ
    if environ.get("PROCESSOR_ARCHITECTURE") == "AMD64" or environ.get("PROCESSOR_ARCHITEW6432") == "AMD64":
        return True
    return False

def AddOrRemoveHIDKeys(isInstall):
    HID_SUB_KEY = "SYSTEM\\CurrentControlSet\\Services\\HidIr\\Remotes\\745a17a0-74d3-11d0-b6fe-00a0c90f57d"
    ValuesToCheck = ['a','b']
    for a in ValuesToCheck:
        tmpkey = HID_SUB_KEY+a
        try:
            key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, tmpkey, 0, reg.KEY_ALL_ACCESS)
            for i in xrange(4):
                valueName = 'CodeSetNum%i' % i
                if isInstall:
                    reg.DeleteValue(key, valueName)
                else:
                    reg.SetValueEx(key, valueName, 0, reg.REG_DWORD, i + 1)
        except WindowsError:
            continue

def Install():
    AddOrRemoveHIDKeys(True)
    osExtension = "x86"
    if Is64BitOS():
        osExtension = "x64"
    pluginDir =  dirname(__file__.decode(sys.getfilesystemencoding()))
    tmpExe = join(pluginDir, "AlternateMceIrService_%s.exe"%osExtension)
    myExe = join(pluginDir, "AlternateMceIrService.exe")
    try:
        os.remove(myExe)
    except:
        pass
    shutil.copyfile(tmpExe,myExe)
    key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, ServiceKey+"\\AlternateMceIrService")
    reg.SetValueEx(key, "EventMessageFile", 0, reg.REG_SZ, myExe)
    reg.SetValueEx(key, "TypesSupported", 0, reg.REG_DWORD, 7)
    service = Service(u"AlternateMceIrService")
    service.Install(myExe)
    service.Start()
    print "Service successfully installed"

def Uninstall():
    AddOrRemoveHIDKeys(False)
    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ServiceKey, 0, reg.KEY_ALL_ACCESS)
    reg.DeleteKey(key, "AlternateMceIrService")
    service = Service(u"AlternateMceIrService")
    service.Stop()
    service.Uninstall()
    print "Service successfully uninstalled"
