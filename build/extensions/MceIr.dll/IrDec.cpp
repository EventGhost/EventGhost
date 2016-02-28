// MceIr.cpp : Defines the entry point for the DLL application.
//

#include "stdafx.h"
#include "MceIr.h"
#include "IrDec.h"

#if _DEBUG
#define Trace    TraceOut
#define Debug    TraceOut
#define DebugSONY
#define  DebugNEC
#define  DebugRC5
#define  DebugRC6
#define  DebugREC80
#else
#define Trace
#define Debug
#define DebugSONY  
#define DebugNEC
#define DebugRC5
#define DebugRC6
#define DebugREC80
#endif

#define PULSE_BIT         0x01000000
#define PULSE_MASK        0x00FFFFFF

#define MCE_TOGGLE_BIT    0x8000
#define MCE_TOGGLE_MASK   0x7FFF

#define RC5_TOGGLE_MASK   0xF7FF
#define RC5X_TOGGLE_MASK  0xFFFF

#define RC6_PREFIX_RC6    0x000FC950
#define RC6_PREFIX_RC6A   0x000FCA90

#define MCE_CUSTOMER_MICROSOFT    0x800F

#define TIMING_RESOLUTION   50  /* 50us */

typedef enum
{
    DETECT_HEADER_PULSE,
    DETECT_HEADER_SPACE,
    DETECT_PRE_DATA,
    DETECT_DATA,
    DETECT_KEYCODE,
    DETECT_LEADING
} DETECTION_STATE;

typedef struct _IR_DETECTION
{
    struct _IR_DETECTION  *pNext;
    DETECTION_STATE      DetectState;
    UCHAR          Bit;
    UCHAR          HalfBit;
    ULONG          Header;
    ULONG          Code;
    ULONG          LastCode;
    ULONG          LastTime;
    ULONG          RepeatCount;
    BOOL          LongPulse;
    BOOL          LongSpace;
} IR_DETECTION, * PIR_DETECTION;

//External variables
extern DWORD  KbdFirstRepeat;
extern DWORD  KbdNextRepeats;
extern HWND    hWndRegistered;

//Local functions
static void MceIrDetectSONY   (PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount);
static void MceIrDetectNEC    (PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount);
static void MceIrDetectRC5    (PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount);
static void MceIrDetectRC6    (PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount);
static void MceIrDetectREC80  (PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount);

IR_DETECTION RemoteSony = { NULL, DETECT_HEADER_PULSE, 0, 0, 0, 0, 0, 0, 0 };
IR_DETECTION RemoteNEC  = { NULL, DETECT_HEADER_PULSE, 0, 0, 0, 0, 0, 0, 0 };
IR_DETECTION RemoteRC5  = { NULL, DETECT_HEADER_PULSE, 0, 0, 0, 0, 0, 0, 0 };
IR_DETECTION RemoteRC6  = { NULL, DETECT_HEADER_PULSE, 0, 0, 0, 0, 0, 0, 0 };
IR_DETECTION RemoteREC80= { NULL, DETECT_HEADER_PULSE, 0, 0, 0, 0, 0, 0, 0 };

static DWORD LastLen    = 0;
static DWORD DataCount  = 0;
static DWORD Data[50]   = {0};

static void MceIrDecodeDWORD(DWORD *pIrData, DWORD IrCount)
{
    MceIrDetectSONY (&RemoteSony, pIrData, IrCount);
    MceIrDetectNEC  (&RemoteNEC,  pIrData, IrCount);
    MceIrDetectRC5  (&RemoteRC5,  pIrData, IrCount);
    MceIrDetectRC6  (&RemoteRC6,  pIrData, IrCount);
    MceIrDetectREC80(&RemoteREC80,pIrData, IrCount);
}

void MceIrDecode(PUCHAR pIrData, DWORD IrCount)
{
    DWORD      BulkIdx = 0;

    int KeyCode;
    int len = 0;

    if (!pIrData)
    {
        if (!LastLen)
            return;
        Data[0] = LastLen;
        DataCount = 1;
        LastLen = 0;
        Debug("MceIrDecode! sending LastLen=>%d\n", LastLen);
    }
#if _DEBUG
    {
        char tmp[512];
        DWORD i;
        tmp[0] = '\0';
        Debug("MceIrDecode! IrCount=>%d\n", IrCount);
        for (i = 0; i < IrCount; i++) {
            sprintf(tmp + strlen(tmp), "%02x ", pIrData[i]);
        }
        Debug("%s\n", tmp);
    }
#endif

    if ((DataCount - sizeof(Data)/sizeof(DWORD)) == 0) 
        return;

    while(BulkIdx < IrCount)
    {
        UCHAR Pulse = 0;

        KeyCode = pIrData[BulkIdx++];
        if (KeyCode & 0x80)
        {
            Pulse = 1;
            KeyCode -= 0x80;
        }
        
        if (Pulse)
            LastLen |= PULSE_BIT;
        if (KeyCode == 0x7f)
        {
            LastLen += KeyCode * TIMING_RESOLUTION;
        }
        else
        {
            Data[DataCount] = LastLen + KeyCode * TIMING_RESOLUTION;
            DataCount++;
            LastLen = 0;
        }
    }

    MceIrDecodeDWORD(Data, DataCount);

    DataCount = 0;
}

void MceIrDecodeVista(DWORD *pData, DWORD len)
{
    for (DWORD i = 0; i < len; i++)
    {
        if ((int)pData[i] < 0)
            pData[i] = (int)pData[i] * -1;
        else
            pData[i] |= PULSE_BIT;
    }
    MceIrDecodeDWORD(pData, len);
}

static void  MceIrDetectSONY(PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount)
{
    DWORD i;

    if (!Data)
    {
        pDetect->DetectState = DETECT_HEADER_PULSE;
        return;
    }

    for (i = 0 ; i < DataCount ; i++)
    {
        DWORD Duration = Data[i] & PULSE_MASK;
        BOOL Pulse = ((Data[i] & PULSE_BIT) != 0);
        BOOL Ignored = TRUE;
        switch(pDetect->DetectState)
        {
        case DETECT_HEADER_PULSE:
            if (Pulse && (Duration >= 2100) && (Duration <= 2700))
            {
                pDetect->DetectState = DETECT_HEADER_SPACE;
                Ignored = FALSE;
                DebugSONY("DETECT_HEADER_SPACE\n");
            }
            break;
        case DETECT_HEADER_SPACE:
            if (!Pulse && (Duration >= 500) && (Duration <= 700))
            {
                pDetect->DetectState = DETECT_DATA;
                Ignored = FALSE;
                pDetect->HalfBit = 0;
                pDetect->Bit = 0;
                pDetect->Code = 0;
                DebugSONY("DETECT_DATA\n");
            }
            break;
        case DETECT_DATA:
            if ((pDetect->HalfBit % 2) == 0)
            {
                if (!Pulse) break;

                if ((Duration >= 400) && (Duration <= 750))
                {
                    Ignored = FALSE;
                    pDetect->HalfBit = 1;
                    pDetect->Bit++;
                    DebugSONY("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                }
                else if ((Duration >= 1000) && (Duration <= 1300))
                {
                    Ignored = FALSE;
                    pDetect->HalfBit = 1;
                    pDetect->Code |= 1 << pDetect->Bit++;
                    DebugSONY("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                }
                else
                {
                    DebugSONY("Pulse error %d on bit %d\n", Duration, pDetect->Bit);
                }
                break;
            }
            else
            {
                if (Pulse) 
                    break;

                if ((Duration >= 400) && (Duration <= 750))
                {
                    Ignored = FALSE;
                    pDetect->HalfBit = 0;
                    DebugSONY("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                }
                else if ((Duration > 8000) &&
                    (pDetect->Bit == 8) || (pDetect->Bit == 12) || (pDetect->Bit == 15) || (pDetect->Bit == 20))
                {
                    Ignored = FALSE;
                    pDetect->DetectState = DETECT_KEYCODE;
                    i--;
                    DebugSONY("DETECT_KEYCODE code:%08X\n", pDetect->Code);
                }
                else
                {
                    DebugSONY("Space error %d on bit %d\n", Duration, pDetect->Bit);
                }
            }
            break;
        }
        if (pDetect->DetectState == DETECT_KEYCODE)
        {
            BOOL IsValid = FALSE;
            if (pDetect->LastCode != pDetect->Code)
            {
                IsValid = TRUE;
                pDetect->LastCode = pDetect->Code;
                pDetect->LastTime = GetTickCount();
                pDetect->RepeatCount = 0;
            }
            else if (KbdFirstRepeat &&
                (pDetect->LastTime + KbdFirstRepeat < GetTickCount()))
            {
                IsValid = TRUE;
                pDetect->LastTime = GetTickCount() + KbdNextRepeats - KbdFirstRepeat;
                pDetect->RepeatCount++;
            }

            pDetect->DetectState = DETECT_HEADER_PULSE;

            if (IsValid)
            {
                pDetect->Code &= 0x0000FFFF;
                Trace("GENERATE_SONY_KEYCODE code:%04X !!!\n", pDetect->Code);
                PostMessage(hWndRegistered, WM_USER, ID_SONY_KEYCODE, (pDetect->RepeatCount << 16) | pDetect->Code);
            }
        }
        if (Ignored && (pDetect->DetectState != DETECT_HEADER_PULSE))
        {
            pDetect->DetectState = DETECT_HEADER_PULSE;
            DebugSONY("DETECT_HEADER_PULSE\n");
        }
    }
}

static void  MceIrDetectNEC(PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount)
{
    DWORD i;

    if (!Data)
    {
        pDetect->DetectState = DETECT_HEADER_PULSE;
        return;
    }

    for (i = 0 ; i < DataCount ; i++)
    {
        DWORD Duration = Data[i] & PULSE_MASK;
        BOOL Pulse = ((Data[i] & PULSE_BIT) != 0);
        BOOL Ignored = TRUE;
        switch(pDetect->DetectState)
        {
        case DETECT_HEADER_PULSE:
            if (Pulse && (Duration >= 7900) && (Duration <= 9200))
            {
                pDetect->DetectState = DETECT_HEADER_SPACE;
                Ignored = FALSE;
                DebugNEC("DETECT_HEADER_SPACE\n");
            }
            break;
        case DETECT_HEADER_SPACE:
            if (!Pulse && (Duration >= 3800) && (Duration <= 4700))
            {
                pDetect->DetectState = DETECT_DATA;
                Ignored = FALSE;
                pDetect->HalfBit = 0;
                pDetect->Bit = 0;
                pDetect->Code = 0;
                DebugNEC("DETECT_PRE_DATA\n");
            }
            break;
        case DETECT_DATA:
            if ((pDetect->HalfBit % 2) == 0)
            {
                if (!Pulse) 
                    break;

                if ((Duration >= 450) && (Duration <= 700))
                {
                    Ignored = FALSE;
                    pDetect->HalfBit = 1;
                    DebugNEC("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                }
                else
                {
                    DebugNEC("Pulse error %d on bit %d\n", Duration, pDetect->Bit);
                }
                break;
            }
            else
            {
                if (Pulse) 
                    break;

                if ((Duration >= 350) && (Duration <= 600))
                {
                    Ignored = FALSE;
                    pDetect->HalfBit = 0;
                    pDetect->Bit++;
                    DebugNEC("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                }
                else if ((Duration >= 1200) && (Duration <= 2800))
                {
                    Ignored = FALSE;
                    pDetect->HalfBit = 0;
                    pDetect->Code |= 1 << pDetect->Bit++;
                    DebugNEC("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                }
                else if ((Duration > 10000) && (pDetect->Bit == 32))
                {
                    Ignored = FALSE;
                    i--;
                    pDetect->DetectState = DETECT_KEYCODE;
                    DebugNEC("DETECT_KEYCODE code:%08X\n", pDetect->Code);
                }
                else
                {
                    Trace("Space error %d on bit %d\n", Duration, pDetect->Bit);
                }
            }
            break;
        }
        if (pDetect->DetectState == DETECT_KEYCODE)
        {
            BOOL IsValid = FALSE;
            if ((HIBYTE(HIWORD(pDetect->Code)) + LOBYTE(HIWORD(pDetect->Code)) != 0xFF) ||
                (HIBYTE(LOWORD(pDetect->Code)) + LOBYTE(LOWORD(pDetect->Code)) != 0xFF))
            {
                Trace("Error checking failed for %08X !!!\n", pDetect->Code);
            }
            else if (pDetect->LastCode != pDetect->Code)
            {
                IsValid = TRUE;
                pDetect->LastCode = pDetect->Code;
                pDetect->LastTime = GetTickCount();
                pDetect->RepeatCount = 0;
            }
            else if (KbdFirstRepeat &&
                (pDetect->LastTime + KbdFirstRepeat < GetTickCount()))
            {
                IsValid = TRUE;
                pDetect->LastTime = GetTickCount() + KbdNextRepeats - KbdFirstRepeat;
                pDetect->RepeatCount++;
            }

            pDetect->DetectState = DETECT_HEADER_PULSE;

            if (IsValid)
            {
                pDetect->Code = (LOBYTE(LOWORD(pDetect->Code)) << 8) | LOBYTE(HIWORD(pDetect->Code));
                Trace("GENERATE_NEC_KEYCODE code:%04X !!!\n", pDetect->Code);
                PostMessage(hWndRegistered, WM_USER, ID_NEC_KEYCODE, (pDetect->RepeatCount << 16) | pDetect->Code);
            }
        }
        if (Ignored && (pDetect->DetectState != DETECT_HEADER_PULSE))
        {
            pDetect->DetectState = DETECT_HEADER_PULSE;
            DebugNEC("DETECT_HEADER_PULSE\n");
        }
    }
}

static void MceIrDetectRC5(PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount)
{
    DWORD i;

    if (!Data)
    {
        pDetect->DetectState = DETECT_HEADER_PULSE;
        return;
    }

    for (i = 0 ; i < DataCount ; i++)
    {
        DWORD Duration = Data[i] & PULSE_MASK;
        BOOL Pulse = ((Data[i] & PULSE_BIT) != 0);
        BOOL Ignored = TRUE;
        //DebugRC5("%s %d\n", Pulse ? "Pulse" : "Space", Duration);
        switch(pDetect->DetectState)
        {
        case DETECT_HEADER_PULSE:
            if (Pulse)
            {
                if ((Duration >= 750) && (Duration <= 1100))
                {
                    pDetect->DetectState = DETECT_HEADER_SPACE;
                    Ignored = FALSE;
                    DebugRC5("DETECT_HEADER_SPACE\n");
                    pDetect->Bit = 13;
                    pDetect->Code = 1 << pDetect->Bit;
                    DebugRC5("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                }
                else if ((Duration >= 1500) && (Duration <= 2000))
                {
                    pDetect->DetectState = DETECT_DATA;
                    Ignored = FALSE;
                    pDetect->Bit = 13;
                    pDetect->Code = 1 << pDetect->Bit;
                    pDetect->HalfBit = 0;
                    DebugRC5("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                    DebugRC5("DETECT_DATA\n");
                }
            }
            break;
        case DETECT_HEADER_SPACE:
            if (!Pulse && (Duration >= 750) && (Duration <= 1100))
            {
                pDetect->DetectState = DETECT_DATA;
                Ignored = FALSE;
                pDetect->HalfBit = 0;
                DebugRC5("DETECT_DATA\n");
            }
            break;
        case DETECT_DATA:
            if (pDetect->HalfBit == 0)
            {
                if (Pulse) 
                {
                    if (((Duration >= 750) && (Duration <= 1100)) ||
                        ((Duration >= 1500) && (Duration <= 2000)))
                    {
                        Ignored = FALSE;
                        pDetect->HalfBit = (Duration >= 1500) ? 0 : 1;
                        pDetect->Bit--;
                        pDetect->Code |= 1 << pDetect->Bit;
                        DebugRC5("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                        if ((pDetect->Bit == 0) ||
                            ((pDetect->Bit == 1) && (Duration >= 1500)))
                        {
                            pDetect->DetectState = DETECT_KEYCODE;
                            DebugRC5("DETECT_KEYCODE code:%08X\n", pDetect->Code);
                        }
                    }
                    else
                    {
                        DebugRC5("Pulse error %d on bit %d\n", Duration, pDetect->Bit);
                    }
                }
                else
                {
                    if (((Duration >= 750) && (Duration <= 1100)) ||
                        ((Duration >= 1500) && (Duration <= 2000)))
                    {
                        Ignored = FALSE;
                        pDetect->HalfBit = (Duration >= 1500) ? 0 : 1;
                        pDetect->Bit--;
                        DebugRC5("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                        if (pDetect->Bit == 0)
                        {
                            pDetect->DetectState = DETECT_KEYCODE;
                            DebugRC5("DETECT_KEYCODE code:%08X\n", pDetect->Code);
                        }
                    }
                    else if ((pDetect->Bit == 7) &&
                        (((Duration >= 4300) && (Duration <= 4700)) ||
                        ((Duration >= 5200) && (Duration <= 5600))))
                    {
                        Ignored = FALSE;
                        pDetect->HalfBit = (Duration >= 5200) ? 0 : 1;
                        pDetect->Code <<= 6;
                        pDetect->Bit += 5;
                        DebugRC5("DATA bit:%d code:%08X\n", pDetect->Bit, pDetect->Code);
                    }
                    else
                    {
                        DebugRC5("Space error %d on bit %d\n", Duration, pDetect->Bit);
                    }
                }
                break;
            }
            if ((Duration >= 750) && (Duration <= 1100))
            {
                Ignored = FALSE;
                pDetect->HalfBit = 0;
                if ((pDetect->Bit == 1) && (Pulse))
                {
                    pDetect->DetectState = DETECT_KEYCODE;
                    DebugRC5("DETECT_KEYCODE code:%08X\n", pDetect->Code);
                }
            }
            else if ((pDetect->Bit == 7) &&
                (((Duration >= 3400) && (Duration <= 3800)) ||
                ((Duration >= 4300) && (Duration <= 4700))))
            {
                Ignored = FALSE;
                pDetect->HalfBit = (Duration >= 4300) ? 0 : 1;
                pDetect->Code <<= 6;
                pDetect->Bit += 6;
            }
            else
            {
                Trace("Duration error %d on bit %d\n", Duration, pDetect->Bit);
            }
            break;
        case DETECT_LEADING:
            if (Pulse) 
                break;
            if (Duration > 10000)
            {
                pDetect->DetectState = DETECT_HEADER_PULSE;
                Ignored = FALSE;
            }
            break;
        }
        if (pDetect->DetectState == DETECT_KEYCODE)
        {
            BOOL IsValid = FALSE;
            if (pDetect->LastCode != pDetect->Code)
            {
                IsValid = TRUE;
                pDetect->LastCode = pDetect->Code;
                pDetect->LastTime = GetTickCount();
                pDetect->RepeatCount = 0;
            }
            else if (KbdFirstRepeat &&
                (pDetect->LastTime + KbdFirstRepeat < GetTickCount()))
            {
                IsValid = TRUE;
                pDetect->LastTime = GetTickCount() + KbdNextRepeats - KbdFirstRepeat;
                pDetect->RepeatCount++;
            }

            pDetect->DetectState = DETECT_LEADING;

            if (IsValid)
            {
                if (pDetect->Code > 0xFFFF)
                {
                    pDetect->Code &= RC5X_TOGGLE_MASK;
                }
                else
                {
                    pDetect->Code &= RC5_TOGGLE_MASK;
                }
                Trace("GENERATE_RC5_KEYCODE code:%04X !!!\n", pDetect->Code);
                PostMessage(hWndRegistered, WM_USER, ID_RC5_KEYCODE, (pDetect->RepeatCount << 16) | pDetect->Code);
            }
        }
        if (Ignored && (pDetect->DetectState != DETECT_LEADING) && (pDetect->DetectState != DETECT_HEADER_PULSE))
        {
            pDetect->DetectState = (Duration > 10000) ? DETECT_HEADER_PULSE : DETECT_LEADING;
            DebugRC5("DETECT_LEADING\n");
        }
    }
}

//WARNING: RC6 byphase encoding is inversed !
//I left this as it is... to avoid compatibility issues...
static void  MceIrDetectRC6(PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount)
{
    DWORD i;

    if (!Data)
    {
        DebugRC6("RC6 !Data => DETECT_HEADER_PULSE\n");
        pDetect->DetectState = DETECT_HEADER_PULSE;
        return;
    }

    for (i = 0 ; i < DataCount ; i++)
    {
        DWORD Duration = Data[i] & PULSE_MASK;
        BOOL Pulse = ((Data[i] & PULSE_BIT) != 0);
        BOOL Ignored = TRUE;
        DebugRC6("Data[%d]=0x%x: %s %d\n", i, Data[i], Pulse ? "Pulse" : "Space", Duration);
        switch(pDetect->DetectState)
        {
        case DETECT_HEADER_PULSE:
            if (Pulse && (Duration >= 2600) && (Duration <= 3300))
            {
                pDetect->DetectState = DETECT_HEADER_SPACE;
                pDetect->Header = 0x000FC000;
                pDetect->Bit = 12;
                pDetect->HalfBit = 0;
                pDetect->Code = 0;
                pDetect->LongPulse = FALSE;
                pDetect->LongSpace = FALSE;
                Ignored = FALSE;
                DebugRC6("RC6 DETECT_HEADER_SPACE\n");
            }
            break;
        case DETECT_HEADER_SPACE:
            if (!Pulse && (Duration >= 750) && (Duration <= 1000))
            {
                Ignored = FALSE;
                pDetect->DetectState = DETECT_PRE_DATA;
                DebugRC6("RC6 DETECT_PRE_DATA\n");
            }
            break;
        case DETECT_PRE_DATA:
            if (Pulse)
            {
                if ((Duration >= 300) && (Duration <= 600))
                {
                    Ignored = FALSE;
                    if (pDetect->Bit) pDetect->Header |= 1 << --pDetect->Bit;
                    DebugRC6("RC6 PRE_DATA bit:%d header:%08X\n", pDetect->Bit, pDetect->Header);
                }
                else if ((Duration >= 750) && (Duration <= 1000))
                {
                    Ignored = FALSE;
                    if (pDetect->Bit) pDetect->Header |= 1 << --pDetect->Bit;
                    if (pDetect->Bit) pDetect->Header |= 1 << --pDetect->Bit;
                    DebugRC6("RC6 PRE_DATA bit:%d header:%08X\n", pDetect->Bit, pDetect->Header);
                }
                else if ((Duration >= 1200) && (Duration <= 1600))
                {
                    Ignored = FALSE;
                    if (pDetect->Bit) pDetect->Header |= 1 << --pDetect->Bit;
                    if (pDetect->Bit) pDetect->Header |= 1 << --pDetect->Bit;
                    if (pDetect->Bit)
                    {
                        pDetect->Header |= 1 << --pDetect->Bit;
                    }
                    else
                    {
                        pDetect->HalfBit = 1;
                        pDetect->LongPulse = TRUE;
                    }
                    DebugRC6("RC6 PRE_DATA bit:%d header:%08X\n", pDetect->Bit, pDetect->Header);
                }
                else
                {
                    DebugRC6("RC6 Error Bit %d %s %d\n", pDetect->Bit, Pulse ? "Pulse" : "Space", Duration);
                }
            }
            else
            {
                if ((Duration >= 300) && (Duration <= 600))
                {
                    Ignored = FALSE;
                    pDetect->Bit--;
                    DebugRC6("RC6 PRE_DATA bit:%d header:%08X\n", pDetect->Bit, pDetect->Header);
                }
                else if ((Duration >= 750) && (Duration <= 1000))
                {
                    Ignored = FALSE;
                    if (pDetect->Bit > 2) pDetect->Bit -= 2; else pDetect->Bit = 0;
                    DebugRC6("RC6 PRE_DATA bit:%d header:%08X\n", pDetect->Bit, pDetect->Header);
                }
                else if ((Duration >= 1200) && (Duration <= 1600))
                {
                    Ignored = FALSE;
                    if (pDetect->Bit >= 3)
                    {
                        pDetect->Bit -= 3;
                    }
                    else
                    {
                        pDetect->HalfBit = 1;
                        pDetect->LongPulse = TRUE;
                        pDetect->Bit = 0;
                    }
                    DebugRC6("RC6 PRE_DATA bit:%d header:%08X\n", pDetect->Bit, pDetect->Header);
                }
                else
                {
                    DebugRC6("RC6 Error Bit %d %s %d\n", pDetect->Bit, Pulse ? "Pulse" : "Space", Duration);
                }
            }
            if ((Ignored == FALSE) && (pDetect->Bit == 0))
            {
                pDetect->DetectState = DETECT_DATA;
                DebugRC6("RC6 DETECT_DATA bit:%d header:%08X\n", pDetect->Bit, pDetect->Header);
            }
            break;
        case DETECT_DATA:
            if ((pDetect->HalfBit % 2) == 0)
            {
               DebugRC6("RC6 DETECT_DATA (pDetect->HalfBit %% 2) == 0)\n");
               if (Pulse && (Duration >= 300) && (Duration <= 600))
                {
                    Ignored = FALSE;
                    pDetect->LongPulse = TRUE;
                    pDetect->HalfBit++;
                    DebugRC6("RC6 DATA bit:%d code:%08X\n", pDetect->Bit, ~pDetect->Code);
                }
                else if (!Pulse && (Duration >= 300) && (Duration <= 600))
                {
                    Ignored = FALSE;
                    pDetect->LongSpace = TRUE;
                    pDetect->HalfBit++;
                    DebugRC6("RC6 DATA bit:%d code:%08X\n", pDetect->Bit, ~pDetect->Code);
                }
                else if (!Pulse && Duration > 4000)
                {
                    if (pDetect->Bit == 16 || pDetect->Bit == 20 || pDetect->Bit == 24 || pDetect->Bit == 32)
                        pDetect->DetectState = DETECT_KEYCODE;
                }
                break;
            }
            if (pDetect->LongPulse)
            {
               DebugRC6("RC6 DETECT_DATA (pDetect->LongPulse)\n");
                pDetect->LongPulse = FALSE;
                if (Pulse)
                {
                    DebugRC6("RC6 Error Pulse after LongPulse %d\n", Duration);
                    break;
                }
                if ((Duration >= 750) && (Duration <= 1000))
                {
                    Ignored = FALSE;
                    pDetect->Bit++;
                    pDetect->Code = pDetect->Code << 1;
                    pDetect->LongSpace = TRUE;
                    pDetect->HalfBit += 2;
                    DebugRC6("RC6 DATA bit:%d code:%08X\n", pDetect->Bit, ~pDetect->Code);
                }
                else if ((Duration >= 300) && (Duration <= 600))
                {
                    Ignored = FALSE;
                    pDetect->Bit++;
                    pDetect->Code = pDetect->Code << 1;
                    pDetect->HalfBit++;
                    DebugRC6("RC6 DATA bit:%d code:%08X\n", pDetect->Bit, ~pDetect->Code);
                }
                else if (Duration > 4000)
                {
                    Ignored = FALSE;
                    pDetect->Bit++;
                    pDetect->Code = pDetect->Code << 1;
                    pDetect->HalfBit++;
                    if (pDetect->Bit == 16 || pDetect->Bit == 20 || pDetect->Bit == 24 || pDetect->Bit == 32)
                        pDetect->DetectState = DETECT_KEYCODE;
                    DebugRC6("RC6 DATA bit:%d code:%08X\n", pDetect->Bit, ~pDetect->Code);
                }
            }
            else if (pDetect->LongSpace)
            {
               DebugRC6("RC6 DETECT_DATA (pDetect->LongSpace)\n");
                pDetect->LongSpace = FALSE;
                if (!Pulse)
                {
                    DebugRC6("RC6 Error Space after LongSpace %d\n",Duration);
                    break;
                }
                if ((Duration >= 750) && (Duration <= 1000))
                {
                    Ignored = FALSE;
                    pDetect->Bit++;
                    pDetect->Code = pDetect->Code << 1;
                    pDetect->Code |= 1;
                    pDetect->LongPulse = TRUE;
                    pDetect->HalfBit += 2;
                    DebugRC6("RC6 DATA bit:%d code:%08X\n", pDetect->Bit, ~pDetect->Code);
                }
                else if ((Duration >= 300) && (Duration <= 600))
                {
                    Ignored = FALSE;
                    pDetect->Bit++;
                    pDetect->Code = pDetect->Code << 1;
                    pDetect->Code |= 1;
                    pDetect->HalfBit++;
                    DebugRC6("RC6 DATA bit:%d code:%08X\n", pDetect->Bit, ~pDetect->Code);
                }
                else if (Duration > 4000)
                {
                    if (pDetect->Bit == 16 || pDetect->Bit == 20 || pDetect->Bit == 24 || pDetect->Bit == 32)
                        pDetect->DetectState = DETECT_KEYCODE;
                    DebugRC6("RC6 DATA bit:%d code:%08X\n", pDetect->Bit, ~pDetect->Code);
                }
            }
            break;
        }
        if (pDetect->DetectState == DETECT_KEYCODE)
        {
            DebugRC6("RC6  DETECT_KEYCODE\n");
            BOOL IsValid = FALSE;
            if (pDetect->LastCode != pDetect->Code)
            {
                IsValid = TRUE;
                pDetect->LastCode = pDetect->Code;
                pDetect->LastTime = GetTickCount();
                pDetect->RepeatCount = 0;
            }
            else if (KbdFirstRepeat &&
                (pDetect->LastTime + KbdFirstRepeat < GetTickCount()))
            {
                IsValid = TRUE;
                pDetect->LastTime = GetTickCount() + KbdNextRepeats - KbdFirstRepeat;
                pDetect->RepeatCount++;
            }

            pDetect->DetectState = DETECT_HEADER_PULSE;

            if (IsValid)
            {
                if ((~pDetect->Code >> 16) == MCE_CUSTOMER_MICROSOFT)
                {
                    pDetect->Code &= MCE_TOGGLE_MASK;
                }
                Trace("RC6 GENERATE_KEYCODE code:%04X !!!\n", (USHORT)~(pDetect->Code | 0x8000));
                PostMessage(hWndRegistered, WM_USER, ID_RC6_KEYCODE, (pDetect->RepeatCount << 16) | pDetect->Code);
            }
        }
        if (Ignored && (pDetect->DetectState != DETECT_HEADER_PULSE))
        {
            pDetect->DetectState = DETECT_HEADER_PULSE;
            DebugRC6("DETECT_HEADER_PULSE\n");
        }
    }
}

static void  MceIrDetectREC80(PIR_DETECTION pDetect, DWORD *Data, DWORD DataCount)
{
    DWORD i;

    if (!Data)
    {
        pDetect->DetectState = DETECT_HEADER_PULSE;
        return;
    }

    for (i = 0 ; i < DataCount ; i++)
    {
        DWORD Duration = Data[i] & PULSE_MASK;
        BOOL Pulse = ((Data[i] & PULSE_BIT) != 0);
        BOOL Ignored = TRUE;
        switch(pDetect->DetectState)
        {
        case DETECT_HEADER_PULSE:
            if (Pulse && (Duration >= 3300) && (Duration <= 4100))
            {
                pDetect->DetectState = DETECT_HEADER_SPACE;
                Ignored = FALSE;
                DebugREC80("DETECT_HEADER_SPACE\n");
            }
            break;
        case DETECT_HEADER_SPACE:
            if (!Pulse && (Duration >= 1400) && (Duration <= 1800))
            {
                pDetect->DetectState = DETECT_DATA;
                Ignored = FALSE;
                pDetect->HalfBit = 0;
                pDetect->Bit = 48;
                pDetect->Header = 0;
                pDetect->Code = 0;
                DebugREC80("DETECT_DATA\n");
            }
            break;
        case DETECT_DATA:
            if ((pDetect->HalfBit % 2) == 0)
            {
                if (!Pulse) break;

                if ((Duration >= 350) && (Duration <= 600))
                {
                    Ignored = FALSE;
                    pDetect->HalfBit = 1;
                    pDetect->Bit--;
                }
                break;
            }
            else
            {
                if (Pulse) 
                    break;

                if ((Duration >= 400) && (Duration <= 750))
                {
                    Ignored = FALSE;
                    pDetect->HalfBit = 0;
                    DebugREC80("DATA bit:%d header:%04X code:%08X\n", pDetect->Bit, pDetect->Header, pDetect->Code);
                }
                else if ((Duration >= 1100) && (Duration <= 1500))
                {
                    Ignored = FALSE;
                    pDetect->HalfBit = 0;
                    if (pDetect->Bit > 15)
                    {
                        pDetect->Header |= 1 << (pDetect->Bit - 16);
                    }
                    else
                    {
                        pDetect->Code |= 1 << pDetect->Bit;
                    }
                    DebugREC80("DATA bit:%d header:%04X code:%08X\n", pDetect->Bit, pDetect->Header, pDetect->Code);
                }
                else
                {
                    break;
                }
                if (pDetect->Bit == 0)
                {
                    pDetect->DetectState = DETECT_KEYCODE;
                    DebugREC80("REC80 DETECT_KEYCODE code:%08X\n", ~pDetect->Code);
                }
            }
            break;
        }
        if (pDetect->DetectState == DETECT_KEYCODE)
        {
            BOOL IsValid = FALSE;
            if (pDetect->LastCode != pDetect->Code)
            {
                IsValid = TRUE;
                pDetect->LastCode = pDetect->Code;
                pDetect->LastTime = GetTickCount();
                pDetect->RepeatCount = 0;
            }
            else if (KbdFirstRepeat &&
                (pDetect->LastTime + KbdFirstRepeat < GetTickCount()))
            {
                IsValid = TRUE;
                pDetect->LastTime = GetTickCount() + KbdNextRepeats - KbdFirstRepeat;
                pDetect->RepeatCount++;
            }

            pDetect->DetectState = DETECT_HEADER_PULSE;

            if (IsValid)
            {
                pDetect->Code &= 0x0000FFFF;
                Trace("GENERATE_REC80_KEYCODE code:%04X !!!\n", pDetect->Code);
                PostMessage(hWndRegistered, WM_USER, ID_REC80_KEYCODE, (pDetect->RepeatCount << 16) | pDetect->Code);
            }
        }
        if (Ignored && (pDetect->DetectState != DETECT_HEADER_PULSE))
        {
            pDetect->DetectState = DETECT_HEADER_PULSE;
            DebugREC80("DETECT_HEADER_PULSE\n");
        }
    }
}
