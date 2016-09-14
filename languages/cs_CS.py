# -*- coding: UTF-8 -*-
class General:
    apply = u"Použít"
    autostartItem = u"Automatický start"
    browse = u"Procházet..."
    cancel = u"Storno"
    choose = u"Volba"
    configTree = u"Konfigurační strom"
    deleteLinkedItems = u"Alespoň jedna položka mimo váš výběr odkazuje na položku uvnitř vašeho výběru. Jestliže přesto budete v odstranění výběru pokračovat, odkazující položka nebude moci dále správně pracovat.\n\nJste si jistý, že chcete výběr odstranit?"
    deleteManyQuestion = u"Tento element má %s subelement(y,ů).\nJsi si jistý, že chcete odstranit všechny ?"
    deletePlugin = u"Tento plugin je použit některou akcí ve vaší konfiguraci.\nNemůžete ho odstranit, dokud neodstraníte všechny akce, které ho používají."
    deleteQuestion = u"Jste si jistý, že chcete odstranit tuto položku?"
    help = u"&Pomoc"
    moreTag = u"více..."
    noOptionsAction = u"Tato akce nemá žádné možnosti nastavení."
    noOptionsPlugin = u"Tento plugin nemá žádné možnosti nastavení."
    ok = u"OK"
    pluginLabel = u"Plugin: %s"
    unnamedEvent = u"<nepojmenovaná událost>"
    unnamedFile = u"<nepojmenovaný soubor>"
    unnamedFolder = u"<nepojmenovaná složka>"
    unnamedMacro = u"<nepojmenované makro>"
class MainFrame:
    onlyLogAssigned = u"Zaznamenávat pouze přiřazené a aktivní události"
    class Logger:
        caption = u"Zapisovač událostí (Logger)"
        descriptionHeader = u"Záznam"
        timeHeader = u"Čas"
        welcomeText = u"-->Vítám vás v aplikaci EventGhost<--"
    class Menu:
        About = u"&O aplikaci EventGhost..."
        AddAction = u"Vložit akci..."
        AddEvent = u"Vložit událost"
        AddFolder = u"Vložit složku"
        AddMacro = u"Vložit makro"
        AddPlugin = u"Vložit Plugin..."
        Apply = u"Použít"
        CheckUpdate = u"Vyhledat novější verzi..."
        ClearLog = u"Vyčistit"
        Close = u"&Zavřít"
        CollapseAll = u"&Sbalit vše"
        ConfigurationMenu = u"&Konfigurace"
        Configure = u"Konfigurovat položku..."
        Copy = u"&Kopírovat"
        Cut = u"&Vyjmout"
        Delete = u"O&dstranit"
        Disabled = u"Zakázat položku"
        EditMenu = u"&Editovat"
        Execute = u"&Spustit položku"
        Exit = u"&Konec"
        ExpandAll = u"&Rozbalit vše"
        ExpandOnEvents = u"Rozbalit při &události"
        ExpandTillMacro = u"Rozbalit pouze do úrovně &makra"
        Export = u"Export..."
        FileMenu = u"&Soubor"
        Find = u"&Najít..."
        FindNext = u"Na&jít další"
        HelpMenu = u"&Pomoc"
        HideShowToolbar = u"Panel nástrojů"
        Import = u"Import..."
        LogActions = u"Logovat &akce"
        LogMacros = u"Logovat &makra"
        LogTime = u"&Logovat čas"
        New = u"&Nový"
        Open = u"&Otevřít..."
        Options = u"&Možnosti..."
        Paste = u"V&ložit"
        Redo = u"&Odvolat zpět (Redo)"
        Rename = u"Přejmenovat položku"
        Reset = u"Reset"
        Save = u"&Uložit"
        SaveAs = u"Uložit &jako..."
        SelectAll = u"&Vybrat vše"
        Undo = u"&Zpět (Undo)"
        ViewMenu = u"&Zobrazit"
        WebForum = u"Internetová diskuse"
        WebHomepage = u"Domovská stránka aplikace EventGhost"
        WebWiki = u"Wikipedie"
    class SaveChanges:
        mesg = u"Konfigurační soubor byl změněn.\n\nChcete změny uložit ?"
        title = u"Uložit změny ?"
    class TaskBarMenu:
        Exit = u"Ukončit EventGhost"
        Hide = u"Skrýt okno aplikace EventGhost"
        Show = u"Otevřít okno aplikace EventGhost"
    class Tree:
        caption = u"Konfigurace"
class Error:
    FileNotFound = u'Soubor "%s" nebyl nalezen.'
    InAction = u'Chyba v akci: "%s"'
    pluginLoadError = u"Chyba při zavádění pluginu %s."
    pluginNotActivated = u'Plugin "%s" nebyl aktivován'
    pluginStartError = u"Chyba při spuštění pluginu: %s"
class CheckUpdate:
    ManErrorMesg = u"Nebylo možné získat informace z webové stránky EventGhost.\n\nProsím, zkuste to znovu později."
    ManErrorTitle = u"Chyba při pokusu o update"
    ManOkMesg = u"Tato verze aplikace EventGhost je nejnovější."
    ManOkTitle = u"Žádná novější verze není k dispozici"
    downloadButton = u"Navštívit stránku stahování"
    newVersionMesg = u"Byla vydána novější verze aplikace EventGhost.\n\n	Vaše verze:	%s\n	Poslední verze:	%s\n\nChcete navštívit stránku stahování hned?"
    title = u"Nová verze aplikace EventGhost je k dispozici..."
    waitMesg = u"Prosím čekejte, dokud EventGhost nezíská potřebné informace."
class AddActionDialog:
    descriptionLabel = u"Popis"
    title = u"Výběr akce ke vložení..."
class AddPluginDialog:
    author = u"Autor:"
    descriptionBox = u"Popis"
    externalPlugins = u"Ovládání externího HW"
    noInfo = u"Žádná informace není k dispozici."
    noMultiload = u"Tento plugin nepodporuje více současných instancí a vy už máte jednu instanci tohoto pluginu ve své konfiguraci."
    noMultiloadTitle = u"Není možný souběh více instancí"
    otherPlugins = u"Ostatní"
    programPlugins = u"Ovládané programy"
    remotePlugins = u"Přijímače dálkových povelů"
    title = u"Výběr pluginu ke vložení..."
    version = u"Verze:"
class AddActionGroupDialog:
    caption = u"Vložit akce ?"
    message = u"EventGhost může vložit složku se všemi akcemi tohoto pluginu do konfiguračního stromu. Jestliže si to přejete, zvolte místo pro vkládanou složku a stiskněte tlačítko OK.\n\nJinak stiskněte tlačítko Storno."
class OptionsDialog:
    CheckUpdate = u"Kontrolovat existenci novější verze při spuštění"
    HideOnClose = u"Skrýt hlavní okno aplikace při stisknutí zavíracího tlačítka"
    HideOnStartup = u"Skrýt při spuštění"
    LanguageGroup = u"Jazyk"
    StartGroup = u"Při spuštění"
    StartWithWindows = u"Spustit při startu Windows"
    Tab1 = u"Všeobecné"
    Title = u"Možnosti"
    UseAutoloadFile = u"Automatické spuštění souboru"
    Warning = u"Změna jazyka se projeví až po novém spuštění aplikace."
    confirmDelete = u"Potvrdit odstranění položky stromu"
    limitMemory1 = u"Limit spotřeby paměti při minimalizaci"
    limitMemory2 = u"MB"
class FindDialog:
    caseSensitive = u"&Rozlišovat velikost"
    direction = u"Směr"
    down = u"&Dolů"
    findButton = u"Na&jít další"
    notFoundMesg = u'"%s" nenalezeno.'
    searchLabel = u"&Najít:"
    searchParameters = u"&Hledat i v parametrech akcí"
    title = u"Hledání"
    up = u"Nahor&u"
    wholeWordsOnly = u"&Pouze celá slova"
class AboutDialog:
    Author = u"Autor: %s"
    CreationDate = u"%a, %d %b %Y %H:%M:%S"
    Title = u"O aplikaci EventGhost"
    Version = u"Verze: %s (build %s)"
    tabAbout = u"O aplikaci"
    tabLicense = u"Licenční ujednání"
    tabSpecialThanks = u"Zvláštní poděkování"
    tabSystemInfo = u"Systémové informace"
class Plugin:
    class EventGhost:
        name = u"EventGhost"
        description = u"Zde jsou akce, které slouží převážně k řízení funkce jádra aplikace EventGhost."
        class AutoRepeat:
            name = u"Automaticky opakovat makro"
            description = u'Makro, ve kterém je tento element použit, bude automaticky opakovaně spouštěno.\n\n<p><b>POZOR:</b> Tato funkce je použitelná pouze pro makra, jejichž délka provádění je dána nějakým externím podnětem (například dlouhým držením tlačítka dálkového ovladače). Element "Automatické opakování makra" by měl být umístěn na konci makra.'
            seconds = u"sec."
            text1 = u"První opakování začít po"
            text2 = u"a opakovat každých"
            text3 = u"Modifikovat četnost opakování po"
            text4 = u"s opakováním každých"
        class Comment:
            name = u"Komentář"
            description = u"Akce bez účinku. Může být použita pro komentování vaší konfigurace."
        class DisableItem:
            name = u"Zakázat položku"
            description = u"Zakáže položku"
            label = u"Zakázat: %s"
            text1 = u"Prosím vyberte položku, která má být zakázána:"
        class EnableExclusive:
            name = u"Výhradně povolit složku/makro"
            description = u"Povolí určitou složku nebo makro ve vaší konfiguraci. Zároveň ale zakáže všechny ostatní složky nebo makra, které mají stejnou úroveň (složka nebo makro) a jsou na stejné větvi konfiguračního stromu."
            label = u"Výhradně povolit: %s"
            text1 = u"Prosím vyberte složku/makro, která/-é má být povolena/-o:"
        class EnableItem:
            name = u"Povolit položku"
            description = u"Povolí položku ve stromu."
            label = u"Povolit: %s"
            text1 = u"Prosím vyberte položku, která má být povolena:"
        class FlushEvents:
            name = u"Zahodit události"
            description = u'Akce "Zahodit události" má za následek vyprázdnění pracovní fronty. To je užitečné v případě, že nějaké makro se zpracovává určitou dobu a události, které se nahromadí během jeho zpracování, by neměly být zpracovány.\n\n<p><b>Příklad:</b> Máte zdlouhavé makro "start systému", jehož zpracování trvá okolo 90 sekund. Koncový uživatel nebude nic vidět, dokud se nerozsvítí projektor. To trvá asi 60 sekund. Je velmi pravděpodobné, že uživatel bude opakovaně mačkat tlačítko dálkového ovladače, které startuje makro (v domnění, že se nic neděje). Pokud na konec makra umístíte příkaz "Zahodit události", všechna nadbytečná stisknutí tlačítka budou z fronty vymazána.'
        class JumpIfLongPress:
            name = u"Skočit při dlouhém stisku"
            description = u"Skočí na jiné makro, pokud tlačítko na dálkovém ovladači je stisknuté déle, než je nastavený čas."
            label = u"Je-li tlačítko stisknuté %s sec, skočit na: %s"
            text1 = u"Je-li tlačítko stisknuté déle než"
            text2 = u"sekund,"
            text3 = u"skočit na:"
            text4 = u"Vyberte makro, na které se má skočit..."
            text5 = u"Prosím vyberte makro, které by mělo být spuštěno,\npokud je dosaženo nastavené délky stisknutí tlačítka."
        class NewJumpIf:
            name = u"Skočit"
            description = u"Skočí na jiné makro, pokud výsledek určité akce odpovídá podmínce."
            choices = [
                u"poslední akce byla úspěšná",
                u"poslední akce byla neúspěšná",
                u"vždy",
            ]
            labels = [
                u'Při úspěchu skočit na "%s"',
                u'Při neúspěchu skočit na "%s"',
                u'Skočit na "%s"',
                u'Při úspěchu skočit na "%s" a vrátit se',
                u'Při neúspěchu skočit na "%s" a vrátit se',
                u'Skočit na "%s" a vrátit se',
            ]
            mesg1 = u"Výběr makra..."
            mesg2 = u"Prosím vyberte makro, které by mělo být spuštěno,\npokud výsledek určité akce odpovídá podmínce."
            text1 = u"Jestliže:"
            text2 = u"Skočit na:"
            text3 = u"a vrátit se po vykonání"
        class PythonCommand:
            name = u"Příkaz jazyka Python"
            description = u"Provede zadaný jednoduchý příkaz jazyka Python."
            parameterDescription = u"Příkaz jazyka Python:"
        class PythonScript:
            name = u"Skript jazyka Python"
            description = u"Vykoná plnohodnotný skript jazyka Python."
        class ShowOSD:
            name = u"Zobrazit OSD"
            description = u"Zobrazí jednoduchý OSD."
            alignment = u"Umístění:"
            alignmentChoices = [
                u"Nahoře vlevo",
                u"Nahoře vpravo",
                u"Dole vlevo",
                u"Dole vpravo",
                u"Uprostřed",
                u"Dole uprostřed",
                u"Nahoře uprostřed",
                u"Vlevo uprostřed",
                u"Vpravo uprostřed",
            ]
            display = u"Zobrazit na:"
            editText = u"Text k zobrazení:"
            label = u"Zobrazit OSD: %s"
            osdColour = u"Barva OSD:"
            osdFont = u"OSD písmo:"
            outlineFont = u"Obrys OSD"
            wait1 = u"Automaticky skrýt OSD po"
            wait2 = u"sekundách (0 = nikdy)"
            xOffset = u"Vodorovný ofset X:"
            yOffset = u"Svislý ofset Y:"
        class StopProcessing:
            name = u"Zastavit zpracování této události"
            description = u"Zastaví zpracování této události"
        class TriggerEvent:
            name = u"Vyvolat událost"
            description = u"Vyvolá požadovanou událost (volitelně po určitém čase)."
            labelWithTime = u'Vyvolat událost "%s" po %.2f sekundách'
            labelWithoutTime = u'Vyvolat událost "%s"'
            text1 = u"Identifikace generované události:"
            text2 = u"Prodleva před uvolněním události:"
            text3 = u"sekund. (0 = uvolnit okamžitě)"
        class Wait:
            name = u"Čekat danou dobu"
            description = u"Čeká danou dobu"
            label = u"Čekat: %s sec"
            seconds = u"sekund"
            wait = u"Čekat"
    class System:
        name = u"Systém"
        description = u"Systém"
        forced = u"Nucené: %s"
        forcedCB = u"Nuceně zavře všechny programy"
        class ChangeDisplaySettings:
            name = u"Změnit nastavení displeje"
            description = u"Změní nastavení displeje"
        class ChangeMasterVolumeBy:
            name = u"Změnit hlavní hlasitost"
            description = u"Změní hlavní hlasitost"
            text1 = u"Změnit hlavní hlasitost o"
            text2 = u"procent."
        class Execute:
            name = u"Spustit aplikaci"
            description = u"Spustí program."
            FilePath = u"Cesta ke spustitelnému souboru:"
            Parameters = u"Parametry příkazové řádky:"
            ProcessOptions = (
                u"Reálný čas",
                u"Nadprůměrná",
                u"Normální",
                u"Podprůměrná",
                u"Nízká",
            )
            ProcessOptionsDesc = u"Priorita procesu:"
            WaitCheckbox = u"Čekat na dokončení"
            WindowOptions = (
                u"Normální",
                u"Minimalizované",
                u"Maximalizované",
                u"Neviditelné",
            )
            WindowOptionsDesc = u"Velikost okna:"
            WorkingDir = u"Pracovní složka:"
            browseExecutableDialogTitle = u"Volba spustitelného souboru"
            browseWorkingDirDialogTitle = u"Volba pracovní složky"
            label = u"Spustit program: %s"
        class Hibernate:
            name = u"Uspat počítač"
            description = u"Tato funkce zastaví systém, vypne napájení a zavede režim spánku."
        class LockWorkstation:
            name = u"Zamknout pracovní stanici"
            description = u"Tato funkce požádá o zamknutí displeje pracovní stanice. Zamknutí chrání stanici před neautorizovaným použitím. Funkce má stejný výsledek jako stisknutí kombinace Ctrl+Alt+Del a klepnutí na Zamknout pracovní stanici (XP Professional)."
        class LogOff:
            name = u"Odhlásit aktuálního uživatele"
            description = u"Zastaví všechny procesy, běžící v účtu aktuálně přihlášeného uživatele. Pak uživatele odhlásí."
        class MonitorGroup:
            name = u"Displej"
            description = u"Tyto akce řídí napájení displeje počítače."
        class MonitorPowerOff:
            name = u"Přepnout monitor do stavu power-off"
            description = u"Přepne displej do stavu power-off. To podporuje většina režimů, šetřících energii."
        class MonitorPowerOn:
            name = u"Znovu povolit monitor"
            description = u"Zapne displej, pokud byl v režimu power-off nebo nízké spotřeby. Také zastaví šetřič obrazovky."
        class MonitorStandby:
            name = u"Přepnout monitor do režimu stand-by"
            description = u"Nastaví režim nízké spotřeby displeje."
        class MuteOff:
            name = u"Zrušit režim Ztlumit vše"
            description = u"Zruší režim Ztlumit vše"
        class MuteOn:
            name = u"Nastavit režim Ztlumit vše"
            description = u"Nastaví režim Ztlumit vše"
        class OpenDriveTray:
            name = u"Vysunout/zasunout dvířka mechaniky"
            description = u"Řídí dvířka CD/DVD-ROM mechaniky."
            driveLabel = u"Mechanika:"
            labels = [
                u"Přesunout dvířka mechaniky: %s",
                u"Vysunout dvířka mechaniky: %s",
                u"Zasunout dvířka mechaniky: %s",
            ]
            options = [
                u"Vysunout nebo zasunout dvířka mechaniky (podle aktuálního stavu)",
                u"Pouze vysunout dvířka mechaniky",
                u"Pouze zasunout dvířka mechaniky",
            ]
            optionsLabel = u"Volba akce"
        class PlaySound:
            name = u"Přehrát zvuk"
            description = u"Přehraje zvuk"
            fileMask = u"Soubory wav (*.WAV)|*.wav|Všechny soubory (*.*)|*.*"
            text1 = u"Cesta ke zvukovému souboru:"
            text2 = u"Čekat na dokončení"
        class PowerDown:
            name = u"Vypnout počítač"
            description = u"Zastaví systém a vypne napájení. Systém musí podporovat funkci power-off."
        class PowerGroup:
            name = u"Řízení napájení"
            description = u"Tyto akce zastavují, uspávají, restartují nebo vypínají počítač. Mohou také zamknout pracovní stanici a odhlásit aktuálního uživatele."
        class Reboot:
            name = u"Restartovat počítač"
            description = u"Zastaví systém a restartuje počítač."
        class RegistryChange:
            name = u"Změnit hodnotu v registru"
            description = u"Změní hodnoty v registru windows"
            actions = (
                u"vytvořit nebo změnit",
                u"změnit pouze existuje-li",
                u"odstranit",
            )
            labels = (
                u'Změnit "%s" na %s',
                u'Změnit "%s" na %s pouze existuje-li',
                u'Odstranit "%s"',
            )
        class RegistryGroup:
            name = u"Registry"
            description = u"Vyhledává nebo mění hodnoty v registru windows."
            actionText = u"Akce:"
            chooseText = u"Volba registrového klíče:"
            defaultText = u"(Výchozí)"
            keyOpenError = u"Chyba otevření registrového klíče"
            keyText = u"Klíč:"
            keyText2 = u"Klíč"
            newValue = u"Nová hodnota:"
            noKeyError = u"Klíč neexistuje"
            noNewValueError = u"Nová hodnota neexistuje"
            noSubkeyError = u"Podklíč neexistuje"
            noTypeError = u"Typ neexistuje"
            noValueNameError = u"Název hodnoty neexistuje"
            noValueText = u"hodnota nenalezena"
            oldType = u"Aktuální typ:"
            oldValue = u"Aktuální hodnota:"
            typeText = u"Typ:"
            valueChangeError = u"Chyba při změně hodnoty"
            valueName = u"Název hodnoty:"
            valueText = u"Hodnota:"
        class RegistryQuery:
            name = u"Dotaz registru"
            description = u"Vyhledá údaj v registru windows a vrátí nebo porovná hodnoty"
            actions = (
                u"kontrola existuje-li",
                u"vrátí výsledek",
                u"porovná s",
            )
            labels = (
                u'Zkontroluj, existuje-li "%s"',
                u'Vrať "%s" jako výsledek',
                u'Porovnej "%s" s %s',
            )
        class ResetIdleTimer:
            name = u"Resetovat dobu nečinnosti"
            description = u"Resetuje dobu nečinnosti"
        class SetClipboard:
            name = u"Zkopírovat řetězec do schránky"
            description = u"Zkopíruje řetězec znaků do systémové schránky."
            error = u"Nemohu otevřít schránku"
        class SetDisplayPreset:
            name = u"Nastavit předvolby displeje"
            description = u"Nastaví předvolby displeje"
            fields = (
                u"Zařízení",
                u"Vlevo",
                u"Nahoře",
                u"Šířka",
                u"Výška",
                u"Kmitočet",
                u"Kvalita barev",
                u"Připojeno",
                u"Primární",
                u"Vlajky",
            )
            query = u"Zjitit aktuální nastavení displeje"
        class SetIdleTime:
            name = u"Nastavit dobu pro nečinnost"
            description = u"Nastaví dobu pro generování události nečinnost"
            label1 = u"Čekat"
            label2 = u"sekund před generováním události nečinnost."
        class SetMasterVolume:
            name = u"Nastavit hlavní hlasitost"
            description = u"Nastaví hlavní hlasitost"
            text1 = u"Nastavit hlavní hlasitost na"
            text2 = u"procent."
        class SetSystemIdleTimer:
            name = u"Nastavit systémový časovač doby nečinnosti"
            description = u"Nastaví systémový časovač doby nečinnosti"
            choices = [
                u"Zákaz systémového časovače doby nečinnosti",
                u"Povolení systémového časovače doby nečinnosti",
            ]
            text = u"Zvolte možnost:"
        class SetWallpaper:
            name = u"Změnit tapetu"
            description = u"Změní tapetu"
            choices = (
                u"Na střed",
                u"Vedle sebe",
                u"Roztáhnout",
            )
            fileMask = u"Všechny soubory obrázků|*.jpg;*.bmp;*.gif|Všechny soubory (*.*)|*.*"
            text1 = u"Cesta k souboru s obrázkem:"
            text2 = u"Pozice:"
        class ShowPicture:
            name = u"Zobrazit obrázek"
            description = u"Zobrazí obrázek"
            allFiles = u"Všechny soubory"
            allImageFiles = u"Všechny soubory typu obrázek"
            display = u"Monitor"
            path = u"Cesta k obrázku (pro vymazání použijte prázdnou cestu):"
        class SoundGroup:
            name = u"Zvuková karta"
            description = u"Tyto akce ovládají zvukovou kartu vašeho počítače."
        class Standby:
            name = u"Uvést počítač do režimu standby"
            description = u"Tato funkce uspí systém vypnutím napájení a uvedením do stavu spánku."
        class StartScreenSaver:
            name = u"Spustit šetřič obrazovky"
            description = u"Spustí šetřič obrazovky, vybraný v nastavení windows."
        class ToggleMute:
            name = u"Nastavit/zrušit režim Ztlumit vše"
            description = u"Nastaví/zruší režim Ztlumit vše"
        class WakeOnLan:
            name = u"Probudit počítač po síti"
            description = u"Probudí počítač vysláním speciálního síťového paketu. \n\nJe třeba uvést MAC adresu počítače ve tvaru:<p><i>00-13-D4-9A-2F-04</i> nebo<br><i>00:13:D4:9A:2F:04</i> "
            parameterDescription = u"MAC adresa počítače, který má být probuzen:"
    class Window:
        name = u"Okno"
        description = u"Akce spojené s řízením okna na obrazovce, jako nalezení určitého okna, přesun, změna velikosti a odeslání stisků kláves k určitému oknu."
        class BringToFront:
            name = u"Přenést do popředí"
            description = u"Přenese určené okno do popředí."
        class Close:
            name = u"Zavřít"
            description = u"Zavře okno aplikace"
        class FindWindow:
            name = u"Najít okno"
            description = u"Najde uvedené okno."
            drag1 = u"Přetáhněte mě\ndo okna."
            drag2 = u"Teď mě přesuňte\ndo okna."
            hide_box = u"Skrýt EventGhost během přesouvání"
            invisible_box = u"Hledat také neviditelné položky"
            label = u"Najít okno: %s"
            label2 = u"Najít okno, které je nejvíce v popředí"
            matchNum1 = u"Vrátit pouze"
            matchNum2 = u". nalezené okno"
            options = (
                u"Aplikace:",
                u"Jméno okna:",
                u"Třída okna:",
                u"Jméno potomka:",
                u"Třída potomka:",
            )
            refresh_btn = u"&Aktualizovat"
            stopMacro = [
                u"Zastavit makro, jestliže cíl není nalezen",
                u"Zastavit makro, jestliže cíl je nalezen",
                u"Nikdy nezastavovat makro",
            ]
            testButton = u"Test"
            wait1 = u"Čekat až"
            wait2 = u"sekund na objevení se okna."
        class Maximize:
            name = u"Maximalizovat"
            description = u"Maximalizuje okno"
        class Minimize:
            name = u"Minimalizovat"
            description = u"Minimalizuje okno"
        class MoveTo:
            name = u"Přesunout absolutně"
            description = u"Přesune okno na dané místo"
            label = u"Přesunout okno na %s"
            text1 = u"Nastavit horizontální pozici X na"
            text2 = u"pixelů"
            text3 = u"Nastavit vertikální pozici Y na"
            text4 = u"pixelů"
        class Resize:
            name = u"Změnit velikost"
            description = u"Změní velikost okna."
            label = u"Změnit velikost okna na %s, %s"
            text1 = u"Nastavit šířku na"
            text2 = u"pixelů"
            text3 = u"Nastavit výšku na"
            text4 = u"pixelů"
        class Restore:
            name = u"Obnovit"
            description = u"Obnoví okno"
        class SendKeys:
            name = u"Emulovat stisk kláves"
            description = u'Tato akce emuluje stisk kláves pro ovládání ostatních programů.\nZnaky, které jsou k ovládání potřeba, napište do editačního pole.\n\n<p>\nPro emulování speciálních kláves je třeba použít klíčová slova a uzavřít je\ndo složených závorek. Například chcete-li použít klávesu "šipka nahoru",\nnapište <b>{Up}</b>. Pro zkombinování více kláves můžete kombinovat\nvíce klíčových slov (znaků) pomocí znaménka plus jako: <b>{Shift+Ctrl+F1}</b>\nnebo <b>{Ctrl+V}</b>. Při zápisu klíčových slov nezáleží na velikosti použitých\nznaků, takže můžete napsat také {SHIFT+ctrl+F1}, pokud se vám to líbí.\n<p>\nPokud je u některých kláves třeba rozlišovat mezi klávesou na levé a pravé straně\nklávesnice (jako třeba u klávesy s logem Windows), mohou být klíčová slova\noznačena předponou "L" nebo "R":\n<br><b>{Win}</b> nebo <b>{LWin}</b> nebo <b>{RWin}</b>\n<p>\nA tady je seznam zbytku klíčových slov, kerým EventGhost rozumí:<br>\n<b>{Ctrl}</b> nebo <b>{Control}<br>\n{Shift}<br>\n{Alt}<br>\n{Return}</b> nebo <b>{Enter}<br>\n{Back}</b> nebo <b>{Backspace}<br>\n{Tab}</b> nebo <b>{Tabulator}<br>\n{Esc}</b> nebo <b>{Escape}<br>\n{Spc}</b> nebo <b>{Space}<br>\n{Up}<br>\n{Down}<br>\n{Left}<br>\n{Right}<br>\n{PgUp}</b> nebo <b>{PageUp}<br>\n{PgDown}</b> nebo <b>{PageDown}<br>\n{Home}<br>\n{End}<br>\n{Ins}</b> nebo <b>{Insert}<br>\n{Del}</b> nebo <b>{Delete}<br>\n{Pause}<br>{Capslock}<br>\n{Numlock}<br>\n{Scrolllock}<br>\n{F1}, {F2}, ... , {F24}<br>\n{Apps}</b> (To je klávesa kontextové nabídky)<b><br>\n<br>\n</b>Toto bude emulovat klávesy numerické klávesnice:<b><br>\n{Divide}<br>\n{Multiply}<br>\n{Subtract}<br>\n{Add}<br>\n{Decimal}<br>\n{Numpad0}, {Numpad1}, ... , {Numpad9}</b>'
            insertButton = u"&Vložit"
            specialKeyTool = u"Nástroj pro zvláštní klávesy"
            textToType = u"Text k emulování:"
            useAlternativeMethod = u"Použít alternativní metodu emulování stisknutých kláves"
            class Keys:
                backspace = u"Klávesa mazání (Backspace)"
                context = u"Klávesa kontextové nabídky"
                delete = u"Delete"
                down = u"Šipka dolů"
                end = u"End"
                enter = u"Enter (na num. klávesnici)"
                escape = u"Escape"
                home = u"Home"
                insert = u"Insert"
                left = u"Šipka vlevo"
                num0 = u"0 na numerické klávesnici"
                num1 = u"1 na numerické klávesnici"
                num2 = u"2 na numerické klávesnici"
                num3 = u"3 na numerické klávesnici"
                num4 = u"4 na numerické klávesnici"
                num5 = u"5 na numerické klávesnici"
                num6 = u"6 na numerické klávesnici"
                num7 = u"7 na numerické klávesnici"
                num8 = u"8 na numerické klávesnici"
                num9 = u"9 na numerické klávesnici"
                numAdd = u"+ na numerické klávesnici"
                numDecimal = u"Tečka na numerické klávesnici"
                numDivide = u"/ na numerické klávesnici"
                numMultiply = u"* na numerické klávesnici"
                numSubtract = u"- na numerické klávesnici"
                pageDown = u"Page Down"
                pageUp = u"Page Up"
                returnKey = u"Enter"
                right = u"Šipka vpravo"
                space = u"Mezerník"
                tabulator = u"Tabelátor"
                up = u"Šipka nahoru"
                win = u"Klávesa s logem Windows"
        class SendMessage:
            name = u"Poslat zprávu"
            description = u'Použije Windows-API funkci "SendMessage" pro odeslání speciální zprávy oknu. Může také použít "PostMessage", je-li to požadováno.'
            text1 = u"Použít PostMessage místo SendMessage"
        class SetAlwaysOnTop:
            name = u'Nastavit vlastnost "Vždy na vrchu"'
            description = u'Nastaví vlastnost "Vždy na vrchu"'
            actions = (
                u'Zrušit vlastnost "Vždy na vrchu"',
                u'Nastavit vlastnost "Vždy na vrchu"',
                u'Nastavit/zrušit vlastnost "Vždy na vrchu"',
            )
            radioBox = u"Zvolte akci:"
    class Mouse:
        name = u"Myš"
        description = u"Akce k řízení ukazatele myši a emulování událostí, generovaných myší."
        class GoDirection:
            name = u"Spustit pohyb myši"
            description = u"Spustí pohyb myši daným směrem"
            label = u"Spustit pohyb myši směrem %.2f°"
            text1 = u"Spustit pohyb ukazatele myši pod úhlem"
            text2 = u"stupňů. (0-360)"
        class LeftButton:
            name = u"Levé tlačítko myši"
            description = u"Levé tlačítko myši"
        class LeftDoubleClick:
            name = u"Poklepat levým tlačítkem myši"
            description = u"Emuluje poklepání levým tlačítkem myši"
        class MiddleButton:
            name = u"Prostřední tlačítko myši"
            description = u"Prostřední tlačítko myši"
        class MouseWheel:
            name = u"Emulovat pohyb kolečka myši"
            description = u"Emuluje pohyb kolečka myši"
            label = u"Kolečkem myši otočit o %d zoubků"
            text1 = u"Otočit kolečkem myši o"
            text2 = u"zoubků. (Záporná hodnota znamená směr dolů)"
        class MoveAbsolute:
            name = u"Absolutně přesunout"
            description = u"Přesune ukazatel myši na absolutně udané souřadnice"
            label = u"Přesunout myš na x:%s, y:%s"
            text1 = u"Nastavit horizontální pozici X na"
            text2 = u"pixelů"
            text3 = u"Nastavit vertikální pozici Y na"
            text4 = u"pixelů"
        class RightButton:
            name = u"Pravé tlačítko myši"
            description = u"Pravé tlačítko myši"
        class RightDoubleClick:
            name = u"Poklepat pravým tlačítkem myši"
            description = u"Emuluje poklepání pravým tlačítkem myši"
        class ToggleLeftButton:
            name = u"Změnit stav levého tlačítka myši"
            description = u"Změní stav levého tlačítka myši"
    class Billy:
        name = u"Billy"
        description = u'Přidává akce k řízení audio přehrávače <a href="http://www.sheepfriends.com/?page=billy">Billy</a>. \n\n<p><BR><B>POZOR !<BR>Správně pracuje pouze s beta verzí 1.04b přehrávače Billy !</B><BR>Se starší verzí bude plugin pracovat v omezeném režimu !</p>'
        text1 = u"Nemohu najít okno přehrávače Billy !"
        class AddFile:
            name = u"Přidat soubor(y)"
            description = u"Otevře dialog pro přidání souboru(ů)."
        class AddFolder:
            name = u"Přidat složku"
            description = u"Otevře dialog pro přidání složky s audio soubory."
        class AddPlistToFav:
            name = u"Přidat seznam k Oblíbeným"
            description = u"Přidá seznam k Oblíbeným."
        class AddURL:
            name = u"Přidat internetové radio"
            description = u"Přidá internetové radio."
        class CheckNewFiles:
            name = u"Zkontrolovat nové soubory"
            description = u"Zkontroluje, zda ve složce nejsou nové soubory."
        class ClearHistory:
            name = u"Vyčistit historii přehraných nebo označených souborů"
            description = u"Odstraní označení přehraných a do fronty zařazených souborů."
        class ClearList:
            name = u"Vyčistit seznam"
            description = u"Vyčistí seznam."
        class CopyEntry:
            name = u"Kopírovat položku seznamu"
            description = u"Kopíruje položku seznamu do schránky."
        class CropQueued:
            name = u"Odstranit neoznačené"
            description = u'"Odstřihne" označené položky seznamu (neoznačené odstraní).'
        class CutEntry:
            name = u"Vyjmout položku seznamu"
            description = u"Vyjme položku seznamu (zkopíruje do schránky)."
        class Delete:
            name = u"Hodit soubor do koše"
            description = u"Odstraní soubor (do koše)."
        class EditEntry:
            name = u"Editovat položku seznamu"
            description = u"Otevře dialog pro editaci položky seznamu."
        class ExitBilly:
            name = u"Ukončit Billy"
            description = u"Ukončí běh přehrávače Billy."
        class Explore:
            name = u"Otevřít složku"
            description = u"Otevře složku s právě přehrávaným souborem."
        class Find:
            name = u"Najít"
            description = u"Otevře dialog pro hledání v aktuálním seznamu."
        class LoadFav1:
            name = u"Zavést Oblíbené 1"
            description = u"Zavede se seznam Oblíbené 1."
        class LoadFav2:
            name = u"Zavést Oblíbené 2"
            description = u"Zavede se seznam Oblíbené 2."
        class LoadFav3:
            name = u"Zavést Oblíbené 3"
            description = u"Zavede se seznam Oblíbené 3."
        class LoadFav4:
            name = u"Zavést Oblíbené 4"
            description = u"Zavede se seznam Oblíbené 4."
        class LoadFav5:
            name = u"Zavést Oblíbené 5"
            description = u"Zavede se seznam Oblíbené 5."
        class LoadFav6:
            name = u"Zavést Oblíbené 6"
            description = u"Zavede se seznam Oblíbené 6."
        class LoadFav7:
            name = u"Zavést Oblíbené 7"
            description = u"Zavede se seznam Oblíbené 7."
        class LoadFav8:
            name = u"Zavést Oblíbené 8"
            description = u"Zavede se seznam Oblíbené 8."
        class LoadFav9:
            name = u"Zavést Oblíbené 9"
            description = u"Zavede se seznam Oblíbené 9."
        class Minimize:
            name = u"Minimalizovat do oznamovací oblasti"
            description = u"Přehrávač se minimalizuje do oznamovací oblasti."
        class Next:
            name = u"Další"
            description = u"Přeskočí na další soubor (skladbu)."
        class OpenFolder:
            name = u"Otevřít složku"
            description = u"Otevře složku s audiosoubory."
        class OpenPlaylist:
            name = u"Otevřít seznam"
            description = u"Otevře (zavede) seznam."
        class OrganizeFav:
            name = u"Organizovat Oblíbené"
            description = u"Otevře dialog pro organizaci Oblíbených."
        class PasteEntry:
            name = u"Vložit položku seznamu"
            description = u"Vloží položku seznamu ze schránky."
        class PausePlay:
            name = u"Pozastavit/Přehrát"
            description = u"Pozastaví/spustí přehrávání."
        class Play:
            name = u"Přehrát"
            description = u"Spustí přehrávání."
        class Previous:
            name = u"Předchozí"
            description = u"Přeskoí na předchozí soubor (skladbu)."
        class Properties:
            name = u"Vlastnosti"
            description = u"Otevře dialog pro editaci nebo hromadné přejmenování (při vícenásobném výběru)."
        class Queue:
            name = u"Zařadit do fronty"
            description = u"Vybraný soubor zařadí do fronty."
        class Record:
            name = u"Ukládat internetové radio"
            description = u"Ukládat internetové radio do souboru."
        class Remove:
            name = u"Odstranit soubor ze seznamu"
            description = u"Odstraní soubor ze seznamu."
        class ResetMixer:
            name = u"Resetovat mixer Windows"
            description = u"Resetuje mixer Windows."
        class Run:
            name = u"Spustit nebo obnovit"
            description = u"Spouští přehrávač Billy s jeho defaultním nastavením nebo ho obnoví."
        class SavePlaylist:
            name = u"Uložit seznam"
            description = u"Otevře dialog pro uložení seznamu."
        class Settings:
            name = u"Nastavení"
            description = u"Otevře nabídku nastavení přehrávače Billy."
        class Stop:
            name = u"Zastavit"
            description = u"Zastaví přehrávání."
        class ToStart:
            name = u"Skočit na začátek souboru"
            description = u"Skočí na začátek přehrávaného souboru."
        class TogglePlayMode:
            name = u"Změnit režim přehrávání"
            description = u"Změní režim přehrávání."
        class ToggleViewMode:
            name = u"Změnit způsob zobrazení"
            description = u"Změní způsob zobrazení seznamu."
    class DesktopRemote:
        name = u"Ovladač na pracovní ploše"
        description = u"Na pracovní ploše vykreslí okno v podobě dálkového ovladače"
        class AddButton:
            name = u"Přidat tlačítko"
            description = u"Přidá tlačítko"
            event = u"Událost:"
            label = u"Nápis:"
        class CreateNew:
            name = u"Vytvořit nový ovladač"
            description = u"Vytvoří nový ovladač"
        class Show:
            name = u"Zobrazit"
            description = u"Zobrazí vytvořený ovladač"
        class StartNewLine:
            name = u"Začít nový řádek"
            description = u"Začne na novém řádku"
    class DirectoryWatcher:
        name = u"Hlídač složky"
        description = u"Generuje události, jestliže soubory v určené složce jsou vytvořeny, smazány\nnebo změněny."
        watchPath = u"Hlídaná složka:"
        watchSubDirs = u"Hlídat i podsložky"
    class E_mail:
        name = u"E-mail"
        description = u"Přidává akce, související s elektronickou poštou."
        accType = u"Typ účtu"
        accountsList = u"Seznam účtů:"
        addressLabel = u"E-mailová adresa:"
        assignError = u'Účet "%s" neexistuje!'
        buttons = (
            u"Přerušit",
            u"Přerušit vše",
            u"Obnovit",
            u"Zavřít",
        )
        cancel = u"Storno"
        client = u"E-mailový klient"
        close = u"Zavřít"
        colLabels = (
            u"Jméno sledování",
            u"Interval",
            u"Poslední kontrola",
            u"Celková událost",
            u"Událost zprávy",
        )
        delete = u"Odstranit"
        deleteServer = u'Server "%s" je použit ve vaší konfiguraci.\nNemůžete ho odstranit.'
        detTitle = u'Sledování "%s" : %s nových e-mailů'
        eBoxCase = (
            u"POP3",
            u"IMAP",
        )
        emailSent = u'E-mail "%s: %s" byl odeslán !'
        error0 = u"Chyba protokolu POP3:"
        error1 = u'Není možné připojit se k POP serveru "%s:%i"'
        error2 = u"Chyba protokolu IMAP:"
        error3 = u'Není možné připojit se k IMAP serveru "%s:%i"'
        error4 = u'Není možné přihlásit se k účtu "%s" na serveru "%s:%i"'
        error5 = u'Server nenalezen "%s", zkouším použít defaultní server "%s".'
        error6 = u"Chyba protokolu SMTP:"
        error7 = u'Není možné připojit se k SMTP serveru "%s:%i"'
        error8 = u"Vaše zpráva nemůže být odeslána !"
        groupLabel = u"Jméno skupiny:"
        groupsList = u"Seznam skupin:"
        groupsTitle = u"Skupiny adresátů pro odchozí e-maily"
        incPort = u"Port"
        incServer = u"Příchozí server:"
        insert = u"Přidat nový"
        label = u"Jméno účtu:"
        labelsDetails = (
            u"Č.",
            u"Účet",
            u"Předmět",
            u"Od",
        )
        listhead = u"Právě aktivní sledování:"
        mailAddress = u"E-mailová adresa:"
        notifLabel = u"čekající(ch)\nzpráv(a,y)"
        observStarts = u'Sledování "%s" spuštěno'
        ok = u"OK"
        outAddress = u"Seznam e-mailových adres:"
        outServer = u"Odchozí (SMTP) server:"
        outServerTitle = u"Nastavení odchozích (SMTP) serverů"
        outText = u"Text:"
        param = u"Parametry účtu"
        popup = (
            u"Zobrazit",
            u"Odstranit",
            u"Obnovit",
            u"E-mailový klient",
            u"Zavřít",
        )
        refresh = u"Obnovit"
        replAddress = u"Adresa pro odpověď (nepovinné):"
        secureConnectChoice1 = (
            u"Ne",
            u">>> TLS zatím nepodporován <<<",
            u">>> TLS zatím nepodporován <<<",
            u"SSL",
        )
        secureConnectChoice2 = (
            u"Ne",
            u"TLS, je-li k dispozici",
            u"TLS",
            u"SSL",
        )
        secureConnectLabel = u"Použít zabezpečené spojení:"
        servLabel = u"Jméno serveru:"
        servParam = u"Parametry serveru"
        serversList = u"Seznam serverů:"
        show = u"Zobrazit"
        textsList = u"Seznam textů:"
        textsTitle = u"Texty pro odchozí e-maily"
        tip0 = u"Kliknutí pravým tlačítkem - skrytí okna\nDvojklik - zobrazení okna s tabulkou čekajících zpráv\nCTRL+dvojklik - otevření defaultního e-mailového klienta"
        txtLabel = u"Jméno textu:"
        useName = u"Použít jména a hesla:"
        useSecure = u"Použít zabezpečenou autentizaci"
        userLogin = u"Přihlašovací jméno uživatele:"
        userName = u"Jméno uživatele (nepovinné):"
        userPassword = u"Heslo:"
        viewerTitle = u"Prohlížeč aktivních sledování"
        warning = u"Při jakékoliv změně konfigurace budou všechna aktivní sledování přerušena !"
        class AbortAllObservations:
            name = u"Přerušení všech sledování"
            description = u"Přeruší všechna sledování."
        class AbortObservation:
            name = u"Přerušení sledování"
            description = u"Přeruší sledování."
            abortNow = u"Přerušit teď !"
            nameObs = u"Jméno sledování:"
            tip = u"Sledování bude přerušeno teď"
        class SendEmail:
            name = u"Odeslání e-mailu"
            description = u"Odešle e-mail."
            copyLabel = u"Kopie:"
            fromLabel = u"Od:"
            outText = u"Text:"
            outTexts = u"Připojit:"
            sendNow = u"Odeslat teď !"
            subjectLabel = u"Předmět:"
            tip = u"Zde může být také výraz jako {eg.event.payload} !"
            tip1 = u"Jméno příjemce (není povinné)"
            tip2 = u"Adresa příjemce (povinné)"
            tip3 = u"E-mail bude odeslán teď !"
            toLabel = u"Komu:"
        class StartObservation:
            name = u"Spuštění sledování"
            description = u"Spustí sledování."
            accounts = u"Účty ke sledování:"
            backCol = u"Barva pozadí:"
            delete = u"Odstranit"
            emailEvent = u"Událost zprávy"
            evtName = u"Jméno události:"
            field_1 = (
                u"Nic",
                u"Předmět",
                u"Od",
                u"Tělo",
            )
            field_2 = (
                u"obsahuje",
                u"neobsahuje",
                u"je",
                u"není",
                u"začíná",
                u"končí",
            )
            forCol = u"Barva textu:"
            interval_1 = u"Interval:"
            interval_2 = u"min."
            message = u"Zobrazit oznamovací okno"
            nameObs = u"Jméno sledování:"
            payload = u"Náklad:"
            radio_buttons = (
                u"Celkové sledování bez filtrace",
                u"Zpráva splňuje všechny následující podmínky",
                u"Zpráva splňuje některou z následujících podmínek",
            )
            startNow = u"Spustit teď !"
            tip0 = u"Zobrazí se oznamovací okno s počtem čekajích zpráv"
            tip1 = u"Po spuštění události bude zpráva ze serveru odstraněna"
            tip2 = u"Spustit sledování teď"
            tip3 = u"Spustí událost pro každý e-mail"
            tip4 = u"Spustí událost při každé změně počtu čekajících zpráv"
            totalEvent = u"Celková událost"
            totalPayload = (
                u"Nic",
                u"Počet",
            )
            warning = u"Nebyl nalezen ani jeden účet, odpovídající seznamu %s !"
    class FileOperations:
        name = u"Souborové operace"
        description = u"Práce s textovými soubory (čtení a zápis)."
        class Read:
            name = u"Čtení textu ze souboru"
            description = u"Přečte text z vybraného souboru."
            FilePath = u"Číst soubor:"
            TreeLabel = u"Číst soubor: %s"
            begin = u"od začátku"
            browseFileDialogTitle = u"Výběr souboru"
            defaultIn = u"unicode (UTF-8)"
            end = u"od konce"
            ignore = u"Ignorovat (přeskočí vadné znaky)"
            inputPage = u"Kódování vstupních dat:"
            lineNum = u"Číst od řádku číslo:"
            listIncluding = u"Řádkové řetězce včetně CR/LF"
            listNotIncluding = u"Řádkové řetězce bez CR/LF"
            oneIncluding = u"Řetězec včetně CR/LF"
            oneNotIncluding = u"Řetězec bez CR/LF"
            oneString = u"Jeden řetězec (včetně CR/LF)"
            readAhead = u"Číst"
            readBehind = u"řádků (0 = celý soubor)"
            replace = u"Nahradit špatné znaky"
            strict = u"Vyvolat výjimku"
            systemPage = u"systémová kódová stránka (%s)"
            txtDecErrMode = u"Ošetření chyb při dekódování:"
            txtMode = u"Přečtený(é) řádek(ky) vrátit jako:"
        class Write:
            name = u"Zapsat text do souboru"
            description = u"Zapíše text do vybraného souboru."
            FilePath = u"Výstupní soubor:"
            TreeLabel = u"Zapsat %s do souboru: %s"
            append = u"Připojit k souboru"
            browseFileDialogTitle = u"Výběr souboru"
            defaultOut = u"unicode (UTF-8)"
            hexdump = u"Řetězec zapsat v HexDump formátu"
            ignore = u"Ignorovat (přeskočí špatné znaky)"
            inString = u"Vstupní text:"
            internal = u"interní unicode"
            logTimes = u"Zapsat časové razítko"
            newLine = u"Připojit k souboru na nový řádek"
            outputPage = u"Kódování výstupních dat:"
            overwrite = u"Soubor přepsat"
            replace = u"Nahradit špatné znaky"
            strict = u"Vyvolat výjimku"
            systemPage = u"systémová kódová stránka (%s)"
            txtEncErrMode = u"Ošetření chyb při kódování:"
            txtModeMulti = u"Režim zápisu"
            writeToLog = u"Zapsat také  do logu EventGhostu"
    class Foobar2000:
        name = u"Foobar2000"
        description = u'Přidává podporu funkcí pro řízení aplikace Foobar2000.\n\n<p><a href="http://www.foobar2000.org/">Domovská stránka aplikace Foobar2000</a>'
        class Exit:
            name = u"Ukončit"
            description = u"Ukončí foobar."
        class Hide:
            name = u"Skrýt"
            description = u"Skryje okno aplikace foobar."
        class NextTrack:
            name = u"Další stopa"
            description = u"Emuluje stisk tlačítka Další stopa (Next track)."
        class Pause:
            name = u"Pozastavit"
            description = u"Emuluje stisk tlačítka Pozastavit (Pausa)."
        class Play:
            name = u"Přehrát"
            description = u"Emuluje stisk tlačítka Přehrát (Play)."
        class PlayPause:
            name = u"Změnit stav Přehrát/Pozastavit"
            description = u"Emuluje stisk tlačítka Přehrát/Pozastavit (Play/Pausa)."
        class PreviousTrack:
            name = u"Předchozí stopa"
            description = u"Emuluje stisk tlačítka Předchozí stopa (Previous track)."
        class Random:
            name = u"Náhodně"
            description = u"Emuluje stisk tlačítka Náhodně (Random)."
        class Run:
            name = u"Spustit"
            description = u"Spustí foobar s aktuálními předvolbami."
        class Show:
            name = u"Obnovit"
            description = u"Otevře okno aplikace foobar."
        class Stop:
            name = u"Zastavit"
            description = u"Emuluje stisk tlačítka Zastavit (Stop)."
    class IgorPlugUSB:
        name = u"IgorPlug-USB"
        description = u'Plugin pro IR přijímač od Igora Češka.\n\n<p><a href="http://www.cesko.host.sk/">Domovská stránka Igora Češka</a></center>'
    class IrfanView:
        name = u"IrfanView"
        description = u'Přidává akce k ovládání <a href="http://www.irfanview.com/">IrfanView</a>.'
        err = u"Nemohu najít soubor i_view32.exe !"
        filemask = u"i_view32.exe|i_view32.exe|Všechny soubory (*.*)|*.*"
        grpDescription1 = u"Přidává nabídku Soubor k ovládání IrfanView."
        grpDescription2 = u"Přidává nabídku Úpravy k ovládání IrfanView."
        grpDescription3 = u"Přidává nabídku Obrázek k ovládání IrfanView."
        grpDescription4 = u"Přidává nabídku Nastavení k ovládání IrfanView."
        grpDescription5 = u"Přidává nabídku Zobrazit k ovládání IrfanView."
        grpDescription6 = u"Přidává ostatní akce k ovládání IrfanView."
        grpName1 = u"Soubor"
        grpName2 = u"Úpravy"
        grpName3 = u"Obrázek"
        grpName4 = u"Nastavení"
        grpName5 = u"Zobrazit"
        grpName6 = u"Ostatní"
        label = u"Cesta k souboru i_view32.exe:"
        text1 = u"Nemohu najít okno IrfanView !"
        class AboutIrfanView:
            name = u'Zobrazit dialog "O programu IrfanView"'
            description = u'Zobrazí dialog "O programu IrfanView".'
        class AcquireBatchScanning:
            name = u"Skenovat/Dávkové skenování"
            description = u"Zobrazí dialog Skenovat/Dávkové skenování."
        class AdobeFiltersDialog:
            name = u"Filtry Adobe 8BF"
            description = u"Filtry Adobe 8BF."
        class AppendToSlideshow:
            name = u"Připojit k aktuální prezentaci"
            description = u"Připojí aktuální soubor k aktuální prezentaci."
        class AutoColorCorrection:
            name = u"Automatické přizpůsobení barev"
            description = u"Automatické přizpůsobení barev."
        class BatchConversionRename:
            name = u"Dávková konverze/přejmenování"
            description = u"Zobrazí dialog Dávková konverze/přejmenování."
        class CaptureDialog:
            name = u'Zobrazit dialog "Sejmutí obrazovky"'
            description = u'Zobrazí dialog "Nastavení zachycení obrazovky".'
        class CloseActualWindow:
            name = u"Zavřít aktuální okno"
            description = u"Zavře aktuální okno (hlavní okno, prezentaci, celoobrazovkový režim, miniatury nebo dialog)."
        class ControlSwitchThumb:
            name = u"Přepnout řízení v okně miniatur"
            description = u"Přepne řízení v okně miniatur."
        class CopyFile:
            name = u"Kopírovat soubor"
            description = u"Kopíruje soubor."
        class CopyFilename:
            name = u"Kopírovat název souboru do schránky"
            description = u"Kopíruje název souboru do schránky."
        class CopyToClipboard:
            name = u"Kopírovat obrázek do schránky"
            description = u"Kopíruje obrázek do schránky."
        class CreateSelection:
            name = u"Vytvořit vlastní výběr"
            description = u"Vytvoří vlastní výběr."
        class CropSelectionRectangle:
            name = u"Oříznout"
            description = u"Ořízne vybraný obdélník."
        class CutSelectionRectangle:
            name = u"Vyjmout výběr"
            description = u"Vyjme vybraný obdélník."
        class DeleteFile:
            name = u"Odstranit soubor"
            description = u"Odstraní aktuální soubor."
        class DirectPrint:
            name = u"Tisknout přímo"
            description = u"Tiskne obrázek přímo - bez otevření dialogu."
        class EditDelete:
            name = u"Odstranit (Vyčistit obrazovku)"
            description = u"Odstraní obrázek (vyčistí obrazovku)."
        class EditMultipageTif:
            name = u"Upravit vícestránkový TIF"
            description = u"Úprava vícestránkového TIFu."
        class EditUndo:
            name = u"Zpět (Undo)"
            description = u"Zpět (Undo)."
        class EffectsSetup:
            name = u"Prohlížeč efektů"
            description = u"Prohlížeč efektů."
        class EnhanceColors:
            name = u"Upravit barvy"
            description = u"Úprava barev."
        class Exit:
            name = u"Konec"
            description = u"Konec."
        class FilterFactoryDialog:
            name = u"Dialog Výroba filtru"
            description = u"Zobrazí dialog Výroba filtru."
        class FullScreen:
            name = u"Celá obrazovka"
            description = u"Celá obrazovka."
        class FullScreenMode1:
            name = u"Režim celá obrazovka - 1:1"
            description = u"Režim celá obrazovka: Zobrazit obrázky/filmy v původní velikosti."
        class FullScreenMode2:
            name = u"Režim celá obrazovka - přizpůsobit pouze velké"
            description = u"Režim celá obrazovka: Přizpůsobit obrazovce pouze velké obrázky (doporučeno)."
        class FullScreenMode3:
            name = u"Režim celá obrazovka - přizpůsobit všechny"
            description = u"Režim celá obrazovka: Přizpůsobit obrazovce všechny obrázky/filmy."
        class FullScreenMode4:
            name = u"Režim celá obrazovka - roztáhnout všechny"
            description = u"Režim celá obrazovka: Roztáhnout všechny obrázky/filmy."
        class Help:
            name = u"Pomoc"
            description = u"Pomoc."
        class HorizontalFlip:
            name = u"Horizontální překlopení"
            description = u"Horizontální překlopení."
        class InsertText:
            name = u"Vložit text do výběru"
            description = u"Vloží text do výběru."
        class JpgLosslessOperations:
            name = u"JPG bezeztrátové operace"
            description = u"JPG bezeztrátové operace (PlugIn)."
        class JumpIntoToolbar:
            name = u"Skočit do editačního pole nástrojové lišty"
            description = u"Skočí do editačního pole nástrojové lišty."
        class LoadFirstFile:
            name = u"První soubor v adresáři"
            description = u"První soubor v adresáři."
        class LoadLastFile:
            name = u"Poslední soubor v adresáři"
            description = u"Poslední soubor v adresáři."
        class LoadNextFile:
            name = u"Další soubor v adresáři"
            description = u"Další soubor v adresáři."
        class LoadPrevFile:
            name = u"Předchozí soubor v adresáři"
            description = u"Předchozí soubor v adresáři."
        class MinimizeWindow:
            name = u"Minimalizovat okno"
            description = u'Minimalizuje okno ("Boss" tlačítko).'
        class MoveFile:
            name = u"Přesunout soubor"
            description = u"Přesune soubor."
        class OpenBrowseDialog:
            name = u'Zobrazit dialog "Procházet-Subadresáře"'
            description = u'Zobrazí dialog "Procházet-Subadresáře".'
        class OpenDialog:
            name = u'Zobrazit dialog "Otevřít"'
            description = u'Zobrazí dialog "Otevřít".'
        class OpenInExternal:
            name = u"Otevřít v externím prohlížeči"
            description = u"Otevře v externím prohlížeči."
        class OpenRandomImage:
            name = u"Otevřít náhodný obrázek"
            description = u"Otevře náhodný obrázek."
        class OriginalSize:
            name = u"Původní velikost"
            description = u"Původní velikost (žádné zvětšení)."
        class PasteFromClipboard:
            name = u"Vložit ze schránky"
            description = u"Vloží ze schránky."
        class PreviousWallpaper:
            name = u"Nastavit jako pozadí plochy - původní."
            description = u"Nastaví původní pozadí plochy."
        class PrintDialog:
            name = u"Zobrazit dialog Tisk"
            description = u"Zobrazí dialog Tisk."
        class PropertiesDialog:
            name = u"Zobrazit dialog Vlastnosti"
            description = u"Zobrazí dialog Vlastnosti."
        class RedEyeReduction:
            name = u"Zrdukovat červené oči (výběr)"
            description = u"Provede redukci červených očí v aktuálním výběru."
        class Refresh:
            name = u"Obnovit"
            description = u"Aktualizuje obsah okna."
        class RenameFile:
            name = u"Přejmenovat soubor"
            description = u"Přejmenuje soubor."
        class ReopenFile:
            name = u"Znovu otevřít"
            description = u"Znovu otevře soubor."
        class ResampleDialog:
            name = u"Zobrazit dialog Změnit velikost/rozlišení"
            description = u"Zobrazí dialog Změnit velikost/rozlišení."
        class RotateAngle:
            name = u"Uživatelská/jemná rotace"
            description = u"Uživatelská/jemná rotace (podle zadaného úhlu)."
        class RotateLeft:
            name = u"Otočit vlevo"
            description = u"Otočí obrázek o 90° vlevo."
        class RotateRight:
            name = u"Otočit vpravo"
            description = u"Otočí obrázek o 90° vpravo."
        class RotationLeft:
            name = u"JPG bezeztrátová rotace vlevo"
            description = u"JPG bezeztrátová rotace vlevo."
        class RotationRight:
            name = u"JPG bezeztrátová rotace vpravo"
            description = u"JPG bezeztrátová rotace vpravo."
        class RunCommandLine:
            name = u"Spustit s příkazovou řádkou"
            description = u"Spustí IrfanView s příkazovou řádkou."
            cmdline = u"Vložte příkazový řádek (např. /killmesoftly ):"
            err = u"Nemohu najít soubor i_view32.exe !"
            help = u"Pomoc"
            label = u"Jmenovka této akce:"
        class RunDefault:
            name = u"Spustit s přednastavenými parametry"
            description = u"Spustí IrfanView s přednastavenými parametry."
            text2 = u"Nemohu najít soubor i_view32.exe !"
        class RunSlideshow:
            name = u"Spustit prezentaci"
            description = u"Spustí IrfanView a otevře prezentaci."
            alpha = u"Použít Alfa prolínání mezi obrázky"
            autoDelay = u"Automaticky po nastaveném zpoždění"
            autoKeyb = u"Automaticky od vstupu myši/klávesnice"
            browseTitle = u"Vybraná složka:"
            close = u"Zavřít IrfanView po posledním souboru"
            delay = u"Zpoždění [s]:"
            dirpath = u"Cesta ke složce:"
            displtext = u"Zobrazit text (název souboru ...):"
            err = u"Nemohu najít soubor i_view32.exe !"
            filemask = u"Textové soubory (*.txt)|*.txt|Seznamy (*.lst)|*.lst|Všechny soubory (*.*)|*.*"
            filepath = u"Cesta k souboru s prezentací:"
            fitAll = u"Přizpůsobit všechny obrázky"
            folder = u"Složka"
            help = u"Pomoc"
            hideCursor = u"Skrýt kurzor myši"
            high = u"Výška:"
            label = u"Jmenovka této prezentace:"
            lineOpt = u"Příkazový řádek:"
            loop = u"Smyčka"
            mask = u'Maska pro "zobrazit text":'
            mode1_1 = u"Původní velikost"
            modeFull = u"Celá obrazovka"
            modeWin = u"Okno uprostřed obrazovky"
            monitor = u"Monitor:"
            noRepeat = u"Neopakovat obrázky"
            onlyBig = u"Přizpůsobit pouze velké obrázky"
            radioboxfit = u"Režim přizpůsobení"
            radioboxmode = u"Režim prezentace"
            radioboxprogress = u"Postup snímků"
            radioboxsource = u"Zdroj prezentace"
            randomDelay = u"Náhodně po nastaveném zpoždění"
            randomKeyb = u"Náhodně od vstupu myši/klávesnice"
            resample = u'Použít funkci "Resample" (pomalejší)'
            runslideshow = u"Spustit prezentaci"
            scratchAll = u"Roztáhnout všechny obrázky"
            soundLoop = u"Smyčka pro MP3 (hudba na pozadí)"
            suppress = u"Potlačit chyby v průběhu přehrávání"
            toolTipFile = u"Napište název souboru nebo kliknutím na tlačítko otevřete dialog"
            toolTipFolder = u"Napište název složky nebo kliknutím na tlačítko otevřete dialog"
            txtFile = u"Soubor s prezentací"
            width = u"Šířka:"
            windowSize = u"Velikost okna [pixely]"
        class RunWithOptions:
            name = u"Spustit s možnostmi"
            description = u"Spustí IrfanView s vlastními předvolbami."
            alpha = u"Použít Alfa prolínání mezi obrázky"
            caption = u"Záhlaví okna"
            centerImage = u"Vystředit obrázek v okně"
            displtext = u"Zobrazit text (název souboru ...)"
            err = u"Nemohu najít soubor i_view32.exe !"
            filemask = u"JPG soubory (*.jpg)|*.jpg|BMP soubory (*.bmp)|*.bmp|PNG soubory (*.png)|*.png|Všechny soubory (*.*)|*.*"
            filepath = u"Cesta k souboru:"
            fitAll = u"Přizpůsobit všechny obrázky"
            fsOptions = u"Možnosti režimu Celá obrazovka"
            help = u"Pomoc"
            hideCursor = u"Skrýt kurzor myši"
            high = u"Výška:"
            label = u"Jmenovka této akce:"
            lineOpt = u"Ostatní volby vložte do příkazového řádku:"
            mask = u'Maska pro "Zobrazit text":'
            menuBar = u"Nabídková lišta"
            mode1_1 = u"Původní velikost"
            modeFull = u"Celá obrazovka"
            modeWin = u"Okno"
            monitor = u"Monitor:"
            onlyBig = u"Přizpůsobit pouze velké obrázky"
            posAndSize = u"Startovní pozice a velikost okna"
            radioboxmode = u"Spustit v režimu"
            radioboxwinmode = u"Režim přizpůsobení - Okno"
            radiofullmode = u"Režim přizpůsobení - Celá obrazovka"
            resample = u'Použít funkci "Resample" (pomalejší)'
            resample2 = u'Použít funkci "Resample"'
            runwithoption = u"Spustit s možnostmi"
            scratchAll = u"Roztáhnout všechny obrázky"
            statusLine = u"Stavový řádek"
            toolBar = u"Nástrojová lišta"
            toolTipFile = u"Napište název souboru nebo kliknutím na tlačítko otevřete dialog"
            width = u"Šířka:"
            winMode1 = u"Přizpůsobit okno obrázku"
            winMode2 = u"Přizpůsobit obrázky oknu"
            winMode3 = u"Přizpůsobit oknu pouze velké obrázky"
            winMode4 = u"Přizpůsobit obrázky pracovní ploše"
            winMode5 = u"Přizpůsobit ploše pouze velké obrázky"
            winMode6 = u"Nepřizpůsobovat"
            winMode7 = u"Přizpůsobit obrázky šířce prac. plochy"
            winMode8 = u"Přizpůsobit obrázky výšce prac. plochy"
            windowHide = u"Skrýt prvky okna (vybráno=skrýt)"
            windowOption = u"Možnosti režimu Okno"
            xCoord = u"X souřadnice:"
            yCoord = u"Y souřadnice:"
        class SaveAs:
            name = u'Zobrazit dialog "Uložit jako"'
            description = u'Zobrazí dialog "Uložit jako".'
        class SaveDialog:
            name = u'Zobrazit dialog "Uložit"'
            description = u'Zobrazí dialog "Uložit".'
        class ScrollDownOrNext:
            name = u"Dolů nebo další soubor"
            description = u"Otevře další soubor ve složce anebo posune obrázek dolů."
        class ScrollImageDown:
            name = u"Posunout dolů"
            description = u"Posune obrázek dolů."
        class ScrollImageUp:
            name = u"Posunout nahoru"
            description = u"Posune obrázek nahoru."
        class ScrollLeftOrPrevious:
            name = u"Vlevo nebo předchozí soubor"
            description = u"Posune obrázek vlevo nebo otevře předchozí soubor."
        class ScrollRightOrNext:
            name = u"Vpravo nebo další soubor"
            description = u"Posune obrázek vpravo nebo otevře další soubor."
        class ScrollToBeginOrFirstFile:
            name = u"Posunout na začátek nebo otevřít první soubor"
            description = u"Posune na začátek (horizontálně) nebo otevře první soubor ve složce."
        class ScrollToEndOrLastFile:
            name = u"Posunout na konec nebo otevřít poslední soubor"
            description = u"Posune na konec (horizontálně) nebo otevře poslední soubor ve složce."
        class ScrollUpOrPrevious:
            name = u"Nahoru nebo předchozí soubor"
            description = u"Otevře předchozí soubor ve složce anebo posune obrázek nahoru."
        class SearchFiles:
            name = u"Hledat soubory"
            description = u"Hledá soubory."
        class SelectAllThumb:
            name = u"Vybrat všechny miniatury"
            description = u"Vybere všechny miniatury (v okně miniatur)."
        class SendByMail:
            name = u"Poslat obrázek e-mailem"
            description = u"Pošle obrázek e-mailem."
        class Sharpen:
            name = u"Zaostřit"
            description = u"Zaostří obrázek."
        class ShowCommentDialog:
            name = u'Zobrazit dialog "Komentář JPG souboru"'
            description = u'Zobrazí dialog "Komentář JPG souboru".'
        class ShowExifDialog:
            name = u'Zobrazit dialog "EXIF info"'
            description = u'Zobrazí dialog "EXIF info".'
        class ShowInHexViewer:
            name = u"Zobrazit v HEX prohlížeči"
            description = u"Otevře obrázek v HEX prohlížeči."
        class ShowInformation:
            name = u"Zobrazit informace o obrázku"
            description = u"Zobrazí informace o obrázku."
        class ShowIptcDialog:
            name = u"Zobrazit dialog IPTC"
            description = u"Zobrazí dialog IPTC."
        class ShowNextPgOrFile:
            name = u"Další stránku nebo soubor"
            description = u"Zobrazí další stránku vícestránkového obrázku nebo otevře další obrázek ve složce."
        class ShowPrevPgOrFile:
            name = u"Předchozí stránku nebo soubor"
            description = u"Zobrazí předchozí stránku vícestránkového obrázku nebo otevře předchozí obrázek ve složce."
        class SlideshowDialog:
            name = u"Zobrazit dialog Prezentace"
            description = u"Zobrazí dialog Prezentace."
        class StartDirSlideshow:
            name = u"Spustit prezentaci ve složce"
            description = u"Spustí prezentaci ze souborů aktuální složky."
        class StopAnimation:
            name = u"Zastavit animaci"
            description = u"Zastaví GIF nebo ANI animaci."
        class SwitchMainThumbnail:
            name = u"Přepnout okno hlavní/miniatury"
            description = u"Přepne mezi hlavním oknem a oknem miniatur (je-li viditelné)."
        class Thumbnails:
            name = u"Miniatury"
            description = u"Miniatury."
        class ToggleAutSlideshow1:
            name = u'Spustit/zastavit "Prezentaci v okně"'
            description = u'Spustí/zastaví  "Prezentaci v okně".'
        class ToggleAutSlideshow2:
            name = u"Zastavit/spustit prezentaci"
            description = u"Zastaví prezentaci. Při opětovném použití prezentace pokračuje."
        class ToggleCaption:
            name = u"Zobrazit/skrýt záhlaví okna"
            description = u"Zobrazí/skryje záhlaví okna."
        class ToggleFit:
            name = u"Přizpůsobit ploše/přizpůsobit obrázku"
            description = u'Přepíná mezi "Přizpůsobit obrázky ploše" a "Přizpůsobit okno obrázku".'
        class ToggleLockZoom:
            name = u"Zamknout/odemknout zvětšení"
            description = u"Zamkne/odemkne zvětšení (také v režimu Celá obrazovka)."
        class ToggleMenuBar:
            name = u"Zobrazit/skrýt nabídkovou lištu"
            description = u"Zobrazí/skryje nabídkovou lištu."
        class ToggleSlideshow:
            name = u"Zobrazit/skrýt text (celá obrazovka/prezentace)"
            description = u"Zobrazí/skryje text (v režimech celá obrazovka/prezentace)."
        class ToggleStatusBar:
            name = u"Zobrazit/skrýt stavový řádek"
            description = u"Zobrazí/skryje stavový řádek."
        class ToggleToolbar:
            name = u"Zobrazit/skrýt nástrojovou lištu"
            description = u"Zobrazí/skryje nástrojovou lištu."
        class VerticalFlip:
            name = u"Vertikální překlopení"
            description = u"Vertikální překlopení."
        class WallpaperCentered:
            name = u"Nastavit jako pozadí plochy - na střed"
            description = u"Nastaví obrázek jako pozadí plochy - na střed."
        class WallpaperStretched:
            name = u"Nastavit jako pozadí plochy - roztáhnout"
            description = u"Nastaví obrázek jako pozadí plochy - roztáhnout"
        class WallpaperTiled:
            name = u"Nastavit jako pozadí plochy - vedle sebe"
            description = u"Nastaví obrázek jako pozadí plochy - vedle sebe"
        class ZoomIn:
            name = u"Zvětšit"
            description = u"Zvětší obrázek."
        class ZoomOut:
            name = u"Zmenšit"
            description = u"Zmenší obrázek."
    class Joystick:
        name = u"Pákový ovladač"
        description = u"Umožňuje použít pákové ovladače a gamepady jako vstupní zařízení pro EventGhost."
    class Keyboard:
        name = u"Klávesnice"
        description = u"Tento plugin generuje události stisknutím kláves (horké klávesy)."
    class MediaMonkey:
        name = u"MediaMonkey"
        description = u'Přidává podporu funkcí pro řízení programu <a href="http://www.MediaMonkey.com/">MediaMonkey</a>.'
        errorConnect = u"MediaMonkey není spuštěn nebo připojen"
        errorNoWindow = u"Nemohu najít okno MediaMonkey"
        extrGrpDescr = u"Zde je akce pro zápis některých parametrů do MediaMonkey."
        extrGrpName = u"Zápis do MediaMonkey"
        infoGrpDescr = u"Zde najdete akce pro získávání informací z MediaMonkey."
        infoGrpName = u"Získávání informací"
        levelGrpDescr = u"Zde najdete další akce pro řízení MediaMonkey (hlasitost, stereováha, posouvání)."
        levelGrpName = u"Další řízení MediaMonkey"
        mainGrpDescr = u"Zde najdete akce pro hlavní řízení MediaMonkey."
        mainGrpName = u"Hlavní řízení MediaMonkey"
        class BalanceLeft:
            name = u"Stereováha vlevo x%"
            description = u"Stereováha vlevo x%."
            label_conf = u"Krok stereováhy:"
            label_tree = u"Stereováhu vlevo o "
        class BalanceRight:
            name = u"Stereováha vpravo x%"
            description = u"Stereováha vpravo x%."
            label_conf = u"Krok stereováhy:"
            label_tree = u"Stereováhu vpravo o "
        class DiscretePause:
            name = u"Šetrně zastavit"
            description = u"Hraje-li MediaPlayer, zastaví ho. Jinak nedělá nic."
        class Exit:
            name = u"Ukončit MediaMonkey"
            description = u"Ukončí MediaMonkey."
        class GetBalance:
            name = u"Získat stereováhu"
            description = u"Získá stereováhu."
        class GetBasicSongInfo:
            name = u"Získat základní informace"
            description = u"Získá základní informace o aktuální skladbě."
            album = u"Album"
            albumartist = u"Interpret alba"
            artist = u"Interpret"
            comment = u"Komentář"
            filename = u"Název souboru"
            filepath = u"Cesta"
            genre = u"Žánr"
            rating = u"Hodnocení"
            track = u"Skladba č."
            tracktitle = u"Název"
            year = u"Rok"
        class GetClassificationInfo:
            name = u"Získat klasifikaci"
            description = u"Získá informace o klasifikaci aktuální skladby."
            custom1 = u"Vlastní 1"
            custom2 = u"Vlastní 2"
            custom3 = u"Vlastní 3"
            mood = u"Nálada"
            occasion = u"Příležitost"
            quality = u"Kvalita"
            tempo = u"Tempo"
        class GetDetailSongInfo:
            name = u"Získat detailní informace"
            description = u"Získá detailní informace o aktuální skladbě."
            BPM = u"BPM"
            ISRC = u"ISRC"
            copyright = u"Copyright"
            encoder = u"Enkodér"
            involvedpeople = u"Další osoby"
            lyricist = u"Textař"
            originalartist = u"Původní interpret"
            originallyricist = u"Původní textař"
            originaltitle = u"Původní název"
            publisher = u"Vydavatel"
        class GetPosition:
            name = u"Získat pozici v ms"
            description = u"Získá pozici v ms."
        class GetRepeat:
            name = u"Získat nepřetržité hraní"
            description = u"Získá informaci o nastavení funkce nepřetržité hraní."
        class GetShuffle:
            name = u"Získat zamíchat skladby"
            description = u"Získá informaci o nastavení funkce zamíchat skladby."
        class GetStatus:
            name = u"Získat stav"
            description = u"Získá informaci, v jakém stavu je MediaMonkey (vrací řetězec Playing, Paused nebo Stoped)."
        class GetTechnicalSongInfo:
            name = u"Získat technické informace"
            description = u"Získá technické informace o aktuální skladbě."
            VBR = u"VBR"
            bitrate = u"Bitrate"
            counter = u"Počet přehrání"
            filesize = u"Velikost"
            frequency = u"Vzorkovací fr."
            lastplayed = u"Naposledy hráno"
            length = u"Délka"
            leveling = u"Vyrovnání"
            stereo = u"Stereo"
        class GetUniversal:
            name = u"Získat univerzální informaci"
            description = u"Získá univerzální informaci"
            get = u"Získat "
            label = u"Výběr požadované informace:"
            class Properties:
                AlbumArtCount = u"Počet obrázků alba"
                AlbumArtistName = u"Jméno interpreta alba"
                AlbumLength = u"Délka alba"
                AlbumLengthString = u"Řetězec délka alba"
                AlbumName = u"Jméno alba"
                ArtistCount = u"Počet intepretů"
                ArtistName = u"Jméno interpreta"
                Author = u"Autor"
                BPM = u"BPM"
                Band = u"Skupina/Orchestr"
                Bitrate = u"Bitrate"
                Channels = u"Stereo"
                Comment = u"Komentář"
                Conductor = u"Dirigent"
                Copyright = u"Copyright"
                Custom1 = u"Vlastní 1"
                Custom2 = u"Vlastní 2"
                Custom3 = u"Vlastní 3"
                DateAdded = u"Datum přidání"
                Encoder = u"Ennkodér"
                FileLength = u"Délka souboru"
                FileModified = u"Soubor změněn"
                Genre = u"Žánr"
                ISRC = u"ISRC"
                InvolvedPeople = u"Další osoby"
                IsntInDB = u"Není v databázi"
                LastPlayed = u"Naposledy hráno"
                Leveling = u"Vyrovnání"
                Lyricist = u"Textař"
                Lyrics = u"Text"
                MediaDriveLetter = u"Písmeno media (disku)"
                MediaDriveType = u"Typ média"
                MediaLabel = u"Pojmenování média"
                MediaSerialNumber = u"Sériové číslo média"
                Mood = u"Nálada"
                MusicComposer = u"Skladatel"
                Occasion = u"Příležitost"
                OriginalArtist = u"Původní interpret"
                OriginalLyricist = u"Původní textař"
                OriginalTitle = u"Původní název"
                OriginalYear = u"Původní rok"
                Path = u"Cesta"
                PeakValue = u"Vrcholová úroveň"
                PlayCounter = u"Počet přehrání"
                PlaylistOrder = u"Číslo seznamu"
                Preview = u"Náhled"
                PreviewPath = u"Cesta náhledu"
                Publisher = u"Vydavatel"
                Quality = u"Kvalita"
                Rating = u"Hodnocení"
                RatingString = u"Řetězec hodnocení"
                SampleRate = u"Vzorkovací fr."
                SongLength = u"Délka skladby"
                SongLengthString = u"Řezězec délka skladby"
                Tempo = u"Tempo"
                Title = u"Název"
                TrackOrder = u"Číslo stopy"
                VBR = u"VBR"
                Year = u"Rok"
        class GetVolume:
            name = u"Získat hlasitost"
            description = u"Získá hlasitost."
        class Next:
            name = u"Další"
            description = u"Skočí na další skladbu"
        class Play:
            name = u"Hrát"
            description = u"Spustí přehrávání."
        class Previous:
            name = u"Předchozí"
            description = u"Skočí na předchozí skladbu"
        class Seek:
            name = u"Skočit vpřed nebo vzad o x%"
            description = u"Skočí vpřed nebo vzad o x%."
            btnBackward = u"Vzad"
            btnForward = u"Vpřed"
            label = u"Délka skoku (%):"
            radiobox = u"Směr posouvání"
            tree_lab1 = u"Skočit "
            tree_lab2 = u"vzad"
            tree_lab3 = u"vpřed"
        class SetBalance:
            name = u"Nastavit stereováhu"
            description = u"Nastaví stereováhu."
            label_conf = u"Streováha (-100 ... 100):"
            label_tree = u"Nastavit stereováhu na "
        class SetVolume:
            name = u"Nastavit hlasitost"
            description = u"Nastaví hlasitost na dané procento (%)."
            label_conf = u"Úroveň hlasitosti:"
            label_tree = u"Nastavit úroveň hlasitosti "
        class Start:
            name = u"Spustit nebo připojit MediaMonkey"
            description = u"Spustí nebo připojí MediaMonkey pomocí COM-API."
            error = u"Nemohu se připojit k MediaMonkey"
        class Stop:
            name = u"Stop"
            description = u"Simuluje stisk tlačítka Stop."
        class ToggleMute:
            name = u"Umlčet/Obnovit"
            description = u"Umlčí nebo obnoví původní hlasitost."
        class TogglePlay:
            name = u"Hrát/Pozastavit"
            description = u"Spouští anebo pozastavuje přehrávání."
        class VolumeDown:
            name = u"Snížit hlasitost"
            description = u"Sníží hlasitost o x%."
            label_conf = u"Krok v %:"
            label_tree = u"Snížit hlasitost o "
        class VolumeUp:
            name = u"Zvýšit hlasitost"
            description = u"Zvýší hlasitost o x%."
            label_conf = u"Krok v %:"
            label_tree = u"Zvýšit hlasitost o "
        class WritingToMM:
            name = u"Zapsat do databáze MM"
            description = u"Zápis některých parametrů do databáze MediaMonkey."
            checkboxlabel = u"Zapsat také do ID3 tagu"
            label = u"Výběr požadované vlastnosti:"
            set = u"Nastavit "
            class Properties:
                Comment = u"Komentář"
                Custom1 = u"Vlastní 1"
                Custom2 = u"Vlastní 2"
                Custom3 = u"Vlastní 3"
                Genre = u"Žánr"
                Mood = u"Nálada"
                Occasion = u"Příležitost"
                Quality = u"Kvalita"
                Rating = u"Hodnocení"
                Tempo = u"Tempo"
    class MediaPlayerClassic:
        name = u"Media Player Classic"
        description = u"Přidává podporu funkcí k ovládání aplikace  Media Player Classic.\n\n<p>Pouze pro verzi <b>6.4.8.9</b> nebo novější.</p>\n<p>Plugin nebude pracovat se staršími verzemi MPC !</p>\n<p>\n<a href=http://www.eventghost.org/forum/viewtopic.php?t=17>Hlášení o chybách</a></p>\n<p><a href=http://sourceforge.net/projects/guliverkli/>\nMedia Player Classic SourceForge Project</a></p>"
        class AlwaysOnTop:
            name = u"Vždy na vrchu"
            description = u"Vždy na vrchu"
        class AudioDelayAdd10ms:
            name = u"Zpoždění zvuku +10ms"
            description = u"Zpoždění zvuku +10ms"
        class AudioDelaySub10ms:
            name = u"Zpoždění zvuku -10ms"
            description = u"Zpoždění zvuku -10ms"
        class BossKey:
            name = u'Tlačítko "Šéf" (Boss)'
            description = u'Tlačítko "Šéf" (Boss)'
        class Close:
            name = u"Zavřít soubor"
            description = u"Zavře soubor"
        class DVDAngleMenu:
            name = u"DVD nabídka úhlů pohledu"
            description = u"DVD nabídka úhlů pohledu"
        class DVDAudioMenu:
            name = u"DVD nabídka - zvuk"
            description = u"DVD nabídka - zvuk"
        class DVDChapterMenu:
            name = u"DVD nabídka - kapitola"
            description = u"DVD nabídka - kapitola"
        class DVDMenuActivate:
            name = u"DVD - aktivace nabídky"
            description = u"DVD - aktivace nabídky"
        class DVDMenuBack:
            name = u"DVD nabídka - zpět"
            description = u"DVD nabídka - zpět"
        class DVDMenuDown:
            name = u"DVD nabídka - dolů"
            description = u"DVD nabídka - dolů"
        class DVDMenuLeave:
            name = u"DVD nabídka - opuštění"
            description = u"DVD nabídka - opuštění"
        class DVDMenuLeft:
            name = u"DVD nabídka - vlevo"
            description = u"DVD nabídka - vlevo"
        class DVDMenuRight:
            name = u"DVD nabídka - vpravo"
            description = u"DVD nabídka - vpravo"
        class DVDMenuUp:
            name = u"DVD nabídka - nahoru"
            description = u"DVD nabídka - nahoru"
        class DVDNextAngle:
            name = u"DVD - další úhel pohledu"
            description = u"DVD - další úhel pohledu"
        class DVDNextAudio:
            name = u"DVD - další zvuková stopa"
            description = u"DVD - další zvuková stopa"
        class DVDNextSubtitle:
            name = u"DVD - další titulky"
            description = u"DVD - další titulky"
        class DVDOnOffSubtitle:
            name = u"DVD - zapnout/vypnout titulky"
            description = u"DVD - zapne/vypne titulky"
        class DVDPrevAngle:
            name = u"DVD - předchozí úhel pohledu"
            description = u"DVD - předchozí úhel pohledu"
        class DVDPrevAudio:
            name = u"DVD - předchozí zvuková stopa"
            description = u"DVD - předchozí zvuková stopa"
        class DVDPrevSubtitle:
            name = u"DVD - předchozí titulky"
            description = u"DVD - předchozí titulky"
        class DVDRootMenu:
            name = u"DVD - hlavní nabídka"
            description = u"DVD - hlavní nabídka"
        class DVDSubtitleMenu:
            name = u"DVD - nabídka titulků"
            description = u"DVD - nabídka titulků"
        class DVDTitleMenu:
            name = u"DVD - úvodní nabídka"
            description = u"DVD - úvodní nabídka"
        class DecreaseRate:
            name = u"Snížit rychlost"
            description = u"Snížení rychlosti"
        class Exit:
            name = u"Ukončit aplikaci"
            description = u"Ukončí aplikaci"
        class FiltersMenu:
            name = u"Nabídka filtrů"
            description = u"Nabídka filtrů"
        class FrameStep:
            name = u"O snímek vpřed"
            description = u"O snímek vpřed"
        class FrameStepBack:
            name = u"O snímek vzad"
            description = u"O snímek vzad"
        class Fullscreen:
            name = u"Na celou obrazovku"
            description = u"Na celou obrazovku"
        class FullscreenWOR:
            name = u"Na celou obrazovku beze změny rozlišení"
            description = u"Na celou obrazovku beze změny rozlišení"
        class GoTo:
            name = u"Přejít na"
            description = u"Přejít na"
        class IncreaseRate:
            name = u"Zvýšit rychlost"
            description = u"Zvýšení rychlosti"
        class JumpBackwardKeyframe:
            name = u"Skok dozadu - klíčové políčko"
            description = u"Skok dozadu - klíčové políčko"
        class JumpBackwardLarge:
            name = u"Skok dozadu - velký"
            description = u"Skok dozadu - velký"
        class JumpBackwardMedium:
            name = u"Skok dozadu - střední"
            description = u"Skok dozadu - střední"
        class JumpBackwardSmall:
            name = u"Skok dozadu - malý"
            description = u"Skok dozadu - malý"
        class JumpForwardKeyframe:
            name = u"Skok dopředu - klíčové políčko"
            description = u"Skok dopředu - klíčové políčko"
        class JumpForwardLarge:
            name = u"Skok dopředu - velký"
            description = u"Skok dopředu - velký"
        class JumpForwardMedium:
            name = u"Skok dopředu - střední"
            description = u"Skok dopředu - střední"
        class JumpForwardSmall:
            name = u"Skok dopředu - malý"
            description = u"Skok dopředu - malý"
        class LoadSubTitle:
            name = u"Načíst titulky"
            description = u"Načtení titulků"
        class Next:
            name = u"Další"
            description = u"Další"
        class NextAudio:
            name = u"Další zvuková stopa"
            description = u"Další zvuková stopa"
        class NextAudioOGM:
            name = u"Další zvuková stopa OGM"
            description = u"Další zvuková stopa OGM"
        class NextPlaylistItem:
            name = u"Další položka playlistu"
            description = u"Další položka playlistu"
        class NextSubtitle:
            name = u"Další titulky"
            description = u"Další titulky"
        class NextSubtitleOGM:
            name = u"Další tituky OGM"
            description = u"Další tituky OGM"
        class OnOffSubtitle:
            name = u"Zapnout/Vypnout titulky"
            description = u"Zapnout/Vypnout titulky"
        class OpenDVD:
            name = u"Otevřít DVD"
            description = u"Otevře DVD"
        class OpenDevice:
            name = u"Otevřít zařízení"
            description = u"Otevře zařízení"
        class OpenFile:
            name = u"Otevřít soubor"
            description = u"Otevře soubor"
        class Options:
            name = u"Možnosti"
            description = u"Možnosti"
        class Pause:
            name = u"Pozastavit"
            description = u"Pozastaví přehrávání"
        class Play:
            name = u"Přehrát"
            description = u"Spustí přehrávání"
        class PlayPause:
            name = u"Přehrát/Pozastavit"
            description = u"Spustí/pozastaví přehrávání"
        class PlayerMenuLong:
            name = u"Nabídka přehrávače - dlouhá"
            description = u"Nabídka přehrávače - dlouhá"
        class PlayerMenuShort:
            name = u"Nabídka přehrávače - krátká"
            description = u"Nabídka přehrávače - krátká"
        class PnSCenter:
            name = u"Pan & Scan - vycentrovat"
            description = u"Pan & Scan - vycentruje"
        class PnSDecHeight:
            name = u"Pan & Scan - zmenšit výšku"
            description = u"Pan & Scan - zmenší výšku"
        class PnSDecSize:
            name = u"Pan & Scan - zmenšit velikost"
            description = u"Pan & Scan - zmenší velikost"
        class PnSDecWidth:
            name = u"Pan & Scan - zmenšit šířku"
            description = u"Pan & Scan - zmenší šířku"
        class PnSDown:
            name = u"Pan & Scan - posunout dolů"
            description = u"Pan & Scan - posune dolů"
        class PnSDownLeft:
            name = u"Pan & Scan - posunout dolů/doleva"
            description = u"Pan & Scan - posune dolů/doleva"
        class PnSDownRight:
            name = u"Pan & Scan - posunout dolů/doprava"
            description = u"Pan & Scan - posune dolů/doprava"
        class PnSIncHeight:
            name = u"Pan & Scan - zvětšit výšku"
            description = u"Pan & Scan - zvětší výšku"
        class PnSIncSize:
            name = u"Pan & Scan - zvětšit velikost"
            description = u"Pan & Scan - zvětší velikost"
        class PnSIncWidth:
            name = u"Pan & Scan - zvětšit šířku"
            description = u"Pan & Scan - zvětší šířku"
        class PnSLeft:
            name = u"Pan & Scan - posunout doleva"
            description = u"Pan & Scan - posune doleva"
        class PnSReset:
            name = u"Pan & Scan - výchozí nastavení"
            description = u"Pan & Scan - výchozí nastavení"
        class PnSRight:
            name = u"Pan & Scan - posunout doprava"
            description = u"Pan & Scan - posune doprava"
        class PnSRotateAddX:
            name = u"Pan & Scan - rotovat X+"
            description = u"Pan & Scan - rotuje X+"
        class PnSRotateAddY:
            name = u"Pan & Scan - rotovat Y+"
            description = u"Pan & Scan - rotuje Y+"
        class PnSRotateAddZ:
            name = u"Pan & Scan - rotovat Z+"
            description = u"Pan & Scan - rotuje Z+"
        class PnSRotateSubX:
            name = u"Pan & Scan - rotovat X-"
            description = u"Pan & Scan - rotuje X-"
        class PnSRotateSubZ:
            name = u"Pan & Scan - rotovat Z-"
            description = u"Pan & Scan - rotuje Z-"
        class PnSUp:
            name = u"Pan & Scan - posunout nahoru"
            description = u"Pan & Scan - posune nahoru"
        class PnSUpLeft:
            name = u"Pan & Scan - posunout nahoru/doleva"
            description = u"Pan & Scan - posune nahoru/doleva"
        class PnSUpRight:
            name = u"Pan & Scan - posunout nahoru/doprava"
            description = u"Pan & Scan - posune nahoru/doprava"
        class PnsRotateSubY:
            name = u"Pan & Scan - rotovat Y-"
            description = u"Pan & Scan - rotuje Y-"
        class PrevAudio:
            name = u"Předchozí zvuková stopa"
            description = u"Předchozí zvuková stopa"
        class PrevAudioOGM:
            name = u"Předchozí zvuková stopa OGM"
            description = u"Předchozí zvuková stopa OGM"
        class PrevSubtitle:
            name = u"Předchozí titulky"
            description = u"Předchozí titulky"
        class PrevSubtitleOGM:
            name = u"Předchozí titulky OGM"
            description = u"Předchozí titulky OGM"
        class Previous:
            name = u"Předchozí"
            description = u"Předchozí"
        class PreviousPlaylistItem:
            name = u"Předchozí položka playlistu"
            description = u"Předchozí položka playlistu"
        class Properties:
            name = u"Vlastnosti"
            description = u"Vlastnosti"
        class QuickOpen:
            name = u"Rychle otevřít soubor"
            description = u"Dialog pro rychlé otevření souboru"
        class ReloadSubtitles:
            name = u"Znovu načíst titulky"
            description = u"Nové načtení titulků"
        class ResetRate:
            name = u"Výchozí rychlost"
            description = u"Výchozí rychlost"
        class SaveAs:
            name = u"Uložit jako"
            description = u"Uložit jako"
        class SaveImage:
            name = u"Uložit obrázek"
            description = u"Uloží obrázek"
        class SaveImageAuto:
            name = u"Uložit miniatury"
            description = u"Aktivuje ukládání miniatur"
        class SaveSubtitle:
            name = u"Uložit titulky"
            description = u"Uloží titulky"
        class Stop:
            name = u"Zastavit"
            description = u"Zastaví přehrávání"
        class ToggleCaptionMenu:
            name = u"Skrýt/Zobrazit záhlaví okna a hlavní nabídku"
            description = u"Skryje/zobrazí záhlaví okna a hlavní nabídku"
        class ToggleCaptureBar:
            name = u"Skrýt/Zobrazit panel záznamu (Record)"
            description = u"Skryje/zobrazí panel záznamu (Record)"
        class ToggleControls:
            name = u"Skrýt/Zobrazit lištu ovládání"
            description = u"Skryje/zobrazí lištu ovládání"
        class ToggleInformation:
            name = u"Skrýt/Zobrazit panel  informací"
            description = u"Skryje/zobrazí panel  informací"
        class TogglePlaylistBar:
            name = u"Skrýt/Zobrazit okno playlistu"
            description = u"Skryje/zobrazí okno playlistu"
        class ToggleSeeker:
            name = u"Skrýt/Zobrazit panel hledání (posuvník)"
            description = u"Skryje/zobrazí panel hledání (posuvník)"
        class ToggleShaderEditorBar:
            name = u"Skrýt/Zobrazit panel editoru stínování"
            description = u"Skryje/zobrazí panel editoru stínování"
        class ToggleStatistics:
            name = u"Skrýt/Zobrazit panel statistik"
            description = u"Skryje/zobrazí panel statistik"
        class ToggleStatus:
            name = u"Skrýt/Zobrazit stavový řádek"
            description = u"Skryje/zobrazí stavový řádek"
        class ToggleSubresyncBar:
            name = u"Skrýt/Zobrazit lištu subresync"
            description = u"Skryje/zobrazí lištu subresync"
        class VidFrmDouble:
            name = u"Výřez videa - dvojnásobná velikost"
            description = u"Výřez videa - dvojnásobná velikost"
        class VidFrmHalf:
            name = u"Výřez videa - poloviční velikost"
            description = u"Výřez videa - poloviční velikost"
        class VidFrmInside:
            name = u"Výřez videa - dotknout se okna zevnitř"
            description = u"Výřez videa - dotknout se okna zevnitř"
        class VidFrmNormal:
            name = u"Výřez videa - standardní velikost"
            description = u"Výřez videa - standardní velikost"
        class VidFrmOutside:
            name = u"Výřez videa - dotknout se okna zvenčí"
            description = u"Výřez videa - dotknout se okna zvenčí"
        class VidFrmStretch:
            name = u"Výřez videa - roztáhnout do okna"
            description = u"Výřez videa - roztáhnout do okna"
        class ViewCompact:
            name = u"Předvolby - vzhled kompaktní"
            description = u"Předvolby - vzhled kompaktní"
        class ViewMinimal:
            name = u"Předvolby - vzhled minimální"
            description = u"Předvolby - vzhled minimální"
        class ViewNormal:
            name = u"Předvolby - vzhled normální"
            description = u"Předvolby - vzhled normální"
        class VolumeDown:
            name = u"Hlasitost - snížit"
            description = u"Hlasitost - snížit"
        class VolumeMute:
            name = u"Hlasitost - ztlumit"
            description = u"Hlasitost - ztlumit"
        class VolumeUp:
            name = u"Hlasitost - zvýšit"
            description = u"Hlasitost - zvýšit"
        class Zoom100:
            name = u"Velikost - 100%"
            description = u"Velikost - 100%"
        class Zoom200:
            name = u"Velikost - 200%"
            description = u"Velikost - 200%"
        class Zoom50:
            name = u"Velikost - 50%"
            description = u"Velikost - 50%"
    class Multitap:
        name = u"Multitap"
        description = u"Umožňuje vícenásobné použití tlačítek (jednak obdoba psaní SMS na mobilních telefonech, jednak vlastní nabídky) a zadávání vícemístných čísel."
        assignError = u'Konfigurace "%s" neexistuje!'
        delete = u"Odstranit"
        evtString = u"Jméno a formát události:"
        genPayload = u"Generovat jako náklad"
        genSuffix = u"Generovat jako sufix události"
        insert = u"Přidat novou"
        label = u"Jméno konfigurace:"
        labelMode = u"Režim multitaperu:"
        labelTimeout1 = u"Časový dohled:"
        labelTimeout2 = u"(0 = bez časového dohledu)"
        menuPreview = u"Seznam konfigurací:"
        numpad = u"Numpad (numerický řetězec)"
        ownOSD = u"Používat OSD"
        param = u"Konfigurační parametry"
        singleKey = u"Jednotlačítkový"
        string = u"Jako SMS"
        class BackSpace:
            name = u"Vymazat (backspace)"
            description = u"Vymaže poslední znak (backspace)."
        class Cancel:
            name = u"Storno"
            description = u"Ukončí (stornuje) akci bez generování události."
        class Enter:
            name = u"Enter"
            description = u"Ukončí zadávání znaků a spouští generování události (bez čekání na timeout)."
        class Key:
            name = u"Klávesa (tlačítko)"
            description = u"Akce po stisknutí klávesy (tlačítka)."
            configLabel = u"Konfigurace:"
            delete = u"Odstranit"
            eventPayload = u"Jméno (náklad) události:"
            eventSuffix = u"Jméno (sufix) události:"
            insert = u"Přidat nové"
            label_1 = u"Znaky při Caps Lock OFF:"
            label_2 = u"Znaky při Caps Lock ON:"
            label_3 = u"Číslice:"
            listEventPayload = u"Nabídka (seznam) :"
            listEventSuffix = u"Nabídka (seznam) :"
            warning = u"Není povoleno použít znak MEZERA\nna první nebo poslední pozici řetězce !"
        class Shift:
            name = u"Caps Lock"
            description = u"V režimu SMS přepíná mezi dvěma seznamy znaků."
    class NetworkReceiver:
        name = u"Síťový přijímač událostí"
        description = u'Přijímá události od pluginu "Síťový vysílač událostí"'
        eventPrefix = u"Prefix události:"
        password = u"Heslo:"
        port = u"Port:"
    class NetworkSender:
        name = u"Síťový vysílač událostí"
        description = u'Prostřednictvím TCP/IP vysílá události k pluginu "Síťový přijímač událostí".'
        host = u"Hostitel:"
        password = u"Heslo:"
        port = u"Port:"
        class Map:
            name = u"Odeslat"
            description = u"Odesílaná událost"
            parameterDescription = u"Identifikátor odesílané události:"
    class Serial:
        name = u"Sériový port"
        description = u"Libovolná komunikace přes sériový port.\n<br>Volitelně může generovat události.\n\n<p><b>Terminátor</b> je řetězec znaků, podle kterého při generování události plugin identifikuje konec přijatých dat."
        baudrate = u"Bitů za sekundu:"
        bytesize = u"Datových bitů:"
        codecChoices = [
            u"Systémová kódová stránka",
            u"HEX",
            u"Latin-1",
            u"UTF-8",
            u"UTF-16",
            u"Python escape řetězec",
        ]
        encoding = u"Kódování:"
        eventPrefix = u"Prefix události:"
        flowcontrol = u"Řízení toku:"
        generateEvents = u"Generovat události z příchozích dat"
        handshakes = [
            u"Žádné",
            u"Xon / Xoff",
            u"Hardwarové",
        ]
        parities = [
            u"Žádná",
            u"Lichá",
            u"Sudá",
        ]
        parity = u"Parita:"
        port = u"Port:"
        stopbits = u"Počet stop-bitů:"
        terminator = u"Terminátor:"
        class Read:
            name = u"Příjem dat"
            description = u"Příjem dat"
            read_all = u"Přijme tolik bytů, kolik jich je právě k dispozici"
            read_some = u"Přijme přesně tento počet bytů:"
            read_time = u"a počká na ně tento maximální počet milisekund:"
        class Write:
            name = u"Vysílání dat"
            description = u"Vysílání dat"
    class Speech:
        name = u"Hlas"
        description = u"Použije službu převod textu na řeč Microsoft Speech API (SAPI)"
        class TextToSpeech:
            name = u"Převod textu na řeč"
            description = u"Používá Microsoft Speech API (SAPI) k převodu textu na řeč."
            buttonInsertDate = u"Vložit aktuální datum"
            buttonInsertTime = u"Vložit aktuální čas"
            errorCreate = u"Nemohu vytvořit hlasový objekt"
            errorNoVoice = u"Hlas se jménem %s není dostupný"
            fast = u"Rychle"
            label = u"Vyslovit: %s"
            labelRate = u"Rychlost:"
            labelVoice = u"Hlas:"
            labelVolume = u"Hlasitost:"
            loud = u"Nahlas"
            normal = u"Normálně"
            silent = u"Tiše"
            slow = u"Pomalu"
            textBoxLabel = u"Text"
            voiceProperties = u"Vlastnosti hlasu"
    class SysTrayMenu:
        name = u"Nabídka v oznamovací oblasti"
        description = u"Umožňuje přidat uživatelskou nabídku do systémové nabídky EventGhost (SysTrayMenu)."
        addBox = u"Přidat:"
        addItemButton = u"Položka nabídky"
        addSeparatorButton = u"Oddělovač"
        deleteButton = u"Odstranit"
        editEvent = u"Editovat:"
        editLabel = u"Nápis:"
        eventHeader = u"Událost"
        labelHeader = u"Nápis"
        unnamedEvent = u"Událost_%s"
        unnamedLabel = u"Nová položka %s"
        class Disable:
            name = u"Zakázat položku"
            description = u"Zakáže položku nabídky."
        class Enable:
            name = u"Povolit položku"
            description = u"Povolí položku nabídky."
    class Task:
        name = u"Správce úloh"
        description = u"Generuje události, související se správou úloh systému Windows."
    class Timer:
        name = u"Časovač"
        description = u"Generuje události po nastavitelné době a opakuje je v daném intervalu.\nOpakování může být nekonečné anebo je možné zadat počet opakování."
        colLabels = (
            u"Název časovače",
            u"Čas spuštění",
            u"Příští událost",
            u"ID události",
            u"Opakováno/zbývá",
            u"Opakovat",
            u"Interval",
        )
        listhl = u"Právě teď aktivní časovače:"
        stopped = u"Plugin zastaven"
        timerFinished = u"Časovač ukončen"
        class TimerAction:
            name = u"Spuštění nového nebo změna běžícího časovače"
            description = u"Umožňuje spustit, zastavit nebo resetovat časovače, které mohou generovat události po nastavené době"
            actions = (
                u"Restartovat časovač se současným nastavením",
                u"Restartovat časovač (pouze pokud běží)",
                u"Vynulovat počítadlo",
                u"Zrušit časovač",
            )
            addCounterToName = u"připojit stav počítadla k ID události"
            eventName = u"ID události:"
            interval1 = u"Interval:"
            interval2 = u"sekund"
            labelStart = u'Spustit časovač "%s" (%s opakování, interval %.2f sekund)'
            labelStartOneTime = u'Spustit časovač "%s"'
            labelStartUnlimited = u'Spustit časovač "%s" (nekonečné opakování, interval %.2f sekund)'
            labels = (
                u'Restartovat časovač "%s"',
                u'Restartovat časovač "%s" pouze pokud běží',
                u'Resetovat počítadlo časovače "%s"',
                u'Zrušit časovač "%s"',
            )
            loop1 = u"Opakování:"
            loop2 = u"(0 = nekonečné)"
            showRemaingLoopsText = u"počítadlo ukazuje zbývající počet opakování"
            start = u"Spustit nový časovač (právě běžící časovač se stejným názvem bude zrušen)"
            startTime = u"Spustit:"
            startTimeTypes = (
                u"okamžitě",
                u"po uplynutí doby intervalu",
                u"přesně v tento čas (HH:MM:SS)",
                u"po uplynutí této doby (HH:MM:SS)",
                u"v příští celé minutě",
                u"v příští celé 5-minutě",
                u"v příští celé čtvthodině",
                u"v příští celé půlhodině",
                u"v příští celé hodině",
            )
            timerName = u"Název časovače:"
    class UIR:
        description = u'Hardwarový plugin pro IR přijímače <a href="http://fly.cc.fer.hr/~mozgic/UIR/">Universal Infrared Receiver V1 (UIR)</a> a <a href="http://www.evation.com/irman/index.html">Irman</a>.\n\n<p><center><img src="irman_front.jpg" alt="Irman" /></a></center>'
    class Webserver:
        name = u"Webový server"
        description = u"Implementuje malý webový server, který může být použit pro generování\nudálostí prostřednictvím HTML-stránek."
        documentRoot = u"Kořenový adresář HTML dokumentu:"
        eventPrefix = u"Prefix události:"
        port = u"Port:"
