#ifndef __ALFRONT_H__
#define __ALFRONT_H__
/*
** Album List for Winamp frontend control API documentation v1.2.
** By Safai Ma.
** Copyright (C) 1999-2002
** Last updated: FEB.03.2002.
**
** Most of the stuff here are the same as using Winamp's frontend
** so that the learning curve is kept to the minimum.
**
** Introduction
** -----------------------
** This file describes a means to easily communicate to Album List
** via the classic Win32 Message API.
**
** These definitions/code assume C/C++. Porting to VB/Delphi shouldn't
** be too hard.
**
** First, you find the HWND of the Album List main window.
**
** HWND hwnd_albumlist = FindWindow("Winamp AL",NULL);
**
** Once you have the hwnd_albumlist, it's a good idea to check the version
** number. To do this, you send a WM_AL_IPC message to hwnd_albumlist.
** Note that WM_AL_IPC is defined as Win32's WM_USER.
**
** Note that sometimes you might want to use PostMessage instead of
** SendMessage.
**
** Requirements
** -----------------------
** You will need to have at least Album List 1.35 to use these functions
**
**
**
** From v2.0 and up
** To access other profile apart from profile 0, you can use the follow
** syntax:
**
** ret = SendMessage(hwnd_albumlist,WM_AL_IPC,MAKELONG(IPC_xxxxx,profile_x),xxxx);
*/

#define WM_AL_IPC WM_USER

/**************************************************************************/

#define IPC_GETVERSION 0

/* (requires AL 1.36+)
** DWORD version = SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_GETVERSION,0);
**
** Version will be 0xaabb00cc for Album List aa.bb.cc (major.minor.build)
**                (0x01230024)               (1.35.36)
**
** The basic format for sending messages to Winamp is:
** int result=SendMessage(hwnd_albumlist,WM_AL_IPC,command_data,command);
** (for the version check, command_data is 0).
*/

#define IPC_PLAYALBUM 100

/*
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_PLAYALBUM,album_index);
**
** You can use IPC_PLAYALBUM to play a particular album in the list.
** album_index is zero based.
** Returns TRUE if successful, FALSE otherwise.
*/

#define IPC_GETALBUMSIZE 101

/* (requires AL 1.36+)
** int size = SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_GETALBUMSIZE,0);
**
** You can use IPC_GETALBUMSIZE to get the number of albums in the list.
** Returns number of albums in the list.
*/

#define IPC_PLAYRANDOMALBUM 102

/* (requires AL 1.36+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_PLAYRANDOMALBUM,0);
**
** You can use IPC_PLAYRANDOMALBUM to a random album.
** Returns TRUE if successful, FALSE otherwise.
*/

#define IPC_GETALBUMNAME 103

/* (requires AL 1.36+, only usable from plug-ins (not external apps))
** char *name = (char*)SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_GETALBUMNAME,album_index);
**
** You can use IPC_GETALBUMNAME to get the name of a particular album.
** This is the same thing that is displayed (Artist - Title)
** returns a pointer to it. returns NULL on error.
*/

#define IPC_GETALBUMINDEX 104
/* (requires AL 1.36+)
** int album_index = SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_GETALBUMINDEX,0);
**
** You can use IPC_GETALBUMINDEX to get the current album index
** 0 based. -1 means none selected.
** returns album index.
*/

#define IPC_GETALBUMYEAR 105
/* (requires AL 1.36+)
** int album_year = SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_GETALBUMYEAR,album_index);
**
** You can use IPC_GETALBUMYEAR to get the album's year (if available)
** returns album's year.
*/

#define IPC_GETALBUMTITLE 106
/* (requires AL 1.36+, only usable from plug-ins (not external apps))
** char *title = (char*)SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_GETALBUMTITLE,album_index);
**
** You can use IPC_GETALBUMTITLE to get the album's title
** returns album's title.
*/

#define IPC_GETALBUMARTIST 107
/* (requires AL 1.36+, only usable from plug-ins (not external apps))
** char *artist = (char*)SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_GETALBUMARTIST,album_index);
**
** You can use IPC_GETALBUMARTIST to get the album's artist namef
** returns album's artist name.
*/

#define IPC_PLAYALBUM1		108
#define IPC_GETALBUMNAME1	109
#define IPC_GETALBUMINDEX1	110
#define IPC_GETALBUMYEAR1	111
#define IPC_GETALBUMTITLE1	112
#define IPC_GETALBUMARTIST1	113
/* (requires AL 1.37+, most only usable from plug-ins (not external apps))
** these work the same as their other COUNTERPART (the one without the "1" appended)
** the only difference is that these take a 1-based index instead of a 0-based index
*/

#define IPC_PLAYPREVALBUM	114
/* (requires AL 1.41+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_PLAYPREVALBUM,0);
**
** You can use IPC_PLAYPREVALBUM to play the next album in the list.
** Returns TRUE if successful, FALSE otherwise.
*/

#define IPC_PLAYNEXTALBUM	115
/* (requires AL 1.41+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_PLAYNEXTALBUM,0);
**
** You can use IPC_PLAYNEXTALBUM to play the next album in the list.
** Returns TRUE if successful, FALSE otherwise.
*/

#define IPC_PLAYALLALBUMS	116
/* (requires AL 1.41+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_PLAYALLALBUMS,0);
**
** You can use IPC_PLAYALLALBUMS to play all albums in the list.
** Returns TRUE if successful, FALSE otherwise.
*/

#define IPC_ENQUEUEALBUM	117
#define IPC_ENQUEUEALBUM1	118

/* (requires AL 1.43+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_ENQUEUEALBUM,album_index);
**
** You can use IPC_ENQUEUEALBUM to enqueue a particular album in the list.
** album_index is zero based.
** Returns TRUE if successful, FALSE otherwise.
**
** IPC_ENQUEUEALBUM1 is the 1-based index version of IPC_ENQUEUEALBUM
*/

#define IPC_SHOWHIDE		119
/* (requires AL 2.0+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_SHOWHIDE,0);
**
** Toggles Album List
*/

#define IPC_PLAYPREVALBUMARTIST	120
/* (requires AL 2.0+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_PLAYPREVALBUMARTIST,0);
**
** You can use IPC_PLAYPREVALBUMARTIST to play the next album (same artist) in the list.
** Returns TRUE if successful, FALSE otherwise.
*/

#define IPC_PLAYNEXTALBUMARTIST	121
/* (requires AL 2.0+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_PLAYNEXTALBUMARTIST,0);
**
** You can use IPC_PLAYNEXTALBUMARTIST to play the next album (same artist) in the list.
** Returns TRUE if successful, FALSE otherwise.
*/

#define IPC_JUMPTOALBUM		122
/* (requires AL 2.0+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_JUMPTOALBUM,0);
**
** You can use IPC_JUMPTOALBUM to bring up the 'Jump to Album' dialog.
** Returns TRUE if successful, FALSE otherwise.
*/

#define IPC_SHOWHIDE_CUR	123
#define IPC_JUMPTOALBUM_CUR	124
#define IPC_PLAYPREVALBUM_CUR	125
#define IPC_PLAYNEXTALBUM_CUR	126
#define IPC_PLAYPREVALBUMARTIST_CUR	127
#define IPC_PLAYNEXTALBUMARTIST_CUR	128
#define IPC_PLAYRANDOMALBUM_CUR	129
/* (requires AL 2.0+)
** same functions as above, but goes to the current profile
*/

#define IPC_COVER_VIEW		130
#define IPC_COVER_VIEW_CUR	131
/* (requires AL 2.0+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_COVER_VIEW,0);
**
** Use this to switch to cover view
*/

#define IPC_LIST_VIEW		132
#define IPC_LIST_VIEW_CUR	133
/* (requires AL 2.0+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_LIST_VIEW,0);
**
** Use this to switch to list view
*/

#define IPC_PLAYALLALBUMS_CUR	134
#define IPC_PLAYALBUM_CUR		135
#define IPC_GETALBUMSIZE_CUR	136
#define IPC_PLAYALBUM1_CUR		137
#define IPC_GETALBUMINDEX_CUR	138
/* (requires AL 2.01+)
** same functions as above, but goes to the current profile
*/

#define IPC_SHOWPREFERENCE		139
#define IPC_SHOWPREFERENCE_CUR	140
/* (requires AL 2.01+)
** SendMessage(hwnd_albumlist,WM_AL_IPC,IPC_SHOWPREFERENCE,0);
**
** Use this to show the preference page
*/

// (requires AL 2.0+)
// add custom stuff to album list
//
//	addStruct a = { "My Menu Entry", ADD_TYPE_MENU, hMyWnd, uMyMsg };
//
//	int genal_add_ipc = wndWinamp.SendIPCMessage((WPARAM)&"GenAlbumListAdd",IPC_REGISTER_WINAMP_IPCMESSAGE);
//	if (genal_add_ipc > 65536)
//	{
//		PostMessage(winampWindow,WM_WA_IPC,(WPARAM)&a,genal_add_ipc);
//	}
//
// the albuminfoStruct will be sent as WPARAM to hMyWnd with uMyMsg
// the structure and the pointers inside the structure are temporary
// and should NOT be stored, make a copy instead before leaving the
// message processing.

// addStruct flags
#define ADD_TYPE_MENU	1

typedef struct {
  char *name;       // this is the name that will appear in the menu
  DWORD flags;      // see above flags
  HWND wnd;         // set the HWND to send message (or 0 for the main winamp window)
  UINT uMsg;        // message that will be sent (must always be !=NULL)

} addStruct;

typedef struct {
  LPCTSTR title;    // display title (artist - album)
  LPCTSTR artist;   // artist name
  LPCTSTR album;    // album name
  LPCTSTR path;     // directory or m3u pathname
  int	  year;		// year
  int	  tracks;	// # of tracks

} albuminfoStruct;


#endif /* __ALFRONT_H__ */
