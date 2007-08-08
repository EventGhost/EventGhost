# -*- coding: UTF-8 -*-
class General:
    apply = u'Verkst\xe4ll'
    autostartItem = u'Autostart'
    browse = u'Bl\xe4ddra...'
    cancel = u'Avbryt'
    choose = u'V\xe4lj'
    configTree = u'Konfigurationstr\xe4d'
    deleteLinkedItems = u'Minst ett objekt utanf\xf6r din markering refererar till ett objekt i din markering. Om du forts\xe4tter att ta bort markeringen, kommer inte det refererande objektet att fungera l\xe4ngre.\n\n\xc4r du s\xe4ker att du vill ta bort markeringen?'
    deleteManyQuestion = u'Detta segment har %s subsegment.\n\xc4r du s\xe4ker att du vill ta bort alla?'
    deletePlugin = u'Detta plugin anv\xe4nds av en eller flera actions i din onfguraton.\nDu ksn inte ts bort det innan alla actions som anv\xe4ndet detta plugin har tagits bort.'
    deleteQuestion = u'\xc4r du s\xe4ker att du vill ta bort detta objekt'
    help = u'&Hj\xe4lp'
    moreHelp = u'Mer information'
    noOptionsAction = u'Denna \xe5tg\xe4rd har inga inst\xe4llningar.'
    noOptionsPlugin = u'Detta plugin har inga inst\xe4llningar.'
    ok = u'OK'
    pluginLabel = u'Plugin: %s'
    unnamedEvent = u'<icke namngiven h\xe4ndelse>'
    unnamedFile = u'<icke namngiven fil>'
    unnamedFolder = u'<icke namngiven katalog>'
    unnamedMacro = u'<icke namngivet makro>'
class MainFrame:
    onlyLogAssigned = u'&Logga endast tilldelade och aktiverade h\xe4ndelser'
    class Logger:
        caption = u'Log'
        descriptionHeader = u'Beskrivning'
        timeHeader = u'Tid'
        welcomeText = u'---> V\xe4lkommen till EventGhost <---'
    class Menu:
        About = u'&Om EventGhost'
        AddPlugin = u'L\xe4gg till Plugin'
        Apply = u'Verkst\xe4ll'
        CheckUpdate = u'S\xf6k efter uppdateringar nu...'
        ClearLog = u'Rensa Log'
        Close = u'&St\xe4ng'
        CollapseAll = u'&F\xe4ll ihop alla'
        ConfigurationMenu = u'&Konfiguration'
        Copy = u'&Kopiera'
        Cut = u'K&lipp ut'
        Delete = u'&Ta bort'
        Disabled = u'Inaktivera objekt'
        Edit = u'Konfigurera objekt'
        EditMenu = u'&Redigera'
        Execute = u'Exekvera objekt'
        Exit = u'&Avsluta'
        ExpandAll = u'&Expandera alla'
        ExpandOnEvents = u'Markera automatiskt vid h\xe4ndelse'
        ExpandTillMacro = u'Expandera automatskt endast till makro'
        Export = u'Exportera...'
        FileMenu = u'&Arkiv'
        Find = u'&S\xf6k...'
        FindNext = u'S\xf6k &N\xe4sta'
        HelpMenu = u'&Hj\xe4lp'
        HideShowToolbar = u'Verktygsf\xe4lt'
        Import = u'Importera...'
        LogActions = u'Logga h\xe4ndelser'
        LogMacros = u'Logga Makron'
        LogTime = u'Logga tid'
        New = u'&Ny'
        NewAction = u'L\xe4gg till \xe5tg\xe4rd'
        NewEvent = u'L\xe4gg till h\xe4ndelse'
        NewFolder = u'L\xe4gg till Katalog'
        NewMacro = u'L\xe4gg till Makro'
        Open = u'&\xd6ppna...'
        Options = u'&Inst\xe4llningar'
        Paste = u'&Klistra in'
        Redo = u'&Upprepa'
        Rename = u'Byt namn'
        Reset = u'Reset'
        Save = u'&Spara'
        SaveAs = u'&Spara som...'
        SelectAll = u'V\xe4lj &alla'
        Undo = u'&\xc5ngra'
        ViewMenu = u'Visa'
        WebForum = u'Support forum'
        WebHomepage = u'Hemsida'
        WebWiki = u'Wikipedia'
    class SaveChanges:
        mesg = u'Filen har \xe4ndrats\n\nVill du spara \xe4ndringarna?'
        title = u'Spara \xe4ndringar?'
    class TaskBarMenu:
        Exit = u'Avsluta'
        Hide = u'G\xf6m EventGhost'
        Show = u'Visa EventGhost'
    class Tree:
        caption = u'Konfiguration'
class Error:
    FileNotFound = u'Det g\xe5r inte att hitta filen "%s"'
    InAction = u'Fel i \xe5tg\xe4rd: "%s"'
    InScript = u'Fel i script: "%s"'
    pluginInfoPyError = u'Fel vid l\xe4sning av __info__.py f\xf6r plugin %s'
    pluginLoadError = u'Fel vid laddning av plugin %s.'
    pluginNotActivated = u'Plugin "%s" \xe4r inte aktiverat'
    pluginNotFound = u'Kan inte hitta plugin: %s'
    pluginStartError = u'Fel vid start av plugin: %s'
class CheckUpdate:
    ManErrorMesg = u'Det gick inte att h\xe4mta information fr\xe5n EventGhosts hemsida\n\nV\xe4nligen f\xf6rs\xf6k igen senare.'
    ManErrorTitle = u'Fel vid s\xf6kning efter uppdatering'
    ManOkMesg = u'Detta \xe4r den senaste versionen av EventGhost.'
    ManOkTitle = u'Det finns ingen senare version'
    downloadButton = u'Bes\xf6k nerladdningssidan'
    newVersionMesg = u'En senare version av EventGhost finns tillg\xe4nglig\n\n\tDin version:\t%s\n\tSenaste versionen\t%s\n\nVill du bes\xf6ka nerladdningssidan nu?'
    title = u'Ny EventGhost-version finns tillg\xe4nglig...'
    waitMesg = u'V\xe4nligen v\xe4nta medan EventGhost mottager uppdateringsinformation.'
class AddActionDialog:
    descriptionLabel = u'Beskrivning'
    title = u'V\xe4lj en \xe5tg\xe4rd att l\xe4gga till...'
class AddPluginDialog:
    author = u'F\xf6rfattare:'
    descriptionBox = u'Beskrivning'
    externalPlugins = u'Extern utrustning'
    noInfo = u'Det finns ingen information tillg\xe4nglig.'
    noMultiload = u'Detta plugin st\xf6djer inte flera instaser. Du har redan en instans av detta plugin i din konfiguration.'
    noMultiloadTitle = u'Flera instanser inte m\xf6jliga'
    otherPlugins = u'\xd6vrigt'
    programPlugins = u'Programkontroll'
    remotePlugins = u'Mottagare'
    title = u'V\xe4lj ett plugin att l\xe4gga till...'
    version = u'Version:'
class OptionsDialog:
    CheckUpdate = u'S\xf6k efter senare versioner vid programstart'
    HideOnClose = u'G\xf6m huvudf\xf6nstret om st\xe4ngboxen trycks.'
    HideOnStartup = u'G\xf6m vid programstart'
    LanguageGroup = u'Spr\xe5k'
    StartGroup = u'Vid programstart'
    StartWithWindows = u'Starta vid Windows-uppstart'
    Tab1 = u'Allm\xe4nt'
    Title = u'Inst\xe4llningar'
    UseAutoloadFile = u'Autoladda fil'
    Warning = u'Spr\xe5k\xe4ndring kr\xe4ver omstart f\xf6r att verkst\xe4llas.'
    confirmDelete = u'Bekr\xe4fta borttagning av tr\xe4d-objekt'
    limitMemory1 = u'Begr\xe4nsa minnesallokeringen medans minimerad till'
    limitMemory2 = u'MB'
class FindDialog:
    caseSensitive = u'&Matcha gemener/VERSALER'
    direction = u'Riktning'
    down = u'&Ner'
    findButton = u'&S\xf6k N\xe4sta'
    notFoundMesg = u'"%s" kunde inte hittas.'
    searchLabel = u'&Hitta:'
    searchParameters = u'S\xf6k \xe4ven \xe5tg\xe4rdsparametrar'
    title = u'S\xf6k'
    up = u'&Upp'
    wholeWordsOnly = u'&Matcha endast hela ord'
class AboutDialog:
    Author = u'F\xf6rfattare: %s'
    CreationDate = u'%a, %d %b %Y %H:%M:%S'
    Title = u'Om EventGhost'
    Version = u'Version: %s (build %s)'
    tabAbout = u'Om'
    tabLicense = u'Licensavtal'
    tabSpecialThanks = u'Speciellt tack'
    tabSystemInfo = u'Systeminformation'
class Plugin:
    class EventGhost:
        name = u'EventGhost'
        description = u'H\xe4r hittar du \xe5tg\xe4rder som kontrollerar grundl\xe4ggande funktioner i EventGhost'
        class AutoRepeat:
            name = u'Repetera automatiskt aktuellt makro'
            description = u'G\xf6r det makro d\xe4r detta kommando l\xe4ggs till till ett automatisk repeterande makro.'
            seconds = u'sekunder'
            text1 = u'Starta f\xf6rsta repetitionen efter'
            text2 = u'med en repetition varje'
            text3 = u'\xd6ka repetitionen n\xe4sta'
            text4 = u'till en repetition varje'
        class Comment:
            name = u'Kommentar'
            description = u'En action som inte g\xf6r n\xe5gonting, som kan anv\xe4ndas f\xf6r att kommentera din konfiguration'
        class DisableItem:
            name = u'Avaktiverar en post'
            description = u'Avaktiverar en post'
            label = u'Avaktivera: %s'
            text1 = u'V\xe4lj den post som ska avaktiveras:'
        class EnableExclusive:
            name = u'Exklusivt aktivera en katalog/ett makro'
            description = u'Aktivera specificerad katalog eller makro i din konfiguration, men avaktivera alla andra kataloger och makron som \xe4r syskon p\xe5 samma niv\xe5 i denna del-gren i tr\xe4det.'
            label = u'Aktivera exklusivitet: %s'
            text1 = u'V\xe4lj den katalog/makro som ska aktiveras:'
        class EnableItem:
            name = u'Aktivera en enhet'
            description = u'Aktiverar en enhet i tr\xe4det'
            label = u'Aktivera: %s'
            text1 = u'V\xe4lj den enhet som ska aktiveras:'
        class FlushEvents:
            name = u'T\xf6m h\xe4ndelser'
            description = u'"T\xf6m h\xe4ndelserna" t\xf6mmer alla h\xe4ndelser som f\xf6r tillf\xe4llet finns i \xe5tg\xe4rdsk\xf6n. Det \xe4r anv\xe4ndbart om ett makro som tar l\xe5ng tid p\xe5 sig, och \xe5tg\xe4rder har k\xf6ats.\n\n<p><b>Exampel:</b> Du har ett uppstartsmakro som tar l\xe5ng tid, l\xe5t s\xe4ga 90 sekunder. Anv\xe4ndaren ser ingenting f\xf6rr\xe4n projektorn startas, vilket tar 60 sekunder. Det \xe4r h\xf6g sannolikhet att han/hon trycker p\xe5 en fj\xe4rrkontroll som startar ett makro flera g\xe5nger efter varann, vilket orsakar att den l\xe5nga \xe5tg\xe4rden k\xf6r flera g\xe5nger. Om du d\xe5 placerar en "T\xf6m h\xe4ndelser" kommando i slutet av ditt makro, kommer alla \xf6verfl\xf6diga knapptryck att ignoreras.\n'
        class Jump:
            name = u'Hoppa'
            description = u'Hoppar till ett annat makro, och \xe5terv\xe4nder om du s\xe5 vill'
            label1 = u'Hoppa till %s'
            label2 = u'Hoppa till %s och \xe5terv\xe4nd'
            mesg1 = u'V\xe4lj ett makro...'
            mesg2 = u'V\xe4lj det makro som ska k\xf6ras:'
            text2 = u'Hoppa till:'
            text3 = u'\xe5terv\xe4nd efter k\xf6rning'
        class JumpIf:
            name = u'Hoppa om'
            description = u'Hoppar till ett annat makro, om det specificerade python-uttrycket returneras sant.'
            label1 = u'Om %s g\xe5 till %s'
            label2 = u'Om %s gosub %s'
            mesg1 = u'V\xe4lj makrot...'
            mesg2 = u'V\xe4lj det makro som ska startas om villkoret \xe4r sant.'
            text1 = u'Om:'
            text2 = u'G\xe5 till:'
            text3 = u'\xe5terv\xe4nd efter k\xf6rning'
        class JumpIfLongPress:
            name = u'Hoppa vid l\xe5ngt tryck'
            description = u'Hoppar till ett annat makro, om en knapp p\xe5 en fj\xe4rrkontroll trycks ner l\xe4ngre \xe4n den konfigurerade tiden.'
            label = u'Om knappen \xe4r nedtryckt %s sec, g\xe5 till: %s'
            text1 = u'Om knappen \xe4r nedtryckt l\xe4ngre \xe4n'
            text2 = u'sekunder,'
            text3 = u'hoppa till:'
            text4 = u'V\xe4lj makro...'
            text5 = u'V\xe4lj det makro som ska triggas om n\xe4r det kommer ett l\xe5ngt tryck.'
        class NewJumpIf:
            name = u'Hoppa'
            description = u'Hoppar till ett annat makro, om det specificerade villkoret uppfylls.'
            choices = [
                u'senaste \xe5tg\xe4rden lyckades',
                u'senaste \xe5tg\xe4rden misslyckades',
                u'alltid',
            ]
            labels = [
                u'Om villkoret uppfylls, hoppa till "%s"',
                u'Om villkoret inte uppfylls, hoppa till "%s"',
                u'Hoppa till "%s"',
                u'Om villkoret uppfylls, hoppa till "%s" och \xe5terv\xe4nd',
                u'Om villkoret inte uppfylls, hoppa till "%s" och \xe5terv\xe4nd',
                u'Hoppa till "%s" och \xe5terv\xe4nd',
            ]
            mesg1 = u'V\xe4lj makro...'
            mesg2 = u'V\xe4lj det makro som ska k\xf6ras, om villkoret uppfylls.'
            text1 = u'Om:'
            text2 = u'Hoppa till:'
            text3 = u'och \xe5terv\xe4nd efter k\xf6rning'
        class PythonCommand:
            name = u'Python-uttryck'
            description = u'K\xf6r ett enstaka Python-uttryck'
            parameterDescription = u'Python-uttryck:'
        class PythonScript:
            name = u'Python-skript'
            description = u'Python-skript'
        class ShowOSD:
            name = u'Visa OSD'
            description = u'Visar en enkel p\xe5 sk\xe4rmen visning.'
            alignment = u'Placering:'
            alignmentChoices = [
                u'Uppe till v\xe4nster',
                u'Uppe till h\xf6ger',
                u'Nere till v\xe4nster',
                u'Nere till h\xf6ger',
                u'Mitten av sk\xe4rmen',
                u'Nere i mitten',
                u'Uppe i mitten',
                u'Till v\xe4nster i mitten',
                u'Till h\xf6ger i mitten',
            ]
            display = u'Visa p\xe5 sk\xe4rm:'
            editText = u'Text som ska visas:'
            label = u'Visa OSD: %s'
            osdColour = u'F\xe4rg:'
            osdColourButton = u'V\xe4lj'
            osdFont = u'Teckensnitt'
            osdFontButton = u'V\xe4lj'
            outlineColour = u'V\xe4lj'
            outlineFont = u'Bakgrundsf\xe4rg'
            wait1 = u'G\xf6m efter'
            wait2 = u'sekunder (0 = aldrig)'
            xOffset = u'Horisontell offset X:'
            yOffset = u'Vertikal offset Y:'
        class StopIf:
            name = u'Stoppa om'
            description = u'Stoppar k\xf6rningen av det aktuella makrot, om det speciella Python-villkoret uppfylls.'
            label = u'Stoppa om %s'
            parameterDescription = u'Python-villkor:'
        class StopProcessing:
            name = u'Stoppa detta event'
            description = u'Stoppa detta event'
        class TriggerEvent:
            name = u'Trigga Event'
            description = u'Genererar ett event'
            labelWithTime = u'Trigga event "%s" efter %.2f sekunder'
            labelWithoutTime = u'Trigga event "%s"'
            text1 = u'Str\xe4ng som ska skickas:'
            text2 = u'F\xf6rdr\xf6jning:'
            text3 = u'sekuder. (0 = omedelbart)'
        class Wait:
            name = u'V\xe4nta ett tag'
            description = u'V\xe4nta ett tag'
            label = u'V\xe4nta: %s sek'
            seconds = u'sekunder'
            wait = u'V\xe4nta'
    class System:
        name = u'System'
        description = u'Kontrollerar olika delar av systemet, s\xe5 som ljudkortet, grafikkortet etc.'
        forced = u'Tvingad: %s'
        forcedCB = u'Tvinga st\xe4nga alla program'
        class ChangeDisplaySettings:
            name = u'\xc4ndra sk\xe4rminst\xe4llningar'
            description = u'\xc4ndra sk\xe4rminst\xe4llningar'
        class ChangeMasterVolumeBy:
            name = u'\xc4ndra huvudvolymen'
            description = u'\xc4ndra huvudvolymen'
            text1 = u'\xc4ndra huvudvolymen med'
            text2 = u'procent.'
        class Execute:
            name = u'Starta applikation'
            description = u'Startar en k\xf6rbar fil.'
            FilePath = u'S\xf6kv\xe4g till filen:'
            Parameters = u'kommandorads inst\xe4llningar:'
            ProcessOptions = (
                u'Realtid',
                u'Mer \xe4n normalt',
                u'Normalt',
                u'Mindre \xe4n normalt',
                u'Overksam',
            )
            ProcessOptionsDesc = u'Processprioritet:'
            WaitCheckbox = u'V\xe4nta tills applikationen \xe4r avslutad innan forts\xe4ttning'
            WindowOptions = (
                u'Normal',
                u'Minimerad',
                u'Maximerad',
                u'Dold',
            )
            WindowOptionsDesc = u'F\xf6nsterinst\xe4llningar'
            WorkingDir = u'Arbetsmapp:'
            browseExecutableDialogTitle = u'V\xe4lj program'
            browseWorkingDirDialogTitle = u'V\xe4lj arbetsmapp'
            label = u'Starta Programmet: %s'
        class Hibernate:
            name = u'S\xe4tt daton i vilol\xe4ge'
            description = u'Denna funktionen s\xe4tter datorn i vilol\xe4ge'
        class LockWorkstation:
            name = u'L\xe5s datorn'
            description = u'Denna funktionen l\xe5ser datorn, samma som att trycka Ctrl+Alt+Del och trycka l\xe5s dator.'
        class LogOff:
            name = u'Logga ur aktuell anv\xe4ndare'
            description = u'St\xe4nger ner alla processer och loggar ur aktuell anv\xe4ndare'
        class MonitorGroup:
            name = u'Sk\xe4rm'
            description = u'Dessa \xe5tg\xe4rder kontrollerar sk\xe4rmen.'
        class MonitorPowerOff:
            name = u'St\xe4ng sk\xe4rmen'
            description = u'S\xe4tter sk\xe4rmen i str\xf6mspar-l\xe4ge'
        class MonitorPowerOn:
            name = u'S\xe4tt p\xe5 sk\xe4rmen'
            description = u'S\xe4tter p\xe5 sk\xe4rmen fr\xe5n str\xf6mspar-l\xe4ge, st\xe4nger \xe4ven av sk\xe4rmsl\xe4ckare.'
        class MonitorStandby:
            name = u'S\xe4tt sk\xe4rmen i stand-by-l\xe4ge'
            description = u'S\xe4tt sk\xe4rmen i stand-by-l\xe4ge'
        class MuteOff:
            name = u'S\xe4tt p\xe5 ljudet'
            description = u'S\xe4tter p\xe5 ljudet'
        class MuteOn:
            name = u'St\xe4ng av ljudet'
            description = u'St\xe4nger av ljudet'
        class OpenDriveTray:
            name = u'\xd6ppna/St\xe4ng CD/DVD-enheter'
            description = u'\xd6ppnar eller st\xe4nger luckan p\xe5  CD/DVD-enheter.'
            driveLabel = u'Enhet:'
            labels = [
                u'Toggla luckan p\xe5 enhet: %s',
                u'\xd6ppna luckan p\xe5 enhet: %s',
                u'St\xe4ng luckan p\xe5 enhet: %s',
            ]
            options = [
                u'\xc4ndrar mellan \xf6ppen och st\xe4ngd lucka',
                u'\xd6ppnar luckan',
                u'St\xe4nger luckan',
            ]
            optionsLabel = u'V\xe4lj h\xe4ndelse'
        class PlaySound:
            name = u'Spela ljud'
            description = u'Spelar upp ett ljud'
            fileMask = u'Wav-filer (*.WAV)|*.wav|Alla filer (*.*)|*.*'
            text1 = u'S\xf6kv\xe4g till ljudfilen:'
            text2 = u'V\xe4nta tills slutet'
        class PowerDown:
            name = u'St\xe4ng av datorn'
            description = u'St\xe4nger av datorn.'
        class PowerGroup:
            name = u'Str\xf6mhantering'
            description = u'Dessa \xe5tg\xe4rder st\xe4nger av, startar om eller f\xf6rs\xe4tter datorn i vilol\xe4ge. Det g\xe5r ocks\xe5 att l\xe5sa datorn samt logga ut anv\xe4ndare.'
        class Reboot:
            name = u'Starta om'
            description = u'Starta om datorn'
        class RegistryChange:
            name = u'\xc4ndra i registret'
            description = u'\xc4ndra v\xe4rden i windows-registret.'
            actions = (
                u'Skapa eller \xe4ndra',
                u'\xc4ndra om redan finns',
                u'Ta bort',
            )
            labels = (
                u'\xc4ndra "%s" till "%s"',
                u'\xc4ndra "%s" till "%s" om det redan finns ett v\xe4rde',
                u'Ta bort "%s"',
            )
        class RegistryGroup:
            name = u'Registret'
            description = u'Fr\xe5gar eller \xe4ndrar v\xe4rden i windows-registret.'
            actionText = u'\xc5tg\xe4rd:'
            chooseText = u'V\xe4lj registernyckel:'
            defaultText = u'(Standard)'
            keyOpenError = u'Fel vid \xf6ppning av registernyckel'
            keyText = u'Nyckel:'
            keyText2 = u'Nyckel'
            newValue = u'Nytt v\xe4rde:'
            noKeyError = u'Ingen nyckel angiven'
            noNewValueError = u'Inget v\xe4rde angivet'
            noSubkeyError = u'Ingen undernyckel angiven'
            noTypeError = u'Ingen typ angiven '
            noValueNameError = u'Inget v\xe4rde angivet'
            noValueText = u'V\xe4rdet hittades inte'
            oldType = u'Nuvarande typ:'
            oldValue = u'Nuvarande v\xe4rde:'
            typeText = u'Typ:'
            valueChangeError = u'Fel vid \xe4ndring av v\xe4rde'
            valueName = u'V\xe4rdenamn:'
            valueText = u'V\xe4rde:'
        class RegistryQuery:
            name = u'Fr\xe5ga registret'
            description = u'Fr\xe5ga registret och f\xe5 tillbaka v\xe4rdet'
            actions = (
                u'kontrollera om det finns',
                u'returnera resultat',
                u'j\xe4mf\xf6r med',
            )
            labels = (
                u'Kontrollera om "%s" finns',
                u'Returnera "%s"',
                u'J\xe4mf\xf6r "%s" med %s',
            )
        class ResetIdleTimer:
            name = u'Nollst\xe4ll Idle-timern'
            description = u'Nollst\xe4ll Idle-timern'
        class SetClipboard:
            name = u'Kopiera str\xe4ng till utklipp'
            description = u'Kopierar str\xe4ng till utklipp'
            error = u'Kan inte \xf6ppna utklipp'
        class SetDisplayPreset:
            name = u'St\xe4ll prim\xe4r bildsk\xe4rm'
            description = u'St\xe4ll prim\xe4r bildsk\xe4rm'
            fields = (
                u'Enehet',
                u'V\xe4nster',
                u'Topp',
                u'Bredd',
                u'H\xf6jd',
                u'Frekvens',
                u'F\xe4rgdjup',
                u'Bifogad',
                u'Prim\xe4r',
                u'Flaggor',
            )
            query = u'Nuvarande bildsk\xe4rmsinst\xe4llningar'
        class SetIdleTime:
            name = u'St\xe4ll Idle-tid'
            description = u'St\xe4ll Idle-tid'
            label1 = u'V\xe4nta'
            label2 = u'sekunder innan idle triggas'
        class SetMasterVolume:
            name = u'St\xe4ll huvudvolymen'
            description = u'St\xe4ll huvudvolymen'
            text1 = u'St\xe4ll huvudvolymen till'
            text2 = u'procent.'
        class SetSystemIdleTimer:
            name = u'St\xe4ll systemets Idle-timer'
            description = u'St\xe4ll systemets Idle-timer'
            choices = [
                u'Avaktivera systemets Idle-timer',
                u'Avaktivera systemets Idle-timer',
            ]
            text = u'V\xe4lj alternativ:'
        class SetWallpaper:
            name = u'\xc4ndra bakgrundsbild'
            description = u'\xc4ndra bakgrundsbild'
            choices = (
                u'Centrerad',
                u'Sida vid sida',
                u'Anpassad',
            )
            fileMask = u'Alla bild-filer|*.jpg;*.bmp;*.gif|All Files (*.*)|*.*'
            text1 = u'S\xf6kv\xe4g till bilden:'
            text2 = u'Placering:'
        class ShowPicture:
            name = u'Visa bild'
            description = u'Visar en bild'
            allFiles = u'Alla filer'
            allImageFiles = u'Alla bild-filer'
            display = u'Sk\xe4rm'
            path = u'S\xf6kv\xe4g till bilden'
        class SoundGroup:
            name = u'Ljudkort'
            description = u'Kontrollera inst\xe4llningarna f\xf6r ljudkortet'
        class Standby:
            name = u'S\xe4tt datorn i stand-by'
            description = u'S\xe4tt datorn i stand-by'
        class StartScreenSaver:
            name = u'Starta sk\xe4rmsl\xe4ckaren'
            description = u'Startar sk\xe4rmsl\xe4ckaren.'
        class ToggleMute:
            name = u'\xc4ndra Mute'
            description = u'\xc4ndra Mute'
        class WakeOnLan:
            name = u'Wake on LAN'
            description = u'Starta en dator genom Wake on LAN (WOL)'
            parameterDescription = u'MAC-adress som ska v\xe4ckas:'
    class Window:
        name = u'F\xf6nster'
        description = u'\xc5tg\xe4rder som kan kontrollera f\xf6nster, s\xe5 som att hitta ett specifikt f\xf6nster, flytta, \xe4ndra storlek och skicka knapptryckningar.'
        class BringToFront:
            name = u'Visa \xf6verst'
            description = u'L\xe4gger det specificeraade f\xf6nstret \xf6verst'
        class Close:
            name = u'St\xe4ng'
            description = u'St\xe4nger ett f\xf6nster'
        class FindWindow:
            name = u'Hitta ett f\xf6nster'
            description = u'Letar efter ett f\xf6nster, som senare kan anv\xe4ndas f\xf6r andra f\xf6nster\xe5tg\xe4rder i makrot.\n\n<p>Om ett makro inte har "Hitta ett f\xf6nster" \xe5tg\xe4rder, kommer alla f\xf6nster\xe5tg\xe4rder p\xe5verka det f\xf6nster som har fokus.'
            drag1 = u'Drag mig till\nett f\xf6nster.'
            drag2 = u'Flytta mig nu\ntill ett f\xf6nster.'
            hide_box = u'G\xf6m EventGhost under dragning'
            invisible_box = u'Leta \xe4ven efter osynliga f\xf6nster'
            label = u'Hitta f\xf6nster: %s'
            label2 = u'Hitta det fr\xe4msta f\xf6nstret'
            matchNum1 = u'Skicka endast tillbaka'
            matchNum2 = u':e tr\xe4ff'
            onlyForground = u'Matcha endast det fr\xe4msta f\xf6nstret'
            options = (
                u'Program:',
                u'F\xf6nsternamn:',
                u'F\xf6nsterklass:',
                u'Namn p\xe5 underf\xf6nster:',
                u'Underklass:',
            )
            refresh_btn = u'&Uppdatera'
            stopMacro = [
                u'Stoppa makro om m\xe5let inte hittas',
                u'Stoppa makro om m\xe5let hittas',
                u'Stoppa aldrig makrot',
            ]
            testButton = u'Testa'
            wait1 = u'V\xe4nta upp till'
            wait2 = u'sekunder f\xf6r att f\xf6nstret visas'
        class Maximize:
            name = u'Maximera'
            description = u'Maximera'
        class Minimize:
            name = u'Minimera'
            description = u'Minimera'
        class MoveTo:
            name = u'Absolut flyttning'
            description = u'Absolut flyttning'
            label = u'Flytta f\xf6nster till %s'
            text1 = u'St\xe4ll horisontell position X till'
            text2 = u'pixlar'
            text3 = u'St\xe4ll vertikal position Y till'
            text4 = u'pixlar'
        class Resize:
            name = u'\xc4ndra storlek'
            description = u'\xc4ndrar ett f\xf6nsters storlek till specificerad storlek.'
            label = u'\xc4ndra storlek till %s, %s'
            text1 = u'S\xe4tt bredd till'
            text2 = u'pixlar'
            text3 = u'S\xe4tt h\xf6jd till'
            text4 = u'pixlar'
        class Restore:
            name = u'\xc5terskapa'
            description = u'\xc5terskapa'
        class SendKeys:
            name = u'Emulera knapptryck'
            description = u'Denna \xe5tg\xe4rd emulerar knapptryckningar f\xf6r att kontrollera andra program.\nSkriv bara in den text du vill i textrutan\n\n<p>\nF\xf6r att emulera specialknappar, m\xe5ste du innesluta ett nyckelord inom m\xe5svingar "{ }"\nTill exempel om du vill knappkombinationen Ctrl och V skriver du <b>{Ctrl+V}</b>\nDet g\xe5r att komibnera fler knapptryckningar s\xe5 som: <b>{Shift+Ctrl+F1}</b>\n<p>\nVissa tangenter skiljer mellan v\xe4nster och h\xf6ger sida av tangentbordet, s\xe5 kan dom b\xf6rja\nmed ett "L" eller ett "R", s\xe5 som Windows-tangenten:\n<b>{Win}</b> or <b>{LWin}</b> or <b>{RWin}</b>\n<p>\nH\xe4r f\xf6ljer en lista p\xe5 andra nyckelord som EventGhost kan hantera:\n<br>\n<b>{Ctrl}</b> eller <b>{Control}<br>\n{Shift}<br>\n{Alt}<br>\n{Return}</b> eller <b>{Enter}<br>\n{Back}</b> eller <b>{Backspace}<br>\n{Tab}</b> eller <b>{Tabulator}<br>\n{Esc}</b> eller <b>{Escape}<br>\n{Spc}</b> eller <b>{Space}<br>\n{Up}<br>\n{Down}<br>\n{Left}<br>\n{Right}<br>\n{PgUp}</b> eller <b>{PageUp}<br>\n{PgDown}</b> eller <b>{PageDown}<br>\n{Home}<br>\n{End}<br>\n{Ins}</b> eller <b>{Insert}<br>\n{Del}</b> eller <b>{Delete}<br>\n{Pause}<br>\n{Capslock}<br>\n{Numlock}<br>\n{Scrolllock}<br>\n{F1}, {F2}, ... , {F24}<br>\n{Apps}</b> (Detta \xe4r menyknappen som sitter brevid den h\xf6gra windows-tangenten)<b><br>\n<br>\n</b>Detta \xe4r knapparna p\xe5 det numeriska tangentbordet:<b><br>\n{Divide}<br>\n{Multiply}<br>\n{Subtract}<br>\n{Add}<br>\n{Decimal}<br>\n{Numpad0}, {Numpad1}, ... , {Numpad9}</b>\n'
            insertButton = u'&L\xe4gg in'
            specialKeyTool = u'Specialknapps verktyg'
            textToType = u'Text som ska skickas:'
            useAlternativeMethod = u'Anv\xe4nd alternativ metod f\xf6r att emulera knapptryck'
            class Keys:
                backspace = u'Sudda'
                context = u'Menyknapp'
                delete = u'Delete'
                down = u'Ner'
                end = u'End'
                enter = u'Enter'
                escape = u'Escape'
                home = u'Home'
                insert = u'Insert'
                left = u'V\xe4nster'
                num0 = u'Numeriskt tangentbord 0'
                num1 = u'Numeriskt tangentbord 1'
                num2 = u'Numeriskt tangentbord 2'
                num3 = u'Numeriskt tangentbord 3'
                num4 = u'Numeriskt tangentbord 4'
                num5 = u'Numeriskt tangentbord 5'
                num6 = u'Numeriskt tangentbord 6'
                num7 = u'Numeriskt tangentbord 7'
                num8 = u'Numeriskt tangentbord 8'
                num9 = u'Numeriskt tangentbord 9'
                numAdd = u'Numeriskt tangentbord +'
                numDecimal = u'Numeriskt tangentbord ,'
                numDivide = u'Numeriskt tangentbord /'
                numMultiply = u'Numeriskt tangentbord *'
                numSubtract = u'Numeriskt tangentbord -'
                pageDown = u'Ner'
                pageUp = u'Upp'
                returnKey = u'Return'
                right = u'H\xf6ger'
                space = u'Mellanslag'
                tabulator = u'Tab'
                up = u'Upp'
                win = u'Windows-tangenten'
        class SendMessage:
            name = u'Skicka meddelande'
            description = u'Anv\xe4nder Windows-api:et SendMessage f\xf6r att skicka ett specifikt meddelande till ett f\xf6nster. Det g\xe5r ocks\xe5 att anv\xe4nda PostMessage om s\xe5 \xf6nskas.'
            text1 = u'Anv\xe4nd PostMessage ist\xe4llet f\xf6r SendMessage'
        class SetAlwaysOnTop:
            name = u'S\xe4tt alltid \xf6verst'
            description = u'S\xe4tt alltid \xf6verst'
            actions = (
                u'Ta bort alltid \xf6verst',
                u'S\xe4tt alltid \xf6verst',
                u'Toggla alltid \xf6verst',
            )
            radioBox = u'V\xe4lj h\xe4ndelse:'
    class Mouse:
        name = u'Mus'
        description = u'\xc5tg\xe4rder som kontrollerar muspekaren.'
        class GoDirection:
            name = u'Flytta musen \xe5t ett h\xe5ll'
            description = u'Flytta musen \xe5t ett h\xe5ll'
            label = u'Flytta musen \xe5t %.2f\xb0'
            text1 = u'Riktning som muspekaren ska flyttas '
            text2 = u'(0-360)'
        class LeftButton:
            name = u'V\xe4nster musknapp'
            description = u'V\xe4nster musknapp'
        class LeftDoubleClick:
            name = u'V\xe4nster musknapp dubbelklick'
            description = u'V\xe4nster musknapp dubbelklick'
        class MiddleButton:
            name = u'Mitten musknapp'
            description = u'Mitten musknapp'
        class MouseWheel:
            name = u'Snurra scrollhjulet'
            description = u'Snurra scrollhjulet'
            label = u'Snurra scrollhjulet %d steg'
            text1 = u'Snurra scrollhjulet med'
            text2 = u'steg. (Negativt v\xe4rde snurrar ner\xe5t)'
        class MoveAbsolute:
            name = u'Absolut flyttning'
            description = u'Absolut flyttning'
            label = u'Flytta muspekaren till x:%s, y:%s'
            text1 = u'S\xe4tt horisontell position X till'
            text2 = u'pixlar'
            text3 = u'S\xe4tt vertikal position Y till'
            text4 = u'pixlar'
        class RightButton:
            name = u'H\xf6ger musknapp'
            description = u'H\xf6ger musknapp'
        class RightDoubleClick:
            name = u'H\xf6ger musknapp dubbelklick'
            description = u'H\xf6ger musknapp dubbelklick'
        class ToggleLeftButton:
            name = u'Toggla v\xe4nster musknapp'
            description = u'Toggla v\xe4nster musknapp'
    class Joystick:
        name = u'Joystick'
        description = u'Anv\xe4nd joystick eller gamepad som in-enhet till EventGhost.'
    class Keyboard:
        name = u'Tangentbord'
        description = u'Detta plugin genererar h\xe4ndelser vid knapptryckningar (Hotkeys)'
    class MediaPlayerClassic:
        name = u'Media Player Classic'
        description = u'Kontrollera <a href="http://sourceforge.net/projects/guliverkli/">Media Player Classic</a>.\n\n<p>Endast f\xf6r version <b>6.4.8.9</b> eller senare. Pluginet fungerar inte med \xe4ldre versioner!>/p>\n<p><a href=http://www.eventghost.org/forum/viewtopic.php?t=17>Bugrapporter</a></p>\n<p><a href="http://sourceforge.net/projects/guliverkli/">Media Player Classic SourceForge Projekt</a></p>'
        class AlwaysOnTop:
            name = u'Alltid \xf6verst'
            description = u'Alltid \xf6verst'
        class AudioDelayAdd10ms:
            name = u'F\xf6rdr\xf6j ljudet +10ms'
            description = u'F\xf6rdr\xf6j ljudet +10ms'
        class AudioDelaySub10ms:
            name = u'F\xf6rdr\xf6j ljudet -10ms'
            description = u'F\xf6rdr\xf6j ljudet -10ms'
        class Close:
            name = u'St\xe4ng fil'
            description = u'St\xe4ng fil'
        class DVDAngleMenu:
            name = u'DVD vinkelmeny'
            description = u'DVD vinkelmeny'
        class DVDAudioMenu:
            name = u'DVD Ljudmeny'
            description = u'DVD Ljudmeny'
        class DVDChapterMenu:
            name = u'DVD kapitelmeny'
            description = u'DVD kapitelmeny'
        class DVDMenuActivate:
            name = u'DVD meny aktivera'
            description = u'DVD meny aktivera'
        class DVDMenuBack:
            name = u'DVD meny tillbaka'
            description = u'DVD meny tillbaka'
        class DVDMenuDown:
            name = u'DVD meny ner'
            description = u'DVD meny ner'
        class DVDMenuLeave:
            name = u'DVD meny l\xe4mna'
            description = u'DVD meny l\xe4mna'
        class DVDMenuLeft:
            name = u'DVD meny v\xe4nster'
            description = u'DVD meny v\xe4nster'
        class DVDMenuRight:
            name = u'DVD meny h\xf6ger'
            description = u'DVD meny h\xf6ger'
        class DVDMenuUp:
            name = u'DVD meny upp'
            description = u'DVD meny upp'
        class DVDNextAngle:
            name = u'DVD n\xe4sta vinkel'
            description = u'DVD n\xe4sta vinkel'
        class DVDNextAudio:
            name = u'DVD n\xe4sta ljud'
            description = u'DVD n\xe4sta ljud'
        class DVDNextSubtitle:
            name = u'DVD n\xe4sta undertext'
            description = u'DVD n\xe4sta undertext'
        class DVDOnOffSubtitle:
            name = u'DVD av/p\xe5 undertext'
            description = u'DVD av/p\xe5 undertext'
        class DVDPrevAngle:
            name = u'DVD f\xf6reg\xe5ende vinkel'
            description = u'DVD f\xf6reg\xe5ende vinkel'
        class DVDPrevAudio:
            name = u'DVD f\xf6reg\xe5ende ljud'
            description = u'DVD f\xf6reg\xe5ende ljud'
        class DVDPrevSubtitle:
            name = u'DVD f\xf6reg\xe5ende undertext'
            description = u'DVD f\xf6reg\xe5ende undertext'
        class DVDRootMenu:
            name = u'DVD rotmeny'
            description = u'DVD rotmeny'
        class DVDSubtitleMenu:
            name = u'DVD undertextmeny'
            description = u'DVD undertextmeny'
        class DVDTitleMenu:
            name = u'DVD titelmeny'
            description = u'DVD titelmeny'
        class DecreaseRate:
            name = u'Minska hastighet'
            description = u'Minska hastighet'
        class Exit:
            name = u'Avsluta'
            description = u'Avsluta applikation'
        class FiltersMenu:
            name = u'Filtermeny'
            description = u'Filtermeny'
        class FrameStep:
            name = u'Stega bild'
            description = u'Stega bild'
        class FrameStepBack:
            name = u'Stega bild bak\xe5t'
            description = u'Stega bild bak\xe5t'
        class Fullscreen:
            name = u'Fullsk\xe4rm'
            description = u'Fullsk\xe4rm'
        class FullscreenWOR:
            name = u'Fullsk\xe4rm utan att \xe4ndra uppl\xf6sning'
            description = u'Fullsk\xe4rm utan att \xe4ndra uppl\xf6sning'
        class GoTo:
            name = u'G\xe5 till '
            description = u'G\xe5 till'
        class IncreaseRate:
            name = u'\xd6ka hastighet'
            description = u'\xd6ka hastighet'
        class JumpBackwardKeyframe:
            name = u'Hoppa bak\xe5t nyckelruta'
            description = u'Hoppa bak\xe5t nyckelruta'
        class JumpBackwardLarge:
            name = u'Hoppa l\xe5ngt bak\xe5t'
            description = u'Hoppa l\xe5ngt bak\xe5t'
        class JumpBackwardMedium:
            name = u'Hoppa bak\xe5t medium'
            description = u'Hoppa bak\xe5t medium'
        class JumpBackwardSmall:
            name = u'Hoppa lite bak\xe5t'
            description = u'Hoppa lite bak\xe5t'
        class JumpForwardKeyframe:
            name = u'Hoppa fram\xe5t nyckelruta'
            description = u'Hoppa fram\xe5t nyckelruta'
        class JumpForwardLarge:
            name = u'Hoppa l\xe5ngt fram\xe5t'
            description = u'Hoppa l\xe5ngt fram\xe5t'
        class JumpForwardMedium:
            name = u'Hoppa fram\xe5t medium'
            description = u'Hoppa fram\xe5t medium'
        class JumpForwardSmall:
            name = u'Hoppa lite fram\xe5t'
            description = u'Hoppa lite fram\xe5t'
        class LoadSubTitle:
            name = u'Ladda undertext'
            description = u'Ladda undertext'
        class Next:
            name = u'N\xe4sta'
            description = u'N\xe4sta'
        class NextAudio:
            name = u'N\xe4sta ljud'
            description = u'N\xe4sta ljud'
        class NextAudioOGM:
            name = u'N\xe4sta OGM ljud'
            description = u'N\xe4sta OGM ljud'
        class NextPlaylistItem:
            name = u'N\xe4sta i playlisten'
            description = u'N\xe4sta i playlisten'
        class NextSubtitle:
            name = u'N\xe4sta undertext'
            description = u'N\xe4sta undertext'
        class NextSubtitleOGM:
            name = u'N\xe4sta OGM undertext'
            description = u'N\xe4sta OGM undertext'
        class OnOffSubtitle:
            name = u'Av/p\xe5 undertext'
            description = u'Av/p\xe5 undertext'
        class OpenDVD:
            name = u'\xd6ppna DVD'
            description = u'\xd6ppna DVD'
        class OpenDevice:
            name = u'\xd6ppna enhet'
            description = u'\xd6ppna enhet'
        class OpenFile:
            name = u'\xd6ppna fil'
            description = u'\xd6ppna fil'
        class Options:
            name = u'Inst\xe4llningar'
            description = u'Inst\xe4llningar'
        class Pause:
            name = u'Pausa'
            description = u'Pausa'
        class Play:
            name = u'Play'
            description = u'Play'
        class PlayPause:
            name = u'Play/Paus'
            description = u'Play/Paus'
        class PrevAudio:
            name = u'F\xf6reg\xe5ende ljud'
            description = u'F\xf6reg\xe5ende ljud'
        class PrevAudioOGM:
            name = u'F\xf6reg\xe5ende OGM ljud'
            description = u'F\xf6reg\xe5ende OGM ljud'
        class PrevSubtitle:
            name = u'F\xf6reg\xe5ende undertext'
            description = u'F\xf6reg\xe5ende undertext'
        class PrevSubtitleOGM:
            name = u'F\xf6reg\xe5ende OGM undertext'
            description = u'F\xf6reg\xe5ende OGM undertext'
        class Previous:
            name = u'F\xf6reg\xe5ende'
            description = u'F\xf6reg\xe5ende'
        class PreviousPlaylistItem:
            name = u'F\xf6reg\xe5ende i playlisten'
            description = u'F\xf6reg\xe5ende i playlisten'
        class Properties:
            name = u'Egenskaper'
            description = u'Egenskaper'
        class QuickOpen:
            name = u'Snabbt \xf6ppna fil'
            description = u'Snabbt \xf6ppna fil'
        class ReloadSubtitles:
            name = u'Ladda om undertexter'
            description = u'Ladda om undertexter'
        class ResetRate:
            name = u'\xc5terst\xe4ll hastighet'
            description = u'\xc5terst\xe4ll hastighet'
        class SaveAs:
            name = u'Spara som'
            description = u'Spara som'
        class SaveImage:
            name = u'Spara bild'
            description = u'Spara bild'
        class SaveImageAuto:
            name = u'Spara bild automatiskt'
            description = u'Spara bild automatiskt'
        class SaveSubtitle:
            name = u'Spara undertext'
            description = u'Spara undertext'
        class Stop:
            name = u'Stopp'
            description = u'Stopp'
        class ToggleControls:
            name = u'Toggla kontroller'
            description = u'Toggla kontroller'
        class ToggleInformation:
            name = u'Toggla information'
            description = u'Toggla information'
        class TogglePlaylistBar:
            name = u'Toggla playlistrutan'
            description = u'Toggla playlistrutan'
        class ToggleSeeker:
            name = u'Toggla s\xf6karen'
            description = u'Toggla s\xf6karen'
        class ToggleStatistics:
            name = u'Toggla statistik'
            description = u'Toggla statistik'
        class ToggleStatus:
            name = u'Toggla status'
            description = u'Toggla status'
        class ViewCompact:
            name = u'Visa kompakt'
            description = u'Visa kompakt'
        class ViewMinimal:
            name = u'Visa minimal'
            description = u'Visa minimal'
        class ViewNormal:
            name = u'Visa normal'
            description = u'Visa normal'
        class VolumeDown:
            name = u'S\xe4nk volymen'
            description = u'S\xe4nk volymen'
        class VolumeMute:
            name = u'Tyst'
            description = u'Tyst'
        class VolumeUp:
            name = u'\xd6ka volymen'
            description = u'\xd6ka volymen'
        class Zoom100:
            name = u'Zooma 100%'
            description = u'Zooma 100%'
        class Zoom200:
            name = u'Zooma 200%'
            description = u'Zooma 200%'
        class Zoom50:
            name = u'Zooma 50%'
            description = u'Zooma 50%'
    class Serial:
        name = u'Serieport'
        description = u'Kommunicera via serieporten'
        baudrate = u'Hastighet:'
        bytesize = u'Antal bitar:'
        eventPrefix = u'H\xe4ndelseprefix:'
        flowcontrol = u'Fl\xf6desreglering:'
        generateEvents = u'Generera h\xe4ndelse vid inkommande data'
        handshakes = [
            u'Ingen',
            u'Xon / Xoff',
            u'H\xe5rdvara',
        ]
        parities = [
            u'Ingen paritet',
            u'Udda',
            u'J\xe4mn',
        ]
        parity = u'Paritet:'
        port = u'Port:'
        stopbits = u'Stopbitar:'
        terminator = u'Terminator:'
        class Read:
            name = u'L\xe4s data'
            description = u'L\xe4s data'
            read_all = u'L\xe4s s\xe5 m\xe5nga byte som finns tillg\xe4ngliga'
            read_some = u'L\xe4s exakt s\xe5h\xe4r m\xe5nga bytes:'
            read_time = u'och v\xe4nta maximalt s\xe5h\xe4r m\xe5nga millisekunder p\xe5 dom:'
        class Write:
            name = u'Skicka data'
            description = u'Skicka data via serieporten\n\n\n<p>Du kan anv\xe4nda Pythonstr\xe4ngar f\xf6r att skicka icke skrivbara tecken.\n\n\nN\xe5gra exempel:\n<p>\\n will skickar en linefeed (LF)<br>\\r skickar en carriage return (CR)<br>\\t skickar en tab<br>\\x0B skickar ascii-tecknet f\xf6r 0B (hexadecimalt)<br>\\\\ skickar en enstaka backslash.'
    class SysTrayMenu:
        name = u'Meny i meddelandef\xe4ltet (SysTray)'
        description = u'Till\xe5ter dig att l\xe4gga till ett eget menyinneh\xe5ll i EventGhosts meny i meddelandef\xe4ltet (SysTray)'
        addBox = u'L\xe4gg till:'
        addItemButton = u'Menyinneh\xe5ll'
        addSeparatorButton = u'Separator'
        deleteButton = u'Ta bort'
        editEvent = u'H\xe4ndelse:'
        editLabel = u'Etikett:'
        eventHeader = u'H\xe4ndelse'
        labelHeader = u'Etikett'
        unnamedEvent = u'H\xe4ndelse%s'
        unnamedLabel = u'Nytt menyinneh\xe5ll %s'
    class TellStick:
        name = u'TellStick'
        description = u'<p>Plugin f\xf6r att kontrollera TellStick-kompatibla enheter.</p>\n\n<p><a href="http://www.telldus.se">Telldus Hemsida</a></p><center><img src="tellstick.png" /></center>'
        class TurnOff:
            name = u'Sl\xe4ck'
            description = u'Sl\xe4cker en TellStick-enhet'
        class TurnOn:
            name = u'T\xe4nd'
            description = u'T\xe4nder en TellStick-enhet'
    class Timer:
        name = u'Timer'
        description = u'Triggar en h\xe4ndelse efter en inst\xe4lld tid och repeterar efter ett intervall om du s\xe5 \xf6nskar'
        colLabels = (
            u'Namn',
            u'Start tid',
            u'N\xe4sta h\xe4ndelse',
            u'Namn p\xe5 h\xe4ndelse',
            u'Loop-r\xe4knare',
            u'Loopar',
            u'Intervall',
        )
        listhl = u'Nuvarande aktiva timrar:'
        stopped = u'Plugin stoppat'
        timerFinished = u'Timern \xe4r klar'
        class TimerAction:
            name = u'Starta ny eller kontrollera befintlig timer'
            description = u' '
            actions = (
                u'Starta om timer med nuvarande inst\xe4llningar',
                u'Starta om timer (endast n\xe4r den k\xf6r)',
                u'\xc5terst\xe4ll loop-r\xe4knaren',
                u'Avbryt',
            )
            addCounterToName = u'l\xe4gg till loop-r\xe4knaren till h\xe4ndelsens namn'
            eventName = u'H\xe4ndelsens namn:'
            interval1 = u'Intervall:'
            interval2 = u'sekunder'
            labelStart = u'Starta timer "%s" (%s loopar, %.2f sekunders intervall)'
            labelStartOneTime = u'Starta timer "%s"'
            labelStartUnlimited = u'Starta timer "%s" (o\xe4ndligt antal loopar, %.2f sekunders intervall)'
            labels = (
                u'Starta om timer "%s"',
                u'Starta om timer "%s" om den fortfarande k\xf6r',
                u'\xc5terst\xe4ll r\xe4knaren f\xf6r timer "%s"',
                u'Avbryt timer "%s"',
            )
            loop1 = u'Loopar:'
            loop2 = u'(0 = obegr\xe4nsat)'
            showRemaingLoopsText = u'loop-r\xe4knare visar antal \xe5terst\xe5ende loopar'
            start = u'Starta ny timer (nuvarande timer med samma namn avbryts)'
            startTime = u'Starta:'
            startTimeTypes = (
                u'omg\xe5ende',
                u'Efter intervall-tiden',
                u'vid angiven tid (TT:MM:SS)',
                u'efter angiven varatighet (TT:MM:SS)',
                u'n\xe4sta hel minut',
                u'n\xe4sta hela fem minuter',
                u'n\xe4sta hela kvart',
                u'n\xe4sta hela halvtimme',
                u'n\xe4sta hel timme',
            )
            timerName = u'Timerns namn:'
    class Webserver:
        name = u'Webserver'
        description = u'Implementerar en enkel webserver, som du kan anv\xe4nda f\xf6r att generera h\xe4ndelser genom HTML-sidor'
        documentRoot = u'Dokument root:'
        eventPrefix = u'H\xe4ndelseprefix:'
        port = u'Port:'
    class Winamp:
        name = u'Winamp'
        description = u'Kontrollera <a href="http://www.winamp.com/">Winamp</a>.'
        class ChangeRepeatStatus:
            name = u'\xc4ndra status p\xe5 repetera'
            description = u'\xc4ndra status p\xe5 repetera'
            radioBoxLabel = u'Egenskaper'
            radioBoxOptions = [
                u'Ta bort repetera',
                u'S\xe4tt repetera',
                u'\xc4ndra repetera',
            ]
        class ChangeShuffleStatus:
            name = u'\xc4ndra slump status'
            description = u'\xc4ndra slump status'
            radioBoxLabel = u'Egenskaper'
            radioBoxOptions = [
                u'Ta bort slump',
                u'S\xe4tt slump',
                u'\xc4ndra slump',
            ]
        class ChooseFile:
            name = u'V\xe4lj fil'
            description = u'V\xe4lj fil'
        class DiscretePause:
            name = u'Pausa'
            description = u'Pausar Winamp om den spelar, men g\xf6r ingenting om den redan \xe4r pausad'
        class ExVis:
            name = u'Starta Visualisation'
            description = u'Starta Visualisation'
        class Exit:
            name = u'Avsluta'
            description = u'Avslutar Winamp'
        class Fadeout:
            name = u'Fada ut'
            description = u'Fadar ut och stoppar'
        class FastForward:
            name = u'Hoppa fram\xe5t'
            description = u'Hoppa 5 sekunder fram\xe5t'
        class FastRewind:
            name = u'Hoppa bak\xe5t'
            description = u'Hoppar 5 sekunder bak\xe5t'
        class NextTrack:
            name = u'N\xe4sta l\xe5t'
            description = u'Hoppar till n\xe4sta l\xe5t i playlisten'
        class Pause:
            name = u'Pausa'
            description = u'Pausar'
        class Play:
            name = u'Play'
            description = u'Play'
        class PreviousTrack:
            name = u'F\xf6reg\xe5ende l\xe5t'
            description = u'Hoppar till f\xf6reg\xe5ende l\xe5t i playlisten'
        class SetVolume:
            name = u'St\xe4ll volymen'
            description = u'St\xe4ll volymen'
        class ShowFileinfo:
            name = u'Visa filinformation'
            description = u'Visa filinformation'
        class Stop:
            name = u'Stoppa'
            description = u'Stoppar'
        class TogglePlay:
            name = u'Toggla play'
            description = u'Togglar mellan play och pause'
        class ToggleRepeat:
            name = u'Toggla repetera'
            description = u'Toggla repetera'
        class ToggleShuffle:
            name = u'Toggla slump'
            description = u'Toggla slump'
        class VolumeDown:
            name = u'Volym ner'
            description = u'S\xe4nker volymen med 1%'
        class VolumeUp:
            name = u'Volym upp'
            description = u'H\xf6jer volymen med 1%'
