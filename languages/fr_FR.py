# -*- coding: UTF-8 -*-
class General:
    apply = u"Appliquer"
    autostartItem = u"Démarrage automatique"
    browse = u"Parcourir..."
    cancel = u"Annuler"
    choose = u"Sélection"
    configTree = u"Arbre de configuration"
    deleteLinkedItems = u"Au moins un élément en dehors de votre sélection se réfère à un élément visible dans votre sélection. Si vous continuez, le référant ne fonctionnera plus correctement.\n\nEtes-vous sûr de vouloir supprimer la sélection?"
    deleteManyQuestion = u"Cet élément possède %s sous-éléments.\nÊtes-vous certain de vouloir tous les supprimer?"
    deletePlugin = u"Ce greffon est utilisé dans votre configuration.\nVous ne pouvez pas l'enlever tant que des actions l'utilisant sont présentes."
    deleteQuestion = u"Etes vous sûr de vouloir supprimer cet élément?"
    help = u"&Aide"
    no = u"&Non"
    noOptionsAction = u"Cette action n'a pas d'option à configurer."
    noOptionsPlugin = u"Ce plugin n'a pas d'option à configurer."
    ok = u"OK"
    pluginLabel = u"Greffon: %s"
    settingsActionCaption = u"Paramètres d'une Action"
    settingsEventCaption = u"Paramètres d'un Evènement"
    settingsPluginCaption = u"Paramètres d'un Greffon"
    supportLink = u"ici"
    supportSentence = u"Le support pour ce greffon se trouve "
    test = u"&Test"
    unnamedEvent = u"<Évènement sans nom>"
    unnamedFile = u"<Sans nom>"
    unnamedFolder = u"<Dossier sans nom>"
    unnamedMacro = u"<Macro-commande sans nom>"
    yes = u"&Oui"
class MainFrame:
    onlyLogAssigned = u"&Journaliser uniquement les évènements assignés et actifs"
    onlyLogAssignedToolTip = u"Ne pas cocher si vous voulez utiliser de nouveaux évènements. Si coché, le journal affichera uniquement les évènements assignés dans une macro active dans la configuration actuelle."
    class Logger:
        caption = u"Journal"
        welcomeText = u"---> Bienvenue dans EventGhost <---"
    class Menu:
        About = u"À &propos d'EventGhost..."
        AddAction = u"Ajouter une action..."
        AddEvent = u"Ajouter un évènement..."
        AddFolder = u"Ajouter un dossier..."
        AddMacro = u"Ajouter une macro-commande..."
        AddPlugin = u"Ajouter un greffon..."
        Apply = u"&Appliquer les modifications"
        CheckUpdate = u"Recherche de &mise-à-jour..."
        ClearLog = u"Effacer le journal"
        Close = u"&Fermer"
        CollapseAll = u"&Replier l'arbre de configuration"
        ConfigurationMenu = u"&Configuration"
        Configure = u"Propriétés de l'élément..."
        Copy = u"Co&pier"
        Cut = u"Coup&er"
        Delete = u"&Supprimer"
        Disabled = u"Désactivé"
        EditMenu = u"&Edition"
        Execute = u"Exécuter"
        Exit = u"&Quitter"
        ExpandAll = u"&Déplier l'arbre de configuration"
        ExpandOnEvents = u"Déplier automatiquement l'arbre lors d'un évènement"
        Export = u"Exporter..."
        FileMenu = u"&Fichier"
        Find = u"&Chercher..."
        FindNext = u"Chercher &Suivant"
        HelpContents = u"&Contenu de l'aide"
        HelpMenu = u"&Aide"
        HideShowToolbar = u"Barre d'outils"
        Import = u"Importer..."
        IndentLog = u"Indenter le journal"
        LogActions = u"Journal : afficher les actions"
        LogMacros = u"Journal : afficher les macros"
        LogTime = u"Journal : afficher l'heure"
        New = u"&Nouveau"
        Open = u"&Ouvrir..."
        Options = u"&Options..."
        Paste = u"C&oller"
        PythonShell = u"Shell Python (prompt)"
        Redo = u"&Refaire"
        Rename = u"Renommer"
        Reset = u"Réinitialiser"
        Save = u"&Sauver"
        SaveAs = u"S&auver Sous..."
        SelectAll = u"&Tout sélectionner"
        Undo = u"Ann&uler"
        ViewMenu = u"Affichage"
        WebForum = u"&Forum d'entre-aide"
        WebHomepage = u"Pa&ge d'accueil d'EventGhost"
        WebWiki = u"&Wiki"
    class Messages:
        cantAddAction = u"Vous ne pouvez ajouter un élément d'action ici.\n\nVeuillez choisir un élément de type 'Macro' ou un emplacement à l'intérieur d'un élément de type 'Macro'. "
        cantAddEvent = u"Vous ne pouvez ajouter un évènement ici.\n\nVeuillez choisir un élément de type 'Macro' ou un emplacement à l'intérieur d'un élément de type 'Macro'. "
        cantConfigure = u"Vous ne pouvez configurer cet élément.\n\nSeuls les actions, évènements et greffons se configurent."
        cantDisable = u"L'élément racine et le démarrage automatique ne peuvent être désactivés."
        cantExecute = u"L'élément racine et le démarrage automatique ne peuvent être exécutés"
        cantRename = u"Seuls les dossiers, macros et actions peuvent être renommés."
    class SaveChanges:
        dontSaveButton = u"Ne pas sauvegarder"
        mesg = u"Ce fichier à été modifié.\n\nVoulez-vous sauvegarder les changements effectués ?\n"
        saveButton = u"&Sauvegarder"
    class TaskBarMenu:
        Exit = u"Sortie"
        Hide = u"Masquer EventGhost"
        Show = u"Afficher EventGhost"
    class Tree:
        caption = u"Configuration"
class Error:
    FileNotFound = u'Le fichier "%s" n\'a pu être trouvé.'
    InAction = u'Erreur lors de l\'Action suivante: "%s"'
    configureError = u"Erreur lors de la configuration: %s"
    pluginLoadError = u"Erreur lors du chargement du greffon %s"
    pluginNotActivated = u'Le greffon "%s" n\'est pas actif'
    pluginStartError = u"Erreur lors du démarrage du greffon: %s"
class Exceptions:
    DeviceInitFailed = u"Impossible d'initialiser le matériel"
    DeviceNotFound = u"Le matériel n'a pas été trouvé!"
    DeviceNotReady = u"Le matériel n'est pas prêt!"
    DriverNotFound = u"Le pilote n'a pas été trouvé!"
    DriverNotOpen = u"Impossible d'ouvrir le pilote!"
    InitFailed = u"L'initialisation a échoué!"
    PluginLoadError = u"Erreur lors du chargement du greffon!"
    PluginNotFound = u"Le greffon n'a pas été trouvé!"
    ProgramNotFound = u"L'application n'a pas été trouvée"
    ProgramNotRunning = u"L'application n'est pas lancée"
    SerialOpenFailed = u"Impossible d'ouvrir le port série!"
class CheckUpdate:
    ManErrorMesg = u"Impossible de récuperer les informations depuis le site d'EventGhost.\n\nVeuillez réessayer plus tard."
    ManOkMesg = u"Cette version d'EventGhost est la plus récente."
    downloadButton = u"Visiter la page de téléchargement."
    newVersionMesg = u"Une nouvelle version d'EventGhost vient de sortir.\n\n	Votre version:	%s\n	Dernière version:	%s\n\nVoulez-vous accéder à la page de téléchargement?"
    waitMesg = u"Veuillez patienter le temps qu'EventGhost récupère les informations de mise-à-jour."
class AddActionDialog:
    descriptionLabel = u"Description"
    title = u"Sélectionner une action à ajouter..."
class AddPluginDialog:
    author = u"Auteur:"
    descriptionBox = u"Description:"
    externalPlugins = u"Equipement externe"
    noInfo = u"Pas d'informations disponible."
    noMultiload = u"Ce greffon ne supporte pas le multichargement et il en existe déjà une instance dans votre configuration."
    noMultiloadTitle = u"Pas de multichargement possible"
    otherPlugins = u"Autres greffons"
    programPlugins = u"Greffons de prise en charge de programme tiers"
    remotePlugins = u"Greffons de prise en charge de télécommande"
    title = u"Choisissez un greffon à ajouter..."
    version = u"Version:"
class AddActionGroupDialog:
    caption = u"Ajouter des Actions?"
    message = u"EventGhost peut ajouter dans votre configuration actuelle un dossier avec toutes les actions disponibles pour ce greffon . Si vous désirez l'ajouter, sélectionnez l'emplacement où il devrait être créé et appuyez sur 'OK'.\n\nDans le cas contraire appuyez sur le bouton \"Annuler\"."
class EventItem:
    eventItem = u"Evènement"
    eventName = u"Nom de l'évènement:"
    notice = u"Remarque : Vous pouvez également glisser/déposer les évènements depuis le journal vers une macro."
class OptionsDialog:
    CheckUpdate = u"Vérifier l'existence d'une nouvelle version"
    HideOnClose = u"Fermer la fenêtre ne fait pas quitter l'application"
    HideOnStartup = u"Masquer au démarrage"
    LanguageGroup = u"Langues"
    StartGroup = u"Démarrage"
    StartWithWindows = u"Lancer au démarrage de Windows"
    Tab1 = u"Général"
    Title = u"Options"
    UseAutoloadFile = u"Chargement automatique du fichier "
    UseFixedFont = u"Utiliser une police à taille fixe dans le journal."
    confirmDelete = u"Demander une confirmation lors de la suppression d'éléments."
    confirmRestart = u"Le changement de langage ne prend effet qu'après un redémarrage de l'application. Voulez-vous redémarrer maintenant?"
    limitMemory1 = u"Quand minimisé, limiter la consommation mémoire à"
    limitMemory2 = u"Mo"
class FindDialog:
    caseSensitive = u"&Sensible à la casse"
    direction = u"Direction"
    down = u"Bas"
    findButton = u"&Chercher le suivant"
    notFoundMesg = u'"%s" n\'a pas été trouvé'
    searchLabel = u"&Chercher:"
    searchParameters = u"Chercher également dans les paramètres d'action"
    title = u"Chercher"
    up = u"&Haut"
    wholeWordsOnly = u"Mot &entier uniquement"
class AboutDialog:
    Author = u"Auteur: %s"
    CreationDate = u"%a, %d %b %Y %H:%M:%S"
    Title = u"À propos d'EventGhost"
    Version = u"Version: %s (build %s)"
    tabAbout = u"A propos"
    tabChangelog = u"Historique (changelog)"
    tabLicense = u"Accords de license"
    tabSpecialThanks = u"Remerciements particuliers"
    tabSystemInfo = u"Informations sur le système"
class WinUsb:
    dialogCaption = u"Greffon EventGhost: %s"
    downloadFailedMsg = u"Le téléchargement a échoué!\n\nVeuillez réessayer plus tard."
    downloadMsg = u"EventGhost doit télécharger des fichiers supplémentaires avant de pouvoir installer le pilote pour le greffon %s.\n\nVoulez-vous commencer le téléchargement maintenant?"
    installMsg = u"Vous devez installer le pilote approprié pour le matériel %s.\n\nEst-ce que EventGhost doit commencer l'installation du pilote à votre place dès maintenant?"
    restartMsg = u"EventGhost doit redémarrer avant de pouvoir utiliser le nouveau pilote. \n\nVoulez-vous redémarrer EventGhost maintenant?"
class Plugin:
    class EventGhost:
        name = u"EventGhost"
        description = u"Vous trouverez ici les principales actions d'EventGhost."
        class AutoRepeat:
            name = u"Répétition automatique de la macro-commande courante"
            description = u"Transforme la macro-commande à laquelle cette action est ajoutée en une macro-commande qui se répète toute seule."
            seconds = u"secondes"
            text1 = u"Première répétition après"
            text2 = u"avec une répétition toutes les"
            text3 = u"Modifier les repetitions au bout de"
            text4 = u"pour avoir une répétition toutes les"
        class Comment:
            name = u"Commentaire"
            description = u"Utilisez cette commande sans effet pour commenter votre configuration."
        class DisableItem:
            name = u"Désactivation d'un élément"
            description = u"Désactive d'un élément"
            cantSelect = u"L'élément sélectionné ne peut changer son état d'activation.\n\nVeuillez sélectionnez un autre élément."
            label = u"Désactivation: %s"
            text1 = u"Veuillez sélectionner l'élément à désactiver:"
        class EnableExclusive:
            name = u"Activation exclusive d'un dossier/d'une macro-commande"
            description = u"\nActive un dossier ou macro-commande, en désactivant tous les autres\ndossiers/macro-commandes situés au même niveau dans l'arbre de\nconfiguration."
            cantSelect = u"L'élément sélectionné ne peut changer son état d'activation.\n\nVeuillez sélectionnez un autre élément."
            label = u"Activation exclusive: %s"
            text1 = u"Veuillez sélectioner le dossier ou la macro-commande qui doit être activée de manière exclusive:"
        class EnableItem:
            name = u"Activation d'un élément"
            description = u"Active un élément"
            cantSelect = u"L'élément sélectionné ne peut changer son état d'activation.\n\nVeuillez sélectionnez un autre élément."
            label = u"Activation: %s"
            text1 = u"Veuillez sélectionner l'élément à activer:"
        class FlushEvents:
            name = u"Effacer les évènements en attente"
            description = u"<rst>\n        \"Effacer les évènements en attente\" efface tous les évènements qui n'ont pas été traités et qui sont dans la file d'attente.\n\nC'est pratique dans le cas où une macro possède des traitements longs, et que des évènements empilés pendant cette attente ne devraient pas être exécutés.\n\n**Exemple:** Vous avez une macro \"Démarrage du projecteur\" qui met environ 90s à s'exécuter. L'utilisateur final ne verra rien jusqu'à ce que le projecteur s'allume, ce qui prend 60s. Il est très probable qu'il appuie sur le bouton de lancement de cette même macro à plusieurs reprises durant cette attente, à tort. Si vous placez un \"Effacer les évènements en attente\" à la fin de la macro, ces inconvénients seront évités."
        class JumpIfDoubleEvent:
            name = u"Sauter si l'évènement est doublé"
            description = u"Saute à une autre macro, si le même évènement qui a déclenché cette macro est à nouveau déclenché dans un délai donné."
            label = u"Si l'évènement est déclenché deux fois, aller à: %s"
            text1 = u"Si l'élément est déclenché deux fois en"
            text2 = u"secondes,"
            text3 = u"aller à:"
            text4 = u"Sélectionnez la macro qui devrait être exécutée si l'évènement est déclenché deux fois..."
            text5 = u"Veuillez sélectionner la macro qui devrait être exécutée si l'évènement est déclenché deux fois."
        class JumpIfLongPress:
            name = u"Sauter si pression longue"
            description = u"Saute à une autre macro si le bouton de la télécommande est maintenu appuyé plus longtemps que ce qui est prévu."
            label = u"Si le bouton est appuyé %s secondes, aller à: %s"
            text1 = u"Si le bouton est appuyé plus longtemps que"
            text2 = u"secondes, "
            text3 = u"aller à:"
            text4 = u"Sélectionner la macro de pression longue..."
            text5 = u"Veuillez sélectionner la macro de pression longue..."
        class NewJumpIf:
            name = u"Saut"
            description = u"Effectue un saut vers une autre macro-commande,\nsi la condition spécifiée est remplie."
            choices = [
                u"la dernière action a réussi",
                u"la dernière action a échoué",
                u"Tout le temps",
            ]
            labels = [
                u'En cas de succès, saute vers "%s"',
                u'En cas d\'échec, saute vers "%s"',
                u'Saute vers "%s"',
                u'En cas de succès, saute vers "%s" et revient',
                u'En cas d\'échec, saute vers "%s" et revient',
                u'Saute vers "%s" et revient',
            ]
            mesg1 = u"Sélectionnez une macro-commande..."
            mesg2 = u"Veuillez sélectionner la macro-commande à exécuter si la condition est remplie:"
            text1 = u"Si:"
            text2 = u"Saut vers:"
            text3 = u"et retour ici à la fin du saut"
        class PythonCommand:
            name = u"Commande Python"
            description = u'Exécute l\'argument comme une commande python unique.<p> <i>Exemple :</i><br><br>print "Bonjour"<br><br><i>ou encore</i><br><br> iMaVariable = 3'
            parameterDescription = u"Commande Python:"
        class PythonScript:
            name = u"Script Python"
            description = u"Véritable script Python."
        class ShowOSD:
            name = u"Afficher un message à l'écran"
            description = u"Affiche un message à l'écran."
            alignment = u"Alignement:"
            alignmentChoices = [
                u"Haut gauche",
                u"Haut droit",
                u"Bas gauche",
                u"Bas droit",
                u"Centre de l'écran",
                u"Bas centre",
                u"Haut centre",
                u"Gauche centre",
                u"Droit centre",
            ]
            display = u"Afficher à l'écran:"
            editText = u"Texte à afficher:"
            label = u"Afficher un message à l'écran: %s"
            osdColour = u"Couleur du texte:"
            osdFont = u"Police:"
            outlineFont = u"Surligner le message"
            skin = u"Aspect visuel amélioré"
            wait1 = u"Masquer le message après"
            wait2 = u"secondes (0 = jamais)"
            xOffset = u"Décalage horizontal X:"
            yOffset = u"Décalage vertical Y:"
        class StopProcessing:
            name = u"Stoppe l'exécution de cet évènement."
            description = u"Stoppe l'exécution de cet évènement."
        class TriggerEvent:
            name = u"Déclencher l'évènement"
            description = u"Déclenche un évènement (éventuellement après un délai)."
            labelWithTime = u'Déclenche un évènement "%s" après %.2f secondes'
            labelWithoutTime = u'Déclenche un évènement "%s"'
            text1 = u"Evènement à déclencher:"
            text2 = u"Retarder le déclenchement de l'évènement:"
            text3 = u"secondes. (0 = immédiat)"
        class Wait:
            name = u"Temporisation"
            description = u"Attend un nombre prédéfini de secondes"
            label = u"Attente: %s secondes"
            seconds = u"secondes"
            wait = u"Attente"
    class System:
        name = u"Système"
        description = u"Contrôle différents aspect de votre système, tel que la carte son, la carte graphique, l'alimentation, etc."
        forced = u"Forcé: %s"
        forcedCB = u"Force la fermeture de tous les programmes"
        class ChangeDisplaySettings:
            name = u"Modifier les paramètres d'affichage"
            display = u"Ecran:"
            storeInRegistry = u"Enregistrer dans la base de registre"
        class ChangeMasterVolumeBy:
            name = u"Modifier le volume principal"
            text1 = u"Modifier le volume de "
            text2 = u"pourcent."
        class Execute:
            name = u"Démarrer une application"
            Parameters = u"Arguments de ligne de commande supplémentaires:"
            WaitCheckbox = u"Attendre que l'application soit fermée avant de continuer"
            WorkingDir = u"Dossier :"
            browseExecutableDialogTitle = u"Choisir l'exécutable"
            browseWorkingDirDialogTitle = u"Choisir le dossier"
            eventCheckbox = u"Déclencher un évènement lorsque l'application est fermée"
            eventSuffix = u"Application.Fermée"
            label = u"Démarrer l'application: %s"
        class GetMute:
            name = u"Muet :Obtenir le statut"
        class Hibernate:
            name = u"Veille prolongée"
        class LockWorkstation:
            name = u"Verrouiller le poste"
        class LogOff:
            name = u"Fermer la session"
        class MonitorGroup:
            name = u"Affichage"
        class MonitorPowerOff:
            name = u"Eteindre le moniteur"
        class MonitorPowerOn:
            name = u"Allumer le moniteur"
        class MonitorStandby:
            name = u"Mettre le moniteur en veille"
        class MuteOff:
            name = u"Muet (désactivé)"
        class MuteOn:
            name = u"Muet (actif)"
        class OpenDriveTray:
            name = u"Ouvrir/Fermer le lecteur"
        class PlaySound:
            name = u"Jouer un son"
            eventSuffix = u"Joué"
            text1 = u"Chemin vers le fichier de son:"
            text2 = u"Attendre que la lecture soit terminée"
            text3 = u"Déclencher un évènement une fois terminé:"
        class PowerDown:
            name = u"Eteindre l'ordinateur"
        class PowerGroup:
            name = u"Gestion de l'alimentation"
        class Reboot:
            name = u"Redémarrer l'ordinateur"
        class RegistryChange:
            name = u"Modifier une valeur de la base de registre"
        class RegistryGroup:
            name = u"Base de Registre"
        class RegistryQuery:
            name = u"Consulter la base de registre"
        class ResetIdleTimer:
            name = u"Réinitialiser le compteur d'inactivité"
        class SetClipboard:
            name = u"Copier un texte dans le presse papier"
        class SetDisplayPreset:
            name = u"Définir un préréglage d'affichage"
        class SetMasterVolume:
            name = u"Définir le volume principal"
        class SetSystemIdleTimer:
            name = u"Définir le délai avant la veille du système"
        class SetWallpaper:
            name = u"Changer le papier peint"
        class ShowPicture:
            name = u"Afficher une image"
        class SoundGroup:
            name = u"Carte son"
        class Standby:
            name = u"Veille"
        class StartScreenSaver:
            name = u"Economiseur d'écran"
        class ToggleMute:
            name = u"Mute (basculer)"
            description = u"Si Mute est activé, alors le désactive. Sinon, active."
    class Window:
        name = u"Fenêtre Windows"
        description = u"Actions relative au contrôle de la fenêtre d'une application."
        class BringToFront:
            name = u"Amener au premier plan"
        class Close:
            name = u"Fermer"
        class FindWindow:
            name = u"Trouver une fenêtre"
            description = u"Recherche une fenêtre, qui est utilisée par la suite par les autres actions de la macro en cours.\n\n<p> Si une macro n'a pas d'action \"Rechercher une fenêtre\", toutes les actions vont utiliser l'application au premier plan. <p> Dans les zones de saisie vous pouvez utiliser les jokers {*} pour une chaîne de caractère et {?} pour un seul caractère."
            drag1 = u"Glissez moi sur une fenêtre"
            drag2 = u"Maintenant déplacez moi sur une fenêtre"
            hide_box = u"Masquer EventGhost pendant le glisser/déposer"
            invisible_box = u"Recherche également les éléments invisibles"
            label = u"Trouver la fenêtre: %s"
            label2 = u"Trouver la fenêtre au premier plan"
            matchNum1 = u"Retourner seulement le"
            matchNum2 = u"ième résultat"
            onlyFrontmost = u"Retourner seulement la fenêtre la plus avancée"
            options = (
                u"Programme",
                u"Nom de la fenêtre:",
                u"Classe de la fenêtre:",
                u"Nom de l'enfant:",
                u"Classe de l'enfant:",
            )
            refresh_btn = u"&Rafraîchir"
            stopMacro = [
                u"Arrêter la macro si la cible n'est pas trouvée",
                u"Arrêter la macro si la cible est trouvée",
                u"Ne jamais arrêter la macro",
            ]
            testButton = u"Test"
            wait1 = u"Attendre"
            wait2 = u"secondes que la fenêtre apparaisse."
        class GrabText:
            name = u"Récupérer le texte"
        class Maximize:
            name = u"Maximiser"
        class Minimize:
            name = u"Minimiser"
        class MoveTo:
            name = u"Déplacement asbolu"
        class Resize:
            name = u"Redimensionner"
        class Restore:
            name = u"Restaurer"
        class SendKeys:
            name = u"Simuler une touche de clavier"
            insertButton = u"&Insérer"
            specialKeyTool = u"Touches spéciales"
            textToType = u"Texte à frapper:"
            useAlternativeMethod = u"Utiliser une méthode alternative pour émuler l'appui des touches"
        class SendMessage:
            name = u"Send Message"
            description = u"\nUtilise la fonction SendMessage de la Windows-API pour envoyer à une fenêtre\nun message. Vous pouvez également utilisez PostMessage si vous le désirez.<p>\nPour les experts seulements."
            text1 = u"Utilisez PostMessage en lieu et place de SendMessage"
        class SetAlwaysOnTop:
            name = u'Activer/Désactiver "Toujours au premier plan"'
            description = u'Définit la propriété "Toujours au premier plan"'
            radioBox = u"Choisir l'action:"
    class Mouse:
        name = u"Souris"
    class Webserver:
        name = u"Webserver (Serveur Web)"
        description = u"Met en place un petit serveur Web, qui peut être utilisé pour générer des évènements via des pages HTML."
    class X10:
        allButton = u"&Tous"
        idBox = u"Sélectionnez un ID"
        noneButton = u"Aucu&n"
        remoteBox = u"Sélectionnez un type de télécommande"
        usePrefix = u"Utiliser le préfixe"
