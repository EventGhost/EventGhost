# -*- coding: UTF-8 -*-
class General:
    apply = u"Toepassen"
    autostartItem = u"Automatisch Starten"
    browse = u"Bladeren"
    cancel = u"Annuleren"
    choose = u"Kiezen"
    configTree = u"Configuratie Boom"
    deleteLinkedItems = u"Ten minste 1 element buiten je selectie, verwijst naar een element in je selectie. Als je doorgaat met deze selectie te verwijderen zal het verwijzende element niet goed meer werken.\n\nBen je zeker dat je deze selectie wenst te verwijderen?"
    deleteManyQuestion = u"Dit element heeft %s onderliggende elementen.\nBen je zeker dat je ze allemaal wenst te verwijderen?"
    deletePlugin = u"Deze invoegtoepassing is in gebruik door acties in je configuratie.\nJe kan het niet verwijderen zolang er acties zijn die deze invoegtoepassing gebruiken."
    deleteQuestion = u"Ben je zeker dat je dit element wenst te verwijderen?"
    help = u"&Help"
    moreTag = u"meer..."
    noOptionsAction = u"Deze actie heeft geen configureerbare opties."
    noOptionsPlugin = u"Deze invoegtoepassing heeft geen opties om in te stellen."
    ok = u"OK"
    pluginLabel = u"Invoegtoepassing: %s"
    test = u"&Test"
    unnamedEvent = u"<onbenoemde gebeurtenis>"
    unnamedFile = u"<onbenoemd bestand>"
    unnamedFolder = u"<onbenoemde Map>"
    unnamedMacro = u"<onbenoemde Makro>"
class MainFrame:
    onlyLogAssigned = u"&Log enkel toegewezen en geactiveerde gebeurtenissen."
    class Logger:
        caption = u"Log"
        descriptionHeader = u"Beschrijving"
        timeHeader = u"Tijd"
        welcomeText = u"---> Welkom bij EventGhost <---"
    class Menu:
        About = u"&Over EventGhost..."
        AddAction = u"Actie Toevoegen"
        AddEvent = u"Gebeurtenis Toevoegen"
        AddFolder = u"Map Toevoegen"
        AddMacro = u"Makro Toevoegen"
        AddPlugin = u"Invoegtoepassing Toevoegen"
        Apply = u"&Wijzigingen Toepassen"
        CheckUpdate = u"Controleren op nieuwe versies..."
        ClearLog = u"Wis Log"
        Close = u"&Sluiten"
        CollapseAll = u"Alles &Toeklappen"
        ConfigurationMenu = u"&Configuratie"
        Configure = u"Configureer Element"
        Copy = u"&Kopiëren"
        Cut = u"&Knippen"
        Delete = u"&Wissen"
        Disabled = u"Element Uitschakelen"
        EditMenu = u"&Bewerken"
        Execute = u"Uitvoeren Element"
        Exit = u"&Sluiten"
        ExpandAll = u"Alles &Openklappen"
        ExpandOnEvents = u"Autom. markeren bij gebeurtenis"
        ExpandTillMacro = u"Autom. uitklappen enkel tot Makro"
        Export = u"Exporteren..."
        FileMenu = u"&Bestand"
        Find = u"&Zoeken"
        FindNext = u"Zoek &Volgende"
        HelpMenu = u"&Help"
        HideShowToolbar = u"Werkbalk"
        Import = u"Importeer..."
        LogActions = u"Log Acties"
        LogMacros = u"Log Makros"
        LogTime = u"Log Tijd"
        New = u"&Nieuw"
        Open = u"&Openen..."
        Options = u"&Opties..."
        Paste = u"&Plakken"
        Redo = u"&Opnieuw"
        Rename = u"Naam wijzigen"
        Reset = u"Reset"
        Save = u"&Opslaan"
        SaveAs = u"Opslaan &Als..."
        SelectAll = u"&Alles Selecteren"
        Undo = u"&Ongedaan Maken"
        ViewMenu = u"Weergave"
        WebForum = u"Ondersteunings Forum"
        WebHomepage = u"Thuis Pagina"
        WebWiki = u"Wiki"
    class SaveChanges:
        mesg = u"Het bestand werd gewijzigd.\n\nWenst u de wijzigingen op te slaan?"
        title = u"Wijzigingen opslaan?"
    class TaskBarMenu:
        Exit = u"&Sluiten"
        Hide = u"Verberg EventGhost"
        Show = u"Toon EventGhost"
    class Tree:
        caption = u"Configuratie"
class Error:
    FileNotFound = u'Bestand "%s" kon niet worden gevonden.'
    InAction = u'Fout in Actie: "%s"'
    configureError = u"Fout gedurende configuratie: %s"
    pluginLoadError = u"Fout gedurende laden van invoegtoepassing %s."
    pluginNotActivated = u'Invoegtoepassing "%s" is niet geactiveerd'
    pluginStartError = u"Fout tijdens opstarten Invoegtoepassing: %s"
class Exceptions:
    DeviceInitFailed = u"Initialisatie Apparaat Mislukt!"
    DeviceNotFound = u"Apparaat niet gevonden!"
    DeviceNotReady = u"Apparaat niet klaar!"
    DriverNotFound = u"Driver niet gevonden!"
    DriverNotOpen = u"Driver kon niet worden geopend!"
    InitFailed = u"Initialisatie Mislukt!"
    PluginNotFound = u"Invoegtoepassing niet gevonden!"
    ProgramNotFound = u"Applicatie niet gevonden!"
    ProgramNotRunning = u"Applicatie is niet aan het uitvoeren!"
    SerialOpenFailed = u"Kan de seriële poort niet openen!"
class CheckUpdate:
    ManErrorMesg = u"Het was niet mogelijk de informatie van de EventGhost website te halen.\n\nProbeer later opnieuw a.u.b."
    ManErrorTitle = u"Fout tijdens het controleren op nieuwere versies."
    ManOkMesg = u"Deze versie van EventGhost is de nieuwste."
    ManOkTitle = u"Geen nieuwere versie beschikbaar."
    downloadButton = u"Ga naar Download Pagina"
    newVersionMesg = u"Een nieuwere versie van EventGhost is beschikbaar.\n\n             Jouw Versie :            %s\n             Laatste Versie :        %s\n\nWens je de download pagina te bezoeken ?"
    title = u"Nieuwe EventGhost versie beschikbaar..."
    waitMesg = u"Gelieve te wachten terwijl EventGhost de update informatie verzamelt."
class AddActionDialog:
    descriptionLabel = u"Beschrijving"
    title = u"Selecteer een actie om toe te voegen..."
class AddPluginDialog:
    author = u"Auteur:"
    descriptionBox = u"Beschrijving"
    externalPlugins = u"Externe Invoegtoepassing"
    noInfo = u"Geen Info beschikbaar."
    noMultiload = u"Deze Invoeg toepassing ondersteunt niet om meerdere malen te worden opgeladen en er is reeds een instantie in je configuratie aanwezig."
    noMultiloadTitle = u"Geen meermaals laden mogelijk."
    otherPlugins = u"Andere"
    programPlugins = u"Programma Besturing"
    remotePlugins = u"Afstandsbediening"
    title = u"Kies een Invoegtoepassing om toe te voegen..."
    version = u"Versie:"
class AddActionGroupDialog:
    caption = u"Acties toevoegen?"
    message = u"Eventghost kan een Map met alle acties voor deze Invoegtoepassing in uw configuratie toevoegen. Indien je dat wenst, selecteer eerst de lokatie waar het moet worden toegevoegd en druk dan op OK.\n\nIndien niet, druk op Cancel."
class OptionsDialog:
    CheckUpdate = u"Controleer op nieuwere versies bij het opstarten."
    HideOnClose = u"Zend naar systeemlade bij het afsluiten."
    HideOnStartup = u"Verbergen bij het opstarten."
    LanguageGroup = u"Taal"
    StartGroup = u"Bij Start"
    StartWithWindows = u"Opstarten als Windows start."
    Tab1 = u"Algemeen"
    Title = u"Opties"
    UseAutoloadFile = u"Bestand vanzelf laden"
    Warning = u"Taal veranderingen worden pas zichtbaar na een herstart van de applicatie."
    confirmDelete = u"Bevestig verwijderen van de boom elementen."
    limitMemory1 = u"Bespaar geheugenverbruik tijdens minimaliseren."
    limitMemory2 = u"MB"
class FindDialog:
    caseSensitive = u"&Hoofdlettergevoelig"
    direction = u"Richting"
    down = u"&Neerwaarts"
    findButton = u"&Zoek Volgende"
    notFoundMesg = u'"%s" kon niet worden gevonden.'
    searchLabel = u"Zoek:"
    searchParameters = u"Zoek ook in actie parameters"
    title = u"Zoeken"
    up = u"&Opwaarts"
    wholeWordsOnly = u"Enkel op het volledige woord zoeken"
class AboutDialog:
    Author = u"Auteur: %s"
    CreationDate = u"%a, %d %b %Y %H:%M:%S"
    Title = u"Over EventGhost"
    Version = u"Versie: %s (compilatie %s)"
    tabAbout = u"Over"
    tabChangelog = u"Versie wijzigingen"
    tabLicense = u"Licentie Overeenkomst"
    tabSpecialThanks = u"Speciale Dank"
    tabSystemInfo = u"Systeem Informatie"
class Plugin:
    class EventGhost:
        name = u"EventGhost"
        description = u"Hier vind je acties die hoofdzakelijk de kernfunctionaliteit van EventGhost controleren."
        class AutoRepeat:
            name = u"Herhaal vanzelf huidige macro"
            description = u"Verandert de makro waar dit commando wordt toegevoegd in een zelf herhalende macro."
            seconds = u"seconden"
            text1 = u"Eerste herhaling starten na"
            text2 = u"met één herhaling elke"
            text3 = u"verhoog de herhaling de volgende"
            text4 = u"tot één herhaling elke"
        class Comment:
            name = u"Opmerking"
            description = u"Gewoon een doe-niets actie die kan gebruikt worden om een opmerking in uw configuratie toe te voegen."
        class DisableItem:
            name = u"Schakel een element uit"
            description = u"Schakel een element uit"
            label = u"Uitschakelen: %s"
            text1 = u"Selecteer het uit te schakelen element:"
        class EnableExclusive:
            name = u"Schakel exclusief een element aan"
            description = u"Dit schakelt een specifieke map of makro in uw configuratie aan, maar schakelt ook alle andere broer/zuster mappen en makros uit, die in dezelfde hoogte in de boom hangen."
            label = u"Schakel exclusief aan: %s"
            text1 = u"Selecteer het exclusief aan te schakelen element:"
        class EnableItem:
            name = u"Schakel een element aan"
            description = u"Schakel een element aan"
            label = u"Schakel aan: %s"
            text1 = u"Selecteer het aan te schakelen element:"
        class FlushEvents:
            name = u"Wis uitstaande gebeurtenissen"
            description = u'De "Wis Uitstaande Gebeurtenissen" wist alle onverwerkte gebeurtenissen die momenteel in de wachtrij om te verwerken zitten.\n\n<p>Het is nuttig in het geval een makro een lange uitvoeringsduur heeft en er ondertussen gebeurtenissen in de wachtrij zitten die niet meer verwerkt hoeven te worden.<p><b>Voorbeeld:</b> U heeft een lange "Start Systeem" makro die 90 seconden duurt om te verwerken. De gebruiker zal niets merken tot de projector oplicht, welke 60 seconden duurt. Het is te verwachten dat de gebruiker verschillende keren de afstandsbedieningsknop gebruikt die dan deze makro verschillende keren probeert uit te voeren en dus de lange wachttijd opnieuw teweeg brengt. Als je een "Wis Uitstaande Gebeurtenissen" makro aan het einde toevoegt, zullen de afstandsbedieningsknopdrukken die te veel zijn, verworpen worden.'
        class JumpIf:
            name = u"Spring als"
            description = u"Springt naar een andere makro, als de gespecifieerde python-evaluatie waar is."
            label1 = u"Als %s ga naar %s"
            label2 = u"Als %s ga langs %s"
            mesg1 = u"Selecteer de makro..."
            mesg2 = u"Gelieve de makro te selecteren die moet worden uitgevoerd indien de conditie waar is."
            text1 = u"Als:"
            text2 = u"Ga Naar:"
            text3 = u"Keer terug na uitvoering"
        class JumpIfLongPress:
            name = u"Spring als langdurig gedrukt"
            description = u"Springt naar een andere makro, als de knop op de afstandsbediening langer dan de geconfigureerde tijd werd ingedrukt."
            label = u"Als de knop %s seconden werd ingedrukt, ga naar: %s"
            text1 = u"Als de knop langer werd ingedrukt dan"
            text2 = u"seconden,"
            text3 = u"spring naar:"
            text4 = u"Selecteer de lange druk makro..."
            text5 = u"Gelieve de makro te selecteren, die moet worden uitgevoerd als de gebeurtenis een lange gebeurtenis is."
        class NewJumpIf:
            name = u"Spring"
            description = u"Spring naar een andere makro, als de opgegeven conditie vervuld is."
            choices = [
                u"laatste actie succesvol was ",
                u"laatste actie onsuccesvol was",
                u"altijd",
            ]
            labels = [
                u'Indien succesvol spring naar "%s"',
                u'Indien onsuccesvol spring naar "%s"',
                u'Spring naar "%s"',
                u'Indien succesvol spring naar "%s" en keer terug',
                u'Indien onsuccesvol spring naar "%s" en keer terug',
                u'Spring naar "%s" en keer terug',
            ]
            mesg1 = u"Selecteer de makro..."
            mesg2 = u"Gelieve de makro te selecteren die moet worden uitgevoerd als de conditie is vervuld."
            text1 = u"Als:"
            text2 = u"Spring Naar:"
            text3 = u"en keer terug na uitvoering."
        class PythonCommand:
            name = u"Python Opdracht"
            description = u"Voert één Python opdracht uit."
            parameterDescription = u"Python Opdracht:"
        class PythonScript:
            name = u"Python Script"
            description = u"Voert volledig functionerend Python script uit."
        class ShowOSD:
            name = u"Toon OSD"
            description = u"Toont een eenvoudige tekst op het scherm"
            alignment = u"Uitlijning:"
            alignmentChoices = [
                u"Boven Links",
                u"Boven Rechts",
                u"Onder Links",
                u"Onder Rechts",
                u"Scherm Centrum",
                u"Onderaan Centrum",
                u"Boven Centrum",
                u"Links Centrum",
                u"Rechts Centrum",
            ]
            display = u"Toont op scherm:"
            editText = u"Te tonen Tekst :"
            label = u"Toon OSD: %s"
            osdColour = u"Tekst kleur:"
            osdFont = u"Tekst Lettertype:"
            outlineFont = u"omlijn OSD:"
            skin = u"Gebruik 'Skin'"
            wait1 = u"Verberg OSD na"
            wait2 = u"seconden (0 = nooit)"
            xOffset = u"Horizontale verschuiving X: "
            yOffset = u"Verticale verschuiving Y: "
        class StopIf:
            name = u"Stop als"
            description = u"Stopt een makro uit te voeren, als de opgegeven Python-evaluatie waar is."
            label = u"Stop als %s"
            parameterDescription = u"Python conditie:"
        class StopProcessing:
            name = u"Stop deze gebeurtenis te verwerken"
            description = u"Na deze actie zal EventGhost niet langer zoeken naar makros die met deze momenteel uit aan het voeren gebeurtenis overeenkomen."
        class TriggerEvent:
            name = u"Genereer Gebeurtenis"
            description = u"Zorgt er voor dat een gebeurtenis wordt gegenereerd (optioneel na enige tijd)"
            labelWithTime = u'Genereer gebeurtenis "%s" na %.2f seconden'
            labelWithoutTime = u'Genereer gebeurtenis "%s"'
            text1 = u"Genereer Gebeurtenis string :"
            text2 = u"Vertraag de generatie met:"
            text3 = u"seconden. (0 = onmiddelijk)"
        class Wait:
            name = u"Wacht enige tijd"
            description = u"Wacht enige tijd"
            label = u"Wacht: %s sec"
            seconds = u"seconden"
            wait = u"Wacht"
    class System:
        name = u"Systeem"
        description = u"Controleert verschillende aspecten van je systeem, zoals geluidskaart, grafische kaart, voedingsbeheer, etc."
        forced = u"Geforceerd: %s"
        forcedCB = u"Geforceerd sluiten van alle programmas"
        class ChangeDisplaySettings:
            name = u"Verander Scherm Instellingen"
            description = u"Verander Scherm Instellingen"
            colourDepth = u"Kleur Diepte:"
            display = u"Scherm:"
            frequency = u"Frequentie:"
            includeAll = u"Voeg schermconfiguraties die deze Monitor niet ondersteunt ook toe."
            label = u"Configureer Scherm%d in configuratie %dx%d@%d Hz"
            resolution = u"Resolutie:"
            storeInRegistry = u"Sla configuratie in Windows Register op."
        class ChangeMasterVolumeBy:
            name = u"Verander Hoofd Volume"
            description = u"Verandert hoofdvolume relatief t.o.v. huidige waarde."
            text1 = u"Verandert hoofdvolume met"
            text2 = u"percent."
        class Execute:
            name = u"Start Toepassing"
            description = u"Start een *.exe bestand"
            FilePath = u"Bestandspad naar *.exe:"
            Parameters = u"Commando lijn opties:"
            ProcessOptions = (
                u"Ware tijd",
                u"Boven normaal",
                u"Normaal",
                u"onder normaal",
                u"inactief",
            )
            ProcessOptionsDesc = u"Process prioriteit:"
            WaitCheckbox = u"Wachten tot toepassing is beëindigt alvorens verder te gaan."
            WindowOptions = (
                u"Normaal",
                u"Geminimaliseerd",
                u"Gemaximaliseerd",
                u"Verborgen",
            )
            WindowOptionsDesc = u"Scherm opties:"
            WorkingDir = u"Werkpad:"
            browseExecutableDialogTitle = u"Kies de *.exe "
            browseWorkingDirDialogTitle = u"Kies het werkpad."
            label = u"Start Toepassing: %s"
        class Hibernate:
            name = u"Hibernate Computer "
            description = u"Deze functie zorgt ervoor dat het systeem in (hibernate) sluimerstand (S4) gaat. \n\nHibernate zorgt ervoor dat je de computer kan afsluiten en hem vervolgens terug kan inschakelen, waarna hij terug zal schakelen naar de toestand wanneer je hem hebt uitgeschakeld (alle programma's,... zullen geladen zijn). Het opstart proces zal ook sneller verlopen (bij traag opstartende computers)."
        class LockWorkstation:
            name = u"Vergrendel Werkstation"
            description = u"Deze functie zend een verzoek om het werkstation's scherm te vergrendelen. Een Werkstation vergrendelen verhindert ongeauthoriseerd gebruik. Deze functie heeft dezelfde werking als Crtl+Alt+Del drukken en vervolgens op vergrendel werkstation te klikken."
        class LogOff:
            name = u"Afmelden huidige gebruiker"
            description = u"Sluit alle lopende processen in de huidige aangemelde sessie. Daarna meldt het de gebruiker af."
        class MonitorGroup:
            name = u"Scherm"
            description = u"Deze acties controleren het stroomgebruik van het computerscherm."
        class MonitorPowerOff:
            name = u"Zet het scherm uit"
            description = u"Zet het scherm in de uit toestand. Dit is de meest stroomverbruik sparende configuratie die het scherm ondersteund."
        class MonitorPowerOn:
            name = u"Zet het scherm aan"
            description = u"Zet het scherm aan, als het in lage stroomverbruik of uit toestand is. Zal ook een uitvoerende screensaver stoppen met uitvoeren."
        class MonitorStandby:
            name = u"Zet het scherm in spaarstand"
            description = u"Zet het scherm in een lage stroomverbruik toestand."
        class MuteOff:
            name = u"Zet Mute Uit"
            description = u"Zet Mute Uit"
        class MuteOn:
            name = u"Zet Mute Aan"
            description = u"Zet Mute Aan"
        class OpenDriveTray:
            name = u"Openen/Sluiten disk lade"
            description = u"Bestuurt de disk lade van de CD/DVD-ROM speler."
            driveLabel = u"Disk:"
            labels = [
                u"Schakel disk lade om: %s",
                u"Open disk lade",
                u"Sluit disk lade",
            ]
            options = [
                u"Schakel tussen openen en sluiten van de disk lade",
                u"Enkel openen disk lade",
                u"Enkel sluiten disk lade",
            ]
            optionsLabel = u"Kies actie"
        class PlaySound:
            name = u"Speel Geluid af"
            description = u"Speel Geluid af"
            fileMask = u"Wav-Bestanden (*.WAV)|*.wav|Alle-Bestanden (*.*)|*.*"
            text1 = u"Pad naar geuidsbestand:"
            text2 = u"Wacht tot beëindigt"
        class PowerDown:
            name = u"Sluit computer af"
            description = u"Sluit het systeem af en schakel de stroom uit. Het systeem moet de stroom-uit functie ondersteunen."
        class PowerGroup:
            name = u"Stroomverbruik Beheer"
            description = u"Deze acties zijn om de computer te onderbreken, slapen, herstarten en uit te schakelen. Je kan ook het werkstation vergrendelen en de gebruiker afmelden."
        class Reboot:
            name = u"Herstart Computer"
            description = u"Sluit systeem af en herstart de computer."
        class RegistryChange:
            name = u"Verander Register Waarde"
            description = u"Wijzigt een waarde in het Windows Register."
            actions = (
                u"creëer of wijzig",
                u"wijzig indien bestaand",
                u"verwijder",
            )
            labels = (
                u'Wijzig "%s" in %s',
                u'Wijzig "%s" in %s indien bestaand',
                u'Verwijder "%s"',
            )
        class RegistryGroup:
            name = u"Register"
            description = u"Bevraagt of wijzigt waarden in het Windows Register"
            actionText = u"Actie:"
            chooseText = u"Kies Register sleutel:"
            defaultText = u"(Standaard)"
            keyOpenError = u"Fout bij openen register sleutel"
            keyText = u"Sleutel:"
            keyText2 = u"Sleutel"
            newValue = u"Nieuwe waarde:"
            noKeyError = u"Geen sleutel opgegeven"
            noNewValueError = u"Geen nieuwe waarde opgegeven"
            noSubkeyError = u"Geen ondersleutel opgegeven"
            noTypeError = u"Geen type opgegeven"
            noValueNameError = u"Geen waarde naam opgegeven"
            noValueText = u"Waarde niet gevonden"
            oldType = u"Huidig Type:"
            oldValue = u"Huidige Waarde:"
            typeText = u"Type:"
            valueChangeError = u"Fout bij wijzigen waarde"
            valueName = u"Waarde naam:"
            valueText = u"Waarde:"
        class RegistryQuery:
            name = u"Bevraag Register"
            description = u"Zoekt in het Windows register en levert of vergelijkt de waarde"
            actions = (
                u"verifieer bestaan",
                u"terug als uitkomst",
                u"vergelijk met",
            )
            labels = (
                u'Verifieer of "%s" bestaat',
                u'Lever "%s" als uitkomst',
                u'Vergelijk "%s" met %s',
            )
        class ResetIdleTimer:
            name = u"Initialiseer inactieve Timer"
            description = u"Initialiseer inactieve Timer"
        class SetClipboard:
            name = u"Kopieer string naar klipbord"
            description = u"Kopieert een string parameter naar het systeem klipbord."
            error = u"Kan het klipbord niet openen."
        class SetDisplayPreset:
            name = u"Configureer Scherm standaard instellingen"
            description = u"Configureer Scherm standaard instellingen"
            fields = (
                u"Toestel",
                u"Links",
                u"Boven",
                u"Breedte",
                u"Hoogte",
                u"Frequentie",
                u"Kleur Diepte",
                u"Aangesloten",
                u"Primair",
                u"Vlaggen",
            )
            query = u"Bevraag huidige systeem instellingen"
        class SetIdleTime:
            name = u"Configureer inactieve tijd"
            description = u"Configureer inactieve tijd. \nDit stelt de tijd in alvorens de inactive gebeurtenis (Idle) wordt gegenereerd."
            label1 = u"Wacht"
            label2 = u"seconden voor genereren van de inactieve gebeurtenis (Idle)."
        class SetMasterVolume:
            name = u"Zet Hoofd Volume"
            description = u"Configureer het hoofd volume met een absolute waarde."
            text1 = u"Zet hoofd volume op"
            text2 = u"percent."
        class SetSystemIdleTimer:
            name = u"Configureer Systeem Inactieve timer"
            description = u"Configureer Systeem Inactieve timer"
            choices = [
                u"Schakel Systeem Inactive Timer uit",
                u"Schakel Systeem Inactive Timer aan",
            ]
            text = u"Kies optie:"
        class SetWallpaper:
            name = u"Verander behangpapier"
            description = u"Verander behangpapier"
            choices = (
                u"Gecentreerd",
                u"Overlappend",
                u"Uitgerokken",
            )
            fileMask = u"Alle Fotos|*.jpg;*.bmp;*.gif;*.png|Alle Bestanden (*.*)|*.*"
            text1 = u"pad naar Foto bestand:"
            text2 = u"Uitlijning:"
        class ShowPicture:
            name = u"Toon Foto"
            description = u"Toont een foto op het scherm."
            allFiles = u"Alle Bestanden"
            allImageFiles = u"Alle Fotos"
            display = u"Scherm"
            path = u"Pad naar foto (gebruik leeg pad om te wissen):"
        class SoundGroup:
            name = u"Geluidskaart"
            description = u"Deze acties controleren de Geluidskaart van je computer."
        class Standby:
            name = u"Slaapstand"
            description = u"Deze functie zet de computer uit, onderbreekt de stroom en gaat in een slaapstand. (Stand-By)"
        class StartScreenSaver:
            name = u"Start de Windows schermbeveiliging"
            description = u"Start de momenteel in Windows ingestelde schermbeveiliging."
        class ToggleMute:
            name = u"Toggel Mute"
            description = u"Toggel Mute"
        class WakeOnLan:
            name = u"Wake on LAN"
            description = u"Ontwaakt een andere computer door een speciaal netwerk pakket te verzenden."
            parameterDescription = u"Te ontwaken Ethernet adapter MAC adres:"
    class Window:
        name = u"Venster"
        description = u"Acties gerelateerd aan het controleren van vensters op de desktop, zoals zoeken van specifieke vensters, verplaatsen, grootte veranderen en toetsen zenden naar vensters."
        class BringToFront:
            name = u"Naar voorgrond brengen"
            description = u"Naar de voorgrond brengen van een specifiek venster"
        class Close:
            name = u"Sluiten"
            description = u"Sluit een windows toepassing."
        class FindWindow:
            name = u"Vind een venster"
            description = u'Zoekt een venster dat later als doel wordt gebruikt in daaropvolgende acties in de makro.\n\n<p>Als een makro geen "Vind Venster" actie bevat, zullen alle acties op het venster in de voorgrond worden toegepast.<p>In de invoervelden gebruik de accolade wildcard {*} om gelijk welke string volgorde en de {?} om een enkele letter te vinden.'
            drag1 = u"Sleep me naar\neen venster"
            drag2 = u"En Sleep me nu\nnaar een venster"
            hide_box = u"Verberg EventGhost gedurende het slepen"
            invisible_box = u"Zoek ook onzichtbare elementen"
            label = u"Zoek Venster: %s"
            label2 = u"Zoek bovenste venster"
            matchNum1 = u"Enkel terugkeren"
            matchNum2 = u"'de overeenkomst"
            onlyFrontmost = u"Enkel overeenkomst bovenste venster "
            options = (
                u"Toepassing:",
                u"Venster Naam:",
                u"Venster Klasse:",
                u"Kind Naam:",
                u"Kind Klasse:",
            )
            refresh_btn = u"&Ververs"
            stopMacro = [
                u"Stop de makro als het doel niet is gevonden",
                u"Stop de makro als het doel is gevonden",
                u"Nooit makro stoppen",
            ]
            testButton = u"Testen"
            wait1 = u"Wacht "
            wait2 = u"seconden om het venster te laten verschijnen"
        class Maximize:
            name = u"Maximaliseer"
            description = u"Maximaliseer"
        class Minimize:
            name = u"Minimaliseer"
            description = u"Minimaliseer"
        class MoveTo:
            name = u"Verplaats Absoluut"
            description = u"Verplaats Absoluut"
            label = u"Verplaats venster naar %s"
            text1 = u"Zet horizontale positie X op"
            text2 = u"pixels"
            text3 = u"Zet verticale positie Y op"
            text4 = u"pixels"
        class Resize:
            name = u"Formaat"
            description = u"Pas het Formaat van het venster aan tot de gewenste grootte."
            label = u"Formaat Venster %s, %s"
            text1 = u"Zet Breedte op"
            text2 = u"pixels"
            text3 = u"Zet hoogte op"
            text4 = u"pixels"
        class Restore:
            name = u"Herstel"
            description = u"Herstel"
        class SendKeys:
            name = u"Simuleer Toetsen"
            description = u"Deze actie simuleert de toetsen van het toetsenbord om andere programmas te besturen. Typ gewoon de tekst die je wil in de edit box.\n\n<p>\nOm speciale toetsen te simuleren, moet je het sleutelwoord in accolades omsluiten.\nVb. Als je een pijltje naar boven toets wenst, schrijf je <b>{Up}</b>. Je kan ook meerdere sleutelwoorden combineren met het plus teken om toetscombinaties te verkrijgen zoals <b>{Shift+Ctrl+F1}</b> of <b>{Ctrl+V}</b>. De sleutelwoorden zijn niet hoofdlettergevoelig, dus je kan ook {SHIFT+ctrl+F1} schrijven indien gewenst.\n<p>"
            insertButton = u"&Invoegen"
            specialKeyTool = u"Speciale toets"
            textToType = u"Tekst te typen:"
            useAlternativeMethod = u"Gebruik alternative methode om toetsen te emuleren."
        class SendMessage:
            name = u"Zend Bericht"
            description = u"Gebruikt de Windows-API SendMessage functie om een venster een specifiek bericht te zenden. Kan ook de PostMessage functie gebruiken indien gewenst."
            text1 = u"Gebruik de PostMessage i.p.v. de SendMessage functie."
        class SetAlwaysOnTop:
            name = u"Zet de 'Altijd bovenaan' eigenschap aan"
            description = u"Zet de 'Altijd bovenaan' eigenschap aan"
            actions = (
                u"Wis altijd bovenaan",
                u"Zet altijd bovenaan",
                u"Toggel altijd bovenaan",
            )
            radioBox = u"Kies actie:"
    class Mouse:
        name = u"Muis"
        description = u"Bevat de acties om de muis wijzer te besturen en om muis gebeurtenissen te emuleren."
        class GoDirection:
            name = u"Start muisbeweging in een richting"
            description = u"Start muisbeweging in een richting"
            label = u"Start muisbeweging in richting van %.2f°"
            text1 = u"Start muisbeweging in richting van"
            text2 = u"graden. (0-360)"
        class LeftButton:
            name = u"Linker muis knop"
            description = u"Linker muis knop"
        class LeftDoubleClick:
            name = u"Linker muis knop dubbelklik"
            description = u"Linker muis knop dubbelklik"
        class MiddleButton:
            name = u"Middenste muis knop"
            description = u"Middenste muis knop"
        class MouseWheel:
            name = u"Draai Muiswiel"
            description = u"Draai Muiswiel"
            label = u"Draai Muiswiel %d klikken"
            text1 = u"Draai Muiswiel met"
            text2 = u"klikken. (Negatief draait neerwaarts)"
        class MoveAbsolute:
            name = u"Beweeg Absoluut"
            description = u"Beweeg Absoluut"
            label = u"Beweeg muis naar x:%s, y:%s"
            text1 = u"Zet horizontale positie x op"
            text2 = u"pixels"
            text3 = u"Zet verticale positie y op"
            text4 = u"pixels"
        class MoveRelative:
            name = u"Beweeg Relatief"
            description = u"Beweeg Relatief"
            label = u"Verander muis positie met x:%s, y:%s"
            text1 = u"Verander horizontale positie x met"
            text2 = u"pixels"
            text3 = u"Verander verticale positie y met"
            text4 = u"pixels"
        class RightButton:
            name = u"Rechter muis knop"
            description = u"Rechter muis knop"
        class RightDoubleClick:
            name = u"Rechter muis knop dubbelklik"
            description = u"Rechter muis knop dubbelklik"
        class ToggleLeftButton:
            name = u"Toggel linker muis knop"
            description = u"Toggel linker muis knop"
    class SoundMixerEx:
        name = u"Sound Mixer Ex"
        description = u"Deze invoegtoepassing laat toe om bijna elke instelling die beschikbaar is op je geluidskaart in te stellen.\n\n<p>Werkt momenteel niet onder Windows Vista.</p>"
        class SetSoundFader:
            name = u"Verander geluids demper/schuifknop"
            description = u"Veranderen naar een selecteerbare geluids demper/schuifknop"
        class SetSoundSwitch:
            name = u"Verander geluids schakelaar"
            description = u"Veranderen naar een selecteerbare geluids schakelaar."
    class Speech:
        name = u"Spraak"
        description = u"Gebruikt de Tekst-naar-Spraak service van de Microsoft Speech API (SAPI)"
        class TextToSpeech:
            name = u"Tekst naar Spraak"
            description = u"Gebruikt de Microsoft Speech API (SAPI) om een tekst te spreken."
            buttonInsertDate = u"Invoegen Datum"
            buttonInsertTime = u"Invoegen Tijd"
            errorCreate = u"Kan het stem object niet creëren."
            errorNoVoice = u"Stem met naam %s is niet beschikbaar"
            fast = u"Snel"
            label = u"Spreek: %s"
            labelRate = u"Snelheid:"
            labelVoice = u"Stem:"
            labelVolume = u"Geluidssterkte:"
            loud = u"Luid"
            normal = u"Normaal"
            silent = u"Stil"
            slow = u"Traag"
            textBoxLabel = u"Tekst"
            voiceProperties = u"Stem eigenschappen"
    class USB_UIRT:
        name = u"USB-UIRT"
        description = u'Hardware Invoegtoepassing voor de <a href="http://www.usbuirt.com/">USB-UIRT</a> transceiver.\n\n<p><a href="http://www.usbuirt.com/"><p><center><img src="picture.jpg" alt="USB-UIRT" /></a></center>'
        blinkRx = u"LED Licht op bij ontvangst IR"
        blinkTx = u"LED Licht op bij verzenden IR"
        irReception = u"IR ontvangst"
        legacyCodes = u"Genereer 'legacy' UIRT2-compatibele gebeurtenissen"
        notFound = u"<niet gevonden>"
        redIndicator = u"Rood indicatie LED in werking"
        stopCodes = u"Geef korte herhaal kodes door als langer durende gebeurtenissen"
        uuFirmDate = u"Firmware Datum:"
        uuFirmVersion = u"Firmware Versie:"
        uuInfo = u"USB-UIRT Informatie"
        uuProtocol = u"Protokol Versie:"
        class TransmitIR:
            name = u"Verzend IR"
            description = u"Verzend een IR kode via de USB-UIRT hardware."
            infinite = u"Oneindig"
            irCode = u"IR Kode:"
            learnButton = u"Leer een IR Kode..."
            repeatCount = u"Herhalings teller:"
            wait1 = u"Wacht:"
            wait2 = u"ms van IR inactiviteit alvorens te verzenden"
            zone = u"Zone:"
            zoneChoices = (
                u"Alle",
                u"Ext. Jack R-Pin",
                u"Ext. Jack L-Pin",
                u"Interne Zender",
            )
            class LearnDialog:
                acceptBurstButton = u"Accepteer 'Burst'"
                forceRaw = u"Forceer RAW-Mode leren"
                frequency = u"Frequentie"
                helpText = u"1. Richt afstandsbediening direct naar USB-UIRT ongeveer 20cm van de USB-UIRT voorkant.\n\n2. DRUK en BLIJF INGEDRUKT HOUDEN de gewenste knop op je afstandsbediening totdat het leren volledig gedaan is."
                progress = u"Leer voortgang"
                signalQuality = u"Signaal"
                title = u"Leer IR Kode"
    class WMPlayer:
        name = u"Windows Media Player"
        description = u'Voegt Acties toe om de <a href="http://www.microsoft.com/windows/windowsmedia/">Windows Media Player</a> te besturen.'
        class Exit:
            name = u"Exit"
            description = u"Sluit Windows Media Player."
        class FastForward:
            name = u"Fast Forward"
            description = u"Snel Vooruit Spoelen."
        class FastRewind:
            name = u"Rewind"
            description = u"Snel Achteruit Spoelen."
        class Fullscreen:
            name = u"Fullscreen"
            description = u"Wisselt tussen volledig scherm en normaal venster."
        class Library:
            name = u"Library"
            description = u'Wisselt naar het "Library" venster.'
        class NextTrack:
            name = u"Next Track"
            description = u"Simuleert een druk op de 'volgende nummer' knop."
        class NowPlaying:
            name = u"Now Playing"
            description = u'Wisselt naar het "Now Playing" venster.'
        class PreviousTrack:
            name = u"Previous Track"
            description = u"Simuleert een druk op de 'vorige nummer' knop."
        class Stop:
            name = u"Stop"
            description = u"Simuleert een druk op de 'stop' knop."
        class ToggleMute:
            name = u"Toggle Mute"
            description = u"Simuleert een druk op de 'Geluid Dempen' knop."
        class TogglePlay:
            name = u"Toggle Play"
            description = u"Simuleert een druk op de 'play / pauze' knop."
        class ToggleRepeat:
            name = u"Toggle Repeat"
            description = u"Toggelt 'Herhaal'."
        class ToggleShuffle:
            name = u"Toggle Shuffle"
            description = u"Toggelt 'Willekeurige Volgorde'."
        class VolumeDown:
            name = u"Volume Down"
            description = u"Verlaagt het WMPlayer volume met 5%."
        class VolumeUp:
            name = u"Volume Up"
            description = u"Verhoogt het WMPlayer volume met 5%."
