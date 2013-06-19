# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import keyword
import re
from wx.stc import *

faces = { 
    'times': 'Times New Roman',
    'mono' : 'Courier New',
    'helv' : 'Arial',
    'other': 'Comic Sans MS',
    'size' : 10,
    'size2': 8,
}


class PythonEditorCtrl(StyledTextCtrl):
    
    def __init__(
        self, 
        parent, 
        ID=-1,
        pos=wx.DefaultPosition, 
        size=wx.DefaultSize,
        style=0,
        value="",
    ):
        StyledTextCtrl.__init__(self, parent, ID, pos, size, style)
        StyleSetSpec = self.StyleSetSpec
        
        self.CmdKeyAssign(ord('B'), STC_SCMOD_CTRL, STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), STC_SCMOD_CTRL, STC_CMD_ZOOMOUT)

        # Setup a margin to hold fold markers
        #self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
        self.SetMarginType(2, STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        # line numbers in the margin
        self.SetMarginType(1, STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 25)

        self.Bind(EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.Bind(EVT_STC_CHARADDED, self.OnCharAdded)
        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.

        # Global default styles for all languages
        StyleSetSpec(STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        StyleSetSpec(STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        StyleSetSpec(STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)

        # Python styles
        # End of line where string is not closed
        StyleSetSpec(
            STC_P_STRINGEOL, 
            "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces
        )

        # register some images for use in the AutoComplete box.
        #self.RegisterImage(1, images.getSmilesBitmap())
        #self.RegisterImage(2, images.getFile1Bitmap())
        #self.RegisterImage(3, images.getCopy2Bitmap())


        self.SetLexer(STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        # Enable folding
        self.SetProperty("fold", "1" ) 

        # Highlight tab/space mixing (shouldn't be any)
        self.SetProperty("tab.timmy.whinge.level", "1")

        # Set left and right margins
        self.SetMargins(2,2)

        # Set up the numbers in the margin for margin #1
        self.SetMarginType(1, STC_MARGIN_NUMBER)
        # Reasonable value for, say, 4-5 digits using a mono font (40 pix)
        self.SetMarginWidth(1, 40)

        # Indentation and tab stuff
        self.SetIndent(4)               # Proscribed indent size for wx
        self.SetIndentationGuides(True) # Show indent guides
        self.SetBackSpaceUnIndents(True)# Backspace unindents rather than delete 1 space
        self.SetTabIndents(True)        # Tab key indents
        self.SetTabWidth(4)             # Proscribed tab size for wx
        self.SetUseTabs(False)          # Use spaces rather than tabs, or
                                        # TabTimmy will complain!    
        # White space
        self.SetViewWhiteSpace(False)   # Don't view white space

        # EOL: Since we are loading/saving ourselves, and the
        # strings will always have \n's in them, set the STC to
        # edit them that way.            
        self.SetEOLMode(STC_EOL_LF)
        self.SetViewEOL(False)
        
        # No right-edge mode indicator
        self.SetEdgeMode(STC_EDGE_NONE)

        # Setup a margin to hold fold markers
        self.SetMarginType(2, STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        # and now set up the fold markers
        MarkerDefine = self.MarkerDefine
        MarkerDefine(STC_MARKNUM_FOLDEREND, STC_MARK_BOXPLUSCONNECTED, "white", "black")
        MarkerDefine(STC_MARKNUM_FOLDEROPENMID, STC_MARK_BOXMINUSCONNECTED, "white", "black")
        MarkerDefine(STC_MARKNUM_FOLDERMIDTAIL, STC_MARK_TCORNER, "white", "black")
        MarkerDefine(STC_MARKNUM_FOLDERTAIL, STC_MARK_LCORNER, "white", "black")
        MarkerDefine(STC_MARKNUM_FOLDERSUB, STC_MARK_VLINE, "white", "black")
        MarkerDefine(STC_MARKNUM_FOLDER, STC_MARK_BOXPLUS, "white", "black")
        MarkerDefine(STC_MARKNUM_FOLDEROPEN, STC_MARK_BOXMINUS, "white", "black")

        # Global default style
        if wx.Platform == '__WXMSW__':
            StyleSetSpec(STC_STYLE_DEFAULT, 
                              'fore:#000000,back:#FFFFFF,face:Courier New,size:9')
        else:
            StyleSetSpec(STC_STYLE_DEFAULT, 
                              'fore:#000000,back:#FFFFFF,face:Courier,size:12')

        # Clear styles and revert to default.
        self.StyleClearAll()

        # Following style specs only indicate differences from default.
        # The rest remains unchanged.

        # Line numbers in margin
        StyleSetSpec(STC_STYLE_LINENUMBER,'fore:#000000,back:#99A9C2')    
        # Highlighted brace
        StyleSetSpec(STC_STYLE_BRACELIGHT,'fore:#00009D,back:#FFFF00')
        # Unmatched brace
        StyleSetSpec(STC_STYLE_BRACEBAD,'fore:#00009D,back:#FF0000')
        # Indentation guide
        StyleSetSpec(STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")

        # Python styles
        StyleSetSpec(STC_P_DEFAULT, 'fore:#000000')
        # Comments
        StyleSetSpec(STC_P_COMMENTLINE,  'fore:#008000')
        StyleSetSpec(STC_P_COMMENTBLOCK, 'fore:#008000')
        # Numbers
        StyleSetSpec(STC_P_NUMBER, 'fore:#008080')
        # Strings and characters
        StyleSetSpec(STC_P_STRING, 'fore:#800080')
        StyleSetSpec(STC_P_CHARACTER, 'fore:#800080')
        # Keywords
        StyleSetSpec(STC_P_WORD, 'fore:#000080,bold')
        # Triple quotes
        #StyleSetSpec(STC_P_TRIPLE, 'fore:#800080,back:#FFFFEA')
        #StyleSetSpec(STC_P_TRIPLEDOUBLE, 'fore:#800080,back:#FFFFEA')
        StyleSetSpec(STC_P_TRIPLE, 'fore:#808000')
        StyleSetSpec(STC_P_TRIPLEDOUBLE, 'fore:#808000')
        # Class names
        StyleSetSpec(STC_P_CLASSNAME, 'fore:#0000FF,bold')
        # Function names
        StyleSetSpec(STC_P_DEFNAME, 'fore:#008080,bold')
        # Operators
        StyleSetSpec(STC_P_OPERATOR, 'fore:#800000,bold')
        # Identifiers. I leave this as not bold because everything seems
        # to be an identifier if it doesn't match the above criterae
        StyleSetSpec(STC_P_IDENTIFIER, 'fore:#000000')

        # Caret color
        self.SetCaretForeground("BLUE")
        # Selection background
        self.SetSelBackground(1, '#66CCFF')

        self.SetSelBackground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.UsePopUp(False)
        
        #Keyword Search/Context Sensitive Autoindent.
        self.rekeyword = re.compile(r"(\sreturn\b)|(\sbreak\b)|(\spass\b)|(\scontinue\b)|(\sraise\b)", re.MULTILINE)
        self.reslash = re.compile(r"\\\Z")
        self.renonwhitespace = re.compile('\S', re.M)
        self.tabwidth = 4
        
        # popup menu
        popupMenu = self.popupMenu = eg.Menu(self, "", eg.text.MainFrame.Menu)
        AddItem = popupMenu.AddItem
        AddItem("Undo")
        AddItem("Redo")
        AddItem()
        AddItem("Cut")
        AddItem("Copy")
        AddItem("Paste")
        AddItem("Delete")
        AddItem()
        AddItem("SelectAll")
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        
        self.SetText(value)
        self.EmptyUndoBuffer()
        self.Bind(EVT_STC_SAVEPOINTLEFT, self.OnSavePointLeft)
        
        
    def OnSavePointLeft(self, event):
        self.Bind(EVT_STC_MODIFIED, self.OnModified)
        wx.PostEvent(self, eg.ValueChangedEvent(self.GetId()))
        event.Skip()
        
        
    def OnModified(self, event):
        wx.PostEvent(self, eg.ValueChangedEvent(self.GetId()))
        event.Skip()
    
    
    def GetValue(self):
        return self.GetText()
    
    
    def SetValue(self, value):
        self.SetText(value)
    
    
    def OnRightClick(self, event):
        self.ValidateEditMenu(self.popupMenu)
        self.PopupMenu(self.popupMenu)


    def ValidateEditMenu(self, menu):
        menu.Undo.Enable(self.CanUndo())
        menu.Redo.Enable(self.CanRedo())
        first, last = self.GetSelection()
        menu.Cut.Enable(first != last)
        menu.Copy.Enable(first != last)
        menu.Paste.Enable(self.CanPaste())
        menu.Delete.Enable(True)

        
    def OnCmdUndo(self, event):
        self.Undo()
        
        
    def OnCmdRedo(self, event):
        self.Redo()
        
        
    def OnCmdCut(self, event):
        self.Cut()
        
        
    def OnCmdCopy(self, event):
        self.Copy()
        
        
    def OnCmdPaste(self, event):
        self.Paste()
        
        
    def OnCmdDelete(self, event):
        self.Delete()
        
        
    def OnCmdSelectAll(self, event):
        self.SelectAll()
        
        
    def Delete(self):
        self.CmdKeyExecute(STC_CMD_CLEAR)
        
        
    def OnKeyPressed(self, event):
        keycode = event.GetKeyCode()
        if (keycode == wx.WXK_RETURN) or (keycode == 372):
            self.CmdKeyExecute(STC_CMD_NEWLINE)
            self._autoindent()
        elif keycode == wx.WXK_TAB and event.GetModifiers() == wx.MOD_CONTROL:
            self.Navigate()
        else:
            event.Skip()
    
    
    def OnCharAdded(self, event):
        event.Skip()
        return
        if event.GetKey() == ord('\n') or event.GetKey() == ord('\r'):
            line = self.GetCurrentLine()                              
            if line > 0:
                indent = self.GetLineIndentation(line-1)
                if indent > 0:
                    prevline = self.GetLine(line-1)
                    i = 0
                    while prevline[i] == ' ' or prevline[i] == '\t':
                        self.AddText(prevline[i])
                        i = i+1
                    if prevline[len(prevline)-2] == '{':
                        self.AddText('\t')


    def OnUpdateUI(self, evt):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
            #pt = self.PointFromPosition(braceOpposite)
            #self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            #self.Refresh(False)


    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)


    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in xrange(lineCount):
            if self.GetFoldLevel(lineNum) & STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break;

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & STC_FOLDLEVELHEADERFLAG and \
               (level & STC_FOLDLEVELNUMBERMASK) == STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1


    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels-1)
                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1;

        return line


    def _autoindent(self):
        pos = self.GetCurrentPos()
        
        #Strip trailing whitespace first.
        currentline = self.LineFromPosition(pos)
        lineendpos = self.GetLineEndPosition(currentline)
        if lineendpos > pos:
            self.SetTargetStart(pos)
            self.SetTargetEnd(lineendpos)
            t = self.GetTextRange(pos, lineendpos)
            self.ReplaceTarget(t.rstrip())

        #Look at last line
        pos = pos - 1
        clinenumber = self.LineFromPosition(pos)
        
        linenumber = clinenumber
            
        self.GotoPos(pos)
                
        self.GotoLine(clinenumber)

        numtabs = self.GetLineIndentation(clinenumber+1) / self.tabwidth
        
        if self.renonwhitespace.search(self.GetLine(clinenumber+1)) is not None:
            if self.renonwhitespace.search(self.GetLine(clinenumber)) is None:
                numtabs += self.GetLineIndentation(clinenumber) / self.tabwidth
        
        if numtabs == 0:
            numtabs = self.GetLineIndentation(linenumber) / self.tabwidth
        
        if True:
            checkat = self.GetLineEndPosition(linenumber) - 1
            if self.GetCharAt(checkat) == ord(':'):
                numtabs = numtabs + 1
            else:
                lastline = self.GetLine(linenumber)
                #Remove Comment:
                comment = lastline.find('#')
                if comment > -1:
                    lastline = lastline[:comment]
                if self.reslash.search(lastline.rstrip()) is None:
                    if self.rekeyword.search(lastline) is not None:
                        numtabs = numtabs - 1
        #Go to current line to add tabs
        
        self.SetTargetStart(pos+1)
        end = self.GetLineEndPosition(clinenumber+1)
        self.SetTargetEnd(end)
        
        self.ReplaceTarget(self.GetTextRange(pos+1, end).lstrip())

        pos = pos + 1
        self.GotoPos(pos)
        x = 0
        while (x < numtabs):
            self.AddText('    ')
            x = x + 1
        #/Auto Indent Code
        
        #Ensure proper keyboard navigation:
        self.CmdKeyExecute(STC_CMD_CHARLEFT)
        self.CmdKeyExecute(STC_CMD_CHARRIGHT)
        
        