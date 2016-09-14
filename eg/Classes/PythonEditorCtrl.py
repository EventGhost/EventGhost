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

import keyword
import re
import wx
from wx.stc import *  #pylint: disable-msg=W0614,W0401

# Local imports
import eg

FACES = {
    'times': 'Times New Roman',
    'mono': 'Courier New',
    'helv': 'Arial',
    'other': 'Comic Sans MS',
    'size': 10,
    'size2': 8,
}

class PythonEditorCtrl(StyledTextCtrl):
    def __init__(
        self,
        parent,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=0,
        value="",
    ):
        StyledTextCtrl.__init__(self, parent, -1, pos, size, style)
        self.SetCodePage(STC_CP_UTF8)
        StyleSetSpec = self.StyleSetSpec  #IGNORE:C0103

        self.CmdKeyAssign(ord('B'), STC_SCMOD_CTRL, STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), STC_SCMOD_CTRL, STC_CMD_ZOOMOUT)

        # Setup a margin to hold fold markers
        #self.SetFoldFlags(16)  # WHAT IS THIS VALUE?

        self.Bind(EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted
        # from Scintilla sample property files.

        # Global default styles for all languages
        StyleSetSpec(STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % FACES)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        StyleSetSpec(STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % FACES)
        StyleSetSpec(STC_STYLE_CONTROLCHAR, "face:%(other)s" % FACES)

        # Python styles
        # End of line where string is not closed
        StyleSetSpec(
            STC_P_STRINGEOL,
            "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % FACES
        )

        # register some images for use in the AutoComplete box.
        #self.RegisterImage(1, images.getSmilesBitmap())
        #self.RegisterImage(2, images.getFile1Bitmap())
        #self.RegisterImage(3, images.getCopy2Bitmap())

        self.SetLexer(STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        # Enable folding
        self.SetProperty("fold", "1")

        # Highlight tab/space mixing (shouldn't be any)
        self.SetProperty("tab.timmy.whinge.level", "1")

        # Set left and right margins
        self.SetMargins(2, 2)

        # Set up the numbers in the margin for margin #1
        self.SetMarginType(1, STC_MARGIN_NUMBER)
        # Reasonable value for, say, 4-5 digits using a mono font (40 pix)
        self.SetMarginWidth(1, 40)

        # Indentation and tab stuff
        self.SetIndentSize(value)
        self.SetIndentationGuides(True)   # Show indent guides
        self.SetBackSpaceUnIndents(True)  # Backspace unindents rather than
                                          # delete 1 space
        self.SetTabIndents(True)          # Tab key indents
        self.SetUseTabs(False)            # Use spaces rather than tabs, or
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
        MarkerDefine = self.MarkerDefine  #IGNORE:C0103
        MarkerDefine(
            STC_MARKNUM_FOLDEREND, STC_MARK_BOXPLUSCONNECTED, "white", "black"
        )
        MarkerDefine(
            STC_MARKNUM_FOLDEROPENMID,
            STC_MARK_BOXMINUSCONNECTED,
            "white",
            "black"
        )
        MarkerDefine(
            STC_MARKNUM_FOLDERMIDTAIL, STC_MARK_TCORNER, "white", "black"
        )
        MarkerDefine(
            STC_MARKNUM_FOLDERTAIL, STC_MARK_LCORNER, "white", "black"
        )
        MarkerDefine(
            STC_MARKNUM_FOLDERSUB, STC_MARK_VLINE, "white", "black"
        )
        MarkerDefine(
            STC_MARKNUM_FOLDER, STC_MARK_BOXPLUS, "white", "black"
        )
        MarkerDefine(
            STC_MARKNUM_FOLDEROPEN, STC_MARK_BOXMINUS, "white", "black"
        )

        # Global default style
        StyleSetSpec(
            STC_STYLE_DEFAULT,
            'fore:#000000,back:#FFFFFF,face:Courier New,size:9'
        )

        # Clear styles and revert to default.
        self.StyleClearAll()

        # Following style specs only indicate differences from default.
        # The rest remains unchanged.

        # Line numbers in margin
        StyleSetSpec(STC_STYLE_LINENUMBER, 'fore:#000000,back:#99A9C2')
        # Highlighted brace
        StyleSetSpec(STC_STYLE_BRACELIGHT, 'fore:#00009D,back:#FFFF00')
        # Unmatched brace
        StyleSetSpec(STC_STYLE_BRACEBAD, 'fore:#00009D,back:#FF0000')
        # Indentation guide
        StyleSetSpec(STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")

        # Python styles
        StyleSetSpec(STC_P_DEFAULT, 'fore:#000000')
        # Comments
        StyleSetSpec(STC_P_COMMENTLINE, 'fore:#008000')
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
        # to be an identifier if it doesn't match the above criteria
        StyleSetSpec(STC_P_IDENTIFIER, 'fore:#000000')

        # Caret color
        self.SetCaretForeground("BLUE")
        # Selection background
        self.SetSelBackground(1, '#66CCFF')

        self.SetSelBackground(
            True,
            wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        )
        self.SetSelForeground(
            True,
            wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        )
        self.UsePopUp(False)

        #Keyword Search/Context Sensitive Autoindent.
        self.rekeyword = re.compile(
            r"(\sreturn\b)|(\sbreak\b)|(\spass\b)|(\scontinue\b)|(\sraise\b)",
            re.MULTILINE
        )
        self.reslash = re.compile(r"\\\Z")
        self.renonwhitespace = re.compile('\S', re.M)

        # popup menu
        menu = wx.Menu()
        text = eg.text.MainFrame.Menu

        def AddMenuItem(ident, menuId):
            self.Bind(wx.EVT_MENU, getattr(self, "OnCmd" + ident), id=menuId)
            return menu.Append(menuId, getattr(text, ident, ident))

        AddMenuItem("Undo", wx.ID_UNDO)
        AddMenuItem("Redo", wx.ID_REDO)
        menu.AppendSeparator()
        AddMenuItem("Cut", wx.ID_CUT)
        AddMenuItem("Copy", wx.ID_COPY)
        AddMenuItem("Paste", wx.ID_PASTE)
        AddMenuItem("Delete", wx.ID_DELETE)
        menu.AppendSeparator()
        AddMenuItem("SelectAll", wx.ID_SELECTALL)
        self.popupMenu = menu

        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

        self.SetText(value)
        self.EmptyUndoBuffer()
        self.Bind(EVT_STC_SAVEPOINTLEFT, self.OnSavePointLeft)

    def AutoIndent(self):
        indentSize = self.SetIndentSize(self.GetValue())

        pos = self.GetCurrentPos()

        #Strip trailing whitespace first.
        currentline = self.LineFromPosition(pos)
        lineendpos = self.GetLineEndPosition(currentline)
        if lineendpos > pos:
            self.SetTargetStart(pos)
            self.SetTargetEnd(lineendpos)
            textRange = self.GetTextRange(pos, lineendpos)
            self.ReplaceTarget(textRange.rstrip())

        #Look at last line
        pos = pos - 1
        clinenumber = self.LineFromPosition(pos)

        linenumber = clinenumber

        self.GotoPos(pos)

        self.GotoLine(clinenumber)

        numtabs = self.GetLineIndentation(clinenumber + 1) / indentSize

        search = self.renonwhitespace.search
        if (
            search(self.GetLine(clinenumber + 1)) is not None and
            search(self.GetLine(clinenumber)) is None
        ):
            numtabs += self.GetLineIndentation(clinenumber) / indentSize

        if numtabs == 0:
            numtabs = self.GetLineIndentation(linenumber) / indentSize

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

        self.SetTargetStart(pos + 1)
        end = self.GetLineEndPosition(clinenumber + 1)
        self.SetTargetEnd(end)

        self.ReplaceTarget(self.GetTextRange(pos + 1, end).lstrip())

        pos = pos + 1
        self.GotoPos(pos)
        x = 0
        while (x < numtabs):
            self.AddText(' ' * indentSize)
            x = x + 1
        #/Auto Indent Code

        #Ensure proper keyboard navigation:
        self.CmdKeyExecute(STC_CMD_CHARLEFT)
        self.CmdKeyExecute(STC_CMD_CHARRIGHT)

    def Delete(self):
        self.CmdKeyExecute(STC_CMD_CLEAR)

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
                    self.SetFoldExpanded(line, visLevels > 1)
                    line = self.Expand(line, doExpand, force, visLevels - 1)
                else:
                    flag = doExpand and self.GetFoldExpanded(line)
                    line = self.Expand(line, flag, force, visLevels - 1)
            else:
                line = line + 1

        return line

    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in xrange(lineCount):
            if self.GetFoldLevel(lineNum) & STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if (
                level & STC_FOLDLEVELHEADERFLAG and
                (level & STC_FOLDLEVELNUMBERMASK) == STC_FOLDLEVELBASE
            ):
                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum + 1, lastChild)

            lineNum = lineNum + 1

    def GetValue(self):
        return self.GetText()

    def OnCmdCopy(self, dummyEvent=None):
        self.Copy()

    def OnCmdCut(self, dummyEvent=None):
        self.Cut()

    def OnCmdDelete(self, dummyEvent=None):
        self.Delete()

    def OnCmdPaste(self, dummyEvent=None):
        self.Paste()

    def OnCmdRedo(self, dummyEvent=None):
        self.Redo()

    def OnCmdSelectAll(self, dummyEvent=None):
        self.SelectAll()

    def OnCmdUndo(self, dummyEvent=None):
        self.Undo()

    def OnKeyPressed(self, event):
        keycode = event.GetKeyCode()
        if (keycode == wx.WXK_RETURN) or (keycode == 372):
            self.CmdKeyExecute(STC_CMD_NEWLINE)
            self.AutoIndent()
        elif keycode == wx.WXK_TAB and event.GetModifiers() == wx.MOD_CONTROL:
            self.Navigate()
        else:
            event.Skip()

    def OnMarginClick(self, event):
        # fold and unfold as needed
        if event.GetMargin() == 2:
            if event.GetShift() and event.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(event.GetPosition())

                if self.GetFoldLevel(lineClicked) & STC_FOLDLEVELHEADERFLAG:
                    if event.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif event.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def OnModified(self, event):
        wx.PostEvent(self, eg.ValueChangedEvent(self.GetId()))
        event.Skip()

    def OnRightClick(self, dummyEvent):
        menu = self.popupMenu
        first, last = self.GetSelection()
        menu.Enable(wx.ID_UNDO, self.CanUndo())
        menu.Enable(wx.ID_REDO, self.CanUndo())
        menu.Enable(wx.ID_CUT, first != last)
        menu.Enable(wx.ID_COPY, first != last)
        menu.Enable(wx.ID_PASTE, self.CanPaste())
        menu.Enable(wx.ID_DELETE, first != last)
        menu.Enable(wx.ID_SELECTALL, True)
        self.PopupMenu(menu)

    def OnSavePointLeft(self, event):
        self.Bind(EVT_STC_MODIFIED, self.OnModified)
        wx.PostEvent(self, eg.ValueChangedEvent(self.GetId()))
        event.Skip()

    def OnUpdateUI(self, dummyEvent):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if (
            charBefore and
            chr(charBefore) in "[]{}()" and
            styleBefore == STC_P_OPERATOR
        ):
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
            if (
                charAfter and
                chr(charAfter) in "[]{}()" and
                styleAfter == STC_P_OPERATOR
            ):
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1 and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
            #pt = self.PointFromPosition(braceOpposite)
            #self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            #self.Refresh(False)

    def SetIndentSize(self, value):
        indentSize = 4
        if value:
            match = re.search("^( +)", value, re.MULTILINE)
            if match:
                indentSize = len(match.group())
        self.SetIndent(indentSize)
        self.SetTabWidth(indentSize)
        return indentSize

    def SetValue(self, value):
        self.SetText(value)
