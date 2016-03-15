# -*- coding: UTF-8 -*-
class General:
    apply = u"Zastosuj"
    autostartItem = u"Autostart"
    browse = u"Przeglądaj..."
    cancel = u"Anuluj"
    choose = u"Wybierz"
    configTree = u"Drzewko konfiguracyjne elementów"
    deleteManyQuestion = u"Ten element posiada %s subelementy.\nCzy jesteś pewien, że chcesz usunąć wszystkie elementy?"
    deletePlugin = u"Ten plugin jest używany do akcji skonfigurowanych przez Ciebie.\nNie możesz go usunąć dopóki nie usuniesz wszelkich akcji używanych przez ten plugin."
    deleteQuestion = u"Czy na pewno chcesz usunąć ten element?"
    help = u"&Pomoc"
    moreTag = u"więcej..."
    noOptionsAction = u"Ta akcja nie ma konfigurowalnych opcji."
    noOptionsPlugin = u"Ten plugin nie ma konfigurowalnych opcji."
    ok = u"OK"
    pluginLabel = u"Plugin: %s"
    test = u"&Test"
    unnamedEvent = u"<Zdarzenie bez nazwy>"
    unnamedFile = u"<BezNazwy>"
    unnamedFolder = u"<Nowy folder>"
    unnamedMacro = u"<Makro bez nazwy>"
class MainFrame:
    onlyLogAssigned = u"&Loguj tylko przypisane i aktywne zdarzenia"
    class Logger:
        caption = u"Log"
        descriptionHeader = u"Opis"
        timeHeader = u"Czas"
        welcomeText = u"---> Witaj w EventGhost <---"
    class Menu:
        About = u"&O programie EventGhost"
        AddAction = u"Dodaj akcje"
        AddEvent = u"Dodaj zdarzenie"
        AddFolder = u"Dodaj folder"
        AddMacro = u"Dodaj Makro"
        AddPlugin = u"Dodaj Plugin"
        Apply = u"&Zastosuj zmiany"
        CheckUpdate = u"Sprawdź aktualizacje...."
        ClearLog = u"Wyczyść logi"
        Close = u"&Zamknij"
        CollapseAll = u"&Zwiń wszystko"
        ConfigurationMenu = u"&Konfiguracja"
        Configure = u"Konfiguruj element"
        Copy = u"&Kopiuj"
        Cut = u"Wy&tnij"
        Delete = u"&Usuń"
        Disabled = u"Wyłącz element"
        EditMenu = u"&Edytuj"
        Execute = u"Uruchom element"
        Exit = u"&Zakończ"
        ExpandAll = u"&Rozwiń wszystko"
        ExpandOnEvents = u"Automatycznie wyróżnij wydarzenie"
        ExpandTillMacro = u"Automatycznie rozwiń makro"
        Export = u"Exportuj..."
        FileMenu = u"&Plik"
        Find = u"&Szukaj"
        FindNext = u"Znajdź następny"
        HelpMenu = u"&Pomoc"
        HideShowToolbar = u"Pasek"
        Import = u"Importuj..."
        LogActions = u"Loguj akcje"
        LogMacros = u"Loguj makra"
        LogTime = u"Loguj czasy"
        New = u"&Nowy"
        Open = u"&Otwórz"
        Options = u"&Opcje..."
        Paste = u"&Wklej"
        Redo = u"&Ponów"
        Rename = u"Zmień nazwę elementu"
        Reset = u"Resetuj"
        Save = u"&Zapisz"
        SaveAs = u"Zapisz jako..."
        SelectAll = u"Zaznacz &wszystko"
        Undo = u"&Cofnij"
        ViewMenu = u"Widok"
        WebForum = u"Forum wsparcia"
        WebHomepage = u"Strona programu"
        WebWiki = u"Wiki"
    class SaveChanges:
        mesg = u"Plik został zmieniony\n\nCzy chcesz zachować wszelkie zmiany?"
        title = u"Zapisać zmiany?"
    class TaskBarMenu:
        Exit = u"Zakończ"
        Hide = u"Ukryj EventGhost"
        Show = u"Pokaż EventGhost"
    class Tree:
        caption = u"Konfiguracja"
class Error:
    FileNotFound = u'Plik "%s" nie został odnaleziony.'
    InAction = u'Błąd w Akcji: %s"'
    configureError = u"Błąd w trakcie konfiguracji: %s"
    pluginLoadError = u"Błąd w trakcie ładowania pliku pluginu %s."
    pluginNotActivated = u'Plugin "%s" nie jest aktywny'
    pluginStartError = u"Błąd w trakcie startu pluginu: %s"
class Exceptions:
    DeviceInitFailed = u"Nie można uruchomić urządzenia!"
    DeviceNotFound = u"Nie znaleziono urządzenia!"
    DeviceNotReady = u"Urządzenie nie jest gotowe!"
    DriverNotFound = u"Sterownik nie został odnaleziony!"
    DriverNotOpen = u"Nie można uruchomić sterownika!"
    PluginNotFound = u"Nie odnaleziono plugina!"
    ProgramNotFound = u"Nie odnaleziono programu!"
    ProgramNotRunning = u"Program nie jest uruchomiony!"
class CheckUpdate:
    ManErrorMesg = u"Nie udało się uzyskać informacji ze strony EventGhost'a.\n\nSpróbuj poźniej."
    ManErrorTitle = u"Błąd w trakcie sprawdzania aktualizacji"
    ManOkMesg = u"Ta wersja EventGhost'a jest najnowsza."
    ManOkTitle = u"Nie ma nowszych wersji"
    downloadButton = u"Odwiedź stronę pobierania"
    newVersionMesg = u"Została wydana nowsza wersja EventGhost'a.\n\n               Twoja wersja:          %s\n               Najnowsza wersja:          %s\n\nCzy chcesz odwiedzić stronę pobierania?"
    title = u"Nowa wersja EventGhost'a jest dostępna..."
    waitMesg = u"Czekaj, aż EventGhost uzyska informacje o aktualizacji."
class AddActionDialog:
    descriptionLabel = u"Opis"
    title = u"Wybierz akcję, aby dodać..."
class AddPluginDialog:
    author = u"Autor:"
    descriptionBox = u"Opis"
    externalPlugins = u"Urządzenia zewnętrzne"
    noInfo = u"Nie ma dostępnych informacji."
    otherPlugins = u"Inne"
    programPlugins = u"Plugin programu"
    remotePlugins = u"Plugin pilota"
    title = u"Wybierz wtyczkę, aby dodać..."
    version = u"Wersja:"
class AddActionGroupDialog:
    caption = u"Dodać akcje?"
class OptionsDialog:
    CheckUpdate = u"Sprawdzaj, czy jest nowsza wersja podczas uruchamiania"
    HideOnClose = u"Chowaj do tray'a przy próbie zamknięcia"
    HideOnStartup = u"Ukrywaj przy starcie"
    LanguageGroup = u"Język"
    StartWithWindows = u"Uruchamiaj wraz z Windowsa"
    Tab1 = u"Ogólne"
    Title = u"Opcje"
    Warning = u"Zmiana języka nastąpi dopiero po ponownym uruchomieniu aplikacji."
    confirmDelete = u"Potwierdzaj kasację drzewka elementów"
    limitMemory1 = u"Zmniejsz zużycie zasobów podczas minimalizacji do"
    limitMemory2 = u"MB"
class FindDialog:
    direction = u"Kierunek"
    down = u"&W dół"
    findButton = u"&Znajdź następny"
    notFoundMesg = u'"%s" nie zostało znalezione.'
    searchLabel = u"&Znajdź:"
    title = u"Znajdowanie"
    up = u"&W górę"
    wholeWordsOnly = u"Uwzględnij całe wyrazy "
class AboutDialog:
    Author = u"Autor: %s"
    CreationDate = u"%a, %d %b %Y %H:%M:%S"
    Title = u"O programie EventGhost"
    Version = u"Wersja: %s (build %s)"
    tabAbout = u"O programie"
    tabChangelog = u"Changelog"
    tabLicense = u"Umowa licencyjna"
    tabSpecialThanks = u"Specjalne podziękowania"
    tabSystemInfo = u"Informacje o systemie"
class Plugin:
    class EventGhost:
        name = u"EventGhost"
        description = u"Tutaj znajdują się akcje, które głównie kontrolują rdzenne funkcje EventGhost'a."
        class Comment:
            name = u"Komentarz"
        class DisableItem:
            name = u"Wyłącza wybrany element"
            description = u"Wyłącz element"
            label = u"Wyłącz: %s"
            text1 = u"Proszę wybrać element, który ma być wyłączony:"
        class EnableItem:
            name = u"Włącz element"
            label = u"Włącz: %s"
            text1 = u"Proszę wybrać element, który powinien być włączony:"
        class JumpIf:
            mesg1 = u"Wybierz makro..."
        class NewJumpIf:
            name = u"Skocz"
            mesg1 = u"Wybierz makro..."
        class ShowOSD:
            alignmentChoices = [
                u"U góry po lewo",
                u"U góry po prawo",
                u"Na dole po lewo",
                u"Na dole po prawo",
                u"Na środku",
                u"Po środku na dole",
                u"Po środku na górze",
                u"Po środku na lewo",
                u"Po środku na prawo",
            ]
    class System:
        name = u"System"
        description = u"Kontroluje różne aspekty systemu, jak np. karta dźwiękowa, karta graficzna, zarządzania energią, itp."
        forced = u"Wymuś: %s"
        forcedCB = u"Wymuś zamknięcie wszystkich programów"
        class ChangeDisplaySettings:
            name = u"Zmień ustawienia wyświetlania"
            description = u"Zmień ustawienia wyświetlania"
            colourDepth = u"Głębia kolorów:"
            display = u"Monitor:"
            frequency = u"Odświeżanie"
            includeAll = u"Pokaż tryby, które ten monitor może nie wyświetlić."
            label = u"Ustaw monitor%d w tryb %dx%d@%d Hz"
            resolution = u"Rozdzielczość:"
            storeInRegistry = u"Zachowaj ustawienie w rejestrze."
        class ChangeMasterVolumeBy:
            name = u"Zmiana głośności"
            description = u"Zmienia głośność w odniesieniu do bieżącej wartości"
            text1 = u"Zmień głośności o"
            text2 = u"procent."
        class Execute:
            name = u"Uruchom aplikacje"
            description = u"Uruchamia plik wykonywalny (*.exe)."
            FilePath = u"Ścieżka do pliku:"
            Parameters = u"Opcje linii poleceń:"
            ProcessOptions = (
                u"Czasu rzeczywistego",
                u"Powyżej normalnego",
                u"Normalny",
                u"Poniżej normalnego",
                u"Niski",
            )
            ProcessOptionsDesc = u"Priorytet procesu:"
            WindowOptions = (
                u"Normalne",
                u"Zminimalizowane",
                u"Zmaksymalizowane",
                u"Ukryte",
            )
            WindowOptionsDesc = u"Opcje okna:"
            label = u"Uruchom program: %s"
        class Hibernate:
            name = u"Hibernacja"
            description = u"Hibernacja jest to stan, w którym komputer jest wyłączony, ale zawartość jego pamięci ulotnej zachowana jest na nośniku pamięci stałej (np. dysku twardym)."
        class LockWorkstation:
            name = u"Zablokuj komputer"
            description = u"Ta funkcja blokuje ekran stacji roboczej. Zabezpiecza to przed nieautoryzowanym dostępem do systemu. Jest to ta sama funkcja, którą uruchamia się poprzez wciśniecie Ctrl+Alt+Del i wybraniu opcji Zablokuj ten komputer."
        class LogOff:
            name = u"Wyloguj bieżącego użytkownika"
            description = u"Zamyka wszystkie aktywne procesy w bieżącej sesji, a następnie wylogowuje użytkownika."
        class MonitorGroup:
            name = u"Ekran"
            description = u"Te opcje służą do zarządzania ekranem komputera."
        class MonitorPowerOff:
            name = u"Ustaw monitor w tryb uśpienia"
            description = u"Ustawia monitor w tryb uśpienia. Jest to najlepszy tryb oszczędności energii, jaki posiada monitor."
        class MonitorPowerOn:
            name = u"Wybudź monitor z trybu uśpienia"
            description = u"Wybudza monitor, jeśli był w trybie uśpienia lub niskiego poboru energii. Zatrzymuje również wyświetlanie wygaszacza."
        class MonitorStandby:
            name = u"Ustaw monitor w tryb Stand-by"
            description = u"Ustawia stan wyświetlacza do trybu niskiego poboru mocy."
        class MuteOff:
            name = u"Wyłącz wyciszenie"
            description = u"Wyłącz wyciszenie"
        class MuteOn:
            name = u"Włącz wyciszenie"
            description = u"Włącz wyciszenie"
        class OpenDriveTray:
            name = u"Wsuń/wysuń tackę napędu"
            description = u"Kontroluje tackę napędu CD/DVD-ROM."
            driveLabel = u"Napęd:"
            options = [
                u"Przełączać pomiędzy wysunięciem a wsunięciem tacki",
                u"Tylko wysuń tackę napędu",
                u"Tylko wsuń tackę napędu",
            ]
            optionsLabel = u"Wybierz akcję"
        class PlaySound:
            name = u"Uruchom dźwięk"
            description = u"Uruchom dźwięk"
            fileMask = u"Pliki wav (*.WAV)|*.wav|Wszystkie pliki (*.*)|*.*"
            text1 = u"Ścieżka do pliku:"
        class PowerDown:
            name = u"Wyłącz komputer"
            description = u"Zamyka system i wyłącza komuter. System musi obsługiwać tę funkcję."
        class PowerGroup:
            name = u"Zarządzanie zasilaniem"
            description = u"Działania te wstrzymują, hibernują, uruchamiają ponownie lub wyłączają komputer. Mogą również blokować stację roboczą oraz wylogowywać bieżącego użytkownika."
        class Reboot:
            name = u"Uruchom ponownie komputer"
            description = u"Uruchamia ponownie komputer"
        class RegistryChange:
            name = u"Zmień wartość rejestru"
            description = u"Zmień wartość w rejestrze Windowsa"
            actions = (
                u"utwórz lub zmień",
                u"zmieni, jeśli tylko istnieje",
                u"skasuj",
            )
            labels = (
                u'Zmiana "%s" na %s',
                u'Zmiana "%s" na %s jeśli tylko istnieje',
                u'Usuwanie "%s"',
            )
        class RegistryGroup:
            name = u"Rejestr"
            description = u"Zapytania lub zmiany wartości w Rejestrze systemu Windows."
            actionText = u"Akcja:"
            chooseText = u"Wybierz klucz rejestru"
            keyOpenError = u"Błąd podczas otwierania klucza rejestru"
            keyText = u"Klucz:"
            keyText2 = u"Klucz"
            newValue = u"Nowa wartość:"
            oldType = u"Aktualny typ:"
            oldValue = u"Aktualna wartość:"
            valueChangeError = u"Błąd podczas modyfikowania wartości"
            valueName = u"Nazwa wartości:"
            valueText = u"Wartość:"
        class RegistryQuery:
            name = u"Zapytanie rejestru"
            description = u"Wysyła zapytanie do rejestru systemu Windows, a następnie zwraca lub porównuje wartość"
            actions = (
                u"sprawdź, czy istnieje",
                u"zwróć jako rezultat",
                u"porównaj do",
            )
            labels = (
                u'Sprawdzanie, czy "%s" istnieje',
                u'Zwracanie "%s" jako rezultat',
                u'Porównywanie "%s" z %s',
            )
        class SetClipboard:
            name = u"Kopiuj ciąg do schowka"
            description = u"Kopiuje ciąg parametru do systemowego schowka."
            error = u"Nie można otworzyć schowka"
        class SetMasterVolume:
            name = u"Ustaw głośność"
            description = u"Ustawia głośność na wybraną wartość."
            text1 = u"Ustaw głośność na"
            text2 = u"procent."
        class SetWallpaper:
            name = u"Zmiana tapety"
            description = u"Zmiana tapety"
            choices = (
                u"Wyśrodkowane",
                u"Sąsiadująco",
                u"Rozciągnięte",
            )
            fileMask = u"Wszystkie typy obrazków|*.jpg;*.bmp;*.gif;*.png|All Files (*.*)|*.*"
            text1 = u"Ścieżka do obrazka:"
            text2 = u"Wyrównanie:"
        class ShowPicture:
            name = u"Pokaż obrazek"
            description = u"Pokazuje wybrany obrazek na ekranie."
            allFiles = u"Wszystkie pliki"
            allImageFiles = u"Wszystkie pliki obrazków"
            display = u"Monitor"
            path = u"Ścieżka pliku (pozostaw puste, aby wyczyścić)"
        class SoundGroup:
            name = u"Karta dźwiękowa"
            description = u"Działania te kontrolują kartę dźwiękową komputera."
        class Standby:
            name = u"Wstrzymaj"
            description = u"Ta funkcja ustawia system w stan wstrzymania."
        class StartScreenSaver:
            name = u"Uruchom wygaszacz ekranu"
            description = u"Uruchamia aktualnie ustawiony wygaszacz ekranu."
        class ToggleMute:
            name = u"Wycisz dźwięk"
            description = u"Wycisz dźwięk"
        class WakeOnLan:
            name = u"Wake on LAN"
            description = u"Dzięki funkcji Wake On LAN możliwe jest zdalne uruchomienie komputera za pośrednictwem sieci. "
            parameterDescription = u"Adres MAC karty sieciowej, aby obudzić:"
    class Window:
        name = u"Okno"
        description = u"Akcje powiązane z kontrolowaniem okienek na pulpicie, np. znajdowanie wybranego okienka, przesuwanie, powiększanie i naciskanie klawiszy na nich."
        class BringToFront:
            name = u"Doprowadzić na wierzch"
            description = u"Doprowadza wybrane okno na wierzch."
        class Close:
            name = u"Zamknij"
            description = u"Zamyka okno aplikacji"
        class FindWindow:
            name = u"Znajdź okno"
        class Maximize:
            name = u"Maksymalizuj"
            description = u"Maksymalizuje okno."
        class Minimize:
            name = u"Minimalizuj"
            description = u"Minimalizuje okno."
        class MoveTo:
            name = u"Przenieś okno"
            description = u"Przenieś okno"
            label = u"Przenieś okno na %s"
            text1 = u"Ustaw pozycję poziomą X na"
            text2 = u"piksel"
            text3 = u"Ustaw pozycję pionową Y na"
            text4 = u"piksel"
        class Resize:
            name = u"Zmień wielkość"
            description = u"Zmienia wielkość okna do podanych parametrów."
            label = u"Zmiena wielkości okna do %s, %s"
            text1 = u"Ustaw szerokość na"
            text2 = u"pikseli"
            text3 = u"Ustaw wysokość na"
            text4 = u"pikseli"
        class Restore:
            name = u"Przywróć"
            description = u"Przywróć"
        class SendKeys:
            name = u"Emuluj naciśnięcia klawiszy"
            description = u'Ta akcja emuluje naciśnięcia klawiszy, aby kontrolować programy. Wystarczy wpisać odpowiedni tekst do pola edycji.\n\n<p>\nAby emulować klawisze specjalne, musisz zamieścić słowa kluczowe w nawiasach klamrowych.\nPrzykład: jeśli chcesz emulować klawisz strzałka w górę, wpisz <b>{Up}</b>.\nMożna połączyć kilka słów kluczowych znakiem plus, aby uzyskać kombinacje takie jak:\n<b>{Ctrl + Shift + F1}</ b> lub <b>{Ctrl + V}</ b>. Wielkość słów kluczowych nie ma znaczenia, \nwięc możesz napisać {SHIFT + ctrl + F1} jeśli chcesz.\n<p>\nNiektóre klawisze znajdują się po lewej i po prawej stronie klawiatury, aby je rozróżnić\ndodaj prefiks "L" lub "R". Przykład dla klawisza z logiem Windowsa, możesz wpisać:\n<b>{Win}</b> lub <b>{LWin}</b> lub <b>{RWin}</b>.\n<p>\nA tutaj znajduje się lista pozostałych słów kluczowych, które EventGhost rozumie:<br>\n<b>{Ctrl}</b> lub <b>{Control}<br>\n{Shift}<br>\n{Alt}<br>\n{Return}</b> lub <b>{Enter}<br>\n{Back}</b> lub <b>{Backspace}<br>\n{Tab}</b> lub <b>{Tabulatlub}<br>\n{Esc}</b> lub <b>{Escape}<br>\n{Spc}</b> lub <b>{Space}<br>\n{Up}<br>\n{Down}<br>\n{Left}<br>\n{Right}<br>\n{PgUp}</b> lub <b>{PageUp}<br>\n{PgDown}</b> lub <b>{PageDown}<br>\n{Home}<br>\n{End}<br>\n{Ins}</b> lub <b>{Insert}<br>\n{Del}</b> lub <b>{Delete}<br>\n{Pause}<br>{Capslock}<br>\n{Numlock}<br>\n{Scrolllock}<br>\n{F1}, {F2}, ... , {F24}<br>\n{Apps}</b> (To jest klucz menu kontekstowego)<b><br>\n<br>\n</b>Te słowa emulują klawisze na klawiaturze numerycznej:<b><br>\n{Divide}<br>\n{Multiply}<br>\n{Subtract}<br>\n{Add}<br>\n{Decimal}<br>\n{Numpad0}, {Numpad1}, ... , {Numpad9}</b>\n'
            insertButton = u"&Wstaw"
            specialKeyTool = u"Narzędzie klawiszy specjalnych"
            textToType = u"Tekst do wpisania:"
            useAlternativeMethod = u"Użyj alternatywnej metody do emulowania naciśnięć klawiszy"
            class Keys:
                backspace = u"Backspace"
                context = u"Klawisz menu kontekstowego"
                delete = u"Delete"
                down = u"Strzałka w dół"
                end = u"End"
                enter = u"Enter"
                escape = u"Esc"
                home = u"Home"
                insert = u"Insert"
                left = u"Strzałka w lewo"
                num0 = u"KN 0"
                num1 = u"KN 1"
                num2 = u"KN 2"
                num3 = u"KN 3"
                num4 = u"KN 4"
                num5 = u"KN 5"
                num6 = u"KN 6"
                num7 = u"KN 7"
                num8 = u"KN 8"
                num9 = u"KN 9"
                numAdd = u"KN Plus (+)"
                numDecimal = u"KN dziesiętny (,)"
                numDivide = u"KN Podziel (/)"
                numMultiply = u"KN Pomnóż (*)"
                numSubtract = u"KN Odejmij (-)"
                pageDown = u"Page Down"
                pageUp = u"Page Up"
                returnKey = u"Return"
                right = u"Strzałka w prawo"
                space = u"Spacja"
                tabulator = u"Tab"
                up = u"Strzałka w górę"
                win = u"Logo Windows"
        class SendMessage:
            name = u"Wyślij wiadomość"
        class SetAlwaysOnTop:
            name = u"Ustaw zawsze na wierzchu"
            description = u"Ustaw zawsze na wierzchu"
            radioBox = u"Wybierz akcje:"
    class Mouse:
        name = u"Mysz"
        description = u"Daje Ci możliwość kontroli wkaźnika myszy i emulowania zdarzeń myszy."
        class GoDirection:
            name = u"Ruch myszy w kierunku"
            description = u"Ruch myszy w kierunku"
            label = u"Ruch myszy w kierunku %.2f°"
            text1 = u"Zacznij poruszaj wskaźnikiem myszy w kierunku"
            text2 = u"stopni. (0-360)"
        class LeftButton:
            name = u"Lewy klawisz myszy"
            description = u"Lewy klawisz myszy"
        class LeftDoubleClick:
            name = u"Podwójne kliknięcie lewego klawisza myszy"
            description = u"Podwójne kliknięcie lewego klawisza myszy"
        class MiddleButton:
            name = u"Środkowy klawisz myszy"
            description = u"Środkowy klawisz myszy"
        class MouseWheel:
            name = u"Obrót rolką myszy"
            description = u"Obrót rolką myszy"
            label = u"Obrót rolką myszy %d kliknięć"
            text1 = u"Obrót rolką myszy o"
            text2 = u"kliknięć. (Minusowe wartości skutkują obrotem w dół)"
        class MoveAbsolute:
            name = u"Przenieś wskaźnik"
            description = u"Przenieś wskaźnik do punktu"
            label = u"Ustaw wskaźnik myszy na pozycji x:%s, y:%s"
            text1 = u"Ustaw pozycję poziomą X na"
            text2 = u"piksel"
            text3 = u"Ustaw pozycję pionową Y na"
            text4 = u"piksel"
        class MoveRelative:
            name = u"Przesuń wskaźnik"
            description = u"Przesuń wskaźnik"
            label = u"Przesuń wskaźnik myszy o x:%s, y:%s"
            text1 = u"Zmień pozycję pionową X o"
            text2 = u"pikseli"
            text3 = u"Zmień pozycję poziomą X o"
            text4 = u"pikseli"
        class RightButton:
            name = u"Prawy klawisz myszy"
            description = u"Prawy klawisz myszy"
        class RightDoubleClick:
            name = u"Podwójne kliknięcie prawego klawisza myszy"
            description = u"Podwójne kliknięcie prawego klawisza myszy"
