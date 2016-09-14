# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import locale
import os
import sys
import wx
from ftplib import FTP
from os.path import basename, getsize
from threading import Event, Thread
from time import clock
from urlparse import urlparse

locale.setlocale(locale.LC_ALL, '')

class ProgressFile(object):
    """
    A proxy to a file, that also holds progress information.
    """
    def __init__(self, filepath, progressCallback=None):
        self.progressCallback = progressCallback

        self.period = 15
        self.start = 0
        self.lastSecond = 0
        self.rate = 0
        self.lastBytes = 0
        self.Reset()

        self.size = getsize(filepath)
        self.fileObject = open(filepath, "rb")
        self.pos = 0
        self.startTime = clock()

    def Add(self, numBytes):
        now = clock()
        if numBytes == 0 and (now - self.lastSecond) < 0.1:
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
        self.rate += numBytes / div

        self.lastSecond = now
        if numBytes > 0:
            self.lastBytes = now
        if self.rate < 0:
            self.rate = 0

    def close(self):  #IGNORE:C0103 Invalid name "close"
        """
        Implements a file-like close()
        """
        self.fileObject.close()
        elapsed = (clock() - self.startTime)
        print "File uploaded in %0.2f seconds" % elapsed
        print "Average speed: %0.2f KiB/s" % (self.size / (elapsed * 1024))

    def read(self, size):  #IGNORE:C0103 Invalid name "read"
        """
        Implements a file-like read() but also updates the progress variables.
        """
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
        return self.fileObject.read(size)

    def Reset(self):
        now = clock()
        self.start = now
        self.lastSecond = now
        self.rate = 0
        self.lastBytes = 0


class UploadDialog(wx.Dialog):
    """
    The progress dialog that is shown while the file is uploaded.
    """
    def __init__(self, parent, filename, url, stopEvent=None):
        self.stopEvent = stopEvent
        self.abort = False
        self.fileSize = getsize(filename)
        wx.Dialog.__init__(self, parent, title="Upload Progress")
        self.messageCtrl = wx.StaticText(
            self,
            label="Uploading: " + basename(filename),
            style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
        )
        self.gauge = wx.Gauge(
            self,
            range=1000,
            style=wx.GA_HORIZONTAL | wx.GA_SMOOTH,
            size=(-1, 15)
        )
        style  = wx.ALIGN_RIGHT | wx.ST_NO_AUTORESIZE

        def SText(label, *args, **kwargs):
            """
            Simpler creation of a wx.StaticText.
            """
            return wx.StaticText(self, -1, label, *args, **kwargs)

        self.remainingCtrl = SText("0:00:00")
        x, y = self.remainingCtrl.GetSizeTuple()
        self.remainingCtrl.SetMinSize((x, y))
        self.remainingCtrl.SetLabel("-")
        self.speedCtrl = SText("-", size=(x, -1), style=style)
        self.elapsedCtrl = SText("-", size=(x, -1), style=style)
        self.totalTimeCtrl = SText("-", size=(x, -1), style=style)
        self.totalSizeCtrl = SText(FormatBytes(self.fileSize), style=style)
        x, y = self.totalSizeCtrl.GetSizeTuple()
        self.remainingSizeCtrl = SText("-", size=(x, -1), style=style)
        self.transferedSizeCtrl = SText("-", size=(x, -1), style=style)

        self.cancelButton = wx.Button(self, wx.ID_CANCEL)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)

        sizer2 = wx.FlexGridSizer(4, 5, 5, 5)
        sizer2.Add(SText("Upload speed:"), 0, wx.LEFT | wx.ALIGN_RIGHT, 5)
        sizer2.Add(self.speedCtrl)
        sizer2.Add(SText("KiB/s"))
        #sizer2.Add((30, 0))
        sizer2.Add((0, 0))
        sizer2.Add((0, 0))

        sizer2.Add(SText("Elapsed time:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.elapsedCtrl)
        sizer2.Add((10, 0))
        sizer2.Add(SText("Transfered size:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.transferedSizeCtrl)

        sizer2.Add(SText("Remaining time:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.remainingCtrl)
        sizer2.Add((10, 0))
        sizer2.Add(SText("Remaining size:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.remainingSizeCtrl)

        sizer2.Add(SText("Total time:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.totalTimeCtrl)
        sizer2.Add((10, 0))
        sizer2.Add(SText("Total size:"), 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.totalSizeCtrl)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.messageCtrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.gauge, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer2, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        sizer.Add((10, 10))
        sizer.Add(self.cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 10)
        self.SetSizerAndFit(sizer)
        #self.SetSize((350, -1))
        self.Bind(wx.EVT_CLOSE, self.OnCancel)

        self.startTime = clock()
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer(self)
        self.timer.Start(100)
        Thread(target=self.ThreadRun, args=(filename, url)).start()
        self.Show()

    def OnCancel(self, dummyEvent):
        self.abort = True
        self.cancelButton.Enable(False)
        self.messageCtrl.SetLabel("Closing connection. Please wait...")

    def OnTimer(self, dummyEvent):
        """
        Called every second to update the progress dialog.
        """
        elapsedTime = clock() - self.startTime
        self.elapsedCtrl.SetLabel(GetTimeStr(elapsedTime))

    def SetProgress(self, *args, **kwargs):
        wx.CallAfter(self._SetProgress, *args, **kwargs)
        if self.abort:
            return False

    def ThreadRun(self, filename, url):
        """
        Uploads the file in a separate thread.
        """
        try:
            UploadFile(filename, url, self)
        finally:
            if self.stopEvent:
                self.stopEvent.set()
            wx.CallAfter(self.Destroy)

    def _SetProgress(self, percent, speed, remainingTime, transferedSize):
        self.gauge.SetValue(int(percent * 10))
        self.SetTitle("%d%% Upload Progress" % percent)
        self.speedCtrl.SetLabel("%0.2f KiB/s" % speed)
        self.remainingCtrl.SetLabel(GetTimeStr(remainingTime))
        elapsedTime = clock() - self.startTime
        self.totalTimeCtrl.SetLabel(GetTimeStr(remainingTime + elapsedTime))
        self.transferedSizeCtrl.SetLabel(FormatBytes(transferedSize))
        self.remainingSizeCtrl.SetLabel(
            FormatBytes(self.fileSize - transferedSize)
        )


def FormatBytes(numBytes):
    """
    Returns a formatted string of a byte count value.
    """
    return locale.format("%d", numBytes, grouping=True)

def GetTimeStr(seconds):
    """
    Returns a nicely formatted time string.
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%0.2d:%0.2d" % (hours, minutes, seconds)

def Upload(srcFilePath, remoteDir):
    stopEvent = Event()
    wx.CallAfter(
        UploadDialog,
        None,
        srcFilePath,
        remoteDir,
        stopEvent
    )
    stopEvent.wait()

def UploadFile(filename, url, dialog):
    log = dialog.messageCtrl.SetLabel
    urlComponents = urlparse(url)
    if urlComponents.scheme == "ftp":
        UploadWithFtp(urlComponents, filename, dialog, log)
    elif urlComponents.scheme == "sftp":
        UploadWithSftp(urlComponents, filename, dialog, log)
    else:
        log("Unknown upload scheme: %s" % urlComponents.scheme)

def UploadWithFtp(urlComponents, filename, dialog, log):
    infile = ProgressFile(filename, dialog.SetProgress)
    log("Connecting to ftp://%s..." % urlComponents.hostname)
    ftp = FTP(
        urlComponents.hostname,
        urlComponents.username,
        urlComponents.password,
        #timeout = 10
    )
    ftp.set_debuglevel(0)
    log("Changing path to: %s" % urlComponents.path)  #IGNORE:E1101
    ftp.sendcmd("TYPE I")
    ftp.cwd(urlComponents.path)  #IGNORE:E1101
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
    ftp.storbinary("STOR " + tempFileName, infile, 32 * 1024)
    infile.close()
    if dialog.abort:
        ftp.delete(tempFileName)
        ftp.quit()
        log("Upload canceled by user.")
    else:
        ftp.rename(tempFileName, basename(filename))
        ftp.quit()
        log("Upload done!")

def UploadWithSftp(urlComponents, filename, dialog, log):
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import paramiko

    infile = ProgressFile(filename, dialog.SetProgress)
    log("Connecting to sftp://%s..." % urlComponents.hostname)
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        sshClient.connect(
            urlComponents.hostname,
            urlComponents.port,
            urlComponents.username,
            urlComponents.password,
        )
    except paramiko.SSHException:
        exit("Error: Couldn't connect to server")
    except paramiko.AuthenicationException:
        exit("Error: Authentication Exception")
    except paramiko.BadHostKeyException:
        exit("Error: Bad Host Key Exception")

    try:
        client = sshClient.open_sftp()
    except:
        exit("Error: Can't create SFTP client")
    log("Changing path to: %s" % urlComponents.path)  #IGNORE:E1101
    client.chdir(urlComponents.path)  #IGNORE:E1101
    log("Getting directory listing...")
    fileList = client.listdir(urlComponents.path)
    log("Creating temp name.")
    for i in range(0, 999999):
        tempFileName = "tmp%06d" % i
        if tempFileName not in fileList:
            break
    if urlComponents.path[-1] == "/":
        remotePath = urlComponents.path
    else:
        remotePath = urlComponents.path + "/"
    tmpPath = remotePath + tempFileName
    log("Uploading " + basename(filename))

    file_size = os.stat(filename).st_size
    fr = client.file(tmpPath, 'wb')
    fr.set_pipelined(True)
    while True:
        data = infile.read(32768)
        if len(data) == 0:
            break
        fr.write(data)
    infile.close()
    fr.close()
    s = client.stat(tmpPath)

    if dialog.abort:
        client.remove(tmpPath)
        log("Upload canceled by user.")
    else:
        if s.st_size != file_size:
            raise IOError(
                'size mismatch in put!  %d != %d' % (s.st_size, file_size)
            )
        if basename(filename) in fileList:
            client.remove(remotePath + basename(filename))
        client.rename(tmpPath, basename(filename))
        localStat = os.stat(filename)
        client.utime(
            remotePath + basename(filename),
            (localStat.st_atime, localStat.st_mtime)
        )
        log("Upload done!")
    client.close()

def Main():
    """
    Main function if called directly from the command line.
    """
    app = wx.App(0)
    UploadDialog(None, sys.argv[1], sys.argv[2])
    app.MainLoop()

if __name__ == "__main__":
    Main()
