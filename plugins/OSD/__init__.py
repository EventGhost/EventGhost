import eg
       
class OSD(eg.PluginClass):
    pass
        
        
class ShowOSD(eg.ActionClass):
    name = "Show OSD"
    
    def __init__(self):
        self.plugin = eg.plugins.EventGhost
        
        
    def __call__(self, *args, **kwargs):
        return eg.plugins.EventGhost.ShowOSD(*args, **kwargs)


    def GetLabel(self, *args, **kwargs):
        return eg.plugins.EventGhost.ShowOSD.GetLabel(*args, **kwargs)
    
    
    def Configure(self, *args, **kwargs):
        return eg.plugins.EventGhost.ShowOSD.Configure(*args, **kwargs)