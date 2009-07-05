import pickle
from string import Template

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
        
TEMPLATE = """\
<b>Name:</b> {name}<br>
<b>Author:</b> {author}<br>
<b>Version:</b> {version}<br>
<b>Description:</b><br>
{description}
"""

class PluginInstall(object):
    
    def PackPlugin(self):
        result = eg.AddPluginDialog.GetModalResult(
            eg.document.frame,
            checkMultiLoad = False
        )
        if not result:
            return
        pluginInfo = result[0]
        pluginData = {
            "name": pluginInfo.englishName,
            "author": pluginInfo.author,
            "version": pluginInfo.version,
            "description": pluginInfo.englishDescription,
        }
        dialog = eg.HtmlDialog(
            eg.document.frame, 
            "Plugin Information", 
            TEMPLATE.format(**pluginData),
            basePath = pluginInfo.path
        )
        dialog.ShowModal()
        dialog.Destroy()
        dialog = wx.FileDialog(
            eg.document.frame,
            defaultFile=pluginInfo.englishName,
            wildcard="EventGhost Plugin (*.egplugin)|*.egplugin",
            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT 
        )
        dialog.ShowModal()
        print dialog.GetPath()
        dialog.Destroy()
        
PluginInstall = PluginInstall()