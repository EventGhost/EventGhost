import wx
import threading
from os.path import join, exists
import builder
import builder.Tasks


class MainDialog(wx.Dialog):

    def __init__(self):
        wx.Dialog.__init__(self, None, title="Build EventGhost Installer")

        # create controls
        self.ctrls = {}
        ctrlsSizer = wx.BoxSizer(wx.VERTICAL)
        for task in builder.Tasks.TASKS:
            if task.enabled is None:
                continue
            section = task.GetId()
            ctrl = wx.CheckBox(self, -1, task.description)
            ctrl.SetValue(task.enabled)
            ctrlsSizer.Add(ctrl, 0, wx.ALL, 5)
            self.ctrls[section] = ctrl
            if not task.IsEnabled():
                ctrl.Enable(False)

#        if not exists(join(builder.SOURCE_DIR, "eg", "StaticImports.py")):
#            self.ctrls["buildStaticImports"].Enable(False)
#            self.ctrls["buildStaticImports"].SetValue(True)
#        if not exists(join(builder.SOURCE_DIR, "EventGhost.chm")):
#            self.ctrls["buildChmDocs"].Enable(False)
#            self.ctrls["buildChmDocs"].SetValue(True)
#        if (
#            not exists(join(builder.SOURCE_DIR, "py%s.exe" % builder.pyVersion))
#            or not exists(join(builder.SOURCE_DIR, "pyw%s.exe" % builder.pyVersion))
#        ):
#            self.ctrls["buildPyExe"].Enable(False)
#            self.ctrls["buildPyExe"].SetValue(True)
#        if not exists(join(builder.SOURCE_DIR, builder.appShortName + ".exe")):
#            self.ctrls["buildLib"].Enable(False)
#            self.ctrls["buildLib"].SetValue(True)

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

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer2, 1, wx.ALL|wx.EXPAND, 0)
        mainSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        self.SetSizerAndFit(mainSizer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def OnOk(self, dummyEvent):
        """ Handles a click on the Ok button. """
        self.okButton.Enable(False)
        self.cancelButton.Enable(False)
        #self.SetWindowStyleFlag(wx.CAPTION|wx.RESIZE_BORDER)
        for task in builder.Tasks.TASKS:
            section = task.GetId()
            if section in self.ctrls:
                ctrl = self.ctrls[section]
                task.enabled = ctrl.GetValue()
                ctrl.Enable(False)
        builder.config.SaveSettings()
        thread = threading.Thread(target=self.DoMain)
        thread.start()


    def DoMain(self):
        builder.Tasks.Main()
        wx.CallAfter(self.Close)


    def OnCancel(self, event):
        """ Handles a click on the cancel button. """
        event.Skip()
        self.Destroy()
        wx.GetApp().ExitMainLoop()


    def OnClose(self, event):
        """ Handles a click on the close box of the frame. """
        self.Destroy()
        event.Skip()
        wx.GetApp().ExitMainLoop()


def Main():
    #installer = MyInstaller()
    app = wx.App(0)
    app.SetExitOnFrameDelete(True)
    mainDialog = MainDialog()
    mainDialog.Show()
    app.MainLoop()

