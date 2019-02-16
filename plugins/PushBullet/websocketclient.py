# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2015  Pako <lubos.ruckl@gmail.com>
#
# This file is part of the PushBullet plugin for EventGhost.
#


import eg
# from .lib.websocket__0440 import WebSocketApp
from websocket import WebSocketApp


class WebSocketClient(WebSocketApp):
    def __init__(self, url, plugin):
        self.plugin = plugin
        self.watchdog = None

        def on_open(arg):
            self.plugin.on_open(arg)

        def on_message(arg1, arg2):
            self.plugin.on_message(arg1, arg2)

        def on_error(_, error):
            eg.PrintError(self.plugin.text.wsError % error)
            self.plugin.stop_watchdog()
            self.watchdog = eg.scheduler.AddTask(5.0, self.plugin.watcher)

        def on_close(_):
            self.plugin.TriggerEvent(self.plugin.text.wsClosedEvt)

        WebSocketApp.__init__(
            self,
            url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )

    def start(self):
        auth = None
        if self.plugin.proxy[0] != "":
            host = str(self.plugin.proxy[0])
            port = self.plugin.proxy[1]
            if self.plugin.proxy[2] != "":
                auth = (
                    str(self.plugin.proxy[2]),
                    str(self.plugin.proxy[3].Get())
                )
        else:
            host = None
            port = None
        self.run_forever(
            http_proxy_host=host,
            http_proxy_port=port,
            http_proxy_auth=auth
        )
