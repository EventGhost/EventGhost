# -*- coding: utf-8 -*-

import eg

eg.RegisterPlugin(
    name = "HTTPRequest",
    author = "David Perry <d.perry@utoronto.ca>",
    version = "0.1.0",
    kind = "other",
    description = "Send HTTP requests.",
    url = "https://github.com/Boolean263/EventGhost-HTTPRequest",
    guid = "{dea987ff-3281-4da2-b0e9-c396b4260c37}",
)

import wx
import requests
from numbers import Number

class HTTPRequest(eg.PluginBase):

    def __init__(self):
        self.AddAction(sendRequest)

    def __start__(self):
        print "HTTPRequest Plugin started"

class sendRequest(eg.ActionBase):
    name = "Send HTTP request"
    description = "Sends an HTTP request."

    methods = ("GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS", "PATCH")
    body_methods = ("POST", "PUT", "PATCH")

    def __call__(self, host, uri="/", method="GET", body=None, timeout=0, ssl=False, sslVerify=True, parseBody=False):
        if not uri:
            uri = "/"
        if not timeout:
            timeout = None

        host = eg.ParseString(host)
        uri = eg.ParseString(uri)

        if isinstance(method, Number):
            method = self.methods[method]
        if method not in self.methods:
            raise ValueError("Invalid request method")
        if method not in self.body_methods:
            body = None

        if body is not None and parseBody:
            body = eg.ParseString(body)

        ret_val = requests.request(method,
                "{}://{}{}".format("https" if ssl else "http", host, uri),
                verify=sslVerify,
                timeout=timeout,
                data=body,
                stream=False)
        ret_val.close()
        return ret_val

    def GetLabel(self, host, uri="/", method="GET", body=None, timeout=0, ssl=False, sslVerify=True, parseBody=False):
        method = self.methods[method] if isinstance(method, Number) else method
        return "{} {}://{}{}".format(method, "https" if ssl else "http", host, uri)

    def Configure(self, host="192.168.0.1", uri="/", method="GET", body="", timeout=0, ssl=False, sslVerify=True, parseBody=False):
        panel = eg.ConfigPanel(self)
        methodCtrl = panel.Choice(method if isinstance(method, Number) else self.methods.index(method), choices=self.methods)
        hostCtrl = panel.TextCtrl(host or "")
        sslCtrl = panel.CheckBox(ssl, "Use HTTPS")
        sslVerifyCtrl = panel.CheckBox(sslVerify, "Verify certificate")
        parseBodyCtrl = panel.CheckBox(parseBody, "Parse body for EventGhost variables")
        timeoutCtrl = panel.SpinIntCtrl(timeout, min=0, max=600)
        uriCtrl = panel.TextCtrl(uri or "/")
        bodyCtrl = panel.TextCtrl("\n\n", style=wx.TE_MULTILINE)
        bodyCtrlHeight = bodyCtrl.GetBestSize()[1]
        bodyCtrl.ChangeValue(body or "")
        bodyCtrl.SetMinSize((-1, bodyCtrlHeight))

        sizer = wx.GridBagSizer(5, 5)
        expand = wx.EXPAND
        align = wx.ALIGN_CENTER_VERTICAL
        sizer.AddMany([
            (panel.StaticText("Method"), (0, 0), (1, 1), align),
            (methodCtrl, (0, 1), (1, 1), expand),
            (panel.StaticText("Host:Port"), (1, 0), (1, 1), align),
            (hostCtrl, (1, 1), (1, 1), expand),
            (panel.StaticText("URI"), (2, 0), (1, 1), align),
            (uriCtrl, (2, 1), (1, 1), expand),
            (sslCtrl, (3, 1), (1, 1), expand),
            (sslVerifyCtrl, (4, 1), (1, 1), align),
            (panel.StaticText("Timeout (seconds)"), (5, 0), (1, 1), align),
            (timeoutCtrl, (5, 1), (1, 1), align),
            (panel.StaticText("Body\n(POST/PUT/PATCH)"), (6, 0), (1, 1), align),
            (bodyCtrl, (6, 1), (1, 1), expand),
            (parseBodyCtrl, (7, 1), (1, 1), expand),
            (panel.StaticText("EventGhost variables in host and URI are always expanded.\nUse a double '{{' to prevent its use as an expansion."), (8, 1), (1, 1), expand),
        ])
        sizer.AddGrowableCol(1)
        panel.sizer.Add(sizer, 1, expand)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                uriCtrl.GetValue() or "/",
                methodCtrl.GetValue() or 0,
                bodyCtrl.GetValue() or "",
                timeoutCtrl.GetValue() or 0,
                sslCtrl.GetValue(),
                sslVerifyCtrl.GetValue(),
                parseBodyCtrl.GetValue()
            )

#
# Editor modelines  -  https://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# coding: utf-8
# End:
#
# vi: set shiftwidth=4 tabstop=4 expandtab fileencoding=utf-8:
# :indentSize=4:tabSize=4:noTabs=true:coding=utf-8:
#
