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
                        result = compareVersions(relName,
                                                 latestPreRelease["name"])
                    else:
                        result = compareVersions(eg.Version.string,
                                                 latestPreRelease["name"])
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

###  The following code is from QGIS

"""
/***************************************************************************
                        Plugin Installer module
                        Plugin version comparision functions
                             -------------------
    Date                 : 2008-11-24
    Copyright            : (C) 2008 by Borys Jurgiel
    Email                : info at borysjurgiel dot pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

Here is Python function for comparing version numbers. It's case insensitive
and recognizes all major notations, prefixes (ver. and version), delimiters
(. - and _) and suffixes (alpha, beta, rc, preview and trunk).

Usage: compareVersions(version1, version2)

The function accepts arguments of any type convertable to unicode string
and returns integer value:
0 - the versions are equal
1 - version 1 is higher
2 - version 2 is higher

-----------------------------------------------------------------------------
HOW DOES IT WORK...
First, both arguments are converted to uppercase unicode and stripped of
'VERSION' or 'VER.' prefix. Then they are chopped into a list of particular
numeric and alphabetic elements. The dots, dashes and underlines are recognized
as delimiters. Also numbers and non numbers are separated. See example below:

'Ver 0.03-120_rc7foo' is converted to ['0','03','120','RC','7','FOO']

Then every pair of elements, from left to right, is compared as string
or as number to provide the best result (you know, 11>9 but also '03'>'007').
The comparing stops when one of elements is greater. If comparing achieves
the end of the shorter list and the matter is still unresolved, the longer
list is usually recognized as higher, except following suffixes:
ALPHA, BETA, RC, PREVIEW and TRUNK which make the version number lower.
"""


def normalizeVersion(s):
    """ remove possible prefix from given string and convert to uppercase """
    prefixes = ['VERSION', 'VER.', 'VER', 'V.', 'V', 'REVISION', 'REV.', 'REV', 'R.', 'R']
    if not s:
        return unicode()
    s = unicode(s).upper()
    for i in prefixes:
        if s[:len(i)] == i:
            s = s.replace(i, '')
    s = s.strip()
    return s


def classifyCharacter(c):
    """ return 0 for delimiter, 1 for digit and 2 for alphabetic character """
    if c in [".", "-", "_", " "]:
        return 0
    if c.isdigit():
        return 1
    else:
        return 2


def chopString(s):
    """ convert string to list of numbers and words """
    l = [s[0]]
    for i in range(1, len(s)):
        if classifyCharacter(s[i]) == 0:
            pass
        elif classifyCharacter(s[i]) == classifyCharacter(s[i - 1]):
            l[len(l) - 1] += s[i]
        else:
            l += [s[i]]
    return l


def compareElements(s1, s2):
    """ compare two particular elements """
    # check if the matter is easy solvable:
    if s1 == s2:
        return 0
    # try to compare as numeric values (but only if the first character is not 0):
    if s1 and s2 and s1.isnumeric() and s2.isnumeric() and s1[0] != '0' and s2[0] != '0':
        if float(s1) == float(s2):
            return 0
        elif float(s1) > float(s2):
            return 1
        else:
            return 2
    # if the strings aren't numeric or start from 0, compare them as a strings:
    # but first, set ALPHA < BETA < PREVIEW < RC < TRUNK < [NOTHING] < [ANYTHING_ELSE]
    if s1 not in ['ALPHA', 'BETA', 'PREVIEW', 'RC', 'TRUNK']:
        s1 = 'Z' + s1
    if s2 not in ['ALPHA', 'BETA', 'PREVIEW', 'RC', 'TRUNK']:
        s2 = 'Z' + s2
    # the final test:
    if s1 > s2:
        return 1
    else:
        return 2


def compareVersions(a, b):
    """ Compare two version numbers. Return 0 if a==b or error, 1 if a>b and 2 if b>a """
    if not a or not b:
        return 0
    a = normalizeVersion(a)
    b = normalizeVersion(b)
    if a == b:
        return 0
    # convert the strings to lists
    v1 = chopString(a)
    v2 = chopString(b)
    # set the shorter string as a base
    l = len(v1)
    if l > len(v2):
        l = len(v2)
    # try to determine within the common length
    for i in range(l):
        if compareElements(v1[i], v2[i]):
            return compareElements(v1[i], v2[i])
    # if the lists are identical till the end of the shorther string, try to compare the odd tail
    #with the simple space (because the 'alpha', 'beta', 'preview' and 'rc' are LESS then nothing)
    if len(v1) > l:
        return compareElements(v1[l], u' ')
    if len(v2) > l:
        return compareElements(u' ', v2[l])
    # if everything else fails...
    if a > b:
        return 1
    else:
        return 2
