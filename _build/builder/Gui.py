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

import sys
import threading
import time
from Queue import Queue

# Local imports
import builder
from builder.Utils import GetVersion, ParseVersion


_stdout = None
_stderr = None

class CtrlWriter(threading.Thread):

    def __init__(self, ctrl):
        self._ctrl = ctrl
        self._queue = Queue()
        self._scroll_queue = []
        threading.Thread.__init__(self)
        self.daemon = True
        self.scroll_position = 0

    def run(self):
        import wx

        global old_scroll_position
        char_height = self._ctrl.GetCharHeight()

        old_scroll_position = self.scroll_position

        try:
            while True:
                def do():
                    global old_scroll_position

                    # self._ctrl.Freeze()

                    shown_lines = int(
                        self._ctrl.GetSizeTuple()[1] / char_height
                    )
                    if new_scroll_position is None:
                        scroll_pos = old_scroll_position
                    else:
                        scroll_pos = new_scroll_position

                    scroll_line = self._ctrl.PositionToXY(scroll_pos)[1]

                    stop_pos = self._ctrl.GetLastPosition()
                    page_stop = self._ctrl.PositionToXY(stop_pos)[1]
                    page_start = page_stop - shown_lines

                    if page_start < 0:
                        page_start -= page_start
                        page_start, page_stop = page_stop, page_start

                    # _stdout.write(
                    #     str(page_start) + ' : ' + str(page_stop) + ' : ' + str(
                    #         scroll_line))

                    self._ctrl.SetInsertionPointEnd()
                    if text is not None:
                        self._ctrl.WriteText(text)

                    if color is not None:
                        self._ctrl.SetStyle(
                            stop_pos,
                            stop_pos + len(text),
                            wx.TextAttr(wx.Colour(*color))
                        )

                    if page_start <= 0 or page_start <= scroll_line <= page_stop:
                        self._ctrl.SetInsertionPoint(
                            self._ctrl.GetLastPosition()
                        )
                        old_scroll_position = self.scroll_position = (
                            self._ctrl.GetLastPosition()
                        )
                    else:
                        old_scroll_position = scroll_pos
                        self._ctrl.SetInsertionPoint(scroll_pos)
                    # self._ctrl.Thaw()

                text = None
                color = None

                while self._scroll_queue:
                    new_scroll_position = self._scroll_queue.pop()
                    do()

                new_scroll_position = None

                if not self._queue.empty():
                    text, color = self._queue.get()
                    self._queue.task_done()
                    do()
        except:
            pass

    def put(self, text, color=None):
        self._queue.put((text, color))

    def put_scroll(self, scroll):
        self._scroll_queue += [scroll]


class GUIStdOut:

    def __init__(self, ctrl):
        self._ctrl = ctrl

    def write(self, data):
        self._ctrl.put(data)

    def __getattr__(self, item):
        return getattr(_stdout, item)


class GUIStdErr:

    def __init__(self, ctrl):
        self._ctrl = ctrl

    def write(self, data):
        self._ctrl.put(data, (255, 0, 0))

    def __getattr__(self, item):
        return getattr(_stderr, item)


def Main(buildSetup):
    from CheckDependencies import DEPENDENCIES, PIPDependency

    pip_dep = PIPDependency()
    try:
        pip_dep.Check()
    except:
        if buildSetup.download_dependencies:
            pip_dep.Download()
            pip_dep.Check()
        else:
            raise
    try:
        DEPENDENCIES[-1].Check()
    except:
        if buildSetup.download_dependencies:
            DEPENDENCIES[-1].Download()
            DEPENDENCIES[-1].Check()
        else:
            raise

    import wx

    class MainDialog(wx.Frame):
        def __init__(self, buildSetup):
            self.buildSetup = buildSetup
            wx.Frame.__init__(
                self,
                None,
                title="Build %s Installer" % buildSetup.name,
            )

            # create controls
            self.ctrls = {}
            ctrlsSizer = wx.BoxSizer(wx.HORIZONTAL)
            leftSizer = wx.BoxSizer(wx.VERTICAL)
            rightSizer = wx.BoxSizer(wx.VERTICAL)
            self.download_dependencies_ctrl = wx.CheckBox(
                self,
                -1,
                'Download Dependencies'
            )
            self.download_dependencies_ctrl.SetValue(buildSetup.download_dependencies)
            leftSizer.Add(self.download_dependencies_ctrl, 0, wx.ALL, 5)
            self.download_dependencies_ctrl.Bind(
                wx.EVT_CHECKBOX,
                self.OnDownloadDependencies
            )

            for i, task in enumerate(buildSetup.tasks):
                if not task.visible:
                    continue
                section = task.GetId()
                ctrl = wx.CheckBox(self, -1, task.description)
                if section.endswith(".BuildInstaller"):
                    checked = task.activated
                    ctrl.Bind(wx.EVT_CHECKBOX, self.OnInstallerCheck)
                ctrl.SetValue(task.activated)
                if i < 7:
                    leftSizer.Add(ctrl, 0, wx.ALL, 5)
                else:
                    rightSizer.Add(ctrl, 0, wx.ALL, 5)
                self.ctrls[section] = ctrl
                if not task.enabled:
                    ctrl.Enable(False)

            if checked:
                self.OnInstallerCheck(True)

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

            ctrlsSizer.Add(leftSizer)
            ctrlsSizer.Add(rightSizer)

            sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer2.Add(ctrlsSizer)

            # create controls for github connection
            ghSzr = wx.StaticBoxSizer(
                wx.StaticBox(self, wx.ID_ANY, u"GitHub"), wx.VERTICAL)
            sb = ghSzr.GetStaticBox()

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
            grdSzr.Add(self.chcRepo, 0, wx.ALL | wx.EXPAND, 5)
            grdSzr.Add(lblBranch, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
            grdSzr.Add(self.chcBranch, 0, wx.ALL | wx.EXPAND, 5)
            grdSzr.AddGrowableCol(1)
            ghSzr.Add(grdSzr, 1, wx.EXPAND)

            if not self.buildSetup.gitConfig["token"]:
                sb.Disable()

            egSzr = wx.StaticBoxSizer(
                wx.StaticBox(self, wx.ID_ANY, "EventGhost"), wx.HORIZONTAL)

            sb = egSzr.GetStaticBox()
            lblVersion = wx.StaticText(sb, wx.ID_ANY, "Version to build:")
            self.versionStr = wx.TextCtrl(sb, wx.ID_ANY)
            self.UpdateVersion()

            refreshVersion = wx.BitmapButton(sb, wx.ID_ANY, wx.ArtProvider.
                                             GetBitmap(wx.ART_GO_DOWN))
            refreshVersion.SetToolTip(wx.ToolTip(
                'Get Version from GitHub. Before using,\n'
                'please fill the github section above.'))
            refreshVersion.Bind(wx.EVT_BUTTON, self.OnRefreshVersion)

            if not self.buildSetup.gitConfig["token"]:
                sb.Disable()

            egSzr.Add(lblVersion, 0, wx.ALIGN_CENTER_VERTICAL |
                      wx.LEFT | wx.RIGHT, 5)
            egSzr.Add(self.versionStr, 1, wx.ALIGN_CENTER_VERTICAL |
                      wx.LEFT | wx.RIGHT, 5)
            egSzr.Add(refreshVersion, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

            if not self.buildSetup.gitConfig["token"]:
                refreshVersion.Disable()

            # widgets for website updating
            web_szr = wx.StaticBoxSizer(
                wx.StaticBox(self, wx.ID_ANY, u"Website (docs)"), wx.VERTICAL)
            sb = web_szr.GetStaticBox()
            url_txt = 'URL (sftp://<user>:<pw>@<domain.net>:' \
                      '<port>/<root/of/website>/)'
            lbl_url = wx.StaticText(
                parent=sb,
                label=url_txt
            )

            lbl_url.SetToolTip(wx.ToolTip(url_txt))
            self.url = wx.TextCtrl(sb, value=self.buildSetup.args.websiteUrl)
            self.url.SetToolTip(wx.ToolTip(url_txt))
            web_szr.Add(lbl_url)
            web_szr.Add(self.url, 0, wx.EXPAND)

            loggingCtrl = self.loggingCtrl = wx.TextCtrl(
                self,
                -1,
                '',
                style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_RICH2,
                size=(-1, 200)
            )
            loggingCtrl.HideNativeCaret()

            global _stdout
            global _stderr

            _stdout = sys.stdout
            _stderr = sys.stderr

            ctrl_writer = CtrlWriter(loggingCtrl)

            sys.stdout = GUIStdOut(ctrl_writer)
            sys.stderr = GUIStdErr(ctrl_writer)

            def on_scroll(evt):
                if evt.GetOrientation() == wx.VERTICAL:
                    ctrl_writer.put_scroll(evt.GetPosition())
                evt.Skip()

            loggingCtrl.Bind(wx.EVT_SCROLLWIN, on_scroll)
            loggingCtrl.Bind(wx.EVT_SCROLL, on_scroll)

            def on_bottom(evt):
                if evt.GetOrientation() == wx.VERTICAL:
                    ctrl_writer.put_scroll(100000000)
                evt.Skip()

            loggingCtrl.Bind(wx.EVT_SCROLL_BOTTOM, on_bottom)
            loggingCtrl.Bind(wx.EVT_SCROLLWIN_BOTTOM, on_bottom)

            ctrl_writer.start()

            # combine all controls to a main sizer
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            centerSizer = wx.BoxSizer(wx.HORIZONTAL)
            mainLeftSizer = wx.BoxSizer(wx.VERTICAL)
            mainRightSizer = wx.BoxSizer(wx.VERTICAL)

            mainLeftSizer.Add(ghSzr, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)
            mainLeftSizer.Add(egSzr, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)
            mainLeftSizer.Add(web_szr, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)
            mainLeftSizer.Add(sizer2, 0, wx.ALL | wx.EXPAND, 10)
            mainRightSizer.Add(loggingCtrl, 1, wx.ALL | wx.EXPAND, 5)

            centerSizer.Add(mainLeftSizer)
            centerSizer.Add(mainRightSizer, 1, wx.EXPAND)
            mainSizer.Add(centerSizer, 0,  wx.EXPAND)
            mainSizer.Add(btnSizer, 0, wx.ALL | wx.ALIGN_RIGHT | wx.EXPAND, 10)
            self.SetSizerAndFit(mainSizer)
            self.SetSize((768, -1))
            self.Center()
            self.Bind(wx.EVT_CLOSE, self.OnClose)

        def DoMain(self):
            builder.Tasks.Main(self.buildSetup)
            sys.stderr.write('\nDone!\n')

        def OnCancel(self, event):
            sys.stdout = _stdout
            sys.stderr = _stderr
            event.Skip()
            self.Destroy()
            wx.GetApp().ExitMainLoop()

        def OnClose(self, event):
            sys.stdout = _stdout
            sys.stderr = _stderr
            event.Skip()
            self.Destroy()
            # wx.GetApp().ExitMainLoop()
            sys.exit(0)

        def OnExit(self):
            sys.stdout = _stdout
            sys.stderr = _stderr
            self.Destroy()
            sys.exit(0)

        def OnDownloadDependencies(self, event):
            self.buildSetup.download_dependencies = (
                self.download_dependencies_ctrl.GetValue()
            )

        def OnInstallerCheck(self, event):
            # We don't want releases going out without a current changelog (which
            # is also included in the documentation), so let's force both to be
            # built when building the installer.
            for ctrl in (
                self.ctrls["builder.BuildChangelog.BuildChangelog"],
                self.ctrls["builder.BuildDocs.BuildChmDocs"],
            ):
                if event is True or event.Checked():
                    ctrl.Enable(False)
                    ctrl.SetValue(True)
                else:
                    ctrl.Enable(True)

        def OnOk(self, dummyEvent):
            repository = self.chcRepo.GetStringSelection()
            try:
                user, repo = repository.split('/')
            except ValueError:
                dlg = wx.MessageDialog(
                    self,
                    caption="Information",
                    style=wx.OK,
                    message="Repositoryname not valid. Must be:\n"
                    "<user or organization>/<repository>."
                )
                dlg.ShowModal()
                return

            for child in self.GetChildren():
                child.Enable(False)

            self.loggingCtrl.Enable(True)
            #self.SetWindowStyleFlag(wx.CAPTION|wx.RESIZE_BORDER)
            for task in self.buildSetup.tasks:
                if not task.visible:
                    continue
                section = task.GetId()
                if section in self.ctrls:
                    ctrl = self.ctrls[section]
                    task.activated = ctrl.GetValue()
            (
                self.buildSetup.appVersion,
                self.buildSetup.appVersionInfo
            ) = (
                ParseVersion(self.versionStr.GetValue())
            )
            self.buildSetup.gitConfig.update({
                "user": user,
                "repo": repo,
                "branch": self.chcBranch.GetStringSelection(),
            })
            self.buildSetup.args.websiteUrl = self.url.GetValue()

            self.buildSetup.config.SaveSettings()
            thread = threading.Thread(target=self.DoMain)
            thread.start()

        def OnRefreshVersion(self, event):
            GetVersion(self.buildSetup)
            self.UpdateVersion()

        def OnRepoSelection(self, event):
            key = self.chcRepo.GetStringSelection()
            self.chcBranch.SetItems(
                self.buildSetup.gitConfig["all_repos"][key]["all_branches"]
            )
            self.chcBranch.SetStringSelection(
                self.buildSetup.gitConfig["all_repos"][key]["def_branch"]
            )

        def UpdateVersion(self):
            if not self.buildSetup.appVersion.startswith("WIP-"):
                self.versionStr.SetValue(self.buildSetup.appVersion)

    for task in buildSetup.tasks:
        task.Setup()
    (buildSetup.appVersion, buildSetup.appVersionInfo) = GetVersion(buildSetup)

    app = wx.App(0)
    app.SetExitOnFrameDelete(True)
    mainDialog = MainDialog(buildSetup)
    mainDialog.Show()
    app.MainLoop()
