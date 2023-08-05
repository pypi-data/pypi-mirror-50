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
#include "drawable.h"
#include "alloc.h"
#include "stretchy_buffer.h"

struct d* D = 0;


void d_init() {
    D = i_calloc(sizeof(*D), 1);
}
void d_shutdown() {
    sbfree(D->drawables);
    i_free(D);
    D = 0;
}

int viewport[2];
void d_viewport(int w, int h) {
    viewport[0] = w;
    viewport[1] = h;
}

LIB2D_EXPORT
void lib2d_draw(const lib2d_drawable* drawable) {
    lib2d_drawable* d = sbadd(D->drawables, 1);
    memcpy(d, drawable, sizeof(*drawable));
}
