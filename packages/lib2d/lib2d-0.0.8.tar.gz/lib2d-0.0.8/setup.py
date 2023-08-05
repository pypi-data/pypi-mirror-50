""""Copyright (C) 2018  Joseph Marshall

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from setuptools import setup, Extension
import os, sys, re

sources = ['src/'+f for f in os.listdir('src') if f.endswith('.c')]
if sys.platform == 'win32':
    libs = ['opengl32']
else:
    if "src/python.c" in sources:
        # python.c is only needed by the windows build
        sources.remove("src/python.c")
    libs = ['GL', 'm']

native = Extension('_lib2d',
                    define_macros = [],
                    include_dirs = ['include', 'src'],
                    libraries = libs,
                    library_dirs = [],
                    extra_compile_args=['-std=c99'],
                    sources = sources,
                    language='c')

version = re.search(r'__version__ = "([0-9\.a-z\-]+)"',
        open("lib2d/__init__.py").read()).groups()[0]

setup(
    name = 'lib2d',
    version = version,
    author = "Joseph Marshall",
    author_email = "jlmrshl@gmail.com",
    description = "A fast and simple 2D sprite rendering library for games",
    license = "MIT",
    url="http://lib2d.com",
    long_description=open("README").read(),

    packages = ["lib2d"],
    ext_modules=[native],

    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: C',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
