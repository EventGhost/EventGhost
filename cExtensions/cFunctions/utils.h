extern void ErrorExit(LPTSTR lpszFunction);
extern void print(const char *fmt, ...);

//#define DEBUG(args) print(args)
#define DEBUG(args) 

#define RAISE_SYSTEMERR(msg) {PyErr_SetString(PyExc_SystemError, msg); return NULL;}
