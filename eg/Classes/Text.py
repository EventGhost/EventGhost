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
import wx
import requests

import eg


class LanguageLoadDialog(wx.Dialog):

    def __init__(self, language, msg):
        url = language.translation_url
        url += (
            '&text=EventGhost Language Translation'
            '&text=' + msg
        )
        response = requests.get(url, timeout=10)
        text = list(unicode(item.decode('utf-8')) for item in response.json()['text'])
        title, message = text

        try:
            eg.PrintDebugNotice(str(text).encode('utf-8'))
        except UnicodeDecodeError:
            eg.PrintDebugNotice(str(text).decode('latin-1').encode('utf-8'))

        message += u' ' + language.label

        wx.Dialog.__init__(
            self,
            None,
            -1,
            style=0
        )

        try:
            eg.PrintDebugNotice(message.encode('utf-8'))
        except UnicodeDecodeError:
            eg.PrintDebugNotice(message.decode('latin-1').encode('utf-8'))

        try:
            eg.PrintDebugNotice(title.encode('utf-8'))
        except UnicodeDecodeError:
            eg.PrintDebugNotice(title.decode('latin-1').encode('utf-8'))

        title_ctrl = wx.StaticText(self, -1, title)
        message_ctrl = wx.StaticText(self, -1, message)
        v_sizer = wx.BoxSizer(wx.VERTICAL)

        v_sizer.Add(title_ctrl, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 10)
        v_sizer.Add(message_ctrl, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 10)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(v_sizer, 0, wx.EXPAND | wx.ALIGN_CENTER)

        self.SetSizerAndFit(h_sizer)
        self.Show()
        title_ctrl.Show()
        message_ctrl.Show()



def Text(language):
    # if not language.is_available:
    #     import time
    #
    #     dlg1 = LanguageLoadDialog(language, 'Translating language to')
    #     time.sleep(2.0)
    #     language.load()
    #     dlg1.Destroy()
    #     dlg2 = LanguageLoadDialog(language, 'Translating plugin descriptions to')
    #     time.sleep(2.0)
    #     language.build_plugin_descriptions()
    #     dlg2.Destroy()
    #     return language
    # else:
    # eg.app.MainLoop()
     # eg.app.ExitMainLoop()
    language.load()
    language.build_plugin_descriptions()
    return language
