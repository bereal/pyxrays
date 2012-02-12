import sys, os

from optparse import OptionParser
from cython.parallel import threadid
from libc.stdio cimport FILE, fprintf, fopen, fclose, printf, sprintf
from libc.string cimport strerror

cdef extern from "errno.h":
    int errno

cdef extern from *:
    ctypedef char* const_char_ptr "const char*"
         
cdef class EventHandler:
    cdef FILE * _file
    cdef int _retcount
    
    def __init__(self, output):
        self._file = fopen(<char *>output, "w")
        self._retcount = 0
    
    def __call__(self, frame, event, arg):
        if event == "call":
            code = frame.f_code
            fprintf(<FILE *>self._file, "%s\t1\t%s\t%s\t%i\n",
                     <int>self._retcount,
                     <const_char_ptr>code.co_name,
                     <const_char_ptr>code.co_filename,
                     <int>code.co_firstlineno)
            self._retcount = 0
        elif event == "return":
            self._retcount += 1

        return self
            
    def close(self):
        fclose(self._file)


class DispatchHandler(object):
    def __init__(self, constructor):
        self._constructor = constructor
        self._handlers = dict()

        
    def __call__(self, frame, event, arg):
        tid = threadid()
        handler = self._handlers.get(tid)
        if not handler:
            handler = self._constructor(tid)
            self._handlers[tid] = handler
            
        return handler(frame, event, arg)


    def runctx(self, cmd, globs, locs):
        sys.setprofile(self)
        try:
            exec cmd in globs, locs
        finally:
            print "Exiting"
            sys.setprofile(None)


    def close(self):
        for e in self._handlers.values():
            e.close()

        self._handlers.clear()
            
        

def create_profiler(basedir = None):
    basedir = basedir or os.getcwd()
    def make_handler(tid):
        path = os.path.join(basedir, '%s.txt' % tid)
        return EventHandler(path)
    
    return DispatchHandler(make_handler)
            
