# -*- coding: latin-1 -*-

class General:
    ok              = "OK"
    cancel          = "Annuler"
    help            = "&Aide"
    unnamedFolder      = "<Dossier sans nom>"
    unnamedMacro       = "<Macro-commande sans nom>"
    unnamedEvent       = "<�v�nement sans nom>"
    unnamedFile         = "<Sans nom>"
    configTree      = "Arbre de configuration"
    autostartItem   = "D�marrage automatique"
    browse    = "Parcourir..."
    choose          = "S�lection"
    deleteManyQuestion      = "Cet �l�ment poss�de %s sous-�l�ments.\n�tes-vous certain de vouloir tous les supprimer?"
    deletePlugin    = "Ce greffon est utilis� dans votre configuration.\nVous ne pouvez pas l'enlever tant que des actions l'utlisant sont pr�sentes."
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
        SelectAll       = "&Tout s�lectionner"
        AddPlugin       = "Ajouter un greffon..."
        NewFolder       = "Ajouter un dossier..."
        NewMacro        = "Ajouter une macro-commande..."
        NewEvent        = "Ajouter un �v�nement..."
        NewAction       = "Ajouter une action..."
        Edit            = "Propri�t�s de l'�lement..."
        Rename          = "Renommer"
        Disabled        = "D�sactiv�"
        Execute         = "Ex�cuter"

        ViewMenu        = "Affichage"
        HideShowToolbar = "Barre d'outils"
        CollapseAll     = "&Replier l'arbre de configuration"
        ExpandAll       = "&D�plier l'arbre de configuration"
        ExpandOnEvents  = "D�plier automatiquement l'arbre lors d'un �v�nement" ##
        ExpandTillMacro = "Limiter le d�pliment automatique au niveau macro-commande" ##
        LogActions      = "Rapport sur les actions"
        LogTime         = "Inclure l'heure dans le rapport"
        
        HelpMenu        = "&Aide"
        About           = "� &propos d'EventGhost..."
        WebHomepage     = "Pa&ge d'accueil d'EventGhost"
        WebForum        = "&Forum d'entre-aide"
        WebWiki         = "&Wiki"
        CheckUpdate     = "Recherche de &mise-�-jour..."

    class TaskBarMenu:
        Show            = "Afficher EventGhost"
        Hide            = "Masquer EventGhost"
        Exit            = "Sortie"
        
    class SaveChanges:
        title           = "Sauver les changements ?"
        mesg            = "Ce fichier � �t� modifi�.\n\nVoulez-vous sauvegarder les changements effectu�s ?\n"

class AboutDialog:
    Title           = "� propos d'EventGhost"
    Author          = "Auteur: %s"
    Version         = "Version: %s (build %s)"
    CreationDate    = "%a, %d %b %Y %H:%M:%S"


class OptionsDialog:
    Title           = "Options"
    Tab1            = "G�n�ral"
    StartGroup      = "D�marrage"
    HideOnStartup   = "Masquer au d�marrage"
    HideOnClose     = "Fermer la fen�tre ne fait pas quitter l'application"
    UseAutoloadFile = "Chargement automatique du fichier " ###
    LanguageGroup   = "Langues"
    Warning         = "Les changements de langues ne prendront effets qu'au red�marrage de l'application."
    StartWithWindows= "Lancer au d�marrage de Windows"
    CheckUpdate     = "V�rifier l'existence d'une nouvelle version"
    
    
class ScriptEditor:
    Title           = "Python-Editor - %s"


class AddPluginDialog:
    title           = "Choisissez un greffon � ajouter..."
    noInfo          = "Pas d'informations disponible."
    noMultiloadTitle= "Pas de multichargement possible"
    noMultiload     = "Ce greffon ne supporte pas le multichargement et il en existe d�j� une instance dans votre configuration."
    remotePlugins   = "Greffons de prise en charge de t�l�commande"
    programPlugins  = "Greffons de prise en charge de programme tiers"
    otherPlugins    = "Autres greffons"
    author          = "Auteur:"
    version         = "Version:"
    descriptionBox  = "Description:"
    
    
class AddActionDialog:
    title           = "S�lectionner une action � ajouter..."
    descriptionLabel = "Description"

class CheckUpdate:
    title = "Nouvelle version d\'EventGhost disponible..."
    newVersionMesg = "Une nouvelle version d\'EventGhost vient de sortir.\n\n\
\tVotre version:\t%s\n\
\tDerni�re version:\t%s\n\n\
Voulez-vous acc�der � la page de t�l�chargement?"
    downloadButton = "Visiter la page de t�l�chargement."
    waitMesg = "Veuillez patienter le temps qu'EventGhost r�cup�re les informations de mise-�-jour."
    ManOkTitle = "Pas de nouvelle version disponible."    
    ManOkMesg = "Cette version d'EventGhost est la derni�re."    
    ManErrorTitle = "Erreur lors de la mise-�-jour"
    ManErrorMesg = "Impossible de r�cuperer les informations depuis le site d'EventGhost.\n\nVeuillez r�essayer plus tard."


class Error:
    FileNotFound    = 'Le fichier "%s" n\'a pu �tre trouv�.'
    InAction        = 'Erreur lors de l\'Action suivante: "%s"'
    InScript        = 'Erreur dans le script: "%s"'


class Plugin:
    class EventGhost:
        description = "Vous trouverez ici les principales actions d'EventGhost."
        
        class PythonCommand:
            name = 'Commande Python'
            description = "Ex�cute l'argument comme une commande python unique.<p> <i>Exemple :</i><br><br>print \"Bonjour\"<br><br><i>ou encore</i><br><br> iMaVariable = 3"
            parameterDescription = 'Commande Python:'
            
        class PythonScript:
            name = 'Script Python'
            description = 'V�ritable script Python.'
            
        class Comment:
            name = 'Commentaire'
            description = 'Utilisez cette commande sans effet pour commenter votre configuration.'
            
        class NewJumpIf:
            name = 'Saut'
            description = 'Effectue un saut vers une autre macro-commande,\nsi la condition sp�cifi�e est remplie.'
            text1 = "Si:"
            text2 = "Saut vers:"
            text3 = "et retour ici � la fin du saut"
            mesg1 = 'S�lectionnez une macro-commande...'
            mesg2 = 'Veuillez s�lectionner la macro-commande � ex�cuter si la condition est remplie:'
            choices = ["la derni�re action a r�ussi",
                       "la derni�re action a �chou�e",
                       "Tout le temps"]
            labels = ['En cas de succes, saute vers "%s"',
                      'En cas d\'�chec, saute vers "%s"',
                      'Saute vers "%s"',
                      'En cas de succes, saute vers "%s" et reviens',
                      'En cas d\'�chec, saute vers "%s" et reviens',
                      'Saute vers "%s" et reviens']
        
        class StopProcessing:
            name = 'Stoppe l\'ex�cution de cet �v�nement.'
            description = 'Stoppe l\'ex�cution de cet �v�nement.'
            
        class Wait:
            name = 'Temporisation'
            description = 'Attend un nombre pr�d�fini de seconde'
            label = 'Attente: %s secondes'
            wait = 'Attent' ##
            seconds = 'secondes'
            
        class EnableExclusive: 
            pass
            
        class EnableItem:
            name = 'Activation d\'un �l�ment'
            description = 'Active un �l�ment'
            label = 'Activation: %s'
            text1 = 'Veuillez s�lectionner l\'�l�ment � activer:'
            
        class DisableItem:
            name = 'D�sactivation d\'un �l�ment'
            description = 'D�sactive d\'un �l�ment'
            label = 'D�sactivation: %s'
            text1 = 'Veuillez s�lectionner l\'�l�ment � d�sactiver:'
            
        class AutoRepeat:
            name = 'R�p�tition automatique de la macro-commande courante'
            description = 'Transforme la macro-commande � laquelle cette action est ajout� en une macro-commande qui se r�p�te toute seule.'
            seconds = 'secondes'
            text1 = 'Premi�re r�p�tition apr�s'
            text2 = 'avec une r�p�tition toutes les'
            text3 = 'Increase repetition the next'
            text4 = 'to one repetition every'
            
        class Jump:
            name = 'Saut'
            description = 'Effectue un saut inconditionnel vers une autre macro-commande et retourne �ventuellement ici.'
            label1 = 'Saut vers %s'
            label2 = 'Saut vers %s avec retour'
            text2 = 'SAute vers:'
            text3 = 'Retour ici � la fin du saut'
            mesg1 = 'S�lectionnez une macro-commande...'
            mesg2 = 'Veuillez s�lectionner la macro-commande � ex�cuter:'
            
        class JumpIf:
            name = 'Saut conditionnel'
            description = 'Effectue un saut vers une autre macro-commande, si une expression python retourne la valeur vraie.'
            label1 = 'Si %s aller vers %s'
            label2 = 'Si %s aller vers %s'
            text1 = 'Si:'
            text2 = 'Aller vers:'
            text3 = 'Retour ici � la fin du saut'
            mesg1 = 'S�lectionnez une macro-commande...'
            mesg2 = 'Veuillez s�lectionner la macro-commande � ex�cuter\nsi l\'expression python est vraie:'
            

    class System:
        name = "Syst�me"
        
    class Window:
        class SendMessage:
            pass
    
    class Mouse:
        name = 'Souris'
        

    class X10:
        allButton = "&Tous"
        noneButton = "Aucu&n"
        remoteBox = "S�lectionnez un type de t�l�commande"
        idBox = "S�lectionnez un ID"
        usePrefix = "Utiliser le pr�fixe"

me = Plugin.EventGhost.EnableExclusive
me.name = 'Activation exclusive d\'un dossier/d\'une macro-commande'
me.description = """
Active un dossier ou macro-commande, en d�sactivant tous les autres
dossiers/macro-commandes situ�s au m�me niveau dans l\'arbre de
configuration."""
me.label = 'Activation exclusive: %s'
me.text1 = 'Veuillez s�lectioner le dossier ou la macro-commande qui doit �tre activ�e de mani�re exclusive:'


me = Plugin.Window.SendMessage
me.name = 'Send Message'
me.description = """
Utilise la fonction SendMessage de la Windows-API pour envoyer � une fen�tre
un message. Vous pouvez �galement utilisez PostMessage si vous le d�sirez.<p>
Pour les experts seulements."""
me.text1 = 'Utilisz PostMessage en lieu et place de SendMessage'

