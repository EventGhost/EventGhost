# -*- coding: utf-8 -*-

version="0.3.2"

#
# plugins/EG App Control/__init__.py
#
# Copyright (C) 2012 by Daniel Brugger
#
# Version history (newest on top):
# 0.3.2    Using new LogListener API from eg.Log class - many thanks to Pako
#          Modified defaults for new Log Monitors slightly / more user friendly.
# 0.3.1    Documentation improved - many thanks to user blaher
# 0.3.0    Action LogMonitor: 
#          - renamed action 'EventOnLogEntry' to 'LogMonitor'
#          - changed visible name to 'Log Monitor'
#          - added ability to parse and return a substring of the log message
#          - major refactoring of the Config dialog
#          - new approach for passing argument lists to __call__ and Configure
#          LogWrapper: 
#          - Fix: Log monitoring stopped when window was minimized
# 0.2.1    Action EventOnLogEntry: check warn messages as well 
# 0.2.0    Added action 'EventOnLogEntry': 
#            Fires an event when a monitored log entry occurs
#          Changed displayed plugin name: "EventGhost Application Control" -> "EG App Control"
# 0.1.1    Added action IsDirty
# 0.1.0    Initial version
#
# This file is part of EventGhost.
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

import eg

eg.RegisterPlugin(
    name="EG App Control",
    description=(
        "Provides actions to control the EventGhost application itself, like 'RestartProgram', 'Save' and others." 
    ),
    author="Daniel Brugger",
    version=version,
    kind="program",
    guid="{22A5D3F6-3628-4B57-8608-C4098A465BEC}", 
    createMacrosOnAdd = True,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=3881",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAAB3RJTUUH3AYPECIphy3u"
        "PgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAbZJREFUeNpVkMtqFFEQhutc+jbabWcmQWMC"
        "gYwjEcRZuBBR3IubeRbfwCdxqwtBF1kJPkEWKiRBGDCMjiSTzMW+nXP6XMpOxDipRdWi"
        "6qv/r2JwHg+BwAvy1I827jGTMBJfr9lKyzrCEZSC5WAXeb2pt+EVb8FLQqIec7GiXpih"
        "HyiipEXnABCvAJRv0sGz590nJim386LqkcK33HqLoJ0KG0UGswyvAGyDDB493urv3O94"
        "mJbrU/n7gRVsFRQXlLLcJUkNeW4vAdoAd3rtfpJwWOkEJLjp4jnM7zaOuqyMpIf+nK12"
        "yiUABtvdtB9GFITRUHsWoO38Kso2lVU7NA8KQDLi/64/N6iNgaKuYSoEzKQkgmiAxDU/"
        "kGvON1sUIeTLLyu1BlMhzKWA6aLCs6Gw6jAce8P2B1a03iI1x/8VGolc1VAKDafHJU72"
        "lXQH6Rfv1403WLOP2qgRmZ2WS5YQZpkAMTZu8ZVO6Ldbu15+7R0Q+hlDd6aPTjQUBSwr"
        "4ORQCjuM99k4fU8U3zUA3zVWOf4cOSjMxdxfgDTrHfnh9tZe81n8ySHu6VCeuHKi8Eg2"
        "PXd55x+Jm+ihAZkcYwAAAABJRU5ErkJggg=="
    )
)


from os.path import join, dirname, abspath, isfile
import codecs

# Utility method to read HTML help files
def GetFileAsStr(filename):
    try:
        filepath = abspath(join(dirname(__file__.decode('mbcs')), filename))
        f = codecs.open(filepath, mode="r", encoding="latin_1", buffering=-1)
        doc = f.read()
        f.close()
        return doc
    except Exception, exc:
        msg = "Error reading help file " + filepath + ", error=" + unicode(exc)
        eg.PrintTraceback(msg)
        return msg


import wx
import re

class EGAppControl(eg.PluginBase):
    
    @eg.LogIt
    def __init__(self):
        self.AddAction(RestartProgram)
        self.AddAction(ExitApplication)
        self.AddAction(SaveConfiguration)
        self.AddAction(IsConfigDirty)
        self.AddAction(HideWindow)
        self.AddAction(RestoreWindow)
        self.AddAction(IsDebug)
        self.AddAction(LogMonitor)
        
    def __start__(self):
        self.logWrapper = LogWrapper(self)
        
    def __stop__(self):
        self.logWrapper.StopAllLogListeners()
        
        
class RestartProgram(eg.ActionBase):
    name = "RestartProgram"
    description = "Restart EventGhost application"

    @eg.LogIt
    def __call__(self):
        wx.CallAfter(eg.app.Restart)


class ExitApplication(eg.ActionBase):
    name = "ExitApplication"
    description = "Terminate EventGhost application"

    @eg.LogIt
    def __call__(self):
        wx.CallAfter(eg.app.Exit)


class SaveConfiguration(eg.ActionBase):
    name = "SaveConfiguration"
    description = "Save the current configuration"

    @eg.LogIt
    def __call__(self):
        wx.CallAfter(eg.document.Save)


class IsConfigDirty(eg.ActionBase):
    name = "IsConfigDirty"
    description = "Returns 'True' if the current configuration has been modified an needs saving."
    
    @eg.LogIt
    def __call__(self):
        return eg.document.isDirty
    
    
class HideWindow(eg.ActionBase):
    name = "HideWindow"
    description = "Hide the main window"

    @eg.LogIt
    def __call__(self):
        wx.CallAfter(eg.document.HideFrame)


class RestoreWindow(eg.ActionBase):
    name = "RestoreWindow"
    description = "Restore the main window"

    @eg.LogIt
    def __call__(self):
        wx.CallAfter(eg.document.ShowFrame)


class IsDebug(eg.ActionBase):
    name = "IsDebug"
    description = "Returns 'True' if EventGhost is in Debug mode."

    @eg.LogIt
    def __call__(self):
        return eg.debugLevel > 0


# message types
MT_ERROR  = 0
MT_WARN   = 1
MT_INFO   = 2
MT_ACTION = 3
MT_MACRO  = 4
MT_EVENT  = 5

MT_LENGTH = 6

DFLT_WATCH_TYPES = [True, True, True, False, False, False]

mtIcons = MT_LENGTH * [ None ]
mtIcons[MT_ERROR]  = (eg.Icons.ERROR_ICON,   "Error")
mtIcons[MT_WARN]   = (eg.Icons.NOTICE_ICON,  "Warning")
mtIcons[MT_INFO]   = (eg.Icons.INFO_ICON,    "Information")
mtIcons[MT_ACTION] = (None,                  "Action") # Actions don't have a single Icon
mtIcons[MT_MACRO]  = (eg.Icons.MACRO_ICON,   "Macro")
mtIcons[MT_EVENT]  = (eg.Icons.EVENT_ICON,   "Event")

# search modes
SM_KEEP_FULL            = 0
SM_FIND_NUMBER          = 1
SM_GET_SUBSTR_BY_CHAR   = 2
SM_GET_SUBSTR_BY_POS    = 3
SM_APPLY_REGEX          = 4

    
class LogMonitor(eg.ActionBase):
    class Text:
        name = "Log Monitor"
        description = (
            "Monitors the screen log and fires an event, if a configured log message occurs."
            "\n\n"
        ) + GetFileAsStr("LogMonitor.html")
        
        startMonitoring = "Start monitoring"
        stopMonitoring = "Stop ALL log message monitors"
        
        monitorLogMsg = "Monitor log message"
        catchMessage = "Capture log message"
        caseSensitive = "Case sensitive"
        wholeMessage = "Whole line"
        msgType = "Monitor log messages of type"
        errorMsg = "Error"
        warnMsg = "Warning"
        infoMsg = "Information"
        actionMsg = "Action"
        macroMsg = "Macro"
        eventMsg = "Event"
        
        actionWhenFound = "Action when found"
        fireEvent = "Fire an event"
        eventName = "Event name"
        onlyOnce = "Fire only once (until next call of this action)"
        eventPayload = "Add parsed log message as payload (accessible through 'eg.event.payload')"
        setVariable = "Set parsed log message as a global variable"
        variableName = "Variable name: eg.globals."
        printToLog = "Print parsed log message to screen log (caution: infinite loops)"
        
        parseLog = "Parse the captured log message"
        keepFullMsg1 = "Don't parse, keep the full log message as is"
        keepFullMsg2 = "The full log message line is available as a result / payload."
        parseNumVal1 = "Parse numeric values"
        parseNumVal2 = "e.g. Extract numeric value 40 from \"HTTP.Volume[u'40']\"."
        multipleFindings = "Multiple findings will be returned as a list."
        grabBetweenChar1 = "Grab the text between characters"
        grabBetweenChar2 = "and"
        grabBetweenChar3 = "Text to be extracted is surrounded by the given characters"
        grabBetweenChar4 = "e.g. 'text' or \"text\" or [text] or <text> or (text) or even <[('text')]> ..."
        grabBetweenPos1 = "Grab the text between position"
        grabBetweenPos2 = "and"
        grabBetweenPos3 = "Extracts a substring of the log message from char position A (inclusive) to B (exclusive)."
        grabBetweenPos4 = "First char position = 0, last char position = -1."
        grabBetweenPos5 = "e.g. Log msg='Welcome to EventGhost', A=0, B=7, result='Welcome'"
        applyRegex1 = "Apply a regular expression"
        applyRegex2 = "You know what you're doing when you choose this option ;)"

    text = Text


    # super class for argument classes   
    class Args:
        
        # Converts a dictionary into an 'Args' class 
        def FromDict(self, d):
            d.pop('self')
            for n, v in d.iteritems():
                setattr(self, n, v)
        
        # Converts the attributes of an 'Args' class into a dictionary
        def ToDict(self):
            d = {}
            for n, v in self.__dict__.iteritems():
                d[n] = v
            return d


    # Class holding the arguments for searching the log message
    class SearchArgs(Args):
        # class constructor
        def __init__(self,
            searchMsg      = '',
            caseSensitive  = True,
            wholeMessage   = False,
            watchMsgTypes  = DFLT_WATCH_TYPES,
        ):
            # Assign constructor args to class attributes
            self.FromDict( locals() )

            
    # Class holding the arguments for parsing the log message
    class ParseArgs(Args):
        # class constructor
        def __init__(self,
            # These arguments will be converted into class attributes with default values
            searchMode         = SM_KEEP_FULL,
            searchChar1        = '',
            searchChar2        = '',
            searchPos1         = 0,
            searchPos2         = 0,
            searchRegex        = r'\d*\.\d+|\d+'
        ):
            # Assign constructor args to class attributes
            self.FromDict( locals() )

            
    # Class holding the arguments for the action to take when log message matched
    class ActionArgs(Args):
        # class constructor
        def __init__(self,
            # These arguments will be converted into class attributes with default values
            fireEvent      = True,
            eventName      = 'LogMessageFound',
            onlyOnce       = False,
            eventPayload   = False,
            setVariable    = False,
            variableName   = 'MyVariable',
            printToLog     = False
        ):
            # Assign constructor args to class attributes
            self.FromDict( locals() )
            
        
    @eg.LogIt
    def __call__(self, start=True, searchArgsD={}, parseArgsD={}, actionArgsD={} ) :
        
        self.searchArgs = self.SearchArgs( **searchArgsD )
        self.parseArgs = self.ParseArgs( **parseArgsD )
        self.actionArgs = self.ActionArgs( **actionArgsD )

        self.monStr = self.searchArgs.searchMsg if self.searchArgs.searchMsg != '' else None
        self.monEvt = self.actionArgs.eventName if self.actionArgs.eventName != '' else None
        self.fired = False

        if start:
            if self.monStr:
                if not self.searchArgs.caseSensitive:
                    self.monStr = self.monStr.lower()
                self.plugin.logWrapper.AddLogListener(self)
        else:
            self.plugin.logWrapper.StopAllLogListeners()


    def ParseMsg(self, line):
        payload = None
        
        try:
            eg.PrintDebugNotice( "ParseMsg self.parseArgs.searchMode", self.parseArgs.searchMode ) 
            if self.parseArgs.searchMode == SM_KEEP_FULL:
                payload = line
                       
            elif self.parseArgs.searchMode == SM_FIND_NUMBER:
                strings = re.findall(r"\d*\.\d+|\d*\,\d+|\d+", line)
                numbers = []
                for s in strings:
                    s = s.replace(',', '.')
                    if s.find('.') >= 0:
                        numbers.append(float(s))
                    else:
                        numbers.append(int(s))
                
                if len(numbers) == 0:
                    payload = None
                elif len(numbers) == 1:
                    payload = numbers[0]
                else:
                    payload = numbers

            elif self.parseArgs.searchMode == SM_GET_SUBSTR_BY_CHAR:
                strings = []
                sstr = line
                p1, p2 = 0, 0
                l1, l2 = len(self.parseArgs.searchChar1), len(self.parseArgs.searchChar2)
                c1, c2 = self.parseArgs.searchChar1, self.parseArgs.searchChar2
                while p1 >= 0 and p1 < len(sstr):
                    sstr = sstr[p1:]
                    eg.PrintDebugNotice( 'sstr', sstr )
                    p1 = sstr.find(c1)
                    if p1 >= 0:
                        p2 = sstr.find(c2)
                        eg.PrintDebugNotice( 'p1', p1, 'p2', p2 )
                        if p2 > p1:
                            strings.append(sstr[p1+l1:p2])
                            p1 = p2 + l2

                if len(strings) == 0:
                    payload = None
                elif len(strings) == 1:
                    payload = strings[0]
                else:
                    payload = strings

            elif self.parseArgs.searchMode == SM_GET_SUBSTR_BY_POS:
                payload = line[self.parseArgs.searchPos1:self.parseArgs.searchPos2]
            
            elif self.parseArgs.searchMode == SM_APPLY_REGEX:
                payload = re.findall(self.parseArgs.searchRegex, line)
                
        except Exception, exc:
            payload = None
            msg = "Error parsing log message <" + unicode(line) + ">, error=" + unicode(exc)
            
            eg.PrintTraceback(msg)

        return payload


    def ProcessMsg(self, line, icon):
        try:
            if self.fired and self.actionArgs.onlyOnce:
                return
            
            found, idx = False, -1
            for i in range(len(self.searchArgs.watchMsgTypes)):
                if icon == mtIcons[i][0]:
                    found = True
                    if self.searchArgs.watchMsgTypes[i]:
                        idx = i
                    break
    
            if (not found and not self.searchArgs.watchMsgTypes[MT_ACTION]
                or found and idx == -1
            ):
                return
            elif not found and self.searchArgs.watchMsgTypes[MT_ACTION]:
                idx = MT_ACTION
    
            l = line if self.searchArgs.caseSensitive else line.lower()
            if (self.searchArgs.wholeMessage and l == self.monStr
                or not self.searchArgs.wholeMessage and l.find(self.monStr) >= 0
            ):
                self.fired = True
                eg.PrintDebugNotice("LogMonitor: Analyzed line: " + line)
                eg.PrintDebugNotice("LogMonitor: Found search string '" + self.monStr 
                    + "' in current log message of type '" + mtIcons[idx][1] + "'")
                
                eg.PrintDebugNotice( "payload = self.ParseMsg(line)" )
                payload = self.ParseMsg(line)
                
                if self.actionArgs.fireEvent and self.monEvt:
                    eg.PrintDebugNotice("LogMonitor: => fire event '" + self.monEvt + "' with payload=", repr(payload))
                    p = payload if self.actionArgs.eventPayload else None
                    self.plugin.TriggerEvent(self.monEvt, payload=p)
                    
                if self.actionArgs.setVariable and self.actionArgs.variableName != '':
                    exec('eg.globals.' + self.actionArgs.variableName + '=' + repr(payload))
    
                if self.actionArgs.printToLog:
                    print payload
                    
        except Exception, exc:
            # don't print anything (infinite loops)
            pass


    @eg.LogIt
    def Configure(self, start=True, searchArgsD={}, parseArgsD={}, actionArgsD={} ) :

        class MonitorLogPanel ( wx.Panel ):
            def __init__(self, parent ):
                wx.Panel.__init__( self, parent )

                # --- components
                self.msgTextCtrl = wx.TextCtrl(self, size=(350, -1))
                self.msgTextCtrl.SetValue(searchArgs.searchMsg)
                guiComponents.append(self.msgTextCtrl)
                        
                self.caseSensCB = wx.CheckBox(self, -1, text.caseSensitive)
                self.caseSensCB.SetValue(searchArgs.caseSensitive)
                guiComponents.append(self.caseSensCB)
         
                self.wholeMsgCB = wx.CheckBox(self, -1, text.wholeMessage)
                self.wholeMsgCB.SetValue(searchArgs.wholeMessage)
                guiComponents.append(self.wholeMsgCB)
         
                self.errorTypeCB = wx.CheckBox(self, -1, text.errorMsg)
                self.errorTypeCB.SetValue(searchArgs.watchMsgTypes[MT_ERROR])
                guiComponents.append(self.errorTypeCB)
         
                self.warnTypeCB = wx.CheckBox(self, -1, text.warnMsg)
                self.warnTypeCB.SetValue(searchArgs.watchMsgTypes[MT_WARN])
                guiComponents.append(self.warnTypeCB)
         
                self.infoTypeCB = wx.CheckBox(self, -1, text.infoMsg)
                self.infoTypeCB.SetValue(searchArgs.watchMsgTypes[MT_INFO])
                guiComponents.append(self.infoTypeCB)
         
                self.actionTypeCB = wx.CheckBox(self, -1, text.actionMsg)
                self.actionTypeCB.SetValue(searchArgs.watchMsgTypes[MT_ACTION])
                guiComponents.append(self.actionTypeCB)
         
                self.macroTypeCB = wx.CheckBox(self, -1, text.macroMsg)
                self.macroTypeCB.SetValue(searchArgs.watchMsgTypes[MT_MACRO])
                guiComponents.append(self.macroTypeCB)
         
                self.eventTypeCB = wx.CheckBox(self, -1, text.eventMsg)
                self.eventTypeCB.SetValue(searchArgs.watchMsgTypes[MT_EVENT])
                guiComponents.append(self.eventTypeCB)
         
                # --- layout
                gridBagSizer = wx.GridBagSizer(hgap=5, vgap=3)
                rowcount = 0
                gridBagSizer.Add(wx.StaticText(self, -1, text.catchMessage), (rowcount, 0), flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(self.msgTextCtrl, (rowcount, 1), flag=wx.EXPAND)
                rowcount += 1
                
                gridBagSizer.Add(self.caseSensCB, (rowcount, 1), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add(self.wholeMsgCB, (rowcount, 1), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add(wx.Size(0, 10), (rowcount, 0))
                rowcount += 1
         
                gridBagSizer.Add(wx.StaticText(self, -1, text.msgType), (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add(self.errorTypeCB, (rowcount, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(self.actionTypeCB, (rowcount, 1), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add(self.warnTypeCB, (rowcount, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(self.macroTypeCB, (rowcount, 1), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add(self.infoTypeCB, (rowcount, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(self.eventTypeCB, (rowcount, 1), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                
                sBoxSizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, text.monitorLogMsg), wx.VERTICAL)
                sBoxSizer.Add(gridBagSizer, proportion=1, flag=wx.EXPAND)
 
                self.SetSizer( sBoxSizer )


        class ParseMsgPanel ( wx.Panel ):

            def onParseRBChange(self, event):
                parentEnabled = startRadioCtrl.GetValue()

                enabled = parentEnabled and self.grabBetweenCharRB.GetValue()
                self.searchChar1Ctl.Enable(enabled)
                self.searchChar2Ctl.Enable(enabled)

                enabled = parentEnabled and self.grabBetweenPosRB.GetValue()
                self.searchPos1Ctl.Enable(enabled)
                self.searchPos2Ctl.Enable(enabled)

                enabled = parentEnabled and self.applyRegexRB.GetValue()
                self.regexCtl.Enable(enabled)


            def __init__(self, parent):
                wx.Panel.__init__( self, parent )

                # --- components
                self.keepFullRB = wx.RadioButton( self, -1, text.keepFullMsg1, style = wx.RB_GROUP )
                self.keepFullRB.SetValue( parseArgs.searchMode == SM_KEEP_FULL )
                self.keepFullRB.Bind(wx.EVT_RADIOBUTTON, self.onParseRBChange)
                guiComponents.append(self.keepFullRB)
        
                self.parseNumValRB = wx.RadioButton( self, -1, text.parseNumVal1 )
                self.parseNumValRB.SetValue( parseArgs.searchMode == SM_FIND_NUMBER )
                self.parseNumValRB.Bind(wx.EVT_RADIOBUTTON, self.onParseRBChange)
                guiComponents.append(self.parseNumValRB)
        
                self.grabBetweenCharRB = wx.RadioButton( self, -1, text.grabBetweenChar1 )
                self.grabBetweenCharRB.SetValue( parseArgs.searchMode == SM_GET_SUBSTR_BY_CHAR )
                self.grabBetweenCharRB.Bind(wx.EVT_RADIOBUTTON, self.onParseRBChange)
                guiComponents.append(self.grabBetweenCharRB)
                
                self.searchChar1Ctl = wx.TextCtrl(self, size=(30, -1))
                self.searchChar1Ctl.SetValue(parseArgs.searchChar1)
                guiComponents.append(self.searchChar1Ctl)
                self.searchChar2Ctl = wx.TextCtrl(self, size=(30, -1))
                self.searchChar2Ctl.SetValue(parseArgs.searchChar2)
                guiComponents.append(self.searchChar2Ctl)
        
                self.grabBetweenPosRB = wx.RadioButton( self, -1, text.grabBetweenPos1 )
                self.grabBetweenPosRB.SetValue( parseArgs.searchMode == SM_GET_SUBSTR_BY_POS )
                self.grabBetweenPosRB.Bind(wx.EVT_RADIOBUTTON, self.onParseRBChange)
                guiComponents.append(self.grabBetweenPosRB)
                
                self.searchPos1Ctl = eg.SpinNumCtrl(self, value=parseArgs.searchPos1, min=-9999, max=9999, fractionWidth=0, integerWidth=4)
                guiComponents.append(self.searchPos1Ctl)
                self.searchPos2Ctl = eg.SpinNumCtrl(self, value=parseArgs.searchPos2, min=-9999, max=9999, fractionWidth=0, integerWidth=4)
                guiComponents.append(self.searchPos2Ctl)
        
                self.applyRegexRB = wx.RadioButton( self, -1, text.applyRegex1 )
                self.applyRegexRB.SetValue( parseArgs.searchMode == SM_APPLY_REGEX )
                self.applyRegexRB.Bind(wx.EVT_RADIOBUTTON, self.onParseRBChange)
                guiComponents.append(self.applyRegexRB)
                
                self.regexCtl = wx.TextCtrl(self, size=(200, -1))
                self.regexCtl.SetValue(parseArgs.searchRegex)
                guiComponents.append(self.regexCtl)

                # --- layout
                gridBagSizer = wx.GridBagSizer(hgap=5, vgap=3)
                rowcount = 0
                
                gridBagSizer.Add(self.keepFullRB, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add( wx.Size( 12, 0 ), ( rowcount, 0 ) )
                gridBagSizer.Add( wx.StaticText( self, -1, text.keepFullMsg2 ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 1 ) )
                rowcount += 1
                
                gridBagSizer.Add(self.parseNumValRB, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.parseNumVal2 ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.multipleFindings ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 1 ) )
                rowcount += 1
                
                innerFGSizer = wx.FlexGridSizer(rows=1, cols=9, hgap=5, vgap=5)
                innerFGSizer.Add(self.grabBetweenCharRB, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(self.searchChar1Ctl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(wx.StaticText(self, -1, text.grabBetweenChar2), flag=wx.ALIGN_CENTER_VERTICAL) 
                innerFGSizer.Add(self.searchChar2Ctl, flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.grabBetweenChar3 ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.grabBetweenChar4 ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.multipleFindings ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 1 ) )
                rowcount += 1
                
                innerFGSizer = wx.FlexGridSizer(rows=1, cols=9, hgap=5, vgap=5)
                innerFGSizer.Add(self.grabBetweenPosRB, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(self.searchPos1Ctl, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(wx.StaticText(self, -1, text.grabBetweenPos2), flag=wx.ALIGN_CENTER_VERTICAL) 
                innerFGSizer.Add(self.searchPos2Ctl, flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.grabBetweenPos3 ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.grabBetweenPos4 ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.grabBetweenPos5 ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 1 ) )
                rowcount += 1

                innerFGSizer = wx.FlexGridSizer(rows=1, cols=5, hgap=5, vgap=5)
                innerFGSizer.Add(self.applyRegexRB, flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(self.regexCtl, flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add( wx.StaticText( self, -1, text.applyRegex2 ), ( rowcount, 1 ), flag = wx.ALIGN_CENTER_VERTICAL ) 
                rowcount += 1
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 1 ) )
                rowcount += 1
        
                sBoxSizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, text.parseLog), wx.VERTICAL)
                sBoxSizer.Add(gridBagSizer, proportion=1, flag=wx.EXPAND)
 
                self.SetSizer( sBoxSizer )
                

        class ActionPanel ( wx.Panel ):
            def onCheckboxChange(self, event):
                parentEnabled = startRadioCtrl.GetValue()

                enabled = parentEnabled and self.fireEventCB.GetValue()
                self.evtTextCtrl.Enable(enabled)
                self.onlyOnceCB.Enable(enabled)
                self.eventPayloadCB.Enable(enabled)

                enabled = parentEnabled and self.setVariableCB.GetValue()
                self.varNameCtrl.Enable(enabled)


            def __init__(self, parent ):
                wx.Panel.__init__( self, parent )

                # --- components
                self.fireEventCB = wx.CheckBox(self, -1, text.fireEvent)
                self.fireEventCB.SetValue(actionArgs.fireEvent)
                self.fireEventCB.Bind(wx.EVT_CHECKBOX, self.onCheckboxChange)
                guiComponents.append(self.fireEventCB)
                
                self.evtTextCtrl = wx.TextCtrl(self, size=(200, -1))
                self.evtTextCtrl.SetValue(actionArgs.eventName)
                guiComponents.append(self.evtTextCtrl)
         
                self.onlyOnceCB = wx.CheckBox(self, -1, text.onlyOnce)
                self.onlyOnceCB.SetValue(actionArgs.onlyOnce)
                guiComponents.append(self.onlyOnceCB)
                
                self.eventPayloadCB = wx.CheckBox(self, -1, text.eventPayload)
                self.eventPayloadCB.SetValue(actionArgs.eventPayload)
                guiComponents.append(self.eventPayloadCB)
                
                self.setVariableCB = wx.CheckBox(self, -1, text.setVariable)
                self.setVariableCB.SetValue(actionArgs.setVariable)
                self.setVariableCB.Bind(wx.EVT_CHECKBOX, self.onCheckboxChange)
                guiComponents.append(self.setVariableCB)
                
                self.varNameCtrl = wx.TextCtrl(self, size=(200, -1))
                self.varNameCtrl.SetValue(actionArgs.variableName)
                guiComponents.append(self.varNameCtrl)
         
                self.printToLogCB = wx.CheckBox(self, -1, text.printToLog)
                self.printToLogCB.SetValue(actionArgs.printToLog)
                guiComponents.append(self.printToLogCB)
                
                # --- layout
                gridBagSizer = wx.GridBagSizer(hgap=5, vgap=3)
                rowcount = 0

                gridBagSizer.Add(self.fireEventCB, (rowcount, 0), span=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add( wx.Size( 12, 0 ), ( rowcount, 0 ) )
                gridBagSizer.Add(wx.StaticText(self, -1, text.eventName), (rowcount, 1), flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(self.evtTextCtrl, (rowcount, 2), flag=wx.EXPAND)
                rowcount += 1
                gridBagSizer.Add(self.onlyOnceCB, (rowcount, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add(self.eventPayloadCB, (rowcount, 2), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 1 ) )
                rowcount += 1
               
                gridBagSizer.Add(self.setVariableCB, (rowcount, 0), span=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                innerFGSizer = wx.FlexGridSizer(rows=1, cols=3, hgap=5, vgap=5)
                innerFGSizer.Add(wx.Size( 12, 0 ))
                innerFGSizer.Add(wx.StaticText(self, -1, text.variableName), flag=wx.ALIGN_CENTER_VERTICAL)
                innerFGSizer.Add(self.varNameCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
                gridBagSizer.Add(innerFGSizer, (rowcount, 0), span=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 1 ) )
                rowcount += 1

                gridBagSizer.Add(self.printToLogCB, (rowcount, 0), span=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL)
                rowcount += 1
                gridBagSizer.Add( wx.Size( 0, 5 ), ( rowcount, 1 ) )
                rowcount += 1

                sBoxSizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, text.actionWhenFound), wx.VERTICAL)
                sBoxSizer.Add(gridBagSizer, proportion=1, flag=wx.EXPAND)
 
                self.SetSizer( sBoxSizer )
                
        # -------------- Event handlers -------------------
        def onStartStopRBChange(event):
            enabled = startRadioCtrl.GetValue()
            for c in guiComponents:
                c.Enable(enabled)
            parseMsgPanel.onParseRBChange(event)
            actionPanel.onCheckboxChange(event)


        # --- Convert method arguments into custom objects
        searchArgs = self.SearchArgs( **searchArgsD )
        parseArgs = self.ParseArgs( **parseArgsD )
        actionArgs = self.ActionArgs( **actionArgsD )
        
        text = self.text
        panel = eg.ConfigPanel()
        guiComponents = []
        
        # -------------- GUI Components -------------------
        startRadioCtrl = wx.RadioButton( panel, -1, text.startMonitoring, style = wx.RB_GROUP )
        startRadioCtrl.SetValue( start )
        startRadioCtrl.Bind(wx.EVT_RADIOBUTTON, onStartStopRBChange)
 
        stopRadioCtrl = wx.RadioButton( panel, -1, text.stopMonitoring )
        stopRadioCtrl.SetValue( not start )
        stopRadioCtrl.Bind(wx.EVT_RADIOBUTTON, onStartStopRBChange)
 
        # --- main layout
        monitorLogPanel = MonitorLogPanel( panel )    
        parseMsgPanel = ParseMsgPanel( panel )
        actionPanel = ActionPanel( panel )
 
        mainGBSizer = wx.GridBagSizer(hgap=5, vgap=3)
        mainGBrow = 0
        mainGBSizer.Add(wx.Size(0, 5), (mainGBrow, 0))
        mainGBrow += 1

        mainGBSizer.Add(startRadioCtrl, (mainGBrow, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        mainGBSizer.Add(stopRadioCtrl, (mainGBrow, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        mainGBrow += 1
        mainGBSizer.Add(wx.Size(0, 5), (mainGBrow, 0))
        mainGBrow += 1
        
        mainGBSizer.Add(monitorLogPanel, (mainGBrow, 0), span=(1, 2), flag=wx.EXPAND)
        mainGBrow += 1
        mainGBSizer.Add(wx.Size(0, 5), (mainGBrow, 0))
        mainGBrow += 1
 
        mainGBSizer.Add(parseMsgPanel, (mainGBrow, 0), span=(1, 2), flag=wx.EXPAND)
        mainGBrow += 1
        mainGBSizer.Add(wx.Size(0, 5), (mainGBrow, 0))
        mainGBrow += 1
 
        mainGBSizer.Add(actionPanel, (mainGBrow, 0), span=(1, 2), flag=wx.EXPAND)
        mainGBrow += 1

        onStartStopRBChange(None)
        panel.sizer.Add(mainGBSizer, proportion=1, flag=wx.EXPAND)

        while panel.Affirmed():
            start = startRadioCtrl.GetValue()
            
            searchArgs.searchMsg        = monitorLogPanel.msgTextCtrl.GetValue().strip()
            searchArgs.caseSensitive    = monitorLogPanel.caseSensCB.GetValue()
            searchArgs.wholeMessage     = monitorLogPanel.wholeMsgCB.GetValue()
            
            searchArgs.watchMsgTypes[MT_ERROR]  = monitorLogPanel.errorTypeCB.GetValue()
            searchArgs.watchMsgTypes[MT_WARN]   = monitorLogPanel.warnTypeCB.GetValue()
            searchArgs.watchMsgTypes[MT_INFO]   = monitorLogPanel.infoTypeCB.GetValue()
            searchArgs.watchMsgTypes[MT_ACTION] = monitorLogPanel.actionTypeCB.GetValue()
            searchArgs.watchMsgTypes[MT_MACRO]  = monitorLogPanel.macroTypeCB.GetValue()
            searchArgs.watchMsgTypes[MT_EVENT]  = monitorLogPanel.eventTypeCB.GetValue()
            
            if searchArgs.searchMsg == '':
                start = False

            found = False
            for wmt in searchArgs.watchMsgTypes: 
                if wmt: found = True
            if not found: 
                start = False

            if parseMsgPanel.keepFullRB.GetValue():
                parseArgs.searchMode = SM_KEEP_FULL
            elif parseMsgPanel.parseNumValRB.GetValue():
                parseArgs.searchMode = SM_FIND_NUMBER
            elif parseMsgPanel.grabBetweenCharRB.GetValue():
                parseArgs.searchMode = SM_GET_SUBSTR_BY_CHAR
            elif parseMsgPanel.grabBetweenPosRB.GetValue():
                parseArgs.searchMode = SM_GET_SUBSTR_BY_POS
            elif parseMsgPanel.applyRegexRB.GetValue():
                parseArgs.searchMode = SM_APPLY_REGEX
            else:
                parseArgs.searchMode = SM_KEEP_FULL
            
            parseArgs.searchChar1   = parseMsgPanel.searchChar1Ctl.GetValue()
            parseArgs.searchChar2   = parseMsgPanel.searchChar2Ctl.GetValue()
            parseArgs.searchPos1    = parseMsgPanel.searchPos1Ctl.GetValue()
            parseArgs.searchPos2    = parseMsgPanel.searchPos2Ctl.GetValue()
            parseArgs.searchRegex   = parseMsgPanel.regexCtl.GetValue()
            
            if parseArgs.searchMode == SM_GET_SUBSTR_BY_CHAR:
                if parseArgs.searchChar1.strip() == '' or parseArgs.searchChar2.strip() == '':
                    parseArgs.searchMode = SM_KEEP_FULL
                    
            if parseArgs.searchMode == SM_APPLY_REGEX:
                if parseArgs.searchRegex.strip() == '':
                    parseArgs.searchMode = SM_KEEP_FULL

            actionArgs.fireEvent    = actionPanel.fireEventCB.GetValue()
            actionArgs.eventName    = actionPanel.evtTextCtrl.GetValue().replace(' ', '')
            actionArgs.onlyOnce     = actionPanel.onlyOnceCB.GetValue()
            actionArgs.eventPayload = actionPanel.eventPayloadCB.GetValue()
            actionArgs.setVariable  = actionPanel.setVariableCB.GetValue()
            actionArgs.variableName = actionPanel.varNameCtrl.GetValue().replace(' ', '')
            actionArgs.printToLog   = actionPanel.printToLogCB.GetValue()
            
            if actionArgs.eventName == '':
                actionArgs.fireEvent = False
            if actionArgs.variableName == '':
                actionArgs.setVariable = False

            panel.SetResult( start, searchArgs.ToDict(), parseArgs.ToDict(), actionArgs.ToDict() )


    def GetLabel(self, start, searchArgsD, *dummyArgs):
        label = ''
        if start:
            label = 'Start log monitoring'
            if searchArgsD:
                label += ': "' + searchArgsD['searchMsg'] + '"'
        else:
            label = 'Stop log monitoring'
        return label



class LogWrapper:
        
    def __init__(self, plugin):
        self.logListener = []
        
    @eg.LogIt
    def AddLogListener(self, listener):
        if len(self.logListener) == 0:
            eg.log.AddLogListener(self)
        if listener not in self.logListener:
            self.logListener.append(listener)

    def WriteLine(self, line, icon, wRef, when, indent):
        for listener in self.logListener:
            listener.ProcessMsg(line, icon)

    @eg.LogIt
    def StopAllLogListeners(self):
        if len(self.logListener) > 0:
            eg.log.RemoveLogListener(self)
            self.logListener = []
