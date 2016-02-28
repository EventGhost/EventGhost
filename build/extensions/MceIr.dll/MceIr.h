#ifndef MCEIR
#define MCEIR

#ifdef cplusplus
extern "C" {
#endif

#define ID_MCEIR_KEYCODE    0x37FF0  //wParam of WM_COMMAND message
//#define ID_SONY_KEYCODE     0x37FF1  
//#define ID_NEC_KEYCODE      0x37FF2  
//#define ID_RC5_KEYCODE      0x37FF3  

#define ID_SONY_KEYCODE     ID_MCEIR_KEYCODE  
#define ID_NEC_KEYCODE      ID_MCEIR_KEYCODE  
#define ID_RC5_KEYCODE      ID_MCEIR_KEYCODE  
#define ID_RC6_KEYCODE      ID_MCEIR_KEYCODE  
#define ID_REC80_KEYCODE    ID_MCEIR_KEYCODE  

#define REMOTEKEY_TVPWR		  0x7b9a  //LOWORD(lParam) of message
#define REMOTEKEY_BLUE		  0x7ba1  //Some keys are specific to MCEIR V1.0 or V2.0...
#define REMOTEKEY_YELLOW	  0x7ba2
#define REMOTEKEY_GREEN		  0x7ba3
#define REMOTEKEY_RED		    0x7ba4
#define REMOTEKEY_TELETEXT  0x7ba5
#define REMOTEKEY_RADIO		  0x7baf
#define REMOTEKEY_PRINT		  0x7bb1
#define REMOTEKEY_VIDEOS	  0x7bb5
#define REMOTEKEY_PICTURES  0x7bb6
#define REMOTEKEY_RECTV		  0x7bb7
#define REMOTEKEY_MUSIC		  0x7bb8
#define REMOTEKEY_TV		    0x7bb9
#define REMOTEKEY_GUIDE		  0x7bd9
#define REMOTEKEY_LIVETV	  0x7bda
#define REMOTEKEY_DVDMENU	  0x7bdb
#define REMOTEKEY_BACK		  0x7bdc
#define REMOTEKEY_OK		    0x7bdd
#define REMOTEKEY_RIGHT     0x7bde
#define REMOTEKEY_LEFT      0x7bdf
#define REMOTEKEY_DOWN      0x7be0
#define REMOTEKEY_UP        0x7be1
#define REMOTEKEY_STAR      0x7be2
#define REMOTEKEY_POUND     0x7be3
#define REMOTEKEY_REPLAY    0x7be4
#define REMOTEKEY_SKIP      0x7be5
#define REMOTEKEY_STOP      0x7be6
#define REMOTEKEY_PAUSE     0x7be7
#define REMOTEKEY_RECORD    0x7be8
#define REMOTEKEY_PLAY      0x7be9
#define REMOTEKEY_REWIND    0x7bea
#define REMOTEKEY_FORWARD   0x7beb
#define REMOTEKEY_CHDOWN    0x7bec
#define REMOTEKEY_CHUP      0x7bed
#define REMOTEKEY_VOLDOWN   0x7bee
#define REMOTEKEY_VOLUP     0x7bef
#define REMOTEKEY_DETAILS   0x7bf0
#define REMOTEKEY_MUTE      0x7bf1
#define REMOTEKEY_EHOME     0x7bf2
#define REMOTEKEY_PCPWR     0x7bf3
#define REMOTEKEY_ENTER     0x7bf4
#define REMOTEKEY_ESCAPE    0x7bf5
#define REMOTEKEY_9         0x7bf6
#define REMOTEKEY_8         0x7bf7
#define REMOTEKEY_7         0x7bf8
#define REMOTEKEY_6         0x7bf9
#define REMOTEKEY_5         0x7bfa
#define REMOTEKEY_4         0x7bfb
#define REMOTEKEY_3         0x7bfc
#define REMOTEKEY_2         0x7bfd
#define REMOTEKEY_1         0x7bfe
#define REMOTEKEY_0         0x7bff

#define BLASTER_BOTH    0
#define BLASTER_1       1
#define BLASTER_2       2

#define SPEED_NONE      0
#define SPEED_FAST      1
#define SPEED_MEDIUM    2
#define SPEED_SLOW      3

#define TYPE_MICROSOFT  0
#define TYPE_SMK        1

BOOL WINAPI MceIrRegisterEvents(HWND hWnd);
BOOL WINAPI MceIrUnregisterEvents();
BOOL WINAPI MceIrSetRepeatTimes(DWORD FirstRepeat, DWORD NextRepeats);
BOOL WINAPI MceIrRecordToFile(HANDLE hFile, DWORD Timeout);
BOOL WINAPI MceIrPlaybackFromFile(HANDLE hFile);
BOOL WINAPI MceIrSuspend();
BOOL WINAPI MceIrResume();
BOOL WINAPI MceIrCheckFile(HANDLE hFile);
BOOL WINAPI MceIrSelectBlaster(DWORD PortNumber);
BOOL WINAPI MceIrSetBlasterSpeed(DWORD Speed);
BOOL WINAPI MceIrSetBlasterType(DWORD Type);

#ifdef cplusplus
}
#endif

#endif //MCEIR