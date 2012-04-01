# -*- coding: utf-8 -*-
# ActiveX/COM Snarl python library
# For proper functioning requires Snarl 2.5.1 or later !
# Version 0.0.2

# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.2 by Pako 2012-01-30 14:12 UTC+1
#     - base64 icon format is now supported
# 0.0.1 by Pako 2012-01-06 15:30 UTC+1
#     - initial version
#-------------------------------------------------------

from win32com.client import constants, gencache, Dispatch, DispatchWithEvents
#===============================================================================

def IsRunning():
    from win32gui import FindWindow
    return FindWindow("w>Snarl", "Snarl")
#===============================================================================

class EventHandler:

    def OnActivated(self):
        self.fn("DaemonActivated")

    def OnNotificationActionSelected(self, uid, command):
        self.fn("ActionSelected.%s" % command, payload = uid)

    def OnNotificationClosed(self, uid):
        self.fn("Closed", payload = uid)

    def OnNotificationExpired(self, uid):
        self.fn("Expired", payload = uid)

    def OnNotificationInvoked(self, uid):
        self.fn("Invoked", payload = uid)

    def OnQuit(self):
        self.fn("AppQuit")

    def OnShowAbout(self):
        self.fn("ShowAbout")

    def OnShowConfig(self):
        self.fn("ShowConfig")

    def OnSnarlLaunched(self):
        self.fn("Launched")

    def OnSnarlQuit(self):
        self.fn("Quit")

    def OnSnarlStarted(self):
        self.fn("Started")

    def OnSnarlStopped(self):
        self.fn("Stopped")

    def OnUserAway(self):
        self.fn("UserAway")

    def OnUserReturned(self):
        self.fn("UserReturned")
#===============================================================================

class SnarlApp(object):
    """Creates an SnarlApp object"""

    def __init__(
        self,
        signature,
        title,
        icon = "",
        configTool = "",
        hint = "",
        isDaemon = False,
        eventHandler = None,
        classes = []
    ):
        self.app = gencache.EnsureDispatch("libsnarl25.SnarlApp")
        for d in constants.__dicts__: # we must find the right dictionary ...
            if 'ERROR_NOTIFICATION_NOT_FOUND' in d: # this is it !
                break        
        codes = d.items()
        codes.sort(reverse = True)
        self.statCodes = dict([[v,k] for k,v in codes[6:]])
        self.statCodes[codes[2][1]] = codes[2][0] # added SUCCESS
        self.classes = NotifClasses(classes)
        if eventHandler:
            self.SetEventHandler(eventHandler)
        self.SetTo(
            configTool,
            hint,
            icon,
            isDaemon,
            signature,
            title
        )


    def SetTo(
        self,
        configTool,
        hint,
        icon,
        isDaemon,
        signature,
        title
    ):
        self.app.Classes = self.classes.Classes()
        self.app.ConfigTool = configTool
        self.app.Hint = hint
        self.app.Icon = icon
        self.app.IsDaemon = isDaemon
        self.app.Signature = signature
        self.app.Title = title


    def GetStatusCode(self, code):
        return self.statCodes[code]


    def SetEventHandler(self, handler):
        self.events = DispatchWithEvents(self.app, handler)


    def register(self):
        return self.GetStatusCode(self.app.Register())


    def unregister(self):
        return self.GetStatusCode(self.app.Unregister())


    def tidyUp(self):
        self.app.TidyUp()


    def addClass(
        self,
        classId,
        name,
        enabled = True,
        title = "",
        text = "",
        icon = "",
        callback = "",
        duration = -1,
        sound = "",
    ):
        cntOld = self.classes.count()
        cntNew = self.classes.add(classId, name, enabled, title, text, icon, callback, duration, sound)
        return int(not cntNew == cntOld + 1)


    def remClass(self, id):
        cntOld = self.classes.count()
        cntNew = self.classes.remove(id)
        return int(not cntNew == cntOld - 1)


    def clearClasses(self):
        return self.classes.makeEmpty()


    def classesCount(self):
        return self.classes.count()


    def notify(
        self,
        actions,
        callbackScript,
        callbackScriptType,
        cls,
        defaultCallback,
        duration,
        icon,
        mergeUID,
        priority,
        replaceUID,
        text,
        title,
        uid,
        sound = None,
        percent = None,
        log = None,
        sensitivity = None
    ):
        note = Notification(
            actions,
            callbackScript,
            callbackScriptType,
            cls,
            defaultCallback,
            duration,
            "",
            mergeUID,
            priority,
            replaceUID,
            text,
            title,
            uid,
        )
        if icon:
            if icon[1] == ":":
                note.Add("icon", icon, True)
            else:
                note.Add("icon-base64", icon.replace("=","%"), True)
        if sound:
            note.Add("sound", sound, True)
        if percent is not None and percent > -1:
            note.Add("value-percent", str(percent), True)
        if log is not None:
            note.Add("log", str(log), True)
        if sensitivity is not None:
            note.Add("sensitivity", str(sensitivity), True)
        return self.GetStatusCode(self.app.Show(note.Note())[0])


    def hideNotification(self, uid):
        return self.GetStatusCode(self.app.Hide(uid))


    def isVisible(self, uid):
        return self.GetStatusCode(self.app.IsVisible(uid))


    def getEtcPath(self):
        return self.app.GetEtcPath()


    def makePath(self, pth):
        return self.app.GetEtcPath(pth)


    def isInstalled(self):
        return self.app.IsSnarlInstalled()


    def isRunning(self):
        return self.app.IsSnarlRunning()


    def version(self):
        ver = self.app.SnarlVersion()
        return ver if ver > 0 else self.GetStatusCode(-ver)


    def isConnected(self):
        return self.app.IsConnected


    def getLibVersion(self):
        return self.app.LibVersion


    def getLibRevision(self):
        return self.app.LibRevision


    def Destroy(self):
        self.app.TidyUp()
        if self.events:
            del self.events
        del self.app
#===============================================================================

class NotifClasses(object):
    def __init__(self, classes = []):
        self.clss = Dispatch("libsnarl25.Classes")
        for cls in classes:
            self.add(*cls)

    def count(self):
        return self.clss.Count()

    def add(self, *cls):
        self.clss.Add(*cls)
        return self.clss.Count()

    def remove(self, cls):
        self.clss.Remove(cls)
        return self.clss.Count()

    def makeEmpty(self):
        self.clss.MakeEmpty()
        return self.clss.Count()

    def Classes(self):
        return self.clss
#===============================================================================

class Notification(object):
    def __init__(
        self,
        actions,
        callbackScript,
        callbackScriptType,
        cls,
        defaultCallback,
        duration,
        icon,
        mergeUID,
        priority,
        replaceUID,
        text,
        title,
        uid,
    ):
        nt = Dispatch("libsnarl25.Notification")
        nt.Actions = NotifActions(actions).Actions()
        nt.CallbackScript = callbackScript
        nt.CallbackScriptType = callbackScriptType
        nt.Class = cls
        nt.DefaultCallback = defaultCallback
        nt.Duration = duration
        if icon:
            nt.Icon = icon
        nt.MergeUID = mergeUID
        nt.Priority = priority
        nt.ReplaceUID = replaceUID
        nt.Text = text
        nt.Title = title
        nt.UID = uid
        self.nt = nt

    def Add(self, name, value, update):
        self.nt.Add(name, value, True)

    def Note(self):
        return self.nt
#===============================================================================

class NotifActions(object):
    def __init__(self, actions=[]):
        self.actns = Dispatch("libsnarl25.Actions")
        self.actions = actions
        for action in actions:
            self.actns.Add(*action)

    def add(self, actn):
        self.actns.Add(*actn)
        self.actions.append(actn)
        return self.actns.Count()

    def remove(self, actn):
        if actn in self.actions:
            ix = self.actions.index(actn)
            self.actns.Remove(ix + 1)
            self.actions.pop(ix)
        return self.actns.Count()

    def makeEmpty(self):
        self.actns.MakeEmpty()
        self.actions = []
        return self.actns.Count()

    def Actions(self):
        return self.actns
#===============================================================================



