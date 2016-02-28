/////////////////////////////////////////////////////////////////////////////
// $Id: regspydll.h 424 2008-05-23 14:46:44Z Bitmonster $
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

#if !defined(regspydll_h__INCLUDED_)
#define regspydll_h__INCLUDED_

#ifdef REGSPYDLL_EXPORTS
#define REGSPYDLL_API __declspec(dllexport)
#else
#define REGSPYDLL_API __declspec(dllimport)
#endif

#include "../RegSpy/resource.h"
#include "../DScaler/HardwareDriver.h"
#include "../RegLog/GenericCard.h"
extern "C" {

REGSPYDLL_API CHardwareDriver* GetDriver(void);
REGSPYDLL_API void DeleteDriver(CHardwareDriver* driver);
REGSPYDLL_API CGenericCard* OpenCard(
	CHardwareDriver* Driver, WORD VendorID, WORD DeviceID, int DeviceIndex);
REGSPYDLL_API DWORD ReadDword(CGenericCard* card, DWORD offset);
REGSPYDLL_API void WriteDword(CGenericCard* card, DWORD offset, DWORD value);
REGSPYDLL_API void DeleteCard(CGenericCard* card);

}

#endif