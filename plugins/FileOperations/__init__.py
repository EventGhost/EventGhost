version="0.1.0" 
# This file is part of EventGhost.
# Copyright (C)  2008 Pako  (lubos.ruckl@quick.cz)
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
#Last change: 2008-10-05 17:28

eg.RegisterPlugin(
    name = "File Operations",
    author = "Pako",
    version = version,
    kind = "other",
    createMacrosOnAdd = False,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAA"
        "ABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAINSURBVBgZBcG/r55z"
        "GAfg6/4+z3va01NHlYgzEfE7MdCIGISFgS4Gk8ViYyM2Mdlsko4GSf8Do0FLRCIkghhY"
        "JA3aVBtEz3nP89wf11VJvPDepdd390+8Nso5nESBQoq0pfvXm9fzWf19453LF85vASqJ"
        "lz748vInb517dIw6EyYBIIG49u+xi9/c9MdvR//99MPPZ7+4cP4IZhhTPbwzT2d+vGoa"
        "VRRp1rRliVvHq+cfvM3TD82+7mun0o/ceO7NT+/4/KOXjwZU1ekk0840bAZzMQ2mooqh"
        "0A72d5x/6sB9D5zYnff3PoYBoWBgFKPKqDKqjCpjKr//dcu9p489dra88cydps30KswA"
        "CfNEKanSaxhlntjJ8Mv12Paie+vZ+0+oeSwwQ0Iw1xAR1CiFNJkGO4wu3ZMY1AAzBI0q"
        "SgmCNJsJUEOtJSMaCTBDLyQ0CknAGOgyTyFFiLI2awMzdEcSQgSAAKVUmAeNkxvWJWCG"
        "tVlDmgYQ0GFtgg4pNtOwbBcwQy/Rife/2yrRRVI0qYCEBly8Z+P4qMEMy7JaVw72N568"
        "e+iwhrXoECQkfH91kY7jwwXMsBx1L93ZruqrK6uuiAIdSnTIKKPLPFcvay8ww/Hh+ufe"
        "znTXu49v95IMoQG3784gYXdTqvRmqn/Wpa/ADFX58MW3L71SVU9ETgEIQQQIOOzub+fh"
        "IvwPRDgeVjWDahIAAAAASUVORK5CYII="
    ),
    description = (
        "File Operations (Reading and Writing)."
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=1011"
)
#=========================================================================================================            

import time
import codecs

def String2Hex(string,length='2'):
    tmp = []
    s2h="%0"+length+"X "
    for c in string:
        tmp.append( s2h % ord( c ) )    
    return ''.join( tmp ).strip()  
#=========================================================================================================            

class FileOperations(eg.PluginClass):
    def __init__(self):
        self.AddAction(Read)
        self.AddAction(Write)
#=========================================================================================================            

class Read(eg.ActionClass):
    name = "Read text from file"
    description = "Reads text from selected file."
    class text:
        TreeLabel = "Read file: %s"
        FilePath = "Read file:"
        browseFileDialogTitle = "Choose the file"
        txtMode = "Learning the line(s) return like as a:"
        listNotIncluding = "List of line strings without CR/LF"
        listIncluding = "List of line strings including CR/LF"
        oneNotIncluding = "String without CR/LF"
        oneIncluding = "String including CR/LF"
        oneString = "One string (including CR/LF)"
        systemPage = "system code page (%s)"
        defaultIn = "unicode (UTF-8)"
        inputPage = "Input data coding:"
        txtDecErrMode = "Error handling during decoding:"
        strict = "Raise an exception"
        ignore = "Ignore (skip bad chars)"
        replace = "Replace bad chars"
        lineNum = "Start read at line number:"
        begin = "from the beginning"
        end = "from the end"
        readAhead = "Read"
        readBehind = "lines (0 = whole file)"
    
    def __call__(
        self,
        inCoding = 0,
        fileName = '',
        mode = 0,
        errDecMode = 0,
        inPage = "",
        fromLine = 1,
        direction = 0,
        lines = 1,
    ):
    
        errorList = ('strict','ignore','replace')
        try:
            input = codecs.open(fileName,'r',inPage, errorList[errDecMode])
        except:
            raise            
        if lines > 0:
            data = input.readlines()
            if direction == 0: #from beginning
                data = data[fromLine-1:fromLine+lines-1]
            else:              #from end
                if fromLine-lines < 1:
                    data = data[-fromLine:]
                else:
                    data = data[-fromLine:-(fromLine-lines)]
            if mode == 2:      #one string
                data = ''.join(data)
            elif mode == 0:    #without CR/LF
                tmp = []
                for line in data:
                    tmp.append(line.rstrip())
                data = tmp
            if lines == 1:
                data = data[0]
        else:                  #whole file
            data = input.read()
        try:    
            input.close()
        except:
            raise
            
        return data
            
    def GetLabel(
        self,
        inCoding,
        fileName,
        mode,
        errDecMode,
        inPage,
        fromLine,
        direction,
        lines = 1,
    ):
        return self.text.TreeLabel % (fileName)

    def Configure(
        self,
        inCoding = 0,
        fileName = '',
        mode = 0,
        errDecMode = 0,
        inPage="",
        fromLine=1,
        direction = 0,
        lines = 1,
    ):
        from codecsList import codecsList
        panel = eg.ConfigPanel(self)
        text = self.text
        self.mode = mode
    #Controls    
        inPageText = wx.StaticText(panel, -1, text.inputPage)
        labelMode = wx.StaticText(panel, -1, text.txtMode)
        labelDecErrMode = wx.StaticText(panel, -1, text.txtDecErrMode)
        fileText = wx.StaticText(panel, -1, text.FilePath)
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            -1, 
            initialValue=fileName,
            labelText="",
            fileMask="*.*",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseFileDialogTitle
        )
        width = labelDecErrMode.GetTextExtent(text.txtDecErrMode)[0]
        choiceDecErrMode = wx.Choice(
            panel,
            -1,
            size = ((width,-1)),
            choices=(text.strict, text.ignore, text.replace)
        )
        choiceDecErrMode.SetSelection(errDecMode)
        choices = [text.systemPage % eg.systemEncoding, text.defaultIn]
        choices.extend(codecsList)
        inPageCtrl = wx.Choice(panel,-1,choices=choices)
        inPageCtrl.SetSelection(inCoding)
        lineNumLbl=wx.StaticText(panel, -1, text.lineNum)
        fromLineNumCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            fromLine,
            min = 1,
            max = 999,
        )
        rb0 = panel.RadioButton(not direction, text.begin, style=wx.RB_GROUP)
        rb1 = panel.RadioButton(direction, text.end)                            
        lblAhead = wx.StaticText(panel, -1, text.readAhead)
        lblBehind = wx.StaticText(panel, -1, text.readBehind)
        linesNumCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            lines,
            min = 0,
            max = 999,
        )
        w0 = inPageCtrl.GetTextExtent(text.listNotIncluding)[0]
        w1 = inPageCtrl.GetTextExtent(text.listIncluding)[0]
        w2 = inPageCtrl.GetTextExtent(text.oneNotIncluding)[0]
        w3 = inPageCtrl.GetTextExtent(text.oneIncluding)[0]
        w4 = inPageCtrl.GetTextExtent(text.oneString)[0]
        width = max(w0,w1,w2,w3,w4)+30
        choiceMode = wx.Choice(panel,-1,size=(width,-1))
    #Sizers
        topSizer = wx.FlexGridSizer(2,0,2,15)
        topSizer.AddGrowableCol(0,1)
        topSizer.AddGrowableCol(1,1)
        topSizer.Add(inPageText,0,wx.EXPAND)
        topSizer.Add(labelDecErrMode,0,wx.EXPAND)
        topSizer.Add(inPageCtrl,0,wx.EXPAND)
        topSizer.Add(choiceDecErrMode,0,wx.EXPAND)
        fromSizer = wx.BoxSizer(wx.HORIZONTAL)
        fromSizer.Add(lineNumLbl,0,wx.TOP,4)
        fromSizer.Add(fromLineNumCtrl,0,wx.LEFT,10)
        fromSizer.Add(rb0,0,wx.EXPAND|wx.LEFT,20)
        fromSizer.Add(rb1,0,wx.EXPAND|wx.LEFT,15)
        linesSizer = wx.BoxSizer(wx.HORIZONTAL)
        linesSizer.Add(lblAhead,0,wx.TOP,4)
        linesSizer.Add(linesNumCtrl,0,wx.LEFT|wx.RIGHT,8)
        linesSizer.Add(lblBehind,0,wx.TOP,4)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(fileText,0,wx.EXPAND)
        mainSizer.Add(filepathCtrl,0,wx.EXPAND)
        mainSizer.Add(topSizer,0,wx.TOP|wx.EXPAND,5)
        mainSizer.Add(linesSizer,0,wx.TOP|wx.EXPAND,11)        
        mainSizer.Add(fromSizer,0,wx.TOP|wx.EXPAND,11)        
        mainSizer.Add(labelMode,0,wx.TOP|wx.EXPAND,11)
        mainSizer.Add(choiceMode,0,wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)
        
        def onLinesNumCtrl(event=None):
            flag = False
            if event:
                self.mode = choiceMode.GetSelection()
            if linesNumCtrl.GetValue() == 0:
                fromLineNumCtrl.SetValue(1)
                rb0.SetValue(True)
                rb1.SetValue(False)
                lineNumLbl.Enable(False)
                fromLineNumCtrl.Enable(False)
                rb0.Enable(False)
                rb1.Enable(False)
            else:
                lineNumLbl.Enable(True)                
                fromLineNumCtrl.Enable(True)
                rb0.Enable(True)
                rb1.Enable(True)
            
            if linesNumCtrl.GetValue() == 1:
                choiceMode.Clear()
                choiceMode.AppendItems(strings=(text.oneNotIncluding,text.oneIncluding))
            else:
                if len(choiceMode.GetStrings()) != 3:
                    choiceMode.Clear()
                    choiceMode.AppendItems(
                        strings=(text.listNotIncluding,text.listIncluding,text.oneString)
                    )    
                    if self.mode == 2:
                        flag = True
            if event:
                choiceMode.SetSelection(0)
                event.Skip()
                if flag:
                    self.mode = 0
            choiceMode.SetSelection(self.mode)
        linesNumCtrl.Bind(wx.EVT_SPIN, onLinesNumCtrl)
        onLinesNumCtrl()
            
        while panel.Affirmed():
            inCoding = inPageCtrl.GetSelection()
            pgTpl = (eg.systemEncoding, 'utf8')
            panel.SetResult(
                inCoding,
                filepathCtrl.GetValue(),
                choiceMode.GetSelection(),
                choiceDecErrMode.GetSelection(),
                inPageCtrl.GetStringSelection() if inCoding > 1 else pgTpl[inCoding],
                fromLineNumCtrl.GetValue(),
                rb1.GetValue(),
                linesNumCtrl.GetValue(),
            )
#=========================================================================================================            

class Write(eg.ActionClass):
    name = "Write text to file"
    description = "Writes text to selected file."
    class text:
        TreeLabel = "Write %s to file: %s"
        FilePath = "Output file:"
        browseFileDialogTitle = "Choose the file"
        txtModeMulti = "Mode of write"
        overwrite = "File overwrite"
        append = "Append to file"
        newLine = "Append to file with new line"
        writeToLog = "Write to EventGhost log too"
        systemPage = "system code page (%s)"
        defaultOut = "unicode (UTF-8)"
        hexdump = "String write in the HexDump form"
        inString = "Input text:"
        logTimes = "Write Timestamp"
        outputPage = "Output data coding:"
        txtEncErrMode = "Error handling during encoding:"
        strict = "Raise an exception"
        ignore = "Ignore (skip bad chars)"
        replace = "Replace bad chars"
        internal = 'unicode internal'
    
    def __call__(
        self,
        outCoding,
        string = "",
        fileName = '',
        mode = 0,
        errEncMode = 0,
        log = False,
        times = False,
        hex = False,
        outPage = "",
    ):
        modeStr='w' if mode==0 else 'a'
        stamp = time.strftime('%c')+'  ' if times else ''
        cr = '\r\n' if mode == 2 else ''        
        errorList = ('strict','ignore','replace')
        string = eg.ParseString(string)
        if hex:
            if outPage != 'unicode_internal':
                string = string.encode(outPage,errorList[errEncMode])
                string = String2Hex(string)
            else:
                string = String2Hex(string,'4')
            outPage = 'ascii'
            
        try:
            file = codecs.open(fileName, modeStr, outPage, errorList[errEncMode]) 
        except:
            raise
        try:
            file.write('%s%s%s' % (stamp, string, cr))
        except:
            raise
        try:    
            file.close()
        except:
            raise
        if log:
            print string
        return string
            
    def GetLabel(
        self,
        outCoding,
        string,
        fileName,
        mode,
        errEncMode,
        log,
        times,
        hex,
        outPage,
    ):
        return self.text.TreeLabel % (string, fileName)

    def Configure(
        self,
        outCoding = 2,
        string = "{eg.result}",
        fileName = u'EG_WTTF.txt',
        mode = 2,
        errEncMode = 0,
        log = False,
        times = False,
        hex = False,
        outPage="",
    ):
        from codecsList import codecsList
        panel = eg.ConfigPanel(self)
        text = self.text
    #Controls    
        stringText = wx.StaticText(panel, -1, text.inString)
        outPageText = wx.StaticText(panel, -1, text.outputPage)
        labelEncErrMode = wx.StaticText(panel, -1, text.txtEncErrMode)
        fileText = wx.StaticText(panel, -1, text.FilePath)
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            -1, 
            initialValue=fileName,
            labelText="",
            fileMask="*.*",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseFileDialogTitle
        )
        width = labelEncErrMode.GetTextExtent(text.txtEncErrMode)[0]
        choiceEncErrMode = wx.Choice(
            panel,
            -1,
            size = ((width,-1)),
            choices=(text.strict, text.ignore, text.replace)
        )
        stringCtrl = wx.TextCtrl(panel, -1, string, style=wx.TE_NOHIDESEL)
        radioBoxMode = wx.RadioBox(
            panel, 
            -1, 
            text.txtModeMulti,
            choices=[text.overwrite, text.append, text.newLine],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(mode)
        choiceEncErrMode.SetSelection(errEncMode)
        writeToLogCheckBox = wx.CheckBox(panel, -1, text.writeToLog)
        writeToLogCheckBox.SetValue(log)
        timesCheckBox = wx.CheckBox(panel, -1, text.logTimes)
        timesCheckBox.SetValue(times)
        hexCheckBox = wx.CheckBox(panel, -1, text.hexdump)
        hexCheckBox.SetValue(hex)
        choices = [text.internal, text.defaultOut, text.systemPage % eg.systemEncoding]
        choices.extend(codecsList)
        outPageCtrl = wx.Choice(panel,-1,choices=choices)
        outPageCtrl.SetSelection(outCoding)
    #Sizers
        topSizer = wx.FlexGridSizer(5,0,1,15)
        topSizer.AddGrowableCol(0,1)
        topSizer.AddGrowableCol(1,1)
        topSizer.Add(stringText,0,wx.EXPAND)
        topSizer.Add(fileText,0,wx.EXPAND)
        topSizer.Add(stringCtrl,0,wx.EXPAND)
        topSizer.Add(filepathCtrl,0,wx.EXPAND)
        topSizer.Add((1,7))
        topSizer.Add((1,7))
        topSizer.Add(outPageText,0,wx.EXPAND)
        topSizer.Add(labelEncErrMode,0,wx.EXPAND)
        topSizer.Add(outPageCtrl,0,wx.EXPAND)
        topSizer.Add(choiceEncErrMode,0,wx.EXPAND)
        chkBoxSizer = wx.BoxSizer(wx.VERTICAL)
        chkBoxSizer.Add(writeToLogCheckBox,0,wx.TOP|wx.LEFT,12)        
        chkBoxSizer.Add(timesCheckBox,0,wx.TOP|wx.LEFT,12)     
        chkBoxSizer.Add(hexCheckBox,0,wx.TOP|wx.LEFT,12)     
        bottomSizer = wx.GridSizer(1,2,1,10)
        bottomSizer.Add(radioBoxMode,0,wx.TOP|wx.EXPAND,5)
        bottomSizer.Add(chkBoxSizer,1,wx.EXPAND)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer,0,wx.EXPAND)
        mainSizer.Add(bottomSizer,0,wx.TOP|wx.EXPAND,10)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)

        while panel.Affirmed():
            outCoding = outPageCtrl.GetSelection()
            pgTpl = ('unicode_internal', 'utf8', eg.systemEncoding)
            panel.SetResult(
                outCoding,
                stringCtrl.GetValue(),
                filepathCtrl.GetValue(),
                radioBoxMode.GetSelection(),
                choiceEncErrMode.GetSelection(),
                writeToLogCheckBox.IsChecked(),
                timesCheckBox.IsChecked(),
                hexCheckBox.IsChecked(),
                outPageCtrl.GetStringSelection() if outCoding > 2 else pgTpl[outCoding],
            )        
#=========================================================================================================            
