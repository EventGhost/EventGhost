import eg

class PluginMetaClass(type):
    """
    The metaclass of PluginClass that allows us to monitor the definition of a
    new plugin.
    """
    
    def __new__(metacls, name, bases, dict):
        newClass = type.__new__(metacls, name, bases, dict)
        if eg._lastDefinedPluginClass is not None:
            raise "More than one PluginClass defined!"
        eg.SetAttr("_lastDefinedPluginClass", newClass)
        return newClass
