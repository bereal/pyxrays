from pyxrays.cHandler import create_profiler

def runctx(statement, globs, locs, filename):
    """Run statement under profiler, supplying your own globals and locals,
    optionally saving results in filename.
    """
    prof = create_profiler(filename)
    try:
        prof.runctx(statement, globs, locs)
    except SystemExit:
        pass

    prof.close()
    
