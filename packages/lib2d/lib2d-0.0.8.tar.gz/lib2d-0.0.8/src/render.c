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

#include "render.h"
#include "drawable.h"
#include "alloc.h"
#include "stretchy_buffer.h"
#include "render_api.h"
#include "error.h"
#include "drawable.h"
#include "atlas_bank.h"
#include "stb_image.h"
#include <stdio.h>

struct lib2d_render_interface* LIB2D_RI = 0;

// Built-in render backends
void r_register_gl(struct lib2d_render_interface*);

struct pending_upload {
    struct pending_upload* next;
    lib2d_texture* texture;
    void* data;
    enum lib2d_r_image_format format;
    int width, height;
};

struct r {
    struct lib2d_r_draw_cmd* batches; // stretchy_buffer

    struct lib2d_r_ctx* ctx;
    struct lib2d_r_target* target;
    struct lib2d_r_layer* layer;

    struct atlas_bank* atlas_bank;
    struct pending_upload* pending_list;
    struct atlas_bank_entry* white_texture;
};
struct r* R = 0;

typedef struct image_internal {
    struct atlas_bank_entry* atlas_entry;
    enum lib2d_shader_type shader;
} image_internal;

int r_init(enum lib2d_render_backend render_backend, void* render_context) {
    // r_init may be called again without calling r_shutdown if the previous
    // graphics context was lost and being re-created.
    if (LIB2D_RI == 0) {
        LIB2D_RI = i_calloc(1, sizeof(*LIB2D_RI));
        R = i_calloc(sizeof(*R), 1);
    } else {
        memset(LIB2D_RI, 0, sizeof(*LIB2D_RI));
    }

    switch (render_backend) {
        case LIB2D_RENDER_BACKEND_GL:
            r_register_gl(LIB2D_RI);
            break;
        default:
            i_error("No implementation found for rendering backend %d", render_backend);
            r_shutdown();
            return -1;
    }
    int res = lib2d_render_api_init(render_context, &R->ctx);
    if (res != 0) {
        r_shutdown();
        return res;
    }

    R->target = lib2d_r_target_new(R->ctx);
    R->layer = lib2d_r_layer_new(R->ctx);
    lib2d_r_target_add_layer(R->target, R->layer);

    R->atlas_bank = atlas_bank_new();
    uint8_t white[4] = {0xff, 0xff, 0xff, 0xff};
    R->white_texture = atlas_bank_new_entry(R->atlas_bank, 1, 1, white,
            LIB2D_IMAGE_FORMAT_RGBA_8888, ATLAS_ENTRY_EXTRUDE_BORDER);

    return 0;
}

void r_shutdown() {
    if (R) {
        sbfree(R->batches);
        while (R->pending_list) {
            struct pending_upload* u = R->pending_list;
            R->pending_list = u->next;
            if (u->data) i_free(u->data);
            i_free(u);
        }
        atlas_bank_entry_delete(R->white_texture);
        atlas_bank_delete(R->atlas_bank);
    }
    if (LIB2D_RI) {
        if (LIB2D_RI->shutdown) LIB2D_RI->shutdown(R->ctx);
        i_free(LIB2D_RI);
        LIB2D_RI = 0;
        R->ctx = NULL;
    }
    if (R) {
        i_free(R);
        R = 0;
    }
}

void r_viewport(int w, int h) {
    lib2d_r_target_set_viewport(R->target, w, h);
}

void r_clear(float r, float g, float b, float a) {
    lib2d_r_clear(r, g, b, a);
}

void r_render() {
    r_upload_pending();
    int count = sbcount(D->drawables);
    if (count == 0) {
        return;
    }
    struct lib2d_r_vertex* vs = lib2d_r_layer_map_verticies(R->layer, count*6);
    struct lib2d_r_draw_cmd cmd = {.start=0, .count=0};
    enum lib2d_shader_type shader = LIB2D_SHADER_TYPE_DEFAULT;
    cmd.batch_cfg.shader = shader;
    int j = 0;
    for (unsigned long i=0; i<count; i++) {
        lib2d_drawable* d = &D->drawables[i];
        image_internal* ii = (image_internal*) d->image.internal;
        struct atlas_bank_entry* e;
        if (!ii) {
            e = R->white_texture;
            shader = LIB2D_SHADER_TYPE_DEFAULT;
        } else {
            e = ii->atlas_entry;
            shader = ii->shader;
        }
        lib2d_texture* tex = atlas_bank_get_texture(e);
        if (cmd.count == 0 || cmd.batch_cfg.tex != tex || shader != cmd.batch_cfg.shader) {
            if (cmd.count != 0) {
                sbpush(R->batches, cmd);
            }
            cmd.batch_cfg.shader = shader;
            cmd.count = 6;
            cmd.start = j;
            cmd.batch_cfg.tex = tex;
            cmd.batch_cfg.blend = true;
        } else {
            cmd.count += 6;
        }

        float u_l, u_r, v_t, v_b;
        struct lib2d_rect r = atlas_bank_get_region(e);
        u_l = r.l;
        u_r = r.r;
        v_t = r.t;
        v_b = r.b;

        vs[j].x = d->x;
        vs[j].y = d->y;
        vs[j].u = u_l;
        vs[j].v = v_t;
        vs[j].color = d->color;
        j++;

        vs[j].x = d->x;
        vs[j].y = d->y + d->h;
        vs[j].u = u_l;
        vs[j].v = v_b;
        vs[j].color = d->color;
        j++;

        vs[j].x = d->x + d->w;
        vs[j].y = d->y + d->h;
        vs[j].u = u_r;
        vs[j].v = v_b;
        vs[j].color = d->color;
        j++;

        vs[j].x = d->x;
        vs[j].y = d->y;
        vs[j].u = u_l;
        vs[j].v = v_t;
        vs[j].color = d->color;
        j++;

        vs[j].x = d->x + d->w;
        vs[j].y = d->y + d->h;
        vs[j].u = u_r;
        vs[j].v = v_b;
        vs[j].color = d->color;
        j++;

        vs[j].x = d->x + d->w;
        vs[j].y = d->y;
        vs[j].u = u_r;
        vs[j].v = v_t;
        vs[j].color = d->color;
        j++;
    }
    lib2d_r_layer_unmap_verticies(R->layer);
    sbresize(D->drawables, 0);
    sbpush(R->batches, cmd);

    struct lib2d_r_draw_cmd* cmds = lib2d_r_layer_map_draw_cmds(R->layer, sbcount(R->batches));
    memcpy(cmds, R->batches, sizeof(*cmds)*sbcount(R->batches));
    lib2d_r_layer_unmap_draw_cmds(R->layer);
    sbresize(R->batches, 0);

    lib2d_r_target_render(R->target);
}

LIB2D_EXPORT
int lib2d_image_load_buffer(unsigned char* data, lib2d_image* image, int w, int h, int bpp) {
    enum lib2d_r_image_format format;
    switch (bpp) {
        case 4: format = LIB2D_IMAGE_FORMAT_RGBA_8888; break;
        case 3: format = LIB2D_IMAGE_FORMAT_RGB_888; break;
        case 2: format = LIB2D_IMAGE_FORMAT_RGB_565; break;
        case 1: format = LIB2D_IMAGE_FORMAT_A_8; break;
        default:
        {
            i_error("Invalid image byte format");
            return -2;
        };
    }
    image_internal* ii = malloc(sizeof(*ii));
    ii->atlas_entry = atlas_bank_new_entry(R->atlas_bank, w, h,
            data, format, ATLAS_ENTRY_TRANSPARENT_BORDER);
    ii->shader = bpp == 1 ? LIB2D_SHADER_TYPE_SINGLE_CHANNEL : LIB2D_SHADER_TYPE_DEFAULT;
    lib2d_image im = {
        .internal = (void*)ii,
    };
    *image = im;
    return 0;
}


LIB2D_EXPORT
int lib2d_image_load(const char* path, lib2d_image* image, lib2d_image_info* info) {
    int w,h,n;
    unsigned char *data = stbi_load(path, &w, &h, &n, 0);
    if (!data) {
        i_error("Failed to load image data");
        return -1;
    }
    if (info) {
        info->w = w;
        info->h = h;
    }
    int res = lib2d_image_load_buffer(data, image, w, h, n);
    stbi_image_free(data);
    return res;
}

LIB2D_EXPORT
void lib2d_image_delete(lib2d_image image) {
    image_internal* ii = (image_internal*) image.internal;
    atlas_bank_entry_delete(ii->atlas_entry);
    image.internal = 0;
    free(ii);
}

lib2d_texture* r_texture_new() {
    lib2d_texture* t = i_calloc(sizeof(*t), 1);
    t->refcount = 1;
    lib2d_r_texture_init(t);
    return t;
}


void r_texture_delete(lib2d_texture* t) {
    assert(t->refcount == 0);
    lib2d_r_texture_deinit(R->ctx, t);
    i_free(t);
}

void r_texture_incref(lib2d_texture* texture) {
    texture->refcount ++;
}
bool r_texture_decref(lib2d_texture* texture) {
    texture->refcount --;
    if (texture->refcount == 0) {
        r_texture_delete(texture);
        return true;
    }
    return false;
}

void r_texture_set_data(lib2d_texture* t, int w, int h, enum lib2d_r_image_format format, void const* data) {
    struct pending_upload* u = i_calloc(1, sizeof(*u));
    u->texture = t;
    r_texture_incref(t);

    u->width = w;
    u->height = h;
    u->format = format;

    size_t bpp = 0;
    switch (format) {
    case LIB2D_IMAGE_FORMAT_RGBA_8888: bpp = 4; break;
    case LIB2D_IMAGE_FORMAT_RGB_888: bpp = 3; break;
    case LIB2D_IMAGE_FORMAT_RGB_565: bpp = 2; break;
    case LIB2D_IMAGE_FORMAT_A_8: bpp = 1; break;
    default: assert(false);
    }

    int size = w*h*bpp;
    u->data = i_malloc(size);
    memcpy(u->data, data, size);

    u->next = R->pending_list;
    R->pending_list = u;
}


static
void do_pending_upload(struct pending_upload* u) {
    if (!r_texture_decref(u->texture)) {
        if (u->width > 0 && u->height > 0) {
            struct lib2d_r_texture_data_info info = {
                .data=u->data,
                .texture=u->texture,
                .format=u->format,
                .width=u->width,
                .height=u->height
            };
            lib2d_r_texture_data(&info);
        }
        u->texture->width = u->width;
        u->texture->height = u->height;
    }
    if (u->data) i_free(u->data);
}

void r_upload_pending() {
    atlas_bank_resolve(R->atlas_bank);
    while (R->pending_list) {
        struct pending_upload* u = R->pending_list;
        do_pending_upload(u);
        R->pending_list = u->next;
        i_free(u);
    }
}
