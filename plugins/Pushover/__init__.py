import eg, httplib, urllib

PRIORITIES = {
  'Lowest': -2,
  'Low': -1,
  'Normal': 0,
  'High': 1,
  'Highest': 2
}

eg.RegisterPlugin(
    name = "Pushover",
    guid='{6542CCE7-D1F5-43DB-804E-CFD34C3B3488}',
    author = "EssKaa",
    version = "1.1",
    createMacrosOnAdd = False,
    canMultiLoad = False,
    description = "This plugin sends notifications to you mobile using the Pushover service. For more details visit: https://pushover.net/"
)

class Pushover(eg.PluginBase):
    def __init__(self):
        self.AddAction(poSendMessage, clsName="Send message", description="")
        
    def __start__(self, username="", token="", device="", retryTime="", expireTime=""):
    	eg.globals.poUsername = username
    	eg.globals.poToken = token
        eg.globals.poDevice = device
        eg.globals.poRetry = retryTime
        eg.globals.poExpire = expireTime
        
    def Configure(self, username="", token="", device="", retryTime=60, expireTime=3600):
    
        panel= eg.ConfigPanel()
        labelUsername = wx.StaticText(panel, label="User / Group Key (not e-mail address):", pos=(10, 22))
        textUsername = wx.TextCtrl(panel, -1, username, (10, 40), (250, -1))
        labelToken = wx.StaticText(panel, label="Application API token:", pos=(10, 72))
        textToken = wx.TextCtrl(panel, -1, token, (10,90), (250, -1))
        labelDevice = wx.StaticText(panel, label="Device - leave blank for all, comma seperated list", pos=(10, 122))
        textDevice = wx.TextCtrl(panel, -1, device, (10,140), (250, -1))
        labelRetry = wx.StaticText(panel, label="Retry time in s (Default: 60s)", pos=(10,172))
        spinRetry = wx.SpinCtrl(panel, -1, "", (10,190), (80, -1))
        spinRetry.SetRange(1,43200)
        spinRetry.SetValue(int(retryTime))
        labelExpire = wx.StaticText(panel, label="Expire time in s (Default: 3600s)", pos=(10,222))
        spinExpire = wx.SpinCtrl(panel, -1, "", (10,240), (80, -1))
        spinExpire.SetRange(1,86400)
        spinExpire.SetValue(int(expireTime))

        while panel.Affirmed():
            panel.SetResult(textUsername.GetValue(), textToken.GetValue(), textDevice.GetValue(), spinRetry.GetValue(), spinExpire.GetValue())

class ActionBase(eg.ActionClass):
    
    def runSendPushoverMessage(self, msgToSend="EventGhost test message.", prio="", sound=""):
        if msgToSend:
            msgToSend = eg.ParseString(msgToSend)
    
        decimalPrio = None
        decimalPrio = PRIORITIES[prio]

        if decimalPrio <= 1:
            urldata = urllib.urlencode({
            "token": eg.globals.poToken,
            "user": eg.globals.poUsername,
            "device": eg.globals.poDevice,
            "message": msgToSend,
            "priority": str(decimalPrio),
            "sound": sound,
            })
        else:
            urldata = urllib.urlencode({
            "token": eg.globals.poToken,
            "user": eg.globals.poUsername,
            "device": eg.globals.poDevice,
            "message": msgToSend,
            "priority": str(decimalPrio),
            "retry": eg.globals.poRetry,
            "expire": eg.globals.poExpire,
            "sound": sound,
            })

        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json", urldata, { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

class poSendMessage(ActionBase):

    def __call__(self, msgToSend=None, prio="Normal", sound=""):

        if not msgToSend:
            raise Exception('Please enter message first')
        return self.runSendPushoverMessage(msgToSend=msgToSend, prio=prio, sound=sound)

    def Configure(self, msgToSend="", prio="Normal", sound=""):
        panel = eg.ConfigPanel()

        prioList = sorted(PRIORITIES.keys(), key=PRIORITIES.__getitem__)

        labelMessage = wx.StaticText(panel, label="Message:", pos=(10, 22))
        textMessage = wx.TextCtrl(panel, -1, msgToSend, (10, 40), (400, -1))
        
        labelCombo = wx.StaticText(panel, label="Priority: ", pos=(10, 72))
        combo = wx.Choice(panel, -1, (10, 90), choices=prioList)
        if prio in prioList:
            combo.SetStringSelection(prio)

        labelSound = wx.StaticText(panel, label="Sound: (for further explanation see Pushover API page)", pos=(10, 122))
        textSound = wx.TextCtrl(panel, -1, sound, (10, 140), (400, -1))

        while panel.Affirmed():
            panel.SetResult(textMessage.GetValue(), prioList[combo.GetCurrentSelection()], textSound.GetValue())
