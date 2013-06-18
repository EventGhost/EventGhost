import eg

class ActionMetaClass(type):
    """
    The metaclass of ActionClass that allows us to monitor the definition of a
    new action.
    """
    
    def __new__(metacls, name, bases, dict):
        newClass = type.__new__(metacls, name, bases, dict)
        if eg._lastDefinedPluginClassInfo:
            eg._lastDefinedPluginClassInfo.actionClassList.append(newClass)
        return newClass
