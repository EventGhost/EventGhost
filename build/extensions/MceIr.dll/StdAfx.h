// stdafx.h : include file for standard system include files,
//  or project specific include files that are used frequently, but
//  are changed infrequently
//

#if !defined(AFX_STDAFX_H__90636EC0_CF3C_40B3_A080_823E34DF0F79__INCLUDED_)
#define AFX_STDAFX_H__90636EC0_CF3C_40B3_A080_823E34DF0F79__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

// Insert your headers here
#define WIN32_LEAN_AND_MEAN     // Exclude rarely-used stuff from Windows headers

#include <windows.h>
#include <stdio.h>
#include <malloc.h>
#include <setupapi.h>
//#pragma warning( disable : 4200 )

//#include <usbdi.h>
typedef struct _USB_DEVICE_DESCRIPTOR {
    UCHAR bLength;
    UCHAR bDescriptorType;
    USHORT bcdUSB;
    UCHAR bDeviceClass;
    UCHAR bDeviceSubClass;
    UCHAR bDeviceProtocol;
    UCHAR bMaxPacketSize0;
    USHORT idVendor;
    USHORT idProduct;
    USHORT bcdDevice;
    UCHAR iManufacturer;
    UCHAR iProduct;
    UCHAR iSerialNumber;
    UCHAR bNumConfigurations;
} USB_DEVICE_DESCRIPTOR, *PUSB_DEVICE_DESCRIPTOR;

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_STDAFX_H__90636EC0_CF3C_40B3_A080_823E34DF0F79__INCLUDED_)
