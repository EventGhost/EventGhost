# -*- coding: UTF-8 -*-
class General:
    autostartItem = u"Démarrage automatique"
    browse = u"Parcourir..."
    cancel = u"Annuler"
    choose = u"Sélection"
    configTree = u"Arbre de configuration"
    deleteManyQuestion = u"Cet élément possède %s sous-éléments.\nÊtes-vous certain de vouloir tous les supprimer?"
    deletePlugin = u"Ce greffon est utilisé dans votre configuration.\nVous ne pouvez pas l'enlever tant que des actions l'utlisant sont présentes."
    help = u"&Aide"
    ok = u"OK"
    pluginLabel = u"Greffon: %s"
    unnamedEvent = u"<Évènement sans nom>"
    unnamedFile = u"<Sans nom>"
    unnamedFolder = u"<Dossier sans nom>"
    unnamedMacro = u"<Macro-commande sans nom>"
class MainFrame:
    class Logger:
        descriptionHeader = u"Description"
        timeHeader = u"Heure"
        welcomeText = u"---> Bienvenu dans EventGhost <---"
    class Menu:
        About = u"À &propos d'EventGhost..."
        AddPlugin = u"Ajouter un greffon..."
        CheckUpdate = u"Recherche de &mise-à-jour..."
        Close = u"&Fermer"
        CollapseAll = u"&Replier l'arbre de configuration"
        Copy = u"Co&pier"
        Cut = u"Coup&er"
        Delete = u"&Supprimer"
        Disabled = u"Désactivé"
        Configure = u"Propriétés de l'élement..."
        EditMenu = u"&Edition"
        Execute = u"Exécuter"
        Exit = u"&Quitter"
        ExpandAll = u"&Déplier l'arbre de configuration"
        ExpandOnEvents = u"Déplier automatiquement l'arbre lors d'un évènement"
        ExpandTillMacro = u"Limiter le dépliment automatique au niveau macro-commande"
        Export = u"Exporter..."
        FileMenu = u"&Fichier"
        HelpMenu = u"&Aide"
        HideShowToolbar = u"Barre d'outils"
        Import = u"Importer..."
        LogActions = u"Rapport sur les actions"
        LogTime = u"Inclure l'heure dans le rapport"
        New = u"&Nouveau"
        AddAction = u"Ajouter une action..."
        AddEvent = u"Ajouter un évènement..."
        AddFolder = u"Ajouter un dossier..."
        AddMacro = u"Ajouter une macro-commande..."
        Open = u"&Ouvrir..."
        Options = u"&Options..."
        Paste = u"C&oller"
        Redo = u"&Refaire"
        Rename = u"Renommer"
        Save = u"&Sauver"
        SaveAs = u"S&auver Sous..."
        SelectAll = u"&Tout sélectionner"
        Undo = u"Ann&uler"
        ViewMenu = u"Affichage"
        WebForum = u"&Forum d'entre-aide"
        WebHomepage = u"Pa&ge d'accueil d'EventGhost"
        WebWiki = u"&Wiki"
    class SaveChanges:
        mesg = u"Ce fichier à été modifié.\n\nVoulez-vous sauvegarder les changements effectués ?\n"
        title = u"Sauver les changements ?"
    class TaskBarMenu:
        Exit = u"Sortie"
        Hide = u"Masquer EventGhost"
        Show = u"Afficher EventGhost"
class Error:
    FileNotFound = u'Le fichier "%s" n\'a pu être trouvé.'
    InAction = u'Erreur lors de l\'Action suivante: "%s"'
class CheckUpdate:
    ManErrorMesg = u"Impossible de récuperer les informations depuis le site d'EventGhost.\n\nVeuillez réessayer plus tard."
    ManErrorTitle = u"Erreur lors de la mise-à-jour"
    ManOkMesg = u"Cette version d'EventGhost est la dernière."
    ManOkTitle = u"Pas de nouvelle version disponible."
    downloadButton = u"Visiter la page de téléchargement."
    newVersionMesg = u"Une nouvelle version d'EventGhost vient de sortir.\n\n	Votre version:	%s\n	Dernière version:	%s\n\nVoulez-vous accéder à la page de téléchargement?"
    title = u"Nouvelle version d'EventGhost disponible..."
    waitMesg = u"Veuillez patienter le temps qu'EventGhost récupère les informations de mise-à-jour."
class AddActionDialog:
    descriptionLabel = u"Description"
    title = u"Sélectionner une action à ajouter..."
class AddPluginDialog:
    author = u"Auteur:"
    descriptionBox = u"Description:"
    noInfo = u"Pas d'informations disponible."
    noMultiload = u"Ce greffon ne supporte pas le multichargement et il en existe déjà une instance dans votre configuration."
    noMultiloadTitle = u"Pas de multichargement possible"
    otherPlugins = u"Autres greffons"
    programPlugins = u"Greffons de prise en charge de programme tiers"
    remotePlugins = u"Greffons de prise en charge de télécommande"
    title = u"Choisissez un greffon à ajouter..."
    version = u"Version:"
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
    Warning = u"Les changements de langues ne prendront effets qu'au redémarrage de l'application."
class AboutDialog:
    Author = u"Auteur: %s"
    CreationDate = u"%a, %d %b %Y %H:%M:%S"
    Title = u"À propos d'EventGhost"
    Version = u"Version: %s (build %s)"
class Plugin:
    class EventGhost:
        description = u"Vous trouverez ici les principales actions d'EventGhost."
        class AutoRepeat:
            name = u"Répétition automatique de la macro-commande courante"
            description = u"Transforme la macro-commande à laquelle cette action est ajouté en une macro-commande qui se répète toute seule."
            seconds = u"secondes"
            text1 = u"Première répétition après"
            text2 = u"avec une répétition toutes les"
            text3 = u"Increase repetition the next"
            text4 = u"to one repetition every"
        class Comment:
            name = u"Commentaire"
            description = u"Utilisez cette commande sans effet pour commenter votre configuration."
        class DisableItem:
            name = u"Désactivation d'un élément"
            description = u"Désactive d'un élément"
            label = u"Désactivation: %s"
            text1 = u"Veuillez sélectionner l'élément à désactiver:"
        class EnableExclusive:
            name = u"Activation exclusive d'un dossier/d'une macro-commande"
            description = u"\nActive un dossier ou macro-commande, en désactivant tous les autres\ndossiers/macro-commandes situés au même niveau dans l'arbre de\nconfiguration."
            label = u"Activation exclusive: %s"
            text1 = u"Veuillez sélectioner le dossier ou la macro-commande qui doit être activée de manière exclusive:"
        class EnableItem:
            name = u"Activation d'un élément"
            description = u"Active un élément"
            label = u"Activation: %s"
            text1 = u"Veuillez sélectionner l'élément à activer:"
        class JumpIf:
            name = u"Saut conditionnel"
            description = u"Effectue un saut vers une autre macro-commande, si une expression python retourne la valeur vraie."
            label1 = u"Si %s aller vers %s"
            label2 = u"Si %s aller vers %s"
            mesg1 = u"Sélectionnez une macro-commande..."
            mesg2 = u"Veuillez sélectionner la macro-commande à exécuter\nsi l'expression python est vraie:"
            text1 = u"Si:"
            text2 = u"Aller vers:"
            text3 = u"Retour ici à la fin du saut"
        class NewJumpIf:
            name = u"Saut"
            description = u"Effectue un saut vers une autre macro-commande,\nsi la condition spécifiée est remplie."
            choices = [
                u"la dernière action a réussi",
                u"la dernière action a échouée",
                u"Tout le temps",
            ]
            labels = [
                u'En cas de succes, saute vers "%s"',
                u'En cas d\'échec, saute vers "%s"',
                u'Saute vers "%s"',
                u'En cas de succes, saute vers "%s" et reviens',
                u'En cas d\'échec, saute vers "%s" et reviens',
                u'Saute vers "%s" et reviens',
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
        class StopProcessing:
            name = u"Stoppe l'exécution de cet évènement."
            description = u"Stoppe l'exécution de cet évènement."
        class Wait:
            name = u"Temporisation"
            description = u"Attend un nombre prédéfini de seconde"
            label = u"Attente: %s secondes"
            seconds = u"secondes"
            wait = u"Attent"
    class System:
        name = u"Système"
    class Window:
        class SendMessage:
            name = u"Send Message"
            description = u"\nUtilise la fonction SendMessage de la Windows-API pour envoyer à une fenêtre\nun message. Vous pouvez également utilisez PostMessage si vous le désirez.<p>\nPour les experts seulements."
            text1 = u"Utilisz PostMessage en lieu et place de SendMessage"
    class Mouse:
        name = u"Souris"
    class X10:
        allButton = u"&Tous"
        idBox = u"Sélectionnez un ID"
        noneButton = u"Aucu&n"
        remoteBox = u"Sélectionnez un type de télécommande"
        usePrefix = u"Utiliser le préfixe"
