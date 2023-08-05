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

#ifndef ATLAS_BANK_H
#define ATLAS_BANK_H

#include "atlas.h"
#include "render_api.h"
#include <stdint.h>

struct atlas_bank;
struct atlas_bank_entry;

struct atlas_bank*
atlas_bank_new();

void
atlas_bank_delete(struct atlas_bank*);

bool
atlas_bank_resolve(struct atlas_bank*);

struct atlas_bank_entry*
atlas_bank_new_entry(struct atlas_bank*, int width, int height,
        uint8_t* use_data, enum lib2d_r_image_format, uint32_t flags);

void
atlas_bank_entry_delete(struct atlas_bank_entry*);

struct lib2d_texture*
atlas_bank_get_texture(struct atlas_bank_entry*);

struct lib2d_rect
atlas_bank_get_region(struct atlas_bank_entry*);

#endif
