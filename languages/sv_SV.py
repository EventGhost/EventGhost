# -*- coding: UTF-8 -*-
class General:
    apply = u"Verkställ"
    autostartItem = u"Autostart"
    browse = u"Bläddra..."
    cancel = u"Avbryt"
    choose = u"Välj"
    configTree = u"Konfigurationsträd"
    deleteLinkedItems = u"Minst ett objekt utanför din markering refererar till ett objekt i din markering. Om du fortsätter att ta bort markeringen, kommer inte det refererande objektet att fungera längre.\n\nÄr du säker att du vill ta bort markeringen?"
    deleteManyQuestion = u"Detta segment har %s subsegment.\nÄr du säker att du vill ta bort alla?"
    deletePlugin = u"Detta plugin används av en eller flera actions i din onfguraton.\nDu ksn inte ts bort det innan alla actions som användet detta plugin har tagits bort."
    deleteQuestion = u"Är du säker att du vill ta bort detta objekt"
    help = u"&Hjälp"
    noOptionsAction = u"Denna åtgärd har inga inställningar."
    noOptionsPlugin = u"Detta plugin har inga inställningar."
    ok = u"OK"
    pluginLabel = u"Plugin: %s"
    unnamedEvent = u"<icke namngiven händelse>"
    unnamedFile = u"<icke namngiven fil>"
    unnamedFolder = u"<icke namngiven katalog>"
    unnamedMacro = u"<icke namngivet makro>"
class MainFrame:
    onlyLogAssigned = u"&Logga endast tilldelade och aktiverade händelser"
    class Logger:
        caption = u"Log"
        descriptionHeader = u"Beskrivning"
        timeHeader = u"Tid"
        welcomeText = u"---> Välkommen till EventGhost <---"
    class Menu:
        About = u"&Om EventGhost"
        AddPlugin = u"Lägg till Plugin"
        Apply = u"Verkställ"
        CheckUpdate = u"Sök efter uppdateringar nu..."
        ClearLog = u"Rensa Log"
        Close = u"&Stäng"
        CollapseAll = u"&Fäll ihop alla"
        ConfigurationMenu = u"&Konfiguration"
        Copy = u"&Kopiera"
        Cut = u"K&lipp ut"
        Delete = u"&Ta bort"
        Disabled = u"Inaktivera objekt"
        Configure = u"Konfigurera objekt"
        EditMenu = u"&Redigera"
        Execute = u"Exekvera objekt"
        Exit = u"&Avsluta"
        ExpandAll = u"&Expandera alla"
        ExpandOnEvents = u"Markera automatiskt vid händelse"
        ExpandTillMacro = u"Expandera automatskt endast till makro"
        Export = u"Exportera..."
        FileMenu = u"&Arkiv"
        Find = u"&Sök..."
        FindNext = u"Sök &Nästa"
        HelpMenu = u"&Hjälp"
        HideShowToolbar = u"Verktygsfält"
        Import = u"Importera..."
        LogActions = u"Logga händelser"
        LogMacros = u"Logga Makron"
        LogTime = u"Logga tid"
        New = u"&Ny"
        AddAction = u"Lägg till åtgärd"
        AddEvent = u"Lägg till händelse"
        AddFolder = u"Lägg till Katalog"
        AddMacro = u"Lägg till Makro"
        Open = u"&Öppna..."
        Options = u"&Inställningar"
        Paste = u"&Klistra in"
        Redo = u"&Upprepa"
        Rename = u"Byt namn"
        Reset = u"Reset"
        Save = u"&Spara"
        SaveAs = u"&Spara som..."
        SelectAll = u"Välj &alla"
        Undo = u"&Ångra"
        ViewMenu = u"Visa"
        WebForum = u"Support forum"
        WebHomepage = u"Hemsida"
        WebWiki = u"Wikipedia"
    class SaveChanges:
        mesg = u"Filen har ändrats\n\nVill du spara ändringarna?"
        title = u"Spara ändringar?"
    class TaskBarMenu:
        Exit = u"Avsluta"
        Hide = u"Göm EventGhost"
        Show = u"Visa EventGhost"
    class Tree:
        caption = u"Konfiguration"
class Error:
    FileNotFound = u'Det går inte att hitta filen "%s"'
    InAction = u'Fel i åtgärd: "%s"'
    pluginLoadError = u"Fel vid laddning av plugin %s."
    pluginNotActivated = u'Plugin "%s" är inte aktiverat'
    pluginStartError = u"Fel vid start av plugin: %s"
class CheckUpdate:
    ManErrorMesg = u"Det gick inte att hämta information från EventGhosts hemsida\n\nVänligen försök igen senare."
    ManErrorTitle = u"Fel vid sökning efter uppdatering"
    ManOkMesg = u"Detta är den senaste versionen av EventGhost."
    ManOkTitle = u"Det finns ingen senare version"
    downloadButton = u"Besök nerladdningssidan"
    newVersionMesg = u"En senare version av EventGhost finns tillgänglig\n\n	Din version:	%s\n	Senaste versionen	%s\n\nVill du besöka nerladdningssidan nu?"
    title = u"Ny EventGhost-version finns tillgänglig..."
    waitMesg = u"Vänligen vänta medan EventGhost mottager uppdateringsinformation."
class AddActionDialog:
    descriptionLabel = u"Beskrivning"
    title = u"Välj en åtgärd att lägga till..."
class AddPluginDialog:
    author = u"Författare:"
    descriptionBox = u"Beskrivning"
    externalPlugins = u"Extern utrustning"
    noInfo = u"Det finns ingen information tillgänglig."
    noMultiload = u"Detta plugin stödjer inte flera instaser. Du har redan en instans av detta plugin i din konfiguration."
    noMultiloadTitle = u"Flera instanser inte möjliga"
    otherPlugins = u"Övrigt"
    programPlugins = u"Programkontroll"
    remotePlugins = u"Mottagare"
    title = u"Välj ett plugin att lägga till..."
    version = u"Version:"
class OptionsDialog:
    CheckUpdate = u"Sök efter senare versioner vid programstart"
    HideOnClose = u"Göm huvudfönstret om stängboxen trycks."
    HideOnStartup = u"Göm vid programstart"
    LanguageGroup = u"Språk"
    StartGroup = u"Vid programstart"
    StartWithWindows = u"Starta vid Windows-uppstart"
    Tab1 = u"Allmänt"
    Title = u"Inställningar"
    UseAutoloadFile = u"Autoladda fil"
    Warning = u"Språkändring kräver omstart för att verkställas."
    confirmDelete = u"Bekräfta borttagning av träd-objekt"
    limitMemory1 = u"Begränsa minnesallokeringen medans minimerad till"
    limitMemory2 = u"MB"
class FindDialog:
    caseSensitive = u"&Matcha gemener/VERSALER"
    direction = u"Riktning"
    down = u"&Ner"
    findButton = u"&Sök Nästa"
    notFoundMesg = u'"%s" kunde inte hittas.'
    searchLabel = u"&Hitta:"
    searchParameters = u"Sök även åtgärdsparametrar"
    title = u"Sök"
    up = u"&Upp"
    wholeWordsOnly = u"&Matcha endast hela ord"
class AboutDialog:
    Author = u"Författare: %s"
    CreationDate = u"%a, %d %b %Y %H:%M:%S"
    Title = u"Om EventGhost"
    Version = u"Version: %s (build %s)"
    tabAbout = u"Om"
    tabLicense = u"Licensavtal"
    tabSpecialThanks = u"Speciellt tack"
    tabSystemInfo = u"Systeminformation"
class Plugin:
    class EventGhost:
        name = u"EventGhost"
        description = u"Här hittar du åtgärder som kontrollerar grundläggande funktioner i EventGhost"
        class AutoRepeat:
            name = u"Repetera automatiskt aktuellt makro"
            description = u"Gör det makro där detta kommando läggs till till ett automatisk repeterande makro."
            seconds = u"sekunder"
            text1 = u"Starta första repetitionen efter"
            text2 = u"med en repetition varje"
            text3 = u"Öka repetitionen nästa"
            text4 = u"till en repetition varje"
        class Comment:
            name = u"Kommentar"
            description = u"En action som inte gör någonting, som kan användas för att kommentera din konfiguration"
        class DisableItem:
            name = u"Avaktiverar en post"
            description = u"Avaktiverar en post"
            label = u"Avaktivera: %s"
            text1 = u"Välj den post som ska avaktiveras:"
        class EnableExclusive:
            name = u"Exklusivt aktivera en katalog/ett makro"
            description = u"Aktivera specificerad katalog eller makro i din konfiguration, men avaktivera alla andra kataloger och makron som är syskon på samma nivå i denna del-gren i trädet."
            label = u"Aktivera exklusivitet: %s"
            text1 = u"Välj den katalog/makro som ska aktiveras:"
        class EnableItem:
            name = u"Aktivera en enhet"
            description = u"Aktiverar en enhet i trädet"
            label = u"Aktivera: %s"
            text1 = u"Välj den enhet som ska aktiveras:"
        class FlushEvents:
            name = u"Töm händelser"
            description = u'"Töm händelserna" tömmer alla händelser som för tillfället finns i åtgärdskön. Det är användbart om ett makro som tar lång tid på sig, och åtgärder har köats.\n\n<p><b>Exampel:</b> Du har ett uppstartsmakro som tar lång tid, låt säga 90 sekunder. Användaren ser ingenting förrän projektorn startas, vilket tar 60 sekunder. Det är hög sannolikhet att han/hon trycker på en fjärrkontroll som startar ett makro flera gånger efter varann, vilket orsakar att den långa åtgärden kör flera gånger. Om du då placerar en "Töm händelser" kommando i slutet av ditt makro, kommer alla överflödiga knapptryck att ignoreras.\n'
        class JumpIf:
            name = u"Hoppa om"
            description = u"Hoppar till ett annat makro, om det specificerade python-uttrycket returneras sant."
            label1 = u"Om %s gå till %s"
            label2 = u"Om %s gosub %s"
            mesg1 = u"Välj makrot..."
            mesg2 = u"Välj det makro som ska startas om villkoret är sant."
            text1 = u"Om:"
            text2 = u"Gå till:"
            text3 = u"återvänd efter körning"
        class JumpIfLongPress:
            name = u"Hoppa vid långt tryck"
            description = u"Hoppar till ett annat makro, om en knapp på en fjärrkontroll trycks ner längre än den konfigurerade tiden."
            label = u"Om knappen är nedtryckt %s sec, gå till: %s"
            text1 = u"Om knappen är nedtryckt längre än"
            text2 = u"sekunder,"
            text3 = u"hoppa till:"
            text4 = u"Välj makro..."
            text5 = u"Välj det makro som ska triggas om när det kommer ett långt tryck."
        class NewJumpIf:
            name = u"Hoppa"
            description = u"Hoppar till ett annat makro, om det specificerade villkoret uppfylls."
            choices = [
                u"senaste åtgärden lyckades",
                u"senaste åtgärden misslyckades",
                u"alltid",
            ]
            labels = [
                u'Om villkoret uppfylls, hoppa till "%s"',
                u'Om villkoret inte uppfylls, hoppa till "%s"',
                u'Hoppa till "%s"',
                u'Om villkoret uppfylls, hoppa till "%s" och återvänd',
                u'Om villkoret inte uppfylls, hoppa till "%s" och återvänd',
                u'Hoppa till "%s" och återvänd',
            ]
            mesg1 = u"Välj makro..."
            mesg2 = u"Välj det makro som ska köras, om villkoret uppfylls."
            text1 = u"Om:"
            text2 = u"Hoppa till:"
            text3 = u"och återvänd efter körning"
        class PythonCommand:
            name = u"Python-uttryck"
            description = u"Kör ett enstaka Python-uttryck"
            parameterDescription = u"Python-uttryck:"
        class PythonScript:
            name = u"Python-skript"
            description = u"Python-skript"
        class ShowOSD:
            name = u"Visa OSD"
            description = u"Visar en enkel på skärmen visning."
            alignment = u"Placering:"
            alignmentChoices = [
                u"Uppe till vänster",
                u"Uppe till höger",
                u"Nere till vänster",
                u"Nere till höger",
                u"Mitten av skärmen",
                u"Nere i mitten",
                u"Uppe i mitten",
                u"Till vänster i mitten",
                u"Till höger i mitten",
            ]
            display = u"Visa på skärm:"
            editText = u"Text som ska visas:"
            label = u"Visa OSD: %s"
            osdColour = u"Färg:"
            osdFont = u"Teckensnitt"
            outlineFont = u"Bakgrundsfärg"
            wait1 = u"Göm efter"
            wait2 = u"sekunder (0 = aldrig)"
            xOffset = u"Horisontell offset X:"
            yOffset = u"Vertikal offset Y:"
        class StopIf:
            name = u"Stoppa om"
            description = u"Stoppar körningen av det aktuella makrot, om det speciella Python-villkoret uppfylls."
            label = u"Stoppa om %s"
            parameterDescription = u"Python-villkor:"
        class StopProcessing:
            name = u"Stoppa detta event"
            description = u"Stoppa detta event"
        class TriggerEvent:
            name = u"Trigga Event"
            description = u"Genererar ett event"
            labelWithTime = u'Trigga event "%s" efter %.2f sekunder'
            labelWithoutTime = u'Trigga event "%s"'
            text1 = u"Sträng som ska skickas:"
            text2 = u"Fördröjning:"
            text3 = u"sekuder. (0 = omedelbart)"
        class Wait:
            name = u"Vänta ett tag"
            description = u"Vänta ett tag"
            label = u"Vänta: %s sek"
            seconds = u"sekunder"
            wait = u"Vänta"
    class System:
        name = u"System"
        description = u"Kontrollerar olika delar av systemet, så som ljudkortet, grafikkortet etc."
        forced = u"Tvingad: %s"
        forcedCB = u"Tvinga stänga alla program"
        class ChangeDisplaySettings:
            name = u"Ändra skärminställningar"
            description = u"Ändra skärminställningar"
        class ChangeMasterVolumeBy:
            name = u"Ändra huvudvolymen"
            description = u"Ändra huvudvolymen"
            text1 = u"Ändra huvudvolymen med"
            text2 = u"procent."
        class Execute:
            name = u"Starta applikation"
            description = u"Startar en körbar fil."
            FilePath = u"Sökväg till filen:"
            Parameters = u"kommandorads inställningar:"
            ProcessOptions = (
                u"Realtid",
                u"Mer än normalt",
                u"Normalt",
                u"Mindre än normalt",
                u"Overksam",
            )
            ProcessOptionsDesc = u"Processprioritet:"
            WaitCheckbox = u"Vänta tills applikationen är avslutad innan fortsättning"
            WindowOptions = (
                u"Normal",
                u"Minimerad",
                u"Maximerad",
                u"Dold",
            )
            WindowOptionsDesc = u"Fönsterinställningar"
            WorkingDir = u"Arbetsmapp:"
            browseExecutableDialogTitle = u"Välj program"
            browseWorkingDirDialogTitle = u"Välj arbetsmapp"
            label = u"Starta Programmet: %s"
        class Hibernate:
            name = u"Sätt daton i viloläge"
            description = u"Denna funktionen sätter datorn i viloläge"
        class LockWorkstation:
            name = u"Lås datorn"
            description = u"Denna funktionen låser datorn, samma som att trycka Ctrl+Alt+Del och trycka lås dator."
        class LogOff:
            name = u"Logga ur aktuell användare"
            description = u"Stänger ner alla processer och loggar ur aktuell användare"
        class MonitorGroup:
            name = u"Skärm"
            description = u"Dessa åtgärder kontrollerar skärmen."
        class MonitorPowerOff:
            name = u"Stäng skärmen"
            description = u"Sätter skärmen i strömspar-läge"
        class MonitorPowerOn:
            name = u"Sätt på skärmen"
            description = u"Sätter på skärmen från strömspar-läge, stänger även av skärmsläckare."
        class MonitorStandby:
            name = u"Sätt skärmen i stand-by-läge"
            description = u"Sätt skärmen i stand-by-läge"
        class MuteOff:
            name = u"Sätt på ljudet"
            description = u"Sätter på ljudet"
        class MuteOn:
            name = u"Stäng av ljudet"
            description = u"Stänger av ljudet"
        class OpenDriveTray:
            name = u"Öppna/Stäng CD/DVD-enheter"
            description = u"Öppnar eller stänger luckan på  CD/DVD-enheter."
            driveLabel = u"Enhet:"
            labels = [
                u"Toggla luckan på enhet: %s",
                u"Öppna luckan på enhet: %s",
                u"Stäng luckan på enhet: %s",
            ]
            options = [
                u"Ändrar mellan öppen och stängd lucka",
                u"Öppnar luckan",
                u"Stänger luckan",
            ]
            optionsLabel = u"Välj händelse"
        class PlaySound:
            name = u"Spela ljud"
            description = u"Spelar upp ett ljud"
            fileMask = u"Wav-filer (*.WAV)|*.wav|Alla filer (*.*)|*.*"
            text1 = u"Sökväg till ljudfilen:"
            text2 = u"Vänta tills slutet"
        class PowerDown:
            name = u"Stäng av datorn"
            description = u"Stänger av datorn."
        class PowerGroup:
            name = u"Strömhantering"
            description = u"Dessa åtgärder stänger av, startar om eller försätter datorn i viloläge. Det går också att låsa datorn samt logga ut användare."
        class Reboot:
            name = u"Starta om"
            description = u"Starta om datorn"
        class RegistryChange:
            name = u"Ändra i registret"
            description = u"Ändra värden i windows-registret."
            actions = (
                u"Skapa eller ändra",
                u"Ändra om redan finns",
                u"Ta bort",
            )
            labels = (
                u'Ändra "%s" till "%s"',
                u'Ändra "%s" till "%s" om det redan finns ett värde',
                u'Ta bort "%s"',
            )
        class RegistryGroup:
            name = u"Registret"
            description = u"Frågar eller ändrar värden i windows-registret."
            actionText = u"Åtgärd:"
            chooseText = u"Välj registernyckel:"
            defaultText = u"(Standard)"
            keyOpenError = u"Fel vid öppning av registernyckel"
            keyText = u"Nyckel:"
            keyText2 = u"Nyckel"
            newValue = u"Nytt värde:"
            noKeyError = u"Ingen nyckel angiven"
            noNewValueError = u"Inget värde angivet"
            noSubkeyError = u"Ingen undernyckel angiven"
            noTypeError = u"Ingen typ angiven "
            noValueNameError = u"Inget värde angivet"
            noValueText = u"Värdet hittades inte"
            oldType = u"Nuvarande typ:"
            oldValue = u"Nuvarande värde:"
            typeText = u"Typ:"
            valueChangeError = u"Fel vid ändring av värde"
            valueName = u"Värdenamn:"
            valueText = u"Värde:"
        class RegistryQuery:
            name = u"Fråga registret"
            description = u"Fråga registret och få tillbaka värdet"
            actions = (
                u"kontrollera om det finns",
                u"returnera resultat",
                u"jämför med",
            )
            labels = (
                u'Kontrollera om "%s" finns',
                u'Returnera "%s"',
                u'Jämför "%s" med %s',
            )
        class ResetIdleTimer:
            name = u"Nollställ Idle-timern"
            description = u"Nollställ Idle-timern"
        class SetClipboard:
            name = u"Kopiera sträng till utklipp"
            description = u"Kopierar sträng till utklipp"
            error = u"Kan inte öppna utklipp"
        class SetDisplayPreset:
            name = u"Ställ primär bildskärm"
            description = u"Ställ primär bildskärm"
            fields = (
                u"Enehet",
                u"Vänster",
                u"Topp",
                u"Bredd",
                u"Höjd",
                u"Frekvens",
                u"Färgdjup",
                u"Bifogad",
                u"Primär",
                u"Flaggor",
            )
            query = u"Nuvarande bildskärmsinställningar"
        class SetIdleTime:
            name = u"Ställ Idle-tid"
            description = u"Ställ Idle-tid"
            label1 = u"Vänta"
            label2 = u"sekunder innan idle triggas"
        class SetMasterVolume:
            name = u"Ställ huvudvolymen"
            description = u"Ställ huvudvolymen"
            text1 = u"Ställ huvudvolymen till"
            text2 = u"procent."
        class SetSystemIdleTimer:
            name = u"Ställ systemets Idle-timer"
            description = u"Ställ systemets Idle-timer"
            choices = [
                u"Avaktivera systemets Idle-timer",
                u"Avaktivera systemets Idle-timer",
            ]
            text = u"Välj alternativ:"
        class SetWallpaper:
            name = u"Ändra bakgrundsbild"
            description = u"Ändra bakgrundsbild"
            choices = (
                u"Centrerad",
                u"Sida vid sida",
                u"Anpassad",
            )
            fileMask = u"Alla bild-filer|*.jpg;*.bmp;*.gif|All Files (*.*)|*.*"
            text1 = u"Sökväg till bilden:"
            text2 = u"Placering:"
        class ShowPicture:
            name = u"Visa bild"
            description = u"Visar en bild"
            allFiles = u"Alla filer"
            allImageFiles = u"Alla bild-filer"
            display = u"Skärm"
            path = u"Sökväg till bilden"
        class SoundGroup:
            name = u"Ljudkort"
            description = u"Kontrollera inställningarna för ljudkortet"
        class Standby:
            name = u"Sätt datorn i stand-by"
            description = u"Sätt datorn i stand-by"
        class StartScreenSaver:
            name = u"Starta skärmsläckaren"
            description = u"Startar skärmsläckaren."
        class ToggleMute:
            name = u"Ändra Mute"
            description = u"Ändra Mute"
        class WakeOnLan:
            name = u"Wake on LAN"
            description = u"Starta en dator genom Wake on LAN (WOL)"
            parameterDescription = u"MAC-adress som ska väckas:"
    class Window:
        name = u"Fönster"
        description = u"Åtgärder som kan kontrollera fönster, så som att hitta ett specifikt fönster, flytta, ändra storlek och skicka knapptryckningar."
        class BringToFront:
            name = u"Visa överst"
            description = u"Lägger det specificeraade fönstret överst"
        class Close:
            name = u"Stäng"
            description = u"Stänger ett fönster"
        class FindWindow:
            name = u"Hitta ett fönster"
            description = u'Letar efter ett fönster, som senare kan användas för andra fönsteråtgärder i makrot.\n\n<p>Om ett makro inte har "Hitta ett fönster" åtgärder, kommer alla fönsteråtgärder påverka det fönster som har fokus.'
            drag1 = u"Drag mig till\nett fönster."
            drag2 = u"Flytta mig nu\ntill ett fönster."
            hide_box = u"Göm EventGhost under dragning"
            invisible_box = u"Leta även efter osynliga fönster"
            label = u"Hitta fönster: %s"
            label2 = u"Hitta det främsta fönstret"
            matchNum1 = u"Skicka endast tillbaka"
            matchNum2 = u":e träff"
            onlyFrontmost = u"Matcha endast det främsta fönstret"
            options = (
                u"Program:",
                u"Fönsternamn:",
                u"Fönsterklass:",
                u"Namn på underfönster:",
                u"Underklass:",
            )
            refresh_btn = u"&Uppdatera"
            stopMacro = [
                u"Stoppa makro om målet inte hittas",
                u"Stoppa makro om målet hittas",
                u"Stoppa aldrig makrot",
            ]
            testButton = u"Testa"
            wait1 = u"Vänta upp till"
            wait2 = u"sekunder för att fönstret visas"
        class Maximize:
            name = u"Maximera"
            description = u"Maximera"
        class Minimize:
            name = u"Minimera"
            description = u"Minimera"
        class MoveTo:
            name = u"Absolut flyttning"
            description = u"Absolut flyttning"
            label = u"Flytta fönster till %s"
            text1 = u"Ställ horisontell position X till"
            text2 = u"pixlar"
            text3 = u"Ställ vertikal position Y till"
            text4 = u"pixlar"
        class Resize:
            name = u"Ändra storlek"
            description = u"Ändrar ett fönsters storlek till specificerad storlek."
            label = u"Ändra storlek till %s, %s"
            text1 = u"Sätt bredd till"
            text2 = u"pixlar"
            text3 = u"Sätt höjd till"
            text4 = u"pixlar"
        class Restore:
            name = u"Återskapa"
            description = u"Återskapa"
        class SendKeys:
            name = u"Emulera knapptryck"
            description = u'Denna åtgärd emulerar knapptryckningar för att kontrollera andra program.\nSkriv bara in den text du vill i textrutan\n\n<p>\nFör att emulera specialknappar, måste du innesluta ett nyckelord inom måsvingar "{ }"\nTill exempel om du vill knappkombinationen Ctrl och V skriver du <b>{Ctrl+V}</b>\nDet går att komibnera fler knapptryckningar så som: <b>{Shift+Ctrl+F1}</b>\n<p>\nVissa tangenter skiljer mellan vänster och höger sida av tangentbordet, så kan dom börja\nmed ett "L" eller ett "R", så som Windows-tangenten:\n<b>{Win}</b> or <b>{LWin}</b> or <b>{RWin}</b>\n<p>\nHär följer en lista på andra nyckelord som EventGhost kan hantera:\n<br>\n<b>{Ctrl}</b> eller <b>{Control}<br>\n{Shift}<br>\n{Alt}<br>\n{Return}</b> eller <b>{Enter}<br>\n{Back}</b> eller <b>{Backspace}<br>\n{Tab}</b> eller <b>{Tabulator}<br>\n{Esc}</b> eller <b>{Escape}<br>\n{Spc}</b> eller <b>{Space}<br>\n{Up}<br>\n{Down}<br>\n{Left}<br>\n{Right}<br>\n{PgUp}</b> eller <b>{PageUp}<br>\n{PgDown}</b> eller <b>{PageDown}<br>\n{Home}<br>\n{End}<br>\n{Ins}</b> eller <b>{Insert}<br>\n{Del}</b> eller <b>{Delete}<br>\n{Pause}<br>\n{Capslock}<br>\n{Numlock}<br>\n{Scrolllock}<br>\n{F1}, {F2}, ... , {F24}<br>\n{Apps}</b> (Detta är menyknappen som sitter brevid den högra windows-tangenten)<b><br>\n<br>\n</b>Detta är knapparna på det numeriska tangentbordet:<b><br>\n{Divide}<br>\n{Multiply}<br>\n{Subtract}<br>\n{Add}<br>\n{Decimal}<br>\n{Numpad0}, {Numpad1}, ... , {Numpad9}</b>\n'
            insertButton = u"&Lägg in"
            specialKeyTool = u"Specialknapps verktyg"
            textToType = u"Text som ska skickas:"
            useAlternativeMethod = u"Använd alternativ metod för att emulera knapptryck"
            class Keys:
                backspace = u"Sudda"
                context = u"Menyknapp"
                delete = u"Delete"
                down = u"Ner"
                end = u"End"
                enter = u"Enter"
                escape = u"Escape"
                home = u"Home"
                insert = u"Insert"
                left = u"Vänster"
                num0 = u"Numeriskt tangentbord 0"
                num1 = u"Numeriskt tangentbord 1"
                num2 = u"Numeriskt tangentbord 2"
                num3 = u"Numeriskt tangentbord 3"
                num4 = u"Numeriskt tangentbord 4"
                num5 = u"Numeriskt tangentbord 5"
                num6 = u"Numeriskt tangentbord 6"
                num7 = u"Numeriskt tangentbord 7"
                num8 = u"Numeriskt tangentbord 8"
                num9 = u"Numeriskt tangentbord 9"
                numAdd = u"Numeriskt tangentbord +"
                numDecimal = u"Numeriskt tangentbord ,"
                numDivide = u"Numeriskt tangentbord /"
                numMultiply = u"Numeriskt tangentbord *"
                numSubtract = u"Numeriskt tangentbord -"
                pageDown = u"Ner"
                pageUp = u"Upp"
                returnKey = u"Return"
                right = u"Höger"
                space = u"Mellanslag"
                tabulator = u"Tab"
                up = u"Upp"
                win = u"Windows-tangenten"
        class SendMessage:
            name = u"Skicka meddelande"
            description = u"Använder Windows-api:et SendMessage för att skicka ett specifikt meddelande till ett fönster. Det går också att använda PostMessage om så önskas."
            text1 = u"Använd PostMessage istället för SendMessage"
        class SetAlwaysOnTop:
            name = u"Sätt alltid överst"
            description = u"Sätt alltid överst"
            actions = (
                u"Ta bort alltid överst",
                u"Sätt alltid överst",
                u"Toggla alltid överst",
            )
            radioBox = u"Välj händelse:"
    class Mouse:
        name = u"Mus"
        description = u"Åtgärder som kontrollerar muspekaren."
        class GoDirection:
            name = u"Flytta musen åt ett håll"
            description = u"Flytta musen åt ett håll"
            label = u"Flytta musen åt %.2f°"
            text1 = u"Riktning som muspekaren ska flyttas "
            text2 = u"(0-360)"
        class LeftButton:
            name = u"Vänster musknapp"
            description = u"Vänster musknapp"
        class LeftDoubleClick:
            name = u"Vänster musknapp dubbelklick"
            description = u"Vänster musknapp dubbelklick"
        class MiddleButton:
            name = u"Mitten musknapp"
            description = u"Mitten musknapp"
        class MouseWheel:
            name = u"Snurra scrollhjulet"
            description = u"Snurra scrollhjulet"
            label = u"Snurra scrollhjulet %d steg"
            text1 = u"Snurra scrollhjulet med"
            text2 = u"steg. (Negativt värde snurrar neråt)"
        class MoveAbsolute:
            name = u"Absolut flyttning"
            description = u"Absolut flyttning"
            label = u"Flytta muspekaren till x:%s, y:%s"
            text1 = u"Sätt horisontell position X till"
            text2 = u"pixlar"
            text3 = u"Sätt vertikal position Y till"
            text4 = u"pixlar"
        class RightButton:
            name = u"Höger musknapp"
            description = u"Höger musknapp"
        class RightDoubleClick:
            name = u"Höger musknapp dubbelklick"
            description = u"Höger musknapp dubbelklick"
        class ToggleLeftButton:
            name = u"Toggla vänster musknapp"
            description = u"Toggla vänster musknapp"
    class Joystick:
        name = u"Joystick"
        description = u"Använd joystick eller gamepad som in-enhet till EventGhost."
    class Keyboard:
        name = u"Tangentbord"
        description = u"Detta plugin genererar händelser vid knapptryckningar (Hotkeys)"
    class MediaPlayerClassic:
        name = u"Media Player Classic"
        description = u'Kontrollera <a href="http://sourceforge.net/projects/guliverkli/">Media Player Classic</a>.\n\n<p>Endast för version <b>6.4.8.9</b> eller senare. Pluginet fungerar inte med äldre versioner!>/p>\n<p><a href=http://www.eventghost.org/forum/viewtopic.php?t=17>Bugrapporter</a></p>\n<p><a href="http://sourceforge.net/projects/guliverkli/">Media Player Classic SourceForge Projekt</a></p>'
        class AlwaysOnTop:
            name = u"Alltid överst"
            description = u"Alltid överst"
        class AudioDelayAdd10ms:
            name = u"Fördröj ljudet +10ms"
            description = u"Fördröj ljudet +10ms"
        class AudioDelaySub10ms:
            name = u"Fördröj ljudet -10ms"
            description = u"Fördröj ljudet -10ms"
        class Close:
            name = u"Stäng fil"
            description = u"Stäng fil"
        class DVDAngleMenu:
            name = u"DVD vinkelmeny"
            description = u"DVD vinkelmeny"
        class DVDAudioMenu:
            name = u"DVD Ljudmeny"
            description = u"DVD Ljudmeny"
        class DVDChapterMenu:
            name = u"DVD kapitelmeny"
            description = u"DVD kapitelmeny"
        class DVDMenuActivate:
            name = u"DVD meny aktivera"
            description = u"DVD meny aktivera"
        class DVDMenuBack:
            name = u"DVD meny tillbaka"
            description = u"DVD meny tillbaka"
        class DVDMenuDown:
            name = u"DVD meny ner"
            description = u"DVD meny ner"
        class DVDMenuLeave:
            name = u"DVD meny lämna"
            description = u"DVD meny lämna"
        class DVDMenuLeft:
            name = u"DVD meny vänster"
            description = u"DVD meny vänster"
        class DVDMenuRight:
            name = u"DVD meny höger"
            description = u"DVD meny höger"
        class DVDMenuUp:
            name = u"DVD meny upp"
            description = u"DVD meny upp"
        class DVDNextAngle:
            name = u"DVD nästa vinkel"
            description = u"DVD nästa vinkel"
        class DVDNextAudio:
            name = u"DVD nästa ljud"
            description = u"DVD nästa ljud"
        class DVDNextSubtitle:
            name = u"DVD nästa undertext"
            description = u"DVD nästa undertext"
        class DVDOnOffSubtitle:
            name = u"DVD av/på undertext"
            description = u"DVD av/på undertext"
        class DVDPrevAngle:
            name = u"DVD föregående vinkel"
            description = u"DVD föregående vinkel"
        class DVDPrevAudio:
            name = u"DVD föregående ljud"
            description = u"DVD föregående ljud"
        class DVDPrevSubtitle:
            name = u"DVD föregående undertext"
            description = u"DVD föregående undertext"
        class DVDRootMenu:
            name = u"DVD rotmeny"
            description = u"DVD rotmeny"
        class DVDSubtitleMenu:
            name = u"DVD undertextmeny"
            description = u"DVD undertextmeny"
        class DVDTitleMenu:
            name = u"DVD titelmeny"
            description = u"DVD titelmeny"
        class DecreaseRate:
            name = u"Minska hastighet"
            description = u"Minska hastighet"
        class Exit:
            name = u"Avsluta"
            description = u"Avsluta applikation"
        class FiltersMenu:
            name = u"Filtermeny"
            description = u"Filtermeny"
        class FrameStep:
            name = u"Stega bild"
            description = u"Stega bild"
        class FrameStepBack:
            name = u"Stega bild bakåt"
            description = u"Stega bild bakåt"
        class Fullscreen:
            name = u"Fullskärm"
            description = u"Fullskärm"
        class FullscreenWOR:
            name = u"Fullskärm utan att ändra upplösning"
            description = u"Fullskärm utan att ändra upplösning"
        class GoTo:
            name = u"Gå till "
            description = u"Gå till"
        class IncreaseRate:
            name = u"Öka hastighet"
            description = u"Öka hastighet"
        class JumpBackwardKeyframe:
            name = u"Hoppa bakåt nyckelruta"
            description = u"Hoppa bakåt nyckelruta"
        class JumpBackwardLarge:
            name = u"Hoppa långt bakåt"
            description = u"Hoppa långt bakåt"
        class JumpBackwardMedium:
            name = u"Hoppa bakåt medium"
            description = u"Hoppa bakåt medium"
        class JumpBackwardSmall:
            name = u"Hoppa lite bakåt"
            description = u"Hoppa lite bakåt"
        class JumpForwardKeyframe:
            name = u"Hoppa framåt nyckelruta"
            description = u"Hoppa framåt nyckelruta"
        class JumpForwardLarge:
            name = u"Hoppa långt framåt"
            description = u"Hoppa långt framåt"
        class JumpForwardMedium:
            name = u"Hoppa framåt medium"
            description = u"Hoppa framåt medium"
        class JumpForwardSmall:
            name = u"Hoppa lite framåt"
            description = u"Hoppa lite framåt"
        class LoadSubTitle:
            name = u"Ladda undertext"
            description = u"Ladda undertext"
        class Next:
            name = u"Nästa"
            description = u"Nästa"
        class NextAudio:
            name = u"Nästa ljud"
            description = u"Nästa ljud"
        class NextAudioOGM:
            name = u"Nästa OGM ljud"
            description = u"Nästa OGM ljud"
        class NextPlaylistItem:
            name = u"Nästa i playlisten"
            description = u"Nästa i playlisten"
        class NextSubtitle:
            name = u"Nästa undertext"
            description = u"Nästa undertext"
        class NextSubtitleOGM:
            name = u"Nästa OGM undertext"
            description = u"Nästa OGM undertext"
        class OnOffSubtitle:
            name = u"Av/på undertext"
            description = u"Av/på undertext"
        class OpenDVD:
            name = u"Öppna DVD"
            description = u"Öppna DVD"
        class OpenDevice:
            name = u"Öppna enhet"
            description = u"Öppna enhet"
        class OpenFile:
            name = u"Öppna fil"
            description = u"Öppna fil"
        class Options:
            name = u"Inställningar"
            description = u"Inställningar"
        class Pause:
            name = u"Pausa"
            description = u"Pausa"
        class Play:
            name = u"Play"
            description = u"Play"
        class PlayPause:
            name = u"Play/Paus"
            description = u"Play/Paus"
        class PrevAudio:
            name = u"Föregående ljud"
            description = u"Föregående ljud"
        class PrevAudioOGM:
            name = u"Föregående OGM ljud"
            description = u"Föregående OGM ljud"
        class PrevSubtitle:
            name = u"Föregående undertext"
            description = u"Föregående undertext"
        class PrevSubtitleOGM:
            name = u"Föregående OGM undertext"
            description = u"Föregående OGM undertext"
        class Previous:
            name = u"Föregående"
            description = u"Föregående"
        class PreviousPlaylistItem:
            name = u"Föregående i playlisten"
            description = u"Föregående i playlisten"
        class Properties:
            name = u"Egenskaper"
            description = u"Egenskaper"
        class QuickOpen:
            name = u"Snabbt öppna fil"
            description = u"Snabbt öppna fil"
        class ReloadSubtitles:
            name = u"Ladda om undertexter"
            description = u"Ladda om undertexter"
        class ResetRate:
            name = u"Återställ hastighet"
            description = u"Återställ hastighet"
        class SaveAs:
            name = u"Spara som"
            description = u"Spara som"
        class SaveImage:
            name = u"Spara bild"
            description = u"Spara bild"
        class SaveImageAuto:
            name = u"Spara bild automatiskt"
            description = u"Spara bild automatiskt"
        class SaveSubtitle:
            name = u"Spara undertext"
            description = u"Spara undertext"
        class Stop:
            name = u"Stopp"
            description = u"Stopp"
        class ToggleControls:
            name = u"Toggla kontroller"
            description = u"Toggla kontroller"
        class ToggleInformation:
            name = u"Toggla information"
            description = u"Toggla information"
        class TogglePlaylistBar:
            name = u"Toggla playlistrutan"
            description = u"Toggla playlistrutan"
        class ToggleSeeker:
            name = u"Toggla sökaren"
            description = u"Toggla sökaren"
        class ToggleStatistics:
            name = u"Toggla statistik"
            description = u"Toggla statistik"
        class ToggleStatus:
            name = u"Toggla status"
            description = u"Toggla status"
        class ViewCompact:
            name = u"Visa kompakt"
            description = u"Visa kompakt"
        class ViewMinimal:
            name = u"Visa minimal"
            description = u"Visa minimal"
        class ViewNormal:
            name = u"Visa normal"
            description = u"Visa normal"
        class VolumeDown:
            name = u"Sänk volymen"
            description = u"Sänk volymen"
        class VolumeMute:
            name = u"Tyst"
            description = u"Tyst"
        class VolumeUp:
            name = u"Öka volymen"
            description = u"Öka volymen"
        class Zoom100:
            name = u"Zooma 100%"
            description = u"Zooma 100%"
        class Zoom200:
            name = u"Zooma 200%"
            description = u"Zooma 200%"
        class Zoom50:
            name = u"Zooma 50%"
            description = u"Zooma 50%"
    class Serial:
        name = u"Serieport"
        description = u"Kommunicera via serieporten"
        baudrate = u"Hastighet:"
        bytesize = u"Antal bitar:"
        eventPrefix = u"Händelseprefix:"
        flowcontrol = u"Flödesreglering:"
        generateEvents = u"Generera händelse vid inkommande data"
        handshakes = [
            u"Ingen",
            u"Xon / Xoff",
            u"Hårdvara",
        ]
        parities = [
            u"Ingen paritet",
            u"Udda",
            u"Jämn",
        ]
        parity = u"Paritet:"
        port = u"Port:"
        stopbits = u"Stopbitar:"
        terminator = u"Terminator:"
        class Read:
            name = u"Läs data"
            description = u"Läs data"
            read_all = u"Läs så många byte som finns tillgängliga"
            read_some = u"Läs exakt såhär många bytes:"
            read_time = u"och vänta maximalt såhär många millisekunder på dom:"
        class Write:
            name = u"Skicka data"
            description = u"Skicka data via serieporten\n\n\n<p>Du kan använda Pythonsträngar för att skicka icke skrivbara tecken.\n\n\nNågra exempel:\n<p>\n will skickar en linefeed (LF)<br>\r skickar en carriage return (CR)<br>\t skickar en tab<br>\x0B skickar ascii-tecknet för 0B (hexadecimalt)<br>\\ skickar en enstaka backslash."
    class SysTrayMenu:
        name = u"Meny i meddelandefältet (SysTray)"
        description = u"Tillåter dig att lägga till ett eget menyinnehåll i EventGhosts meny i meddelandefältet (SysTray)"
        addBox = u"Lägg till:"
        addItemButton = u"Menyinnehåll"
        addSeparatorButton = u"Separator"
        deleteButton = u"Ta bort"
        editEvent = u"Händelse:"
        editLabel = u"Etikett:"
        eventHeader = u"Händelse"
        labelHeader = u"Etikett"
        unnamedEvent = u"Händelse%s"
        unnamedLabel = u"Nytt menyinnehåll %s"
    class TellStick:
        name = u"TellStick"
        description = u'<p>Plugin för att kontrollera TellStick-kompatibla enheter.</p>\n\n<p><a href="http://www.telldus.se">Telldus Hemsida</a></p><center><img src="tellstick.png" /></center>'
        class TurnOff:
            name = u"Släck"
            description = u"Släcker en TellStick-enhet"
        class TurnOn:
            name = u"Tänd"
            description = u"Tänder en TellStick-enhet"
    class Timer:
        name = u"Timer"
        description = u"Triggar en händelse efter en inställd tid och repeterar efter ett intervall om du så önskar"
        colLabels = (
            u"Namn",
            u"Start tid",
            u"Nästa händelse",
            u"Namn på händelse",
            u"Loop-räknare",
            u"Loopar",
            u"Intervall",
        )
        listhl = u"Nuvarande aktiva timrar:"
        stopped = u"Plugin stoppat"
        timerFinished = u"Timern är klar"
        class TimerAction:
            name = u"Starta ny eller kontrollera befintlig timer"
            description = u" "
            actions = (
                u"Starta om timer med nuvarande inställningar",
                u"Starta om timer (endast när den kör)",
                u"Återställ loop-räknaren",
                u"Avbryt",
            )
            addCounterToName = u"lägg till loop-räknaren till händelsens namn"
            eventName = u"Händelsens namn:"
            interval1 = u"Intervall:"
            interval2 = u"sekunder"
            labelStart = u'Starta timer "%s" (%s loopar, %.2f sekunders intervall)'
            labelStartOneTime = u'Starta timer "%s"'
            labelStartUnlimited = u'Starta timer "%s" (oändligt antal loopar, %.2f sekunders intervall)'
            labels = (
                u'Starta om timer "%s"',
                u'Starta om timer "%s" om den fortfarande kör',
                u'Återställ räknaren för timer "%s"',
                u'Avbryt timer "%s"',
            )
            loop1 = u"Loopar:"
            loop2 = u"(0 = obegränsat)"
            showRemaingLoopsText = u"loop-räknare visar antal återstående loopar"
            start = u"Starta ny timer (nuvarande timer med samma namn avbryts)"
            startTime = u"Starta:"
            startTimeTypes = (
                u"omgående",
                u"Efter intervall-tiden",
                u"vid angiven tid (TT:MM:SS)",
                u"efter angiven varatighet (TT:MM:SS)",
                u"nästa hel minut",
                u"nästa hela fem minuter",
                u"nästa hela kvart",
                u"nästa hela halvtimme",
                u"nästa hel timme",
            )
            timerName = u"Timerns namn:"
    class Webserver:
        name = u"Webserver"
        description = u"Implementerar en enkel webserver, som du kan använda för att generera händelser genom HTML-sidor"
        documentRoot = u"Dokument root:"
        eventPrefix = u"Händelseprefix:"
        port = u"Port:"
    class Winamp:
        name = u"Winamp"
        description = u'Kontrollera <a href="http://www.winamp.com/">Winamp</a>.'
        class ChangeRepeatStatus:
            name = u"Ändra status på repetera"
            description = u"Ändra status på repetera"
            radioBoxLabel = u"Egenskaper"
            radioBoxOptions = [
                u"Ta bort repetera",
                u"Sätt repetera",
                u"Ändra repetera",
            ]
        class ChangeShuffleStatus:
            name = u"Ändra slump status"
            description = u"Ändra slump status"
            radioBoxLabel = u"Egenskaper"
            radioBoxOptions = [
                u"Ta bort slump",
                u"Sätt slump",
                u"Ändra slump",
            ]
        class ChooseFile:
            name = u"Välj fil"
            description = u"Välj fil"
        class DiscretePause:
            name = u"Pausa"
            description = u"Pausar Winamp om den spelar, men gör ingenting om den redan är pausad"
        class ExVis:
            name = u"Starta Visualisation"
            description = u"Starta Visualisation"
        class Exit:
            name = u"Avsluta"
            description = u"Avslutar Winamp"
        class Fadeout:
            name = u"Fada ut"
            description = u"Fadar ut och stoppar"
        class FastForward:
            name = u"Hoppa framåt"
            description = u"Hoppa 5 sekunder framåt"
        class FastRewind:
            name = u"Hoppa bakåt"
            description = u"Hoppar 5 sekunder bakåt"
        class NextTrack:
            name = u"Nästa låt"
            description = u"Hoppar till nästa låt i playlisten"
        class Pause:
            name = u"Pausa"
            description = u"Pausar"
        class Play:
            name = u"Play"
            description = u"Play"
        class PreviousTrack:
            name = u"Föregående låt"
            description = u"Hoppar till föregående låt i playlisten"
        class SetVolume:
            name = u"Ställ volymen"
            description = u"Ställ volymen"
        class ShowFileinfo:
            name = u"Visa filinformation"
            description = u"Visa filinformation"
        class Stop:
            name = u"Stoppa"
            description = u"Stoppar"
        class TogglePlay:
            name = u"Toggla play"
            description = u"Togglar mellan play och pause"
        class ToggleRepeat:
            name = u"Toggla repetera"
            description = u"Toggla repetera"
        class ToggleShuffle:
            name = u"Toggla slump"
            description = u"Toggla slump"
        class VolumeDown:
            name = u"Volym ner"
            description = u"Sänker volymen med 1%"
        class VolumeUp:
            name = u"Volym upp"
            description = u"Höjer volymen med 1%"
