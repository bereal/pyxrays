from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
#from Cython.Build import  cythonize

setup(
    name = "Pyxrays",
    packages = ["pyxrays"],
    cmdclass = {'build_ext': build_ext},
    scripts = ['scripts/pyxrays'],
    ext_modules = [Extension('pyxrays.cHandler',
                             ['pyxrays/cHandler.pyx'],
                             extra_compile_args = ['-O3', '-Wall'])]
)
