import wx
from time import clock
from os.path import basename, getsize
from threading import Thread
from ftplib import FTP
from urlparse import urlparse


def GetTimeStr(t):
    t, s = divmod(t, 60)
    h, m = divmod(t, 60)
    return "%d:%0.2d:%0.2d" % (h, m, s)
    

class ProgressFile(object):
    
    def __init__(self, filepath, progressCallback=None):
        self.progressCallback = progressCallback
        
        self.period = 15
        self.Reset()

        self.size = getsize(filepath)
        self.fd = open(filepath, "rb")
        self.pos = 0
        self.startTime = clock()
        
        
    def Reset(self):
        now = clock()
        self.start = now
        self.lastSecond = now
        self.rate = 0
        self.lastBytes = 0
        
        
    def read(self, size):
        if size + self.pos > self.size:
            size = self.size - self.pos
        self.Add(size)
        remaining = (self.size - self.pos + size) / self.rate
        percent = 100.0 * self.pos / self.size
        if self.progressCallback:
            res = self.progressCallback(percent, (self.rate / 1024), remaining)
            if res is False:
                return ""      
        self.pos += size
        return self.fd.read(size)


    def close(self):
        self.fd.close()
        elapsed = (clock() - self.startTime)
        print "File uploaded in %0.2f seconds" % elapsed
        print "Average speed: %0.2f KiB/s" % (self.size / (elapsed * 1024))

    
    def Add(self, b):
        now = clock()
        if b == 0 and (now - self.lastSecond) < 0.1:
            return
        
        if self.rate == 0:
            self.Reset()
            
        div = self.period * 1.0
        if self.start > now:
            self.start = now
        if now < self.lastSecond:
            self.lastSecond = now
            
        timePassedSinceStart = now - self.start
        timePassed = now - self.lastSecond
        if timePassedSinceStart < div:
            div = timePassedSinceStart
        if div < 1:
            div = 1.0
            
        self.rate *= 1 - timePassed / div
        self.rate += b / div
        
        self.lastSecond = now
        if b > 0:
            self.lastBytes = now
        if self.rate < 0:
            self.rate = 0
        
        
        
def UploadFile(filename, url, dialog):
    log = dialog.messageCtrl.SetLabel
    urlComponents = urlparse(url)
    fd = ProgressFile(filename, dialog.SetProgress)
    log("Connecting to ftp://%s..." % urlComponents.hostname)
    ftp = FTP(
        urlComponents.hostname, 
        urlComponents.username, 
        urlComponents.password,
        timeout = 10
    )
    log("Changing path to: %s" % urlComponents.path)
    ftp.cwd(urlComponents.path)
    log("Getting directory listing...")
    try:
        fileList = ftp.nlst()
    except:
        fileList = []
    log("Creating temp name.")
    for i in range(0, 999999):
        tempFileName = "tmp%06d" % i
        if tempFileName not in fileList:
            break
    log("Uploading " + basename(filename))
    ftp.storbinary("STOR " + tempFileName, fd, 32 * 1024)
    fd.close()
    if dialog.abort:
        ftp.delete(tempFileName)
        ftp.quit()
        log("Upload canceled by user.")
    else:
        ftp.rename(tempFileName, basename(filename))
        ftp.quit()
        log("Upload done!")
    
    
    
class UploadDialog(wx.Dialog):
    
    def __init__(self, parent, filename, url):
        self.abort = False
        wx.Dialog.__init__(self, parent, title="Upload Progress")
        self.messageCtrl = wx.StaticText(
            self, 
            label="Uploading: " + basename(filename), 
            style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE
        )
        self.gauge = wx.Gauge(
            self, 
            range=1000, 
            style=wx.GA_HORIZONTAL|wx.GA_SMOOTH
        )
        self.speedCtrl = wx.StaticText(self, -1, "-")
        self.remainingCtrl = wx.StaticText(self, -1, "-")
        self.elapsedCtrl = wx.StaticText(self, -1, "-")
        self.totalTimeCtrl = wx.StaticText(self, -1, "-")
        
        self.cancelButton = wx.Button(self, wx.ID_CANCEL)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.messageCtrl, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.gauge, 0, wx.EXPAND|wx.ALL, 5)
        
        sizer2 = wx.GridSizer(4, 2, 5, 5)
        label = wx.StaticText(self, -1, "Upload speed:")
        sizer2.Add(label, 0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        sizer2.Add(self.speedCtrl, 0, wx.LEFT, 5)
        label = wx.StaticText(self, -1, "Elapsed time:")
        sizer2.Add(label, 0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        sizer2.Add(self.elapsedCtrl, 0, wx.LEFT, 5)
        label = wx.StaticText(self, -1, "Remaining time:")
        sizer2.Add(label, 0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        sizer2.Add(self.remainingCtrl, 0, wx.LEFT, 5)
        label = wx.StaticText(self, -1, "Total time:")
        sizer2.Add(label, 0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        sizer2.Add(self.totalTimeCtrl, 0, wx.LEFT, 5)
        
        sizer.Add(sizer2, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add((10, 10))
        sizer.Add(self.cancelButton, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 10)
        self.SetSizerAndFit(sizer)
        self.SetSize((300, -1))
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.OnCancel)
        self.thread = Thread(target=self.ThreadRun, args=(filename, url))
        self.startTime = clock()
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        self.thread.start()
        
        
    def OnTimer(self, event):
        elapsedTime = clock() - self.startTime
        self.elapsedCtrl.SetLabel(GetTimeStr(elapsedTime))
        
    
    def ThreadRun(self, filename, url):
        try:
            UploadFile(filename, url, self)
        finally:
            wx.CallAfter(self.Destroy)
    
    
    def OnCancel(self, event):
        self.abort = True
        self.cancelButton.Enable(False)
        self.messageCtrl.SetLabel("Closing connection. Please wait...")
     
     
    def SetProgress(self, percent, speed, remaining):
        wx.CallAfter(self._SetProgress, percent, speed, remaining)
        if self.abort:
            return False
        
        
    def _SetProgress(self, percent, speed, remaining):
        self.gauge.SetValue(int(percent * 10))
        self.SetTitle("%d%% Upload Progress" % percent)
        self.speedCtrl.SetLabel("%0.2f KiB/s" % speed)
        self.remainingCtrl.SetLabel(GetTimeStr(remaining))
        elapsedTime = clock() - self.startTime
        #self.elapsedCtrl.SetLabel(GetTimeStr(elapsedTime))
        self.totalTimeCtrl.SetLabel(GetTimeStr(remaining + elapsedTime))
        
        