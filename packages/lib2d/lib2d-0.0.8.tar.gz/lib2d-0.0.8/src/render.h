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

#ifndef __LIB2D_RENDER__
#define __LIB2D_RENDER__
#include "lib2d.h"
#include "render_api.h"
#include <stdbool.h>


int r_init(enum lib2d_render_backend render_backend, void* render_context);
void r_shutdown();
void r_upload_pending();
void r_render();
void r_clear(float, float, float, float);
void r_viewport(int w, int h);
lib2d_texture* r_texture_new();
void r_texture_incref(lib2d_texture* texture);
bool r_texture_decref(lib2d_texture* texture);
void r_texture_set_data(lib2d_texture* texture, int w, int h, enum lib2d_r_image_format format, void const* data);

#endif
