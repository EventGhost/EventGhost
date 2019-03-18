from pynma import PyNMA

eg.RegisterPlugin(
    name = "Notify My Android",
    version = "1.0",
    author = "Torbjorn Weserlund",
    guid = "{A4F0DEFE-2E0B-47F3-A155-ED72C7A4E270}",
    description = (
        "Send notifications using Notify My Android"
    ),
    canMultiLoad = True,
)


import wx
from hashlib import md5


class Text:
    key = "API Key:"
    application = "Application:"
    siteStr = "Site:"
    settingsBox = "Notify My Android settings"
    securityBox = "Security"
    class SendNotification:
        parameterDescription = "Event name to send:"
        eventText = "Event:"
        dataText = "Data:"
        priorityText = "Priority (-2 - 2 ):"


class NotifyMyAndroid(eg.PluginBase):
    text = Text

    key = ""
    application = ""
    siteStr = ""


    def __init__(self):
        self.AddAction(SendNotification)


    def __start__(self, key, application, site):
        self.key = key
        self.application = application
        self.siteStr = site


    def Configure(self, key="", application="Eventghost", siteStr="http://www.eventghost.com"):
        text = self.text
        panel = eg.ConfigPanel()
        keyCtrl = panel.TextCtrl(key)
        applicationCtrl = panel.TextCtrl(application)
        siteStrCtrl = panel.TextCtrl(siteStr)

        st1 = panel.StaticText(text.key)
        st2 = panel.StaticText(text.application)
        st3 = panel.StaticText(text.siteStr)
        eg.EqualizeWidths((st1, st2, st3))
        settingsBox = panel.BoxedGroup(
            text.settingsBox,
            (st1, keyCtrl),
            (st2, applicationCtrl),
            (st3, siteStrCtrl),
        )

        panel.sizer.Add(settingsBox, 0, wx.EXPAND)


        while panel.Affirmed():
            panel.SetResult(
                keyCtrl.GetValue(),
                applicationCtrl.GetValue(),
                siteStrCtrl.GetValue()
            )
        self.key = keyCtrl.GetValue()
        self.application = applicationCtrl.GetValue()
        self.siteStr = siteStrCtrl.GetValue()


    def SendNotification(self, event="", data="" , prio=0):

        p = PyNMA(str(self.key))
        res = p.push( self.application, event, data , self.siteStr, prio, batch_mode=False)
        return res



class SendNotification(eg.ActionWithStringParameter):

    text = Text

    def Configure(self, event="", data="Eventghost", priority=0):
        text = self.text
        panel = eg.ConfigPanel()
        eventCtrl = panel.TextCtrl(event)
        dataCtrl = panel.TextCtrl(data)
        priorityCtrl = panel.SpinIntCtrl(priority, min=-2, max=2)

        st1 = panel.StaticText(text.SendNotification.eventText)
        st2 = panel.StaticText(text.SendNotification.dataText)
        st3 = panel.StaticText(text.SendNotification.priorityText)
        eg.EqualizeWidths((st1, st2, st3))
        settingsBox = panel.BoxedGroup(
            "Event information:",
            (st1, eventCtrl),
            (st2, dataCtrl),
            (st3, priorityCtrl),
        )

        panel.sizer.Add(settingsBox, 0, wx.EXPAND)


        while panel.Affirmed():
            panel.SetResult(
                eventCtrl.GetValue(),
                dataCtrl.GetValue(),
                priorityCtrl.GetValue()
            )


    def __call__(self, event="", data="" , prio=0):
        res = self.plugin.SendNotification(event,data,prio)
        return res

