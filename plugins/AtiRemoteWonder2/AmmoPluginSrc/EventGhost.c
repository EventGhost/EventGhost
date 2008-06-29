/*
 * File:		EventGhost.c
 *
 * Purpose:		Plug-In for ATI Remote Wonder II. Used to 
 *				forward all keypresses to EventGhost.
 *
 * Author:		EventGhost Project
 *
 * Copyright:	Copyright (c) 2008 EventGhost Project
 *
 */

#include <windows.h>
#include <stdio.h>
#include "ammo.h"				// Required for ATI Remote Wonder plug-in SDK API

static WORD wLastKeyEvent = -1;
static WORD wInstanceNum = 0;

/*
 * Function:	WhatKeysDoYouWant
 *
 * Purpose:		Determines what groups of keys should be re-directed to
 *				the plug-in.
 *
 * Inputs:		None
 *
 * Returns:		A bit mask which indicates the groups of keys that should
 *				be re-directed to this plug-in.
 *
 * When called: This function is called once when the plug-in is first loaded,
 *				and again after calling Configure().
 */
DWORD WhatKeysDoYouWant (void)
{
	return CUSTOM_RAW|MOUSE_GROUP|CHANNEL_GROUP|VOLUME_GROUP|NUMBER_GROUP
		|CURSOR_GROUP|PLAY_GROUP|MENU|SETUP|ENTER|RECORD|STOPWATCH|RESIZE
		|WEB_LAUNCH|HELP|INFO|POWER|BOOK|ATI|APP_GROUP;
}


/*
 * Function:	UseWhenNotInFocus
 *
 * Purpose:		Determines if the plug-in can be used when it is not
 *				in focus.
 *
 * Inputs:		
 *
 * Returns:		TRUE to indicate the plug-in can be used when it is
 *				not in focus, FALSE if it can not be used.
 */
BOOL UseWhenNotInFocus (void)
{
	return TRUE;
}


/*
 * Function:	EnumerateProgrammableFunction
 *
 * Purpose:		Enumerate the descriptions of the programamble
 *				functions provided by this plug-in.
 *
 * Inputs:		wIndex - index of requested description
 *
 * Returns:		Pointer to the programmable function description
 *				or NULL if wIndex is greater than the number of
 *				programmable functions provided by this plug-in.
 *
 * When called:	This function is called after any call to WhatKeysDoYouWant()
 *				that returns a request for custom mapped keys (CUSTOM_MAPPED).
 */
char *EnumerateProgrammableFunction (WORD wIndex)
{	
	return NULL;
}


/*
 * Function:	Configure
 *
 * Purpose:		Displays any configuration/setup page required by
 *				this plug-in. 
 *
 * Inputs:		hWnd - handle to the parent window. The parent window
 *				is used to ensure correct modal behaviour when creating 
 *				dialog and message boxes in this plug-in.
 *
 * Returns:		None
 *
 * When called: This function is called when the "Configure" button in the
 *				ATI Remote Wonder software is pressed.
 */
void Configure (HANDLE hWnd)
{
	// Display an 'About' message box
	MessageBox(hWnd, "EventGhost Plug-In Version 1.0", "About", MB_OK);	
}


/*
 * Function:	AreYouInFocus
 *
 * Purpose:		Determines if this plug-in is currently in-focus.
 *
 * Inputs:		None
 *
 * Returns:		TRUE if the plug-in is currently in focus, FALSE
 *				otherwise.
 *
 * When called:	This function is called when a key event occurs that
 *				the plug-in has requested.
 */
int AreYouInFocus (void)
{
	return TRUE;
}


/*
 * Function:	HandleKey
 *
 * Purpose:		Handles remote control keys.
 *
 * Inputs:		bCustom   - TRUE if wKeyEvent has been mapped to a custom
 *						    programamble option.
 *				wKeyEvent - Remote control key code for button that was
 *							pressed.
 *				wState    - RMCTRL_KEY_ON, when button is first pressed
 *						    RMCTRL_KEY_REPEAT, when button is held down
 *						    RMCTRL_KEY_OFF, when button is released
 *
 * Returns:		TRUE if the plug-in handled the command, FALSE otherwise.
 *
 * When called: This function is called whenever a key event occurs that
 *				the plug-in has requested when the plug-in is in focus.
 */
BOOL HandleKey (BOOL bCustom, WORD wKeyEvent, WORD wState)
{
	HWND hEventGhost;
	
	switch(wState)
	{
		case RMCTRL_KEY_ON:
			// Mouse movements generate repated RMCTRL_KEY_ON events. We suppress 
			// them here.
			if(wKeyEvent == wLastKeyEvent && wKeyEvent >= 15 && wKeyEvent <= 22)
				return TRUE;
			wLastKeyEvent = wKeyEvent;
			break;
		case RMCTRL_KEY_OFF:
			wLastKeyEvent = -1;
			break;
		default:
			// we are not interested in other states, so we take a quick exit
			return TRUE;
	}
	// Find the EventGhost message window.
	hEventGhost = FindWindow(NULL, "EventGhost Message Receiver");
	if(hEventGhost != NULL)
	{
		// And if found send the key event to EventGhost
		PostMessage(hEventGhost, 0x8123+wInstanceNum, wKeyEvent, wState);
	}
	return TRUE;	
}


BOOL WINAPI DllMain (HINSTANCE hInst, DWORD dwReason, LPVOID lpvReserved)
{
	char myPath[MAX_PATH] = "";
	DWORD strLength = GetModuleFileName(hInst, myPath, MAX_PATH);
	if(isdigit(myPath[strLength-5]))
	{
		wInstanceNum = ((int) myPath[strLength-5]) - 48;
	}
	return 1;
}
