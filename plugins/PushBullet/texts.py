# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2015  Pako <lubos.ruckl@gmail.com>
#
# This file is part of the PushBullet plugin for EventGhost.
#


from eg import TranslatableStrings


class Text(TranslatableStrings):
    recips = "Recipients:"
    device = "Device:"
    recip = "Recipient:"
    header = (
        "Device",
        "Name",
        "Phone number"
    )
    file = "File:"
    ext = "List of file extensions:"
    notLbl = " not"
    ifExt = "if extension"
    inLbl = "in"
    autoOpen = "Automatically open downloaded pictures"
    firstWord = """If title of push (type Note) is missing, use the first word out of the body as the event suffix"""
    enabMirr = "Enable popping up of mirrored notification"
    nLabel = 'Nickname of this "device":'
    apiLabel = 'API key:'
    password = "Encryption password:"
    prefix = 'Event prefix:'
    mode = 'The title of the push to use as:'
    modes = ("event suffix", "payload[0]")
    complPush = "Use the complete original push as last part of the payload"
    folder = 'Directory for file download:'
    timeout = 'Timeout for auto-hide [s]:'
    pTimeout = 'Picture hide timeout [s]:'
    timeout2 = "(0 = not to hide)"
    err = 'Failed to open file "%s"'
    debug = "Logging level:"
    debug2 = "(the higher the number, the more message writes ...)"
    hideBtn = "Hide disable button on mirrored notifications"
    title3 = "Unmute a disabled application"
    title4 = "PushBullet - quick replying to: %s"
    enabLbl = "Disabled application:"
    cancel = "Cancel"
    ok = "OK"
    unmute = "Unmute"
    reenab = "Re-enable mirroring for an app ..."
    tooltip = "Right mouse button closes this window"
    disable = 'Mute "%s"'
    clipFilter = 'Filter of clipboard change monitoring ' \
                 '(device checked = notifying disabled)'
    filterToolTip = "This combo is enabled only if the devices are synced !"
    wavs = "Alerting sounds location:"
    reconnect = "Haven't seen a nop lately, reconnecting"
    waiting = "Haven't seen a nop lately, waiting for connectivity"
    waiting2 = "PushBullet: No connectivity, waiting ..."
    uplFld = u'Failed to upload the file "%s"'
    uplSucc = u'The file "%s" was uploaded successfully'
    addLstnr = 'Adding push messaging listener'
    wsMssg = "WebSocket message: %s"
    dcrptdMssg = "Decrypted message: %s"
    rspnsr = "Response = %s"
    fTriggMute = 'Failed to trigger mute of app %s'
    triggMute = "Triggered mute of app %s"
    fPong = 'Failed to send pong'
    pong = "Pong was sent"
    fTriggUnmute = 'Failed to trigger unmute of app %s'
    triggUnmute = "Triggered unmute of app %s"
    gettPshs = "Getting pushes, modified_after = %.7f"
    fLoadPshs = "Failed to load pushes"
    thrReqRes = "Threads request response = %s"
    fLoadThrds = "Failed to load threads"
    e2eMssg1 = 'End to end encryption: Invalid version'
    e2eMssg2 = 'End to end encryption: Decrypted message is not a dictionary'
    e2eMssg3 = 'End to end encryption: Decryption failed'
    smsSent = 'SMS sent successfuly to device "%s"'
    smsSentF = 'SMS sent to device "%s" failed'
    fRetrTmstmp = "Failed to retrieve timestamp"
    mdfdUpd = "modified_after updated: %.7f"
    wsOpenedEvt = "WebSocketOpened"
    wsClosedEvt = "WebSocketClosed"
    wsError = u"PushBullet: WebSocket error: %s"
    idenSaved = 'New iden "%s" automatically saved'
    dsbldUpdated = 'List of disabled app automatically updated'
    emlObtained = "Email address obtained"
    accReqFailed = "Account request failed"
    noApi = "No API key"
    noNick = "No nickname"
    devRcvd = "Devices received: %s"
    devReqFailed = "Device request failed"
    bookRcvd = 'Phonebook from device "%s" received'
    thrdsRcvd = 'SMS threads from device "%s" received'
    bookReqFailed = 'Phonebook request from device "%s" failed'
    noDev = "No devices"
    pcMssng = "This EventGhost is missing in the device list. " \
              "Request for creating device sent."
    devCrtd = "Device created: %s"
    crDevFld = "Creating device failed"
    pushDelted = "Push deleted"
    pushDelFld = 'Push deleting failed: "%s"'
    forwRep = "Forwarding reply to extension in %s"
    forwRepFld = "Failed to forward reply to extension in %s"
    dismissNote = 'Notification "%s" dismissed'
    dismissNoteFld = 'Dismiss of notification "%s" failed'
    dismissPush = 'Push "%s" dismissed'
    dismissPushFld = 'Dismiss of push "%s" failed'
    dismissSms = 'Triggered remote sms dismissal'
    dismissSmsFld = 'Failed to trigger remote sms dismissal'
    notIdMissing = 'Parameter "notification_id" is missing!'
    notDismiss = 'Push "%s" is marked as "not dismissable" ! ' \
                 "Still, I'll try it."
    reply = "Reply"
    replyPrompt = "Type your reply here.\n" \
                  "You can use the Enter (or Return) key to make new line.\n" \
                  "You can use Ctrl-Enter (Ctrl-Return) to send the message.\n" \
                  "The dialog can be resized.\n" \
                  "You can even copy a text from the incoming messages !"
    frndsRcvd = "Friends received: %s"
    chnnlsRcvd = "Channels received: %s"
    trgtsDrvd = "Targets derived: %s"
    pushRslt = "Push results: %s"
    dwnldFailed = 'Download of "%s" failed (code %i)'
    nicknameUsed = 'PushBullet: Chosen nickname "%s" is already used for ' \
                   'other device, than the "EventGhost"  !!!'
    wavFldr = "Select the folder that stores sounds ..."
    toolWav = '''Here you can select the folder, where you saved the alerting
sounds. If the field is left blank, this feature will not be used. 
Sounds must be in "wav" format and must have the same name, 
as the corresponding push type (for example, "note.wav", for "note" push). 
If some sound is missing, this feature will not be used (for the corresponding 
push type).'''
    kinds = (
        "Note",
        "Link",
        "File",
        "Mirror",
    )
    choices = [
        "the file extension is one of the listed extension",
        "the file extension is not one of the listed extension",
    ]
    mirroring = "Mirroring"
    bcgColour = "Background Colour:"
    alignment = "Alignment:"
    alignmentChoices = [
        "Top Left",
        "Top Right",
        "Bottom Left",
        "Bottom Right",
        "Screen Center",
        "Bottom Center",
        "Top Center",
        "Left Center",
        "Right Center",
    ]
    display = "Show on display:"
    xOffset = "Horizontal offset X:"
    yOffset = "Vertical offset Y:"
    pushGroupsTitle = 'Push recipient groups'
    smsGroupsTitle = 'SMS recipient groups'
    groupsList = "List of groups:"
    groupLabel = "Group name:"
    delete = 'Delete'
    insert = 'Add new'
    tsLabel = "Push targets:"
    unknStream = 'PushBullet: Unknown stream push type: "%s"'
    reqErr = "PushBullet: Request error: %s"
    noKey = '''Pushbullet: Encrypted data received.
            You must enter the encryption password,
            or turn off the End to end encryption on your other devices.'''
    headers = (
        "Host:",
        "Port:",
        "Username:",
        "Password:",
    )
    proxyInfo = """If the proxy server does not require authentication, 
leave the Username and Password entries blank."""
    proxyTitle = "Proxy settings"
