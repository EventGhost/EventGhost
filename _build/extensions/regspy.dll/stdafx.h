// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//
/*
#pragma once

#define WIN32_LEAN_AND_MEAN		// Exclude rarely-used stuff from Windows headers
// Windows Header Files:
#include <windows.h>
*/
// TODO: reference additional headers your program requires here

/////////////////////////////////////////////////////////////////////////////
// $Id: stdafx.h 424 2008-05-23 14:46:44Z Bitmonster $
/////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2002 John Adcock.  All rights reserved.
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

#if !defined(REGSPYDLL_STDAFX_H__INCLUDED_)
#define REGSPYDLL_STDAFX_H__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#define VC_EXTRALEAN
#include <afxwin.h>
#include <afxext.h>
#include <afxcmn.h>

#include <atlbase.h>

// Windows Header Files:
#include <windowsx.h>

#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <io.h>
#include <fcntl.h>
#include <commctrl.h>
#include <sys/timeb.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <ddraw.h>
#include <process.h>
#include <math.h>
#include <mmsystem.h>
#include <vfw.h>
#include <winioctl.h>
#include "../DScaler/ErrorBox.h"
#include "DSDrv.h"
#include "HtmlHelp.H"
#include <vector>
#include <string>

// fix for including external header with IDC_STATIC defined
#ifdef IDC_STATIC
#undef IDC_STATIC
#endif

using namespace std;


//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif