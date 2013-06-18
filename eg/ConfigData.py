import wx
import Persistent
import os

configFilePath = ''
config = None

class DefaultConfig:
    buildNum = 0
    language = 'en_EN'
    startWithWindows = False
    hideOnStartup = False
    checkUpdate = False
    logActions = True
    onlyLogAssigned = False
    useAutoloadFile = True
    autoloadFilePath = os.path.join(
        wx.StandardPaths.Get().GetUserDataDir(),
        'MyConfig.xml'
    )
    storedBootTime = 0
    limitMemory = True
    limitMemorySize = 8
    confirmDelete = True
    class plugins:
        pass



locale = wx.Locale()
if locale.GetLanguageName(locale.GetSystemLanguage()) == 'German':
    DefaultConfig.language = 'de_DE'


def LoadConfig():
    global configFilePath, config
    configDir = wx.StandardPaths.Get().GetUserDataDir()
    if not os.path.exists(configDir):
        os.makedirs(configDir)
        import shutil
        shutil.copy("Example.xml", os.path.join(configDir, "MyConfig.xml"))
    configFilePath = os.path.join(configDir, "config.py")
    config = Persistent.PyLoad(configFilePath, DefaultConfig)
    if config.language == "Deutsch":
        config.language = "de_DE"
    return config


def SaveConfig():
    global configFilePath, config
    import eg
    config.buildNum = eg.buildNum
    Persistent.PySave(config, configFilePath)
