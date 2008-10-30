# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate: 2008-10-09 23:58:28 +0200 (Do, 09 Okt 2008) $
# $LastChangedRevision: 521 $
# $LastChangedBy: bitmonster $

import wx
import sys
from time import clock
from os.path import basename, getsize
from threading import Thread
from ftplib import FTP
from urlparse import urlparse
import functools
import locale

locale.setlocale(locale.LC_ALL, '')
FormatBytes = functools.partial(locale.format, "%d", grouping=True)

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
            res = self.progressCallback(
                percent, 
                (self.rate / 1024), 
                remaining, 
                self.pos
            )
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
        #timeout = 10
    )
    ftp.set_debuglevel(0)
    log("Changing path to: %s" % urlComponents.path)
    ftp.sendcmd("TYPE I")
    ftp.cwd(urlComponents.path)
    log("Getting directory listing...")
    # Some ProFTP versions have a bug when submitting the contents of an
    # empty directory with the NLST command. The command will never return, 
    # because ProFTP dosn't open a data connection in this case.
    # So we first use the LIST command to make sure the directory is not empty
    fileList = []
    ftp.dir(fileList.append)
    if len(fileList):
        fileList = ftp.nlst()
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
        self.fileSize = getsize(filename)
        wx.Dialog.__init__(self, parent, title="Upload Progress")
        self.messageCtrl = wx.StaticText(
            self, 
            label="Uploading: " + basename(filename), 
            style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE
        )
        self.gauge = wx.Gauge(
            self, 
            range=1000, 
            style=wx.GA_HORIZONTAL|wx.GA_SMOOTH,
            size=(-1, 15)
        )
        style  = wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE
        self.remainingCtrl = wx.StaticText(self, -1, "0:00:00", style=style)
        x, y = self.remainingCtrl.GetSizeTuple()
        self.remainingCtrl.SetMinSize((x, y))
        self.remainingCtrl.SetLabel("-")
        self.speedCtrl = wx.StaticText(self, -1, "-", size=(x, -1), style=style)
        self.elapsedCtrl = wx.StaticText(self, -1, "-", size=(x, -1), style=style)
        self.totalTimeCtrl = wx.StaticText(self, -1, "-", size=(x, -1), style=style)
        self.totalSizeCtrl = wx.StaticText(
            self, 
            -1, 
            FormatBytes(self.fileSize), 
            style=style
        )
        x, y = self.totalSizeCtrl.GetSizeTuple()
        self.remainingSizeCtrl = wx.StaticText(self, -1, "-", size=(x, -1), style=style)
        self.transferedSizeCtrl = wx.StaticText(self, -1, "-", size=(x, -1), style=style)
        
        self.cancelButton = wx.Button(self, wx.ID_CANCEL)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        def ST(label, *args, **kwargs):
            return wx.StaticText(self, -1, label, *args, **kwargs)
        
        sizer2 = wx.FlexGridSizer(4, 5, 5, 5)
        sizer2.Add(ST("Upload speed:"), 0, wx.LEFT|wx.ALIGN_RIGHT, 5)
        sizer2.Add(self.speedCtrl)
        sizer2.Add((30, 0))
        sizer2.Add((0, 0))
        sizer2.Add((0, 0))
        
        sizer2.Add(ST("Elapsed time:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.elapsedCtrl)
        sizer2.Add((10, 0))
        sizer2.Add(ST("Transfered size:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.transferedSizeCtrl)
        
        sizer2.Add(ST("Remaining time:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.remainingCtrl)
        sizer2.Add((10, 0))
        sizer2.Add(ST("Remaining size:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.remainingSizeCtrl)
        
        sizer2.Add(ST("Total time:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.totalTimeCtrl)
        sizer2.Add((10, 0))
        sizer2.Add(ST("Total size:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.totalSizeCtrl)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.messageCtrl, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.gauge, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(sizer2, 0, wx.ALIGN_CENTER|wx.EXPAND|wx.LEFT|wx.RIGHT, 15)
        sizer.Add((10, 10))
        sizer.Add(self.cancelButton, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 10)
        self.SetSizerAndFit(sizer)
        #self.SetSize((350, -1))
        self.Bind(wx.EVT_CLOSE, self.OnCancel)
        self.thread = Thread(target=self.ThreadRun, args=(filename, url))
        self.startTime = clock()
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        self.thread.start()
        self.Show()
       
        
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
     
     
    def SetProgress(self, *args, **kwargs):
        wx.CallAfter(self._SetProgress, *args, **kwargs)
        if self.abort:
            return False
        
        
    def _SetProgress(self, percent, speed, remainingTime, transferedSize):
        self.gauge.SetValue(int(percent * 10))
        self.SetTitle("%d%% Upload Progress" % percent)
        self.speedCtrl.SetLabel("%0.2f KiB/s" % speed)
        self.remainingCtrl.SetLabel(GetTimeStr(remainingTime))
        elapsedTime = clock() - self.startTime
        self.totalTimeCtrl.SetLabel(GetTimeStr(remainingTime + elapsedTime))
        self.transferedSizeCtrl.SetLabel(FormatBytes(transferedSize))
        self.remainingSizeCtrl.SetLabel(FormatBytes(self.fileSize - transferedSize))
        
        
if __name__ == "__main__":
    app = wx.App(0)
    UploadDialog(None, sys.argv[1], sys.argv[2])
    app.MainLoop()