#ifndef IRDEC
#define IRDEC

#ifdef cplusplus
extern "C" {
#endif

void TraceOut(LPSTR szFormat, ...);
void MceIrDecode(PUCHAR pIrData, DWORD IrCount);
void MceIrDecodeVista(DWORD *pData, DWORD len);

#ifdef cplusplus
}
#endif

#endif //IRDEC