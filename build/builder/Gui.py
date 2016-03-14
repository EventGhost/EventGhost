# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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


import sys
import threading
import wx

import builder
from Utils import GetRevision

class MainDialog(wx.Dialog):

    def __init__(self, buildSetup):
        self.buildSetup = buildSetup
        wx.Dialog.__init__(
            self, None, title="Build %s Installer" % buildSetup.name
        )

        # create controls
        self.ctrls = {}
        ctrlsSizer = wx.BoxSizer(wx.VERTICAL)
        for task in buildSetup.tasks:
            if not task.visible:
                continue
            section = task.GetId()
            ctrl = wx.CheckBox(self, -1, task.description)
            ctrl.SetValue(task.activated)
            ctrlsSizer.Add(ctrl, 0, wx.ALL, 5)
            self.ctrls[section] = ctrl
            if not task.enabled:
                ctrl.Enable(False)

        self.okButton = wx.Button(self, wx.ID_OK)
        self.okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.okButton.SetDefault()
        self.cancelButton = wx.Button(self, wx.ID_CANCEL)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        # add controls to sizers
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.AddButton(self.okButton)
        btnSizer.AddButton(self.cancelButton)
        btnSizer.Realize()

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(ctrlsSizer)

        # create controls for github connection
        ghSzr = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"GitHub"), wx.VERTICAL)
        sb = self  # <- wx=2.8, wx>=2.9 -> ghSzr.GetStaticBox()

        lblRepo = wx.StaticText(sb, wx.ID_ANY, u"Repository:")
        self.chcRepo = wx.Choice(sb, wx.ID_ANY)
        repos = buildSetup.gitConfig["all_repos"].keys()
        self.chcRepo.SetItems(repos)
        self.chcRepo.SetStringSelection(buildSetup.gitConfig["repo_full"])
        self.chcRepo.Bind(wx.EVT_CHOICE, self.OnRepoSelection)

        lblBranch = wx.StaticText(sb, wx.ID_ANY, u"Branch:")
        self.chcBranch = wx.Choice(sb, wx.ID_ANY)
        self.chcBranch.SetItems(
            buildSetup.gitConfig["all_repos"]
            [buildSetup.gitConfig["repo_full"]]["all_branches"]
        )
        self.chcBranch.SetStringSelection(
            buildSetup.gitConfig["all_repos"]
            [buildSetup.gitConfig["repo_full"]]["def_branch"]
        )

        grdSzr = wx.FlexGridSizer(0, 2, 0, 0)
        grdSzr.SetFlexibleDirection(wx.BOTH)
        grdSzr.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        grdSzr.Add(lblRepo, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        grdSzr.Add(self.chcRepo, 0, wx.ALL, 5)
        grdSzr.Add(lblBranch, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        grdSzr.Add(self.chcBranch, 0, wx.ALL, 5)
        ghSzr.Add(grdSzr, 1, wx.EXPAND)

        egSzr = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "EventGhost"), wx.HORIZONTAL)

        sb = self  # <- wx=2.8, wx>=2.9 -> egSzr.GetStaticBox()
        lblVersion = wx.StaticText(sb, wx.ID_ANY, "Version to build:")
        self.versionStr = wx.TextCtrl(sb, wx.ID_ANY,
                                      value=buildSetup.appVersion)
        refreshVersion = wx.BitmapButton(sb, wx.ID_ANY, wx.ArtProvider.
                                         GetBitmap(wx.ART_GO_DOWN))
        refreshVersion.SetToolTip(wx.ToolTip(
            'Get Version from GitHub. Before using,\n'
            'please fill the github section above.'))
        refreshVersion.Bind(wx.EVT_BUTTON, self.RefreshVersion)

        egSzr.Add(lblVersion, 0, wx.ALIGN_CENTER_VERTICAL |
                  wx.LEFT | wx.RIGHT, 5 )
        egSzr.Add(self.versionStr, 0, wx.ALIGN_CENTER_VERTICAL |
                  wx.LEFT | wx.RIGHT, 5)
        egSzr.Add(refreshVersion, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

        # combine all controls to a main sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(ghSzr, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        mainSizer.Add(egSzr, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        mainSizer.Add(sizer2, 1, wx.ALL | wx.EXPAND, 10)
        mainSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        self.SetSizerAndFit(mainSizer)
        self.Center()
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def OnOk(self, dummyEvent):
        """ Handles a click on the Ok button. """
        repository = self.chcRepo.GetStringSelection()
        try:
            user, repo = repository.split('/')
        except ValueError:
            dlg = wx.MessageDialog(self, caption="Information", style=wx.OK,
                            message="Repositoryname not valid. Must be:\n"
                            "<user or organization>/<repository>.")
            rc = dlg.ShowModal()
            return

        self.okButton.Enable(False)
        self.cancelButton.Enable(False)
        #self.SetWindowStyleFlag(wx.CAPTION|wx.RESIZE_BORDER)
        for task in self.buildSetup.tasks:
            if not task.visible:
                continue
            section = task.GetId()
            if section in self.ctrls:
                ctrl = self.ctrls[section]
                task.activated = ctrl.GetValue()
                ctrl.Enable(False)
        self.buildSetup.appVersion = self.versionStr.GetValue()
        self.buildSetup.gitConfig.update({
            "user": user,
            "repo": repo,
            "branch": self.chcBranch.GetStringSelection(),
            })
        self.buildSetup.config.SaveSettings()
        thread = threading.Thread(target=self.DoMain)
        thread.start()


    def DoMain(self):
        builder.Tasks.Main(self.buildSetup)
        wx.CallAfter(self.OnExit)


    def OnExit(self):
        self.Destroy()
        sys.exit(0)


    def OnCancel(self, event):
        """ Handles a click on the cancel button. """
        event.Skip()
        self.Destroy()
        wx.GetApp().ExitMainLoop()


    def OnClose(self, event):
        """ Handles a click on the close box of the frame. """
        event.Skip()
        self.Destroy()
        wx.GetApp().ExitMainLoop()


    def RefreshVersion(self, event):
        GetRevision(self.buildSetup)
        self.versionStr.SetValue(self.buildSetup.appVersion)


    def OnRepoSelection(self, event):
        key = self.chcRepo.GetStringSelection()
        self.chcBranch.SetItems(
            self.buildSetup.gitConfig["all_repos"][key]["all_branches"]
        )
        self.chcBranch.SetStringSelection(
            self.buildSetup.gitConfig["all_repos"][key]["def_branch"]
        )

def Main(buildSetup):
    app = wx.App(0)
    app.SetExitOnFrameDelete(True)
    mainDialog = MainDialog(buildSetup)
    mainDialog.Show()
    app.MainLoop()

