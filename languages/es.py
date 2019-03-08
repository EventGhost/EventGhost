# -*- coding: UTF-8 -*-
class General:
    apply = u"Aplicar"
    autostartItem = u"AutoIniciar"
    browse = u"Explorar..."
    cancel = u"Cancelar"
    choose = u"Escoger"
    configTree = u"Opciones de Configuracion"
    deleteLinkedItems = u"Al menos un elemento no seleccionado esta referenciado en un elemento que si ha sido seleccionado. Si desea continuar borrando la actual seleccion, el elemento referido no volvera a operar correctamente nunca mas.\n\nEsta ud. seguro de querer borrar la seleccion actual?"
    deleteManyQuestion = u"Este Elemento tiene %s subelementos.\nEsta ud. seguro de que quiere borrar todos ellos?"
    deletePlugin = u"Este plugin es usado por alguna accion de su configuracion actual.\nNo puede se borrado, hasta que las acciones que estan usando el plugin hallan sido eliminadas."
    deleteQuestion = u"Esta ud. seguro que quiere borrar este elemento?"
    help = u"&Ayuda"
    moreTag = u"mas..."
    noOptionsAction = u"Esta accion no tiene opciones configurables."
    noOptionsPlugin = u"Este plugin no tiene opciones configurables"
    ok = u"Aceptar"
    pluginLabel = u"Plugin: %s"
    test = u"&Test"
    unnamedEvent = u"<evento sin nombre>"
    unnamedFile = u"<fichero sin nombre>"
    unnamedFolder = u"<directorio sin nombre>"
    unnamedMacro = u"<macro sin nombre>"
class MainFrame:
    onlyLogAssigned = u"&Registrar solamente los eventos asignados y activados"
    class Logger:
        caption = u"Log"
        descriptionHeader = u"Descripcion"
        timeHeader = u"Tiempo"
        welcomeText = u"---> Bienvenido a EventGhost <---"
    class Menu:
        About = u"&Acerca de EventGhost"
        AddPlugin = u"Añadir Plugin"
        Apply = u"&Aplicar Cambios"
        CheckUpdate = u"Comprobar actualizaciones ahora...."
        ClearLog = u"Limpiar Log"
        Close = u"&Cerrar"
        CollapseAll = u"&Colapsar Todo"
        ConfigurationMenu = u"&Configuracion"
        Copy = u"&Copiar"
        Cut = u"Cor&tar"
        Delete = u"&Borrar"
        Disabled = u"Deshabilitar Elemento"
        Configure = u"Configurar Elemento"
        EditMenu = u"&Editar"
        Execute = u"Ejecutar Elemento"
        Exit = u"&Salir"
        ExpandAll = u"&Expandir Todo"
        ExpandOnEvents = u"Auto Resaltar un evento"
        ExpandTillMacro = u"Auto expandir solo hasta macro"
        Export = u"Exportar..."
        FileMenu = u"&Archivo"
        Find = u"&Buscar"
        FindNext = u"Buscar &Siguiente"
        HelpMenu = u"&Ayuda"
        HideShowToolbar = u"Barra de Herramientas"
        Import = u"Importar..."
        LogActions = u"Registro de Acciones "
        LogMacros = u"Registro de Macros"
        LogTime = u"Registro de Tiempos"
        New = u"&Nuevo"
        AddAction = u"Añadir Accion"
        AddEvent = u"Añadir Evento"
        AddFolder = u"Añadir directorio"
        AddMacro = u"Añadir Macro"
        Open = u"&Abrir"
        Options = u"&Opciones..."
        Paste = u"&Pegar"
        Redo = u"&Rehacer"
        Rename = u"Renombrar Elemento"
        Reset = u"Inicializar"
        Save = u"&Guardar"
        SaveAs = u"Guardar &Como"
        SelectAll = u"Seleccionar &Todo"
        Undo = u"&Deshacer"
        ViewMenu = u"Ver"
        WebForum = u"Foros de Soporte"
        WebHomepage = u"Pagina Web"
        WebWiki = u"Wiki"
    class SaveChanges:
        mesg = u"El fiche ha sido cambiado.\n\nDesea guardar los cambios?"
        title = u"Guardar cambios?"
    class TaskBarMenu:
        Exit = u"Salir"
        Hide = u"Ocultar EventGhost"
        Show = u"Mostrar EventGhost"
    class Tree:
        caption = u"Configuracion"
class Error:
    FileNotFound = u'El fichero "%s" no pudo ser encontrado.'
    InAction = u'Error en la accion: %s"'
    pluginLoadError = u"Se ha producido un error mientras se cargaba el plugin-archivo %s"
    pluginNotActivated = u'El Plugin "%s" no esta activado'
    pluginStartError = u"Error iniciando el plugin: %s"
class Exceptions:
    DeviceInitFailed = u"No se ha podido iniciar el dispositivo!"
    DeviceNotFound = u"El dispositivo no se ha encontrado!"
    DeviceNotReady = u"El dispositivo no esta listo!"
    DriverNotFound = u"El controlador no se ha encontrado!"
    DriverNotOpen = u"No se ha podido abrir el controlador!"
    InitFailed = u"Fallo iniciando!"
    PluginNotFound = u"Plugin no encontrado!"
    ProgramNotFound = u"La aplicacion no ha podido ser encontrada!"
    ProgramNotRunning = u"La aplicacion no esta en ejecucion!"
    SerialOpenFailed = u"No se puede abrir el puerto serie"
class CheckUpdate:
    ManErrorMesg = u"No ha sido posible obtener la informacion necesaria de la pagina de EventGhost.\n\nPor Favor intentelo nuevamente mas tarde."
    ManErrorTitle = u"Se ha producido un error mientra se verificaba la actualizacion"
    ManOkMesg = u"Su version de EventGhost esta actualizada."
    ManOkTitle = u"No existe ninguna version nueva."
    downloadButton = u"Visitar la pagina de descarga"
    newVersionMesg = u"Una nueve version de EventGhos ha sido liberada.\n\n               Version actual:          %s\n               Ultima version:          %s\n\nDesea descargar la nueva version ?"
    title = u"Una nueva version de EventGhost esta disponible..."
    waitMesg = u"Por Favor espere mientra EventGhost actualiza la informacion."
class AddActionDialog:
    descriptionLabel = u"Descripcion"
    title = u"Seleccione una accion para añadir..."
class AddPluginDialog:
    author = u"Autor:"
    descriptionBox = u"Descripcion"
    externalPlugins = u"Equipamiento externo"
    noInfo = u"No hay informacion disponible."
    noMultiload = u"Este plugin no soporta multiples ejecuciones y ud. tiene al menos una instacion de este plugin en su configuracion."
    noMultiloadTitle = u"No son posibles multiples ejecuciones "
    otherPlugins = u"Otros"
    programPlugins = u"Control de programa"
    remotePlugins = u"Receptor remoto"
    title = u"Escoja un plugin para añadir..."
    version = u"Version:"
class AddActionGroupDialog:
    caption = u"Añadir Acciones?"
    message = u"EventGhost puede añadir un directorio con todas las acciones para este plugin a su estructura de configuracion. Si es lo que ud. desea hacer, seleccione la ubicacion donde desea añadirlos y presione aceptar.\n\nEn caso contrario presione el boton de Cancelar."
class OptionsDialog:
    CheckUpdate = u"Chequear nuevas versiones al iniciar"
    HideOnClose = u"Enviar a la barra de sistema al cerrar"
    HideOnStartup = u"Ocultar al iniciar"
    LanguageGroup = u"Idioma"
    StartGroup = u"Al iniciar"
    StartWithWindows = u"Ejecutar al iniciar Windows"
    Tab1 = u"General"
    Title = u"Opciones"
    UseAutoloadFile = u"Fichero Autocargado"
    Warning = u"El cambio de idioma solo tendra efecto tras reiniciar la aplicacion."
    confirmDelete = u"Confirmar borrado el borrado de un elemento de la configuracion."
    limitMemory1 = u"Limitar el consumo de memoria mientras esta minimizado a"
    limitMemory2 = u"MB"
class FindDialog:
    caseSensitive = u"&Diferenciar caracteres"
    direction = u"Direccion"
    down = u"&Abajo"
    findButton = u"&Buscar siguiente"
    notFoundMesg = u'"%s" no pudo ser encontrado.'
    searchLabel = u"&Buscar por:"
    searchParameters = u"Buscar tambien por los parametros de la accion"
    title = u"Buscar"
    up = u"&Arriba"
    wholeWordsOnly = u"Coincidir &toda la palabra "
class AboutDialog:
    Author = u"Autor: %s"
    CreationDate = u"%a, %d %b %Y %H:%M:%S"
    Title = u"Acerca de EventGhost"
    Version = u"Version: %s (build %s)"
    tabAbout = u"Acerca de"
    tabChangelog = u"Registro de cambios"
    tabLicense = u"Acuerdo de Licencia"
    tabSpecialThanks = u"Agradecimientos Especiales"
    tabSystemInfo = u"Informacion de Sistema"
class Plugin:
    class EventGhost:
        name = u"EventGhost"
        description = u"Aqui puede encontrar acciones que principalmente controlan el nucleo de EventGhost."
        class AutoRepeat:
            name = u"Repetir automaticamente la macro actual"
            description = u"Convierte la macro donde se añada este comando en macro que se repite automaticamente."
            seconds = u"segundos"
            text1 = u"Emprezar la primera repeticion despues de"
            text2 = u"un repeticion cada"
            text3 = u"Incrementar la repeticon la proxima"
            text4 = u"a una repeticion cada"
        class Comment:
            name = u"Comentario"
            description = u"No realiza ninguna accion, puede ser utilizada para comentar su configuracion."
        class DisableItem:
            name = u"Deshabilitar un elemento"
            description = u"Deshabilitar un elemento"
            label = u"Deshabilitar: %s"
            text1 = u"Por favor seleccione el elemento que deberia ser deshabilitado:"
        class EnableExclusive:
            name = u"Habilitar en modo exclusivo un directorio/macro"
            description = u"Esto habilitara una carpeta o una macro especificada en su configuración, pero también inhabilita el resto de carpetas y las macros que sean parejos en el mismo nivel secundario de la estructura."
            label = u"Habilitar exclusivamente:  %s"
            text1 = u"Por favor seleccione el directorio/macro que deberia se activado:"
        class EnableItem:
            name = u"Habilitar un elemento"
            description = u"Habilitar un elemento en la estructura"
            label = u"Habilitar: %s"
            text1 = u"Por favor seleccione el elemento que deberia ser habilitado:"
        class FlushEvents:
            name = u"Limpiar eventos pendientes"
            description = u'"Limpiar eventos pendientes" limpia todos los eventos sin procesar que existan actualmente en la cola de procesos.\n\n<p> Es util en el caso de que una macro lleve tiempo procesandose, y existan eventos encolados durando el procedimiento que no deban ser procesados.<p><b>Ejemplo:</b> Se tiene una macro de "inicio de sistema" que consume 90 segundos en procesarse. El usuario final no ve nada hasta que el proyector se enciende , lo cual consume 60s. Es muy probable que dicho usuario presione varias veces el boton del mando que lanza la macro en una columna, causando que el largo procesi se lance una y otra vez. Si se coloca un comando de "limpiar eventos pendientes" al final de la macro, todas las pulsaciones innecesarias  se ignoraran.'
        class JumpIf:
            name = u"Saltar si"
            description = u"Salta a otra macro, si la evaluacion (python) es valida."
            label1 = u"Si %s ir a %s "
            label2 = u"Si %s ir a sub %s "
            mesg1 = u"Seleccione la macro..."
            mesg2 = u"or favor selecione la macro que deberia ser ejecutada, si la condicion es valida."
            text1 = u"Si:"
            text2 = u"Ir a:"
            text3 = u"Volver tras ejecutar"
        class JumpIfLongPress:
            name = u"Saltar si se presiona prolongadamente"
            description = u"Salta a otra macro, si un boton del mando se mantiene pulsado mas tiempo del especificado."
            label = u"Si el boton se presiona %s sec, ir a: %s"
            text1 = u"Si el boton se mantiene pulsado mas de"
            text2 = u"segundos,"
            text3 = u"saltar a:"
            text4 = u"Seleccionar la macro de pulsacion prolongada...."
            text5 = u"Por favor selccecionar la macro, que sera disparada si el evento es un evento prolongado."
        class NewJumpIf:
            name = u"Salta"
            description = u"Salta a otra macro, si la condicion especificada se cumple"
            choices = [
                u"ultima accion realizada",
                u"la ultima accion fue fallida",
                u"Siempre",
            ]
            labels = [
                u'Si la condicion se cumple saltar a "%s"',
                u'Si la condicion no se cumple salatar a "%s"',
                u'Saltar a "%s"',
                u'Si la condicion se cumple, saltar a "%s" y volver',
                u'Si falla, saltar a "%s" y volver',
                u'Saltar a "%s" y volver',
            ]
            mesg1 = u"Seleccione la macro...."
            mesg2 = u"Por favor seleccione la macro que quiera ejecutar, si la condicion se cumple."
            text1 = u"Si:"
            text2 = u"Saltar a:"
            text3 = u"y volver tras ejecutar"
        class PythonCommand:
            name = u"Comando de Python"
            description = u"Ejecuta una sentencia simple de Python."
            parameterDescription = u"Sentencia de Python:"
        class PythonScript:
            name = u"Programa de Python"
            description = u"Capacidades totales para ejecutar programa de Python."
        class ShowOSD:
            name = u"Mostrar Informacion en Pantalla (OSD)"
            description = u"Muestra una indicacion en pantalla."
            alignment = u"Alineacion:"
            alignmentChoices = [
                u"Arriba Izquierda",
                u"Arriba derecha",
                u"Abajo Izquierda",
                u"Abajo derecha",
                u"Centro de la pantalla",
                u"Abajo centrado",
                u"Arriba centrado",
                u"Izquierda centrado",
                u"Derecha centrado",
            ]
            display = u"Mostrar en pantalla:"
            editText = u"Texto a mostrar:"
            label = u"Mostrar OSD: %s"
            osdColour = u"Color OSD:"
            osdFont = u"Fuente OSD:"
            outlineFont = u"Contorno OSD"
            wait1 = u"Ocultar OSD tras"
            wait2 = u"segundos (0 = nunca)"
            xOffset = u"Posicion horizontal X:"
            yOffset = u"Posicion Vertical Y:"
        class StopIf:
            name = u"Parar si"
            description = u"Para la ejecucion de la macro actual, si la funcion de Python devuelve verdadero."
            label = u"Para si %s"
            parameterDescription = u"Condicion Python:"
        class StopProcessing:
            name = u"Parar de procesar este evento"
            description = u"Parar de procesar este evento"
        class TriggerEvent:
            name = u"Lanzar el evento"
            description = u"Causa que un evento sea generado (opcionalmente despues de un tiempo determinado)."
            labelWithTime = u'Lanzar el evento "%s" despues de  %.2f segundos'
            labelWithoutTime = u'Lanzar el evento "%s"'
            text1 = u"El evento generara la cadena:"
            text2 = u"Retardo en el disparo del evento:"
            text3 = u"segundos.(0 = Lanzar inmediatamente)"
        class Wait:
            name = u"Esperar un tiempo"
            description = u"Esperar un tiempo"
            label = u"Esperar: %s seg"
            seconds = u"segundos"
            wait = u"Esperar"
    class System:
        name = u"Sistema"
        description = u"Controla diferentes aspectos de su sistema, como la tarjeta de sonido, tarjeta grafica, encendido, etcetera."
        forced = u"Fuerza: %s"
        forcedCB = u"Fuerza el cierre de todos los programas"
        class ChangeDisplaySettings:
            name = u"Cambia la configuracion de pantalla"
            description = u"Cambia la configuracion de pantalla"
            colourDepth = u"Profundidad de color:"
            display = u"Pantalla:"
            frequency = u"Frecuencia:"
            includeAll = u"Incluir modos que el monitor podria no soportar."
            label = u"Configurar el monitor %d en modo %dx%d@%d Hz"
            resolution = u"Resolucion:"
            storeInRegistry = u"Almacenar este modo en el registro."
        class ChangeMasterVolumeBy:
            name = u"Cambiar volumen maestro"
            description = u"Cambia el volumen maestro respecto de valor actual"
            text1 = u"Cambiar el volumen maestro por"
            text2 = u"por ciento."
        class Execute:
            name = u"Inicia una aplicacion"
            description = u"Inicia un fichero ejecutable."
            FilePath = u"Ruta del ejecutable:"
            Parameters = u"Opciones de la linea de comandos:"
            ProcessOptions = (
                u"Tiempo Real",
                u"Superior a normal",
                u"Normal",
                u"Menor de normal",
                u"Detenido",
            )
            ProcessOptionsDesc = u"Prioridad del proceso:"
            WaitCheckbox = u"Esperar hasta que la aplicacion haya finalizado antes de proceder"
            WindowOptions = (
                u"Normal",
                u"Minimizada",
                u"Maximizada",
                u"Oculta",
            )
            WindowOptionsDesc = u"Opciones de ventana:"
            WorkingDir = u"Directorio de trabajo:"
            browseExecutableDialogTitle = u"Escoja el ejecutable"
            browseWorkingDirDialogTitle = u"Escoja el directorio de trabajo"
            label = u"Iniciar programa: %s"
        class Hibernate:
            name = u"Hibernar el ordenador"
            description = u"Esat funcion suspende el sistema, apagando y entrando en modo de hibernacion (S4)."
        class LockWorkstation:
            name = u"Bloquear la estacion de trabajo"
            description = u"Esta funcion realiza una peticion para bloquear la pantalla de la estacion de trabajo. Bloqueando al estacion de trabajo se protege del acceso no autorizado de la misma. Esta funcion tiene el mismo resultado que si se pulsa Ctrl+Alt+Sup y se hace click sobre bloquear la estacion de trabajo."
        class LogOff:
            name = u"Cierra la sesion del usuario actual"
            description = u"Para todos los procesos en ejecucion en la sesion actual. Tras lo cual cierra la sesion del usuario."
        class MonitorGroup:
            name = u"Pantalla"
            description = u"Estas acciones controlan el estado de encendido de los dispositivos de visualizacion."
        class MonitorPowerOff:
            name = u"Apaga el monitor"
            description = u"Apaga el monitor. Se utilizara el modo mas economico que soporte el dispositivo."
        class MonitorPowerOn:
            name = u"Enciende el monitor"
            description = u"Enciende el monitor, cuando este en modo de bajo consumo o reposo. Tambien parara el salvapantallas."
        class MonitorStandby:
            name = u"Pone el monitor en modo reposo"
            description = u"Pone el monitor en modo de bajo consumo."
        class MuteOff:
            name = u"Cambia Mute a apagado"
            description = u"Cambia Mute a apagado"
        class MuteOn:
            name = u"Cambia Mute a encendido"
            description = u"Cambia Mute a encendido"
        class OpenDriveTray:
            name = u"Abre/Cierra la bandeja"
            description = u"Controla la bandeja del lector de CD/DVD"
            driveLabel = u"Unidad:"
            labels = [
                u"Cambiar la bandeja de la unidad: %s",
                u"Expulsar la bandeja de la unidad: %s",
                u"Cierra la bandeja de la unidad: %s",
            ]
            options = [
                u"Cambiar entre abrir y cerrar la bandeja de la unidad",
                u"Solamnte abrir la bandeja",
                u"Solamente cerrar la bandeja",
            ]
            optionsLabel = u"Escoger accion"
        class PlaySound:
            name = u"Reproducir un sonido"
            description = u"Reproducir un sonido"
            fileMask = u"Wav-Files (*.WAV)|*.wav|All-Files (*.*)|*.*"
            text1 = u"Ruta del fichero de sonido:"
            text2 = u"Espera a finalizar"
        class PowerDown:
            name = u"Apaga el ordenador"
            description = u"Cierran el sistema y lo apagan. El sistema debe soportar esta funcionalidad."
        class PowerGroup:
            name = u"Administracion de energia"
            description = u"Estas acciones suspenden, hibernan, rebotan y apagan el ordenador. ambien pueden bloquear el equipo y cerrar la sesion del usuario actual."
        class Reboot:
            name = u"Reinicia el ordenador"
            description = u"Apaga el ordenador y reinicia el sistema"
        class RegistryChange:
            name = u"Cambia un valor del registro"
            description = u"Cambia un valor en el registro de windows"
            actions = (
                u"crea o cambia",
                u"cambia solamente si existe",
                u"borra",
            )
            labels = (
                u'Cambia "%s" por %s',
                u'Cambia "%s" por %s solamente si existe',
                u'Borra "%s"',
            )
        class RegistryGroup:
            name = u"Registro"
            description = u"Consulta o cambia valores en el registro."
            actionText = u"Accion:"
            chooseText = u"Escoja la clave del registro:"
            defaultText = u"(Por defecto)"
            keyOpenError = u"Error abriendo la clave del registro"
            keyText = u"Clave:"
            keyText2 = u"Clave"
            newValue = u"Nuevo valor:"
            noKeyError = u"Ninguna clave especificada"
            noNewValueError = u"Ningun nuevo valor especificado"
            noSubkeyError = u"Ninguna subclave especificada"
            noTypeError = u"Ningun tipo especificado"
            noValueNameError = u"Ningun valor especificado"
            noValueText = u"valor no encontrado"
            oldType = u"Tipo actual:"
            oldValue = u"Valor actual:"
            typeText = u"Tipo:"
            valueChangeError = u"Error mientras se modificaba el valor"
            valueName = u"Nombre del valor:"
            valueText = u"Valor:"
        class RegistryQuery:
            name = u"Busca en el registro"
            description = u"Busca en el registro y devuelve o compara un valor"
            actions = (
                u"Verifica si existe",
                u"devuelve un resultado",
                u"Compara con",
            )
            labels = (
                u'Chequea si "%s" existe',
                u'Devuelve "%s" como resultado',
                u'Compara "%s" con %s',
            )
        class ResetIdleTimer:
            name = u"Reiniciar el temporizador de inactividad"
            description = u"Reiniciar el temporizador de inactividad"
        class SetClipboard:
            name = u"Copiar una cadena al portapapeles"
            description = u"Copia el parametro de cadena en el portapapeles"
            error = u"No se puede acceder al portapapeles"
        class SetDisplayPreset:
            name = u"Especificar configuracion grafica"
            description = u"Especificar Configuracion grafica"
            fields = (
                u"Dispositivo",
                u"Izquierda",
                u"Arriba",
                u"Ancho",
                u"Altura",
                u"Frecuencia",
                u"Profundidad de Color",
                u"Enlazado",
                u"Primario",
                u"Marcar",
            )
            query = u"Obtener configuracion grafica actual"
        class SetIdleTime:
            name = u"Especificar periodo de inactividad"
            description = u"Especificar periodo de inactividad"
            label1 = u"Esperar"
            label2 = u"segundos antes de lanzar un evento de inactividad"
        class SetMasterVolume:
            name = u"Cambiar el volumen maestro"
            description = u"Cambiar el volumen maestro a un valor absoluto"
            text1 = u"Cambiar el volumen maestro a "
            text2 = u"porcentaje."
        class SetSystemIdleTimer:
            name = u"Activar el temporizador de inactividad del sistema"
            description = u"Activar el temporizador de inactividad del sistema"
            choices = [
                u"Deshabilitar el temporizador de inactividad del sistema",
                u"Habilitar el temporizador de inactividad del sistema",
            ]
            text = u"Escoja una opcion:"
        class SetWallpaper:
            name = u"Cambiar el fondo de pantalla"
            description = u"Cambiar el fondo de pantalla"
            choices = (
                u"Centrado",
                u"Mosaico",
                u"Estirado",
            )
            fileMask = u"Todos los fichero graficos |*.jpg;*.bmp;*.gif;*.png|Todos (*.*)|*.*"
            text1 = u"Ruta del fichero grafico:"
            text2 = u"Alineamiento:"
        class ShowPicture:
            name = u"Mostrar una imagen"
            description = u"Mostrar una imagen en pantalla."
            allFiles = u"Todos los ficheros"
            allImageFiles = u"Todos los ficheros graficos"
            display = u"Monitor"
            path = u"Ruta de la imagen (usar una ruta en blanco para limpiar):"
        class SoundGroup:
            name = u"Tarjeta de Sonido"
            description = u"Estas acciones controlan la tarjeta de sonido de su ordenador"
        class Standby:
            name = u"Ponen el ordenador en modo espera"
            description = u"Esta funcion suspende el sistema apagando y entrando en modo suspendido (espera)."
        class StartScreenSaver:
            name = u"Inicia el salva pantallas"
            description = u"Inicia el salvapantallas configurado actualmente en el sistema."
        class ToggleMute:
            name = u"Cambia a Silencio "
            description = u"Cambia a silencio"
        class WakeOnLan:
            name = u"Encender por red"
            description = u"Arranca otro ordenador mediante el envio de un paquete especial de red."
            parameterDescription = u"Direccion MAC del adaptador de red del ordenador a iniciar:"
    class Window:
        name = u"Ventana"
        description = u"Acciones relativas al control de vantana en el escritorio, como encontrar un aventana especifica, moverla, redimensionarla y enviar pulsaciones de teclado a las mismas."
        class BringToFront:
            name = u"Traen al frente"
            description = u"Traer un ventana especificada a primer plano."
        class Close:
            name = u"Cerrar"
            description = u"Cerrar una aplicacion windows"
        class FindWindow:
            name = u"Buscar una ventana"
            description = u'Buscar un aventana, que posteriormente sera usada como objetivo de futuras acciones de ventana en una macro.\n\n<p>Si una macro no tiene acciones de "Buscar una ventana", todas las acciones de ventana se aplicaran a la ventana en primer plano.<p>En las cajas de edicion se puede utilizar comodines {*} reemplazar cualquier cadena de caracteres o {?} para reeemplazar un caracter.'
            drag1 = u"Arrastrame hasta\nuna ventana."
            drag2 = u"Ahora mueveme\na una ventana."
            hide_box = u"Ocultar EventGhost mientras se arrastra"
            invisible_box = u"Buscar tambien elementos no visibles"
            label = u"Buscar ventana: %s"
            label2 = u"Buscar la ventana en primer plano"
            matchNum1 = u"Solamente devolver"
            matchNum2 = u"coincidencia"
            onlyFrontmost = u"Solamente "
            options = (
                u"Programa:",
                u"Nombre de la ventana:",
                u"Clase de Ventana:",
                u"Ventana hija:",
                u"Clase hija:",
            )
            refresh_btn = u"&Refrescar"
            stopMacro = [
                u"Parar la macro si el objetivo no es encontrado",
                u"Parar la macro si el objetivo es encontrado",
                u"Nunca parar la macro",
            ]
            testButton = u"Probar"
            wait1 = u"Esperar hasta"
            wait2 = u"Segundos a que la ventana aparezca"
        class Maximize:
            name = u"Maximizar"
            description = u"Maximizar"
        class Minimize:
            name = u"Minimizar"
            description = u"Minimizar"
        class MoveTo:
            name = u"Movimiento absoluto"
            description = u"Movimiento absoluto"
            label = u"Mover la ventana a %s"
            text1 = u"Cambiar la posicion horizontal X a"
            text2 = u"pixels"
            text3 = u"Cambiar la posicion vertical Y a"
            text4 = u"pixels"
        class Resize:
            name = u"Redimensionar"
            description = u"Redimensiona una ventana a un tamaño dado. "
            label = u"Redimensionar ventana a %s, %s"
            text1 = u"Cambiar anchura a"
            text2 = u"pixels"
            text3 = u"Cambiar altura a "
            text4 = u"pixels"
        class Restore:
            name = u"Restaurar"
            description = u"Restaurar"
        class SendKeys:
            name = u"Emular pulsaciones de teclado"
            description = u"Esta accion emula la pulsacion de teclas con el fin de controlar programas. Unicamente incluye el texto que desees en la casilla de edicion.\n\n<p>\nPara emular teclas especiales, se deben encerrar las palabras clave entre corchetes. Por ejemplo si se desea un cursor arriba se debe escribir\n <b>{Up}</b>. Se pueden combinar multiples palabras clave con el simbolo de sumar para obtener combinaciones como <b>{Shift+Ctrl+F1}</b> or <b>{Ctrl+V}</b>. Las palabras clave no son sensibles a mayusculas\npor lo que se puede utilizar {SHIFT+ctrl+F1} si se prefiere. \n<p>"
            insertButton = u"&Insertar"
            specialKeyTool = u"Tecals especiales"
            textToType = u"Texto a teclear:"
            useAlternativeMethod = u"Usar metodo alternativo para emular pulsaciones de teclado"
            class Keys:
                backspace = u"Retroceder"
                context = u"Menu Contextual"
                delete = u"Borrar"
                down = u"Abajo"
                end = u"Fin"
                enter = u"Intro"
                escape = u"Escape"
                home = u"Inicio"
                insert = u"Insertar"
                left = u"Izquierda"
                num0 = u"0 Teclado Numerico"
                num1 = u"1 Teclado Numerico"
                num2 = u"2 Teclado Numerico"
                num3 = u"3 Teclado Numerico"
                num4 = u"4 Teclado Numerico"
                num5 = u"5 Teclado Numerico"
                num6 = u"6 Teclado Numerico"
                num7 = u"7 Teclado Numerico"
                num8 = u"8 Teclado Numerico"
                num9 = u"9 Teclado Numerico"
                numAdd = u"Suma Teclado Numerico"
                numDecimal = u"Decimal Teclado Numerico"
                numDivide = u"Division Teclado Numerico"
                numMultiply = u"Multiplicacion Teclado Numerico"
                numSubtract = u"Resta Teclado Numerico"
                pageDown = u"Pagina Abajo"
                pageUp = u"Pagina Arriba"
                returnKey = u"Retorno"
                right = u"Derecha"
                space = u"Espacio"
                tabulator = u"Tabulador"
                up = u"Arriba"
                win = u"Tecla Windows"
        class SendMessage:
            name = u"Enviar mensaje"
            description = u"Usa la funcion SendMessage de la API de Windows para enviar a windows un mensaje. Se puede utilizar PostMessage si se desea."
            text1 = u"Usar PostMessage en lugar de SendMessage "
        class SetAlwaysOnTop:
            name = u"Activar la propiedad siempre encima"
            description = u"Activar la propiedad siempre encima"
            actions = (
                u"Limpiar siempre encima",
                u"Habilitar siempre encima",
                u"Cambiar siempre encima",
            )
            radioBox = u"Escoja una opcion:"
    class Mouse:
        name = u"Raton"
        description = u"Permite acciones para controlar el raton y emulacion de eventos del raton"
        class GoDirection:
            name = u"Iniciar movimiento del raton en una direccion"
            description = u"Iniciar movimiento del raton en una direccion"
            label = u"Iniciar movimiento del raton direccion %.2f°"
            text1 = u"Empezar moviendo el puntero del raton en direccion"
            text2 = u"grados (0-360)"
        class LeftButton:
            name = u"Boton izquierdo del raton"
            description = u"Boton izquierdo del raton"
        class LeftDoubleClick:
            name = u"Doble pulsacion en el boton izquierdo del raton"
            description = u"Doble pulsacion en el boton izquierdo del raton"
        class MiddleButton:
            name = u"Boton central del raton"
            description = u"Boton central del raton"
        class MouseWheel:
            name = u"Girar rueda del raton"
            description = u"Girar rueda del raton"
            label = u"Girar rueda del raton %d intervalos"
            text1 = u"Girar rueda del raton por"
            text2 = u"intervalos. (valores negativos giran en retroceso)"
        class MoveAbsolute:
            name = u"Movimiento absoluto"
            description = u"Movimiento absoluto"
            label = u"Mover el raton a: %s, y:%s"
            text1 = u"Fijar la posicion horizontal X a"
            text2 = u"pixels"
            text3 = u"Fijar la posicion vertical Y a"
            text4 = u"pixels"
        class MoveRelative:
            name = u"Movimiento relativo"
            description = u"Movimiento relativo"
            label = u"Cambiar la posicion a x:%s, y:%s"
            text1 = u"Cambiar la posicion horizontal X por"
            text2 = u"pixels"
            text3 = u"Cambiar la posicion vertical Y por "
            text4 = u"pixels"
        class RightButton:
            name = u"Boton derecho del raton"
            description = u"Boton derecho del raton"
        class RightDoubleClick:
            name = u"Doble pulsacion del boton derecho del raton"
            description = u"Doble pulsacion del boton derecho del raton"
        class ToggleLeftButton:
            name = u"Botón izquierdo de palanca"
            description = u"Botón izquierdo de palanca del ratón"
