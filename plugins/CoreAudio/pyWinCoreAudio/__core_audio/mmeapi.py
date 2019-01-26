WAVERR_BASE = 32

WAVERR_BADFORMAT = WAVERR_BASE # /* unsupported wave format */
WAVERR_STILLPLAYING = WAVERR_BASE + 1 # /* still something playing */
WAVERR_UNPREPARED = WAVERR_BASE + 2 # /* header not prepared */
WAVERR_SYNC = WAVERR_BASE + 3 # /* device is synchronous */
WAVERR_LASTERROR = WAVERR_BASE + 3 # /* last error in range */


def MAKEFOURCC(ch0, ch1, ch2, ch3):
    return (
        ord(ch0) |
        ord(ch1) << 8 |
        ord(ch2) << 16 |
        ord(ch3) << 24
    )


MM_JOY1MOVE = 0x3A0 # /* joystick */
MM_JOY2MOVE = 0x3A1
MM_JOY1ZMOVE = 0x3A2
MM_JOY2ZMOVE = 0x3A3
MM_JOY1BUTTONDOWN = 0x3B5
MM_JOY2BUTTONDOWN = 0x3B6
MM_JOY1BUTTONUP = 0x3B7
MM_JOY2BUTTONUP = 0x3B8

MM_MCINOTIFY = 0x3B9 # /* MCI */

MM_WOM_OPEN = 0x3BB # /* waveform output */
MM_WOM_CLOSE = 0x3BC
MM_WOM_DONE = 0x3BD

MM_WIM_OPEN = 0x3BE # /* waveform input */
MM_WIM_CLOSE = 0x3BF
MM_WIM_DATA = 0x3C0

MM_MIM_OPEN = 0x3C1 # /* MIDI input */
MM_MIM_CLOSE = 0x3C2
MM_MIM_DATA = 0x3C3
MM_MIM_LONGDATA = 0x3C4
MM_MIM_ERROR = 0x3C5
MM_MIM_LONGERROR = 0x3C6

MM_MOM_OPEN = 0x3C7 # /* MIDI output */
MM_MOM_CLOSE = 0x3C8
MM_MOM_DONE = 0x3C9

MM_DRVM_OPEN = 0x3D0 # /* installable drivers */
MM_DRVM_CLOSE = 0x3D1
MM_DRVM_DATA = 0x3D2
MM_DRVM_ERROR = 0x3D3

MM_STREAM_OPEN = 0x3D4
MM_STREAM_CLOSE = 0x3D5
MM_STREAM_DONE = 0x3D6
MM_STREAM_ERROR = 0x3D7


MM_MOM_POSITIONCB = 0x3CA # /* Callback for MEVT_POSITIONCB */

MM_MCISIGNAL = 0x3CB

MM_MIM_MOREDATA = 0x3CC # /* MIM_DONE w/ pending events */

MM_MIXM_LINE_CHANGE = 0x3D0 # /* mixer line change notify */
MM_MIXM_CONTROL_CHANGE = 0x3D1 # /* mixer control change notify */

# /****************************************************************************

#                 String resource number bases (internal use)

# ****************************************************************************/

MMSYSERR_BASE = 0
WAVERR_BASE = 32
MIDIERR_BASE = 64
TIMERR_BASE = 96
JOYERR_BASE = 160
MCIERR_BASE = 256
MIXERR_BASE = 1024

MCI_STRING_OFFSET = 512
MCI_VD_OFFSET = 1024
MCI_CD_OFFSET = 1088
MCI_WAVE_OFFSET = 1152
MCI_SEQ_OFFSET = 1216

# /****************************************************************************

#                         General error return values

# ****************************************************************************/

# /* general error return values */
MMSYSERR_NOERROR = 0 # /* no error */
MMSYSERR_ERROR = MMSYSERR_BASE + 1 # /* unspecified error */
MMSYSERR_BADDEVICEID = MMSYSERR_BASE + 2 # /* device ID out of range */
MMSYSERR_NOTENABLED = MMSYSERR_BASE + 3 # /* driver failed enable */
MMSYSERR_ALLOCATED = MMSYSERR_BASE + 4 # /* device already allocated */
MMSYSERR_INVALHANDLE = MMSYSERR_BASE + 5 # /* device handle is invalid */
MMSYSERR_NODRIVER = MMSYSERR_BASE + 6 # /* no device driver present */
MMSYSERR_NOMEM = MMSYSERR_BASE + 7 # /* memory allocation error */
MMSYSERR_NOTSUPPORTED = MMSYSERR_BASE + 8 # /* function isn't supported */
MMSYSERR_BADERRNUM = MMSYSERR_BASE + 9 # /* error value out of range */
MMSYSERR_INVALFLAG = MMSYSERR_BASE + 10 # /* invalid flag passed */
MMSYSERR_INVALPARAM = MMSYSERR_BASE + 11 # /* invalid parameter passed */

# /* handle being used simultaneously on another thread (eg callback) */
MMSYSERR_HANDLEBUSY = MMSYSERR_BASE + 12
MMSYSERR_INVALIDALIAS = MMSYSERR_BASE + 13 # /* specified alias not found */
MMSYSERR_BADDB = MMSYSERR_BASE + 14 # /* bad registry database */
MMSYSERR_KEYNOTFOUND = MMSYSERR_BASE + 15 # /* registry key not found */
MMSYSERR_READERROR = MMSYSERR_BASE + 16 # /* registry read error */
MMSYSERR_WRITEERROR = MMSYSERR_BASE + 17 # /* registry write error */
MMSYSERR_DELETEERROR = MMSYSERR_BASE + 18 # /* registry delete error */
MMSYSERR_VALNOTFOUND = MMSYSERR_BASE + 19 # /* registry value not found */

# /* driver does not call DriverCallback */
MMSYSERR_NODRIVERCB = MMSYSERR_BASE + 20
MMSYSERR_MOREDATA = MMSYSERR_BASE + 21 # /* more data to be returned */
MMSYSERR_LASTERROR = MMSYSERR_BASE + 21 # /* last error in range */


# /****************************************************************************

#                           Driver callback support

# ****************************************************************************/

# /* flags used with waveOutOpen(), waveInOpen(), midiInOpen(), and */
# /* midiOutOpen() to specify the type of the dwCallback parameter. */

CALLBACK_TYPEMASK = 0x00070000 # /* callback type mask */
CALLBACK_NULL = 0x00000000 # /* no callback */
CALLBACK_WINDOW = 0x00010000 # /* dwCallback is a HWND */
CALLBACK_TASK = 0x00020000 # /* dwCallback is a HTASK */
CALLBACK_FUNCTION = 0x00030000 # /* dwCallback is a FARPROC */
CALLBACK_THREAD = CALLBACK_TASK # /* thread ID replaces 16 bit task */
CALLBACK_EVENT = 0x00050000 # /* dwCallback is an EVENT Handle */
