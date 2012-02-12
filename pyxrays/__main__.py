import os
import sys
import errno
from optparse import OptionParser

from pyxrays.profiler import runctx
    
def main():
    usage = "%s [-o output_file_path] [-s sort] scriptfile [arg] ..." % sys.argv[0]
    parser = OptionParser(usage=usage)
    parser.allow_interspersed_args = False
    parser.add_option('-o', '--outdir', dest="outdir",
        help="Save report to <outdir>", default=os.getcwd())


    if not sys.argv[1:]:
        parser.print_usage()
        sys.exit(2)

    (options, args) = parser.parse_args()
    sys.argv[:] = args

    if len(args) > 0:
        progname = args[0]
        sys.path.insert(0, os.path.dirname(progname))
        with open(progname, 'rb') as fp:
            code = compile(fp.read(), progname, 'exec')
        globs = {
            '__file__': progname,
            '__name__': '__main__',
            '__package__': None,
        }

        try:
            os.makedirs(options.outdir)
        except OSError, e:
            if e.errno != errno.EEXIST: raise
            
        runctx(code, globs, None, options.outdir)
    else:
        parser.print_usage()


if __name__=='__main__':
    main()
