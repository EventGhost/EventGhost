import os
import wx

import eg
from eg.IconTools import GetIcon, pilToBitmap
from eg.Controls.SizeGrip import SizeGrip

        
kindTags = ["remote", "program", "external", "other"]

class DefaultConfig:
    position = None
    size = (552, 382)
    splitPosition = 216
    expandDict = {}
    lastSelection = None

config = eg.GetConfig("AddPluginDialog", DefaultConfig)


class Text:
    title = "Choose a plugin to add..."
    noInfo = "No information available."
    noMultiloadTitle = "No multiload possible"
    noMultiload = \
        "This plugin doesn't support multiload and you already have one " \
        "instance of this plugin in your configuration."
    remotePlugins = "Remote Receiver"
    programPlugins = "Program Control"
    externalPlugins = "External Hardware Control"
    otherPlugins = "Other"
    author = "Author:"
    version = "Version:"
    descriptionBox = "Description"
    
Text = eg.GetTranslation(Text)


class AddPluginDialog(eg.Dialog):

    def __init__(self):
        self.resultData = None
        self.resize2pending = False
        eg.Dialog.__init__(
            self, 
            None, 
            -1, 
            Text.title,
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        )

        splitter = wx.SplitterWindow(
            self,
            style = wx.SP_LIVE_UPDATE
                |wx.CLIP_CHILDREN
                |wx.NO_FULL_REPAINT_ON_RESIZE
        )
        self.splitter = splitter

        self.tree = tree = wx.TreeCtrl(
            splitter,
            style=wx.TR_SINGLE
                |wx.TR_HAS_BUTTONS
                |wx.TR_HIDE_ROOT
                |wx.TR_LINES_AT_ROOT
        )
        
        tree.SetMinSize((170, 200))

        imageList = wx.ImageList(16, 16)
        tree.SetImageList(imageList)
        imageList.Add(GetIcon("images/plugin.png"))
        imageList.Add(GetIcon("images/folder.png"))
        self.imageList = imageList
        
        root = tree.AddRoot("")
        typeIds = {
            kindTags[0]: tree.AppendItem(root, Text.remotePlugins, 1),
            kindTags[1]: tree.AppendItem(root, Text.programPlugins, 1),
            kindTags[2]: tree.AppendItem(root, Text.externalPlugins, 1),
            kindTags[3]: tree.AppendItem(root, Text.otherPlugins, 1),
        }
        self.typeIds = typeIds
        itemToSelect = typeIds["remote"]
        
        pluginList = []
        for item in os.listdir("Plugins"):
            if item.startswith("."):
                continue
            file_name, extension = os.path.splitext(item)
            if os.path.isdir("Plugins/" + item) or extension in (".py", ".egp"):
                if pluginList.count(file_name) == 0:
                    pluginList.append(file_name)
        defaultTarget = typeIds["other"]
        for filename in pluginList:
            info = eg.GetPluginInfo(filename)
            idx = 0
            name = filename
            target = defaultTarget
            if info:
                if info.kind == "hidden":
                    continue
                name = info.name
                if info.icon:
                    idx = imageList.Add(pilToBitmap(info.icon))
                target = typeIds.get(info.kind, target)
            id = tree.AppendItem(target, name, idx)
            tree.SetPyData(id, info)
            if filename == config.lastSelection:
                itemToSelect = id
                
        
        for kind, treeId in typeIds.iteritems():
            if config.expandDict.get(kind, True):
                tree.Expand(typeIds[kind])
            else:
                tree.Collapse(typeIds[kind])
        
        tree.ScrollTo(itemToSelect)
        
        self.htmlTemplate = (
            '<html><body bgcolor="#%02X%02X%02X">%%s</body></html>' 
                % self.GetBackgroundColour().Get()
        )

        rightPanel = wx.Panel(splitter)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightPanel.SetSizer(rightSizer)
        
        self.nameText = nameText = wx.StaticText(rightPanel)
        nameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        rightSizer.Add(nameText, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)
        
        subSizer = wx.FlexGridSizer(2,2)
        self.authorLabel = wx.StaticText(rightPanel, label=Text.author)
        subSizer.Add(self.authorLabel)
        self.authorText = wx.StaticText(rightPanel)
        subSizer.Add(self.authorText, 0, wx.EXPAND|wx.LEFT, 5)
        self.versionLabel = wx.StaticText(rightPanel, label=Text.version)
        subSizer.Add(self.versionLabel)
        self.versionText = wx.StaticText(rightPanel)
        subSizer.Add(self.versionText, 0, wx.EXPAND|wx.LEFT, 5)
        rightSizer.Add(subSizer, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)
        
        staticBoxSizer = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label=Text.descriptionBox)
        )
        
        descrBox = eg.HtmlWindow(rightPanel)
        descrBox.SetBasePath("/plugins/")
        self.descrBox = descrBox
        staticBoxSizer.Add(descrBox, 1, wx.EXPAND)
        
        rightSizer.Add(staticBoxSizer, 1, wx.EXPAND|wx.LEFT, 5)
        
        splitter.SplitVertically(self.tree, rightPanel)
        splitter.SetMinimumPaneSize(60)
        splitter.SetSashGravity(0.0)
        splitter.UpdateSize()

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))
        self.okButton = self.buttonRow.okButton
        self.okButton.Enable(False)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(splitter, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)
        
        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        mainSizer.Fit(self)
        minSize = mainSizer.GetMinSize()
        #self.SetMinSize(minSize)
        self.SetSize(config.size)
        splitter.SetSashPosition(config.splitPosition)
        if config.position:
            self.SetPosition(config.position)
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)
        tree.SelectItem(itemToSelect)


    def OnSelect(self, event):
        item = event.GetItem()
        self.resultData = info = self.tree.GetPyData(item)       
        if info is None:
            name = self.tree.GetItemText(item)
            description = Text.noInfo
            self.authorLabel.SetLabel("")
            self.authorText.SetLabel("")
            self.versionLabel.SetLabel("")
            self.versionText.SetLabel("")
            self.okButton.Enable(False)
            event.Skip()
        else:
            name = info.name
            description = info.description
            self.descrBox.SetBasePath(info.path)
            self.authorLabel.SetLabel(Text.author)
            self.authorText.SetLabel(info.author)
            self.versionLabel.SetLabel(Text.version)
            self.versionText.SetLabel(info.version)
            self.okButton.Enable(True)
        self.nameText.SetLabel(name)
        self.descrBox.SetPage(self.htmlTemplate % description)


    def CheckMultiload(self):
        info = self.resultData
        if (
            info
            and info.pluginCls 
            and not info.pluginCls.canMultiLoad 
            and info.instances
        ):
            wx.MessageBox(
                Text.noMultiload,
                Text.noMultiloadTitle, 
                style=wx.ICON_EXCLAMATION
            )
            return False
        else:
            return True
        
        
    def OnItemActivated(self, event):
        item = self.tree.GetSelection()
        info = self.tree.GetPyData(item)
        if info is not None:
            if self.CheckMultiload():
                self.EndModal(wx.ID_OK)
            else:
                event.Skip()
        else:
            event.Skip()
        
        
    def OnOK(self, event):
        eg.whoami()
        if self.CheckMultiload():
            event.Skip()
        
        
    def OnCancel(self, event):
        self.Close()


    def Destroy(self):
        config.size = self.GetSizeTuple()
        config.position = self.GetPositionTuple()
        config.splitPosition = self.splitter.GetSashPosition()
        expandDict = {}
        for kind, treeId in self.typeIds.iteritems():
            expandDict[kind] = self.tree.IsExpanded(treeId)
        config.expandDict = expandDict        
        wx.Dialog.Destroy(self)
