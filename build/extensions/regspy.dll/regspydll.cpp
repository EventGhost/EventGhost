/////////////////////////////////////////////////////////////////////////////
// $Id: regspydll.cpp 424 2008-05-23 14:46:44Z Bitmonster $
/////////////////////////////////////////////////////////////////////////////
//
//  This file is subject to the terms of the GNU General Public License as
//  published by the Free Software Foundation.  A copy of this license is
//  included with this software distribution in the file COPYING.  If you
//  do not have a copy, you may obtain a copy by writing to the Free
//  Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
//
//  This software is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details
/////////////////////////////////////////////////////////////////////////////
//
// A simple DLL exporting functions for reading and writing 
// registers on a tv tuner card. Based on RegSpy.cpp.

#include "stdafx.h"
#include "regspydll.h"
#include "../RegLog/GenericCard.h"

// Get a driver needed by OpenCard, or NULL if it fails to load.
REGSPYDLL_API CHardwareDriver* GetDriver(void){
	CHardwareDriver* driver = new CHardwareDriver();
	if (driver->LoadDriver() == TRUE)
	{
		return driver;
	} else {
		delete driver;
		return NULL;
	}
}

// You must clean up the driver when you are done.
REGSPYDLL_API void DeleteDriver(CHardwareDriver* driver){
	driver->UnloadDriver();
	delete driver;
}

// Get an open card that you can read from
// or NULL if the card doesn't exit or can't be opened.
REGSPYDLL_API CGenericCard* OpenCard(
	CHardwareDriver* driver, WORD vendorId, WORD deviceId, int deviceIndex)
{
	DWORD subSystemId;
	if (driver->DoesThisPCICardExist(
			vendorId, deviceId, deviceIndex, subSystemId) == TRUE)
	{
		static CGenericCard* card = new CGenericCard(driver);
		if(card->OpenPCICard(vendorId, deviceId, deviceIndex) == TRUE)
		{
			return card;
		}else{
			delete card;
			return NULL;
		}
	} else {
		return NULL;
	}
}

// Read a Dword from one of the card's registers
REGSPYDLL_API DWORD ReadDword(CGenericCard* card, DWORD offset){
	return card->ReadDword(offset);
}

// Read a Dword from one of the card's registers
REGSPYDLL_API void WriteDword(CGenericCard* card, DWORD offset, DWORD value){
	return card->WriteDword(offset, value);
}

// You must clean up the card when you are done.
REGSPYDLL_API void DeleteCard(CGenericCard* card){
	delete card;
}

///////////////////////////////////////////////////////////////////////////////
// From RegSpy.cpp: This load of junk required so that we can link with
// some of the Dscaler files
///////////////////////////////////////////////////////////////////////////////

void __cdecl LOG(int , LPCSTR, ...)
{
}

HWND hWnd = NULL;

void __cdecl HideSplashScreen()
{
}

extern "C"
{
    long gBuildNum = 0;
}

void __cdecl OSD_Redraw(struct HWND__ *,struct HDC__ *)
{
}

void __cdecl OSD_ShowTextPersistent(struct HWND__ *,char const *,double)
{
}

void __cdecl OSD_ProcessDisplayUpdate(struct HDC__ *,struct tagRECT *)
{
}

int __cdecl GetDisplayAreaRect(struct HWND__ *,struct tagRECT *, BOOL)
{
    return FALSE;
}

void __cdecl OSD_ShowTextPersistent(char const *,double)
{
}