extern void ErrorExit(LPTSTR lpszFunction);
extern void dbgprint(const char *fmt, ...);

//#define DEBUG

#ifdef DEBUG
	#define DBG dbgprint
#else
	#define DBG(args) 
#endif

#define RAISE_SYSTEMERR(msg) {PyErr_SetString(PyExc_SystemError, msg); return NULL;}
