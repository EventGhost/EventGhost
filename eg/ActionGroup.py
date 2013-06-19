import eg.IconTools
import eg
import new
import types
import Image

from ActionClass import ActionClass
from Utils import SetClass
import IconTools



class ActionInfo(object):
    iconIndex = None
    
    def __init__(self, iconIndex):
        self.iconIndex = iconIndex
        
        
    def GetWxIcon(self):
        return eg.imageList.GetIcon(self.iconIndex)
    
    
    
def CreateAction(actionCls, plugin):
    if not issubclass(actionCls, ActionClass):
        eg.notice("create new class from " + str(actionCls))
        actionCls = new.classobj(
            actionCls.__name__,
            (actionCls, ActionClass), 
            {}
        )
    action = actionCls.__new__(actionCls)
    action.plugin = plugin
    if action.iconFile:
        try:
            path = plugin.info.path + action.iconFile + ".png"
            img = Image.open(path).convert("RGBA")
        except:
            eg.PrintError(
                "Error while loading icon file %s" % action.iconFile
            )
            iconIndex = plugin.info.iconIndex
        else:
            iconIndex = eg.IconTools.SetupIcons2(img)
    else:
        iconIndex = plugin.info.iconIndex

    text = actionCls.text
    if text is None:
        text = getattr(plugin.text, actionCls.__name__, None)
        if text is None:
            class text:
                pass
            text = text()
            setattr(plugin.text, actionCls.__name__, text)
    elif type(text) == types.ClassType:        
        translation = getattr(plugin.text, actionCls.__name__, None)
        if translation is None:
            translation = text()
        SetClass(translation, text)
        text = translation
        setattr(plugin.text, actionCls.__name__, text)
    textCls = text.__class__
    if not hasattr(textCls, "name"):
        name = actionCls.name
        textCls.name = actionCls.__name__ if name is None else name
    
    if not hasattr(textCls, "description"):
        description = actionCls.description
        textCls.description = textCls.name if description is None else description
        
    actionCls.text = text
    action.name = text.name
    action.description = text.description
    action.info = ActionInfo(iconIndex)
    action.__init__()
    return action
    
    
                
class ActionGroup:
    plugin = None
    name = None
    description = None
    iconIndex = eg.IconTools.ICON_IDX_FOLDER
    
    def __init__(self, plugin, name=None, description=None, iconFile=None):
        self.plugin = plugin
        self.expanded = False
        self.name = name or plugin.name
        self.description = description or plugin.description
        if iconFile is None:
            self.iconIndex = plugin.info.iconIndex + 2
        else:
            self.iconIndex = IconTools.CreateActionGroupIcon(plugin, iconFile)
        self.actionList = []
        
        
    def AddGroup(self, name=None, description=None, iconFile=None):
        group = ActionGroup(self.plugin, name, description, iconFile)
        self.actionList.append(group)
        return group
    
    
    def AddAction(self, actionClass, hidden=False):
        action = CreateAction(actionClass, self.plugin)
        setattr(self.plugin, actionClass.__name__, action)
        if not hidden:
            self.actionList.append(action)
        return action
    


