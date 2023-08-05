/*
 * Copyright (C) 2019 Joseph Marshall
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "lib2d.h"
#include "error.h"
#include "stb_image.h"
#include "alloc.h"
#include "drawable.h"
#include "render.h"

#define STBI_MALLOC(sz)           i_malloc(sz)
#define STBI_REALLOC(p,newsz)     i_realloc(p,newsz)
#define STBI_FREE(p)              i_free(p)

LIB2D_EXPORT
int lib2d_init(enum lib2d_render_backend render_backend, void* render_context) {
    int res = r_init(render_backend, render_context);
    if (res != 0) { return res; }
    d_init();
    return 0;
}

LIB2D_EXPORT
void lib2d_shutdown() {
    d_shutdown();
    r_shutdown();
}

LIB2D_EXPORT
void lib2d_viewport(int w, int h) {
    r_viewport(w, h);
    d_viewport(w, h);
}

LIB2D_EXPORT
void lib2d_render() {
    r_render();
}

LIB2D_EXPORT
void lib2d_clear(float r, float g, float b, float a) {
    r_clear(r, g, b, a);
}
