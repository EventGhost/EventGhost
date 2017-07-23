extern void ErrorExit(LPTSTR lpszFunction);
extern void DBG(const char *fmt, ...);

//#define DEBUG

#define RAISE_SYSTEMERR(msg) {PyErr_SetString(PyExc_SystemError, msg); return NULL;}
