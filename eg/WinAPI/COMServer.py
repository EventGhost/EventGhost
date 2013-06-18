import pythoncom
import eg

class EventGhostCom:
    _public_methods_ = ['TriggerEvent', 'BringToFront']
    _reg_progid_ = "EventGhost"
    _reg_clsid_ = "{7EB106DC-468D-4345-9CFE-B0021039114B}"
    _reg_clsctx_ = pythoncom.CLSCTX_LOCAL_SERVER

    def TriggerEvent(self, eventString, payload=None):
        eg.TriggerEvent(eventString, payload)

    def BringToFront(self):
        eg.mainFrame.BringToFront()


