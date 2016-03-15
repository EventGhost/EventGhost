# -*- coding: UTF-8 -*-
class General:
    apply = u"Ü&bernehmen"
    autostartItem = u"Autostart"
    browse = u"Suchen..."
    cancel = u"Abbrechen"
    choose = u"Auswählen"
    configTree = u"Konfigurations-Baum"
    deleteLinkedItems = u"Wenigstens ein Element außerhalb der momentanen Selektion verweist auf ein Element innerhalb der zu löschenden Selektion. Wenn sie diese Selektion löschen, wird das verweisende Element nicht mehr richtig funktionieren.\n\nSind sie sicher, dass sie die Selektion löschen wollen?"
    deleteManyQuestion = u"Dieses Element hat %s Unterelemente.\n\nSollen wirklich alle gelöscht werden?"
    deletePlugin = u"Dieses Plugin wird von Befehlen in ihrer aktuellen Konfiguration benutzt.\n\nSie können es erst entfernen, wenn alle Befehle die dieses Plugin benutzen\nvorher ebenfalls entfernt wurden."
    deleteQuestion = u"Soll dieses Element wirklich gelöscht werden?"
    help = u"&Hilfe"
    moreTag = u"mehr..."
    no = u"&Nein"
    noOptionsAction = u"Diese Aktion hat keine einstellbaren Optionen."
    noOptionsPlugin = u"Dieses Plugin hat keine einstellbaren Optionen."
    ok = u"Ok"
    pluginLabel = u"Plugin: %s"
    settingsActionCaption = u"Befehls-Element Einstellungen"
    settingsEventCaption = u"Ereignis-Element Einstellungen"
    settingsPluginCaption = u"Plugin-Element Einstellungen"
    test = u"&Test"
    unnamedEvent = u"<Unbenanntes Ereignis>"
    unnamedFile = u"<Unbenannte Datei>"
    unnamedFolder = u"<Unbenannter Ordner>"
    unnamedMacro = u"<Unbenanntes Makro>"
    yes = u"&Ja"
class MainFrame:
    onlyLogAssigned = u"Nur &zugewiesene und aktivierte Ereignisse aufzeichnen"
    onlyLogAssignedToolTip = u"Wenn markiert, zeigt das Log nur noch Ereignisse an, die in der momentanen\nKonstellation der Konfiguration ein Makro ausführen werden. Deshalb sollte diese\nOption *nicht* aktiviert werden, wenn man neue Ereignisse zuweisen will."
    class Logger:
        caption = u"Log"
        welcomeText = u"---> Willkommen beim EventGhost <---"
    class Menu:
        About = u"&Über EventGhost..."
        AddAction = u"&Befehl hinzufügen"
        AddEvent = u"&Ereignis hinzufügen"
        AddFolder = u"&Ordner hinzufügen"
        AddMacro = u"&Makro hinzufügen"
        AddPlugin = u"&Plugin hinzufügen"
        Apply = u"Änderungen &anwenden"
        CheckUpdate = u"Auf neuere Version prüfen..."
        ClearLog = u"Log löschen"
        Close = u"S&chließen"
        CollapseAll = u"Alle einklappen"
        ConfigurationMenu = u"&Konfiguration"
        Configure = u"Element &konfigurieren..."
        Copy = u"&Kopieren"
        Cut = u"&Ausschneiden"
        Delete = u"&Löschen"
        Disabled = u"Element &deaktivieren"
        EditMenu = u"&Bearbeiten"
        Execute = u"Element &ausführen"
        Exit = u"&Beenden"
        ExpandAll = u"Alle ausklappen"
        ExpandOnEvents = u"Selektiere Elemente bei Ausführung"
        Export = u"Exportieren..."
        FileMenu = u"&Datei"
        Find = u"S&uchen..."
        FindNext = u"&Weitersuchen"
        HelpContents = u"&Hilfethemen"
        HelpMenu = u"&Hilfe"
        HideShowToolbar = u"Symbolleiste"
        Import = u"Importieren..."
        IndentLog = u"Log einrücken"
        LogActions = u"Auch Befehle aufzeichnen"
        LogMacros = u"Auch Makros aufzeichnen"
        LogTime = u"Auch Zeiten aufzeichnen"
        New = u"&Neu"
        Open = u"Ö&ffnen..."
        Options = u"&Einstellungen..."
        Paste = u"E&infügen"
        PythonShell = u"Python Shell"
        Redo = u"&Wiederholen"
        Rename = u"Element &umbenennen"
        Reset = u"Zurücksetzen"
        Save = u"&Speichern"
        SaveAs = u"Speichern &unter..."
        SelectAll = u"&Alles markieren"
        Undo = u"&Rückgängig"
        ViewMenu = u"&Ansicht"
        WebForum = u"Forum"
        WebHomepage = u"Homepage"
        WebWiki = u"Wiki"
    class Messages:
        cantAddAction = u"Sie können kein Befehls-Element an dieser Stelle hinzufügen.\n\nBitte selektieren sie ein Makro-Element oder ein Element innerhalb eines Makros um ein Befehls-Element hinzuzufügen."
        cantAddEvent = u"Sie können kein Ereignis-Element an dieser Stelle hinzufügen.\n\nBitte selektieren sie ein Makro-Element oder ein Element innerhalb eines Makros um ein Ereignis-Element hinzuzufügen."
        cantConfigure = u"Sie können dieses Element nicht konfigurieren.\n\nNur Befehls-, Ereignis- und Plugin-Elemente sind konfigurierbar."
        cantDisable = u"Sie können dieses Element nicht deaktivieren.\n\nEine Deaktivierung des Wurzel-Elementes und des Autostart-Elementes sind nicht möglich."
        cantExecute = u"Sie können dieses Element nicht ausführen.\n\nOrdner-Elemente, Ereignis-Elemente und das Wurzel-Element können nicht ausgeführt werden."
        cantRename = u"Sie können dieses Element nicht umbenennen.\n\nNur Ordner-, Makro- und Befehls-Elemente können umbenannt werden."
    class SaveChanges:
        dontSaveButton = u"&Nicht Speichern"
        mesg = u"Die Datei wurde verändert.\n\nAktuelle Änderungen speichern?\n"
        saveButton = u"&Speichern"
    class TaskBarMenu:
        Exit = u"Beenden"
        Hide = u"EventGhost verstecken"
        Show = u"EventGhost wiederherstellen"
    class Tree:
        caption = u"Konfiguration"
class Error:
    FileNotFound = u'Datei "%s" konnte nicht gefunden werden.'
    InAction = u'Fehler in Befehl: "%s"'
    configureError = u"Fehler beim Konfigurieren von: %s"
    pluginLoadError = u"Fehler beim Laden der Plugin-Datei %s."
    pluginNotActivated = u'Plugin "%s" ist nicht aktiviert'
    pluginStartError = u"Fehler beim Start des Plugins: %s"
class Exceptions:
    DeviceInitFailed = u"Gerät kann nicht initialisiert werden!"
    DeviceNotFound = u"Gerät nicht gefunden!"
    DeviceNotReady = u"Gerät ist nicht bereit!"
    DriverNotFound = u"Treiber nicht gefunden!"
    DriverNotOpen = u"Kann den Treiber nicht öffnen!"
    InitFailed = u"Initialisierung fehlgeschlagen!"
    PluginLoadError = u"Fehler beim Laden des Plugins!"
    PluginNotFound = u"Plugin nicht gefunden!"
    ProgramNotFound = u"Programm nicht gefunden!"
    ProgramNotRunning = u"Programm ist nicht gestartet!"
    SerialOpenFailed = u"Kann den seriellen Anschluss nicht öffnen!"
class CheckUpdate:
    ManErrorMesg = u"Es konnte nicht festgestellt werden, ob es eine neuere Version von EventGhost gibt.\n\nBitte versuchen sie es später noch einmal."
    ManOkMesg = u"Es ist keine neuere Version von EventGhost verfügbar."
    downloadButton = u"Download-Seite besuchen"
    newVersionMesg = u"Eine neuere Version von EventGhost wurde veröffentlicht.\n\n Diese Version:      %s\n    Aktuellste Version: %s\n\nWollen Sie die Download-Seite besuchen?"
    waitMesg = u"Bitte warten sie während EventGhost die Update-Informationen bezieht."
class AddActionDialog:
    descriptionLabel = u"Beschreibung"
    title = u"Befehl auswählen..."
class AddPluginDialog:
    author = u"Autor:"
    descriptionBox = u"Beschreibung"
    externalPlugins = u"Steuerung externer Geräte"
    noInfo = u"Keine Information verfügbar."
    noMultiload = u"Dieses Plugin unterstützt kein Mehrfachladen und\nSie haben schon eine Instanz dieses Plugins in ihrer Konfiguration."
    noMultiloadTitle = u"Mehrfachladen nicht möglich"
    otherPlugins = u"Sonstige"
    programPlugins = u"Programmsteuerung"
    remotePlugins = u"Fernbedienungsempfänger"
    title = u"Plugin hinzufügen..."
    version = u"Version:"
class AddActionGroupDialog:
    caption = u"Befehle hinzufügen?"
    message = u"EventGhost kann einen Ordner mit allen Befehlen dieses Plugins dem Konfigurationsbaum hinzufügen. Wenn Sie dieses wollen, selektieren Sie bitte unten die Stelle an dem dies geschehen soll und drücken die OK-Schaltfläche.\n\nAnsonsten drücken Sie bitte die Abbrechen-Schaltfläche."
class EventItem:
    eventItem = u"Ereignis-Element"
    eventName = u"Ereignis Name:"
    notice = u"Hinweis: Sie können ein Ereignis-Element auch zuweisen, indem Sie es vom Log auf ein Makro-Element ziehen."
class OptionsDialog:
    CheckUpdate = u"Auf neuere Version prüfen beim Programmstart"
    HideOnClose = u"Minimiere wenn Schließen-Schaltfläche gedrückt wird"
    HideOnStartup = u"Minimiert starten"
    LanguageGroup = u"Sprache"
    StartGroup = u"Beim Start"
    StartWithWindows = u"Automatisch mit Windows starten"
    Tab1 = u"Allgemein"
    Title = u"Einstellungen"
    UseAutoloadFile = u"Lade Datei beim Start:"
    confirmDelete = u"Zeige Warnhinweis beim Löschen von Elementen"
    limitMemory1 = u"Begrenze Speicherverbrauch wenn minimiert auf"
    limitMemory2 = u"MB"
class FindDialog:
    caseSensitive = u"Groß-/Kleins&chreibung beachten"
    direction = u"Suchrichtung"
    down = u"Nach &unten"
    findButton = u"&Weitersuchen"
    notFoundMesg = u'"%s" kann nicht gefunden werden.'
    searchLabel = u"&Suchen nach:"
    searchParameters = u"Auch &Parameter von Aktionen durchsuchen"
    title = u"Suchen"
    up = u"Nach &oben"
    wholeWordsOnly = u"Nu&r ganzes Wort suchen"
class AboutDialog:
    Author = u"Autor: %s"
    CreationDate = u"%a, %d %b %Y %H:%M:%S"
    Title = u"Über EventGhost"
    Version = u"Version: %s (build %s)"
    tabAbout = u"Über EventGhost"
    tabChangelog = u"Versionshistorie"
    tabLicense = u"Lizenzabkommen"
    tabSpecialThanks = u"Besonderer Dank"
    tabSystemInfo = u"System Information"
class Plugin:
    class EventGhost:
        name = u"EventGhost"
        description = u"Diese Aktionen betreffen hauptsächlich die Kern-Funktionen von EventGhost."
        class AutoRepeat:
            name = u"Automatische Wiederholung"
            description = u"Ein Makro, dem dieser Befehl hinzugefügt wurde, wird solange wiederholt, wie die auslösende Taste gedrückt gehalten wird."
            seconds = u"Sekunden"
            text1 = u"Beginne erste Wiederholung nach"
            text2 = u"mit einer Wiederholung alle"
            text3 = u"Beschleunige Wiederholungen innerhalb von"
            text4 = u"auf eine Wiederholung alle"
        class Comment:
            name = u"Beschreibung"
            description = u"Ein Befehl der nichts tut, aber zur Kommentierung der Konfiguration benutzt werden kann."
        class DisableItem:
            name = u"Deaktiviere ein Element"
            description = u"Deaktiviere ein Element"
            label = u"Deaktiviere: %s"
            text1 = u"Bitte wählen Sie das zu deaktivierende Element:"
        class EnableExclusive:
            name = u"Aktiviere exklusiv Ordner/Makro"
            description = u"Aktiviert einen Ordner oder ein Makro, wobei gleichzeitig alle anderen Ordner/Makros, die auf der gleichen Baumebene liegen, deaktiviert werden."
            label = u"Aktiviere exklusiv: %s"
            text1 = u"Bitte wählen Sie das exklusiv zu aktivierende Element:"
        class EnableItem:
            name = u"Aktiviere ein Element"
            description = u"Aktiviere ein Element"
            label = u"Aktiviere: %s"
            text1 = u"Bitte wählen Sie das zu aktivierende Element:"
        class FlushEvents:
            name = u"Verwerfe alle ausstehenden Ereignisse"
            description = u'Diese Aktion verwirft alle Ereignisse die sich momentan in der Verarbeitungsschlange befinden.\n\nDieses ist nützlich, wenn ein Makro eine ziemlich lange Zeit zum Verarbeiten braucht und sich Ereignisse innherhalb dieser Zeit angesammelt haben, die nicht verarbeitet werden sollen.\n\n<p><b>Beispiel:</b> Sie haben ein lang andauerndes "Starte System" Makro, welches ca. 90 Sekunden braucht um z.B. einen Projektor anzuschalten und dann verschiedene Programme zu starten. Der Benutzer wird von dieser Ausführung nichts sehen, bis endlich der Projektor ein Bild zeigt und daher u.U. aus Ungeduld die auslösende Taste mehrfach drücken, was dazu führen würde, dass diese lange Verarbeitung wieder und wieder gestartet wird. Um dieses zu verhindern, können Sie die "Verwerfe alle ausstehenden Ereignisse" Aktion an das Ende Ihres Makros stellen, wodurch die überflüssigen Tastendruck-Wiederholungen entfernt werden.'
        class JumpIfLongPress:
            name = u"Wenn langer Tastendruck"
            description = u"Springt zu einem anderen Makro, wenn die auslösende Taste länger als die eingestellte Zeit gedrückt wird."
            label = u"Wenn Tastendruck länger als %s s, gehe zu: %s"
            text1 = u"Wenn die Taste länger als"
            text2 = u"Sekunden gedrückt wird, springe zu dem"
            text3 = u"Makro:"
            text4 = u"Makro auswählen..."
            text5 = u"Bitte wählen Sie das Makro, welches bei einem langen\nTastendruck angesprungen werden soll."
        class NewJumpIf:
            name = u"Sprungbefehl"
            description = u"Springt zu einem anderen Makro, wenn die angegebene Bedingung zutrifft."
            choices = [
                u"letzter Befehl erfolgreich",
                u"letzter Befehl nicht erfolgreich",
                u"Immer",
            ]
            labels = [
                u'Wenn erfolgreich springe zu "%s"',
                u'Wenn erfolglos springe zu "%s"',
                u'Springe zu "%s"',
                u'Wenn erfolgreich springe zu "%s" und kehre zurück',
                u'Wenn erfolglos springe zu "%s" und kehre zurück',
                u'Springe zu "%s" und kehre zurück',
            ]
            mesg1 = u"Wähle Makro..."
            mesg2 = u"Bitte wählen sie das Makro, welches ausgeführt werden soll, wenn die Bedingung zutrifft."
            text1 = u"Wenn:"
            text2 = u"Springe zu:"
            text3 = u"und kehre zurück nach der Ausführung"
        class PythonCommand:
            name = u"Python Befehl"
            description = u"Führt das angegebene Parameter als einzeiligen Python-Befehl aus."
            parameterDescription = u"Python Anweisung:"
        class PythonScript:
            name = u"Python Skript"
            description = u"Über diesen Befehl können Python Skripte erzeugt werden, die alle Möglichkeiten der Programmiersprache Python bieten."
        class ShowOSD:
            name = u"Zeige OSD"
            description = u'Zeigt einen einfaches "On Screen Display"'
            alignment = u"Ausrichtung:"
            alignmentChoices = [
                u"oben links",
                u"oben rechts",
                u"unten links",
                u"unten rechts",
                u"mittig",
                u"mittig unten",
                u"mittig oben",
                u"mittig links",
                u"mittig rechts",
            ]
            display = u"Zeige auf Monitor:"
            editText = u"Darzustellender Text:"
            label = u"Zeige OSD: %s"
            osdColour = u"OSD Farbe:"
            osdFont = u"OSD Zeichensatz:"
            outlineFont = u"Umrandungsfarbe"
            skin = u"Benutze Skin"
            wait1 = u"Blende OSD nach"
            wait2 = u"Sekunden automatisch aus. (0 = nicht ausblenden)"
            xOffset = u"Horizontaler Versatz X:"
            yOffset = u"Vertikaler Versatz Y:"
        class StopProcessing:
            name = u"Beende Bearbeitung dieses Ereignisses"
            description = u"Wird dieser Befehl ausgeführt, dann sucht EventGhost nicht mehr nach weiteren Makros, die zu dem aktuellen Ereignis passen würden."
        class TriggerEvent:
            name = u"Erzeuge Ereignis"
            description = u"Erzeugt ein neues Ereignis (optional nach einiger Zeit)."
            labelWithTime = u'Erzeuge Ereignis "%s" nach %.2f Sekunden'
            labelWithoutTime = u'Erzeuge Ereignis "%s"'
            text1 = u"Zu erzeugender Ereignis-Name:"
            text2 = u"Verzögere das Ereignis um:"
            text3 = u"Sekunden. (0 = erzeuge sofort)"
        class Wait:
            name = u"Warte"
            description = u"Unterbricht die Ausführung des Makros für eine angegebene Zeit, bevor der nächste Befehl ausgeführt wird."
            label = u"Warte: %s s"
            seconds = u"Sekunden"
            wait = u"Warte"
    class System:
        name = u"System"
        description = u"Diese Aktionen steuern verschiedene Eigenschaften des Betriebssystems."
        forced = u"Erzwungen: %s"
        forcedCB = u"Erzwinge Schließung aller Programme"
        class ChangeDisplaySettings:
            name = u"Ändere Anzeige-Einstellungen"
            description = u"Anzeige-Eigenschaften ändern"
            colourDepth = u"Farbtiefe:"
            display = u"Bildschirm:"
            frequency = u"Bildschirmfrequenz:"
            includeAll = u"Modi anzeigen, die von dieser Monitor unter Umständen nicht unterstützt werden."
            label = u"Setze Anzeige %d auf %dx%d@%d Hz"
            resolution = u"Auflösung:"
            storeInRegistry = u"Speichere Einstellung in der Registry."
        class ChangeMasterVolumeBy:
            name = u"Verändere Master-Lautstärke"
            description = u"Ändert die Gesamtlautstärke relativ."
            text1 = u"Verändere Master-Lautstärke um"
            text2 = u"Prozent."
        class Execute:
            name = u"Starte Anwendung"
            description = u"Startet eine ausführbare Datei."
            FilePath = u"Pfad zur ausführbaren Datei:"
            Parameters = u"Aufruf-Parameter:"
            ProcessOptions = (
                u"Echtzeit",
                u"Höher als normal",
                u"Normal",
                u"Niedriger als normal",
                u"Niedrig",
            )
            ProcessOptionsDesc = u"Prozess Priorität:"
            WaitCheckbox = u"Auf Beendigung des Programmes warten bevor fortgeschritten wird."
            WindowOptions = (
                u"Normal",
                u"Minimiert",
                u"Maximiert",
                u"Versteckt",
            )
            WindowOptionsDesc = u"Fenster-Optionen:"
            WorkingDir = u"Startverzeichnis:"
            browseExecutableDialogTitle = u"Wählen sie die ausführbare Datei"
            browseWorkingDirDialogTitle = u"Wählen sie das Arbeitsverzeichnis"
            label = u"Starte Anwendung: %s"
        class Hibernate:
            name = u"Ruhezustand"
            description = u"Wenn der Computer in den Ruhezustand wechselt, wird der Inhalt des Arbeitsspeichers gespeichert und der Computer wird heruntergefahren. Wenn er wieder gestartet wird, kehrt er zum vorherigen Zustand zurück. (Hibernation/S4)"
        class LockWorkstation:
            name = u"Computer sperren"
            description = u'Dieser Befehl sendet eine Anforderung and das System den Bildschirm zu sperren. Den Computer zu sperren schützt ihn vor unbefugtem Zugriff. Dieser Befehl führt zu dem gleichen Ergebnis wie das Drücken von Ctrl+Alt+Del und das anschließende Klicken auf "Computer sperren".'
        class LogOff:
            name = u"Benutzer abmelden"
            description = u"Beendet alle Programme in der aktuellen Benutzeranmeldung. Anschließend wird der Benutzer abgemeldet."
        class MonitorGroup:
            name = u"Bildschirm"
            description = u"Diese Befehle steuern verschiedene Eigenschaften des Bildschirms."
        class MonitorPowerOff:
            name = u"Bildschirm ausschalten"
            description = u"Schaltet das Anzeigegerät in den Power-Off Zustand. Dies ist der energiesparenste Modus, den das Anzeigegerät unterstützt."
        class MonitorPowerOn:
            name = u"Bildschirm reaktivieren"
            description = u"Schaltet das Anzeigegerät wieder an, wenn es sich im Energeisparmodus oder Power-Off-Modus befindet. Stoppt auch einen eventuell laufenden Bildschirmschoner."
        class MonitorStandby:
            name = u"Bildschirm standby"
            description = u"Schaltet das Anzeigegerät in den Energiesparmodus."
        class MuteOff:
            name = u"Stummschaltung aus"
            description = u"Deaktiviert die Stummschaltung."
        class MuteOn:
            name = u"Stummschaltung an"
            description = u"Aktiviert die Stummschaltung."
        class OpenDriveTray:
            name = u"Öffne/Schließe Laufwerksschublade"
            description = u"Ermöglicht es die Laufwerksschublade von CD und DVD-Laufwerken zu öffnen und zu schließen."
            driveLabel = u"Laufwerk:"
            labels = [
                u"Öffne/Schließe Laufwerksschublade: %s",
                u"Öffne Laufwerksschublade: %s",
                u"Schließe Laufwerksschublade: %s",
            ]
            options = [
                u"Laufwerksschublade wechselnd öffnen und schließen",
                u"Nur Laufwerksschublade öffnen",
                u"Nur Laufwerksschublade schließen",
            ]
            optionsLabel = u"Wähle Aktion"
        class PlaySound:
            name = u"Audiodatei abspielen"
            description = u"Spielt eine Audiodatei ab."
            fileMask = u"WAV-Dateien (*.WAV)|*.wav|Alle Dateien (*.*)|*.*"
            text1 = u"Pfad zur Audiodatei:"
            text2 = u"Warte auf Beendigung"
        class PowerDown:
            name = u"Rechner ausschalten"
            description = u"Fährt das System herunter und schaltet den Rechner aus."
        class PowerGroup:
            name = u"Energieoptionen"
            description = u"Diese Aktionen steuern den Energiestatus des Rechners."
        class Reboot:
            name = u"Rechner neu starten"
            description = u"Führt einen Neustart des Rechners aus."
        class RegistryChange:
            name = u"Registrierungs-Wert ändern"
            description = u"Verändert einen Wert in der Windows-Registrierung"
            actions = (
                u"anlegen oder verändern",
                u"nur ändern wenn vorhanden",
                u"löschen",
            )
            labels = (
                u'Ändere "%s" zu "%s"',
                u'Ändere "%s" zu "%s" nur wenn vorhanden',
                u'Lösche "%s"',
            )
        class RegistryGroup:
            name = u"Registrierung"
            description = u"Abfrage und Änderung von Werten in der Windows-Registrierung."
            actionText = u"Aktion:"
            chooseText = u"Registrierungs-Schlüssel wählen:"
            defaultText = u"(Standard)"
            keyOpenError = u"Fehler beim Öffnen des Registrierungs-Schlüssels"
            keyText = u"Schlüssel:"
            keyText2 = u"Schlüssel"
            newValue = u"Neuer Wert"
            noKeyError = u"Kein Schlüssel angegeben"
            noNewValueError = u"Kein neuer Wert angegeben"
            noSubkeyError = u"Kein Unterschlüssel angegeben"
            noTypeError = u"Keinen Type angegeben"
            noValueNameError = u"Kein Name für den Wert angegeben"
            noValueText = u"Wert nicht gefunden"
            oldType = u"Momentaner Typ:"
            oldValue = u"Momentaner Wert:"
            typeText = u"Typ:"
            valueChangeError = u"Fehler beim Versuch den Wert zu ändern"
            valueName = u"Name:"
            valueText = u"Wert:"
        class RegistryQuery:
            name = u"Registrierungs-Wert auslesen"
            description = u"Fragt die Windows-Registrierung ab und liefert einen Wert zurück oder vergleicht ihn."
            actions = (
                u"teste auf Existenz",
                u"liefere als Resultat zurück",
                u"vergleiche mit",
            )
            labels = (
                u'Prüfe ob "%s" vorhanden',
                u'Liefere "%s" als Resultat zurück',
                u'Vergleiche "%s" mit "%s"',
            )
        class SetClipboard:
            name = u"Zeichenkette in die Zwischenablage kopieren"
            description = u"Kopiert eine als Parameter angegebene Zeichenkette in die System-Zwischenablage."
            error = u"Kann Zwischenablage nicht öffnen"
        class SetDisplayPreset:
            fields = (
                u"Gerät",
                u"Links",
                u"Oben",
                u"Breite",
                u"Höhe",
                u"Frequenz",
                u"Farbtiefe",
                u"angeschlossen",
                u"primär",
                u"Flags",
            )
            query = u"Abfrage der momentanen Anzeige-Einstellungen"
        class SetMasterVolume:
            name = u"Setze Master-Lautstärke"
            description = u"Setzt die Gesamtlautstärke auf einen absoluten Wert."
            text1 = u"Setze Master-Lautstärke auf"
            text2 = u"Prozent."
        class SetWallpaper:
            name = u"Desktop-Hintergrund wechseln"
            description = u"Wechselt das Desktop-Hintergrundbild."
            choices = (
                u"Zentriert",
                u"Nebeneinander",
                u"Gestreckt",
            )
            fileMask = u"Alle Bilddateien|*.jpg;*.bmp;*.gif|Alle Dateien (*.*)|*.*"
            text1 = u"Pfad zur Bilddatei:"
            text2 = u"Ausrichtung:"
        class ShowPicture:
            name = u"Bild anzeigen"
            description = u"Zeigt eine Bilddatei auf dem Bildschirm an."
            allFiles = u"Alle Dateien"
            allImageFiles = u"Alle Bilddateien"
            display = u"Monitor:"
            path = u"Pfad zur Bilddatei:"
        class SoundGroup:
            name = u"Audiokarte"
            description = u"Diese Aktionen steuern die Audio-Funktionen des Computers."
        class Standby:
            name = u"Rechner standby"
            description = u"Versetzt den Rechner in den energiesparenden Standby-Modus, bei dem der Arbeitsspeicher aber weiterhin mit Strom versorgt wird."
        class StartScreenSaver:
            name = u"Starte Bildschirmschoner"
            description = u"Startet den momentan im Betreibssystem ausgewählten Blidschrimschoner."
        class ToggleMute:
            name = u"Stummschaltung umschalten"
            description = u"Wechselt die Stummschaltung von aktiviert auf deaktiviert und umgekehrt."
        class WakeOnLan:
            name = u"Wake on LAN"
            description = u"Sendet ein spezielles Netzwerkpaket um einen ausgeschalteten Computer über die eingebaute Netzwerkkarte zu starten."
            parameterDescription = u"MAC-Adresse der aufzuweckende Netzwerkkarten :"
    class Window:
        name = u"Fenster"
        class BringToFront:
            name = u"Fenster nach vorne bringen"
            description = u"Bringt ein Fenster vor alle anderen Fenster des Desktops."
        class Close:
            name = u"Fenster schließen"
            description = u"Schließt Anwendungs-Fenster"
        class FindWindow:
            name = u"Finde Fenster"
            description = u'Sucht ein oder mehrere Fenster, welche dann für weitere Befehle der Fenster-Gruppe als Ziel definiert werden.\n\n<p>Wenn ein Makro keinen "Finde Fenster" Befehl besitzt, werden alle Fenster Befehle dieses Makros nur auf das vorderste Fenster zielen.\n<p>In den Textfeldern können Sie die in geschweifte Klammern gesetzten Platzhalter {*} für beliebiger Zeichenfolgen und/oder {?} für genau ein Zeichen verwenden.'
            drag1 = u"Ziehe mich auf\nein Fenster."
            drag2 = u"Nun bewege mich\nauf ein Fenster."
            hide_box = u"Verstecke EventGhost beim Ziehen"
            invisible_box = u"Auch unsichtbare Objekte durchsuchen"
            label = u"Finde Fenster: %s"
            label2 = u"Finde vorderstes Fenster"
            matchNum1 = u"Nur den Treffer Nr."
            matchNum2 = u"zurückgeben"
            onlyFrontmost = u"Nur vorderstes Fenster suchen"
            options = (
                u"Programm:",
                u"Fenster Name:",
                u"Fenster Klasse:",
                u"Unter-Fenster Name:",
                u"Unter-Fenster Klasse:",
            )
            refresh_btn = u"&Aktualisieren"
            stopMacro = [
                u"Stoppe Makro wenn Ziel nicht gefunden",
                u"Stoppe Makro wenn Ziel gefunden",
                u"Niemals Makro stoppen",
            ]
            testButton = u"Test"
            wait1 = u"Warte bis zu "
            wait2 = u"Sekunden auf das Erscheinen des Fensters."
        class Maximize:
            name = u"Fenster maximieren"
            description = u"Maximiert Fenster"
        class Minimize:
            name = u"Fenster minimieren"
            description = u"Minimiert Fenster"
        class MoveTo:
            name = u"Fenster verschieben"
            description = u"Verschiebt Fenster"
            label = u"Fenster nach %s verschieben"
            text1 = u"Setze horizontale Position X:"
            text2 = u"Pixel"
            text3 = u"Setze vertikale Position Y:"
            text4 = u"Pixel"
        class Resize:
            name = u"Fenstergröße ändern"
            description = u"Ändert die Größe eines Fensters."
            label = u"Ändere Fenstergröße auf %s, %s"
            text1 = u"Setze Breite auf"
            text2 = u"Pixel"
            text3 = u"Setze Höhe auf"
            text4 = u"Pixel"
        class Restore:
            name = u"Fenster wiederherstellen"
            description = u"Stellt die Größe eines vorher maximierten Fensters wieder her."
        class SendKeys:
            name = u"Emuliere Tastatureingabe"
            description = u'Diese Aktion emuliert Tastatureingaben, die zur Kontrolle von anderen Programmen verwendet werden können. \n\n<p>Geben Sie einfach den zu tippenden Text in die Textbox ein. Um Sondertasten zu emulieren, muss ein Schlüsselwort in geschweifte Klammern gesetzt werden.\n<p>\nFor example if you want to have a cursor-up-key you write <b>{Up}</b>. You \ncan combine multiple keywords with the plus sign to get key-combinations like \n<b>{Shift+Ctrl+F1}</b> or <b>{Ctrl+V}</b>. The keywords are not \ncase-sensitive, so you can write {SHIFT+ctrl+F1} as well if you like. \n<p>\nSome keys differentiate between the left or the right side of the keyboard \nand can then be prefixed with an "L" or "R", like the Windows-Key:<br>\n<b>{Win}</b> or <b>{LWin}</b> or <b>{RWin}</b>\n<p>\nAnd here is the list of the remaining keywords EventGhost understands:<br>\n<b>{Ctrl}</b> or <b>{Control}<br>\n{Shift}<br>\n{Alt}<br>\n{Return}</b> or <b>{Enter}<br>\n{Back}</b> or <b>{Backspace}<br>\n{Tab}</b> or <b>{Tabulator}<br>\n{Esc}</b> or <b>{Escape}<br>\n{Spc}</b> or <b>{Space}<br>\n{Up}<br>\n{Down}<br>\n{Left}<br>\n{Right}<br>\n{PgUp}</b> or <b>{PageUp}<br>\n{PgDown}</b> or <b>{PageDown}<br>\n{Home}<br>\n{End}<br>\n{Ins}</b> or <b>{Insert}<br>\n{Del}</b> or <b>{Delete}<br>\n{Pause}<br>{Capslock}<br>\n{Numlock}<br>\n{Scrolllock}<br>\n{F1}, {F2}, ... , {F24}<br>\n{Apps}</b> (This is the context-menu-key)<b><br>\n<br>\n</b>These will emulate keys from the numpad:<b><br>\n{Divide}<br>{Multiply}<br>\n{Subtract}<br>\n{Add}<br>\n{Decimal}<br>\n{Numpad0}, {Numpad1}, ... , {Numpad9}</b>\n'
            insertButton = u"&Einfügen"
            specialKeyTool = u"Sondertasten Werkzeug"
            textToType = u"Zu tippender Text:"
            useAlternativeMethod = u"Verwende alternative Methode zur Emulation von Tastatureingaben."
            class Keys:
                backspace = u"Rücktaste"
                context = u"Kontextmenü Taste"
                delete = u"Entfernen"
                down = u"Pfeiltaste nach unten"
                end = u"Ende"
                home = u"Pos1"
                insert = u"Einfügen"
                left = u"Pfeiltaste nach links"
                num0 = u"Ziffernblock 0"
                num1 = u"Ziffernblock 1"
                num2 = u"Ziffernblock 2"
                num3 = u"Ziffernblock 3"
                num4 = u"Ziffernblock 4"
                num5 = u"Ziffernblock 5"
                num6 = u"Ziffernblock 6"
                num7 = u"Ziffernblock 7"
                num8 = u"Ziffernblock 8"
                num9 = u"Ziffernblock 9"
                numAdd = u"Ziffernblock +"
                numDecimal = u"Ziffernblock Dezimaltrenner"
                numDivide = u"Ziffernblock /"
                numMultiply = u"Ziffernblock *"
                numSubtract = u"Ziffernblock -"
                pageDown = u"Bild runter"
                pageUp = u"Bild hoch"
                right = u"Pfeiltaste nach rechts"
                space = u"Leerschritt"
                up = u"Pfeiltaste nach oben"
                win = u"Windows Taste"
    class Mouse:
        name = u"Maus"
        class GoDirection:
            name = u"Starte Mausbewegung in eine Richtung"
            label = u"Starte Mausbewegung in Richtung %.2f°"
            text1 = u"Starte Mausbewegung in Richtung"
            text2 = u"Grad."
        class LeftButton:
            name = u"Linke Maustaste"
        class LeftDoubleClick:
            name = u"Linke Maustaste Doppelklick "
        class MiddleButton:
            name = u"Mittlere Maustaste"
        class MouseWheel:
            name = u"Drehe Mausrad"
            description = u"Emuliert Drehungen des Mausrades"
            label = u"Drehe Mausrad um %d Rastungen"
            text1 = u"Drehe Mausrad um"
            text2 = u"Rastungen. (Negative Werte drehen nach unten)"
        class MoveAbsolute:
            name = u"Setze Maus-Position"
            label = u"Bewege Maus nach x:%s, y:%s"
            text1 = u"Setze horizontale Position X:"
            text2 = u"Pixel"
            text3 = u"Setze vertikale Position Y:"
            text4 = u"Pixel"
        class RightButton:
            name = u"Rechte Maustaste"
        class RightDoubleClick:
            name = u"Rechte Maustaste Doppelklick"
        class ToggleLeftButton:
            name = u"Linke Maustaste umschalten"
    class FS20PCS:
        description = u"<rst>\nSenden von Befehlen an FS20 Empfänger.\n\n|\n\n|fS20Image|_\n\n`Zum Shop <http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=27743>`__\n\n.. |fS20Image| image:: picture.jpg\n.. _fS20Image: http://www.elv.de/\n"
        address = u"Adresse:"
        errorFind = u"ELV FS20 PCS wurde nicht gefunden"
        level = u"Stufe:"
        repeat = u"Wiederholungen:"
        repeatSuffix = u"{0} ({1} Wiederholungen)"
        timedActionDescription = u"Bietet zeitgesteuerte Kontrolle von FS20 Geräten"
        timedActionName = u"Zeitgesteuerte Aktionen"
        timerValue = u"Timerzeit:"
        class Dim:
            name = u"Dimmen"
            description = u"Dimmt sofort auf eine Helligkeitsstufe"
            labelFormat = u"Dimme {0} auf {1:.02f}%"
        class DimAlternating:
            name = u"Abwechselnd Herauf- bzw. Herunterdimmen"
            description = u"Heraufdimmen bis Maximum, Pause, Herabdimmen bis Minimum, Pause, usw."
            labelFormat = u"Dimme {0} abwechselnd herauf- bzw. herunter"
        class DimAlternatingOffTimer:
            name = u"Abwechselnd Herauf- bzw. Herunterdimmen und nach Timerzeit ausstellen"
            description = u"Dimme im Wechsel sofort eine Helligkeitsstufe herauf bzw. herab (bei langem Tastendruck mehrere Helligkeitsstufen herauf bis Maximum und nach kurzer Pause wieder herab bis Minimum usw. - solange Taste gedrückt wird) und schalte nach Timerzeit Aus (im Wechsel)"
            labelFormat = u"Dimme {0} abwechselnd herauf- bzw. herunter und schalte nach {1} aus"
        class DimDown:
            name = u"Herunterdimmen"
            description = u"Eine Helligkeitsstufe dunkler dimmen"
            labelFormat = u"Dimme {0} eine Helligkeitsstufe dunkler"
        class DimDownOffTimer:
            name = u"Herunterdimmen und nach Timerzeit abschalten"
            description = u"Eine Helligkeitsstufe dunkler dimmen und nach Timerzeit abschalten"
            labelFormat = u"Dimme {0} eine Helligkeitsstufe dunkler und schalte nach {1} aus"
        class DimTimer:
            name = u"In Timerzeit herunterdimmen"
            description = u"Dimmt in Timerzeit auf eine Helligkeitsstufe"
            labelFormat = u"Dimme {0} in {2} auf {1:.02f}%"
        class DimUp:
            name = u"Heraufdimmen"
            description = u"Eine Helligkeitsstufe heller dimmen"
            labelFormat = u"Dimme {0} eine Helligkeitsstufe heller"
        class DimUpOffTimer:
            name = u"Heraufdimmen und nach Timerzeit abschalten"
            description = u"Eine Helligkeitsstufe heller dimmen und nach Timerzeit ausschalten"
            labelFormat = u"Dimme {0} eine Helligkeitsstufe heller und schalte nach {1} aus"
        class Off:
            name = u"Ausschalten"
            description = u"Schaltet Gerät aus (dimmt auf 0%)"
            labelFormat = u"Schalte {0} aus"
        class OffPreviousValueInternal:
            name = u"Aus für interne Timerzeit, anschließend alter Wert"
            description = u"Aus (dimmt auf 0%) für interne Timerzeit, anschließend alter Wert"
            labelFormat = u"Schalte {0} für interne Timerzeit aus kehre anschließend auf alten Wert zurück"
        class OffPreviousValueTimer:
            name = u"Aus für Timerzeit, anschließend alter Wert"
            description = u"Aus (dimmt auf 0%) für Timerzeit, anschließend alter Wert"
            labelFormat = u"Schalte {0} für {1} aus kehre anschließend auf alten Wert zurück"
        class OffTimer:
            name = u"Aus in Timerzeit"
            description = u"Schaltet Gerät in Timerzeit aus (dimmt auf 0%)"
            labelFormat = u"Schalte {0} in {1} aus"
        class On:
            name = u"Anschalten"
            description = u"Schaltet Gerät ein (dimmt auf 100%)"
            labelFormat = u"Schalte {0} an"
        class OnOffInternal:
            name = u"Schalte Gerät für interne Timerzeit an (dimme auf 100%) und schalte anschließend ab"
            description = u"Schaltet Gerät für interne Timerzeit an (dimmt auf 100%) und schalte anschließend ab"
            labelFormat = u"Schalte {0} für interne Timerzeit an und schalte anschließend ab"
        class OnOffTimer:
            name = u"Schalte Gerät für Timerzeit an (dimme auf 100%) und schalte anschließend ab"
            description = u"Schaltet Gerät für Timerzeit an (dimmt auf 100%) und schalte anschließend ab"
            labelFormat = u"Schalte {0} für {0} an und schalte anschließend ab"
        class OnPreviousStateInternal:
            name = u"Schalte Gerät für interne Timerzeit an (dimme auf 100%) und kehre anschließend auf alten Zustand"
            description = u"Schaltet Gerät für interne Timerzeit an (dimmt auf 100%) und kehrt anschließend zum vorherigen Zustand zurück"
            labelFormat = u"Schalte {0} für interne Timerzeit an und kehre anschließend zum vorherigen Zustand zurück"
        class OnPreviousStateTimer:
            name = u"Schalte Gerät für Timerzeit an (dimme auf 100%) und kehre anschließend auf alten Zustand"
            description = u"Schaltet Gerät für Timerzeit an (dimmt auf 100%) und kehrt anschließend zum vorherigen Zustand zurück"
            labelFormat = u"Schalte {0} für {1} an und kehre anschließend zum vorherigen Zustand zurück"
        class OnTimer:
            name = u"An in Timerzeit"
            description = u"Schaltet Gerät für Timerzeit ein (dimmt auf 100%)"
            labelFormat = u"Schalte {0} für {1} an"
        class PreviousValue:
            name = u"Mit früherem Wert einschalten"
            description = u"Schaltet Gerät mit früherem Wert ein"
            labelFormat = u"Schalte {0} mit früherem Wert ein"
        class PreviousValueOffInternal:
            name = u"Mit früherem Wert für interne Timerzeit ein- und anschließend abschalten"
            description = u"Schaltet Gerät mit früherem Wertfür interne Timerzeit ein und anschließend ab"
            labelFormat = u"Schalte {0} mit früherem Wert für interne Timerzeit ein und anschließend ab"
        class PreviousValueOffTimer:
            name = u"Mit früherem Wert für Timerzeit ein- und anschließend abschalten"
            description = u"Schaltet Gerät mit früherem Wertfür Timerzeit ein und anschließend ab"
            labelFormat = u"Schalte {0} mit früherem Wert für {1} ein und anschließend ab"
        class PreviousValuePreviousStateInternal:
            name = u"Mit früherem Wert für interne Timerzeit einschalten und anschließend zu altem Zustand zurückkehren"
            description = u"Schaltet Gerät mit früherem Wert für interne Timerzeit ein und kehrt anschließend zu altem Zustand zurück"
            labelFormat = u"Schalte {0} mit früherem Wert für interne Timerzeit ein und kehre anschließend zu altem Zustand zurück"
        class PreviousValuePreviousStateTimer:
            name = u"Mit früherem Wert für Timerzeit einschalten und anschließend zu altem Zustand zurückkehren"
            description = u"Schaltet Gerät mit früherem Wert für Timerzeit ein und kehrt anschließend zu altem Zustand zurück"
            labelFormat = u"Schalte {0} mit früherem Wert für {1} ein und  kehre anschließend zu altem Zustand zurück"
        class PreviousValueTimer:
            name = u"In Timerzeit mit altem Wert einschalten"
            description = u"Schaltet Gerät in Timerzeit mit altem Wert ein"
            labelFormat = u"Schalte {0} in {1} mit altem Wert ein"
        class ProgramCode:
            name = u"Anlernen von Hauscode und Adresse"
            description = u"Lernt die Hauscode und Adresse ohne eine Aktion auszulösen."
            labelFormat = u"Adresse {0} anlernen"
        class ProgramDimDownRampTimer:
            name = u"Programmierung der internen Rampenzeit für Herabdimmen"
            description = u"Programmiert die interne Rampenzeit für Herabdimmen"
            labelFormat = u"Programmiere die internen Rampenzeit für Heraufdimmen von {0} auf {1}"
        class ProgramDimUpRampTimer:
            name = u"Programmierung der internen Rampenzeit für Heraufdimmen"
            description = u"Programmiert die interne Rampenzeit für Heraufdimmen"
            labelFormat = u"Programmiere die internen Rampenzeit für Herabdimmen von {0} auf {1}"
        class ProgramFactoryDefaults:
            name = u"Auf Auslieferzustand zurücksetzen"
            description = u"Setzt ein Gerät auf den Auslieferzustand zurück.\n(wird nicht von allen FS20-Empfänger unterstützt)"
            labelFormat = u"Setzt {0} auf Auslieferzustand zurück"
        class ProgramInternalTimer:
            name = u"Programmierung der internen Timerzeit"
            description = u"Programmiert die internen Timerzeit"
            labelFormat = u"Programmiere die interne Timerzeit von {0} auf {1}"
        class ProgramTimer:
            name = u"Programmierung der internen Timerzeit starten bzw. stoppen"
            description = u"Starte bzw. stoppt die Programmierung der internen Timerzeit"
            labelFormat = u"Starte bzw. stoppt die Programmierung der internen Timerzeit für {0}"
        class Toggle:
            name = u"Umschalten"
            description = u"Wechselt zwischen „Aus“ und „An, alter Wert“"
            labelFormat = u"Wechsle {0} zwischen aus und vorherigem Wert"
        class ToggleTimer:
            name = u"Umschalten nach Timerzeit"
            description = u"Wechselt in Timerzeit zwischen „Aus“ und „An, alter Wert“"
            labelFormat = u"Wechsle {0} zwischen aus und vorherigem Wert in {1}"
    class Joystick:
        name = u"Joystick"
        description = u"Dieses Plugin erlaubt es Joysticks und Gamepads als Ereignisquelle zu verwenden."
    class Keyboard:
        name = u"Tastatur"
        description = u"Dieses Plugin generiert Ereignisse bei Tastendruck (Hotkey)."
    class MediaPlayerClassic:
        name = u"Media Player Classic"
        description = u'Fügt Aktionen zur Steuerung des <a href="http://sourceforge.net/projects/guliverkli/">Media Player Classic</a> hinzu'
        class AlwaysOnTop:
            name = u"Immer im Vordergrund"
        class AudioDelayAdd10ms:
            name = u"Audio Verzögerung +10ms"
        class AudioDelaySub10ms:
            name = u"Audio Verzögerung -10ms"
        class BossKey:
            name = u"Boss-Taste"
        class Close:
            name = u"Datei schliessen"
        class DVDAngleMenu:
            name = u"DVD Blickwinkel-Menü"
        class DVDAudioMenu:
            name = u"DVD Audio-Menü"
        class DVDChapterMenu:
            name = u"DVD Kapitel-Menü"
        class DVDMenuActivate:
            name = u"DVD Menü aktivieren"
        class DVDMenuBack:
            name = u"DVD Menü zurück"
        class DVDMenuDown:
            name = u"DVD Menü runter"
        class DVDMenuLeave:
            name = u"DVD Menü verlassen"
        class DVDMenuLeft:
            name = u"DVD Menü links"
        class DVDMenuRight:
            name = u"DVD Menü rechts"
        class DVDMenuUp:
            name = u"DVD Menü hoch"
        class DVDNextAngle:
            name = u"DVD Blickwinkel vorwärts"
        class DVDNextAudio:
            name = u"DVD Audio vorwärts"
        class DVDNextSubtitle:
            name = u"DVD Untertitel vorwärts"
        class DVDOnOffSubtitle:
            name = u"DVD Untertitel An/Aus"
        class DVDPrevAngle:
            name = u"DVD Blickwinkel zurück"
        class DVDPrevAudio:
            name = u"DVD Audio zurück"
        class DVDPrevSubtitle:
            name = u"DVD Untertitel zurück"
        class DVDRootMenu:
            name = u"DVD Root-Menü"
        class DVDSubtitleMenu:
            name = u"DVD Untertitel-Menü"
        class DVDTitleMenu:
            name = u"DVD Titel-Menü"
        class DecreaseRate:
            name = u"Geschwindigkeit verringern"
        class Exit:
            name = u"Anwendung beenden"
        class FiltersMenu:
            name = u"Filter Menü"
        class FrameStep:
            name = u"Einzelbild vorwärts"
        class FrameStepBack:
            name = u"Einzelbild zurück"
        class Fullscreen:
            name = u"Vollbild"
        class FullscreenWOR:
            name = u"Vollbild (w/o res.change)"
        class GoTo:
            name = u"Gehe zu"
        class GroupDvdControls:
            name = u"DVD Steuerung"
        class GroupExtendedControls:
            name = u"Erweiterte Steuerung"
        class GroupMainControls:
            name = u"Main Steuerung"
        class GroupViewModes:
            name = u"Ansichten Steuerung"
        class IncreaseRate:
            name = u"Geschwindigkeit erhöhen"
        class JumpBackwardKeyframe:
            name = u"Rückwärts springen (Keyframe)"
        class JumpBackwardLarge:
            name = u"Rückwärts springen (viel)"
        class JumpBackwardMedium:
            name = u"Rückwärts springen (mittel)"
        class JumpBackwardSmall:
            name = u"Rückwärts springen (gering)"
        class JumpForwardKeyframe:
            name = u"Vorwärts springen (Keyframe)"
        class JumpForwardLarge:
            name = u"Vorwärts springen (viel)"
        class JumpForwardMedium:
            name = u"Vorwärts springen (mittel)"
        class JumpForwardSmall:
            name = u"Vorwärts springen (gering)"
        class LoadSubTitle:
            name = u"Untertitel laden"
        class Next:
            name = u"Vorwärts"
        class NextAudio:
            name = u"Audio vorwärts"
        class NextAudioOGM:
            name = u"Audio vorwärts OGM"
        class NextPlaylistItem:
            name = u"Playlisten Eintrag vorwärts"
        class NextSubtitle:
            name = u"Untertitel vorwärts"
        class NextSubtitleOGM:
            name = u"Untertitel vorwärts OGM"
        class OnOffSubtitle:
            name = u"Untertitel An/Aus"
        class OpenDVD:
            name = u"DVD öffnen"
        class OpenDevice:
            name = u"Gerät öffnen"
        class OpenFile:
            name = u"Datei öffnen"
        class Options:
            name = u"Optionen"
        class Pause:
            name = u"Pause"
        class Play:
            name = u"Wiedergabe"
        class PlayPause:
            name = u"Wiedergabe/Pause"
        class PlayerMenuLong:
            name = u"Player Menü (lang)"
        class PlayerMenuShort:
            name = u"Player Menü (kurz)"
        class PnSCenter:
            name = u"Pan & Scan zentrieren"
        class PnSDecHeight:
            name = u"Pan & Scan Decrease Höhe"
        class PnSDecSize:
            name = u"Pan & Scan Decrease Größe"
        class PnSDecWidth:
            name = u"Pan & Scan Decrease Breite"
        class PnSDown:
            name = u"Pan & Scan runter"
        class PnSDownLeft:
            name = u"Pan & Scan runter/links"
        class PnSDownRight:
            name = u"Pan & Scan runter/rechts"
        class PnSIncHeight:
            name = u"Pan & Scan Increase Höhe"
        class PnSIncSize:
            name = u"Pan & Scan Increase Größe"
        class PnSIncWidth:
            name = u"Pan & Scan Increase Breite"
        class PnSLeft:
            name = u"Pan & Scan links"
        class PnSReset:
            name = u"Pan & Scan Reset"
        class PnSRight:
            name = u"Pan & Scan rechts"
        class PnSRotateAddX:
            name = u"Pan & Scan Rotate X+"
        class PnSRotateAddY:
            name = u"Pan & Scan Rotate Y+"
        class PnSRotateAddZ:
            name = u"Pan & Scan Rotate Z+"
        class PnSRotateSubX:
            name = u"Pan & Scan Rotate X-"
        class PnSRotateSubZ:
            name = u"Pan & Scan Rotate Z-"
        class PnSUp:
            name = u"Pan & Scan hoch"
        class PnSUpLeft:
            name = u"Pan & Scan hoch/links"
        class PnSUpRight:
            name = u"Pan & Scan hoch/rechts"
        class PnsRotateSubY:
            name = u"Pan & Scan Rotate Y-"
        class PrevAudio:
            name = u"Audio zurück"
        class PrevAudioOGM:
            name = u"Audio zurück OGM"
        class PrevSubtitle:
            name = u"Untertitel zurück"
        class PrevSubtitleOGM:
            name = u"Untertitel zurück OGM"
        class Previous:
            name = u"Zurück"
        class PreviousPlaylistItem:
            name = u"Playlisten Eintrag zurück"
        class Properties:
            name = u"Eigenschaften"
        class QuickOpen:
            name = u"Schnelles Datei öffnen"
        class ReloadSubtitles:
            name = u"Untertitel erneut laden"
        class ResetRate:
            name = u"Geschwindigkeit zurücksetzen"
        class SaveAs:
            name = u"Speichern als"
        class SaveImage:
            name = u"Bild speichern"
        class SaveImageAuto:
            name = u"Bild speichern (auto)"
        class SaveSubtitle:
            name = u"Untertitel speichern"
        class Stop:
            name = u"Stopp"
        class ToggleCaptionMenu:
            name = u"Toggle Caption Menu"
        class ToggleCaptureBar:
            name = u"Toggle Capture Bar"
        class ToggleControls:
            name = u"Toggle Controls"
        class ToggleInformation:
            name = u"Toggle Information"
        class TogglePlaylistBar:
            name = u"Toggle Playlist Bar"
        class ToggleSeeker:
            name = u"Toggle Seeker"
        class ToggleShaderEditorBar:
            name = u"Toggle Shader Editor Bar"
        class ToggleStatistics:
            name = u"Toggle Statistics"
        class ToggleStatus:
            name = u"Toggle Status"
        class ToggleSubresyncBar:
            name = u"Toggle Subresync Bar"
        class VidFrmDouble:
            name = u"Video Frame doppelt"
        class VidFrmHalf:
            name = u"Video Frame halb"
        class VidFrmInside:
            name = u"Video Frame Inside"
        class VidFrmNormal:
            name = u"Video Frame normal"
        class VidFrmOutside:
            name = u"Video Frame Outside"
        class VidFrmStretch:
            name = u"Video Frame Stretch"
        class ViewCompact:
            name = u"Anzeige Kompakt"
        class ViewMinimal:
            name = u"Anzeige Minimal"
        class ViewNormal:
            name = u"Anzeige Normal"
        class VolumeDown:
            name = u"Lautstärke leiser"
        class VolumeMute:
            name = u"Lautstärke Stummschaltung"
        class VolumeUp:
            name = u"Lautstärke lauter"
        class Zoom100:
            name = u"Zoom 100%"
        class Zoom200:
            name = u"Zoom 200%"
        class Zoom50:
            name = u"Zoom 50%"
    class NetworkReceiver:
        name = u"Netzwerk Ereignis Empfänger"
        description = u'Empfängt Ereignisse von einem "Netzwerk Ereignis Sender" Plugin.'
        eventPrefix = u"Ereignis Prefix:"
        password = u"Passwort:"
        port = u"Port:"
    class NetworkSender:
        name = u"Netzwerk Ereignis Sender"
        description = u'Sendet Ereignisse zu einem "Netzwerk Ereignis Empfänger" Plugin über das TCP/IP Protokoll.'
        password = u"Passwort:"
        securityBox = u"Sicherheit"
        tcpBox = u"TCP/IP Einstellungen"
    class Serial:
        name = u"Serieller Anschluss"
        description = u"Allgemeine Kommunikation über einen seriellen Anschluss."
        baudrate = u"Bits pro Sekunde:"
        bytesize = u"Datenbits:"
        encoding = u"Zeichenkodierung:"
        eventPrefix = u"Ereignis-Prefix"
        flowcontrol = u"Flusssteuerung:"
        generateEvents = u"Generiere Ereignisse bei eintreffenden Daten"
        handshakes = [
            u"Keine",
            u"Xon / Xoff",
            u"Hardware",
        ]
        parities = [
            u"Keine",
            u"Ungerade",
            u"Gerade",
        ]
        parity = u"Parität:"
        port = u"Anschluss:"
        stopbits = u"Stopbits:"
        terminator = u"Endzeichen:"
        class Read:
            name = u"Lese"
            read_all = u"Lese soviele Zeichen wie momentan verfügbar sind."
            read_some = u"Lese genau diese Anzahl an Zeichen:"
            read_time = u"und warte maximal diese Anzahl an Millisekunden auf sie:"
        class Write:
            name = u"Sende"
    class Speech:
        name = u"Sprachausgabe"
        description = u"Verwendet die Microsoft Speech API (SAPI) um Texte in Sprache zu wandeln."
        class TextToSpeech:
            name = u"Text in Sprache"
            description = u"Verwendet die Microsoft Speech API (SAPI) um Texte in Sprache zu wandeln."
            buttonInsertDate = u"Datum einfügen"
            buttonInsertTime = u"Zeit einfügen"
            errorCreate = u"Kann Sprachobjekt nicht herstellen"
            errorNoVoice = u"Die Stimme mit dem Namen %s ist nicht verfügbar"
            fast = u"Schnell"
            label = u"Spreche: %s"
            labelRate = u"Geschwindigkeit:"
            labelVoice = u"Stimme:"
            labelVolume = u"Lautstärke:"
            loud = u"Laut"
            normal = u"Normal"
            silent = u"Leise"
            slow = u"Langsam"
            textBoxLabel = u"Text"
            voiceProperties = u"Spracheigenschaften"
    class SysTrayMenu:
        name = u"System Tray Menü"
        description = u"Ermöglicht es das Tray-Menü von EventGhost um eigene Menü-Einträge zu erweitern."
        addBox = u"Hinzufügen:"
        addItemButton = u"Menüeintrag"
        addSeparatorButton = u"Trennlinie"
        deleteButton = u"Entfernen"
        editEvent = u"Ereignis:"
        editLabel = u"Beschriftung:"
        eventHeader = u"Ereignis"
        labelHeader = u"Beschriftung"
        unnamedEvent = u"Ereignis%s"
        unnamedLabel = u"Neuer Menü-Eintrag %s"
    class TestPatterns:
        name = u"Testbild"
        description = u"Ermöglicht die Anzeige einer Reihe von Testbildern."
        aspectRatio = u"Seitenverhältnis:"
        aspectRatios = [
            u"1:1 Pixel-Zuordnung",
            u"4:3 Vollbild",
            u"16:9 Vollbild",
            u"4:3 Vollbild nach ITU-R BT.601 PAL",
            u"16:9 Vollbild nach ITU-R BT.601 PAL",
        ]
        backgroundColour = u"Hintergrundfarbe:"
        coverage = u"Abdeckung (Prozent):"
        display = u"Bildschirm:"
        dotDiameter = u"Durchmesser:"
        firstColour = u"Erste Farbe:"
        foregroundColour = u"Vordergrundfarbe:"
        lastColour = u"Letzte Farbe:"
        lineSize = u"Linienstärke:"
        makeDoubleBars = u"Doppelte Balken"
        numElements = u"Elementanzahl:"
        numHorizontalElements = u"Anzahl horizontaler Elemente:"
        numVerticalElements = u"Anzahl vertikaler Elemente:"
        numberFont = u"Nummer Zeichensatz:"
        orientation = u"Ausrichtung:"
        orientations = [
            u"horizontal",
            u"vertical",
        ]
        radius1 = u"Radius:"
        radius2 = u"% (0=ganzer Bildschirm)"
        secondColour = u"Zweite Farbe:"
        showNumbers = u"Zeige Nummern"
        useAntiAlias = u"Verwende Anti-Aliasing"
        class Bars:
            name = u"Balken"
        class Checkerboard:
            name = u"Schachbrett"
        class Close:
            name = u"Schließen"
        class Dots:
            name = u"Punkte"
        class Focus:
            name = u"Fokus"
        class Geometry:
            name = u"Geometrie"
        class Grid:
            name = u"Gitter"
        class IreWindow:
            name = u"IRE Fenster"
        class Lines:
            name = u"Linien"
        class SetDisplay:
            name = u"Anzeige setzen"
        class SiemensStar:
            name = u"Siemensstern"
    class USBRFID:
        description = u"<rst>\nEmpfängt Codes ELV USB/RFID-Interface.\n\n|\n\n|productImage|_\n\n`Direct shop link <http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=28049>`__\n\n.. |productImage| image:: picture.jpg\n.. _productImage: http://www.elv.de/ "
        duration = u"Dauer"
        errorFind = u"USB/RFID-Interface wurde nicht gefunden"
        class Buzzer:
            name = u"Piepton"
            description = u"Piepton einschalten"
            labelFormat = u"Piepton für {0}0 ms einschalten"
        class GreenLED:
            name = u"Grüne LED"
            description = u"Grüne LED einschalten"
            labelFormat = u"Grüne LED für {0}0 ms einschalten"
        class RedLED:
            name = u"Rote LED"
            description = u"Rote LED einschalten"
            labelFormat = u"Rote LED für {0}0 ms einschalten"
    class USB_UIRT:
        name = u"USB-UIRT"
        blinkRx = u"Blinke bei Empfang"
        blinkTx = u"Blinke beim Senden"
        irReception = u"IR Empfang"
        legacyCodes = u"Generiere UIRT2-kompatible Ereignisse"
        notFound = u"<unbekannt>"
        redIndicator = u"Funktion der roten Anzeige-LED"
        stopCodes = u"Akzeptiere kurze Wiederholsequenzen als fortdauernde Ereignisse"
        uuFirmDate = u"Firmware Datum: "
        uuFirmVersion = u"Firmware Version: "
        uuInfo = u"USB-UIRT Information"
        uuProtocol = u"Protokoll Version: "
        class TransmitIR:
            name = u"Sende IR"
            description = u"Sendet eine IR-Code durch das USB-UIRT Gerät."
            infinite = u"unendlich"
            irCode = u"IR-Code:"
            learnButton = u"Lerne IR-Code..."
            repeatCount = u"Wiederholungen:"
            wait1 = u"Warte auf:"
            wait2 = u"ms IR Inaktivität vor Aussendung"
            zone = u"Zone:"
            zoneChoices = (
                u"Alle",
                u"Anschlussbuchse R-Kontakt",
                u"Anschlussbuchse L-Kontakt",
                u"Interner Sender",
            )
            class LearnDialog:
                acceptBurstButton = u"Akzeptiere Signalfolge"
                forceRaw = u"Lernen im RAW-Modus erzwingen"
                frequency = u"Frequenz"
                helpText = u"1. Lassen Sie die Fernbedienung aus einer \nEntfernung von ungefähr 15 cm (oder auch weniger)\nauf die Vorderseite des USB-UIRT zeigen.\n\n2. DRÜCKEN und HALTEN Sie die gewünschte Taste\nder Fernbedienung, bis das Lernen abgeschlossen ist.\n"
                progress = u"Lern-Fortschritt"
                signalQuality = u"Signal"
                title = u"Lerne IR-Code"
    class Webserver:
        name = u"Webserver"
        description = u"Ein kleiner Webserver, mit dem Ereignisse durch HTML-Webseiten generiert werden können."
        documentRoot = u"Datenverzeichnis:"
        eventPrefix = u"Ereignis Prefix:"
        port = u"TCP/IP Port:"
    class X10:
        name = u"X10 Fernbedienung"
        description = u"<rst>\nPlugin für X10 kompatible Funkfernbedienungen.\n\nDies beinhaltet Fernbedienungen wie:\n\n* `ATI Remote Wonder \n  <http://www.ati.com/products/remotewonder/index.html>`_\n* `ATI Remote Wonder PLUS \n  <http://www.ati.com/products/remotewonderplus/index.html>`_\n* `SnapStream Firefly \n  <http://www.snapstream.com/products/firefly/>`_\n* `NVIDIA Personal Cinema Remote \n  <http://www.nvidia.com/object/feature_PC_remote.html>`_\n* `Marmitek PC Control \n  <http://www.marmitek.com/>`_\n* `Pearl Q-Sonic Master Remote 6in1 \n  <http://www.pearl.de/product.jsp?pdid=PE4444&catid=1601&vid=916&curr=DEM>`_\n* `Niveus PC Remote Control \n  <http://www.niveusmedia.com/>`_\n* Medion RF Remote Control\n* Packard Bell RF MCE Remote Control OR32E\n"
        allButton = u"&Alle"
        errorMesg = u"Kein X10 Empfänger gefunden!"
        idBox = u"Aktivierte IDs:"
        noneButton = u"&Keine"
        remoteBox = u"Fernbedienungstyp:"
        usePrefix = u"Ereignis-Prefix:"
