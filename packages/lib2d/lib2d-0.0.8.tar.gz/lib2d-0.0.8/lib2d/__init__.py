"""lib2d is a fast and simple 2D sprite rendering library for games licensed under the MIT.
"""

__credits__ = (
"""
Copyright (C) 2019 Joseph Marshall

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
""")

__author__ = "Joseph Marshall <jlmrshl@gmail.com>"
__version__ = "0.0.8"

from builtins import bytes
from ctypes import *
import lib2d.finalizer
from enum import IntEnum
import weakref

_lib = None

class _CtypesEnum(IntEnum):
    @classmethod
    def from_param(cls, obj):
        return int(obj)

class RenderBackend(_CtypesEnum):
    """An enum to specify which rendering backend to use.

    Examples:
        >>> lib2d.init(RenderBackend.GL)
    """
    GL = 0

def init(render_backend=RenderBackend.GL, render_context=0):
    """Initializes lib2d.

    Depending on the RenderBackend used you may need to pass in relevant
    context information. This is platform specific.  For OpenGL make sure the
    context is currently bound when you call this function and pass NULL to
    render_context.

    Examples:
        >>> import pygame
        >>> from pygame.locals import *
        >>> screen = pygame.display.set_mode((800, 600), HWSURFACE|OPENGL|DOUBLEBUF)
        >>> lib2d.init(RenderBackend.GL)
        >>> lib2d.viewport(800, 600)
    """
    global _lib
    
    # load the C library
    try:
        import importlib.machinery
        f = importlib.machinery.PathFinder.find_module("_lib2d").path
    except ImportError:
        import imp
        f = imp.find_module("_lib2d")[1]
    _lib = CDLL(f)
    
    _lib.lib2d_init.argtypes = [RenderBackend, c_void_p]
    _lib.lib2d_init.restype = c_int

    _lib.lib2d_shutdown.argtypes = []
    _lib.lib2d_shutdown.restype = None

    _lib.lib2d_viewport.argtypes = [c_int, c_int]
    _lib.lib2d_viewport.restype = None

    _lib.lib2d_render.argtypes = []
    _lib.lib2d_render.restype = None

    _lib.lib2d_image_load.argtypes = [c_char_p, c_void_p]
    _lib.lib2d_image_load.restype = c_int

    _lib.lib2d_image_delete.argtypes = [_Image]
    _lib.lib2d_image_delete.restype = None

    _lib.lib2d_draw.argtypes = [c_void_p]
    _lib.lib2d_draw.restype = None

    _lib.lib2d_font_load.argtypes = [c_char_p, c_void_p]
    _lib.lib2d_font_load.restype = c_int

    _lib.lib2d_font_delete.argtypes = [_Font]
    _lib.lib2d_font_delete.restype = None

    _lib.lib2d_text.argtypes = [_Font, c_float, c_char_p, c_int, c_int, c_uint32]
    _lib.lib2d_text.restype = None

    _lib.lib2d_get_error.argtypes = []
    _lib.lib2d_get_error.restype = c_char_p

    if _lib.lib2d_init(render_backend, render_context) != 0:
        raise Exception(_lib.lib2d_get_error())

def shutdown():
    """Releases all resources created by lib2d.
    
    Examples:
        >>> lib2d.init()
        >>> # game code ...
        >>> lib2d.shutdown()
    """
    global _lib
    for im in Image._bank.values():
        im._finalizer()
    Image._bank.clear()
    _lib.lib2d_shutdown()
    _lib = None

def viewport(width, height):
    """Informs lib2d of the current viewport size.
    
    This should be kept up to date with the size of the window or surface you are rendering to.
    """
    _lib.lib2d_viewport(width, height)

def render():
    """Executes all draw commands issued since the last call to this function."""
    _lib.lib2d_render()


class _ImageInfo(Structure):
    _fields_ = [("w", c_int),
               ("h", c_int)]

class _Image(Structure):
    _fields_ = [("internal", c_void_p)]

class Image(object):
    """References a bitmap that can be rendered by a Drawable.

    Attributes:
        w (int): Width of this image
        h (int): Height of this image

    Examples:
        >>> lib2d.init()
        >>> logo = lib2d.Image("docs/theme/img/logo.png")
    """

    _bank = weakref.WeakValueDictionary()
    def __init__(self, path):
        """Load an image from the file system at `path`."""
        if path in Image._bank:
            im = Image._bank[path]
            self.w = im.w
            self.h = im.h
            self._image = im._image
        else:
            info = _ImageInfo(0, 0)
            self._image = _Image()
            if _lib.lib2d_image_load(c_char_p(bytes(path, 'utf8')), byref(self._image), byref(info)) != 0:
                raise Exception(_lib.lib2d_get_error())
            self.w = info.w
            self.h = info.h
            Image._bank[path] = self
        
        self._finalizer = finalizer.finalize(self, self.__delete)

    def __delete(self):
        if self._image:
            _lib.lib2d_image_delete(self._image)
            self._image = None


class _Font(Structure):
    _fields_ = [("internal", c_void_p)]

class Font(object):
    """A TrueType font that can render text.

    Examples:
        >>> lib2d.init()
        >>> font = lib2d.Font("demos/04_text/FreeSans.ttf")
        >>> font.text("Hello Lib2D!", font_size=80)
    """

    _bank = weakref.WeakValueDictionary()
    def __init__(self, path):
        """Load a TrueType font from the file system at `path`."""
        if path in Font._bank:
            self._font = Font._bank[path]
        else:
            self._font = _Font()
            if _lib.lib2d_font_load(c_char_p(bytes(path, 'utf8')), byref(self._font)) != 0:
                raise Exception(_lib.lib2d_get_error())
            Font._bank[path] = self
        
        self._finalizer = finalizer.finalize(self, self.__delete)

    def __delete(self):
        if self._font:
            _lib.lib2d_font_delete(self._font)
            self._font = None

    def text(self, text, font_size=20, x=0, y=0, color=0x000000ff):
        """ Schedules UTF-8 text to be rendered to the screen when `lib2d_render()` is called."""
        _lib.lib2d_text(self._font, font_size, c_char_p(bytes(text, 'utf8')), x, y, color)



class Drawable(Structure):
    """An entity that renders a graphical source, such as an image, to the display.

    Attributes:
        image: An Image (or a path to an image on the file system) to render when `draw()` is called.
        x (float): How many pixels from the left of the screen to render.
        y (float): How many pixels down from the top of the screen to render.
        w (float): Width of this drawable.
        h (float): Height of this drawable.
        color (int): Multiplies each pixel value of the referenced image by this color (format: `0xRRGGBBAA`).
    """
    _fields_ = [("x", c_float),
               ("y", c_float),
               ("w", c_float),
               ("h", c_float),
               ("_image_i", _Image),
               ("color", c_uint32),
               ]

    def __init__(self, image=None, x=0, y=0, w=0, h=0, color=0xffffffff):
        """If an image is passed when creating a drawable, width and height are set to
        match the image's size if not given explicitly.
        """
        self.image = image
        if self.image:
            if w == 0:
                w = self.image.w
            if h == 0:
                h = self.image.h
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def _get_image(self):
        return self._image
    def _set_image(self, image):
        if image is None:
            self._image = None
            self._image_i = _Image(0)
            return
        if isinstance(image, str):
            image = Image(image)
        self._image = image
        self._image_i = image._image
    image = property(_get_image, _set_image)

    def draw(self):
        """Schedule this Drawable to be rendered when `lib2d.render()` is called.
        
        The current state at the time of calling this function is what will be
        used when rendering. So it's possible to call draw, change this
        drawable's state, and call draw again to render in its new state.

        Examples:
            # This will render the same green square at two locations.
            >>> lib2d.init()
            >>> d = lib2d.Drawable(x=100, y=0, w=100, h=100, color=0x00ff00ff)
            >>> d.draw()
            >>> d.y = 100
            >>> d.draw()

        """
        _lib.lib2d_draw(byref(self))

__all__ = ['init', 'shutdown', 'viewport', 'render', 'RenderBackend', 'Drawable', 'Image', 'Font']
