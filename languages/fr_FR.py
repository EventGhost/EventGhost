# -*- coding: UTF-8 -*-
class General:
    autostartItem = u'D\xe9marrage automatique'
    browse = u'Parcourir...'
    cancel = u'Annuler'
    choose = u'S\xe9lection'
    configTree = u'Arbre de configuration'
    deleteManyQuestion = u'Cet \xe9l\xe9ment poss\xe8de %s sous-\xe9l\xe9ments.\n\xcates-vous certain de vouloir tous les supprimer?'
    deletePlugin = u"Ce greffon est utilis\xe9 dans votre configuration.\nVous ne pouvez pas l'enlever tant que des actions l'utlisant sont pr\xe9sentes."
    help = u'&Aide'
    ok = u'OK'
    pluginLabel = u'Greffon: %s'
    unnamedEvent = u'<\xc9v\xe8nement sans nom>'
    unnamedFile = u'<Sans nom>'
    unnamedFolder = u'<Dossier sans nom>'
    unnamedMacro = u'<Macro-commande sans nom>'
class MainFrame:
    class Logger:
        descriptionHeader = u'Description'
        timeHeader = u'Heure'
        welcomeText = u'---> Bienvenu dans EventGhost <---'
    class Menu:
        About = u"\xc0 &propos d'EventGhost..."
        AddPlugin = u'Ajouter un greffon...'
        CheckUpdate = u'Recherche de &mise-\xe0-jour...'
        Close = u'&Fermer'
        CollapseAll = u"&Replier l'arbre de configuration"
        Copy = u'Co&pier'
        Cut = u'Coup&er'
        Delete = u'&Supprimer'
        Disabled = u'D\xe9sactiv\xe9'
        Edit = u"Propri\xe9t\xe9s de l'\xe9lement..."
        EditMenu = u'&Edition'
        Execute = u'Ex\xe9cuter'
        Exit = u'&Quitter'
        ExpandAll = u"&D\xe9plier l'arbre de configuration"
        ExpandOnEvents = u"D\xe9plier automatiquement l'arbre lors d'un \xe9v\xe8nement"
        ExpandTillMacro = u'Limiter le d\xe9pliment automatique au niveau macro-commande'
        Export = u'Exporter...'
        FileMenu = u'&Fichier'
        HelpMenu = u'&Aide'
        HideShowToolbar = u"Barre d'outils"
        Import = u'Importer...'
        LogActions = u'Rapport sur les actions'
        LogTime = u"Inclure l'heure dans le rapport"
        New = u'&Nouveau'
        NewAction = u'Ajouter une action...'
        NewEvent = u'Ajouter un \xe9v\xe8nement...'
        NewFolder = u'Ajouter un dossier...'
        NewMacro = u'Ajouter une macro-commande...'
        Open = u'&Ouvrir...'
        Options = u'&Options...'
        Paste = u'C&oller'
        Redo = u'&Refaire'
        Rename = u'Renommer'
        Save = u'&Sauver'
        SaveAs = u'S&auver Sous...'
        SelectAll = u'&Tout s\xe9lectionner'
        Undo = u'Ann&uler'
        ViewMenu = u'Affichage'
        WebForum = u"&Forum d'entre-aide"
        WebHomepage = u"Pa&ge d'accueil d'EventGhost"
        WebWiki = u'&Wiki'
    class SaveChanges:
        mesg = u'Ce fichier \xe0 \xe9t\xe9 modifi\xe9.\n\nVoulez-vous sauvegarder les changements effectu\xe9s ?\n'
        title = u'Sauver les changements ?'
    class TaskBarMenu:
        Exit = u'Sortie'
        Hide = u'Masquer EventGhost'
        Show = u'Afficher EventGhost'
class Error:
    FileNotFound = u'Le fichier "%s" n\'a pu \xeatre trouv\xe9.'
    InAction = u'Erreur lors de l\'Action suivante: "%s"'
    InScript = u'Erreur dans le script: "%s"'
class CheckUpdate:
    ManErrorMesg = u"Impossible de r\xe9cuperer les informations depuis le site d'EventGhost.\n\nVeuillez r\xe9essayer plus tard."
    ManErrorTitle = u'Erreur lors de la mise-\xe0-jour'
    ManOkMesg = u"Cette version d'EventGhost est la derni\xe8re."
    ManOkTitle = u'Pas de nouvelle version disponible.'
    downloadButton = u'Visiter la page de t\xe9l\xe9chargement.'
    newVersionMesg = u"Une nouvelle version d'EventGhost vient de sortir.\n\n\tVotre version:\t%s\n\tDerni\xe8re version:\t%s\n\nVoulez-vous acc\xe9der \xe0 la page de t\xe9l\xe9chargement?"
    title = u"Nouvelle version d'EventGhost disponible..."
    waitMesg = u"Veuillez patienter le temps qu'EventGhost r\xe9cup\xe8re les informations de mise-\xe0-jour."
class AddActionDialog:
    descriptionLabel = u'Description'
    title = u'S\xe9lectionner une action \xe0 ajouter...'
class AddPluginDialog:
    author = u'Auteur:'
    descriptionBox = u'Description:'
    noInfo = u"Pas d'informations disponible."
    noMultiload = u'Ce greffon ne supporte pas le multichargement et il en existe d\xe9j\xe0 une instance dans votre configuration.'
    noMultiloadTitle = u'Pas de multichargement possible'
    otherPlugins = u'Autres greffons'
    programPlugins = u'Greffons de prise en charge de programme tiers'
    remotePlugins = u'Greffons de prise en charge de t\xe9l\xe9commande'
    title = u'Choisissez un greffon \xe0 ajouter...'
    version = u'Version:'
class OptionsDialog:
    CheckUpdate = u"V\xe9rifier l'existence d'une nouvelle version"
    HideOnClose = u"Fermer la fen\xeatre ne fait pas quitter l'application"
    HideOnStartup = u'Masquer au d\xe9marrage'
    LanguageGroup = u'Langues'
    StartGroup = u'D\xe9marrage'
    StartWithWindows = u'Lancer au d\xe9marrage de Windows'
    Tab1 = u'G\xe9n\xe9ral'
    Title = u'Options'
    UseAutoloadFile = u'Chargement automatique du fichier '
    Warning = u"Les changements de langues ne prendront effets qu'au red\xe9marrage de l'application."
class AboutDialog:
    Author = u'Auteur: %s'
    CreationDate = u'%a, %d %b %Y %H:%M:%S'
    Title = u"\xc0 propos d'EventGhost"
    Version = u'Version: %s (build %s)'
class Plugin:
    class EventGhost:
        description = u"Vous trouverez ici les principales actions d'EventGhost."
        class AutoRepeat:
            name = u'R\xe9p\xe9tition automatique de la macro-commande courante'
            description = u'Transforme la macro-commande \xe0 laquelle cette action est ajout\xe9 en une macro-commande qui se r\xe9p\xe8te toute seule.'
            seconds = u'secondes'
            text1 = u'Premi\xe8re r\xe9p\xe9tition apr\xe8s'
            text2 = u'avec une r\xe9p\xe9tition toutes les'
            text3 = u'Increase repetition the next'
            text4 = u'to one repetition every'
        class Comment:
            name = u'Commentaire'
            description = u'Utilisez cette commande sans effet pour commenter votre configuration.'
        class DisableItem:
            name = u"D\xe9sactivation d'un \xe9l\xe9ment"
            description = u"D\xe9sactive d'un \xe9l\xe9ment"
            label = u'D\xe9sactivation: %s'
            text1 = u"Veuillez s\xe9lectionner l'\xe9l\xe9ment \xe0 d\xe9sactiver:"
        class EnableExclusive:
            name = u"Activation exclusive d'un dossier/d'une macro-commande"
            description = u"\nActive un dossier ou macro-commande, en d\xe9sactivant tous les autres\ndossiers/macro-commandes situ\xe9s au m\xeame niveau dans l'arbre de\nconfiguration."
            label = u'Activation exclusive: %s'
            text1 = u'Veuillez s\xe9lectioner le dossier ou la macro-commande qui doit \xeatre activ\xe9e de mani\xe8re exclusive:'
        class EnableItem:
            name = u"Activation d'un \xe9l\xe9ment"
            description = u'Active un \xe9l\xe9ment'
            label = u'Activation: %s'
            text1 = u"Veuillez s\xe9lectionner l'\xe9l\xe9ment \xe0 activer:"
        class Jump:
            name = u'Saut'
            description = u'Effectue un saut inconditionnel vers une autre macro-commande et retourne \xe9ventuellement ici.'
            label1 = u'Saut vers %s'
            label2 = u'Saut vers %s avec retour'
            mesg1 = u'S\xe9lectionnez une macro-commande...'
            mesg2 = u'Veuillez s\xe9lectionner la macro-commande \xe0 ex\xe9cuter:'
            text2 = u'SAute vers:'
            text3 = u'Retour ici \xe0 la fin du saut'
        class JumpIf:
            name = u'Saut conditionnel'
            description = u'Effectue un saut vers une autre macro-commande, si une expression python retourne la valeur vraie.'
            label1 = u'Si %s aller vers %s'
            label2 = u'Si %s aller vers %s'
            mesg1 = u'S\xe9lectionnez une macro-commande...'
            mesg2 = u"Veuillez s\xe9lectionner la macro-commande \xe0 ex\xe9cuter\nsi l'expression python est vraie:"
            text1 = u'Si:'
            text2 = u'Aller vers:'
            text3 = u'Retour ici \xe0 la fin du saut'
        class NewJumpIf:
            name = u'Saut'
            description = u'Effectue un saut vers une autre macro-commande,\nsi la condition sp\xe9cifi\xe9e est remplie.'
            choices = [
                u'la derni\xe8re action a r\xe9ussi',
                u'la derni\xe8re action a \xe9chou\xe9e',
                u'Tout le temps',
            ]
            labels = [
                u'En cas de succes, saute vers "%s"',
                u'En cas d\'\xe9chec, saute vers "%s"',
                u'Saute vers "%s"',
                u'En cas de succes, saute vers "%s" et reviens',
                u'En cas d\'\xe9chec, saute vers "%s" et reviens',
                u'Saute vers "%s" et reviens',
            ]
            mesg1 = u'S\xe9lectionnez une macro-commande...'
            mesg2 = u'Veuillez s\xe9lectionner la macro-commande \xe0 ex\xe9cuter si la condition est remplie:'
            text1 = u'Si:'
            text2 = u'Saut vers:'
            text3 = u'et retour ici \xe0 la fin du saut'
        class PythonCommand:
            name = u'Commande Python'
            description = u'Ex\xe9cute l\'argument comme une commande python unique.<p> <i>Exemple :</i><br><br>print "Bonjour"<br><br><i>ou encore</i><br><br> iMaVariable = 3'
            parameterDescription = u'Commande Python:'
        class PythonScript:
            name = u'Script Python'
            description = u'V\xe9ritable script Python.'
        class StopProcessing:
            name = u"Stoppe l'ex\xe9cution de cet \xe9v\xe8nement."
            description = u"Stoppe l'ex\xe9cution de cet \xe9v\xe8nement."
        class Wait:
            name = u'Temporisation'
            description = u'Attend un nombre pr\xe9d\xe9fini de seconde'
            label = u'Attente: %s secondes'
            seconds = u'secondes'
            wait = u'Attent'
    class System:
        name = u'Syst\xe8me'
    class Window:
        class SendMessage:
            name = u'Send Message'
            description = u'\nUtilise la fonction SendMessage de la Windows-API pour envoyer \xe0 une fen\xeatre\nun message. Vous pouvez \xe9galement utilisez PostMessage si vous le d\xe9sirez.<p>\nPour les experts seulements.'
            text1 = u'Utilisz PostMessage en lieu et place de SendMessage'
    class Mouse:
        name = u'Souris'
    class X10:
        allButton = u'&Tous'
        idBox = u'S\xe9lectionnez un ID'
        noneButton = u'Aucu&n'
        remoteBox = u'S\xe9lectionnez un type de t\xe9l\xe9commande'
        usePrefix = u'Utiliser le pr\xe9fixe'
