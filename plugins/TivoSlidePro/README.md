Tivo Slide Pro - EventGhost Plugin
=========

About
-----
This is a plugin for [EventGhost] which overrides the default behavior of the Tivo Slide Pro remote, and lets you override just about every button on the remote. You __MUST__ have the USB drivers provided with EventGhost installed. If you are using Windows 7, 8, or 8.1 64-bit, then you must __disable digitally signed drivers__ BEFORE you can install the eventghost driver.

How to Install
-----
1. Download the zip and extract it to your computer
2. Copy the folder `TivoSlidePro` into `C:\Program Files (x86)\EventGhost\plugins` for 64-bit windows or `C:\Program Files\EventGhost\plugins` for 32-bit windows.
3. __If you have a 64-bit operating system, disbale driver signing enforcement.__ If not, continue to the next step.
    - How to: [Windows 7 x64]
    - How to: [Windows 8 x64]
    - How to: [Windows 8.1 x64]
4. Open EventGhost and add the `TivoSlidePro` plugin to your configuration. It should ask you about downloading and installing a new driver on your system.
    - If it fails, make sure you did step #3 correctly, and beforehand!
5. By default the plugin only sends events to EventGhost to handle. __If you would like the Keyboard to work__ like normal, you must scroll down and copy the `Keyboard Simulation XML` into your configuration!
6. You can modify the keyboard simulation xml any way you like if there are certain buttons you want to handle yourself.

EventGhost Events
------
- Every button on the keyboard except `Sym` and `Caps`
- Lowercase versus Uppercase versus Symbol of the keyboard buttons is all handled automatically and generates different events for each
- Every button on the top of the remote
- The numbers 0-9 on the slide out keyboard are labelled as `Tivo.SlidePro.Keyboard.0` -> `Tivo.SlidePro.Keyboard.9`, the numbers 0-9 on the top of the remote are `Tivo.SlidePro.Button.0` -> `Tivo.SlidePro.Button.9`
- Actions for sliding the keyboard open and close

Limitations
--------
- __You currently cannot use the slide out keyboard on the windows lock screen__
- `Sym` and `Caps` buttons cannot be handled/overriden. (Note: There is nothing that can be done about this, because the remote does not send a signal when you press these buttons, they merely affect what gets sent when you press a letter.)


Keyboard Simulation XML
-----
__Copy the following text and paste it at the root of your EventGhost configuration. A folder will be created that handles the keyboard keys and sends those keys back to Windows (Use the GUI, or copy relevant parts into your own xml)__
```
<?xml version="1.0" encoding="UTF-8" ?>
<EventGhost Version="1640">
    <Folder Name="Tivo Slide Pro Keyboard Simulation">
        <Macro Name="Letters - Lowercase">
            <Event Name="Tivo.SlidePro.Keyboard.a" />
            <Event Name="Tivo.SlidePro.Keyboard.b" />
            <Event Name="Tivo.SlidePro.Keyboard.c" />
            <Event Name="Tivo.SlidePro.Keyboard.d" />
            <Event Name="Tivo.SlidePro.Keyboard.e" />
            <Event Name="Tivo.SlidePro.Keyboard.f" />
            <Event Name="Tivo.SlidePro.Keyboard.g" />
            <Event Name="Tivo.SlidePro.Keyboard.h" />
            <Event Name="Tivo.SlidePro.Keyboard.i" />
            <Event Name="Tivo.SlidePro.Keyboard.j" />
            <Event Name="Tivo.SlidePro.Keyboard.k" />
            <Event Name="Tivo.SlidePro.Keyboard.l" />
            <Event Name="Tivo.SlidePro.Keyboard.m" />
            <Event Name="Tivo.SlidePro.Keyboard.n" />
            <Event Name="Tivo.SlidePro.Keyboard.o" />
            <Event Name="Tivo.SlidePro.Keyboard.p" />
            <Event Name="Tivo.SlidePro.Keyboard.q" />
            <Event Name="Tivo.SlidePro.Keyboard.r" />
            <Event Name="Tivo.SlidePro.Keyboard.s" />
            <Event Name="Tivo.SlidePro.Keyboard.t" />
            <Event Name="Tivo.SlidePro.Keyboard.u" />
            <Event Name="Tivo.SlidePro.Keyboard.v" />
            <Event Name="Tivo.SlidePro.Keyboard.w" />
            <Event Name="Tivo.SlidePro.Keyboard.x" />
            <Event Name="Tivo.SlidePro.Keyboard.y" />
            <Event Name="Tivo.SlidePro.Keyboard.z" />
            <Action>
                EventGhost.NewJumpIf(XmlIdLink(999333111), 2, False)
            </Action>
        </Macro>
        <Macro Name="Letters - Uppercase">
            <Event Name="Tivo.SlidePro.Keyboard.A" />
            <Event Name="Tivo.SlidePro.Keyboard.B" />
            <Event Name="Tivo.SlidePro.Keyboard.C" />
            <Event Name="Tivo.SlidePro.Keyboard.D" />
            <Event Name="Tivo.SlidePro.Keyboard.E" />
            <Event Name="Tivo.SlidePro.Keyboard.F" />
            <Event Name="Tivo.SlidePro.Keyboard.G" />
            <Event Name="Tivo.SlidePro.Keyboard.H" />
            <Event Name="Tivo.SlidePro.Keyboard.I" />
            <Event Name="Tivo.SlidePro.Keyboard.J" />
            <Event Name="Tivo.SlidePro.Keyboard.K" />
            <Event Name="Tivo.SlidePro.Keyboard.L" />
            <Event Name="Tivo.SlidePro.Keyboard.M" />
            <Event Name="Tivo.SlidePro.Keyboard.N" />
            <Event Name="Tivo.SlidePro.Keyboard.O" />
            <Event Name="Tivo.SlidePro.Keyboard.P" />
            <Event Name="Tivo.SlidePro.Keyboard.Q" />
            <Event Name="Tivo.SlidePro.Keyboard.R" />
            <Event Name="Tivo.SlidePro.Keyboard.S" />
            <Event Name="Tivo.SlidePro.Keyboard.T" />
            <Event Name="Tivo.SlidePro.Keyboard.U" />
            <Event Name="Tivo.SlidePro.Keyboard.V" />
            <Event Name="Tivo.SlidePro.Keyboard.W" />
            <Event Name="Tivo.SlidePro.Keyboard.X" />
            <Event Name="Tivo.SlidePro.Keyboard.Y" />
            <Event Name="Tivo.SlidePro.Keyboard.Z" />
            <Action>
                EventGhost.NewJumpIf(XmlIdLink(999333111), 2, False)
            </Action>
        </Macro>
        <Macro Name="Keyboard Numbers">
            <Event Name="Tivo.SlidePro.Keyboard.1" />
            <Event Name="Tivo.SlidePro.Keyboard.2" />
            <Event Name="Tivo.SlidePro.Keyboard.3" />
            <Event Name="Tivo.SlidePro.Keyboard.4" />
            <Event Name="Tivo.SlidePro.Keyboard.5" />
            <Event Name="Tivo.SlidePro.Keyboard.6" />
            <Event Name="Tivo.SlidePro.Keyboard.7" />
            <Event Name="Tivo.SlidePro.Keyboard.8" />
            <Event Name="Tivo.SlidePro.Keyboard.9" />
            <Event Name="Tivo.SlidePro.Keyboard.0" />
            <Action>
                EventGhost.NewJumpIf(XmlIdLink(999333111), 2, False)
            </Action>
        </Macro>
        <Macro Name="Numbers (Top of Remote)" Enabled="False">
            <Event Name="Tivo.SlidePro.Button.1" />
            <Event Name="Tivo.SlidePro.Button.2" />
            <Event Name="Tivo.SlidePro.Button.3" />
            <Event Name="Tivo.SlidePro.Button.4" />
            <Event Name="Tivo.SlidePro.Button.5" />
            <Event Name="Tivo.SlidePro.Button.6" />
            <Event Name="Tivo.SlidePro.Button.7" />
            <Event Name="Tivo.SlidePro.Button.8" />
            <Event Name="Tivo.SlidePro.Button.9" />
            <Event Name="Tivo.SlidePro.Button.0" />
            <Action>
                EventGhost.NewJumpIf(XmlIdLink(999333111), 2, False)
            </Action>
            <Action Name="Enable this section to make the numbers (0-9) on the top of the remote act like number keys on a keyboard">
                EventGhost.Comment()
            </Action>
        </Macro>
        <Macro Name="Symbols">
            <Event Name="Tivo.SlidePro.Keyboard.Ampersand" />
            <Event Name="Tivo.SlidePro.Keyboard.Quote" />
            <Event Name="Tivo.SlidePro.Keyboard.LessThan" />
            <Event Name="Tivo.SlidePro.Keyboard.GreaterThan" />
            <Event Name="Tivo.SlidePro.Keyboard.Apostrophe" />
            <Event Name="Tivo.SlidePro.Keyboard.Comma" />
            <Event Name="Tivo.SlidePro.Keyboard.Period" />
            <Event Name="Tivo.SlidePro.Keyboard.Asterik" />
            <Event Name="Tivo.SlidePro.Keyboard.ExclamationMark" />
            <Event Name="Tivo.SlidePro.Keyboard.AtSymbol" />
            <Event Name="Tivo.SlidePro.Keyboard.Pound" />
            <Event Name="Tivo.SlidePro.Keyboard.DollarSign" />
            <Event Name="Tivo.SlidePro.Keyboard.Percent" />
            <Event Name="Tivo.SlidePro.Keyboard.Caret" />
            <Event Name="Tivo.SlidePro.Keyboard.OpenParen" />
            <Event Name="Tivo.SlidePro.Keyboard.CloseParen" />
            <Event Name="Tivo.SlidePro.Keyboard.Tilde" />
            <Event Name="Tivo.SlidePro.Keyboard.Underscore" />
            <Event Name="Tivo.SlidePro.Keyboard.Plus" />
            <Event Name="Tivo.SlidePro.Keyboard.OpenCurlyBrace" />
            <Event Name="Tivo.SlidePro.Keyboard.CloseCurlyBrace" />
            <Event Name="Tivo.SlidePro.Keyboard.Backtick" />
            <Event Name="Tivo.SlidePro.Keyboard.Minus" />
            <Event Name="Tivo.SlidePro.Keyboard.Equals" />
            <Event Name="Tivo.SlidePro.Keyboard.OpenSquareBracket" />
            <Event Name="Tivo.SlidePro.Keyboard.CloseSquareBracket" />
            <Event Name="Tivo.SlidePro.Keyboard.Backslash" />
            <Event Name="Tivo.SlidePro.Keyboard.VerticalBar" />
            <Event Name="Tivo.SlidePro.Keyboard.Semicolon" />
            <Event Name="Tivo.SlidePro.Keyboard.Colon" />
            <Event Name="Tivo.SlidePro.Keyboard.QuestionMark" />
            <Event Name="Tivo.SlidePro.Keyboard.Slash" />
            <Action>
                EventGhost.NewJumpIf(XmlIdLink(999333111), 2, False)
            </Action>
        </Macro>
        <Macro Name="D-Pad">
            <Event Name="Tivo.SlidePro.Keyboard.Up" />
            <Event Name="Tivo.SlidePro.Keyboard.Down" />
            <Event Name="Tivo.SlidePro.Keyboard.Left" />
            <Event Name="Tivo.SlidePro.Keyboard.Right" />
            <Event Name="Tivo.SlidePro.Keyboard.Select" />
            <Action>
                EventGhost.NewJumpIf(XmlIdLink(999333111), 2, False)
            </Action>
        </Macro>
        <Macro Name="Misc">
            <Event Name="Tivo.SlidePro.Keyboard.Backspace" />
            <Event Name="Tivo.SlidePro.Keyboard.Space" />
            <Event Name="Tivo.SlidePro.Keyboard.Clear" Enabled="False" />
            <Event Name="Tivo.SlidePro.Keyboard.Enter" />
            <Action>
                EventGhost.NewJumpIf(XmlIdLink(999333111), 2, False)
            </Action>
        </Macro>
        <Macro Name="SimulateLastKeypress" id="999333111">
            <Action>
                Tivo.SimulateLastKeypress()
            </Action>
            <Action>
                EventGhost.AutoRepeat(0.80000000000000004, 0.01, 0.01, 999.0)
            </Action>
        </Macro>
    </Folder>
</EventGhost>
```

[EventGhost]: http://www.eventghost.org/
[Windows 7 x64]: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=5&cad=rja&uact=8&ved=0CF0QtwIwBA&url=http%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dk4RwaI4mn6Y&ei=nllVU4rSJIaxyATUnoLoAQ&usg=AFQjCNHn-Bw-KKDdkH5mrH8Sx2WItpDgYw&sig2=Ijsl6p5gQrffyb6NsSTPhg
[Windows 8 x64]: https://learn.sparkfun.com/tutorials/disabling-driver-signature-on-windows-8/disabling-signed-driver-enforcement-on-windows-8
[Windows 8.1 x64]: http://www.howtogeek.com/167723/how-to-disable-driver-signature-verification-on-64-bit-windows-8.1-so-that-you-can-install-unsigned-drivers/
 