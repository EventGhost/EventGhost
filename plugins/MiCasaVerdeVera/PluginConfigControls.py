ENABLEPORT = False

import eg
import os
import xml.etree.ElementTree as ET
from ChoiceControls import *
from TextControls import *


class PluginConfig(wx.Panel):
    text = Text

    def __init__(self, plugin, parent, host, port, prefix, upSpeed, addons):

        self.parent = parent
        self.plugin = plugin

        wx.Panel.__init__(self, parent)

        self.addOns = addons

        text = self.text.Vera
        panel = parent

        mainBox = wx.StaticBox(self, -1, text.PluginBox)
        connectionBox = wx.StaticBox(self, -1, text.VeraBox)
        prefixBox = wx.StaticBox(self, -1, text.PrefixBox)
        speedBox = wx.StaticBox(self, -1, text.UpdateBox)

        mainSizer = wx.StaticBoxSizer(mainBox, wx.VERTICAL)
        connectionSizer = wx.StaticBoxSizer(connectionBox, wx.HORIZONTAL)
        prefixSizer = wx.StaticBoxSizer(prefixBox, wx.HORIZONTAL)
        speedSizer = wx.StaticBoxSizer(speedBox, wx.HORIZONTAL)
        leftConnection = wx.BoxSizer(wx.VERTICAL)
        rightConnection = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        hostCtrl = wx.TextCtrl(self, -1, host, size=(100, 20))
        hostText = wx.StaticText(self, -1, text.VeraIPText, size=(100, 20))
        portCtrl = eg.SpinIntCtrl(self, -1, port, max=65535, size=(100, 20))
        portText = wx.StaticText(self, -1, text.VeraPortText, size=(100, 20))
        prefixCtrl = wx.TextCtrl(self, -1, prefix, size=(100, 20))
        prefixText = wx.StaticText(self, -1, text.PrefixText, size=(100, 20))
        upspeedCtrl = eg.SpinNumCtrl(self, -1, upSpeed, increment=0.05, min=0.10, size=(100, 20))
        upspeedText = wx.StaticText(self, -1, text.UpSpeedText, size=(100, 20))
        dataButton = wx.Button(self, -1, text.DataButton, size=(75, 20))
        addOnButton = wx.Button(self, -1, text.AddOnButton, size=(75, 20))
        errorText = wx.StaticText(self, -1, ' \n ')

        leftConnection.Add(hostText, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.BOTTOM, 5)
        leftConnection.Add(portText, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM, 5)
        rightConnection.Add(hostCtrl, 0, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 5)
        rightConnection.Add(portCtrl, 0, wx.EXPAND | wx.ALIGN_RIGHT | wx.LEFT | wx.BOTTOM | wx.RIGHT, 5)

        connectionSizer.Add(leftConnection, 0, wx.EXPAND | wx.ALIGN_LEFT)
        connectionSizer.Add(rightConnection, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        prefixSizer.Add(prefixText, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.BOTTOM, 5)
        prefixSizer.Add(prefixCtrl, 0, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 5)
        speedSizer.Add(upspeedText, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.BOTTOM, 5)
        speedSizer.Add(upspeedCtrl, 0, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 5)
        buttonSizer.Add(dataButton, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.BOTTOM, 5)
        buttonSizer.Add(addOnButton, 0, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(mainSizer)

        mainSizer.Add(connectionSizer, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 5)
        mainSizer.Add(prefixSizer, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM | wx.RIGHT, 5)
        mainSizer.Add(speedSizer, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        mainSizer.Add(errorText, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 15)
        mainSizer.Add(buttonSizer, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM | wx.RIGHT, 5)

        dataButton.Bind(wx.EVT_BUTTON, self.onData)
        addOnButton.Bind(wx.EVT_BUTTON, self.onAddOn)
        hostCtrl.Bind(wx.EVT_CHAR, self.onHost)

        self.hostCtrl = hostCtrl
        self.portCtrl = portCtrl
        self.prefixCtrl = prefixCtrl
        self.upspeedCtrl = upspeedCtrl
        self.errorText = errorText
        self.dataButton = dataButton

        portCtrl.Enable(ENABLEPORT)
        if host == '127.0.0.1':
            dataButton.Enable(False)

    def GetValues(self):
        return [
            self.hostCtrl.GetValue(),
            self.portCtrl.GetValue(),
            self.prefixCtrl.GetValue(),
            self.upspeedCtrl.GetValue()
        ]

    def onHost(self, evt):
        self.dataButton.Enable(True)
        evt.Skip()

    def onData(self, evt):
        data = self.CallVera()
        if data:
            self.VeraData = VeraData(self.parent)
            self.VeraData.XMLToTree(data)
            wx.CallAfter(self.VeraData.Show)
        evt.Skip()

    def onAddOn(self, evt):
        plugins = {}
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        print files
        for f in files:
            if f == '__init__.py': continue
            if f.split('.')[-1:][0] != 'py': continue
            with open(f, 'r') as pfile:
                line = pfile.readline()
                line = line.split(':')
                if line[0] != '#*~*PluginName': continue
                plugins[line[1]] = {}
                plugins[line[1]]['Description'] = line[2]
                plugins[line[1]]['Installed'] = False
        print plugins
        with open('__init__.py', 'r') as pfile:
            pass

        # *~*PluginName:Menu System:Menu system that allows for user friendly control of the Vera unit.*~*
        evt.Skip()

    def CallVera(self):
        import urllib2
        host = self.hostCtrl.GetValue()
        port = str(self.portCtrl.GetValue())

        URL = 'http://' + host + ':' + port
        URL += '/data_request?id=' + STATIC.URLS['userData'][0]
        try:
            reply = urllib2.urlopen(URL)
        except Exception as err:
            err = str(err)
            try:
                err = err[:30] + '\n' + err[30:]
            except:
                pass
            self.errorText.SetLabel(err)
            return None
        else:
            return reply.read()


class VeraData(wx.Frame):

    def __init__(self, parent):

        self.parent = parent
        style = wx.STAY_ON_TOP | wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER
        wx.Frame.__init__(self, parent, style=style)

    def XMLToTree(self, xmlstring):

        self.xml = ET.fromstring(xmlstring)
        self.tree = wx.TreeCtrl(self, style=wx.TR_HAS_BUTTONS)
        root = self.fillmeup()
        self.tree.Expand(root)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def fillmeup(self):
        xml = self.xml
        tree = self.tree
        root = tree.AddRoot(xml.tag)
        rootdata = xml.attrib
        system = tree.AppendItem(root, 'system_settings')
        for key in sorted(rootdata.keys()):
            val = tree.AppendItem(system, key)
            tree.AppendItem(val, rootdata[key])

        def add(parent, elem):
            for e in elem:
                tag = e.tag
                text = e.text
                data = e.attrib
                item = None
                if not data:
                    if tag == '' or tag == '\n':
                        add(parent, e)
                    else:
                        item = tree.AppendItem(parent, tag)
                        if text and text != '\n' and text != '':
                            val = tree.AppendItem(item, text)
                else:
                    name = e.tag
                    for key in ['name', 'Name', 'ip', 'Title', 'text', 'SourceName', 'DeviceType', 'FileName',
                                'device_type', 'udn', 'Function', 'variable']:
                        try:
                            name = data.pop(key)
                        except:
                            pass
                        else:
                            break
                    item = tree.AppendItem(parent, name)
                    for key in sorted(data.keys()):
                        val = tree.AppendItem(item, key)
                        if data[key] != '':
                            tree.AppendItem(val, str(data[key]))
                if item:
                    add(item, e)

        add(root, xml)
        return root

    def OnClose(self, evt):
        self.Destroy()
