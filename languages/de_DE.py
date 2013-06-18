# -*- coding: UTF-8 -*-
class General:
    autostartItem = u'Autostart'
    browse = u'Suchen...'
    cancel = u'Abbrechen'
    choose = u'Ausw\xe4hlen'
    configTree = u'Konfigurations-Baum'
    deleteLinkedItems = u'Wenigstens ein Element au\xdferhalb der momentanen Selektion verweist auf ein Element innerhalb der zu l\xf6schenden Selektion. Wenn sie diese Selektion l\xf6schen, wird das verweisende Element nicht mehr richtig funktionieren.\n\nSind sie sicher, dass sie die Selektion l\xf6schen wollen?'
    deleteManyQuestion = u'Dieses Element hat %s Unterelemente.\n\nSollen wirklich alle gel\xf6scht werden?'
    deletePlugin = u'Dieses Plugin wird von Befehlen in ihrer aktuellen Konfiguration benutzt.\n\nSie k\xf6nnen es erst entfernen, wenn alle Befehle die dieses Plugin benutzen\nvorher ebenfalls entfernt wurden.'
    deleteQuestion = u'Soll dieses Element wirklich gel\xf6scht werden?'
    help = u'&Hilfe'
    moreHelp = u'Weitere Hilfe'
    noOptionsAction = u'Diese Aktion hat keine einstellbaren Optionen.'
    noOptionsPlugin = u'Dieses Plugin hat keine einstellbaren Optionen.'
    ok = u'Ok'
    pluginLabel = u'Plugin: %s'
    unnamedEvent = u'<Unbenanntes Ereignis>'
    unnamedFile = u'<Unbenannte Datei>'
    unnamedFolder = u'<Unbenannter Ordner>'
    unnamedMacro = u'<Unbenanntes Makro>'
class MainFrame:
    onlyLogAssigned = u'Nur &zugewiesene und aktivierte Ereignisse aufzeichnen'
    class Logger:
        caption = u'Log'
        descriptionHeader = u'Beschreibung'
        timeHeader = u'Zeit'
        welcomeText = u'---> Willkommen beim EventGhost <---'
    class Menu:
        About = u'&\xdcber EventGhost...'
        AddPlugin = u'&Plugin hinzuf\xfcgen'
        Apply = u'\xc4nderungen &anwenden'
        CheckUpdate = u'Auf neuere Version pr\xfcfen...'
        ClearLog = u'Log l\xf6schen'
        Close = u'S&chlie\xdfen'
        CollapseAll = u'Alle einklappen'
        ConfigurationMenu = u'&Konfiguration'
        Copy = u'&Kopieren'
        Cut = u'&Ausschneiden'
        Delete = u'&L\xf6schen'
        Disabled = u'Element &deaktivieren'
        Edit = u'Element &konfigurieren'
        EditMenu = u'&Bearbeiten'
        Execute = u'Element &ausf\xfchren'
        Exit = u'&Beenden'
        ExpandAll = u'Alle ausklappen'
        ExpandOnEvents = u'Autom. markieren bei Ereignis'
        ExpandTillMacro = u'Autom. nur bis Makro ausklappen'
        Export = u'Exportieren...'
        FileMenu = u'&Datei'
        Find = u'S&uchen...'
        FindNext = u'&Weitersuchen'
        HelpMenu = u'&Hilfe'
        HideShowToolbar = u'Symbolleiste'
        Import = u'Importieren...'
        LogActions = u'Auch Befehle aufzeichnen'
        LogTime = u'Auch Zeiten aufzeichnen'
        New = u'&Neu'
        NewAction = u'&Befehl hinzuf\xfcgen'
        NewEvent = u'&Ereignis hinzuf\xfcgen'
        NewFolder = u'&Ordner hinzuf\xfcgen'
        NewMacro = u'&Makro hinzuf\xfcgen'
        Open = u'\xd6&ffnen...'
        Options = u'&Einstellungen...'
        Paste = u'E&inf\xfcgen'
        Redo = u'&Wiederholen'
        Rename = u'Element &umbenennen'
        Reset = u'\ufef7'
        Save = u'&Speichern'
        SaveAs = u'Speichern &unter...'
        SelectAll = u'&Alles markieren'
        Undo = u'&R\xfcckg\xe4ngig'
        ViewMenu = u'&Ansicht'
        WebForum = u'Forum'
        WebHomepage = u'Homepage'
        WebWiki = u'Wiki'
    class SaveChanges:
        mesg = u'Die Datei wurde ver\xe4ndert.\n\nAktuelle \xc4nderungen speichern?\n'
        title = u'\xc4nderungen speichern?'
    class TaskBarMenu:
        Exit = u'Beenden'
        Hide = u'EventGhost verstecken'
        Show = u'EventGhost wiederherstellen'
    class Tree:
        caption = u'Konfiguration'
class Error:
    FileNotFound = u'Datei "%s" konnte nicht gefunden werden.'
    InAction = u'Fehler in Befehl: "%s"'
    InScript = u'Fehler in Skript: "%s"'
    pluginNotActivated = u'Plugin "%s" ist nicht aktiviert'
    pluginStartError = u'Fehler beim Start des Plugins: %s'
class CheckUpdate:
    ManErrorMesg = u'Es konnte nicht festgestellt werden, ob es eine neuere Version von EventGhost gibt.\n\nBitte versuchen sie es sp\xe4ter noch einmal.'
    ManErrorTitle = u'Fehler bei der \xdcberpr\xfcfung'
    ManOkMesg = u'Es ist keine neuere Version von EventGhost verf\xfcgbar.'
    ManOkTitle = u'Keine neuere Version verf\xfcgbar'
    downloadButton = u'Download-Seite besuchen'
    newVersionMesg = u'Eine neuere Version von EventGhost wurde ver\xf6ffentlicht.\n\n\tDiese Version:\t\t%s\n\tAktuellste Version:\t%s\n\nWollen Sie die Download-Seite besuchen?'
    title = u'Neuere EventGhost-Version verf\xfcgbar...'
    waitMesg = u'Bitte warten sie w\xe4hrend EventGhost die Update-Informationen bezieht.'
class AddActionDialog:
    descriptionLabel = u'Beschreibung'
    title = u'Befehl ausw\xe4hlen...'
class AddPluginDialog:
    author = u'Autor:'
    descriptionBox = u'Beschreibung'
    externalPlugins = u'Steuerung externer Ger\xe4te'
    noInfo = u'Keine Information verf\xfcgbar.'
    noMultiload = u'Dieses Plugin unterst\xfctzt kein Mehrfachladen und\nSie haben schon eine Instanz dieses Plugins in ihrer Konfiguration.'
    noMultiloadTitle = u'Mehrfachladen nicht m\xf6glich'
    otherPlugins = u'Sonstige'
    programPlugins = u'Programmsteuerung'
    remotePlugins = u'Fernbedienungsempf\xe4nger'
    title = u'Plugin hinzuf\xfcgen...'
    version = u'Version:'
class OptionsDialog:
    CheckUpdate = u'Auf neuere Version pr\xfcfen beim Programmstart'
    HideOnClose = u'Minimiere wenn Schlie\xdfen-Schaltfl\xe4che gedr\xfcckt wird'
    HideOnStartup = u'Minimiert starten'
    LanguageGroup = u'Sprache'
    StartGroup = u'Beim Start'
    StartWithWindows = u'Automatisch mit Windows starten'
    Tab1 = u'Allgemein'
    Title = u'Einstellungen'
    UseAutoloadFile = u'Lade Datei beim Start:'
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
    Author = u'Autor: %s'
    CreationDate = u'%a, %d %b %Y %H:%M:%S'
    Title = u'\xdcber EventGhost'
    Version = u'Version: %s (build %s)'
    tabAbout = u'\xdcber EventGhost'
    tabLicense = u'Lizenzabkommen'
    tabSpecialThanks = u'Besonderer Dank'
    tabSystemInfo = u'System Information'
class Plugin:
    class EventGhost:
        name = u'EventGhost'
        description = u'Diese Aktionen betreffen haupts\xe4chlich die Kern-Funktionen von EventGhost.'
        class AutoRepeat:
            name = u'Automatische Wiederholung'
            description = u'Ein Makro, dem dieser Befehl hinzugef\xfcgt wurde, wird solange wiederholt, wie die ausl\xf6sende Taste gedr\xfcckt gehalten wird.'
            seconds = u'Sekunden'
            text1 = u'Beginne erste Wiederholung nach'
            text2 = u'mit einer Wiederholung alle'
            text3 = u'Beschleunige Wiederholungen innerhalb von'
            text4 = u'auf eine Wiederholung alle'
        class Comment:
            name = u'Beschreibung'
            description = u'Ein Befehl der nichts tut, aber zur Kommentierung der Konfiguration benutzt werden kann.'
        class DisableItem:
            name = u'Deaktiviere ein Element'
            description = u'Deaktiviere ein Element'
            label = u'Deaktiviere: %s'
            text1 = u'Bitte w\xe4hlen Sie das zu deaktivierende Element:'
        class EnableExclusive:
            name = u'Aktiviere exklusiv Ordner/Makro'
            description = u'Aktiviert einen Ordner oder ein Makro, wobei gleichzeitig alle anderen Ordner/Makros, die auf der gleichen Baumebene liegen, deaktiviert werden.'
            label = u'Aktiviere exklusiv: %s'
            text1 = u'Bitte w\xe4hlen Sie das exklusiv zu aktivierende Element:'
        class EnableItem:
            name = u'Aktiviere ein Element'
            description = u'Aktiviere ein Element'
            label = u'Aktiviere: %s'
            text1 = u'Bitte w\xe4hlen Sie das zu aktivierende Element:'
        class FlushEvents:
            name = u'Verwerfe alle ausstehenden Ereignisse'
            description = u'Diese Aktion verwirft alle Ereignisse die sich momentan in der Verarbeitungsschlange befinden.\n\nDieses ist n\xfctzlich, wenn ein Makro eine ziemlich lange Zeit zum Verarbeiten braucht und sich Ereignisse innherhalb dieser Zeit angesammelt haben, die nicht verarbeitet werden sollen.\n\n<p><b>Beispiel:</b> Sie haben ein lang andauerndes "Starte System" Makro, welches ca. 90 Sekunden braucht um z.B. einen Projektor anzuschalten und dann verschiedene Programme zu starten. Der Benutzer wird von dieser Ausf\xfchrung nichts sehen, bis endlich der Projektor ein Bild zeigt und daher u.U. aus Ungeduld die ausl\xf6sende Taste mehrfach dr\xfccken, was dazu f\xfchren w\xfcrde, dass diese lange Verarbeitung wieder und wieder gestartet wird. Um dieses zu verhindern, k\xf6nnen Sie die "Verwerfe alle ausstehenden Ereignisse" Aktion an das Ende Ihres Makros stellen, wodurch die \xfcberfl\xfcssigen Tastendruck-Wiederholungen entfernt werden.'
        class Jump:
            name = u'Unbedingter Sprung'
            description = u'Springt zu einem anderen Makro.'
            label1 = u'Springe zu %s'
            label2 = u'Springe zu %s und kehre zur\xfcck'
            mesg1 = u'W\xe4hle Makro...'
            mesg2 = u'Bitte w\xe4hlen sie das Makro, welches ausgef\xfchrt werden soll:'
            text2 = u'Gehe zu:'
            text3 = u'Kehre zur\xfcck nach Ausf\xfchrung'
        class JumpIf:
            name = u'Bedingter Sprung'
            description = u'Springt zu einem anderen Makro, wenn die angegebene Python-Bedingung den Wahrheitswert "True" ergibt.'
            label1 = u'Wenn %s springe zu %s'
            label2 = u'Wenn %s springe zu %s und kehre zur\xfcck'
            mesg1 = u'W\xe4hle Makro...'
            mesg2 = u'Bitte w\xe4hlen sie das Makro, welches ausgef\xfchrt werden soll, wenn die Python-Bedingung zutrifft.'
            text1 = u'Wenn:'
            text2 = u'Gehe zu:'
            text3 = u'Kehre zur\xfcck nach Ausf\xfchrung'
        class JumpIfLongPress:
            name = u'Wenn langer Tastendruck'
            description = u'Springt zu einem anderen Makro, wenn die ausl\xf6sende Taste l\xe4nger als die eingestellte Zeit gedr\xfcckt wird.'
            label = u'Wenn Tastendruck l\xe4nger als %s s, gehe zu: %s'
            text1 = u'Wenn die Taste l\xe4nger als'
            text2 = u'Sekunden gedr\xfcckt wird, springe zu dem'
            text3 = u'Makro:'
            text4 = u'Makro ausw\xe4hlen...'
            text5 = u'Bitte w\xe4hlen Sie das Makro, welches bei einem langen\nTastendruck angesprungen werden soll.'
        class NewJumpIf:
            name = u'Sprungbefehl'
            description = u'Springt zu einem anderen Makro, wenn die angegebene Bedingung zutrifft.'
            choices = [
                u'letzter Befehl erfolgreich',
                u'letzter Befehl nicht erfolgreich',
                u'Immer',
            ]
            labels = [
                u'Wenn erfolgreich springe zu "%s"',
                u'Wenn erfolglos springe zu "%s"',
                u'Springe zu "%s"',
                u'Wenn erfolgreich springe zu "%s" und kehre zur\xfcck',
                u'Wenn erfolglos springe zu "%s" und kehre zur\xfcck',
                u'Springe zu "%s" und kehre zur\xfcck',
            ]
            mesg1 = u'W\xe4hle Makro...'
            mesg2 = u'Bitte w\xe4hlen sie das Makro, welches ausgef\xfchrt werden soll, wenn die Bedingung zutrifft.'
            text1 = u'Wenn:'
            text2 = u'Springe zu:'
            text3 = u'und kehre zur\xfcck nach der Ausf\xfchrung'
        class PythonCommand:
            name = u'Python Befehl'
            description = u'F\xfchrt das angegebene Parameter als einzeiligen Python-Befehl aus.'
            parameterDescription = u'Python Anweisung:'
        class PythonScript:
            name = u'Python Skript'
            description = u'\xdcber diesen Befehl k\xf6nnen Python Skripte erzeugt werden, die alle M\xf6glichkeiten der Programmiersprache Python bieten.'
        class ShowOSD:
            name = u'Zeige OSD'
            description = u'Zeigt einen einfaches "On Screen Display"'
            alignment = u'Ausrichtung:'
            alignmentChoices = [
                u'oben links',
                u'oben rechts',
                u'unten links',
                u'unten rechts',
                u'mittig',
            ]
            display = u'Zeige auf Monitor:'
            editText = u'Darzustellender Text:'
            label = u'Zeige OSD: %s'
            osdColour = u'OSD Farbe:'
            osdColourButton = u'Zeichensatz Farbe'
            osdFont = u'OSD Zeichensatz:'
            osdFontButton = u'Zeichensatz'
            outlineColour = u'Umrandungsfarbe'
            outlineFont = u'Umrandungsfarbe'
            wait1 = u'Blende OSD nach'
            wait2 = u'Sekunden automatisch aus. (0 = nicht ausblenden)'
            xOffset = u'Horizontaler Versatz X:'
            yOffset = u'Vertikaler Versatz Y:'
        class StopIf:
            name = u'Stoppe wenn'
            description = u'Unterbricht die Ausf\xfchrung des aktuellen Makros, wenn die angegebene Python-Bedingung den Wert "wahr" liefert.'
            label = u'Stoppe wenn %s'
            parameterDescription = u'Python-Bedingung:'
        class StopProcessing:
            name = u'Beende Bearbeitung dieses Ereignisses'
            description = u'Wird dieser Befehl ausgef\xfchrt, dann sucht EventGhost nicht mehr nach weiteren Makros, die zu dem aktuellen Ereignis passen w\xfcrden.'
        class TriggerEvent:
            name = u'Erzeuge Ereignis'
            description = u'Erzeugt ein neues Ereignis (optional nach einiger Zeit).'
            labelWithTime = u'Erzeuge Ereignis "%s" nach %.2f Sekunden'
            labelWithoutTime = u'Erzeuge Ereignis "%s"'
            text1 = u'Zu erzeugender Ereignis-Name:'
            text2 = u'Verz\xf6gere das Ereignis um:'
            text3 = u'Sekunden. (0 = erzeuge sofort)'
        class Wait:
            name = u'Warte'
            description = u'Unterbricht die Ausf\xfchrung des Makros f\xfcr eine angegebene Zeit, bevor der n\xe4chste Befehl ausgef\xfchrt wird.'
            label = u'Warte: %s s'
            seconds = u'Sekunden'
            wait = u'Warte'
    class System:
        name = u'System'
        description = u'Diese Aktionen steuern verschiedene Eigenschaften des Betriebssystems.'
        forced = u'Erzwungen: %s'
        forcedCB = u'Erzwinge Schlie\xdfung aller Programme'
        class ChangeDisplaySettings:
            name = u'\xc4ndere Anzeige-Einstellungen'
            description = u'Anzeige-Eigenschaften \xe4ndern'
        class ChangeMasterVolumeBy:
            name = u'Ver\xe4ndere Master-Lautst\xe4rke'
            description = u'\xc4ndert die Gesamtlautst\xe4rke relativ.'
            text1 = u'Ver\xe4ndere Master-Lautst\xe4rke um'
            text2 = u'Prozent.'
        class Execute:
            name = u'Starte Anwendung'
            description = u'Startet eine ausf\xfchrbare Datei.'
            FilePath = u'Pfad zur ausf\xfchrbaren Datei:'
            Parameters = u'Aufruf-Parameter:'
            ProcessOptions = (
                u'Echtzeit',
                u'H\xf6her als normal',
                u'Normal',
                u'Niedriger als normal',
                u'Niedrig',
            )
            ProcessOptionsDesc = u'Prozess Priorit\xe4t:'
            WaitCheckbox = u'Auf Beendigung des Programmes warten bevor fortgeschritten wird.'
            WindowOptions = (
                u'Normal',
                u'Minimiert',
                u'Maximiert',
                u'Versteckt',
            )
            WindowOptionsDesc = u'Fenster-Optionen:'
            WorkingDir = u'Startverzeichnis:'
            browseExecutableDialogTitle = u'W\xe4hlen sie die ausf\xfchrbare Datei'
            browseWorkingDirDialogTitle = u'W\xe4hlen sie das Arbeitsverzeichnis'
            label = u'Starte Anwendung: %s'
        class Hibernate:
            name = u'Hibernate Modus'
        class LockWorkstation:
            name = u'Rechner sperren'
        class LogOff:
            name = u'Benutzer abmelden'
        class MonitorGroup:
            name = u'Bildschirm'
        class MonitorPowerOff:
            name = u'Bildschirm ausschalten'
        class MonitorPowerOn:
            name = u'Bildschirm reaktivieren'
        class MonitorStandby:
            name = u'Bildschirm standby'
        class MuteOff:
            name = u'Stummschaltung aus'
            description = u'Deaktiviert die Stummschaltung.'
        class MuteOn:
            name = u'Stummschaltung an'
            description = u'Aktiviert die Stummschaltung.'
        class OpenDriveTray:
            name = u'\xd6ffne/Schlie\xdfe Laufwerksschublade'
            description = u'Erm\xf6glicht es die Laufwerksschublade von CD und DVD-Laufwerken zu \xf6ffnen und zu schlie\xdfen.'
            driveLabel = u'Laufwerk:'
            labels = [
                u'\xd6ffne/Schlie\xdfe Laufwerksschublade: %s',
                u'\xd6ffne Laufwerksschublade: %s',
                u'Schlie\xdfe Laufwerksschublade: %s',
            ]
            options = [
                u'Laufwerksschublade wechselnd \xf6ffnen und schlie\xdfen',
                u'Nur Laufwerksschublade \xf6ffnen',
                u'Nur Laufwerksschublade schlie\xdfen',
            ]
            optionsLabel = u'W\xe4hle Aktion'
        class PlaySound:
            name = u'Audiodatei abspielen'
            fileMask = u'WAV-Dateien (*.WAV)|*.wav|Alle Dateien (*.*)|*.*'
            text1 = u'Pfad zur Audiodatei:'
            text2 = u'Warte auf Beendigung'
        class PowerDown:
            name = u'Rechner ausschalten'
        class PowerGroup:
            name = u'Energieoptionen'
        class Reboot:
            name = u'Rechner neu starten'
        class RegistryChange:
            name = u'Registrierungs-Wert \xe4ndern'
        class RegistryQuery:
            name = u'Registrierungs-Wert auslesen'
        class SetClipboard:
            name = u'Zeichenkette in die Zwischenablage kopieren'
            description = u'Kopiert eine als Parameter angegebene Zeichenkette in die System-Zwischenablage.'
            error = u'Kann Zwischenablage nicht \xf6ffnen'
        class SetMasterVolume:
            name = u'Setze Master-Lautst\xe4rke'
            description = u'Setzt die Gesamtlautst\xe4rke auf einen absoluten Wert.'
            text1 = u'Setze Master-Lautst\xe4rke auf'
            text2 = u'Prozent.'
        class SetWallpaper:
            name = u'Desktop-Hintergrund wechseln'
            description = u'Wechselt das Desktop-Hintergrundbild.'
            choices = (
                u'Zentriert',
                u'Nebeneinander',
                u'Gestreckt',
            )
            fileMask = u'Alle Bilddateien|*.jpg;*.bmp;*.gif|Alle Dateien (*.*)|*.*'
            text1 = u'Pfad zur Bilddatei:'
            text2 = u'Ausrichtung:'
        class ShowPicture:
            name = u'Bild anzeigen'
            allFiles = u'Alle Dateien'
            allImageFiles = u'Alle Bilddateien'
            display = u'Monitor:'
            path = u'Pfad zur Bilddatei:'
        class SoundGroup:
            name = u'Audiokarte'
            description = u'Diese Aktionen steuern die Audio-Funktionen des Computers.'
        class Standby:
            name = u'Rechner standby'
        class StartScreenSaver:
            name = u'Starte Bildschirmschoner'
            description = u'Startet den momentan im Betreibssystem ausgew\xe4hlten Blidschrimschoner.'
        class ToggleMute:
            name = u'Stummschaltung umschalten'
            description = u'Wechselt die Stummschaltung von aktiviert auf deaktiviert und umgekehrt.'
    class Window:
        name = u'Fenster'
        class BringToFront:
            name = u'Fenster nach vorne bringen'
            description = u'Bringt ein Fenster vor alle anderen Fenster des Desktops.'
        class Close:
            name = u'Fenster schlie\xdfen'
            description = u'Schlie\xdft Anwendungs-Fenster'
        class FindWindow:
            name = u'Finde Fenster'
            description = u'Sucht ein Fenster, welches dann f\xfcr weitere Befehle der Fenster-Gruppe als Ziel definiert wird.'
            drag1 = u'Ziehe mich auf\nein Fenster.'
            drag2 = u'Nun bewege mich\nauf ein Fenster.'
            hide_box = u'Verstecke EventGhost beim Ziehen'
            invisible_box = u'Auch unsichtbare Objekte durchsuchen'
            label = u'Finde Fenster: %s'
            label2 = u'Finde vorderstes Fenster'
            matchNum1 = u'Nur den Treffer Nr.'
            matchNum2 = u'zur\xfcckgeben'
            onlyForground = u'Nur vorderstes Fenster suchen'
            options = (
                u'Programm:',
                u'Fenster Name:',
                u'Fenster Klasse:',
                u'Unter-Fenster Name:',
                u'Unter-Fenster Klasse:',
            )
            refresh_btn = u'&Aktualisieren'
            stopMacro = [
                u'Stoppe Makro wenn Ziel nicht gefunden',
                u'Stoppe Makro wenn Ziel gefunden',
                u'Niemals Makro stoppen',
            ]
            testButton = u'Test'
            wait1 = u'Warte bis zu '
            wait2 = u'Sekunden auf das Erscheinen des Fensters.'
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
            text1 = u'Setze horizontale Position X:'
            text2 = u'Pixel'
            text3 = u'Setze vertikale Position Y:'
            text4 = u'Pixel'
        class Resize:
            name = u'Fenstergr\xf6\xdfe \xe4ndern'
            description = u'\xc4ndert die Gr\xf6\xdfe eines Fensters.'
            label = u'\xc4ndere Fenstergr\xf6\xdfe auf %s, %s'
            text1 = u'Setze Breite auf'
            text2 = u'Pixel'
            text3 = u'Setze H\xf6he auf'
            text4 = u'Pixel'
        class Restore:
            name = u'Fenster wiederherstellen'
        class SendKeys:
            name = u'Emuliere Tastatureingabe'
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
        name = u'Maus'
        class GoDirection:
            name = u'Starte Mausbewegung in eine Richtung'
            label = u'Starte Mausbewegung in Richtung %.2f\xb0'
            text1 = u'Starte Mausbewegung in Richtung'
            text2 = u'Grad.'
        class LeftButton:
            name = u'Linke Maustaste'
        class LeftDoubleClick:
            name = u'Linke Maustaste Doppelklick '
        class MouseWheel:
            name = u'Drehe Mausrad'
            description = u'Emuliert Drehungen des Mausrades'
            label = u'Drehe Mausrad um %d Rastungen'
            text1 = u'Drehe Mausrad um'
            text2 = u'Rastungen. (Negative Werte drehen nach unten)'
        class MoveAbsolute:
            name = u'Setze Maus-Position'
            label = u'Bewege Maus nach x:%s, y:%s'
            text1 = u'Setze horizontale Position X:'
            text2 = u'Pixel'
            text3 = u'Setze vertikale Position Y:'
            text4 = u'Pixel'
        class RightButton:
            name = u'Rechte Maustaste'
        class RightDoubleClick:
            name = u'Rechte Maustaste Doppelklick'
        class ToggleLeftButton:
            name = u'Linke Maustaste umschalten'
    class Joystick:
        name = u'Joystick'
        description = u'Dieses Plugin erlaubt es Joysticks und Gamepads als Ereignisquelle zu verwenden.'
    class Keyboard:
        name = u'Tastatur'
        description = u'Dieses Plugin generiert Ereignisse bei Tastendruck (Hotkey).'
    class NetworkReceiver:
        name = u'Netzwerk Ereignis Empf\xe4nger'
        description = u'Empf\xe4ngt Ereignisse von einem "Netzwerk Ereignis Sender" Plugin.'
        event_prefix = u'Ereignis Prefix:'
        password = u'Passwort:'
        port = u'Port:'
    class NetworkSender:
        name = u'Netzwerk Ereignis Sender'
        description = u'Sendet Ereignisse zu einem "Netzwerk Ereignis Empf\xe4nger" Plugin \xfcber das TCP/IP Protokoll.'
        password = u'Passwort:'
    class Serial:
        name = u'Serieller Anschluss'
        description = u'Allgemeine Kommunikation \xfcber einen seriellen Anschluss.'
        baudrate = u'Bits pro Sekunde:'
        bytesize = u'Datenbits:'
        flowcontrol = u'Flusssteuerung:'
        handshakes = [
            u'Keine',
            u'Xon / Xoff',
            u'Hardware',
        ]
        parities = [
            u'Keine',
            u'Ungerade',
            u'Gerade',
        ]
        parity = u'Parit\xe4t:'
        port = u'Port:'
        stopbits = u'Stopbits:'
        class Read:
            name = u'Lese'
            read_all = u'Lese soviele Zeichen wie momentan verf\xfcgbar sind.'
            read_some = u'Lese genau diese Anzahl an Zeichen:'
            read_time = u'und warte maximal diese Anzahl an Millisekunden auf sie:'
        class Write:
            name = u'Sende'
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
    class SysTrayMenu:
        name = u'System Tray Men\xfc'
        description = u'Erm\xf6glicht es das Tray-Men\xfc von EventGhost um eigene Men\xfc-Eintr\xe4ge zu erweitern.'
        addButton = u'Hinzuf\xfcgen'
        deleteButton = u'Entfernen'
        editEvent = u'Ereignis:'
        editLabel = u'Beschriftung:'
        eventHeader = u'Ereignis'
        labelHeader = u'Beschriftung'
        unnamedEvent = u'Ereignis%s'
        unnamedLabel = u'Neuer Men\xfc-Eintrag %s'
    class USB_UIRT:
        blinkRx = u'Blinke bei Empfang'
        blinkTx = u'Blinke beim Senden'
        irReception = u'IR Empfang'
        legacyCodes = u'Generiere UIRT2-kompatible Ereignisse'
        notFound = u'<unbekannt>'
        redIndicator = u'Funktion der roten Anzeige-LED'
        uuFirmDate = u'Firmware Datum: '
        uuFirmVersion = u'Firmware Version: '
        uuInfo = u'USB-UIRT Information'
        uuProtocol = u'Protokoll Version: '
        class TransmitIR:
            name = u'Sende IR'
            description = u'Sendet eine IR-Code durch das USB-UIRT Ger\xe4t.'
            infinite = u'unendlich'
            irCode = u'IR-Code:'
            learnButton = u'Lerne IR-Code...'
            repeatCount = u'Wiederholungen:'
            testButton = u'Teste IR Aussendung'
            wait1 = u'Warte auf:'
            wait2 = u'ms IR Inaktivit\xe4t vor Aussendung'
            zone = u'Zone:'
            zoneChoices = (
                u'Alle',
                u'Anschlussbuchse R-Kontakt',
                u'Anschlussbuchse L-Kontakt',
                u'Interner Sender',
            )
            class LearnDialog:
                acceptBurstButton = u'Akzeptiere Signalfolge'
                forceRaw = u'Lernen im RAW-Modus erzwingen'
                frequency = u'Frequenz'
                helpText = u'1. Lassen Sie die Fernbedienung aus einer \nEntfernung von ungef\xe4hr 15 cm (oder auch weniger)\nauf die Vorderseite des USB-UIRT zeigen.\n\n2. DR\xdcCKEN und HALTEN Sie die gew\xfcnschte Taste\nder Fernbedienung, bis das Lernen abgeschlossen ist.\n'
                progress = u'Lern-Fortschritt'
                signalQuality = u'Signal'
                title = u'Lerne IR-Code'
    class Webserver:
        name = u'Webserver'
        description = u'Ein kleiner Webserver, mit dem Ereignisse durch HTML-Webseiten generiert werden k\xf6nnen.'
        documentRoot = u'Datenverzeichnis:'
        eventPrefix = u'Ereignis Prefix:'
        port = u'TCP/IP Port:'
    class X10:
        name = u'X10 Fernbedienung'
        description = u'Plugin f\xfcr X10 kompatible Funkfernbedienungen.\n\nDies beinhaltet Fernbedienungen wie:<br>\n<ul>\n<li><a href="http://www.ati.com/products/remotewonder/index.html">ATI Remote Wonder</a></li>\n<li><a href="http://www.snapstream.com/">SnapStream Firefly</a></li>\n<li><a href="http://www.nvidia.com/object/feature_PC_remote.html">NVIDIA Personal Cinema Remote</a></li>\n<li><a href="http://www.marmitek.com/">Marmitek PC Control</a></li>\n<li><a href="http://www.pearl.de/product.jsp?pdid=PE4444&catid=1601&vid=916&curr=DEM">Pearl Q-Sonic Master Remote 6in1</a></li>\n<li>Medion RF Remote Control</li>\n</ul>\n'
        allButton = u'&Alle'
        errorMesg = u'Kein X10 Empf\xe4nger gefunden!'
        idBox = u'Aktivierte IDs:'
        noneButton = u'&Keine'
        remoteBox = u'Fernbedienungstyp:'
        usePrefix = u'Ereignis-Prefix:'
