# -*- coding: UTF-8 -*-
class General:
    apply = u'Pou\u017e\xedt'
    autostartItem = u'Automatick\xfd start'
    browse = u'Proch\xe1zet...'
    cancel = u'Storno'
    choose = u'Volba'
    configTree = u'Konfigura\u010dn\xed strom'
    deleteLinkedItems = u'Alespo\u0148 jedna polo\u017eka mimo v\xe1\u0161 v\xfdb\u011br odkazuje na polo\u017eku uvnit\u0159 va\u0161eho v\xfdb\u011bru. Jestli\u017ee p\u0159esto budete v odstran\u011bn\xed v\xfdb\u011bru pokra\u010dovat, odkazuj\xedc\xed polo\u017eka nebude moci d\xe1le spr\xe1vn\u011b pracovat.\n\nJste si jist\xfd, \u017ee chcete v\xfdb\u011br odstranit?'
    deleteManyQuestion = u'Tento element m\xe1 %s subelement(y,\u016f).\nJsi si jist\xfd, \u017ee chcete odstranit v\u0161echny ?'
    deletePlugin = u'Tento plugin je pou\u017eit n\u011bkterou akc\xed ve va\u0161\xed konfiguraci.\nNem\u016f\u017eete ho odstranit, dokud neodstran\xedte v\u0161echny akce, kter\xe9 ho pou\u017e\xedvaj\xed.'
    deleteQuestion = u'Jste si jist\xfd, \u017ee chcete odstranit tuto polo\u017eku?'
    help = u'&Pomoc'
    moreHelp = u'V\xedce...'
    moreTag = u'v\xedce...'
    noOptionsAction = u'Tato akce nem\xe1 \u017e\xe1dn\xe9 mo\u017enosti nastaven\xed.'
    noOptionsPlugin = u'Tento plugin nem\xe1 \u017e\xe1dn\xe9 mo\u017enosti nastaven\xed.'
    ok = u'OK'
    pluginLabel = u'Plugin: %s'
    unnamedEvent = u'<nepojmenovan\xe1 ud\xe1lost>'
    unnamedFile = u'<nepojmenovan\xfd soubor>'
    unnamedFolder = u'<nepojmenovan\xe1 slo\u017eka>'
    unnamedMacro = u'<nepojmenovan\xe9 makro>'
class MainFrame:
    onlyLogAssigned = u'Zaznamen\xe1vat pouze p\u0159i\u0159azen\xe9 a aktivn\xed ud\xe1losti'
    class Logger:
        caption = u'Zapisova\u010d ud\xe1lost\xed (Logger)'
        descriptionHeader = u'Z\xe1znam'
        timeHeader = u'\u010cas'
        welcomeText = u'-->V\xedt\xe1m v\xe1s v aplikaci EventGhost<--'
    class Menu:
        About = u'&O aplikaci EventGhost...'
        AddPlugin = u'Vlo\u017eit Plugin...'
        Apply = u'Pou\u017e\xedt'
        CheckUpdate = u'Vyhledat nov\u011bj\u0161\xed verzi...'
        ClearLog = u'Vy\u010distit'
        Close = u'&Zav\u0159\xedt'
        CollapseAll = u'&Sbalit v\u0161e'
        ConfigurationMenu = u'&Konfigurace'
        Copy = u'&Kop\xedrovat'
        Cut = u'&Vyjmout'
        Delete = u'O&dstranit'
        Disabled = u'Zak\xe1zat polo\u017eku'
        Edit = u'Konfigurovat polo\u017eku...'
        EditMenu = u'&Editovat'
        Execute = u'&Spustit polo\u017eku'
        Exit = u'&Konec'
        ExpandAll = u'&Rozbalit v\u0161e'
        ExpandOnEvents = u'Rozbalit p\u0159i &ud\xe1losti'
        ExpandTillMacro = u'Rozbalit pouze do \xfarovn\u011b &makra'
        Export = u'Export...'
        FileMenu = u'&Soubor'
        Find = u'&Naj\xedt...'
        FindNext = u'Na&j\xedt dal\u0161\xed'
        HelpMenu = u'&Pomoc'
        HideShowToolbar = u'Panel n\xe1stroj\u016f'
        Import = u'Import...'
        LogActions = u'Logovat &akce'
        LogMacros = u'Logovat &makra'
        LogTime = u'&Logovat \u010das'
        New = u'&Nov\xfd'
        NewAction = u'Vlo\u017eit akci...'
        NewEvent = u'Vlo\u017eit ud\xe1lost'
        NewFolder = u'Vlo\u017eit slo\u017eku'
        NewMacro = u'Vlo\u017eit makro'
        Open = u'&Otev\u0159\xedt...'
        Options = u'&Mo\u017enosti...'
        Paste = u'V&lo\u017eit'
        Redo = u'&Odvolat zp\u011bt (Redo)'
        Rename = u'P\u0159ejmenovat polo\u017eku'
        Reset = u'Reset'
        Save = u'&Ulo\u017eit'
        SaveAs = u'Ulo\u017eit &jako...'
        SelectAll = u'&Vybrat v\u0161e'
        Undo = u'&Zp\u011bt (Undo)'
        ViewMenu = u'&Zobrazit'
        WebForum = u'Internetov\xe1 diskuse'
        WebHomepage = u'Domovsk\xe1 str\xe1nka aplikace EventGhost'
        WebWiki = u'Wikipedie'
    class SaveChanges:
        mesg = u'Konfigura\u010dn\xed soubor byl zm\u011bn\u011bn.\n\nChcete zm\u011bny ulo\u017eit ?'
        title = u'Ulo\u017eit zm\u011bny ?'
    class TaskBarMenu:
        Exit = u'Ukon\u010dit EventGhost'
        Hide = u'Skr\xfdt okno aplikace EventGhost'
        Show = u'Otev\u0159\xedt okno aplikace EventGhost'
    class Tree:
        caption = u'Konfigurace'
class Error:
    FileNotFound = u'Soubor "%s" nebyl nalezen.'
    InAction = u'Chyba v akci: "%s"'
    InScript = u'Chyba ve skriptu: "%s"'
    pluginInfoPyError = u'Chyba p\u0159i \u010dten\xed souboru __info__.py pro plugin %s'
    pluginLoadError = u'Chyba p\u0159i zav\xe1d\u011bn\xed pluginu %s.'
    pluginNotActivated = u'Plugin "%s" nebyl aktivov\xe1n'
    pluginNotFound = u'Plugin %s nenalezen.'
    pluginStartError = u'Chyba p\u0159i spu\u0161t\u011bn\xed pluginu: %s'
class CheckUpdate:
    ManErrorMesg = u'Nebylo mo\u017en\xe9 z\xedskat informace z webov\xe9 str\xe1nky EventGhost.\n\nPros\xedm, zkuste to znovu pozd\u011bji.'
    ManErrorTitle = u'Chyba p\u0159i pokusu o update'
    ManOkMesg = u'Tato verze aplikace EventGhost je nejnov\u011bj\u0161\xed.'
    ManOkTitle = u'\u017d\xe1dn\xe1 nov\u011bj\u0161\xed verze nen\xed k dispozici'
    downloadButton = u'Nav\u0161t\xedvit str\xe1nku stahov\xe1n\xed'
    newVersionMesg = u'Byla vyd\xe1na nov\u011bj\u0161\xed verze aplikace EventGhost.\n\n\tVa\u0161e verze:\t%s\n\tPosledn\xed verze:\t%s\n\nChcete nav\u0161t\xedvit str\xe1nku stahov\xe1n\xed hned?'
    title = u'Nov\xe1 verze aplikace EventGhost je k dispozici...'
    waitMesg = u'Pros\xedm \u010dekejte, dokud EventGhost nez\xedsk\xe1 pot\u0159ebn\xe9 informace.'
class AddActionDialog:
    descriptionLabel = u'Popis'
    title = u'V\xfdb\u011br akce ke vlo\u017een\xed...'
class AddPluginDialog:
    author = u'Autor:'
    descriptionBox = u'Popis'
    externalPlugins = u'Ovl\xe1d\xe1n\xed extern\xedho HW'
    noInfo = u'\u017d\xe1dn\xe1 informace nen\xed k dispozici.'
    noMultiload = u'Tento plugin nepodporuje v\xedce sou\u010dasn\xfdch instanc\xed a vy u\u017e m\xe1te jednu instanci tohoto pluginu ve sv\xe9 konfiguraci.'
    noMultiloadTitle = u'Nen\xed mo\u017en\xfd soub\u011bh v\xedce instanc\xed'
    otherPlugins = u'Ostatn\xed'
    programPlugins = u'Ovl\xe1dan\xe9 programy'
    remotePlugins = u'P\u0159ij\xedma\u010de d\xe1lkov\xfdch povel\u016f'
    title = u'V\xfdb\u011br pluginu ke vlo\u017een\xed...'
    version = u'Verze:'
class AddActionGroupDialog:
    caption = u'Vlo\u017eit akce ?'
    message = u'EventGhost m\u016f\u017ee vlo\u017eit slo\u017eku se v\u0161emi akcemi tohoto pluginu do konfigura\u010dn\xedho stromu. Jestli\u017ee si to p\u0159ejete, zvolte m\xedsto pro vkl\xe1danou slo\u017eku a stiskn\u011bte tla\u010d\xedtko OK.\n\nJinak stiskn\u011bte tla\u010d\xedtko Storno.'
class OptionsDialog:
    CheckUpdate = u'Kontrolovat existenci nov\u011bj\u0161\xed verze p\u0159i spu\u0161t\u011bn\xed'
    HideOnClose = u'Skr\xfdt hlavn\xed okno aplikace p\u0159i stisknut\xed zav\xedrac\xedho tla\u010d\xedtka'
    HideOnStartup = u'Skr\xfdt p\u0159i spu\u0161t\u011bn\xed'
    LanguageGroup = u'Jazyk'
    StartGroup = u'P\u0159i spu\u0161t\u011bn\xed'
    StartWithWindows = u'Spustit p\u0159i startu Windows'
    Tab1 = u'V\u0161eobecn\xe9'
    Title = u'Mo\u017enosti'
    UseAutoloadFile = u'Automatick\xe9 spu\u0161t\u011bn\xed souboru'
    Warning = u'Zm\u011bna jazyka se projev\xed a\u017e po nov\xe9m spu\u0161t\u011bn\xed aplikace.'
    confirmDelete = u'Potvrdit odstran\u011bn\xed polo\u017eky stromu'
    limitMemory1 = u'Limit spot\u0159eby pam\u011bti p\u0159i minimalizaci'
    limitMemory2 = u'MB'
class FindDialog:
    caseSensitive = u'&Rozli\u0161ovat velikost'
    direction = u'Sm\u011br'
    down = u'&Dol\u016f'
    findButton = u'Na&j\xedt dal\u0161\xed'
    notFoundMesg = u'"%s" nenalezeno.'
    searchLabel = u'&Naj\xedt:'
    searchParameters = u'&Hledat i v parametrech akc\xed'
    title = u'Hled\xe1n\xed'
    up = u'Nahor&u'
    wholeWordsOnly = u'&Pouze cel\xe1 slova'
class AboutDialog:
    Author = u'Autor: %s'
    CreationDate = u'%a, %d %b %Y %H:%M:%S'
    Title = u'O aplikaci EventGhost'
    Version = u'Verze: %s (build %s)'
    tabAbout = u'O aplikaci'
    tabLicense = u'Licen\u010dn\xed ujedn\xe1n\xed'
    tabSpecialThanks = u'Zvl\xe1\u0161tn\xed pod\u011bkov\xe1n\xed'
    tabSystemInfo = u'Syst\xe9mov\xe9 informace'
class Plugin:
    class EventGhost:
        name = u'EventGhost'
        description = u'Zde jsou akce, kter\xe9 slou\u017e\xed p\u0159ev\xe1\u017en\u011b k \u0159\xedzen\xed funkce j\xe1dra aplikace EventGhost.'
        class AutoRepeat:
            name = u'Automaticky opakovat makro'
            description = u'Makro, ve kter\xe9m je tento element pou\u017eit, bude automaticky opakovan\u011b spou\u0161t\u011bno.\n\n<p><b>POZOR:</b> Tato funkce je pou\u017eiteln\xe1 pouze pro makra, jejich\u017e d\xe9lka prov\xe1d\u011bn\xed je d\xe1na n\u011bjak\xfdm extern\xedm podn\u011btem (nap\u0159\xedklad dlouh\xfdm dr\u017een\xedm tla\u010d\xedtka d\xe1lkov\xe9ho ovlada\u010de). Element "Automatick\xe9 opakov\xe1n\xed makra" by m\u011bl b\xfdt um\xedst\u011bn na konci makra.'
            seconds = u'sec.'
            text1 = u'Prvn\xed opakov\xe1n\xed za\u010d\xedt po'
            text2 = u'a opakovat ka\u017ed\xfdch'
            text3 = u'Modifikovat \u010detnost opakov\xe1n\xed po'
            text4 = u's opakov\xe1n\xedm ka\u017ed\xfdch'
        class Comment:
            name = u'Koment\xe1\u0159'
            description = u'Akce bez \xfa\u010dinku. M\u016f\u017ee b\xfdt pou\u017eita pro komentov\xe1n\xed va\u0161\xed konfigurace.'
        class DisableItem:
            name = u'Zak\xe1zat polo\u017eku'
            description = u'Zak\xe1\u017ee polo\u017eku'
            label = u'Zak\xe1zat: %s'
            text1 = u'Pros\xedm vyberte polo\u017eku, kter\xe1 m\xe1 b\xfdt zak\xe1z\xe1na:'
        class EnableExclusive:
            name = u'V\xfdhradn\u011b povolit slo\u017eku/makro'
            description = u'Povol\xed ur\u010ditou slo\u017eku nebo makro ve va\u0161\xed konfiguraci. Z\xe1rove\u0148 ale zak\xe1\u017ee v\u0161echny ostatn\xed slo\u017eky nebo makra, kter\xe9 maj\xed stejnou \xfarove\u0148 (slo\u017eka nebo makro) a jsou na stejn\xe9 v\u011btvi konfigura\u010dn\xedho stromu.'
            label = u'V\xfdhradn\u011b povolit: %s'
            text1 = u'Pros\xedm vyberte slo\u017eku/makro, kter\xe1/-\xe9 m\xe1 b\xfdt povolena/-o:'
        class EnableItem:
            name = u'Povolit polo\u017eku'
            description = u'Povol\xed polo\u017eku ve stromu.'
            label = u'Povolit: %s'
            text1 = u'Pros\xedm vyberte polo\u017eku, kter\xe1 m\xe1 b\xfdt povolena:'
        class FlushEvents:
            name = u'Zahodit ud\xe1losti'
            description = u'Akce "Zahodit ud\xe1losti" m\xe1 za n\xe1sledek vypr\xe1zdn\u011bn\xed pracovn\xed fronty. To je u\u017eite\u010dn\xe9 v p\u0159\xedpad\u011b, \u017ee n\u011bjak\xe9 makro se zpracov\xe1v\xe1 ur\u010ditou dobu a ud\xe1losti, kter\xe9 se nahromad\xed b\u011bhem jeho zpracov\xe1n\xed, by nem\u011bly b\xfdt zpracov\xe1ny.\n\n<p><b>P\u0159\xedklad:</b> M\xe1te zdlouhav\xe9 makro "start syst\xe9mu", jeho\u017e zpracov\xe1n\xed trv\xe1 okolo 90 sekund. Koncov\xfd u\u017eivatel nebude nic vid\u011bt, dokud se nerozsv\xedt\xed projektor. To trv\xe1 asi 60 sekund. Je velmi pravd\u011bpodobn\xe9, \u017ee u\u017eivatel bude opakovan\u011b ma\u010dkat tla\u010d\xedtko d\xe1lkov\xe9ho ovlada\u010de, kter\xe9 startuje makro (v domn\u011bn\xed, \u017ee se nic ned\u011bje). Pokud na konec makra um\xedst\xedte p\u0159\xedkaz "Zahodit ud\xe1losti", v\u0161echna nadbyte\u010dn\xe1 stisknut\xed tla\u010d\xedtka budou z fronty vymaz\xe1na.'
        class JumpIfLongPress:
            name = u'Sko\u010dit p\u0159i dlouh\xe9m stisku'
            description = u'Sko\u010d\xed na jin\xe9 makro, pokud tla\u010d\xedtko na d\xe1lkov\xe9m ovlada\u010di je stisknut\xe9 d\xe9le, ne\u017e je nastaven\xfd \u010das.'
            label = u'Je-li tla\u010d\xedtko stisknut\xe9 %s sec, sko\u010dit na: %s'
            text1 = u'Je-li tla\u010d\xedtko stisknut\xe9 d\xe9le ne\u017e'
            text2 = u'sekund,'
            text3 = u'sko\u010dit na:'
            text4 = u'Vyberte makro, na kter\xe9 se m\xe1 sko\u010dit...'
            text5 = u'Pros\xedm vyberte makro, kter\xe9 by m\u011blo b\xfdt spu\u0161t\u011bno,\npokud je dosa\u017eeno nastaven\xe9 d\xe9lky stisknut\xed tla\u010d\xedtka.'
        class NewJumpIf:
            name = u'Sko\u010dit'
            description = u'Sko\u010d\xed na jin\xe9 makro, pokud v\xfdsledek ur\u010dit\xe9 akce odpov\xedd\xe1 podm\xednce.'
            choices = [
                u'posledn\xed akce byla \xfasp\u011b\u0161n\xe1',
                u'posledn\xed akce byla ne\xfasp\u011b\u0161n\xe1',
                u'v\u017edy',
            ]
            labels = [
                u'P\u0159i \xfasp\u011bchu sko\u010dit na "%s"',
                u'P\u0159i ne\xfasp\u011bchu sko\u010dit na "%s"',
                u'Sko\u010dit na "%s"',
                u'P\u0159i \xfasp\u011bchu sko\u010dit na "%s" a vr\xe1tit se',
                u'P\u0159i ne\xfasp\u011bchu sko\u010dit na "%s" a vr\xe1tit se',
                u'Sko\u010dit na "%s" a vr\xe1tit se',
            ]
            mesg1 = u'V\xfdb\u011br makra...'
            mesg2 = u'Pros\xedm vyberte makro, kter\xe9 by m\u011blo b\xfdt spu\u0161t\u011bno,\npokud v\xfdsledek ur\u010dit\xe9 akce odpov\xedd\xe1 podm\xednce.'
            text1 = u'Jestli\u017ee:'
            text2 = u'Sko\u010dit na:'
            text3 = u'a vr\xe1tit se po vykon\xe1n\xed'
        class PythonCommand:
            name = u'P\u0159\xedkaz jazyka Python'
            description = u'Provede zadan\xfd jednoduch\xfd p\u0159\xedkaz jazyka Python.'
            parameterDescription = u'P\u0159\xedkaz jazyka Python:'
        class PythonScript:
            name = u'Skript jazyka Python'
            description = u'Vykon\xe1 plnohodnotn\xfd skript jazyka Python.'
        class ShowOSD:
            name = u'Zobrazit OSD'
            description = u'Zobraz\xed jednoduch\xfd OSD.'
            alignment = u'Um\xedst\u011bn\xed:'
            alignmentChoices = [
                u'Naho\u0159e vlevo',
                u'Naho\u0159e vpravo',
                u'Dole vlevo',
                u'Dole vpravo',
                u'Uprost\u0159ed',
                u'Dole uprost\u0159ed',
                u'Naho\u0159e uprost\u0159ed',
                u'Vlevo uprost\u0159ed',
                u'Vpravo uprost\u0159ed',
            ]
            display = u'Zobrazit na:'
            editText = u'Text k zobrazen\xed:'
            label = u'Zobrazit OSD: %s'
            osdColour = u'Barva OSD:'
            osdFont = u'OSD p\xedsmo:'
            outlineFont = u'Obrys OSD'
            wait1 = u'Automaticky skr\xfdt OSD po'
            wait2 = u'sekund\xe1ch (0 = nikdy)'
            xOffset = u'Vodorovn\xfd ofset X:'
            yOffset = u'Svisl\xfd ofset Y:'
        class StopProcessing:
            name = u'Zastavit zpracov\xe1n\xed t\xe9to ud\xe1losti'
            description = u'Zastav\xed zpracov\xe1n\xed t\xe9to ud\xe1losti'
        class TriggerEvent:
            name = u'Vyvolat ud\xe1lost'
            description = u'Vyvol\xe1 po\u017eadovanou ud\xe1lost (voliteln\u011b po ur\u010dit\xe9m \u010dase).'
            labelWithTime = u'Vyvolat ud\xe1lost "%s" po %.2f sekund\xe1ch'
            labelWithoutTime = u'Vyvolat ud\xe1lost "%s"'
            text1 = u'Identifikace generovan\xe9 ud\xe1losti:'
            text2 = u'Prodleva p\u0159ed uvoln\u011bn\xedm ud\xe1losti:'
            text3 = u'sekund. (0 = uvolnit okam\u017eit\u011b)'
        class Wait:
            name = u'\u010cekat danou dobu'
            description = u'\u010cek\xe1 danou dobu'
            label = u'\u010cekat: %s sec'
            seconds = u'sekund'
            wait = u'\u010cekat'
    class System:
        name = u'Syst\xe9m'
        description = u'Syst\xe9m'
        forced = u'Nucen\xe9: %s'
        forcedCB = u'Nucen\u011b zav\u0159e v\u0161echny programy'
        class ChangeDisplaySettings:
            name = u'Zm\u011bnit nastaven\xed displeje'
            description = u'Zm\u011bn\xed nastaven\xed displeje'
        class ChangeMasterVolumeBy:
            name = u'Zm\u011bnit hlavn\xed hlasitost'
            description = u'Zm\u011bn\xed hlavn\xed hlasitost'
            text1 = u'Zm\u011bnit hlavn\xed hlasitost o'
            text2 = u'procent.'
        class Execute:
            name = u'Spustit aplikaci'
            description = u'Spust\xed program.'
            FilePath = u'Cesta ke spustiteln\xe9mu souboru:'
            Parameters = u'Parametry p\u0159\xedkazov\xe9 \u0159\xe1dky:'
            ProcessOptions = (
                u'Re\xe1ln\xfd \u010das',
                u'Nadpr\u016fm\u011brn\xe1',
                u'Norm\xe1ln\xed',
                u'Podpr\u016fm\u011brn\xe1',
                u'N\xedzk\xe1',
            )
            ProcessOptionsDesc = u'Priorita procesu:'
            WaitCheckbox = u'\u010cekat na dokon\u010den\xed'
            WindowOptions = (
                u'Norm\xe1ln\xed',
                u'Minimalizovan\xe9',
                u'Maximalizovan\xe9',
                u'Neviditeln\xe9',
            )
            WindowOptionsDesc = u'Velikost okna:'
            WorkingDir = u'Pracovn\xed slo\u017eka:'
            browseExecutableDialogTitle = u'Volba spustiteln\xe9ho souboru'
            browseWorkingDirDialogTitle = u'Volba pracovn\xed slo\u017eky'
            label = u'Spustit program: %s'
        class Hibernate:
            name = u'Uspat po\u010d\xedta\u010d'
            description = u'Tato funkce zastav\xed syst\xe9m, vypne nap\xe1jen\xed a zavede re\u017eim sp\xe1nku.'
        class LockWorkstation:
            name = u'Zamknout pracovn\xed stanici'
            description = u'Tato funkce po\u017e\xe1d\xe1 o zamknut\xed displeje pracovn\xed stanice. Zamknut\xed chr\xe1n\xed stanici p\u0159ed neautorizovan\xfdm pou\u017eit\xedm. Funkce m\xe1 stejn\xfd v\xfdsledek jako stisknut\xed kombinace Ctrl+Alt+Del a klepnut\xed na Zamknout pracovn\xed stanici (XP Professional).'
        class LogOff:
            name = u'Odhl\xe1sit aktu\xe1ln\xedho u\u017eivatele'
            description = u'Zastav\xed v\u0161echny procesy, b\u011b\u017e\xedc\xed v \xfa\u010dtu aktu\xe1ln\u011b p\u0159ihl\xe1\u0161en\xe9ho u\u017eivatele. Pak u\u017eivatele odhl\xe1s\xed.'
        class MonitorGroup:
            name = u'Displej'
            description = u'Tyto akce \u0159\xedd\xed nap\xe1jen\xed displeje po\u010d\xedta\u010de.'
        class MonitorPowerOff:
            name = u'P\u0159epnout monitor do stavu power-off'
            description = u'P\u0159epne displej do stavu power-off. To podporuje v\u011bt\u0161ina re\u017eim\u016f, \u0161et\u0159\xedc\xedch energii.'
        class MonitorPowerOn:
            name = u'Znovu povolit monitor'
            description = u'Zapne displej, pokud byl v re\u017eimu power-off nebo n\xedzk\xe9 spot\u0159eby. Tak\xe9 zastav\xed \u0161et\u0159i\u010d obrazovky.'
        class MonitorStandby:
            name = u'P\u0159epnout monitor do re\u017eimu stand-by'
            description = u'Nastav\xed re\u017eim n\xedzk\xe9 spot\u0159eby displeje.'
        class MuteOff:
            name = u'Zru\u0161it re\u017eim Ztlumit v\u0161e'
            description = u'Zru\u0161\xed re\u017eim Ztlumit v\u0161e'
        class MuteOn:
            name = u'Nastavit re\u017eim Ztlumit v\u0161e'
            description = u'Nastav\xed re\u017eim Ztlumit v\u0161e'
        class OpenDriveTray:
            name = u'Vysunout/zasunout dv\xed\u0159ka mechaniky'
            description = u'\u0158\xedd\xed dv\xed\u0159ka CD/DVD-ROM mechaniky.'
            driveLabel = u'Mechanika:'
            labels = [
                u'P\u0159esunout dv\xed\u0159ka mechaniky: %s',
                u'Vysunout dv\xed\u0159ka mechaniky: %s',
                u'Zasunout dv\xed\u0159ka mechaniky: %s',
            ]
            options = [
                u'Vysunout nebo zasunout dv\xed\u0159ka mechaniky (podle aktu\xe1ln\xedho stavu)',
                u'Pouze vysunout dv\xed\u0159ka mechaniky',
                u'Pouze zasunout dv\xed\u0159ka mechaniky',
            ]
            optionsLabel = u'Volba akce'
        class PlaySound:
            name = u'P\u0159ehr\xe1t zvuk'
            description = u'P\u0159ehraje zvuk'
            fileMask = u'Soubory wav (*.WAV)|*.wav|V\u0161echny soubory (*.*)|*.*'
            text1 = u'Cesta ke zvukov\xe9mu souboru:'
            text2 = u'\u010cekat na dokon\u010den\xed'
        class PowerDown:
            name = u'Vypnout po\u010d\xedta\u010d'
            description = u'Zastav\xed syst\xe9m a vypne nap\xe1jen\xed. Syst\xe9m mus\xed podporovat funkci power-off.'
        class PowerGroup:
            name = u'\u0158\xedzen\xed nap\xe1jen\xed'
            description = u'Tyto akce zastavuj\xed, usp\xe1vaj\xed, restartuj\xed nebo vyp\xednaj\xed po\u010d\xedta\u010d. Mohou tak\xe9 zamknout pracovn\xed stanici a odhl\xe1sit aktu\xe1ln\xedho u\u017eivatele.'
        class Reboot:
            name = u'Restartovat po\u010d\xedta\u010d'
            description = u'Zastav\xed syst\xe9m a restartuje po\u010d\xedta\u010d.'
        class RegistryChange:
            name = u'Zm\u011bnit hodnotu v registru'
            description = u'Zm\u011bn\xed hodnoty v registru windows'
            actions = (
                u'vytvo\u0159it nebo zm\u011bnit',
                u'zm\u011bnit pouze existuje-li',
                u'odstranit',
            )
            labels = (
                u'Zm\u011bnit "%s" na %s',
                u'Zm\u011bnit "%s" na %s pouze existuje-li',
                u'Odstranit "%s"',
            )
        class RegistryGroup:
            name = u'Registry'
            description = u'Vyhled\xe1v\xe1 nebo m\u011bn\xed hodnoty v registru windows.'
            actionText = u'Akce:'
            chooseText = u'Volba registrov\xe9ho kl\xed\u010de:'
            defaultText = u'(V\xfdchoz\xed)'
            keyOpenError = u'Chyba otev\u0159en\xed registrov\xe9ho kl\xed\u010de'
            keyText = u'Kl\xed\u010d:'
            keyText2 = u'Kl\xed\u010d'
            newValue = u'Nov\xe1 hodnota:'
            noKeyError = u'Kl\xed\u010d neexistuje'
            noNewValueError = u'Nov\xe1 hodnota neexistuje'
            noSubkeyError = u'Podkl\xed\u010d neexistuje'
            noTypeError = u'Typ neexistuje'
            noValueNameError = u'N\xe1zev hodnoty neexistuje'
            noValueText = u'hodnota nenalezena'
            oldType = u'Aktu\xe1ln\xed typ:'
            oldValue = u'Aktu\xe1ln\xed hodnota:'
            typeText = u'Typ:'
            valueChangeError = u'Chyba p\u0159i zm\u011bn\u011b hodnoty'
            valueName = u'N\xe1zev hodnoty:'
            valueText = u'Hodnota:'
        class RegistryQuery:
            name = u'Dotaz registru'
            description = u'Vyhled\xe1 \xfadaj v registru windows a vr\xe1t\xed nebo porovn\xe1 hodnoty'
            actions = (
                u'kontrola existuje-li',
                u'vr\xe1t\xed v\xfdsledek',
                u'porovn\xe1 s',
            )
            labels = (
                u'Zkontroluj, existuje-li "%s"',
                u'Vra\u0165 "%s" jako v\xfdsledek',
                u'Porovnej "%s" s %s',
            )
        class ResetIdleTimer:
            name = u'Resetovat dobu ne\u010dinnosti'
            description = u'Resetuje dobu ne\u010dinnosti'
        class SetClipboard:
            name = u'Zkop\xedrovat \u0159et\u011bzec do schr\xe1nky'
            description = u'Zkop\xedruje \u0159et\u011bzec znak\u016f do syst\xe9mov\xe9 schr\xe1nky.'
            error = u'Nemohu otev\u0159\xedt schr\xe1nku'
        class SetDisplayPreset:
            name = u'Nastavit p\u0159edvolby displeje'
            description = u'Nastav\xed p\u0159edvolby displeje'
            fields = (
                u'Za\u0159\xedzen\xed',
                u'Vlevo',
                u'Naho\u0159e',
                u'\u0160\xed\u0159ka',
                u'V\xfd\u0161ka',
                u'Kmito\u010det',
                u'Kvalita barev',
                u'P\u0159ipojeno',
                u'Prim\xe1rn\xed',
                u'Vlajky',
            )
            query = u'Zjitit aktu\xe1ln\xed nastaven\xed displeje'
        class SetIdleTime:
            name = u'Nastavit dobu pro ne\u010dinnost'
            description = u'Nastav\xed dobu pro generov\xe1n\xed ud\xe1losti ne\u010dinnost'
            label1 = u'\u010cekat'
            label2 = u'sekund p\u0159ed generov\xe1n\xedm ud\xe1losti ne\u010dinnost.'
        class SetMasterVolume:
            name = u'Nastavit hlavn\xed hlasitost'
            description = u'Nastav\xed hlavn\xed hlasitost'
            text1 = u'Nastavit hlavn\xed hlasitost na'
            text2 = u'procent.'
        class SetSystemIdleTimer:
            name = u'Nastavit syst\xe9mov\xfd \u010dasova\u010d doby ne\u010dinnosti'
            description = u'Nastav\xed syst\xe9mov\xfd \u010dasova\u010d doby ne\u010dinnosti'
            choices = [
                u'Z\xe1kaz syst\xe9mov\xe9ho \u010dasova\u010de doby ne\u010dinnosti',
                u'Povolen\xed syst\xe9mov\xe9ho \u010dasova\u010de doby ne\u010dinnosti',
            ]
            text = u'Zvolte mo\u017enost:'
        class SetWallpaper:
            name = u'Zm\u011bnit tapetu'
            description = u'Zm\u011bn\xed tapetu'
            choices = (
                u'Na st\u0159ed',
                u'Vedle sebe',
                u'Rozt\xe1hnout',
            )
            fileMask = u'V\u0161echny soubory obr\xe1zk\u016f|*.jpg;*.bmp;*.gif|V\u0161echny soubory (*.*)|*.*'
            text1 = u'Cesta k souboru s obr\xe1zkem:'
            text2 = u'Pozice:'
        class ShowPicture:
            name = u'Zobrazit obr\xe1zek'
            description = u'Zobraz\xed obr\xe1zek'
            allFiles = u'V\u0161echny soubory'
            allImageFiles = u'V\u0161echny soubory typu obr\xe1zek'
            display = u'Monitor'
            path = u'Cesta k obr\xe1zku (pro vymaz\xe1n\xed pou\u017eijte pr\xe1zdnou cestu):'
        class SoundGroup:
            name = u'Zvukov\xe1 karta'
            description = u'Tyto akce ovl\xe1daj\xed zvukovou kartu va\u0161eho po\u010d\xedta\u010de.'
        class Standby:
            name = u'Uv\xe9st po\u010d\xedta\u010d do re\u017eimu standby'
            description = u'Tato funkce usp\xed syst\xe9m vypnut\xedm nap\xe1jen\xed a uveden\xedm do stavu sp\xe1nku.'
        class StartScreenSaver:
            name = u'Spustit \u0161et\u0159i\u010d obrazovky'
            description = u'Spust\xed \u0161et\u0159i\u010d obrazovky, vybran\xfd v nastaven\xed windows.'
        class ToggleMute:
            name = u'Nastavit/zru\u0161it re\u017eim Ztlumit v\u0161e'
            description = u'Nastav\xed/zru\u0161\xed re\u017eim Ztlumit v\u0161e'
        class WakeOnLan:
            name = u'Probudit po\u010d\xedta\u010d po s\xedti'
            description = u'Probud\xed po\u010d\xedta\u010d vysl\xe1n\xedm speci\xe1ln\xedho s\xed\u0165ov\xe9ho paketu. \n\nJe t\u0159eba uv\xe9st MAC adresu po\u010d\xedta\u010de ve tvaru:<p><i>00-13-D4-9A-2F-04</i> nebo<br><i>00:13:D4:9A:2F:04</i> '
            parameterDescription = u'MAC adresa po\u010d\xedta\u010de, kter\xfd m\xe1 b\xfdt probuzen:'
    class Window:
        name = u'Okno'
        description = u'Akce spojen\xe9 s \u0159\xedzen\xedm okna na obrazovce, jako nalezen\xed ur\u010dit\xe9ho okna, p\u0159esun, zm\u011bna velikosti a odesl\xe1n\xed stisk\u016f kl\xe1ves k ur\u010dit\xe9mu oknu.'
        class BringToFront:
            name = u'P\u0159en\xe9st do pop\u0159ed\xed'
            description = u'P\u0159enese ur\u010den\xe9 okno do pop\u0159ed\xed.'
        class Close:
            name = u'Zav\u0159\xedt'
            description = u'Zav\u0159e okno aplikace'
        class FindWindow:
            name = u'Naj\xedt okno'
            description = u'Najde uveden\xe9 okno.'
            drag1 = u'P\u0159et\xe1hn\u011bte m\u011b\ndo okna.'
            drag2 = u'Te\u010f m\u011b p\u0159esu\u0148te\ndo okna.'
            hide_box = u'Skr\xfdt EventGhost b\u011bhem p\u0159esouv\xe1n\xed'
            invisible_box = u'Hledat tak\xe9 neviditeln\xe9 polo\u017eky'
            label = u'Naj\xedt okno: %s'
            label2 = u'Naj\xedt okno, kter\xe9 je nejv\xedce v pop\u0159ed\xed'
            matchNum1 = u'Vr\xe1tit pouze'
            matchNum2 = u'. nalezen\xe9 okno'
            onlyForground = u'Pouze okno, kter\xe9 je nejv\xedce v pop\u0159ed\xed'
            options = (
                u'Aplikace:',
                u'Jm\xe9no okna:',
                u'T\u0159\xedda okna:',
                u'Jm\xe9no potomka:',
                u'T\u0159\xedda potomka:',
            )
            refresh_btn = u'&Aktualizovat'
            stopMacro = [
                u'Zastavit makro, jestli\u017ee c\xedl nen\xed nalezen',
                u'Zastavit makro, jestli\u017ee c\xedl je nalezen',
                u'Nikdy nezastavovat makro',
            ]
            testButton = u'Test'
            wait1 = u'\u010cekat a\u017e'
            wait2 = u'sekund na objeven\xed se okna.'
        class Maximize:
            name = u'Maximalizovat'
            description = u'Maximalizuje okno'
        class Minimize:
            name = u'Minimalizovat'
            description = u'Minimalizuje okno'
        class MoveTo:
            name = u'P\u0159esunout absolutn\u011b'
            description = u'P\u0159esune okno na dan\xe9 m\xedsto'
            label = u'P\u0159esunout okno na %s'
            text1 = u'Nastavit horizont\xe1ln\xed pozici X na'
            text2 = u'pixel\u016f'
            text3 = u'Nastavit vertik\xe1ln\xed pozici Y na'
            text4 = u'pixel\u016f'
        class Resize:
            name = u'Zm\u011bnit velikost'
            description = u'Zm\u011bn\xed velikost okna.'
            label = u'Zm\u011bnit velikost okna na %s, %s'
            text1 = u'Nastavit \u0161\xed\u0159ku na'
            text2 = u'pixel\u016f'
            text3 = u'Nastavit v\xfd\u0161ku na'
            text4 = u'pixel\u016f'
        class Restore:
            name = u'Obnovit'
            description = u'Obnov\xed okno'
        class SendKeys:
            name = u'Emulovat stisk kl\xe1ves'
            description = u'Tato akce emuluje stisk kl\xe1ves pro ovl\xe1d\xe1n\xed ostatn\xedch program\u016f.\nZnaky, kter\xe9 jsou k ovl\xe1d\xe1n\xed pot\u0159eba, napi\u0161te do edita\u010dn\xedho pole.\n\n<p>\nPro emulov\xe1n\xed speci\xe1ln\xedch kl\xe1ves je t\u0159eba pou\u017e\xedt kl\xed\u010dov\xe1 slova a uzav\u0159\xedt je\ndo slo\u017een\xfdch z\xe1vorek. Nap\u0159\xedklad chcete-li pou\u017e\xedt kl\xe1vesu "\u0161ipka nahoru",\nnapi\u0161te <b>{Up}</b>. Pro zkombinov\xe1n\xed v\xedce kl\xe1ves m\u016f\u017eete kombinovat\nv\xedce kl\xed\u010dov\xfdch slov (znak\u016f) pomoc\xed znam\xe9nka plus jako: <b>{Shift+Ctrl+F1}</b>\nnebo <b>{Ctrl+V}</b>. P\u0159i z\xe1pisu kl\xed\u010dov\xfdch slov nez\xe1le\u017e\xed na velikosti pou\u017eit\xfdch\nznak\u016f, tak\u017ee m\u016f\u017eete napsat tak\xe9 {SHIFT+ctrl+F1}, pokud se v\xe1m to l\xedb\xed.\n<p>\nPokud je u n\u011bkter\xfdch kl\xe1ves t\u0159eba rozli\u0161ovat mezi kl\xe1vesou na lev\xe9 a prav\xe9 stran\u011b\nkl\xe1vesnice (jako t\u0159eba u kl\xe1vesy s logem Windows), mohou b\xfdt kl\xed\u010dov\xe1 slova\nozna\u010dena p\u0159edponou "L" nebo "R":\n<br><b>{Win}</b> nebo <b>{LWin}</b> nebo <b>{RWin}</b>\n<p>\nA tady je seznam zbytku kl\xed\u010dov\xfdch slov, ker\xfdm EventGhost rozum\xed:<br>\n<b>{Ctrl}</b> nebo <b>{Control}<br>\n{Shift}<br>\n{Alt}<br>\n{Return}</b> nebo <b>{Enter}<br>\n{Back}</b> nebo <b>{Backspace}<br>\n{Tab}</b> nebo <b>{Tabulator}<br>\n{Esc}</b> nebo <b>{Escape}<br>\n{Spc}</b> nebo <b>{Space}<br>\n{Up}<br>\n{Down}<br>\n{Left}<br>\n{Right}<br>\n{PgUp}</b> nebo <b>{PageUp}<br>\n{PgDown}</b> nebo <b>{PageDown}<br>\n{Home}<br>\n{End}<br>\n{Ins}</b> nebo <b>{Insert}<br>\n{Del}</b> nebo <b>{Delete}<br>\n{Pause}<br>{Capslock}<br>\n{Numlock}<br>\n{Scrolllock}<br>\n{F1}, {F2}, ... , {F24}<br>\n{Apps}</b> (To je kl\xe1vesa kontextov\xe9 nab\xeddky)<b><br>\n<br>\n</b>Toto bude emulovat kl\xe1vesy numerick\xe9 kl\xe1vesnice:<b><br>\n{Divide}<br>\n{Multiply}<br>\n{Subtract}<br>\n{Add}<br>\n{Decimal}<br>\n{Numpad0}, {Numpad1}, ... , {Numpad9}</b>'
            insertButton = u'&Vlo\u017eit'
            specialKeyTool = u'N\xe1stroj pro zvl\xe1\u0161tn\xed kl\xe1vesy'
            textToType = u'Text k emulov\xe1n\xed:'
            useAlternativeMethod = u'Pou\u017e\xedt alternativn\xed metodu emulov\xe1n\xed stisknut\xfdch kl\xe1ves'
            class Keys:
                backspace = u'Kl\xe1vesa maz\xe1n\xed (Backspace)'
                context = u'Kl\xe1vesa kontextov\xe9 nab\xeddky'
                delete = u'Delete'
                down = u'\u0160ipka dol\u016f'
                end = u'End'
                enter = u'Enter (na num. kl\xe1vesnici)'
                escape = u'Escape'
                home = u'Home'
                insert = u'Insert'
                left = u'\u0160ipka vlevo'
                num0 = u'0 na numerick\xe9 kl\xe1vesnici'
                num1 = u'1 na numerick\xe9 kl\xe1vesnici'
                num2 = u'2 na numerick\xe9 kl\xe1vesnici'
                num3 = u'3 na numerick\xe9 kl\xe1vesnici'
                num4 = u'4 na numerick\xe9 kl\xe1vesnici'
                num5 = u'5 na numerick\xe9 kl\xe1vesnici'
                num6 = u'6 na numerick\xe9 kl\xe1vesnici'
                num7 = u'7 na numerick\xe9 kl\xe1vesnici'
                num8 = u'8 na numerick\xe9 kl\xe1vesnici'
                num9 = u'9 na numerick\xe9 kl\xe1vesnici'
                numAdd = u'+ na numerick\xe9 kl\xe1vesnici'
                numDecimal = u'Te\u010dka na numerick\xe9 kl\xe1vesnici'
                numDivide = u'/ na numerick\xe9 kl\xe1vesnici'
                numMultiply = u'* na numerick\xe9 kl\xe1vesnici'
                numSubtract = u'- na numerick\xe9 kl\xe1vesnici'
                pageDown = u'Page Down'
                pageUp = u'Page Up'
                returnKey = u'Enter'
                right = u'\u0160ipka vpravo'
                space = u'Mezern\xedk'
                tabulator = u'Tabel\xe1tor'
                up = u'\u0160ipka nahoru'
                win = u'Kl\xe1vesa s logem Windows'
        class SendMessage:
            name = u'Poslat zpr\xe1vu'
            description = u'Pou\u017eije Windows-API funkci "SendMessage" pro odesl\xe1n\xed speci\xe1ln\xed zpr\xe1vy oknu. M\u016f\u017ee tak\xe9 pou\u017e\xedt "PostMessage", je-li to po\u017eadov\xe1no.'
            text1 = u'Pou\u017e\xedt PostMessage m\xedsto SendMessage'
        class SetAlwaysOnTop:
            name = u'Nastavit vlastnost "V\u017edy na vrchu"'
            description = u'Nastav\xed vlastnost "V\u017edy na vrchu"'
            actions = (
                u'Zru\u0161it vlastnost "V\u017edy na vrchu"',
                u'Nastavit vlastnost "V\u017edy na vrchu"',
                u'Nastavit/zru\u0161it vlastnost "V\u017edy na vrchu"',
            )
            radioBox = u'Zvolte akci:'
    class Mouse:
        name = u'My\u0161'
        description = u'Akce k \u0159\xedzen\xed ukazatele my\u0161i a emulov\xe1n\xed ud\xe1lost\xed, generovan\xfdch my\u0161\xed.'
        class GoDirection:
            name = u'Spustit pohyb my\u0161i'
            description = u'Spust\xed pohyb my\u0161i dan\xfdm sm\u011brem'
            label = u'Spustit pohyb my\u0161i sm\u011brem %.2f\xb0'
            text1 = u'Spustit pohyb ukazatele my\u0161i pod \xfahlem'
            text2 = u'stup\u0148\u016f. (0-360)'
        class LeftButton:
            name = u'Lev\xe9 tla\u010d\xedtko my\u0161i'
            description = u'Lev\xe9 tla\u010d\xedtko my\u0161i'
        class LeftDoubleClick:
            name = u'Poklepat lev\xfdm tla\u010d\xedtkem my\u0161i'
            description = u'Emuluje poklep\xe1n\xed lev\xfdm tla\u010d\xedtkem my\u0161i'
        class MiddleButton:
            name = u'Prost\u0159edn\xed tla\u010d\xedtko my\u0161i'
            description = u'Prost\u0159edn\xed tla\u010d\xedtko my\u0161i'
        class MouseWheel:
            name = u'Emulovat pohyb kole\u010dka my\u0161i'
            description = u'Emuluje pohyb kole\u010dka my\u0161i'
            label = u'Kole\u010dkem my\u0161i oto\u010dit o %d zoubk\u016f'
            text1 = u'Oto\u010dit kole\u010dkem my\u0161i o'
            text2 = u'zoubk\u016f. (Z\xe1porn\xe1 hodnota znamen\xe1 sm\u011br dol\u016f)'
        class MoveAbsolute:
            name = u'Absolutn\u011b p\u0159esunout'
            description = u'P\u0159esune ukazatel my\u0161i na absolutn\u011b udan\xe9 sou\u0159adnice'
            label = u'P\u0159esunout my\u0161 na x:%s, y:%s'
            text1 = u'Nastavit horizont\xe1ln\xed pozici X na'
            text2 = u'pixel\u016f'
            text3 = u'Nastavit vertik\xe1ln\xed pozici Y na'
            text4 = u'pixel\u016f'
        class RightButton:
            name = u'Prav\xe9 tla\u010d\xedtko my\u0161i'
            description = u'Prav\xe9 tla\u010d\xedtko my\u0161i'
        class RightDoubleClick:
            name = u'Poklepat prav\xfdm tla\u010d\xedtkem my\u0161i'
            description = u'Emuluje poklep\xe1n\xed prav\xfdm tla\u010d\xedtkem my\u0161i'
        class ToggleLeftButton:
            name = u'Zm\u011bnit stav lev\xe9ho tla\u010d\xedtka my\u0161i'
            description = u'Zm\u011bn\xed stav lev\xe9ho tla\u010d\xedtka my\u0161i'
    class Billy:
        name = u'Billy'
        description = u'P\u0159id\xe1v\xe1 akce k \u0159\xedzen\xed audio p\u0159ehr\xe1va\u010de <a href="http://www.sheepfriends.com/?page=billy">Billy</a>. \n\n<p><BR><B>POZOR !<BR>Spr\xe1vn\u011b pracuje pouze s beta verz\xed 1.04b p\u0159ehr\xe1va\u010de Billy !</B><BR>Se star\u0161\xed verz\xed bude plugin pracovat v omezen\xe9m re\u017eimu !</p>'
        filemask = u'Billy.exe|Billy.exe|V\u0161echny soubory (*.*)|*.*'
        grpDescription1 = u'Skupina nejd\u016fle\u017eit\u011bj\u0161\xedch akc\xed k ovl\xe1d\xe1n\xed p\u0159ehr\xe1va\u010de Billy'
        grpDescription2 = u'Skupina akc\xed pro pr\xe1ci se seznamy audiosoubor\u016f'
        grpDescription3 = u'Skupina zvl\xe1\u0161tn\xedch akc\xed (nap\u0159. reset mixeru Windows)'
        grpDescription4 = u'Skupina akc\xed pro pr\xe1ci s Obl\xedben\xfdmi'
        grpName1 = u'Hlavn\xed'
        grpName2 = u'Seznamy'
        grpName3 = u'Zvl\xe1\u0161tn\xed akce'
        grpName4 = u'Obl\xedben\xe9'
        label = u'Cesta k souboru Billy.exe:'
        text1 = u'Nemohu naj\xedt okno p\u0159ehr\xe1va\u010de Billy !'
        title = u'Napsal Pako podle n\u011bkter\xfdch plugin\u016f od autor\u016f MonsterMagnet a Bitmonster'
        version = u'Verze: '
        class AddFile:
            name = u'P\u0159idat soubor(y)'
            description = u'Otev\u0159e dialog pro p\u0159id\xe1n\xed souboru(\u016f).'
        class AddFolder:
            name = u'P\u0159idat slo\u017eku'
            description = u'Otev\u0159e dialog pro p\u0159id\xe1n\xed slo\u017eky s audio soubory.'
        class AddPlistToFav:
            name = u'P\u0159idat seznam k Obl\xedben\xfdm'
            description = u'P\u0159id\xe1 seznam k Obl\xedben\xfdm.'
        class AddURL:
            name = u'P\u0159idat internetov\xe9 radio'
            description = u'P\u0159id\xe1 internetov\xe9 radio.'
        class CheckNewFiles:
            name = u'Zkontrolovat nov\xe9 soubory'
            description = u'Zkontroluje, zda ve slo\u017ece nejsou nov\xe9 soubory.'
        class ClearHistory:
            name = u'Vy\u010distit historii p\u0159ehran\xfdch nebo ozna\u010den\xfdch soubor\u016f'
            description = u'Odstran\xed ozna\u010den\xed p\u0159ehran\xfdch a do fronty za\u0159azen\xfdch soubor\u016f.'
        class ClearList:
            name = u'Vy\u010distit seznam'
            description = u'Vy\u010dist\xed seznam.'
        class CopyEntry:
            name = u'Kop\xedrovat polo\u017eku seznamu'
            description = u'Kop\xedruje polo\u017eku seznamu do schr\xe1nky.'
        class CropQueued:
            name = u'Odstranit neozna\u010den\xe9'
            description = u'"Odst\u0159ihne" ozna\u010den\xe9 polo\u017eky seznamu (neozna\u010den\xe9 odstran\xed).'
        class CutEntry:
            name = u'Vyjmout polo\u017eku seznamu'
            description = u'Vyjme polo\u017eku seznamu (zkop\xedruje do schr\xe1nky).'
        class Delete:
            name = u'Hodit soubor do ko\u0161e'
            description = u'Odstran\xed soubor (do ko\u0161e).'
        class EditEntry:
            name = u'Editovat polo\u017eku seznamu'
            description = u'Otev\u0159e dialog pro editaci polo\u017eky seznamu.'
        class ExitBilly:
            name = u'Ukon\u010dit Billy'
            description = u'Ukon\u010d\xed b\u011bh p\u0159ehr\xe1va\u010de Billy.'
        class Explore:
            name = u'Otev\u0159\xedt slo\u017eku'
            description = u'Otev\u0159e slo\u017eku s pr\xe1v\u011b p\u0159ehr\xe1van\xfdm souborem.'
        class Find:
            name = u'Naj\xedt'
            description = u'Otev\u0159e dialog pro hled\xe1n\xed v aktu\xe1ln\xedm seznamu.'
        class LoadFav1:
            name = u'Zav\xe9st Obl\xedben\xe9 1'
            description = u'Zavede se seznam Obl\xedben\xe9 1.'
        class LoadFav2:
            name = u'Zav\xe9st Obl\xedben\xe9 2'
            description = u'Zavede se seznam Obl\xedben\xe9 2.'
        class LoadFav3:
            name = u'Zav\xe9st Obl\xedben\xe9 3'
            description = u'Zavede se seznam Obl\xedben\xe9 3.'
        class LoadFav4:
            name = u'Zav\xe9st Obl\xedben\xe9 4'
            description = u'Zavede se seznam Obl\xedben\xe9 4.'
        class LoadFav5:
            name = u'Zav\xe9st Obl\xedben\xe9 5'
            description = u'Zavede se seznam Obl\xedben\xe9 5.'
        class LoadFav6:
            name = u'Zav\xe9st Obl\xedben\xe9 6'
            description = u'Zavede se seznam Obl\xedben\xe9 6.'
        class LoadFav7:
            name = u'Zav\xe9st Obl\xedben\xe9 7'
            description = u'Zavede se seznam Obl\xedben\xe9 7.'
        class LoadFav8:
            name = u'Zav\xe9st Obl\xedben\xe9 8'
            description = u'Zavede se seznam Obl\xedben\xe9 8.'
        class LoadFav9:
            name = u'Zav\xe9st Obl\xedben\xe9 9'
            description = u'Zavede se seznam Obl\xedben\xe9 9.'
        class Minimize:
            name = u'Minimalizovat do oznamovac\xed oblasti'
            description = u'P\u0159ehr\xe1va\u010d se minimalizuje do oznamovac\xed oblasti.'
        class Next:
            name = u'Dal\u0161\xed'
            description = u'P\u0159esko\u010d\xed na dal\u0161\xed soubor (skladbu).'
        class OpenFolder:
            name = u'Otev\u0159\xedt slo\u017eku'
            description = u'Otev\u0159e slo\u017eku s audiosoubory.'
        class OpenPlaylist:
            name = u'Otev\u0159\xedt seznam'
            description = u'Otev\u0159e (zavede) seznam.'
        class OrganizeFav:
            name = u'Organizovat Obl\xedben\xe9'
            description = u'Otev\u0159e dialog pro organizaci Obl\xedben\xfdch.'
        class PasteEntry:
            name = u'Vlo\u017eit polo\u017eku seznamu'
            description = u'Vlo\u017e\xed polo\u017eku seznamu ze schr\xe1nky.'
        class PausePlay:
            name = u'Pozastavit/P\u0159ehr\xe1t'
            description = u'Pozastav\xed/spust\xed p\u0159ehr\xe1v\xe1n\xed.'
        class Play:
            name = u'P\u0159ehr\xe1t'
            description = u'Spust\xed p\u0159ehr\xe1v\xe1n\xed.'
        class Previous:
            name = u'P\u0159edchoz\xed'
            description = u'P\u0159esko\xed na p\u0159edchoz\xed soubor (skladbu).'
        class Properties:
            name = u'Vlastnosti'
            description = u'Otev\u0159e dialog pro editaci nebo hromadn\xe9 p\u0159ejmenov\xe1n\xed (p\u0159i v\xedcen\xe1sobn\xe9m v\xfdb\u011bru).'
        class Queue:
            name = u'Za\u0159adit do fronty'
            description = u'Vybran\xfd soubor za\u0159ad\xed do fronty.'
        class Record:
            name = u'Ukl\xe1dat internetov\xe9 radio'
            description = u'Ukl\xe1dat internetov\xe9 radio do souboru.'
        class Remove:
            name = u'Odstranit soubor ze seznamu'
            description = u'Odstran\xed soubor ze seznamu.'
        class ResetMixer:
            name = u'Resetovat mixer Windows'
            description = u'Resetuje mixer Windows.'
        class Run:
            name = u'Spustit nebo obnovit'
            description = u'Spou\u0161t\xed p\u0159ehr\xe1va\u010d Billy s jeho defaultn\xedm nastaven\xedm nebo ho obnov\xed.'
            text2 = u'Nemohu naj\xedt soubor Billy.exe !'
        class SavePlaylist:
            name = u'Ulo\u017eit seznam'
            description = u'Otev\u0159e dialog pro ulo\u017een\xed seznamu.'
        class Settings:
            name = u'Nastaven\xed'
            description = u'Otev\u0159e nab\xeddku nastaven\xed p\u0159ehr\xe1va\u010de Billy.'
        class Stop:
            name = u'Zastavit'
            description = u'Zastav\xed p\u0159ehr\xe1v\xe1n\xed.'
        class ToStart:
            name = u'Sko\u010dit na za\u010d\xe1tek souboru'
            description = u'Sko\u010d\xed na za\u010d\xe1tek p\u0159ehr\xe1van\xe9ho souboru.'
        class TogglePlayMode:
            name = u'Zm\u011bnit re\u017eim p\u0159ehr\xe1v\xe1n\xed'
            description = u'Zm\u011bn\xed re\u017eim p\u0159ehr\xe1v\xe1n\xed.'
        class ToggleViewMode:
            name = u'Zm\u011bnit zp\u016fsob zobrazen\xed'
            description = u'Zm\u011bn\xed zp\u016fsob zobrazen\xed seznamu.'
    class DesktopRemote:
        name = u'Ovlada\u010d na pracovn\xed plo\u0161e'
        description = u'Na pracovn\xed plo\u0161e vykresl\xed okno v podob\u011b d\xe1lkov\xe9ho ovlada\u010de'
        class AddButton:
            name = u'P\u0159idat tla\u010d\xedtko'
            description = u'P\u0159id\xe1 tla\u010d\xedtko'
            event = u'Ud\xe1lost:'
            label = u'N\xe1pis:'
        class CreateNew:
            name = u'Vytvo\u0159it nov\xfd ovlada\u010d'
            description = u'Vytvo\u0159\xed nov\xfd ovlada\u010d'
        class Show:
            name = u'Zobrazit'
            description = u'Zobraz\xed vytvo\u0159en\xfd ovlada\u010d'
        class StartNewLine:
            name = u'Za\u010d\xedt nov\xfd \u0159\xe1dek'
            description = u'Za\u010dne na nov\xe9m \u0159\xe1dku'
    class DirectoryWatcher:
        name = u'Hl\xedda\u010d slo\u017eky'
        description = u'Generuje ud\xe1losti, jestli\u017ee soubory v ur\u010den\xe9 slo\u017ece jsou vytvo\u0159eny, smaz\xe1ny\nnebo zm\u011bn\u011bny.'
        watchPath = u'Hl\xeddan\xe1 slo\u017eka:'
        watchSubDirs = u'Hl\xeddat i podslo\u017eky'
    class Egon:
        name = u'Egon'
        description = u'Hardwarov\xfd plugin pro IR USB p\u0159ij\xedma\u010d <a href="http://ruckl.wz.cz/egon/egon.html">Egon</a>.\n\n<p><img src="Egon_top.png" /><BR><B><U>Charakteristika:</U></B><BR>Mal\xfd, jednoduch\xfd, minimum sou\u010d\xe1stek, jednostrann\xfd pl. spoj spoj\u016f<BR>Mo\u017enost upgrade firmware pomoc\xed bootloaderu<BR>Konfigurovateln\xfd pomoc\xed termin\xe1lov\xe9ho programu<BR>Aktu\xe1ln\xed verze rozpozn\xe1 17 IR protokol\u016f (nap\u0159. RC5 apod.)<BR>Implementov\xe1n re\u017eim pro anal\xfdzu nezn\xe1m\xe9ho protokolu<BR><BR><I>Konstrukce je zdarma pro nekomer\u010dn\xed pou\u017eit\xed</I>'
        error = u'Nemohu otev\u0159\xedt virtu\xe1ln\xed s\xe9riov\xfd port'
        port = u'Virtu\xe1ln\xed s\xe9riov\xfd port:'
    class Foobar2000:
        name = u'Foobar2000'
        description = u'P\u0159id\xe1v\xe1 podporu funkc\xed pro \u0159\xedzen\xed aplikace Foobar2000.\n\n<p><a href="http://www.foobar2000.org/">Domovsk\xe1 str\xe1nka aplikace Foobar2000</a>'
        class Exit:
            name = u'Ukon\u010dit'
            description = u'Ukon\u010d\xed foobar.'
        class Hide:
            name = u'Skr\xfdt'
            description = u'Skryje okno aplikace foobar.'
        class NextTrack:
            name = u'Dal\u0161\xed stopa'
            description = u'Emuluje stisk tla\u010d\xedtka Dal\u0161\xed stopa (Next track).'
        class Pause:
            name = u'Pozastavit'
            description = u'Emuluje stisk tla\u010d\xedtka Pozastavit (Pausa).'
        class Play:
            name = u'P\u0159ehr\xe1t'
            description = u'Emuluje stisk tla\u010d\xedtka P\u0159ehr\xe1t (Play).'
        class PlayPause:
            name = u'Zm\u011bnit stav P\u0159ehr\xe1t/Pozastavit'
            description = u'Emuluje stisk tla\u010d\xedtka P\u0159ehr\xe1t/Pozastavit (Play/Pausa).'
        class PreviousTrack:
            name = u'P\u0159edchoz\xed stopa'
            description = u'Emuluje stisk tla\u010d\xedtka P\u0159edchoz\xed stopa (Previous track).'
        class Random:
            name = u'N\xe1hodn\u011b'
            description = u'Emuluje stisk tla\u010d\xedtka N\xe1hodn\u011b (Random).'
        class Run:
            name = u'Spustit'
            description = u'Spust\xed foobar s aktu\xe1ln\xedmi p\u0159edvolbami.'
        class Show:
            name = u'Obnovit'
            description = u'Otev\u0159e okno aplikace foobar.'
        class Stop:
            name = u'Zastavit'
            description = u'Emuluje stisk tla\u010d\xedtka Zastavit (Stop).'
    class IgorPlugUSB:
        name = u'IgorPlug-USB'
        description = u'Plugin pro IR p\u0159ij\xedma\u010d od Igora \u010ce\u0161ka.\n\n<p><a href="http://www.cesko.host.sk/">Domovsk\xe1 str\xe1nka Igora \u010ce\u0161ka</a></center>'
    class Joystick:
        name = u'P\xe1kov\xfd ovlada\u010d'
        description = u'Umo\u017e\u0148uje pou\u017e\xedt p\xe1kov\xe9 ovlada\u010de a gamepady jako vstupn\xed za\u0159\xedzen\xed pro EventGhost.'
    class Keyboard:
        name = u'Kl\xe1vesnice'
        description = u'Tento plugin generuje ud\xe1losti stisknut\xedm kl\xe1ves (hork\xe9 kl\xe1vesy).'
    class MediaPlayerClassic:
        name = u'Media Player Classic'
        description = u'P\u0159id\xe1v\xe1 podporu funkc\xed k ovl\xe1d\xe1n\xed aplikace  Media Player Classic.\n\n<p>Pouze pro verzi <b>6.4.8.9</b> nebo nov\u011bj\u0161\xed.</p>\n<p>Plugin nebude pracovat se star\u0161\xedmi verzemi MPC !</p>\n<p>\n<a href=http://www.eventghost.org/forum/viewtopic.php?t=17>Hl\xe1\u0161en\xed o chyb\xe1ch</a></p>\n<p><a href=http://sourceforge.net/projects/guliverkli/>\nMedia Player Classic SourceForge Project</a></p>'
        class AlwaysOnTop:
            name = u'V\u017edy na vrchu'
            description = u'V\u017edy na vrchu'
        class AudioDelayAdd10ms:
            name = u'Zpo\u017ed\u011bn\xed zvuku +10ms'
            description = u'Zpo\u017ed\u011bn\xed zvuku +10ms'
        class AudioDelaySub10ms:
            name = u'Zpo\u017ed\u011bn\xed zvuku -10ms'
            description = u'Zpo\u017ed\u011bn\xed zvuku -10ms'
        class BossKey:
            name = u'Tla\u010d\xedtko "\u0160\xe9f" (Boss)'
            description = u'Tla\u010d\xedtko "\u0160\xe9f" (Boss)'
        class Close:
            name = u'Zav\u0159\xedt soubor'
            description = u'Zav\u0159e soubor'
        class DVDAngleMenu:
            name = u'DVD nab\xeddka \xfahl\u016f pohledu'
            description = u'DVD nab\xeddka \xfahl\u016f pohledu'
        class DVDAudioMenu:
            name = u'DVD nab\xeddka - zvuk'
            description = u'DVD nab\xeddka - zvuk'
        class DVDChapterMenu:
            name = u'DVD nab\xeddka - kapitola'
            description = u'DVD nab\xeddka - kapitola'
        class DVDMenuActivate:
            name = u'DVD - aktivace nab\xeddky'
            description = u'DVD - aktivace nab\xeddky'
        class DVDMenuBack:
            name = u'DVD nab\xeddka - zp\u011bt'
            description = u'DVD nab\xeddka - zp\u011bt'
        class DVDMenuDown:
            name = u'DVD nab\xeddka - dol\u016f'
            description = u'DVD nab\xeddka - dol\u016f'
        class DVDMenuLeave:
            name = u'DVD nab\xeddka - opu\u0161t\u011bn\xed'
            description = u'DVD nab\xeddka - opu\u0161t\u011bn\xed'
        class DVDMenuLeft:
            name = u'DVD nab\xeddka - vlevo'
            description = u'DVD nab\xeddka - vlevo'
        class DVDMenuRight:
            name = u'DVD nab\xeddka - vpravo'
            description = u'DVD nab\xeddka - vpravo'
        class DVDMenuUp:
            name = u'DVD nab\xeddka - nahoru'
            description = u'DVD nab\xeddka - nahoru'
        class DVDNextAngle:
            name = u'DVD - dal\u0161\xed \xfahel pohledu'
            description = u'DVD - dal\u0161\xed \xfahel pohledu'
        class DVDNextAudio:
            name = u'DVD - dal\u0161\xed zvukov\xe1 stopa'
            description = u'DVD - dal\u0161\xed zvukov\xe1 stopa'
        class DVDNextSubtitle:
            name = u'DVD - dal\u0161\xed titulky'
            description = u'DVD - dal\u0161\xed titulky'
        class DVDOnOffSubtitle:
            name = u'DVD - zapnout/vypnout titulky'
            description = u'DVD - zapne/vypne titulky'
        class DVDPrevAngle:
            name = u'DVD - p\u0159edchoz\xed \xfahel pohledu'
            description = u'DVD - p\u0159edchoz\xed \xfahel pohledu'
        class DVDPrevAudio:
            name = u'DVD - p\u0159edchoz\xed zvukov\xe1 stopa'
            description = u'DVD - p\u0159edchoz\xed zvukov\xe1 stopa'
        class DVDPrevSubtitle:
            name = u'DVD - p\u0159edchoz\xed titulky'
            description = u'DVD - p\u0159edchoz\xed titulky'
        class DVDRootMenu:
            name = u'DVD - hlavn\xed nab\xeddka'
            description = u'DVD - hlavn\xed nab\xeddka'
        class DVDSubtitleMenu:
            name = u'DVD - nab\xeddka titulk\u016f'
            description = u'DVD - nab\xeddka titulk\u016f'
        class DVDTitleMenu:
            name = u'DVD - \xfavodn\xed nab\xeddka'
            description = u'DVD - \xfavodn\xed nab\xeddka'
        class DecreaseRate:
            name = u'Sn\xed\u017eit rychlost'
            description = u'Sn\xed\u017een\xed rychlosti'
        class Exit:
            name = u'Ukon\u010dit aplikaci'
            description = u'Ukon\u010d\xed aplikaci'
        class FiltersMenu:
            name = u'Nab\xeddka filtr\u016f'
            description = u'Nab\xeddka filtr\u016f'
        class FrameStep:
            name = u'O sn\xedmek vp\u0159ed'
            description = u'O sn\xedmek vp\u0159ed'
        class FrameStepBack:
            name = u'O sn\xedmek vzad'
            description = u'O sn\xedmek vzad'
        class Fullscreen:
            name = u'Na celou obrazovku'
            description = u'Na celou obrazovku'
        class FullscreenWOR:
            name = u'Na celou obrazovku beze zm\u011bny rozli\u0161en\xed'
            description = u'Na celou obrazovku beze zm\u011bny rozli\u0161en\xed'
        class GoTo:
            name = u'P\u0159ej\xedt na'
            description = u'P\u0159ej\xedt na'
        class IncreaseRate:
            name = u'Zv\xfd\u0161it rychlost'
            description = u'Zv\xfd\u0161en\xed rychlosti'
        class JumpBackwardKeyframe:
            name = u'Skok dozadu - kl\xed\u010dov\xe9 pol\xed\u010dko'
            description = u'Skok dozadu - kl\xed\u010dov\xe9 pol\xed\u010dko'
        class JumpBackwardLarge:
            name = u'Skok dozadu - velk\xfd'
            description = u'Skok dozadu - velk\xfd'
        class JumpBackwardMedium:
            name = u'Skok dozadu - st\u0159edn\xed'
            description = u'Skok dozadu - st\u0159edn\xed'
        class JumpBackwardSmall:
            name = u'Skok dozadu - mal\xfd'
            description = u'Skok dozadu - mal\xfd'
        class JumpForwardKeyframe:
            name = u'Skok dop\u0159edu - kl\xed\u010dov\xe9 pol\xed\u010dko'
            description = u'Skok dop\u0159edu - kl\xed\u010dov\xe9 pol\xed\u010dko'
        class JumpForwardLarge:
            name = u'Skok dop\u0159edu - velk\xfd'
            description = u'Skok dop\u0159edu - velk\xfd'
        class JumpForwardMedium:
            name = u'Skok dop\u0159edu - st\u0159edn\xed'
            description = u'Skok dop\u0159edu - st\u0159edn\xed'
        class JumpForwardSmall:
            name = u'Skok dop\u0159edu - mal\xfd'
            description = u'Skok dop\u0159edu - mal\xfd'
        class LoadSubTitle:
            name = u'Na\u010d\xedst titulky'
            description = u'Na\u010dten\xed titulk\u016f'
        class Next:
            name = u'Dal\u0161\xed'
            description = u'Dal\u0161\xed'
        class NextAudio:
            name = u'Dal\u0161\xed zvukov\xe1 stopa'
            description = u'Dal\u0161\xed zvukov\xe1 stopa'
        class NextAudioOGM:
            name = u'Dal\u0161\xed zvukov\xe1 stopa OGM'
            description = u'Dal\u0161\xed zvukov\xe1 stopa OGM'
        class NextPlaylistItem:
            name = u'Dal\u0161\xed polo\u017eka playlistu'
            description = u'Dal\u0161\xed polo\u017eka playlistu'
        class NextSubtitle:
            name = u'Dal\u0161\xed titulky'
            description = u'Dal\u0161\xed titulky'
        class NextSubtitleOGM:
            name = u'Dal\u0161\xed tituky OGM'
            description = u'Dal\u0161\xed tituky OGM'
        class OnOffSubtitle:
            name = u'Zapnout/Vypnout titulky'
            description = u'Zapnout/Vypnout titulky'
        class OpenDVD:
            name = u'Otev\u0159\xedt DVD'
            description = u'Otev\u0159e DVD'
        class OpenDevice:
            name = u'Otev\u0159\xedt za\u0159\xedzen\xed'
            description = u'Otev\u0159e za\u0159\xedzen\xed'
        class OpenFile:
            name = u'Otev\u0159\xedt soubor'
            description = u'Otev\u0159e soubor'
        class Options:
            name = u'Mo\u017enosti'
            description = u'Mo\u017enosti'
        class Pause:
            name = u'Pozastavit'
            description = u'Pozastav\xed p\u0159ehr\xe1v\xe1n\xed'
        class Play:
            name = u'P\u0159ehr\xe1t'
            description = u'Spust\xed p\u0159ehr\xe1v\xe1n\xed'
        class PlayPause:
            name = u'P\u0159ehr\xe1t/Pozastavit'
            description = u'Spust\xed/pozastav\xed p\u0159ehr\xe1v\xe1n\xed'
        class PlayerMenuLong:
            name = u'Nab\xeddka p\u0159ehr\xe1va\u010de - dlouh\xe1'
            description = u'Nab\xeddka p\u0159ehr\xe1va\u010de - dlouh\xe1'
        class PlayerMenuShort:
            name = u'Nab\xeddka p\u0159ehr\xe1va\u010de - kr\xe1tk\xe1'
            description = u'Nab\xeddka p\u0159ehr\xe1va\u010de - kr\xe1tk\xe1'
        class PnSCenter:
            name = u'Pan & Scan - vycentrovat'
            description = u'Pan & Scan - vycentruje'
        class PnSDecHeight:
            name = u'Pan & Scan - zmen\u0161it v\xfd\u0161ku'
            description = u'Pan & Scan - zmen\u0161\xed v\xfd\u0161ku'
        class PnSDecSize:
            name = u'Pan & Scan - zmen\u0161it velikost'
            description = u'Pan & Scan - zmen\u0161\xed velikost'
        class PnSDecWidth:
            name = u'Pan & Scan - zmen\u0161it \u0161\xed\u0159ku'
            description = u'Pan & Scan - zmen\u0161\xed \u0161\xed\u0159ku'
        class PnSDown:
            name = u'Pan & Scan - posunout dol\u016f'
            description = u'Pan & Scan - posune dol\u016f'
        class PnSDownLeft:
            name = u'Pan & Scan - posunout dol\u016f/doleva'
            description = u'Pan & Scan - posune dol\u016f/doleva'
        class PnSDownRight:
            name = u'Pan & Scan - posunout dol\u016f/doprava'
            description = u'Pan & Scan - posune dol\u016f/doprava'
        class PnSIncHeight:
            name = u'Pan & Scan - zv\u011bt\u0161it v\xfd\u0161ku'
            description = u'Pan & Scan - zv\u011bt\u0161\xed v\xfd\u0161ku'
        class PnSIncSize:
            name = u'Pan & Scan - zv\u011bt\u0161it velikost'
            description = u'Pan & Scan - zv\u011bt\u0161\xed velikost'
        class PnSIncWidth:
            name = u'Pan & Scan - zv\u011bt\u0161it \u0161\xed\u0159ku'
            description = u'Pan & Scan - zv\u011bt\u0161\xed \u0161\xed\u0159ku'
        class PnSLeft:
            name = u'Pan & Scan - posunout doleva'
            description = u'Pan & Scan - posune doleva'
        class PnSReset:
            name = u'Pan & Scan - v\xfdchoz\xed nastaven\xed'
            description = u'Pan & Scan - v\xfdchoz\xed nastaven\xed'
        class PnSRight:
            name = u'Pan & Scan - posunout doprava'
            description = u'Pan & Scan - posune doprava'
        class PnSRotateAddX:
            name = u'Pan & Scan - rotovat X+'
            description = u'Pan & Scan - rotuje X+'
        class PnSRotateAddY:
            name = u'Pan & Scan - rotovat Y+'
            description = u'Pan & Scan - rotuje Y+'
        class PnSRotateAddZ:
            name = u'Pan & Scan - rotovat Z+'
            description = u'Pan & Scan - rotuje Z+'
        class PnSRotateSubX:
            name = u'Pan & Scan - rotovat X-'
            description = u'Pan & Scan - rotuje X-'
        class PnSRotateSubZ:
            name = u'Pan & Scan - rotovat Z-'
            description = u'Pan & Scan - rotuje Z-'
        class PnSUp:
            name = u'Pan & Scan - posunout nahoru'
            description = u'Pan & Scan - posune nahoru'
        class PnSUpLeft:
            name = u'Pan & Scan - posunout nahoru/doleva'
            description = u'Pan & Scan - posune nahoru/doleva'
        class PnSUpRight:
            name = u'Pan & Scan - posunout nahoru/doprava'
            description = u'Pan & Scan - posune nahoru/doprava'
        class PnsRotateSubY:
            name = u'Pan & Scan - rotovat Y-'
            description = u'Pan & Scan - rotuje Y-'
        class PrevAudio:
            name = u'P\u0159edchoz\xed zvukov\xe1 stopa'
            description = u'P\u0159edchoz\xed zvukov\xe1 stopa'
        class PrevAudioOGM:
            name = u'P\u0159edchoz\xed zvukov\xe1 stopa OGM'
            description = u'P\u0159edchoz\xed zvukov\xe1 stopa OGM'
        class PrevSubtitle:
            name = u'P\u0159edchoz\xed titulky'
            description = u'P\u0159edchoz\xed titulky'
        class PrevSubtitleOGM:
            name = u'P\u0159edchoz\xed titulky OGM'
            description = u'P\u0159edchoz\xed titulky OGM'
        class Previous:
            name = u'P\u0159edchoz\xed'
            description = u'P\u0159edchoz\xed'
        class PreviousPlaylistItem:
            name = u'P\u0159edchoz\xed polo\u017eka playlistu'
            description = u'P\u0159edchoz\xed polo\u017eka playlistu'
        class Properties:
            name = u'Vlastnosti'
            description = u'Vlastnosti'
        class QuickOpen:
            name = u'Rychle otev\u0159\xedt soubor'
            description = u'Dialog pro rychl\xe9 otev\u0159en\xed souboru'
        class ReloadSubtitles:
            name = u'Znovu na\u010d\xedst titulky'
            description = u'Nov\xe9 na\u010dten\xed titulk\u016f'
        class ResetRate:
            name = u'V\xfdchoz\xed rychlost'
            description = u'V\xfdchoz\xed rychlost'
        class SaveAs:
            name = u'Ulo\u017eit jako'
            description = u'Ulo\u017eit jako'
        class SaveImage:
            name = u'Ulo\u017eit obr\xe1zek'
            description = u'Ulo\u017e\xed obr\xe1zek'
        class SaveImageAuto:
            name = u'Ulo\u017eit miniatury'
            description = u'Aktivuje ukl\xe1d\xe1n\xed miniatur'
        class SaveSubtitle:
            name = u'Ulo\u017eit titulky'
            description = u'Ulo\u017e\xed titulky'
        class Stop:
            name = u'Zastavit'
            description = u'Zastav\xed p\u0159ehr\xe1v\xe1n\xed'
        class ToggleCaptionMenu:
            name = u'Skr\xfdt/Zobrazit z\xe1hlav\xed okna a hlavn\xed nab\xeddku'
            description = u'Skryje/zobraz\xed z\xe1hlav\xed okna a hlavn\xed nab\xeddku'
        class ToggleCaptureBar:
            name = u'Skr\xfdt/Zobrazit panel z\xe1znamu (Record)'
            description = u'Skryje/zobraz\xed panel z\xe1znamu (Record)'
        class ToggleControls:
            name = u'Skr\xfdt/Zobrazit li\u0161tu ovl\xe1d\xe1n\xed'
            description = u'Skryje/zobraz\xed li\u0161tu ovl\xe1d\xe1n\xed'
        class ToggleInformation:
            name = u'Skr\xfdt/Zobrazit panel  informac\xed'
            description = u'Skryje/zobraz\xed panel  informac\xed'
        class TogglePlaylistBar:
            name = u'Skr\xfdt/Zobrazit okno playlistu'
            description = u'Skryje/zobraz\xed okno playlistu'
        class ToggleSeeker:
            name = u'Skr\xfdt/Zobrazit panel hled\xe1n\xed (posuvn\xedk)'
            description = u'Skryje/zobraz\xed panel hled\xe1n\xed (posuvn\xedk)'
        class ToggleShaderEditorBar:
            name = u'Skr\xfdt/Zobrazit panel editoru st\xednov\xe1n\xed'
            description = u'Skryje/zobraz\xed panel editoru st\xednov\xe1n\xed'
        class ToggleStatistics:
            name = u'Skr\xfdt/Zobrazit panel statistik'
            description = u'Skryje/zobraz\xed panel statistik'
        class ToggleStatus:
            name = u'Skr\xfdt/Zobrazit stavov\xfd \u0159\xe1dek'
            description = u'Skryje/zobraz\xed stavov\xfd \u0159\xe1dek'
        class ToggleSubresyncBar:
            name = u'Skr\xfdt/Zobrazit li\u0161tu subresync'
            description = u'Skryje/zobraz\xed li\u0161tu subresync'
        class VidFrmDouble:
            name = u'V\xfd\u0159ez videa - dvojn\xe1sobn\xe1 velikost'
            description = u'V\xfd\u0159ez videa - dvojn\xe1sobn\xe1 velikost'
        class VidFrmHalf:
            name = u'V\xfd\u0159ez videa - polovi\u010dn\xed velikost'
            description = u'V\xfd\u0159ez videa - polovi\u010dn\xed velikost'
        class VidFrmInside:
            name = u'V\xfd\u0159ez videa - dotknout se okna zevnit\u0159'
            description = u'V\xfd\u0159ez videa - dotknout se okna zevnit\u0159'
        class VidFrmNormal:
            name = u'V\xfd\u0159ez videa - standardn\xed velikost'
            description = u'V\xfd\u0159ez videa - standardn\xed velikost'
        class VidFrmOutside:
            name = u'V\xfd\u0159ez videa - dotknout se okna zven\u010d\xed'
            description = u'V\xfd\u0159ez videa - dotknout se okna zven\u010d\xed'
        class VidFrmStretch:
            name = u'V\xfd\u0159ez videa - rozt\xe1hnout do okna'
            description = u'V\xfd\u0159ez videa - rozt\xe1hnout do okna'
        class ViewCompact:
            name = u'P\u0159edvolby - vzhled kompaktn\xed'
            description = u'P\u0159edvolby - vzhled kompaktn\xed'
        class ViewMinimal:
            name = u'P\u0159edvolby - vzhled minim\xe1ln\xed'
            description = u'P\u0159edvolby - vzhled minim\xe1ln\xed'
        class ViewNormal:
            name = u'P\u0159edvolby - vzhled norm\xe1ln\xed'
            description = u'P\u0159edvolby - vzhled norm\xe1ln\xed'
        class VolumeDown:
            name = u'Hlasitost - sn\xed\u017eit'
            description = u'Hlasitost - sn\xed\u017eit'
        class VolumeMute:
            name = u'Hlasitost - ztlumit'
            description = u'Hlasitost - ztlumit'
        class VolumeUp:
            name = u'Hlasitost - zv\xfd\u0161it'
            description = u'Hlasitost - zv\xfd\u0161it'
        class Zoom100:
            name = u'Velikost - 100%'
            description = u'Velikost - 100%'
        class Zoom200:
            name = u'Velikost - 200%'
            description = u'Velikost - 200%'
        class Zoom50:
            name = u'Velikost - 50%'
            description = u'Velikost - 50%'
    class NetworkReceiver:
        name = u'S\xed\u0165ov\xfd p\u0159ij\xedma\u010d ud\xe1lost\xed'
        description = u'P\u0159ij\xedm\xe1 ud\xe1losti od pluginu "S\xed\u0165ov\xfd vys\xedla\u010d ud\xe1lost\xed"'
        event_prefix = u'Prefix ud\xe1losti:'
        password = u'Heslo:'
        port = u'Port:'
    class NetworkSender:
        name = u'S\xed\u0165ov\xfd vys\xedla\u010d ud\xe1lost\xed'
        description = u'Prost\u0159ednictv\xedm TCP/IP vys\xedl\xe1 ud\xe1losti k pluginu "S\xed\u0165ov\xfd p\u0159ij\xedma\u010d ud\xe1lost\xed".'
        host = u'Hostitel:'
        password = u'Heslo:'
        port = u'Port:'
        class Map:
            name = u'Odeslat'
            description = u'Odes\xedlan\xe1 ud\xe1lost'
            parameterDescription = u'Identifik\xe1tor odes\xedlan\xe9 ud\xe1losti:'
    class Serial:
        name = u'S\xe9riov\xfd port'
        description = u'Libovoln\xe1 komunikace p\u0159es s\xe9riov\xfd port.\n<br>Voliteln\u011b m\u016f\u017ee generovat ud\xe1losti.\n\n<p><b>Termin\xe1tor</b> je \u0159et\u011bzec znak\u016f, podle kter\xe9ho p\u0159i generov\xe1n\xed ud\xe1losti plugin identifikuje konec p\u0159ijat\xfdch dat.'
        baudrate = u'Bit\u016f za sekundu:'
        bytesize = u'Datov\xfdch bit\u016f:'
        codecChoices = [
            u'Syst\xe9mov\xe1 k\xf3dov\xe1 str\xe1nka',
            u'HEX',
            u'Latin-1',
            u'UTF-8',
            u'UTF-16',
            u'Python escape \u0159et\u011bzec',
        ]
        encoding = u'K\xf3dov\xe1n\xed:'
        eventPrefix = u'Prefix ud\xe1losti:'
        flowcontrol = u'\u0158\xedzen\xed toku:'
        generateEvents = u'Generovat ud\xe1losti z p\u0159\xedchoz\xedch dat'
        handshakes = [
            u'\u017d\xe1dn\xe9',
            u'Xon / Xoff',
            u'Hardwarov\xe9',
        ]
        parities = [
            u'\u017d\xe1dn\xe1',
            u'Lich\xe1',
            u'Sud\xe1',
        ]
        parity = u'Parita:'
        port = u'Port:'
        stopbits = u'Po\u010det stop-bit\u016f:'
        terminator = u'Termin\xe1tor:'
        class Read:
            name = u'P\u0159\xedjem dat'
            description = u'P\u0159\xedjem dat'
            read_all = u'P\u0159ijme tolik byt\u016f, kolik jich je pr\xe1v\u011b k dispozici'
            read_some = u'P\u0159ijme p\u0159esn\u011b tento po\u010det byt\u016f:'
            read_time = u'a po\u010dk\xe1 na n\u011b tento maxim\xe1ln\xed po\u010det milisekund:'
        class Write:
            name = u'Vys\xedl\xe1n\xed dat'
            description = u'Vys\xedl\xe1n\xed dat'
    class Speech:
        name = u'Hlas'
        description = u'Pou\u017eije slu\u017ebu p\u0159evod textu na \u0159e\u010d Microsoft Speech API (SAPI)'
        class TextToSpeech:
            name = u'P\u0159evod textu na \u0159e\u010d'
            description = u'Pou\u017e\xedv\xe1 Microsoft Speech API (SAPI) k p\u0159evodu textu na \u0159e\u010d.'
            buttonInsertDate = u'Vlo\u017eit aktu\xe1ln\xed datum'
            buttonInsertTime = u'Vlo\u017eit aktu\xe1ln\xed \u010das'
            buttonPlayback = u'P\u0159ehr\xe1t'
            errorCreate = u'Nemohu vytvo\u0159it hlasov\xfd objekt'
            errorNoVoice = u'Hlas se jm\xe9nem %s nen\xed dostupn\xfd'
            fast = u'Rychle'
            label = u'Vyslovit: %s'
            labelRate = u'Rychlost:'
            labelVoice = u'Hlas:'
            labelVolume = u'Hlasitost:'
            loud = u'Nahlas'
            normal = u'Norm\xe1ln\u011b'
            silent = u'Ti\u0161e'
            slow = u'Pomalu'
            textBoxLabel = u'Text'
            voiceProperties = u'Vlastnosti hlasu'
    class SysTrayMenu:
        name = u'Nab\xeddka v oznamovac\xed oblasti'
        description = u'Umo\u017e\u0148uje p\u0159idat u\u017eivatelskou nab\xeddku do syst\xe9mov\xe9 nab\xeddky EventGhost (SysTrayMenu).'
        addBox = u'P\u0159idat:'
        addItemButton = u'Polo\u017eka nab\xeddky'
        addSeparatorButton = u'Odd\u011blova\u010d'
        deleteButton = u'Odstranit'
        editEvent = u'Editovat:'
        editLabel = u'N\xe1pis:'
        eventHeader = u'Ud\xe1lost'
        labelHeader = u'N\xe1pis'
        unnamedEvent = u'Ud\xe1lost_%s'
        unnamedLabel = u'Nov\xe1 polo\u017eka %s'
        class Disable:
            name = u'Zak\xe1zat polo\u017eku'
            description = u'Zak\xe1\u017ee polo\u017eku nab\xeddky.'
        class Enable:
            name = u'Povolit polo\u017eku'
            description = u'Povol\xed polo\u017eku nab\xeddky.'
    class Task:
        name = u'Spr\xe1vce \xfaloh'
        description = u'Generuje ud\xe1losti, souvisej\xedc\xed se spr\xe1vou \xfaloh syst\xe9mu Windows.'
    class Timer:
        name = u'\u010casova\u010d'
        description = u'Generuje ud\xe1losti po nastaviteln\xe9 dob\u011b a opakuje je v dan\xe9m intervalu.\nOpakov\xe1n\xed m\u016f\u017ee b\xfdt nekone\u010dn\xe9 anebo je mo\u017en\xe9 zadat po\u010det opakov\xe1n\xed.'
        colLabels = (
            u'N\xe1zev \u010dasova\u010de',
            u'\u010cas spu\u0161t\u011bn\xed',
            u'P\u0159\xed\u0161t\xed ud\xe1lost',
            u'ID ud\xe1losti',
            u'Opakov\xe1no/zb\xfdv\xe1',
            u'Opakovat',
            u'Interval',
        )
        listhl = u'Pr\xe1v\u011b te\u010f aktivn\xed \u010dasova\u010de:'
        stopped = u'Plugin zastaven'
        timerFinished = u'\u010casova\u010d ukon\u010den'
        class TimerAction:
            name = u'Spu\u0161t\u011bn\xed nov\xe9ho nebo zm\u011bna b\u011b\u017e\xedc\xedho \u010dasova\u010de'
            description = u'Umo\u017e\u0148uje spustit, zastavit nebo resetovat \u010dasova\u010de, kter\xe9 mohou generovat ud\xe1losti po nastaven\xe9 dob\u011b'
            actions = (
                u'Restartovat \u010dasova\u010d se sou\u010dasn\xfdm nastaven\xedm',
                u'Restartovat \u010dasova\u010d (pouze pokud b\u011b\u017e\xed)',
                u'Vynulovat po\u010d\xedtadlo',
                u'Zru\u0161it \u010dasova\u010d',
            )
            addCounterToName = u'p\u0159ipojit stav po\u010d\xedtadla k ID ud\xe1losti'
            eventName = u'ID ud\xe1losti:'
            interval1 = u'Interval:'
            interval2 = u'sekund'
            labelStart = u'Spustit \u010dasova\u010d "%s" (%s opakov\xe1n\xed, interval %.2f sekund)'
            labelStartOneTime = u'Spustit \u010dasova\u010d "%s"'
            labelStartUnlimited = u'Spustit \u010dasova\u010d "%s" (nekone\u010dn\xe9 opakov\xe1n\xed, interval %.2f sekund)'
            labels = (
                u'Restartovat \u010dasova\u010d "%s"',
                u'Restartovat \u010dasova\u010d "%s" pouze pokud b\u011b\u017e\xed',
                u'Resetovat po\u010d\xedtadlo \u010dasova\u010de "%s"',
                u'Zru\u0161it \u010dasova\u010d "%s"',
            )
            loop1 = u'Opakov\xe1n\xed:'
            loop2 = u'(0 = nekone\u010dn\xe9)'
            showRemaingLoopsText = u'po\u010d\xedtadlo ukazuje zb\xfdvaj\xedc\xed po\u010det opakov\xe1n\xed'
            start = u'Spustit nov\xfd \u010dasova\u010d (pr\xe1v\u011b b\u011b\u017e\xedc\xed \u010dasova\u010d se stejn\xfdm n\xe1zvem bude zru\u0161en)'
            startTime = u'Spustit:'
            startTimeTypes = (
                u'okam\u017eit\u011b',
                u'po uplynut\xed doby intervalu',
                u'p\u0159esn\u011b v tento \u010das (HH:MM:SS)',
                u'po uplynut\xed t\xe9to doby (HH:MM:SS)',
                u'v p\u0159\xed\u0161t\xed cel\xe9 minut\u011b',
                u'v p\u0159\xed\u0161t\xed cel\xe9 5-minut\u011b',
                u'v p\u0159\xed\u0161t\xed cel\xe9 \u010dtvthodin\u011b',
                u'v p\u0159\xed\u0161t\xed cel\xe9 p\u016flhodin\u011b',
                u'v p\u0159\xed\u0161t\xed cel\xe9 hodin\u011b',
            )
            timerName = u'N\xe1zev \u010dasova\u010de:'
    class UIR:
        description = u'Hardwarov\xfd plugin pro IR p\u0159ij\xedma\u010de <a href="http://fly.cc.fer.hr/~mozgic/UIR/">Universal Infrared Receiver V1 (UIR)</a> a <a href="http://www.evation.com/irman/index.html">Irman</a>.\n\n<p><center><img src="irman_front.jpg" alt="Irman" /></a></center>'
    class Webserver:
        name = u'Webov\xfd server'
        description = u'Implementuje mal\xfd webov\xfd server, kter\xfd m\u016f\u017ee b\xfdt pou\u017eit pro generov\xe1n\xed\nud\xe1lost\xed prost\u0159ednictv\xedm HTML-str\xe1nek.'
        documentRoot = u'Ko\u0159enov\xfd adres\xe1\u0159 HTML dokumentu:'
        eventPrefix = u'Prefix ud\xe1losti:'
        port = u'Port:'
