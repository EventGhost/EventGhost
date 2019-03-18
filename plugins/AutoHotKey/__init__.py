import eg
import ahk

eg.RegisterPlugin(
    name="AutoHotKey",
    author="Krafty",
    version="1.0.0",
    kind="other",
    guid="{D6D3E0B8-40CB-4576-BB20-277F740C68C0}",
    description="""AutoHotKey Eventghost Plugin""",
)

def ahkExec(script):
    """Executes AutoHotKey Code"""
    script = replaceEgVars(script)
    ahk.start()
    ahk.ready()
    ahk.execute(str(script))

def replaceEgVars(script):
    """Replaces variables that start with eg with actual Eventghost variables"""
    if script.find("#eg.") != -1:
        words = script.split("#eg.")
        for w in range(1, len(words)):
            var = "eg." + words[w].split("#", 1)[0]
            try:
                # Replaces Eventghost Variable with it's actual value
                script = script.replace('#' + var + '#', str(eval(var)))
            except SyntaxError:
                eg.PrintError("AHK: Make sure all eg variables end with a '#'")
                break
            except ImportError:
                eg.PrintError("AHK: Variable '" + var + "' does not exist.")
    return script

class AutoHotKey(eg.PluginBase):

    def __init__(self):
        self.AddAction(ahkCommand)
        self.AddAction(ahkScript)
        self.AddAction(ahkFile)
        self.AddAction(ahkMsgBox)
        self.AddAction(ahksysBeep)
        self.AddAction(ahkBlockInput)
        self.AddAction(ahkBlockInputOff)
        self.AddAction(ahkImageSearch)
        self.AddAction(ahkInputBox)

    def __start__(self):
        pass
    def __stop__(self):
        pass
    def __close__(self):
        pass

class ahkCommand(eg.ActionWithStringParameter):
    """Executes user-entered AHK Command"""
    name = "AutoHotKey Command"
    description = "Execute AutoHotKey Command"
    class text:
        parameterDescription = "AutoHotKey Command:"

    def __call__(self, command):
        ahkExec(command)

class ahkScript(eg.ActionBase):
    """Executes user-entered AHK Script"""
    name = "AutoHotKey Script"
    description = "Execute AutoHotKey Script"

    def GetLabel(self, dummy=""):
        """Sets Label to name of Action when executed."""
        return self.name

    def __call__(self, sourceCode):
        ahkExec(sourceCode)

    def Configure(self, sourceCode=""):
        panel = eg.ConfigPanel(resizable=True)
        editCtrl = eg.PythonEditorCtrl(panel, value=sourceCode)
        panel.sizer.Add(editCtrl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                editCtrl.GetValue(),
            )

class ahkFile(eg.ActionBase):
    """Executes Selected AHK File"""
    name = "AutoHotKey File"
    description = "Execute AutoHotKey File"

    def __call__(self, filePath):
        with open(filePath, 'r') as f:
            ahkExec(f.read())

    def Configure(self, filePath=""):
        panel = eg.ConfigPanel()
        filepathCtrl = eg.FileBrowseButton(
            panel,
            size=(340, -1),
            initialValue=filePath,
            labelText="File",
            fileMask="AutoHotKey Files|*.ahk",
            )
        panel.sizer.Add(filepathCtrl)
        while panel.Affirmed():
            panel.SetResult(
                filepathCtrl.GetValue(),
            )

    def GetLabel(self, filePath):
        """Sets Label to name of Action when executed."""
        return self.name + ': "' + filePath + '"'

class ahkMsgBox(eg.ActionBase):
    """Creates a Message Box"""
    name = "AutoHotKey Message Box"
    description = "Create an AutoHotKey Message Box."

    def GetLabel(self, dummy=""):
        """Sets Label to name of Action when executed."""
        return "Message Box"

    def __call__(self, msgText, msgID, msgTitle, msgTO, bStyle, iStyle,
        selButton, onTop):
        opVal = bStyle + (iStyle * 16) + (selButton * 256)
        if onTop:
            opVal += 4096
        msgText = replaceEgVars(msgText)
        msgText = msgText.replace('\n', '`n')
        script = ahk.Script()
        script.message(text=msgText, title=msgTitle, options=opVal,
            timeout=msgTO)
        buttons = ["OK", "Cancel", "Yes", "No", "TryAgain", "Continue", "Abort",
        "Retry", "Ignore"]
        for b in buttons:
            if script.msgResult(name=b):
                if msgID == "":
                    eg.TriggerEvent(msgTitle + "." + b, prefix="AHK.MsgBox")
                else:
                    eg.TriggerEvent(msgID + "." + b, prefix="AHK.MsgBox")
                break

    def Configure(self, msgText="", msgID="", msgTitle="", msgTO=0, bStyle=0,
        iStyle=0, selButton=0, onTop=0):
        panel = eg.ConfigPanel()
        messageCtrl = panel.TextCtrl(msgText, size=(-1, 72), style=wx.TE_MULTILINE)
        msgIDCtrl = panel.TextCtrl(msgID)
        titleCtrl = panel.TextCtrl(msgTitle)
        timeoutCtrl = panel.SpinIntCtrl(msgTO, min=0, max=2147483)
        bStyles = ["OK", "OK/Cancel", "Abort/Retry/Ignore", "Yes/No/Cancel",
        "Yes/No", "Retry/Cancel", "Cancel/Try Again/Continue"]
        bStyleCtrl = panel.Choice(bStyle, bStyles)
        iStyles = ["", "Hand (stop/error)", "Question", "Exclamation",
        "Asterisk (info)"]
        iStyleCtrl = panel.Choice(iStyle, iStyles)
        selButtonCtrl = panel.Choice(selButton, ["1st", "2nd", "3rd"])
        onTopCtrl = panel.CheckBox(onTop, "Always on Top")

        panel.sizer.Add(panel.StaticText("Message:"))
        panel.sizer.Add(messageCtrl, 1, wx.EXPAND)
        panel.sizer.AddMany([
            panel.StaticText("\nMessage ID:"), msgIDCtrl,
            panel.StaticText("\nTitle:"), titleCtrl,
            panel.StaticText("\nTimeout(Seconds):"), timeoutCtrl,
            panel.StaticText("Leave 0 for no timeout."),
            panel.StaticText("\nButton Style:"), bStyleCtrl,
            panel.StaticText("\nIcon Style:"), iStyleCtrl,
            panel.StaticText("\nDefault Selected Button:"), selButtonCtrl,
            panel.StaticText(""), onTopCtrl,
        ])

        while panel.Affirmed():
            panel.SetResult(
                messageCtrl.GetValue(), msgIDCtrl.GetValue(),
                titleCtrl.GetValue(), timeoutCtrl.GetValue(),
                bStyleCtrl.GetValue(), iStyleCtrl.GetValue(),
                selButtonCtrl.GetValue(), onTopCtrl.GetValue(),
            )

class ahksysBeep(eg.ActionBase):
    """Emits a tone from the PC speaker through AutoHotKey"""
    name = "AutoHotKey SoundBeep"
    description = "Emits a tone from the PC speaker through AutoHotKey"

    def __call__(self, freq, dur):
        ahkExec("SoundBeep, " + str(freq) + ", " + str(dur))

    def Configure(self, freq=523, dur=150):
        panel = eg.ConfigPanel()
        freqCtrl = panel.SpinIntCtrl(freq, min=0, max=32767)
        durCtrl = panel.SpinIntCtrl(dur, min=0, max=60000)
        panel.sizer.AddMany([
            panel.StaticText("Frequency:"), freqCtrl,
            panel.StaticText("\nDuration:"), durCtrl,
        ])

        while panel.Affirmed():
            panel.SetResult(freqCtrl.GetValue(), durCtrl.GetValue())

    def GetLabel(self, freq, dur):
        """Sets Label to name of Action when executed."""
        return "SoundBeep " + freq + " " + dur

class ahkBlockInput(eg.ActionBase):
    """Blocks User Input until BlockInput Off Action is called or timeout."""
    name = "AutoHotKey Block Input"
    description = """Blocks User Input until BlockInput Off Action is called or
    timeout. Eventghost must be running as administrator."""

    def __call__(self, timeout):
        ahkExec("BlockInput, On")
        if timeout != 0:
            from threading import Timer
            t = Timer(timeout, ahkExec, ["BlockInput, Off"])
            t.start()

    def Configure(self, timeout=0):
        panel = eg.ConfigPanel()
        timeoutCtrl = panel.SpinIntCtrl(timeout, min=0, max=3600)
        panel.sizer.AddMany([
            panel.StaticText("Timeout(seconds):"), timeoutCtrl,
            panel.StaticText("Leave 0 for no Timeout"),
        ])

        while panel.Affirmed():
            panel.SetResult(timeoutCtrl.GetValue())

    def GetLabel(self):
        """Sets Label to name of Action when executed."""
        return self.name

class ahkBlockInputOff(eg.ActionBase):
    """Turns of BlockInput Off"""
    name = "BlockInput Off"
    description = "Turns off BlockInput"

    def __call__(self):
        ahkExec("BlockInput, Off")

    def GetLabel(self):
        """Sets Label to name of Action when executed."""
        return self.name

class ahkImageSearch(eg.ActionBase):
    """Allows user to search for image on the screen and click
    where it was found."""
    name = "AutoHotKey Click Image"
    description = """Find an image on the screen or active window and
    click it and/or trigger an event."""

    def __call__(self, imagePath, evtID, cType, evtF, evtNF):
        script = "\nSysGet, VirtualWidth, 78\nSysGet, VirtualWidth, 79"
        script += "\nImageSearch, imageX, imageY, 0, 0"
        script += ", %A_ScreenWidth%, %A_ScreenHeight%, " + imagePath
        if cType != 0:
            script += "\nif ErrorLevel = 0"
            if cType == 1:
                script += "\n    Click %imageX%, %imageY%, left"
            if cType == 2:
                script += "\n    Click %imageX%, %imageY%, 2"
            if cType == 3:
                script += "\n    Click %imageX%, %imageY%, right"

        script = replaceEgVars(script)
        ImgScript = ahk.Script()
        ImgScript.variable("imageX", int)
        ImgScript.variable("imageY", int)
        ahk.execute(str(script))
        errorLevel = ImgScript.ErrorLevel
        if evtID:
            evtID += "."
        if errorLevel == 0 and evtF == True:
            eg.TriggerEvent(evtID + "ImageFound", prefix="AHK.ImageSearch",
                payload=[ImgScript.imageX, ImgScript.imageY])
        if errorLevel == 1 and evtNF == True:
            eg.TriggerEvent(evtID + "ImageNotFound", prefix="AHK.ImageSearch")
        if errorLevel == 2:
            eg.PrintError("There was an error. Try another image format.")

    def Configure(self, imagePath="", evtID="", cType=0, evtF=False, evtNF=False):
        panel = eg.ConfigPanel()
        imagePathCtrl = eg.FileBrowseButton(
            panel,
            size=(340, -1),
            initialValue=imagePath,
            labelText="Image",
            fileMask="Image|*.gif;*.jpg;*.jpeg;*.bmp;*.png;*.ico;*.cur;*.ani",
            )
        evtIDCtrl = panel.TextCtrl(evtID)
        clickTypes = ["No Click", "Single-Click", "Double-Click", "Right-Click"]
        clickCtrl = panel.Choice(cType, clickTypes)
        foundEvtCtrl = panel.CheckBox(evtF, "Trigger Event if Image Found")
        noFoundEvtCtrl = panel.CheckBox(evtNF,
            "Trigger Event if Image Not Found")

        panel.sizer.AddMany([
            panel.StaticText("Image:"), imagePathCtrl,
            panel.StaticText("ID(for event triggers):"), evtIDCtrl,
            panel.StaticText("Click Type:"), clickCtrl,
            foundEvtCtrl, noFoundEvtCtrl,
        ])

        while panel.Affirmed():
            panel.SetResult(
                imagePathCtrl.GetValue(), evtIDCtrl.GetValue(),
                clickCtrl.GetValue(), foundEvtCtrl.GetValue(),
                noFoundEvtCtrl.GetValue(),
            )

    def GetLabel(self):
        """Sets Label to name of Action when executed."""
        return self.name

class ahkInputBox(eg.ActionBase):
    """Displays an input box where the user can enter a value and store
    to a variable."""
    name = "AutoHotKey Input Box"
    description = """Displays an input box and stores the entered value to
    an eg variable."""

    def __call__(self, outVar, title, prompt, password, width, height, xPos, yPos):
        script = "\nInputBox"

        if outVar != "eg." or outVar != "":
            script += ", output"
        else:
            eg.PrintError("No Output Variable Provided")
            return
        if title:
            script += ", " + title
        else:
            script += ", "
        if prompt:
            script += ", " + prompt
        else:
            script += ", "
        if password:
            script += ", hide"
        else:
            script += ", "
        script += ", " + width + ", " + height
        if xPos:
            script += ", " + xPos
        else:
            script += ", "
        if yPos:
            script += ", " + yPos
        else:
            script += ", "

        inputScript = ahk.Script()
        inputScript.variable("output", str)
        ahk.execute(str(script))

        print script
        print outVar + " = inputScript.output"
        try:
            if inputScript.ErrorLevel == 0:
                exec(outVar + " = inputScript.output")
            else:
                exec(outVar + " = ''")
        except:
            eg.PrintError("Problem with output variable.")

    def Configure(self, outVar="eg.", title="", prompt="", password=False,
        width="375", height="189", xPos="", yPos=""):
        panel = eg.ConfigPanel()
        outVarCtrl = panel.TextCtrl(outVar)
        titleCtrl = panel.TextCtrl(title)
        promptCtrl = panel.TextCtrl(prompt, size=(300, -1))
        passCtrl = panel.CheckBox(password, "Hide Characters")
        wCtrl = panel.TextCtrl(width)
        hCtrl = panel.TextCtrl(height)
        xCtrl = panel.TextCtrl(xPos)
        yCtrl = panel.TextCtrl(yPos)
        panel.sizer.AddMany([
            panel.StaticText("Output Variable:"), outVarCtrl,
            panel.StaticText("\nTitle:"), titleCtrl,
            panel.StaticText("\nPrompt:"), promptCtrl,
            panel.StaticText("\n"), passCtrl,
            panel.StaticText("\nWidth:"), wCtrl,
            panel.StaticText("\nHeight:"), hCtrl,
            panel.StaticText("\nX Position:"), xCtrl,
            panel.StaticText("\nY Position:"), yCtrl,
        ])

        while panel.Affirmed():
            panel.SetResult(
                outVarCtrl.GetValue(), titleCtrl.GetValue(),
                promptCtrl.GetValue(), passCtrl.GetValue(),
                wCtrl.GetValue(), hCtrl.GetValue(),
                xCtrl.GetValue(), yCtrl.GetValue(),
            )

    def GetLabel(self):
        """Sets Label to name of Action when executed."""
        return self.name
