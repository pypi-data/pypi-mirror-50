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

#include "atlas_bank.h"
#include "atlas.h"
#include "stretchy_buffer.h"
#include "render.h"
#include <stdlib.h>

static
struct atlas_ref*
create_atlas(struct atlas_bank*, enum lib2d_r_image_format);

static
struct atlas_ref*
get_or_create_atlas(struct atlas_bank*, enum lib2d_r_image_format);

struct atlas_bank_entry {
    struct atlas_ref* ref;
    struct atlas_entry* atlas_entry;

    // Doesn't store the refcount... it's done once in atlas_ref
    struct lib2d_texture* texture;

    struct lib2d_rect texture_region;
    uint32_t flags;
};

struct atlas_ref {
    struct atlas* atlas;
    struct lib2d_texture* texture;
    struct atlas_bank_entry** entries; // stretchy_buffer
    enum lib2d_r_image_format format;
    bool dirty;
}; 

struct atlas_bank {
    // Because we may create a new entry while looping through these, we store
    // pointers in the stretchy_buffer.
    struct atlas_ref** atlas_refs; // stretchy_buffer
};

struct atlas_bank*
atlas_bank_new() {
    struct atlas_bank* bank = i_malloc(sizeof(struct atlas_bank));
    bank->atlas_refs = NULL;
    return bank;
}

void
atlas_bank_delete(struct atlas_bank* bank) {
    sbforeachv(struct atlas_ref* ref, bank->atlas_refs) {
        sbforeachv(struct atlas_bank_entry* e, ref->entries) {
            atlas_remove_entry(ref->atlas, e->atlas_entry);
            i_free(e);
        }
        sbfree(ref->entries);
        atlas_delete(ref->atlas);
        r_texture_decref(ref->texture);
        i_free(ref);
    }
    sbfree(bank->atlas_refs);
    i_free(bank);
}

bool
atlas_bank_resolve(struct atlas_bank* bank) {
    bool reresolve = false;
    bool found_dirty = false;
    sbforeachv(struct atlas_ref* ref, bank->atlas_refs) {
        if (!ref->dirty) continue;
        found_dirty = true;
        ref->dirty = false;
        unsigned int out_w, out_h;
        uint8_t* data = atlas_pack(ref->atlas, 2048, 2048, &out_w, &out_h);
        r_texture_set_data(ref->texture, out_w, out_h, ref->format, data);
        i_free(data);

        struct atlas_entry* const* failed = atlas_get_pack_failed(ref->atlas, NULL);
        if (sbcount(failed)) {
            reresolve = true;
            struct atlas_ref* new_ref = create_atlas(bank, ref->format);
            new_ref->dirty = true;

            sbforeachv(struct atlas_entry* e, failed) {
                atlas_move_entry(new_ref->atlas, ref->atlas, e);
                for (int i=0; i<sbcount(ref->entries); i++) {
                    struct atlas_bank_entry* b_e = ref->entries[i];
                    if (b_e->atlas_entry == e) {
                        sbremove(ref->entries, i, 1);
                        sbpush(new_ref->entries, b_e);
                        b_e->ref = new_ref;
                        break;
                    }
                }
            }
        }

        float sx = 1.f / out_w;
        float sy = 1.f / out_h;
        sbforeachv(struct atlas_bank_entry* b_e, ref->entries) {
            b_e->texture = ref->texture;
            unsigned int x, y, w, h;
            atlas_entry_get_packed_location(b_e->atlas_entry,
                    &x, &y, &w, &h);
            if (b_e->flags) {
                x ++;
                y ++;
                w -= 2;
                h -= 2;
            }
            b_e->texture_region.l = x * sx;
            b_e->texture_region.t = y * sy;
            b_e->texture_region.r = (x+w) * sx;
            b_e->texture_region.b = (y+h) * sy;
        }
    }

    if (reresolve) atlas_bank_resolve(bank);
    return found_dirty;
}

struct atlas_bank_entry*
atlas_bank_new_entry(struct atlas_bank* bank, int width, int height,
        uint8_t* data, enum lib2d_r_image_format format, uint32_t flags) {
    struct atlas_bank_entry* e = i_malloc(sizeof(struct atlas_bank_entry));
    e->texture = NULL;

    struct atlas_ref* ref = get_or_create_atlas(bank, format);
    ref->dirty = true;
    e->atlas_entry = atlas_add_entry(ref->atlas, width, height, data, flags);
    e->flags = flags;
    e->ref = ref;

    sbpush(ref->entries, e);
    return e;
}

void
atlas_bank_entry_delete(struct atlas_bank_entry* e) {
    atlas_remove_entry(e->ref->atlas, e->atlas_entry);
    sbforeachv(struct atlas_bank_entry* c, e->ref->entries) {
        if (c == e) {
            sbremove(e->ref->entries, stb__counter, 1);
            break;
        }
    }
    i_free(e);
}

struct lib2d_texture*
atlas_bank_get_texture(struct atlas_bank_entry* e) {
    return e->texture;
}

struct lib2d_rect
atlas_bank_get_region(struct atlas_bank_entry* e) {
    return e->texture_region;
}


static
struct atlas_ref*
create_atlas(struct atlas_bank* bank, enum lib2d_r_image_format format) {
    int bpp = 0;
    switch (format) {
    case LIB2D_IMAGE_FORMAT_RGBA_8888: bpp = 4; break;
    case LIB2D_IMAGE_FORMAT_RGB_888: bpp = 3; break;
    case LIB2D_IMAGE_FORMAT_RGB_565: bpp = 2; break;
    case LIB2D_IMAGE_FORMAT_A_8: bpp = 1; break;
    default: assert(false);
    }
    struct atlas_ref* ref = i_malloc(sizeof(struct atlas_ref));
    sbpush(bank->atlas_refs, ref);
    ref->atlas = atlas_new(bpp);
    ref->texture = r_texture_new();
    ref->format = format;
    ref->entries = NULL;
    return ref;
}

static
struct atlas_ref*
get_or_create_atlas(struct atlas_bank* bank, enum lib2d_r_image_format format) {
    for (int i=sbcount(bank->atlas_refs)-1; i>=0; i--) {
        struct atlas_ref* ref = bank->atlas_refs[i];
        if (ref->format == format)
            return ref;
    }

    return create_atlas(bank, format);
}

