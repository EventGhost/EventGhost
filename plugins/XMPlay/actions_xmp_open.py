# -*- coding: utf-8 -*-
#

from os import path

import wx

import eg
from . import utils_xmp
from . import actions_xmp_dde


class Add(utils_xmp.TextSetter):

    def __call__(self, value="", from_eg_result=False):
        if from_eg_result:
            value = str(eg.result)
        if self.plugin.is_xmp_off(): return False
        self.plugin.dde_get_conversation("System").execute("[list(%s)]" % value)
        return True
        
        

class Open(utils_xmp.TextSetter):

    def __call__(self, value="", from_eg_result=False):
        if from_eg_result:
            value = str(eg.result)
        if self.plugin.is_xmp_off(): return False
        self.plugin.dde_get_conversation("System").execute("[open(%s)]" % value)
        return True
             

            
class OpenFileFolder(eg.ActionBase):

    class text:
        label1 = "List of audio files, playlists and folders:"
        toolTipList = """If some row is marked (selected),
the new item(s) is (are) inserted in its position.
Otherwise a new entry is inserted at the end of the list.
Row can be selected with the left mouse button
and unselected with the right mouse button.
In addition to audio files, playlists and folders,
you can also insert Python expression such as {eg.result}.
Then you can use for example OSE plugin to play
the selected directory!"""
        elements = (
            '',
            'File(s) or playlist(s)',
            'Folder',
            'Python expression "{eg.result}"',
            'Python expression "{eg.event.payload}"',
            'Other Python expression'
        )
        clear = "Clear all"
        delete = "Delete item"
        wildcards = """
            XMPlay-able or playlists|*.ogg;*.mp3;*.mp2;*.mp1;*.wma;*.wav;*.aac;*.mp4;*.m4a;*.m4b;*.cda;*.mo3;*.it;*.xm;*.s3m;*.mtm;*.mod;*.umx;*.pls;*.m3u;*.asx;*.wax|
            XMPlay-able|*.ogg;*.mp3;*.mp2;*.mp1;*.wma;*.wav;*.aac;*.mp4;*.m4a;*.m4b;*.cda;*.mo3;*.it;*.xm;*.s3m;*.mtm;*.mod;*.umx|
            Playlists (pls/m3u/asx/wax)|*.pls;*.m3u;*.asx;*.wax|
            Modules (mo3/it/xm/s3m/mtm/mod/umx)|*.mo3;*.it;*.xm;*.s3m;*.mtm;*.mod;*.umx|
            Ogg Vorbis (ogg)|*.ogg|
            MPEG (mp3/mp2/mp1)|*.mp3;*.mp2;*.mp1|
            WAVE (wav)|*.wav|
            Advanced Audio Coding (aac/mp4/m4a/m4b)|*.aac;*.mp4;*.m4a;*.m4b|
            CD audio (cda)|*.cda|
            Windows Media Audio (wma)|*.wma|
            All files (*.*)|*.*
        """
        radioboxtitle = "Action with selected files"
        modes = (
            "Replace current playlist",
            "Add to current playlist"
        )
        choiceLbl = "Choose item (file, playlist, folder ...) to insert"
        caption = "Please enter text"
        message = 'Python expression - for example {eg.event.suffix} :'

    def __call__(self, filepath, mode):
        if self.plugin.is_xmp_off():
            return False
        fp = eg.ParseString(filepath[0])
        if path.isfile(fp) or path.isdir(fp):
            self.plugin.dde_get_conversation("System").execute("[%s(%s)]" % (("open", "list")[mode], fp))
            print "[%s(%s)]" % (("open", "list")[mode], fp)
        if len(filepath) > 1:
            for fp in filepath[1:]:
                fp = eg.ParseString(fp)
                if path.isfile(fp) or path.isdir(fp):
                    self.plugin.dde_get_conversation("System").execute("[%s(%s)]" % ("list", fp))

    def Configure(self, filepath = [], mode=0):
        if filepath:
            self.startDir = path.split(filepath[0])[0]
        elif hasattr(eg.folderPath, "Music"): # W2k has not
            self.startDir = eg.folderPath.Music
        else:
            self.startDir = ""
        text = self.text
        panel = eg.ConfigPanel(resizable=True)
        radioBox = wx.RadioBox(
            panel,
            -1,
            text.radioboxtitle,
            choices = text.modes,
            style=wx.RA_SPECIFY_COLS
        )
        radioBox.SetSelection(mode)
        label1Text = wx.StaticText(panel, -1, text.label1)
        pathCtrl = wx.ListBox(
            panel,
            -1,
            choices = filepath,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        pathCtrl.SetToolTip(text.toolTipList)
        buttonSizer = wx.GridBagSizer(2, 10)
        elemCtrl = wx.Choice(panel, -1, choices=text.elements)
        clearButton = wx.Button(panel, -1, text.clear)
        deleteButton = wx.Button(panel, -1, text.delete)
        choiceLabel = wx.StaticText(panel, -1, text.choiceLbl)
        buttonSizer.Add(choiceLabel, (0, 0))
        buttonSizer.Add(elemCtrl, (1, 0), flag = wx.EXPAND)
        buttonSizer.Add(deleteButton, (1, 2))
        buttonSizer.Add(clearButton, (1, 4))
        buttonSizer.AddGrowableCol(1)
        buttonSizer.AddGrowableCol(3)
        panel.sizer.Add(label1Text, 0)
        panel.sizer.Add(pathCtrl, 1, wx.TOP|wx.EXPAND)
        panel.sizer.Add(buttonSizer, 0, wx.TOP|wx.EXPAND, 10)
        panel.sizer.Add(radioBox, 0, wx.EXPAND|wx.TOP, 10)

        def EnableButtons():
            if pathCtrl.GetSelection() > -1:
                deleteButton.Enable(True)
            else:
                deleteButton.Enable(False)
            if pathCtrl.GetCount() == 0:
                clearButton.Enable(False)
            else:
                clearButton.Enable(True)

        EnableButtons()

        def OnPathCtrl(event):
            EnableButtons()
            event.Skip()
        pathCtrl.Bind(wx.EVT_LISTBOX, OnPathCtrl)

        def OnPathCtrlRightClick(event):
            pathCtrl.SetSelection(-1)
            EnableButtons()
            event.Skip()
        pathCtrl.Bind(wx.EVT_RIGHT_DOWN, OnPathCtrlRightClick)

        def OnElemCtrl(event):
            pos = pathCtrl.GetSelection()
            if pos == -1:
                sel = pathCtrl.GetCount()
            else:
                sel = pos
            ix = event.GetSelection()
            if ix == 1:
                fileDialog = wx.FileDialog(
                    panel,
                    message=text.elements[1],
                    wildcard=text.wildcards,
                    defaultDir = self.startDir,
                    style=wx.OPEN|wx.FD_MULTIPLE
                )
                try:
                    if fileDialog.ShowModal() == wx.ID_OK:
                        val = fileDialog.GetPaths()
                        self.startDir = path.split(val[0])[0]
                        pathCtrl.InsertItems(val, sel)
                        if pos > -1:
                            pathCtrl.SetSelection(sel)
                finally:
                    fileDialog.Destroy()
            elif ix == 2:
                folderDialog = wx.DirDialog(
                    panel,
                    message="",
                    defaultPath = self.startDir,
                    style=wx.DD_DIR_MUST_EXIST
                )
                try:
                    if folderDialog.ShowModal() == wx.ID_OK:
                        val = folderDialog.GetPath()
                        pathCtrl.InsertItems([val,], sel)
                        if pos > -1:
                            pathCtrl.SetSelection(sel)
                        self.startDir = val
                finally:
                    folderDialog.Destroy()
            elif ix in (3, 4):
                item = text.elements[ix]
                pathCtrl.InsertItems([item[item.find('"')+1:-1],], sel)
                if pos > -1:
                    pathCtrl.SetSelection(sel)
            elif ix == 5:
                dlg = wx.TextEntryDialog(
                    panel,
                    text.message,
                    text.caption,
                    "",
                    wx.OK | wx.CANCEL | wx.CENTRE,
                    wx.DefaultPosition
                )
                if dlg.ShowModal() == wx.ID_OK:
                    val = dlg.GetValue()
                    if val:
                        if val[0] != "{":
                            val = "{" + val
                        if val[-1] != "}":
                            val = val + "}"
                        pathCtrl.InsertItems([val,], sel)
                        if pos > -1:
                            pathCtrl.SetSelection(sel)
                dlg.Destroy()
            elemCtrl.SetSelection(0)
            EnableButtons()
            event.Skip()
        elemCtrl.Bind(wx.EVT_CHOICE, OnElemCtrl)

        def OnDeleteButton(event):
            sel = pathCtrl.GetSelection()
            if sel > -1:
                pathCtrl.Delete(sel)
                length = pathCtrl.GetCount()
                if length == sel:
                    sel -= 1
                if sel > -1:
                    pathCtrl.SetSelection(sel)
            EnableButtons()
            event.Skip()
        deleteButton.Bind(wx.EVT_BUTTON, OnDeleteButton)

        def OnClearButton(event):
            pathCtrl.Set([])
            EnableButtons()
            event.Skip()
        clearButton.Bind(wx.EVT_BUTTON, OnClearButton)

        while panel.Affirmed():
            panel.SetResult(
                pathCtrl.GetStrings(), radioBox.GetSelection()
            )
