# -*- coding: latin-1 -*-

class General:
    ok              = "OK"
    cancel          = "Annuler"
    help            = "&Aide"
    unnamedFolder      = "<Dossier sans nom>"
    unnamedMacro       = "<Macro-commande sans nom>"
    unnamedEvent       = "<Évènement sans nom>"
    unnamedFile         = "<Sans nom>"
    configTree      = "Arbre de configuration"
    autostartItem   = "Démarrage automatique"
    browse    = "Parcourir..."
    choose          = "Sélection"
    deleteManyQuestion      = "Cet élément possède %s sous-éléments.\nÊtes-vous certain de vouloir tous les supprimer?"
    deletePlugin    = "Ce greffon est utilisé dans votre configuration.\nVous ne pouvez pas l'enlever tant que des actions l'utlisant sont présentes."
    pluginLabel          = "Greffon: %s"


class MainFrame:
    class Logger:
        descriptionHeader = "Description"
        timeHeader = "Heure"
        welcomeText = "---> Bienvenu dans EventGhost <---"
    
    class Menu:
        FileMenu        = "&Fichier"
        New             = "&Nouveau"
        Open            = "&Ouvrir..."
        Save            = "&Sauver"
        SaveAs          = "S&auver Sous..."
        Export          = "Exporter..."
        Import          = "Importer..."
        Close           = "&Fermer"
        Options         = "&Options..."
        Exit            = "&Quitter"
        
        EditMenu        = "&Edition"
        Undo            = "Ann&uler"
        Redo            = "&Refaire"
        Cut             = "Coup&er"
        Copy            = "Co&pier"
        Paste           = "C&oller"
        Delete          = "&Supprimer"
        ClearAll        = "Tout effacer"
        SelectAll       = "&Tout sélectionner"
        AddPlugin       = "Ajouter un greffon..."
        NewFolder       = "Ajouter un dossier..."
        NewMacro        = "Ajouter une macro-commande..."
        NewEvent        = "Ajouter un évènement..."
        NewAction       = "Ajouter une action..."
        Edit            = "Propriétés de l'élement..."
        Rename          = "Renommer"
        Disabled        = "Désactivé"
        Execute         = "Exécuter"

        ViewMenu        = "Affichage"
        HideShowToolbar = "Barre d'outils"
        CollapseAll     = "&Replier l'arbre de configuration"
        ExpandAll       = "&Déplier l'arbre de configuration"
        ExpandOnEvents  = "Déplier automatiquement l'arbre lors d'un évènement" ##
        ExpandTillMacro = "Limiter le dépliment automatique au niveau macro-commande" ##
        LogActions      = "Rapport sur les actions"
        LogTime         = "Inclure l'heure dans le rapport"
        
        HelpMenu        = "&Aide"
        About           = "À &propos d'EventGhost..."
        WebHomepage     = "Pa&ge d'accueil d'EventGhost"
        WebForum        = "&Forum d'entre-aide"
        WebWiki         = "&Wiki"
        CheckUpdate     = "Recherche de &mise-à-jour..."

    class TaskBarMenu:
        Show            = "Afficher EventGhost"
        Hide            = "Masquer EventGhost"
        Exit            = "Sortie"
        
    class SaveChanges:
        title           = "Sauver les changements ?"
        mesg            = "Ce fichier à été modifié.\n\nVoulez-vous sauvegarder les changements effectués ?\n"

class AboutDialog:
    Title           = "À propos d'EventGhost"
    Author          = "Auteur: %s"
    Version         = "Version: %s (build %s)"
    CreationDate    = "%a, %d %b %Y %H:%M:%S"


class OptionsDialog:
    Title           = "Options"
    Tab1            = "Général"
    StartGroup      = "Démarrage"
    HideOnStartup   = "Masquer au démarrage"
    HideOnClose     = "Fermer la fenêtre ne fait pas quitter l'application"
    UseAutoloadFile = "Chargement automatique du fichier " ###
    LanguageGroup   = "Langues"
    Warning         = "Les changements de langues ne prendront effets qu'au redémarrage de l'application."
    StartWithWindows= "Lancer au démarrage de Windows"
    CheckUpdate     = "Vérifier l'existence d'une nouvelle version"
    
    
class ScriptEditor:
    Title           = "Python-Editor - %s"


class AddPluginDialog:
    title           = "Choisissez un greffon à ajouter..."
    noInfo          = "Pas d'informations disponible."
    noMultiloadTitle= "Pas de multichargement possible"
    noMultiload     = "Ce greffon ne supporte pas le multichargement et il en existe déjà une instance dans votre configuration."
    remotePlugins   = "Greffons de prise en charge de télécommande"
    programPlugins  = "Greffons de prise en charge de programme tiers"
    otherPlugins    = "Autres greffons"
    author          = "Auteur:"
    version         = "Version:"
    descriptionBox  = "Description:"
    
    
class AddActionDialog:
    title           = "Sélectionner une action à ajouter..."
    descriptionLabel = "Description"

class CheckUpdate:
    title = "Nouvelle version d\'EventGhost disponible..."
    newVersionMesg = "Une nouvelle version d\'EventGhost vient de sortir.\n\n\
\tVotre version:\t%s\n\
\tDernière version:\t%s\n\n\
Voulez-vous accéder à la page de téléchargement?"
    downloadButton = "Visiter la page de téléchargement."
    waitMesg = "Veuillez patienter le temps qu'EventGhost récupère les informations de mise-à-jour."
    ManOkTitle = "Pas de nouvelle version disponible."    
    ManOkMesg = "Cette version d'EventGhost est la dernière."    
    ManErrorTitle = "Erreur lors de la mise-à-jour"
    ManErrorMesg = "Impossible de récuperer les informations depuis le site d'EventGhost.\n\nVeuillez réessayer plus tard."


class Error:
    FileNotFound    = 'Le fichier "%s" n\'a pu être trouvé.'
    InAction        = 'Erreur lors de l\'Action suivante: "%s"'
    InScript        = 'Erreur dans le script: "%s"'


class Plugin:
    class EventGhost:
        description = "Vous trouverez ici les principales actions d'EventGhost."
        
        class PythonCommand:
            name = 'Commande Python'
            description = "Exécute l'argument comme une commande python unique.<p> <i>Exemple :</i><br><br>print \"Bonjour\"<br><br><i>ou encore</i><br><br> iMaVariable = 3"
            parameterDescription = 'Commande Python:'
            
        class PythonScript:
            name = 'Script Python'
            description = 'Véritable script Python.'
            
        class Comment:
            name = 'Commentaire'
            description = 'Utilisez cette commande sans effet pour commenter votre configuration.'
            
        class NewJumpIf:
            name = 'Saut'
            description = 'Effectue un saut vers une autre macro-commande,\nsi la condition spécifiée est remplie.'
            text1 = "Si:"
            text2 = "Saut vers:"
            text3 = "et retour ici à la fin du saut"
            mesg1 = 'Sélectionnez une macro-commande...'
            mesg2 = 'Veuillez sélectionner la macro-commande à exécuter si la condition est remplie:'
            choices = ["la dernière action a réussi",
                       "la dernière action a échouée",
                       "Tout le temps"]
            labels = ['En cas de succes, saute vers "%s"',
                      'En cas d\'échec, saute vers "%s"',
                      'Saute vers "%s"',
                      'En cas de succes, saute vers "%s" et reviens',
                      'En cas d\'échec, saute vers "%s" et reviens',
                      'Saute vers "%s" et reviens']
        
        class StopProcessing:
            name = 'Stoppe l\'exécution de cet évènement.'
            description = 'Stoppe l\'exécution de cet évènement.'
            
        class Wait:
            name = 'Temporisation'
            description = 'Attend un nombre prédéfini de seconde'
            label = 'Attente: %s secondes'
            wait = 'Attent' ##
            seconds = 'secondes'
            
        class EnableExclusive: 
            pass
            
        class EnableItem:
            name = 'Activation d\'un élément'
            description = 'Active un élément'
            label = 'Activation: %s'
            text1 = 'Veuillez sélectionner l\'élément à activer:'
            
        class DisableItem:
            name = 'Désactivation d\'un élément'
            description = 'Désactive d\'un élément'
            label = 'Désactivation: %s'
            text1 = 'Veuillez sélectionner l\'élément à désactiver:'
            
        class AutoRepeat:
            name = 'Répétition automatique de la macro-commande courante'
            description = 'Transforme la macro-commande à laquelle cette action est ajouté en une macro-commande qui se répète toute seule.'
            seconds = 'secondes'
            text1 = 'Première répétition après'
            text2 = 'avec une répétition toutes les'
            text3 = 'Increase repetition the next'
            text4 = 'to one repetition every'
            
        class Jump:
            name = 'Saut'
            description = 'Effectue un saut inconditionnel vers une autre macro-commande et retourne éventuellement ici.'
            label1 = 'Saut vers %s'
            label2 = 'Saut vers %s avec retour'
            text2 = 'SAute vers:'
            text3 = 'Retour ici à la fin du saut'
            mesg1 = 'Sélectionnez une macro-commande...'
            mesg2 = 'Veuillez sélectionner la macro-commande à exécuter:'
            
        class JumpIf:
            name = 'Saut conditionnel'
            description = 'Effectue un saut vers une autre macro-commande, si une expression python retourne la valeur vraie.'
            label1 = 'Si %s aller vers %s'
            label2 = 'Si %s aller vers %s'
            text1 = 'Si:'
            text2 = 'Aller vers:'
            text3 = 'Retour ici à la fin du saut'
            mesg1 = 'Sélectionnez une macro-commande...'
            mesg2 = 'Veuillez sélectionner la macro-commande à exécuter\nsi l\'expression python est vraie:'
            

    class System:
        name = "Système"
        
    class Window:
        class SendMessage:
            pass
    
    class Mouse:
        name = 'Souris'
        

    class X10:
        allButton = "&Tous"
        noneButton = "Aucu&n"
        remoteBox = "Sélectionnez un type de télécommande"
        idBox = "Sélectionnez un ID"
        usePrefix = "Utiliser le préfixe"

me = Plugin.EventGhost.EnableExclusive
me.name = 'Activation exclusive d\'un dossier/d\'une macro-commande'
me.description = """
Active un dossier ou macro-commande, en désactivant tous les autres
dossiers/macro-commandes situés au même niveau dans l\'arbre de
configuration."""
me.label = 'Activation exclusive: %s'
me.text1 = 'Veuillez sélectioner le dossier ou la macro-commande qui doit être activée de manière exclusive:'


me = Plugin.Window.SendMessage
me.name = 'Send Message'
me.description = """
Utilise la fonction SendMessage de la Windows-API pour envoyer à une fenêtre
un message. Vous pouvez également utilisez PostMessage si vous le désirez.<p>
Pour les experts seulements."""
me.text1 = 'Utilisz PostMessage en lieu et place de SendMessage'

