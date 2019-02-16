# coding=utf8

import wx


class ComposeMsg:
    def __init__(self):
        pass

    # noinspection PyAttributeOutsideInit
    def send_cfg(self, panel, sbjct, from_adr, to_adr, cc_adr, body, templates, to_name, text, plugin):
        subject_lbl = wx.StaticText(panel, wx.ID_ANY, text.subjectLabel)
        self.subject_ctrl = wx.TextCtrl(panel, wx.ID_ANY, sbjct)
        from_lbl = wx.StaticText(panel, wx.ID_ANY, text.fromLabel)
        choices = ["%s <%s> - %s" % (item[2], item[3], item[0]) for item in plugin.configs]
        self.from_ctrl = wx.Choice(panel, wx.ID_ANY, choices=choices)
        self.from_ctrl.SetStringSelection(from_adr)
        to_lbl = wx.StaticText(panel, wx.ID_ANY, text.toLabel)
        self.to_name_ctrl = wx.TextCtrl(panel, wx.ID_ANY, to_name)
        self.to_ctrl = wx.TextCtrl(panel, wx.ID_ANY, to_adr)
        copy_lbl = wx.StaticText(panel, wx.ID_ANY, text.copyLabel)
        choices = ['']
        choices.extend([item[0] for item in plugin.groups])
        self.cc_ctrl = wx.Choice(panel, wx.ID_ANY, choices=choices)
        self.cc_ctrl.SetStringSelection(cc_adr)
        text_lbl = wx.StaticText(panel, wx.ID_ANY, text.outText)
        self.body_ctrl = wx.TextCtrl(
            parent=panel,
            id=wx.ID_ANY,
            size=(-1, 60),
            style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.HSCROLL | wx.TE_AUTO_URL | wx.TE_RICH2
        )
        self.body_ctrl.SetValue(body)
        texts_lbl = wx.StaticText(panel, wx.ID_ANY, text.outTexts)
        choices = ['']
        choices.extend([item[0] for item in plugin.texts])
        self.templates_ctrl = wx.ComboBox(panel, wx.ID_ANY, choices=choices, size=(200, -1))
        self.templates_ctrl.SetValue(templates)
        self.to_name_ctrl.SetToolTip(wx.ToolTip(text.tip1 + '.\n' + text.tip))
        self.to_ctrl.SetToolTip(wx.ToolTip(text.tip2 + '.\n' + text.tip))
        self.body_ctrl.SetToolTip(wx.ToolTip(text.tip))
        self.subject_ctrl.SetToolTip(wx.ToolTip(text.tip))
        self.templates_ctrl.SetToolTip(wx.ToolTip(text.tip))

        top_sizer = wx.GridBagSizer(5, 5)
        top_sizer.Add(subject_lbl, (0, 0), flag=wx.ALIGN_RIGHT)
        top_sizer.Add(self.subject_ctrl, (0, 1), (1, 2), flag=wx.EXPAND)
        top_sizer.Add(from_lbl, (1, 0), flag=wx.ALIGN_RIGHT)
        top_sizer.Add(self.from_ctrl, (1, 1), (1, 2), flag=wx.EXPAND)
        top_sizer.Add(to_lbl, (2, 0), flag=wx.ALIGN_RIGHT)
        top_sizer.Add(self.to_name_ctrl, (2, 1), flag=wx.EXPAND)
        top_sizer.Add(self.to_ctrl, (2, 2), flag=wx.EXPAND)
        top_sizer.Add(copy_lbl, (3, 0), flag=wx.ALIGN_RIGHT)
        top_sizer.Add(self.cc_ctrl, (3, 1), (1, 2), flag=wx.EXPAND)
        top_sizer.Add(text_lbl, (4, 0), flag=wx.ALIGN_RIGHT)
        top_sizer.Add(self.body_ctrl, (4, 1), (1, 2), flag=wx.EXPAND)
        top_sizer.Add(texts_lbl, (5, 0), flag=wx.ALIGN_RIGHT)
        top_sizer.Add(self.templates_ctrl, (5, 1), (1, 2), flag=wx.EXPAND)
        top_sizer.AddGrowableCol(1)
        top_sizer.AddGrowableCol(2)
        top_sizer.AddGrowableRow(4)

        return top_sizer
