# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, Walter Kraembring
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of Walter Kraembring nor the names of its contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


##############################################################################
# Revision history:
#
# 2011-06-19  Still experimental, many modifications & improvements
# 2011-05-27  Experimental change of SetProcessWorkingSetSize call
# 2011-05-25  First version, thanks to Barry Barnreiter for OpenOPC
# (barry_b@users.sourceforge.net) 
##############################################################################

import eg

eg.RegisterPlugin(
    name="OPC",
    guid='{3ABF9B84-1C04-42F0-81FE-69F29309DFC3}',
    author="Walter Kraembring",
    version="0.0.8",
    kind="other",
    canMultiLoad=True,
    createMacrosOnAdd=False,
    url="http://www.eventghost.net/forum/",
    description=(
        '<p>Plugin to connect to '
        'OPC DA Servers</a></p>'
        '\n\n<p>'
        '<center><img src="opc.png" /></center>'
    ),
)

import OpenOPC
import pythoncom
import wx
from threading import Event, Thread


class Text:
    infoOpcServerObject = "OPC object created"
    infoPlugin = "OPC plugin stopped"
    infoStatus = "OPC is not found"
    infoGroupsCreate = "Please wait, creating item groups..."
    infoGroupsReady = "Ready, groups are created..."
    infoGroupsRemove = "Please wait, removing item groups..."
    infoGroupsDeleted = "Ready, groups are removed..."
    infoNoDevice = "OPC was not found"
    infoThreadStopped = "OPC monitor thread has stopped"
    threadWaitTime = "Thread wait time (x.y s): "
    selectBoxOpcServer = "Select the OPC server to connect to: "

    class OPC_write_command:
        textBoxName = "Enter a descriptive name for the command"
        textBoxTag = "Select the tag"
        textBoxItem = "Select the item"
        textBoxCommand = "Select or type the commmand to send"


class OPC_Client(eg.PluginClass):
    text = Text

    def __init__(self):
        self.stopThreadEvent = None
        self.AddAction(OPC_write_command)

    def __start__(
        self,
        OPC_name,
        tw
    ):
        self.bOpcObjectCreated = False
        self.OPC_name = OPC_name
        self.iDelay = tw
        self.tags = []
        self.items = {}
        self.tag_items = []
        self.previousStatus = []
        self.opc = OpenOPC.client()

        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadWorker,
            args=(self.stopThreadEvent,)
        )
        thread.start()

    def __stop__(self):
        if self.stopThreadEvent:
            self.stopThreadEvent.set()
        print self.text.infoPlugin

    def __close__(self):
        if self.stopThreadEvent:
            self.stopThreadEvent.set()
        print self.text.infoPlugin

    def ThreadWorker(self, stopThreadEvent):
        # The polling is started
        while not stopThreadEvent.isSet():
            stopThreadEvent.wait(self.iDelay)
            if not self.bOpcObjectCreated:
                self.findOpcServer()
            for i in range(0, len(self.tags)):
                tmp = []
                tag = self.tags[i]
                self.tag_items = self.items[tag]
                if len(self.previousStatus) > 0:
                    tmp = self.previousStatus[i]
                for j in range(0, len(self.tag_items)):
                    try:
                        g_list = self.opc.read(group='MyGroup_' + str(i) + str(j))
                        name, value, quality, time = g_list[0]
                        if len(self.previousStatus) > 0:
                            if value != tmp[j]:
                                eg.TriggerEvent(self.tag_items[j], payload=value)
                                tmp[j] = value
                    except:
                        eg.PrintError("OPC timeout")
                        stopThreadEvent.wait(self.iDelay)
                self.previousStatus[i] = tmp

        # Clean up used groups 
        print self.text.infoGroupsRemove
        for i in range(0, len(self.tags)):
            for j in range(0, len(self.tag_items)):
                # print 'MyGroup_'+str(i)+str(j)
                self.opc.remove('MyGroup_' + str(i) + str(j))
        print self.text.infoGroupsDeleted
        self.opc.close()
        self.bOpcObjectCreated = False
        print self.text.infoThreadStopped

    def getOPCitems_datatype(self, item):
        vt = dict([(pythoncom.__dict__[vtype], vtype) for vtype in pythoncom.__dict__.keys() if vtype[:2] == "VT"])

        # Detect data type for the item
        my_opc = OpenOPC.client()
        my_opc.connect(self.OPC_name)
        data_type = my_opc.properties(item, id=1)
        my_opc.close()
        del my_opc

        # Replace variant id with type strings
        try:
            data_type = str(vt[data_type])
        except:
            data_type = str(data_type)
            pass
        return (data_type)

    def findOpcServer(self):
        self.tags = []
        self.previousStatus = []
        try:
            self.opc.connect(self.OPC_name)

            # Create list of all tags
            self.tags = self.opc.list()
            below_root_tags = []

            # Create lists of all items and build up the initial groups
            for i in range(0, len(self.tags)):
                result = self.opc.list(self.tags[i], recursive=True)
                below_root_tags.append(result)
            tag_items = {}
            print self.text.infoGroupsCreate
            for i in range(0, len(self.tags)):
                tag_items[self.tags[i]] = below_root_tags[i]
            self.items = tag_items

            # Read the values first time for each group
            for i in range(0, len(self.tags)):
                tmp = []
                t_items = tag_items[self.tags[i]]
                for j in range(0, len(t_items)):
                    try:
                        value, quality, time = self.opc.read(
                            t_items[j],
                            group='MyGroup_' + str(i) + str(j)
                        )
                        tmp.insert(j, value)
                    except:
                        tmp.insert(j, "None")
                        pass
                #                    data_type = self.getOPCitems_datatype(t_items[j])                     
                #                    print "t_items[j]: ", t_items[j], "data_type: ", data_type
                self.previousStatus.append(tmp)
            self.bOpcObjectCreated = True
            print self.text.infoGroupsReady
        except:
            self.bOpcObjectCreated = False
            eg.PrintError(self.text.infoStatus)

    # Get the choice of OPC server from the dropdown
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        OPC_name="Select OPC server to control",
        tw=0.5,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer = wx.GridBagSizer(5, 5)

        # Find installed OPC servers
        try:
            find_opc = OpenOPC.client()
            list = find_opc.servers()
            find_opc.close()
            del find_opc
        except:
            list = []

        # Create a dropdown for selection of the OPC server
        opcServerCtrl = wx.Choice(parent=panel, pos=(10, 10))
        opcServerCtrl.AppendItems(items=list)
        if list:
            opcServerCtrl.SetStringSelection(
                OPC_name if OPC_name in list else list[0]
            )
        mySizer.Add(wx.StaticText(
            panel,
            -1,
            self.text.selectBoxOpcServer),
            (1, 0)
        )
        mySizer.Add(opcServerCtrl, (1, 1))
        opcServerCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Set the OPC poll rate (delay between polls)
        thread_wait = panel.SpinNumCtrl(
            tw,
            decimalChar='.',  # by default, use '.' for decimal point
            groupChar=',',  # by default, use ',' for grouping
            fractionWidth=2,
            integerWidth=2,
            increment=0.10,
            min=0.10,
            max=30.0
        )
        thread_wait.SetInitialSize((60, -1))
        mySizer.Add(wx.StaticText(
            panel,
            -1,
            self.text.threadWaitTime),
            (2, 0)
        )
        mySizer.Add(thread_wait, (2, 1))

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        while panel.Affirmed():
            OPC_name = opcServerCtrl.GetStringSelection()
            tw = thread_wait.GetValue()

            panel.SetResult(
                OPC_name,
                tw,
                *args
            )


class OPC_write_command(eg.ActionClass):
    name = "OPC write item value"
    description = "Action to write item value"

    def __call__(self, name, tag, item, command, configured):
        my_opc = OpenOPC.client()
        my_opc.connect(self.plugin.OPC_name)
        my_opc[item] = command
        my_opc.close()
        del my_opc

    def getOPCtags(self):
        # Get the tags for the selected OPC server
        t_list = self.plugin.tags
        return (t_list)

    def getOPCitems(self, tag):
        # Get the items for the selected tag
        i_list = self.plugin.items[tag]
        if len(i_list) == 0:
            i_list = ['Empty']
        return (i_list)

    def OnTagChoice(self, event=None):
        plugin = self.plugin
        tagCtrl = self.tagCtrl
        itemCtrl = self.itemCtrl
        self.tag = tagCtrl.GetStringSelection()

        # Get the items for the selected tag
        i_list = self.getOPCitems(self.tag)
        itemCtrl.Clear()
        itemCtrl.AppendItems(items=i_list)
        # itemCtrl.SetStringSelection(i_list[0] if event else self.item)
        itemCtrl.SetStringSelection(
            self.item if self.item in i_list
            else i_list[0]
        )
        self.OnItemChoice()
        if event:
            event.Skip()

    def OnItemChoice(self, event=None):
        tagCtrl = self.tagCtrl
        itemCtrl = self.itemCtrl
        configured = self.configured
        panel = itemCtrl.GetParent()
        staticBoxSizer = panel.sizer.GetItem(3).GetSizer()

        # Disable drop-downs if already configured
        if configured:
            tagCtrl.Enable(False)
            itemCtrl.Enable(False)

        if len(staticBoxSizer.GetChildren()):
            dynamicSizer = staticBoxSizer.GetItem(0).GetSizer()
            dynamicSizer.Clear(True)
            staticBoxSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()

        sel_item = itemCtrl.GetStringSelection()
        itemCtrl.SetStringSelection(
            sel_item if sel_item in itemCtrl.GetStrings()
            else itemCtrl.GetStrings()[0]
        )

        if sel_item != "Empty":
            # Detect data type for the selected item
            self.data_type = self.plugin.getOPCitems_datatype(sel_item)
        else:
            self.data_type = "Empty"

        # Create a field for the command with correct data type
        if self.data_type in ("VT_I8", "VT_I4", "VT_I2", "VT_I1", "VT_INT"):
            cmdCtrl = panel.SpinIntCtrl(
                self.command,
                min=0,
                max=99999
            )
            if not event:
                cmdCtrl.SetValue(self.command)

        if self.data_type in ("VT_BSTR", "VT_BTSR_ARRAY"):
            cmdCtrl = wx.TextCtrl(panel, -1, str(self.command))
            if not event:
                cmdCtrl.ChangeValue(self.command)

        if self.data_type == "VT_BOOL":
            cmdCtrl = wx.Choice(parent=panel, pos=(10, 10))
            list = [
                'True', 'False'
            ]
            cmdCtrl.AppendItems(items=list)
            cmdCtrl.SetStringSelection(
                self.command if self.command in list
                else list[0]
            )
            if not event:
                cmdCtrl.SetStringSelection(self.command)

        if self.data_type in ("VT_R4", "VT_R8"):
            cmdCtrl = panel.SpinNumCtrl(
                self.command,
                decimalChar='.',  # by default, use '.' for decimal point
                groupChar=',',  # by default, use ',' for grouping
                fractionWidth=1,
                integerWidth=5,
                min=0.0,
                max=99999.0,
                increment=0.1
            )
            if not event:
                cmdCtrl.SetValue(self.command)

        if self.data_type in ("VT_UI8", "VT_UI4", "VT_UI2", "VT_UI1", "VT_UINT"):
            cmdCtrl = panel.SpinIntCtrl(
                self.command,
                min=0,
                max=99999
            )
            if not event:
                cmdCtrl.GetValue()

        if self.data_type == "Empty":
            cmdCtrl = wx.TextCtrl(panel, -1, str(self.command))
            cmdCtrl.Enable(False)
            if not event:
                cmdCtrl.ChangeValue(self.command)

        if self.data_type in (
            "8194", "8195", "8196", "8197", "8198", "8199", "8200", "8201", "8203", "8204",
            "8208", "8209", "8210", "8211", "8212", "8213", "8214", "8215", "8216", "VT_CY",
            "VT_DATE"
        ):
            cmdCtrl = wx.TextCtrl(panel, -1, str(self.command))
            if not event:
                cmdCtrl.ChangeValue(self.command)

        elif self.data_type == None:
            cmdCtrl = wx.TextCtrl(panel, -1, str(self.command))
            if not event:
                cmdCtrl.ChangeValue(self.command)

        dynamicSizer = wx.BoxSizer(wx.HORIZONTAL)
        dynamicSizer.Add(cmdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(dynamicSizer, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Layout()
        self.cmdCtrl = cmdCtrl
        if event:
            event.Skip()

    def Configure(
        self,
        name="Give the command a name",
        tag="",
        item="",
        command="",
        configured=False
    ):

        text = self.text
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        self.tag = tag
        self.item = item
        self.command = command
        self.configured = configured
        self.data_type = None
        t_list = []
        i_list = []

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Get the tags
        t_list = self.getOPCtags()

        # Create a dropdown to select tag
        tagCtrl = self.tagCtrl = wx.Choice(parent=panel, pos=(10, 10))
        tagCtrl.AppendItems(items=t_list)
        tagCtrl.SetStringSelection(
            self.tag if self.tag in t_list
            else t_list[0]
        )
        self.tag = tagCtrl.GetStringSelection()
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxTag)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(tagCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        tagCtrl.Bind(wx.EVT_CHOICE, self.OnTagChoice)

        # Get the items for the selected tag
        i_list = self.getOPCitems(self.tag)

        # Create a dropdown to select the item
        itemCtrl = self.itemCtrl = wx.Choice(parent=panel, pos=(10, 10))
        itemCtrl.AppendItems(items=i_list)
        itemCtrl.SetStringSelection(
            self.item if self.item in i_list
            else i_list[0]
        )
        self.item = itemCtrl.GetStringSelection()
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxItem)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(itemCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        itemCtrl.Bind(wx.EVT_CHOICE, self.OnItemChoice)

        # Create an entry field for the command
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        self.OnTagChoice()  # This is used when opening the dialog

        def OnButton(event):
            # Disable drop-downs on button events
            event.Skip()
            tagCtrl.Enable(False)
            itemCtrl.Enable(False)

        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnButton)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            cmdCtrl = self.cmdCtrl
            if self.data_type == "VT_BOOL":
                self.command = cmdCtrl.GetStringSelection()
            else:
                self.command = cmdCtrl.GetValue()
            self.configured = True
            panel.SetResult(
                nameCtrl.GetValue(),
                tagCtrl.GetStringSelection(),
                itemCtrl.GetStringSelection(),
                self.command,
                self.configured
            )
