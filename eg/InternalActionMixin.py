from ActionClass import ActionClass, ActionWithStringParameter

class _mixin:
    def GetLabel(self, *args, **kwargs):
        s = self.name
        if args:
            s += ': ' + str(args[0])
        return s
    
    
    def GetTitle(self):
        return self.name
        


class ActionClass(_mixin, ActionClass):
    pass


class ActionWithStringParameter(_mixin, ActionWithStringParameter):
    pass
