# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import binascii
import wx
import _winreg

# Local imports
import eg
from eg.cFunctions import RegEnumKeysAndValues

regKeys = (
    (_winreg.HKEY_CLASSES_ROOT, "HKEY_CLASSES_ROOT", "HKCR"),
    (_winreg.HKEY_CURRENT_USER, "HKEY_CURRENT_USER", "HKCU"),
    (_winreg.HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE", "HKLM"),
    (_winreg.HKEY_USERS, "HKEY_USERS", "HKU"),
    (_winreg.HKEY_CURRENT_CONFIG, "HKEY_CURRENT_CONFIG", "HKCC")
)

regTypes = (
    (None, "Auto"),
    (_winreg.REG_BINARY, "REG_BINARY"),
    (_winreg.REG_DWORD, "REG_DWORD"),
    (_winreg.REG_EXPAND_SZ, "REG_EXPAND_SZ"),
    (_winreg.REG_MULTI_SZ, "REG_MULTI_SZ"),
    (_winreg.REG_NONE, "REG_NONE"),
    (_winreg.REG_SZ, "REG_SZ")
)

class Config(eg.PersistentData):
    lastKeySelected = _winreg.HKEY_CURRENT_USER
    lastSubkeySelected = "Software"
    lastValueNameSelected = None


class Text:
    name = description = "Registry"

    noKeyError = "No key given"
    noSubkeyError = "No subkey given"
    noTypeError = "No type given"
    noNewValueError = "No new value given"
    noValueNameError = "No value name given"
    keyOpenError = "Error opening registry key"
    valueChangeError = "Error while modifying value"

    defaultText = "(Default)"
    chooseText = "Choose Registry Key:"
    keyText = "Key:"
    valueText = "Value:"
    valueName = "Value name:"
    actionText = "Action:"
    newValue = "New value:"
    oldValue = "Current value:"
    oldType = "Current Type:"
    typeText = "Type:"

    keyText2 = "Key"
    noValueText = "value not found"


class RegistryChange(eg.ActionBase):
    name = "Change Registry Value"
    description = "Changes a value in the Windows registry."
    iconFile = "icons/Registry"

    class text:
        actions = ("create or change", "change if exists only", "delete")
        labels = (
            'Change "%s" to %s',
            'Change "%s" to %s if exists only',
            'Delete "%s"'
        )
        disableParsing = "Disable parsing of string"

    def __call__(
        self,
        key,
        subkey,
        valueName,
        action,
        keyType,
        newValue,
        disableParsing=False
    ):
        if not disableParsing:
            newValue = eg.ParseString(newValue)
        if not key:
            self.PrintError(self.text2.noKeyError)
            return 0
        if not subkey:
            self.PrintError(self.text2.noSubkeyError)
            return 0
        if not valueName:
            self.PrintError(self.text2.noValueNameError)
            return 0

        #try to get handle
        try:
            if action == 0:
                regHandle = _winreg.CreateKey(key, subkey)
            else:
                regHandle = _winreg.OpenKey(
                    key,
                    subkey,
                    0,
                    _winreg.KEY_WRITE | _winreg.KEY_READ
                )
        except EnvironmentError, exc:
            if action != 1:
                eg.PrintError(self.text2.keyOpenError + ": " + str(exc))
            return 0

        #getting old value
        oldType = None
        try:
            regValue = _winreg.QueryValueEx(regHandle, valueName)
            oldType = regValue[1]
        except EnvironmentError, exc:
            #exit because value does not exist
            if (action == 1):
                _winreg.CloseKey(regHandle)
                return 1
            if (action == 2):
                _winreg.CloseKey(regHandle)
                return 0

        #try to determine type if none is given
        if ((action == 0) or (action == 1)) and keyType is None:
            if oldType is None:
                try:
                    int(newValue)
                    #is int
                    keyType = _winreg.REG_DWORD
                except ValueError, exc:
                    if newValue.count("%") > 1:
                        keyType = _winreg.REG_EXPAND_SZ
                    else:
                        keyType = _winreg.REG_SZ
            #if key already exists use the old type
            else:
                keyType = oldType

        #set or delete key
        try:
            if (action == 0) or (action == 1):
                if keyType == _winreg.REG_DWORD:
                    newValue = int(newValue)
                #change key
                _winreg.SetValueEx(regHandle, valueName, 0, keyType, newValue)
            elif (action == 2):
                #delete value
                _winreg.DeleteValue(regHandle, valueName)
            return 1
        except (EnvironmentError, ValueError), exc:
            self.PrintError(self.text2.valueChangeError + ": " + str(exc))
            return 0

    def Configure(
        self,
        key = None,
        subkey = None,
        valueName = None,
        action = 0,
        keyType = None,
        newValue = "",
        disableParsing=False
    ):
        text = self.text
        text2 = self.text2

        if key is None:
            key = Config.lastKeySelected
            subkey = Config.lastSubkeySelected
            valueName = Config.lastValueNameSelected
        else:
            Config.lastKeySelected = key
            Config.lastSubkeySelected = subkey
            Config.lastValueNameSelected = valueName

        panel = eg.ConfigPanel(resizable=True)
        disableParsingBox = panel.CheckBox(
            bool(disableParsing),
            text.disableParsing
        )
        #keyChooser
        regChooserCtrl = RegistryChooser(
            panel,
            -1,
            text2,
            key,
            subkey,
            valueName
        )

        def UpdateLastSelectedKeys(event):
            a, b, c = regChooserCtrl.tree.GetValue()
            Config.lastKeySelected = a
            Config.lastSubkeySelected = b
            Config.lastValueNameSelected = c
            event.Skip()

        regChooserCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, UpdateLastSelectedKeys)

        panel.sizer.Add(regChooserCtrl, 1, flag=wx.EXPAND)
        panel.sizer.Add(wx.Size(5, 5))

        #Action
        actionSizer = wx.BoxSizer(wx.HORIZONTAL)

        choices = len(text.actions)
        rb = range(0, choices)

        actionSizer.Add(
            wx.StaticText(panel, -1, text2.actionText),
            flag=wx.ALIGN_CENTER_VERTICAL
        )

        def OnRadioButton(event):
            #disables elements depending on action selection
            flag = not rb[2].GetValue()
            newValueCtrl.Enable(flag)
            typeChoice.Enable(flag)
            event.Skip()

        rb[0] = wx.RadioButton(panel, -1, text.actions[0], style = wx.RB_GROUP)
        rb[0].SetValue(action == 0)
        actionSizer.Add(rb[0], flag = wx.ALIGN_CENTER_VERTICAL)

        rb[1] = wx.RadioButton(panel, -1, text.actions[1])
        rb[1].SetValue(action == 1)
        actionSizer.Add(rb[1], flag = wx.ALIGN_CENTER_VERTICAL)

        rb[2] = wx.RadioButton(panel, -1, text.actions[2])
        rb[2].SetValue(action == 2)
        actionSizer.Add(rb[2], flag = wx.ALIGN_CENTER_VERTICAL)

        panel.sizer.Add(actionSizer)
        panel.sizer.Add(wx.Size(5, 5))

        #new Value Input
        newValueSizer = wx.FlexGridSizer(2, 4, 5, 5)
        newValueSizer.AddGrowableCol(1)

        newValueSizer.Add(
            wx.StaticText(panel, -1, text2.newValue),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        newValueCtrl = wx.TextCtrl(panel, -1, newValue, size=(200, -1))
        newValueSizer.Add(newValueCtrl, flag = wx.EXPAND)

        newValueSizer.Add(
            wx.StaticText(panel, -1, text2.typeText),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        typeChoice = wx.Choice(panel, -1)
        for i, value in enumerate(regTypes):
            typeChoice.Append(value[1])
            if value[0] == keyType:
                typeChoice.SetSelection(i)

        newValueSizer.Add(typeChoice)
        newValueSizer.Add((-1, -1))
        newValueSizer.Add(disableParsingBox)

        OnRadioButton(wx.CommandEvent())
        rb[0].Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        rb[1].Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        rb[2].Bind(wx.EVT_RADIOBUTTON, OnRadioButton)

        panel.sizer.Add(newValueSizer, flag = wx.EXPAND)

        while panel.Affirmed():
            key, subkey, valueName = regChooserCtrl.GetValue()

            for i, item in enumerate(rb):
                if item.GetValue():
                    action = i
                    break

            keyType = regTypes[typeChoice.GetSelection()][0]

            newValue = newValueCtrl.GetValue()

            panel.SetResult(
                key,
                subkey,
                valueName,
                action,
                keyType,
                newValue,
                disableParsingBox.GetValue()
            )

    def GetLabel(
        self,
        key,
        subkey,
        valueName,
        action,
        keyType,
        newValue,
        disableParsing=False
    ):
        hkey = FullKeyName(key, subkey, valueName)
        if action == 2:
            return self.text.labels[action] % hkey
        return self.text.labels[action] % (hkey, newValue)

    @classmethod
    def OnAddAction(cls):
        cls.text2 = cls.plugin.text.RegistryGroup


class RegistryQuery(eg.ActionBase):
    name = "Query Registry"
    description = (
        "Queries the Windows registry and returns or compares the value."
    )
    iconFile = "icons/Registry"

    class text:
        actions = ("check if exists", "return as result", "compare to")
        labels = (
            'Check if "%s" exists',
            'Return "%s" as result',
            'Compare "%s" with %s'
        )

    def __call__(self, key, subkey, valueName, action, compareValue):
        if not key:  #nothing selected
            return None

        success = False
        try:
            regHandle = _winreg.OpenKey(key, subkey)
            success = True
        except EnvironmentError:
            pass

        #key does not exist or is not readable
        if not success:
            if action == 0:
                return False
            elif action == 1:
                return None
            elif action == 2:
                return False

        #key found and no value specfied
        if valueName is None:
            if action == 0:
                return True
            self.PrintError(self.text2.noValueNameError)
            if action == 1:
                return None
            elif action == 2:
                return False

        #reading value
        try:
            regValue = _winreg.QueryValueEx(regHandle, valueName)
            value = regValue[0]
            if action == 0:
                return True
            elif action == 1:
                return value
            elif action == 2:
                return str(value) == compareValue
        except EnvironmentError:
            if action == 0:
                return False
            elif action == 1:
                return None
            elif action == 2:
                return False

    def Configure(
        self,
        key = None,
        subkey = None,
        valueName = None,
        action = 0,
        compareValue = ""
    ):
        text = self.text
        text2 = self.text2

        if key is None:
            key = Config.lastKeySelected
            subkey = Config.lastSubkeySelected
            valueName = Config.lastValueNameSelected
        else:
            Config.lastKeySelected = key
            Config.lastSubkeySelected = subkey
            Config.lastValueNameSelected = valueName

        panel = eg.ConfigPanel(resizable=True)

        #keyChooser
        regChooserCtrl = RegistryChooser(
            panel,
            -1,
            text2,
            key,
            subkey,
            valueName
        )

        def UpdateLastSelectedKeys(event):
            a, b, c = regChooserCtrl.tree.GetValue()
            Config.lastKeySelected = a
            Config.lastSubkeySelected = b
            Config.lastValueNameSelected = c
            event.Skip()

        regChooserCtrl.tree.Bind(
            wx.EVT_TREE_SEL_CHANGED, UpdateLastSelectedKeys
        )

        panel.sizer.Add(regChooserCtrl, 1, flag=wx.EXPAND)
        panel.sizer.Add(wx.Size(5, 5))

        choices = len(text.actions)
        rb = range(0, choices)
        sizer2 = wx.FlexGridSizer(1, choices + 2, 5, 5)
        sizer2.AddGrowableCol(4)

        sizer2.Add(
            wx.StaticText(panel, -1, text2.actionText),
            flag=wx.ALIGN_CENTER_VERTICAL
        )

        def OnRadioButton(event):
            flag = rb[2].GetValue()
            compareValueCtrl.Enable(flag)
            event.Skip()

        rb[0] = wx.RadioButton(
            panel,
            -1,
            text.actions[0],
            style = wx.RB_GROUP
        )
        rb[0].SetValue(action == 0)
        sizer2.Add(rb[0], flag = wx.ALIGN_CENTER_VERTICAL)

        rb[1] = wx.RadioButton(panel, -1, text.actions[1])
        rb[1].SetValue(action == 1)
        sizer2.Add(rb[1], flag = wx.ALIGN_CENTER_VERTICAL)

        rb[2] = wx.RadioButton(panel, -1, text.actions[2])
        rb[2].SetValue(action == 2)
        sizer2.Add(rb[2], flag = wx.ALIGN_CENTER_VERTICAL)

        compareValueCtrl = wx.TextCtrl(panel, -1, compareValue, size=(200, -1))
        sizer2.Add(compareValueCtrl, flag = wx.EXPAND)

        OnRadioButton(wx.CommandEvent())
        rb[0].Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        rb[1].Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        rb[2].Bind(wx.EVT_RADIOBUTTON, OnRadioButton)

        panel.sizer.Add(sizer2, flag = wx.EXPAND)

        while panel.Affirmed():
            key, subkey, valueName = regChooserCtrl.GetValue()
            compareValue = compareValueCtrl.GetValue()
            for i in range(0, 3):
                if rb[i].GetValue():
                    action = i
                    break
            panel.SetResult(key, subkey, valueName, action, compareValue)

    def GetLabel(self, key, subkey, valueName, action, compareValue):
        hkey = FullKeyName(key, subkey, valueName)
        if action == 2:
            return self.text.labels[action] % (hkey, compareValue)
        return self.text.labels[action] % hkey

    @classmethod
    def OnAddAction(cls):
        cls.text2 = cls.plugin.text.RegistryGroup


class RegistryChooser(wx.Window):
    def __init__(
        self,
        parent,
        id = -1,
        text = None,
        key = _winreg.HKEY_CURRENT_USER,
        subkey = "Software",
        valueName = None,
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        style = wx.EXPAND
    ):
        self.text = text
        wx.Window.__init__(self, parent, id, pos, size, style)
        sizer = wx.GridBagSizer(5, 5)

        sizer.SetEmptyCellSize((0, 0))
        sizer.Add(
            wx.StaticText(self, -1, text.chooseText),
            (0, 0),
            (1, 6),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        sizer.Add(
            wx.StaticText(self, -1, text.keyText),
            (2, 0),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        #key
        keyChoice = wx.Choice(self, -1)
        for i in range(0, len(regKeys)):
            keyChoice.Append(regKeys[i][1])
            if regKeys[i][0] == key:
                keyChoice.SetSelection(i)
        sizer.Add(keyChoice, (2, 1))

        sizer.Add(
            wx.StaticText(self, -1, "\\"),
            (2, 2),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        #subkey
        subkeyCtrl = wx.TextCtrl(self, -1, subkey, size=(200, -1))
        sizer.Add(subkeyCtrl, (2, 3), flag = wx.EXPAND)

        sizer.Add(
            wx.StaticText(self, -1, text.valueName),
            (2, 4),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        #old Value
        sizer.Add(
            wx.StaticText(self, -1, text.oldValue),
            (3, 0),
            flag = wx.ALIGN_CENTER_VERTICAL
        )
        self.oldValueCtrl = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.oldValueCtrl.Enable(False)
        sizer.Add(
            self.oldValueCtrl,
            (3, 1),
            (1, 3),
            flag = wx.EXPAND
        )
        sizer.Add(
            wx.StaticText(self, -1, text.oldType),
            (3, 4),
            flag = wx.ALIGN_CENTER_VERTICAL
        )
        self.oldTypeCtrl = wx.TextCtrl(self, -1)
        self.oldTypeCtrl.Enable(False)
        sizer.Add(
            self.oldTypeCtrl,
            (3, 5),
            flag = wx.EXPAND
        )
        self.FillOldValue(key, subkey, valueName)

        #Create TreeCtrl
        tree = RegistryLazyTree(self, -1, key, subkey, valueName, text=text)
        sizer.Add(tree, (1, 0), (1, 6), flag = wx.EXPAND)

        if valueName is None:
            valueName = ""
        elif len(valueName) == 0:
            valueName = text.defaultText
        valueNameCtrl = wx.TextCtrl(self, -1, valueName, size=(100, -1))
        sizer.Add(valueNameCtrl, (2, 5), flag = wx.EXPAND)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(3, 2)
        sizer.AddGrowableCol(5, 1)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()
        self.SetMinSize(self.GetSize())

        self.keyChoice = keyChoice
        self.subkeyCtrl = subkeyCtrl
        self.valueNameCtrl = valueNameCtrl
        self.tree = tree
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelect)
        self.subkeyCtrl.Bind(wx.EVT_TEXT, self.OnSubkeyEnter)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def FillOldValue(self, key, subkey, valueName):
        curType = None
        curValue = None
        if valueName is not None:
            try:
                regHandle = _winreg.OpenKey(key, subkey)
                regValue = _winreg.QueryValueEx(regHandle, valueName)
                _winreg.CloseKey(regHandle)
                for i in range(1, len(regTypes)):
                    if regTypes[i][0] == regValue[1]:
                        curType = regTypes[i][1]
                        break
            except EnvironmentError:
                curType = ""
                curValue = self.text.noValueText
            if len(curType) > 0:
                try:
                    curValue = unicode(regValue[0])
                except:
                    #convert to hex
                    curValue = "0x" + binascii.hexlify(regValue[0]).upper()
        else:
            curType = self.text.keyText2
            curValue = ""

        self.oldValueCtrl.SetValue(str(curValue))
        self.oldTypeCtrl.SetValue(curType)

    def GetValue(self):
        #key
        key = regKeys[self.keyChoice.GetSelection()][0]

        #subkey
        subkey = self.subkeyCtrl.GetValue()

        #valueName
        valueName = self.valueNameCtrl.GetValue()
        if len(valueName) == 0:
            valueName = None
        elif valueName == self.text.defaultText:
            valueName = ""

        return key, subkey, valueName

    def OnSize(self, dummyEvent):
        if self.GetAutoLayout():
            self.Layout()

    def OnSubkeyEnter(self, event):
        value = self.subkeyCtrl.GetValue()
        if value.startswith("HK") and value.count("\\") > 0:
            #probably a whole key pasted
            tmp = value.split("\\", 1)
            key = tmp[0].upper()  #get first part
            value = tmp[1]
            for i in range(0, len(regKeys)):
                if regKeys[i][1] == key or regKeys[i][2] == key:
                    self.keyChoice.SetSelection(i)
                    self.subkeyCtrl.SetValue(value)
                    break
        event.Skip()

    def OnTreeSelect(self, event):
        key, subkey, valueName = self.tree.GetValue()
        if key is not None:  #change only if not root node
            if valueName is None:
                self.valueNameCtrl.SetValue("")
            elif len(valueName) == 0:
                self.valueNameCtrl.SetValue(self.text.defaultText)
            else:
                self.valueNameCtrl.SetValue(valueName)
            self.subkeyCtrl.SetValue(subkey)
            for i in range(0, len(regKeys)):
                if regKeys[i][0] == key:
                    self.keyChoice.SetSelection(i)
                    break
        self.FillOldValue(key, subkey, valueName)
        event.Skip()


class RegistryLazyTree(wx.TreeCtrl):
    def __init__(
        self,
        parent,
        id=-1,
        key = _winreg.HKEY_CURRENT_USER,
        subkey = "Software",
        valueName = None,
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        style = wx.TR_HAS_BUTTONS,
        validator = wx.DefaultValidator,
        name="RegistryLazyTree",
        text = None
    ):
        self.text = text
        wx.TreeCtrl.__init__(
            self, parent, id, pos, size, style, validator, name
        )

        self.imageList = imageList = wx.ImageList(16, 16)
        rootIcon = imageList.Add(eg.Icons.GetInternalBitmap("root"))
        self.folderIcon = imageList.Add(eg.Icons.GetInternalBitmap("folder"))
        self.valueIcon = imageList.Add(eg.Icons.GetInternalBitmap("action"))
        self.SetImageList(imageList)
        self.SetMinSize((-1, 200))
        self.treeRoot = self.AddRoot(
            "Registry",
            image = rootIcon,
            data = wx.TreeItemData((True, None, None, None))
        )
        #Adding keys
        for item in regKeys:
            #a tupel of 4 values is assigned to every item
            #1) stores if the key has yet to be queried for subkey, when
            #   selected
            #2) _winreg.hkey constant
            #3) name of the key
            #4) value name, None if just a key, empty string for default value
            tmp = self.AppendItem(
                self.treeRoot,
                item[1],
                image = self.folderIcon,
                data =wx.TreeItemData((False, item[0], "", None))
            )
            self.SetItemHasChildren(tmp, True)
            if item[0] == key:
                self.SelectItem(tmp)

        #select old value in tree
        self.OnTreeChange(wx.CommandEvent(), key, subkey, valueName)
        self.EnsureVisible(self.GetSelection())

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeChange)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandNode)

    def GetValue(self):
        data = self.GetItemData(self.GetSelection()).GetData()
        return data[1], data[2], data[3]

    def OnExpandNode(self, event):
        self.OnTreeChange(event, node = event.GetItem())

    def OnTreeChange(
        self,
        event,
        key2Select = None,
        subkey2Select = None,
        valueName2Select = None,
        node = None
    ):
        if not node:
            node = self.GetSelection()

        keyHasBeenQueried, fatherKey, \
            fatherSubkey, fatherValueName = self.GetItemData(node).GetData()
        subkey2Find = None
        newItemSelected = False

        if not keyHasBeenQueried:  #check for subkeys
            self.SetItemData(
                node,
                wx.TreeItemData(
                    (True, fatherKey, fatherSubkey, fatherValueName)
                )
            )

            #buildung tree
            try:
                regHandle = _winreg.OpenKey(fatherKey, fatherSubkey)
            except EnvironmentError, exc:
                eg.PrintError(self.text.keyOpenError + ": " + str(exc))
                return 0

            #query subkeys
            if len(fatherSubkey) == 0:
                parentSubkey = ""
            else:
                parentSubkey = fatherSubkey + "\\"

            #preparing strings to find the subkey2Select key
            if valueName2Select:
                valueName2Select = valueName2Select.lower()
            if subkey2Select:
                subkey2Select = subkey2Select.lower()
            if key2Select and subkey2Select and key2Select == fatherKey:
                length = len(fatherSubkey)
                if subkey2Select[0:length] == fatherSubkey.lower():
                    subkey2Find = subkey2Select[length:]
                    if subkey2Find.startswith("\\"):
                        subkey2Find = subkey2Find[1:]
                    subkeys = subkey2Find.split("\\", 1)
                    subkey2Find = subkeys[0]

            #building Tree
            keyNames, valueList = RegEnumKeysAndValues(regHandle.handle)

            #sorting
            keyNames.sort(lambda a, b: cmp(a[0].lower(), b[0].lower()))
            valueList.sort(lambda a, b: cmp(a[0].lower(), b[0].lower()))

            #subkeys
            for keyName, numSubKeys, numSubValues in keyNames:
                hasChildren = bool(numSubKeys + numSubValues > 0)
                data = (
                    not hasChildren,
                    fatherKey,
                    parentSubkey + keyName,
                    None
                )
                tmp = self.AppendItem(
                    node,
                    keyName,
                    image=self.folderIcon,
                    data=wx.TreeItemData(data)
                )
                if subkey2Find == keyName.lower():
                    newItemSelected = True
                    self.SelectItem(tmp)
                self.SetItemHasChildren(tmp, hasChildren)

            #values
            for valueName, valueType in valueList:
                if len(valueName) == 0:
                    enumValueName = self.text.defaultText
                else:
                    enumValueName = valueName
                data = (True, fatherKey, fatherSubkey, valueName)
                tmp = self.AppendItem(
                    node,
                    enumValueName,
                    image = self.valueIcon,
                    data = wx.TreeItemData(data)
                )
                if (
                    valueName2Select is not None and
                    valueName.lower() == valueName2Select and
                    subkey2Select == fatherSubkey.lower()
                ):
                    newItemSelected = True
                    self.SelectItem(tmp)

        if newItemSelected:
            self.OnTreeChange(
                wx.CommandEvent(),
                key2Select,
                subkey2Select,
                valueName2Select
            )
        event.Skip()


def FullKeyName(key, subkey, valueName, maxSubkeyLength=15):
    label = "root"
    if not key:
        return label

    for i in range(0, len(regKeys)):
        if regKeys[i][0] == key:
            label = regKeys[i][2]
            break

    if not subkey:
        return label

    if (
        maxSubkeyLength and
        len(subkey) > maxSubkeyLength and
        subkey.count("\\") != 0
    ):
        label += "\\...\\" + subkey.rsplit("\\", 1)[1]
    else:
        label += "\\" + subkey

    if valueName is None:
        return label
    elif len(valueName) == 0:
        return label + "\\" + Text.RegistryGroup.defaultText
    else:
        return label + "\\" + valueName
