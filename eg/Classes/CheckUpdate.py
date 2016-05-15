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

import eg
import wx
import re
import threading
import webbrowser
from agithub.GitHub import GitHub
from operator import itemgetter


class Text(eg.TranslatableStrings):
    newVersionMesg = \
        "A newer version of EventGhost has been released.\n\n"\
        "\tYour version:\t%s\n"\
        "\tNewest version:\t%s\n\n"\
        "Do you want to visit the download page now?"
    downloadButton = "Visit download page"
    waitMesg = "Please wait while EventGhost retrieves update information."
    ManOkMesg = "There is currently no newer version of EventGhost available."
    ManErrorMesg = \
        "It wasn't possible to get the information from the EventGhost "\
        "website.\n\n"\
        "Please try it again later."
    wipUpdateMsg = "Update check not available in developer version."


class MessageDialog(eg.Dialog):

    def __init__(self, version, url):
        self.url = url
        currentVersion = eg.Version.string
        eg.Dialog.__init__(self, None, -1, eg.APP_NAME)
        bmp = wx.ArtProvider.GetBitmap(
            wx.ART_INFORMATION,
            wx.ART_MESSAGE_BOX,
            (32, 32)
        )
        staticBitmap = wx.StaticBitmap(self, -1, bmp)
        staticText = self.StaticText(
            Text.newVersionMesg % (currentVersion, version)
        )
        downloadButton = wx.Button(self, -1, Text.downloadButton)
        downloadButton.Bind(wx.EVT_BUTTON, self.OnOk)
        cancelButton = wx.Button(self, -1, eg.text.General.cancel)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        sizer2 = eg.HBoxSizer(
            (staticBitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10),
            ((5, 5), 0),
            (
                staticText,
                0,
                wx.TOP|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL,
                10
            ),
        )
        self.SetSizerAndFit(
            eg.VBoxSizer(
                (sizer2),
                ((5, 5), 1),
                (
                    eg.HBoxSizer(
                        (downloadButton),
                        ((5, 5), 0),
                        (cancelButton),
                    ), 0, wx.ALIGN_CENTER_HORIZONTAL
                ),
                ((2, 10), 0),
            )
        )
        self.ShowModal()


    def OnCancel(self, event):
        self.Close()


    def OnOk(self, event):
        webbrowser.open(self.url, True, True)
        self.Close()



def CenterOnParent(self):
    parent = eg.document.frame
    if parent is None:
        return
    x, y = parent.GetPosition()
    parentWidth, parentHeight = parent.GetSize()
    width, height = self.GetSize()
    self.SetPosition(
        ((parentWidth - width) / 2 + x, (parentHeight - height) / 2 + y)
    )


def ShowWaitDialog():
    dialog = wx.Dialog(None, style=wx.THICK_FRAME|wx.DIALOG_NO_PARENT)
    staticText = wx.StaticText(dialog, -1, Text.waitMesg)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(staticText, 1, wx.ALL, 20)
    dialog.SetSizerAndFit(sizer)
    CenterOnParent(dialog)
    dialog.Show()
    wx.GetApp().Yield()
    return dialog


def _checkUpdate(manually=False):
    dialog = None
    try:
        if manually:
            if eg.Version.base == "WIP":
                wx.MessageBox(Text.wipUpdateMsg, eg.APP_NAME)
                return
            dialog = ShowWaitDialog()

        gh = GitHub()

        # get the latest release
        rc, data = gh.repos["EventGhost"]["EventGhost"].releases.latest.get()
        if rc != 200:
            if manually:
                dialog.Destroy()
                dlg = wx.MessageDialog(
                    None,
                    Text.ManErrorMesg,
                    eg.APP_NAME,
                    style=wx.OK | wx.ICON_ERROR
                )
                dlg.ShowModal()
                dlg.Destroy()
            return

        relName = data["name"]
        relUrl = data["html_url"]
        cmpResult = compareVersions(eg.Version.string, relName)

        if eg.config.checkPreRelease:
            # check if we have a pre-release that is newer than latest release
            # and installed version
            rc2, data2 = gh.repos["EventGhost"]["EventGhost"].releases.get()
            if rc2 == 200:
                prereleases = [item for item in data2 if
                               item["prerelease"] == True]
                if len(prereleases) > 0:
                    latestPreRelease = sorted(
                        prereleases,
                        key=itemgetter("created_at", "published_at"),
                        reverse=True
                    )[0]
                    if cmpResult == 2:
                        result = compareVersions(
                            relName,
                            latestPreRelease["name"]
                        )
                    else:
                        result = compareVersions(
                            eg.Version.string,
                            latestPreRelease["name"]
                        )
                    if result == 2:
                        cmpResult = 2
                        relName = latestPreRelease["name"]
                        relUrl = latestPreRelease["html_url"]
        if dialog:
            dialog.Destroy()
            dialog = None
        if cmpResult == 2:
            wx.CallAfter(MessageDialog, relName, relUrl)
        else:
            if manually:
                dlg = wx.MessageDialog(
                    None,
                    Text.ManOkMesg,
                    eg.APP_NAME,
                    style=wx.OK|wx.ICON_INFORMATION
                )
                dlg.ShowModal()
                dlg.Destroy()
    except:
        if dialog:
            dialog.Destroy()
        if manually:
            dlg = wx.MessageDialog(
                None,
                Text.ManErrorMesg,
                eg.APP_NAME,
                style=wx.OK|wx.ICON_ERROR
            )
            dlg.ShowModal()
            dlg.Destroy()



class CheckUpdate:
    @classmethod
    @eg.LogIt
    def Start(cls):
        threading.Thread(target=_checkUpdate, name="CheckUpdate").start()


    @classmethod
    def CheckUpdateManually(cls):
        _checkUpdate(manually=True)


def compareVersions(ver_a, ver_b):
    """ Compare two version numbers. Return 0 if a==b or error, 1 if a>b and 2 if b>a """
    if not ver_a or not ver_b:
        return 0
    try:
        a = Version(ver_a)
        b = Version(ver_b)
    except InvalidVersion:
        return -1

    if a > b:
        return 1
    elif b > a:
        return 2
    return 0


class InvalidVersion(Exception):
    pass


def ParseVersion(ver):
    match = re.search(
        "^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
        "(-(?P<pre>:alpha|beta|rc)(?P<pre_nr>\d+))?$",
        ver.strip().lower()
    )
    if match:
        return match.groupdict()
    else:
        raise InvalidVersion


class Version:
    def __init__(self, ver_str):
        ver = ParseVersion(ver_str)
        self.ver_str = "{0:04}{1:04}{2:04}{3}{4:04}".format(
            int(ver["major"]),
            int(ver["minor"]),
            int(ver["patch"]),
            ver["pre"] if ver["pre"] else "z",
            int(ver["pre_nr"]) if ver["pre_nr"] else 9999
        )

    def __lt__(self, other):
        return self.ver_str < other.ver_str

    def __le__(self, other):
        return self.ver_str <= other.ver_str

    def __gt__(self, other):
        return self.ver_str > other.ver_str

    def __ge__(self, other):
        return self.ver_str >= other.ver_str

    def __eq__(self, other):
        return self.ver_str == other.ver_str

    def __ne__(self, other):
        return self.ver_str != other.ver_str
