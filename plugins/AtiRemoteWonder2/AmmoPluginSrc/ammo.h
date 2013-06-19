/*
 * File:		AMMO.H
 *
 * Purpose:		Defines the ATI Remote Wonder plug-in key groups and key
 *				definitions.
 *
 * Author:		ATI
 *
 * Copyright:	Copyright (c) 2005 ATI Technologies Inc
 *
 */

#include <windows.h>

///////////////////////////////////////////////////////
// Function prototypes for plug-in
///////////////////////////////////////////////////////

DWORD	WhatKeysDoYouWant				(void);
char	*EnumerateProgrammableFunction	(WORD wIndex);
void	Configure						(HANDLE hWnd);
int		AreYouInFocus					(void);
BOOL	HandleKey						(BOOL bCustom, WORD wKeyEvent, WORD wState);
BOOL	UseWhenNotInFocus				(void);

///////////////////////////////////////////////////////
// Remote control key groups
///////////////////////////////////////////////////////

#define CUSTOM_RAW		0x000001	// A - F, sent raw
#define CUSTOM_MAPPED	0x000002	// A - F, remapped to custom commands
#define MOUSE_GROUP		0x000004	// 8 directions, left, right, and the hand
#define CHANNEL_GROUP	0x000008	// Channel Up, Channel Down
#define VOLUME_GROUP	0x000010	// Volume Up, Volume Down, Mute
#define NUMBER_GROUP	0x000020	// Numeric keys 0 - 9
#define CURSOR_GROUP	0x000040	// Up, Down, Left, Right
#define PLAY_GROUP		0x000080	// Fast Forward, Rewind, Play, Stop, Pause
#define MENU			0x000100	// Menu key
#define SETUP			0x000200	// Setup key
#define ENTER			0x000400	// Ok key
#define RECORD			0x000800	// Record key
#define STOPWATCH		0x001000	// Stopwatch key
#define RESIZE			0x002000	// Resize key
#define WEB_LAUNCH		0x004000	// WEB launch key (only for Remote Wonder)
#define HELP			0x008000	// Help key (only for Remote Wonder II)
#define INFO			0x010000	// INFO key (only for Remote Wonder II)
#define POWER			0x020000	// POWER key
#define BOOK			0x040000	// BOOK key (only for Remote Wonder)
#define ATI				0x080000	// ATI key (Remote Wonder II, Remote Wonder Plus)
#define APP_GROUP		0x100000	// TV, TV-2, DVD, FM, GUIDE

///////////////////////////////////////////////////////
// Key states
///////////////////////////////////////////////////////
#define RMCTRL_KEY_OFF					0
#define RMCTRL_KEY_ON					1
#define RMCTRL_KEY_REPEAT				2

///////////////////////////////////////////////////////
// Remote control key defintions
///////////////////////////////////////////////////////

// Numeric Keys
#define RMCTRL_0						0
#define RMCTRL_1						1
#define RMCTRL_2						2
#define RMCTRL_3						3
#define RMCTRL_4						4
#define RMCTRL_5						5
#define RMCTRL_6						6
#define RMCTRL_7						7
#define RMCTRL_8						8
#define RMCTRL_9						9

// Mouse keys
#define RMCTRL_HAND						10
#define RMCTRL_LEFTMOUSE				11
#define RMCTRL_RIGHTMOUSE				12
#define RMCTRL_LEFTMOUSEDOUBLECLICK		13
#define RMCTRL_RIGHTMOUSEDOUBLECLICK	14
#define RMCTRL_DIRPADRIGHT				15	
#define RMCTRL_DIRPADUP					16
#define RMCTRL_DIRPADLEFT				17
#define RMCTRL_DIRPADDOWN				18
#define RMCTRL_DIRPADRIGHTUP			19
#define RMCTRL_DIRPADRIGHTDOWN			20
#define RMCTRL_DIRPADLEFTUP				21
#define RMCTRL_DIRPADLEFTDOWN			22

// Channel Keys
#define RMCTRL_CHANNELUP				23
#define RMCTRL_CHANNELDOWN				24

// Volume Keys
#define RMCTRL_VOLUMEUP					25
#define RMCTRL_VOLUMEDOWN				26
#define RMCTRL_MUTE						27

// Menu Key
#define RMCTRL_MENU						28

// Setup Key
#define RMCTRL_SETUP					29

// Cursor Keys
#define RMCTRL_UP						30
#define	RMCTRL_DOWN						31
#define RMCTRL_LEFT						32
#define RMCTRL_RIGHT					33

// Enter (OK) Key
#define RMCTRL_ENTER					34

// Play Keys
#define RMCTRL_FF						35
#define RMCTRL_RW						36
#define RMCTRL_PLAY						37
#define RMCTRL_PAUSE					38
#define RMCTRL_STOP						39

// Record key
#define RMCTRL_RECORD					40

// Stopwatch key
#define RMCTRL_STOPWATCH				41

// Programmable Keys
#define RMCTRL_A						42
#define RMCTRL_B						43
#define RMCTRL_C						44
#define RMCTRL_D						45
#define RMCTRL_E						46
#define RMCTRL_F						47

// Resize key
#define RMCTRL_RESIZE					48

// Web launch key (only for Remote Wonder)
#define RMCTRL_WEB_LAUNCH				49

// Help key (only for Remote Wonder II)
#define RMCTRL_HELP						50

// Info key (only for Remote Wonder II)
#define RMCTRL_INFO						51

// Power key
#define RMCTRL_POWER					52

// Book key (only for Remote Wonder)
#define RMCTRL_BOOK						53

// ATI key (Remote Wonder II, Remote Wonder Plus)
#define RMCTRL_ATI						54

// Application Keys
#define RMCTRL_TV						55
#define RMCTRL_TV2						56
#define RMCTRL_FM						57
#define RMCTRL_DVD						58
#define RMCTRL_GUIDE					59


// end of "ammo.h"