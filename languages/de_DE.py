class General:
    autostartItem = 'Autostart'
    browse = 'Suchen...'
    cancel = 'Abbrechen'
    choose = 'Ausw\xe4hlen'
    configTree = 'Konfigurations-Baum'
    deleteLinkedItems = u'Wenigstens ein Element au\xdferhalb der momentanen Selektion verweist auf ein Element innerhalb der zu l\xf6schenden Selektion. Wenn sie diese Selektion l\xf6schen, wird das verweisende Element nicht mehr richtig funktionieren.\n\nSind sie sicher, dass sie die Selektion l\xf6schen wollen?'
    deleteManyQuestion = 'Dieses Element hat %s Unterelemente.\n\nSollen wirklich alle gel\xf6scht werden?'
    deletePlugin = 'Dieses Plugin wird von Befehlen in ihrer aktuellen Konfiguration benutzt.\n\nSie k\xf6nnen es erst entfernen, wenn alle Befehle die dieses Plugin benutzen\nvorher ebenfalls entfernt wurden.'
    deleteQuestion = u'Soll dieses Element wirklich gel\xf6scht werden?'
    help = '&Hilfe'
    moreHelp = u'Weitere Hilfe'
    noOptionsAction = u'Diese Aktion hat keine einstellbaren Optionen.'
    noOptionsPlugin = u'Dieses Plugin hat keine einstellbaren Optionen.'
    ok = 'Ok'
    pluginLabel = 'Plugin: %s'
    unnamedEvent = '<Unbenanntes Ereignis>'
    unnamedFile = '<Unbenannte Datei>'
    unnamedFolder = '<Unbenannter Ordner>'
    unnamedMacro = '<Unbenanntes Makro>'
class MainFrame:
    onlyLogAssigned = u'Nur &zugewiesene und aktivierte Ereignisse aufzeichnen'
    class Logger:
        caption = u'Log'
        descriptionHeader = 'Beschreibung'
        timeHeader = 'Zeit'
        welcomeText = '---> Willkommen beim EventGhost <---'
    class Menu:
        About = '&\xdcber EventGhost...'
        AddPlugin = u'&Plugin hinzuf\xfcgen'
        Apply = u'\xc4nderungen &anwenden'
        CheckUpdate = 'Auf neuere Version pr\xfcfen...'
        ClearAll = 'Alles l\xf6schen'
        Close = 'S&chlie\xdfen'
        CollapseAll = 'Alle einklappen'
        ConfigurationMenu = u'&Konfiguration'
        Copy = '&Kopieren'
        Cut = '&Ausschneiden'
        Delete = '&L\xf6schen'
        Disabled = u'Element &deaktivieren'
        Edit = u'Element &konfigurieren'
        EditMenu = '&Bearbeiten'
        Execute = u'Element &ausf\xfchren'
        Exit = '&Beenden'
        ExpandAll = 'Alle ausklappen'
        ExpandOnEvents = 'Autom. markieren bei Ereignis'
        ExpandTillMacro = 'Autom. nur bis Makro ausklappen'
        Export = 'Exportieren...'
        FileMenu = '&Datei'
        Find = u'S&uchen...'
        FindNext = u'&Weitersuchen'
        HelpMenu = '&Hilfe'
        HideShowToolbar = 'Symbolleiste'
        Import = 'Importieren...'
        LogActions = 'Auch Befehle aufzeichnen'
        LogTime = 'Auch Zeiten aufzeichnen'
        New = '&Neu'
        NewAction = u'&Befehl hinzuf\xfcgen'
        NewEvent = '&Ereignis hinzuf\xfcgen'
        NewFolder = '&Ordner hinzuf\xfcgen'
        NewMacro = '&Makro hinzuf\xfcgen'
        Open = '\xd6&ffnen...'
        Options = '&Einstellungen...'
        Paste = 'E&inf\xfcgen'
        Redo = '&Wiederholen'
        Rename = u'Element &umbenennen'
        Save = '&Speichern'
        SaveAs = 'Speichern &unter...'
        SelectAll = '&Alles markieren'
        Undo = '&R\xfcckg\xe4ngig'
        ViewMenu = u'&Ansicht'
        WebForum = u'Forum'
        WebHomepage = u'Homepage'
        WebWiki = u'Wiki'
    class SaveChanges:
        mesg = 'Die Datei wurde ver\xe4ndert.\n\nAktuelle \xc4nderungen speichern?\n'
        title = '\xc4nderungen speichern?'
    class TaskBarMenu:
        Exit = 'Beenden'
        Hide = 'EventGhost verstecken'
        Show = 'EventGhost wiederherstellen'
    class Tree:
        caption = u'Konfiguration'
class Error:
    FileNotFound = 'Datei "%s" konnte nicht gefunden werden.'
    InAction = 'Fehler in Befehl: "%s"'
    InScript = 'Fehler in Skript: "%s"'
    pluginNotActivated = u'Plugin "%s" ist nicht aktiviert'
    pluginStartError = u'Fehler beim Start des Plugins: %s'
class CheckUpdate:
    ManErrorMesg = 'Es konnte nicht festgestellt werden, ob es eine neuere Version von EventGhost gibt.\n\nBitte versuchen sie es sp\xe4ter noch einmal.'
    ManErrorTitle = 'Fehler bei der \xdcberpr\xfcfung'
    ManOkMesg = 'Es ist keine neuere Version von EventGhost verf\xfcgbar.'
    ManOkTitle = 'Keine neuere Version verf\xfcgbar'
    downloadButton = 'Download-Seite besuchen'
    newVersionMesg = 'Eine neuere Version von EventGhost wurde ver\xf6ffentlicht.\n\n\tDiese Version:\t\t%s\n\tAktuellste Version:\t%s\n\nWollen Sie die Download-Seite besuchen?'
    title = 'Neuere EventGhost-Version verf\xfcgbar...'
    waitMesg = 'Bitte warten sie w\xe4hrend EventGhost die Update-Informationen bezieht.'
class AddActionDialog:
    descriptionLabel = 'Beschreibung'
    title = 'Befehl ausw\xe4hlen...'
class AddPluginDialog:
    author = 'Autor:'
    descriptionBox = 'Beschreibung'
    externalPlugins = 'Steuerung externer Ger\xe4te'
    noInfo = 'Keine Information verf\xfcgbar.'
    noMultiload = 'Dieses Plugin unterst\xfctzt kein Mehrfachladen und\nSie haben schon eine Instanz dieses Plugins in ihrer Konfiguration.'
    noMultiloadTitle = 'Mehrfachladen nicht m\xf6glich'
    otherPlugins = 'Sonstige'
    programPlugins = 'Programmsteuerung'
    remotePlugins = 'Fernbedienungsempf\xe4nger'
    title = 'Plugin hinzuf\xfcgen...'
    version = 'Version:'
class OptionsDialog:
    CheckUpdate = 'Auf neuere Version pr\xfcfen beim Programmstart'
    HideOnClose = 'Minimiere wenn Schlie\xdfen-Schaltfl\xe4che gedr\xfcckt wird'
    HideOnStartup = 'Minimiert starten'
    LanguageGroup = 'Sprache'
    StartGroup = 'Beim Start'
    StartWithWindows = 'Automatisch mit Windows starten'
    Tab1 = 'Allgemein'
    Title = 'Einstellungen'
    UseAutoloadFile = 'Lade Datei beim Start:'
    Warning = u'\xc4nderung der Sprache werden erst nach einem Neustart der Applikation wirksam.'
    confirmDelete = u'Zeige Warnhinweis beim L\xf6schen von Elementen'
    limitMemory1 = u'Begrenze Speicherverbrauch wenn minimiert auf'
    limitMemory2 = u'MB'
class FindDialog:
    caseSensitive = u'Gro\xdf-/Kleins&chreibung beachten'
    direction = u'Suchrichtung'
    down = u'Nach &unten'
    findButton = u'&Weitersuchen'
    notFoundMesg = u'"%s" kann nicht gefunden werden.'
    searchLabel = u'&Suchen nach:'
    searchParameters = u'Auch &Parameter von Aktionen durchsuchen'
    title = u'Suchen'
    up = u'Nach &oben'
    wholeWordsOnly = u'Nu&r ganzes Wort suchen'
class AboutDialog:
    Author = 'Autor: %s'
    CreationDate = '%a, %d %b %Y %H:%M:%S'
    Title = '\xdcber EventGhost'
    Version = 'Version: %s (build %s)'
    tabAbout = u'\xdcber'
    tabLicense = u'Lizenzabkommen'
    tabSpecialThanks = u'Besonderer Dank'
    tabSystemInfo = u'System Information'
class Plugin:
    class EventGhost:
        name = u'EventGhost'
        description = u'Diese Aktionen betreffen haupts\xe4chlich die Kern-Funktionen von EventGhost.'
        class AutoRepeat:
            name = 'Automatische Wiederholung'
            description = u'Ein Makro, dem dieser Befehl hinzugef\xfcgt wurde, wird solange wiederholt, wie die ausl\xf6sende Taste gedr\xfcckt gehalten wird.'
            seconds = 'Sekunden'
            text1 = 'Beginne erste Wiederholung nach'
            text2 = 'mit einer Wiederholung alle'
            text3 = 'Beschleunige Wiederholungen innerhalb von'
            text4 = 'auf eine Wiederholung alle'
        class Comment:
            name = 'Beschreibung'
            description = 'Ein Befehl der nichts tut, aber zur Kommentierung der Konfiguration benutzt werden kann.'
        class DisableItem:
            name = 'Deaktiviere ein Element'
            description = 'Deaktiviere ein Element'
            label = 'Deaktiviere: %s'
            text1 = 'Bitte w\xe4hlen Sie das zu deaktivierende Element:'
        class EnableExclusive:
            name = 'Aktiviere exklusiv Ordner/Makro'
            description = 'Aktiviert einen Ordner oder ein Makro, wobei gleichzeitig alle anderen Ordner/Makros, die auf der gleichen Baumebene liegen, deaktiviert werden.'
            label = 'Aktiviere exklusiv: %s'
            text1 = 'Bitte w\xe4hlen Sie das exklusiv zu aktivierende Element:'
        class EnableItem:
            name = 'Aktiviere ein Element'
            description = 'Aktiviere ein Element'
            label = 'Aktiviere: %s'
            text1 = 'Bitte w\xe4hlen Sie das zu aktivierende Element:'
        class FlushEvents:
            name = u'Verwerfe alle ausstehenden Ereignisse'
            description = u'Diese Aktion verwirft alle Ereignisse die sich momentan in der Verarbeitungsschlange befinden.\n\nDieses ist n\xfctzlich, wenn ein Makro eine ziemlich lange Zeit zum Verarbeiten braucht und sich Ereignisse innherhalb dieser Zeit angesammelt haben, die nicht verarbeitet werden sollen.\n\n<p><b>Beispiel:</b> Sie haben ein lang andauerndes "Starte System" Makro, welches ca. 90 Sekunden braucht um z.B. einen Projektor anzuschalten und dann verschiedene Programme zu starten. Der Benutzer wird von dieser Ausf\xfchrung nichts sehen, bis endlich der Projektor ein Bild zeigt und daher u.U. aus Ungeduld die ausl\xf6sende Taste mehrfach dr\xfccken, was dazu f\xfchren w\xfcrde, dass diese lange Verarbeitung wieder und wieder gestartet wird. Um dieses zu verhindern, k\xf6nnen Sie die "Verwerfe alle ausstehenden Ereignisse" Aktion an das Ende Ihres Makros stellen, wodurch die \xfcberfl\xfcssigen Tastendruck-Wiederholungen entfernt werden.'
        class Jump:
            name = 'Unbedingter Sprung'
            description = 'Springt zu einem anderen Makro.'
            label1 = 'Springe zu %s'
            label2 = 'Springe zu %s und kehre zur\xfcck'
            mesg1 = 'W\xe4hle Makro...'
            mesg2 = 'Bitte w\xe4hlen sie das Makro, welches ausgef\xfchrt werden soll:'
            text2 = 'Gehe zu:'
            text3 = 'Kehre zur\xfcck nach Ausf\xfchrung'
        class JumpIf:
            name = 'Bedingter Sprung'
            description = 'Springt zu einem anderen Makro, wenn die angegebene Python-Bedingung den Wahrheitswert "True" ergibt.'
            label1 = 'Wenn %s springe zu %s'
            label2 = 'Wenn %s springe zu %s und kehre zur\xfcck'
            mesg1 = 'W\xe4hle Makro...'
            mesg2 = 'Bitte w\xe4hlen sie das Makro, welches ausgef\xfchrt werden soll, wenn die Python-Bedingung zutrifft.'
            text1 = 'Wenn:'
            text2 = 'Gehe zu:'
            text3 = 'Kehre zur\xfcck nach Ausf\xfchrung'
        class JumpIfLongPress:
            name = 'Wenn langer Tastendruck'
            description = 'Springt zu einem anderen Makro, wenn die ausl\xf6sende Taste l\xe4nger als die eingestellte Zeit gedr\xfcckt wird.'
            label = 'Wenn Tastendruck l\xe4nger als %s s, gehe zu: %s'
            text1 = 'Wenn die Taste l\xe4nger als'
            text2 = 'Sekunden gedr\xfcckt wird, springe zu dem'
            text3 = 'Makro:'
            text4 = 'Makro ausw\xe4hlen...'
            text5 = 'Bitte w\xe4hlen Sie das Makro, welches bei einem langen\nTastendruck angesprungen werden soll.'
        class NewJumpIf:
            name = 'Sprungbefehl'
            description = 'Springt zu einem anderen Makro, wenn die angegebene Bedingung zutrifft.'
            choices = [
                'letzter Befehl erfolgreich',
                'letzter Befehl nicht erfolgreich',
                'Immer',
            ]
            labels = [
                'Wenn erfolgreich springe zu "%s"',
                'Wenn erfolglos springe zu "%s"',
                'Springe zu "%s"',
                'Wenn erfolgreich springe zu "%s" und kehre zur\xfcck',
                'Wenn erfolglos springe zu "%s" und kehre zur\xfcck',
                'Springe zu "%s" und kehre zur\xfcck',
            ]
            mesg1 = 'W\xe4hle Makro...'
            mesg2 = 'Bitte w\xe4hlen sie das Makro, welches ausgef\xfchrt werden soll, wenn die Bedingung zutrifft.'
            text1 = 'Wenn:'
            text2 = 'Springe zu:'
            text3 = 'und kehre zur\xfcck nach der Ausf\xfchrung'
        class PythonCommand:
            name = 'Python Befehl'
            description = 'F\xfchrt das angegebene Parameter als einzeiligen Python-Befehl aus.'
            parameterDescription = u'Python Anweisung:'
        class PythonScript:
            name = 'Python Skript'
            description = '\xdcber diesen Befehl k\xf6nnen Python Skripte erzeugt werden, die alle M\xf6glichkeiten der Programmiersprache Python bieten.'
        class ShowOSD:
            name = 'Zeige OSD'
            description = u'Zeigt einen einfaches "On Screen Display"'
            alignment = 'Ausrichtung:'
            alignmentChoices = [
                'oben links',
                'oben rechts',
                'unten links',
                'unten rechts',
                'mittig',
            ]
            display = 'Zeige auf Monitor:'
            editText = 'Darzustellender Text:'
            label = 'Zeige OSD: %s'
            osdColour = 'OSD Farbe:'
            osdColourButton = 'Zeichensatz Farbe'
            osdFont = 'OSD Zeichensatz:'
            osdFontButton = 'Zeichensatz'
            outlineColour = 'Umrandungsfarbe'
            outlineFont = 'Umrandungsfarbe'
            wait1 = 'Blende OSD nach'
            wait2 = 'Sekunden automatisch aus. (0 = nicht ausblenden)'
            xOffset = 'Horizontaler Versatz X:'
            yOffset = 'Vertikaler Versatz Y:'
        class StopProcessing:
            name = 'Beende Bearbeitung dieses Ereignisses'
            description = u'Wird dieser Befehl ausgef\xfchrt, dann sucht EventGhost nicht mehr nach weiteren Makros, die zu dem aktuellen Ereignis passen w\xfcrden.'
        class TriggerEvent:
            name = 'Erzeuge Ereignis'
            description = 'Erzeugt ein neues Ereignis (optional nach einiger Zeit).'
            labelWithTime = 'Erzeuge Ereignis "%s" nach %.2f Sekunden'
            labelWithoutTime = 'Erzeuge Ereignis "%s"'
            text1 = 'Zu erzeugender Ereignis-Name:'
            text2 = 'Verz\xf6gere das Ereignis um:'
            text3 = 'Sekunden. (0 = erzeuge sofort)'
        class Wait:
            name = 'Warte'
            description = 'Unterbricht die Ausf\xfchrung des Makros f\xfcr eine angegebene Zeit, bevor der n\xe4chste Befehl ausgef\xfchrt wird.'
            label = 'Warte: %s s'
            seconds = 'Sekunden'
            wait = 'Warte'
    class System:
        name = u'System'
        forced = 'Erzwungen: %s'
        forcedCB = 'Erzwinge Schlie\xdfung aller Programme'
        class ChangeDisplaySettings:
            name = u'\xc4ndere Anzeige-Einstellungen'
        class ChangeMasterVolumeBy:
            name = 'Ver\xe4ndere Master-Lautst\xe4rke'
            text1 = 'Ver\xe4ndere Master-Lautst\xe4rke um'
            text2 = 'Prozent.'
        class Execute:
            name = 'Starte Anwendung'
            description = u'Startet eine ausf\xfchrbare Datei.'
            FilePath = 'Pfad zur ausf\xfchrbaren Datei:'
            Parameters = 'Aufruf-Parameter:'
            ProcessOptions = (
                'Echtzeit',
                'H\xf6her als normal',
                'Normal',
                'Niedriger als normal',
                'Niedrig',
            )
            ProcessOptionsDesc = 'Prozess Priorit\xe4t:'
            WaitCheckbox = u'Auf Beendigung des Programmes warten bevor fortgeschritten wird.'
            WindowOptions = (
                'Normal',
                'Minimiert',
                'Maximiert',
                'Versteckt',
            )
            WindowOptionsDesc = 'Fenster-Optionen:'
            WorkingDir = u'Startverzeichnis:'
            label = 'Starte Anwendung: %s'
        class Hibernate:
            name = 'Hibernate Modus'
        class LockWorkstation:
            name = 'Rechner sperren'
        class LogOff:
            name = 'Benutzer abmelden'
        class MonitorGroup:
            name = 'Bildschirm'
        class MonitorPowerOff:
            name = 'Bildschirm ausschalten'
        class MonitorPowerOn:
            name = 'Bildschirm reaktivieren'
        class MonitorStandby:
            name = 'Bildschirm standby'
        class MuteOff:
            name = 'Stummschaltung aus'
        class MuteOn:
            name = 'Stummschaltung an'
        class OpenDriveTray:
            name = '\xd6ffne/Schlie\xdfe Laufwerksschublade'
            description = 'Erm\xf6glicht es die Laufwerksschublade von CD und DVD-Laufwerken zu \xf6ffnen und zu schlie\xdfen.'
            driveLabel = 'Laufwerk:'
            labels = [
                '\xd6ffne/Schlie\xdfe Laufwerksschublade: %s',
                '\xd6ffne Laufwerksschublade: %s',
                'Schlie\xdfe Laufwerksschublade: %s',
            ]
            options = [
                'Laufwerksschublade wechselnd \xf6ffnen und schlie\xdfen',
                'Nur Laufwerksschublade \xf6ffnen',
                'Nur Laufwerksschublade schlie\xdfen',
            ]
            optionsLabel = 'W\xe4hle Aktion'
        class PlaySound:
            name = 'Audiodatei abspielen'
            fileMask = 'WAV-Dateien (*.WAV)|*.wav|Alle Dateien (*.*)|*.*'
            text1 = 'Pfad zur Audiodatei:'
            text2 = 'Warte auf Beendigung'
        class PowerDown:
            name = 'Rechner ausschalten'
        class PowerGroup:
            name = 'Energieoptionen'
        class Reboot:
            name = 'Rechner neu starten'
        class SetClipboard:
            name = 'Zeichenkette in die Zwischenablage kopieren'
            description = 'Kopiert eine als Parameter angegebene Zeichenkette in die System-Zwischenablage.'
            error = 'Kann Zwischenablage nicht \xf6ffnen'
        class SetMasterVolume:
            name = 'Setze Master-Lautst\xe4rke'
            text1 = 'Setze Master-Lautst\xe4rke auf'
            text2 = 'Prozent.'
        class SetWallpaper:
            name = 'Desktop-Hintergrund wechseln'
            choices = (
                'Zentriert',
                'Nebeneinander',
                'Gestreckt',
            )
            fileMask = 'Alle Bilddateien|*.jpg;*.bmp;*.gif|Alle Dateien (*.*)|*.*'
            text1 = 'Pfad zur Bilddatei:'
            text2 = 'Ausrichtung:'
        class SoundGroup:
            name = 'Audiokarte'
        class Standby:
            name = 'Rechner standby'
        class StartScreenSaver:
            name = 'Starte Bildschirmschoner'
        class ToggleMute:
            name = 'Stummschaltung umschalten'
    class Window:
        name = 'Fenster'
        class BringToFront:
            name = u'Fenster nach vorne bringen'
            description = u'Bringt ein Fenster vor alle anderen Fenster des Desktops.'
        class Close:
            name = u'Fenster schlie\xdfen'
            description = 'Schlie\xdft Anwendungs-Fenster'
        class FindWindow:
            name = 'Finde Fenster'
            description = u'Sucht ein Fenster, welches dann f\xfcr weitere Befehle der Fenster-Gruppe als Ziel definiert wird.'
            drag1 = 'Ziehe mich auf\nein Fenster.'
            drag2 = 'Nun bewege mich\nauf ein Fenster.'
            hide_box = 'Verstecke EventGhost beim Ziehen'
            invisible_box = 'Auch unsichtbare Objekte durchsuchen'
            label = 'Finde Fenster: %s'
            label2 = 'Finde vorderstes Fenster'
            matchNum1 = 'Nur den Treffer Nr.'
            matchNum2 = 'zur\xfcckgeben'
            onlyForground = 'Nur vorderstes Fenster suchen'
            options = (
                'Programm:',
                'Fenster Name:',
                'Fenster Klasse:',
                'Unter-Fenster Name:',
                'Unter-Fenster Klasse:',
            )
            refresh_btn = '&Aktualisieren'
            stopMacro = [
                'Stoppe Makro wenn Ziel nicht gefunden',
                'Stoppe Makro wenn Ziel gefunden',
                'Niemals Makro stoppen',
            ]
            testButton = 'Test'
            wait1 = 'Warte bis zu '
            wait2 = 'Sekunden auf das Erscheinen des Fensters.'
        class Maximize:
            name = u'Fenster maximieren'
            description = u'Maximiert Fenster'
        class Minimize:
            name = u'Fenster minimieren'
            description = u'Minimiert Fenster'
        class MoveTo:
            name = u'Fenster verschieben'
            description = u'Verschiebt Fenster'
            label = u'Fenster nach %s verschieben'
            text1 = 'Setze horizontale Position X:'
            text2 = 'Pixel'
            text3 = 'Setze vertikale Position Y:'
            text4 = 'Pixel'
        class Resize:
            name = u'Fenstergr\xf6\xdfe \xe4ndern'
            description = u'\xc4ndert die Gr\xf6\xdfe eines Fensters.'
            label = '\xc4ndere Fenstergr\xf6\xdfe auf %s, %s'
            text1 = 'Setze Breite auf'
            text2 = 'Pixel'
            text3 = 'Setze H\xf6he auf'
            text4 = 'Pixel'
        class Restore:
            name = u'Fenster wiederherstellen'
        class SendKeys:
            name = 'Emuliere Tastatureingabe'
            description = u'Diese Aktion emuliert Tastatureingaben, die zur Kontrolle von anderen Programmen verwendet werden k\xf6nnen. \n\n<p>Geben Sie einfach den zu tippenden Text in die Textbox ein. Um Sondertasten zu emulieren, muss ein Schl\xfcsselwort in geschweifte Klammern gesetzt werden.\n<p>\nFor example if you want to have a cursor-up-key you write <b>{Up}</b>. You \ncan combine multiple keywords with the plus sign to get key-combinations like \n<b>{Shift+Ctrl+F1}</b> or <b>{Ctrl+V}</b>. The keywords are not \ncase-sensitive, so you can write {SHIFT+ctrl+F1} as well if you like. \n<p>\nSome keys differentiate between the left or the right side of the keyboard \nand can then be prefixed with an "L" or "R", like the Windows-Key:<br>\n<b>{Win}</b> or <b>{LWin}</b> or <b>{RWin}</b>\n<p>\nAnd here is the list of the remaining keywords EventGhost understands:<br>\n<b>{Ctrl}</b> or <b>{Control}<br>\n{Shift}<br>\n{Alt}<br>\n{Return}</b> or <b>{Enter}<br>\n{Back}</b> or <b>{Backspace}<br>\n{Tab}</b> or <b>{Tabulator}<br>\n{Esc}</b> or <b>{Escape}<br>\n{Spc}</b> or <b>{Space}<br>\n{Up}<br>\n{Down}<br>\n{Left}<br>\n{Right}<br>\n{PgUp}</b> or <b>{PageUp}<br>\n{PgDown}</b> or <b>{PageDown}<br>\n{Home}<br>\n{End}<br>\n{Ins}</b> or <b>{Insert}<br>\n{Del}</b> or <b>{Delete}<br>\n{Pause}<br>{Capslock}<br>\n{Numlock}<br>\n{Scrolllock}<br>\n{F1}, {F2}, ... , {F24}<br>\n{Apps}</b> (This is the context-menu-key)<b><br>\n<br>\n</b>These will emulate keys from the numpad:<b><br>\n{Divide}<br>{Multiply}<br>\n{Subtract}<br>\n{Add}<br>\n{Decimal}<br>\n{Numpad0}, {Numpad1}, ... , {Numpad9}</b>\n'
            insertButton = u'&Einf\xfcgen'
            specialKeyTool = u'Sondertasten Werkzeug'
            textToType = u'Zu tippender Text:'
            useAlternativeMethod = u'Verwende alternative Methode zur Emulation von Tastatureingaben.'
            class Keys:
                backspace = u'R\xfccktaste'
                context = u'Kontextmen\xfc Taste'
                delete = u'Entfernen'
                down = u'Pfeiltaste nach unten'
                end = u'Ende'
                home = u'Pos1'
                insert = u'Einf\xfcgen'
                left = u'Pfeiltaste nach links'
                num0 = u'Ziffernblock 0'
                num1 = u'Ziffernblock 1'
                num2 = u'Ziffernblock 2'
                num3 = u'Ziffernblock 3'
                num4 = u'Ziffernblock 4'
                num5 = u'Ziffernblock 5'
                num6 = u'Ziffernblock 6'
                num7 = u'Ziffernblock 7'
                num8 = u'Ziffernblock 8'
                num9 = u'Ziffernblock 9'
                numAdd = u'Ziffernblock +'
                numDecimal = u'Ziffernblock Dezimaltrenner'
                numDivide = u'Ziffernblock /'
                numMultiply = u'Ziffernblock *'
                numSubtract = u'Ziffernblock -'
                pageDown = u'Bild runter'
                pageUp = u'Bild hoch'
                right = u'Pfeiltaste nach rechts'
                space = u'Leerschritt'
                up = u'Pfeiltaste nach oben'
                win = u'Windows Taste'
    class Mouse:
        name = 'Maus'
        class GoDirection:
            name = 'Starte Mausbewegung in eine Richtung'
            label = 'Starte Mausbewegung in Richtung %.2f\xb0'
            text1 = 'Starte Mausbewegung in Richtung'
            text2 = 'Grad.'
        class LeftButton:
            name = 'Linke Maustaste'
        class LeftDoubleClick:
            name = 'Linke Maustaste Doppelklick '
        class MouseWheel:
            name = u'Drehe Mausrad'
            description = u'Emuliert Drehungen des Mausrades'
            label = u'Drehe Mausrad um %d Rastungen'
            text1 = u'Drehe Mausrad um'
            text2 = u'Rastungen. (Negative Werte drehen nach unten)'
        class MoveAbsolute:
            name = 'Setze Maus-Position'
            label = 'Bewege Maus nach x:%s, y:%s'
            text1 = 'Setze horizontale Position X:'
            text2 = 'Pixel'
            text3 = 'Setze vertikale Position Y:'
            text4 = 'Pixel'
        class RightButton:
            name = 'Rechte Maustaste'
        class RightDoubleClick:
            name = 'Rechte Maustaste Doppelklick'
        class ToggleLeftButton:
            name = 'Linke Maustaste umschalten'
    class Joystick:
        name = u'Joystick'
        description = u'Dieses Plugin erlaubt es Joysticks und Gamepads als Ereignisquelle zu verwenden.'
    class Keyboard:
        name = u'Tastatur'
        description = u'Dieses Plugin generiert Ereignisse bei Tastendruck (Hotkey).'
    class NetworkReceiver:
        name = u'Netzwerk Ereignis Empf\xe4nger'
        description = u'Empf\xe4ngt Ereignisse von einem "Netzwerk Ereignis Sender" Plugin.'
        event_prefix = 'Ereignis Prefix:'
        password = 'Passwort:'
        port = 'Port:'
    class NetworkSender:
        name = u'Netzwerk Ereignis Sender'
        description = u'Sendet Ereignisse zu einem "Netzwerk Ereignis Empf\xe4nger" Plugin \xfcber das TCP/IP Protokoll.'
        password = u'Passwort:'
    class Serial:
        name = 'Serieller Anschluss'
        description = 'Allgemeine Kommunikation \xfcber einen seriellen Anschluss.'
        baudrate = 'Bits pro Sekunde:'
        bytesize = 'Datenbits:'
        flowcontrol = 'Flusssteuerung:'
        handshakes = [
            'Keine',
            'Xon / Xoff',
            'Hardware',
        ]
        parities = [
            'Keine',
            'Ungerade',
            'Gerade',
        ]
        parity = 'Parit\xe4t:'
        port = 'Port:'
        stopbits = 'Stopbits:'
        class Read:
            name = 'Lese'
            read_all = 'Lese soviele Zeichen wie momentan verf\xfcgbar sind.'
            read_some = 'Lese genau diese Anzahl an Zeichen:'
            read_time = 'und warte maximal diese Anzahl an Millisekunden auf sie:'
        class Write:
            name = 'Sende'
    class Speech:
        name = u'Sprachausgabe'
        description = u'Verwendet die Microsoft Speech API (SAPI) um Texte in Sprache zu wandeln.'
        class TextToSpeech:
            name = u'Text in Sprache'
            description = u'Verwendet die Microsoft Speech API (SAPI) um Texte in Sprache zu wandeln.'
            buttonInsertDate = u'Datum einf\xfcgen'
            buttonInsertTime = u'Zeit einf\xfcgen'
            buttonPlayback = u'Stimmenvorschau'
            errorCreate = u'Kann Sprachobjekt nicht herstellen'
            errorNoVoice = u'Die Stimme mit dem Namen %s ist nicht verf\xfcgbar'
            fast = u'Schnell'
            label = u'Spreche: %s'
            labelRate = u'Geschwindigkeit:'
            labelVoice = u'Stimme:'
            labelVolume = u'Lautst\xe4rke:'
            loud = u'Laut'
            normal = u'Normal'
            silent = u'Leise'
            slow = u'Langsam'
            textBoxLabel = u'Text'
            voiceProperties = u'Spracheigenschaften'
    class USB_UIRT:
        blinkRx = 'Blinke bei Empfang'
        blinkTx = 'Blinke beim Senden'
        irReception = 'IR Empfang'
        legacyCodes = 'Generiere UIRT2-kompatible Ereignisse'
        notFound = '<unbekannt>'
        redIndicator = 'Funktion der roten Anzeige-LED'
        uuFirmDate = 'Firmware Datum: '
        uuFirmVersion = 'Firmware Version: '
        uuInfo = 'USB-UIRT Information'
        uuProtocol = 'Protokoll Version: '
        class TransmitIR:
            name = 'Sende IR'
            description = u'Sendet eine IR-Code durch das USB-UIRT Ger\xe4t.'
            infinite = u'unendlich'
            irCode = 'IR-Code:'
            learnButton = 'Lerne IR-Code...'
            repeatCount = 'Wiederholungen:'
            testButton = 'Teste IR Aussendung'
            wait1 = 'Warte auf:'
            wait2 = 'ms IR Inaktivit\xe4t vor Aussendung'
            zone = 'Zone:'
            zoneChoices = (
                'Alle',
                'Anschlussbuchse R-Kontakt',
                'Anschlussbuchse L-Kontakt',
                'Interner Sender',
            )
            class LearnDialog:
                acceptBurstButton = 'Akzeptiere Signalfolge'
                forceRaw = 'Lernen im RAW-Modus erzwingen'
                frequency = 'Frequenz'
                helpText = '1. Lassen Sie die Fernbedienung aus einer \nEntfernung von ungef\xe4hr 15 cm (oder auch weniger)\nauf die Vorderseite des USB-UIRT zeigen.\n\n2. DR\xdcCKEN und HALTEN Sie die gew\xfcnschte Taste\nder Fernbedienung, bis das Lernen abgeschlossen ist.\n'
                progress = 'Lern-Fortschritt'
                signalQuality = 'Signal'
                title = 'Lerne IR-Code'
    class Webserver:
        name = 'Webserver'
        description = 'Ein kleiner Webserver, mit dem Ereignisse durch HTML-Webseiten generiert werden k\xf6nnen.'
        documentRoot = u'Datenverzeichnis:'
        eventPrefix = u'Ereignis Prefix:'
        port = u'TCP/IP Port:'
    class X10:
        name = 'X10 Fernbedienung'
        description = u'Plugin f\xfcr X10 kompatible Funkfernbedienungen.\n\nDies beinhaltet Fernbedienungen wie:<br>\n<ul>\n<li><a href="http://www.ati.com/products/remotewonder/index.html">ATI Remote Wonder</a></li>\n<li><a href="http://www.snapstream.com/">SnapStream Firefly</a></li>\n<li><a href="http://www.nvidia.com/object/feature_PC_remote.html">NVIDIA Personal Cinema Remote</a></li>\n<li><a href="http://www.marmitek.com/">Marmitek PC Control</a></li>\n<li><a href="http://www.pearl.de/product.jsp?pdid=PE4444&catid=1601&vid=916&curr=DEM">Pearl Q-Sonic Master Remote 6in1</a></li>\n<li>Medion RF Remote Control</li>\n</ul>\n'
        allButton = '&Alle'
        errorMesg = u'Kein X10 Empf\xe4nger gefunden!'
        idBox = u'Aktivierte IDs:'
        noneButton = '&Keine'
        remoteBox = u'Fernbedienungstyp:'
        usePrefix = u'Ereignis-Prefix:'
