import pickle

class PluginInfo(object):
    name = "<unknown>"
    author = "<unknown>"
    version = "<unknown>"
    description = "<unknown>"
    
    def __init__(self, name, author, version, description):
        self.name = name
        self.version = version
        self.author = author
        self.description = description
        
        
        
class PluginInstall(object):
    
    def PackPlugin(self):
        result = eg.AddPluginDialog.GetModalResult(eg.document.frame)
        if not result:
            return
        pluginInfo = result[0]
        info = PluginInfo(pluginInfo.englishName, pluginInfo.author, pluginInfo.version, pluginInfo.englishDescription)
        print pluginInfo.author
        print pluginInfo.version
        print pluginInfo.englishName
        print pluginInfo.englishDescription
        data = pickle.dumps(info)
        print data
        print pickle.loads(data)
PluginInstall = PluginInstall()