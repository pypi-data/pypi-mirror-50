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

#ifndef __LIB2D_RENDER_API__
#define __LIB2D_RENDER_API__

#include "lib2d.h"
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

enum lib2d_r_image_format {
    LIB2D_IMAGE_FORMAT_RGBA_8888,
    LIB2D_IMAGE_FORMAT_RGB_888,
    LIB2D_IMAGE_FORMAT_RGB_565,
    LIB2D_IMAGE_FORMAT_A_8,
};

enum lib2d_shader_type {
    LIB2D_SHADER_TYPE_DEFAULT,
    LIB2D_SHADER_TYPE_SINGLE_CHANNEL,
    LIB2D_SHADER_TYPE_END
};

struct lib2d_r_texture;

typedef struct lib2d_texture {
    int width, height;
    struct lib2d_r_texture* r;
    int refcount;
} lib2d_texture;


struct lib2d_r_texture_data_info {
    void* data;
    struct lib2d_texture* texture;
    int width, height;
    enum lib2d_r_image_format format;
};


struct lib2d_rect {
    float l, t, r, b;
};


struct lib2d_r_vertex {
    float x, y;
    float u, v;
    uint32_t color;
};

struct lib2d_r_batch_cfg {
    struct lib2d_texture* tex;
    enum lib2d_shader_type shader;
    bool blend;
};

struct lib2d_r_draw_cmd {
    unsigned int start;
    unsigned int count;
    struct lib2d_r_batch_cfg batch_cfg;
};

struct lib2d_r_ctx;
struct lib2d_r_layer;
struct lib2d_r_target;

struct lib2d_render_interface {
    int (*init)(void* device, struct lib2d_r_ctx** ctx);
    void (*shutdown)(struct lib2d_r_ctx* ctx);

    void (*clear)(float r, float g, float b, float a);

    struct lib2d_r_target* (*target_new)(struct lib2d_r_ctx* ctx);
    void (*target_set_viewport)(struct lib2d_r_target*, int w, int h);
    void (*target_render)(struct lib2d_r_target*);
    void (*target_delete)(struct lib2d_r_target*);
    void (*target_reset_layers)(struct lib2d_r_target*);
    void (*target_add_layer)(struct lib2d_r_target*, struct lib2d_r_layer*);

    struct lib2d_r_layer* (*layer_new)(struct lib2d_r_ctx* ctx);
    void (*layer_delete)(struct lib2d_r_layer*);
    struct lib2d_r_vertex* (*layer_map_verticies)(struct lib2d_r_layer* layer, int count);
    void (*layer_unmap_verticies)(struct lib2d_r_layer* layer);
    struct lib2d_r_draw_cmd* (*layer_map_draw_cmds)(struct lib2d_r_layer* layer, int count);
    void (*layer_unmap_draw_cmds)(struct lib2d_r_layer* layer);

    void (*texture_init)(struct lib2d_texture*);
    void (*texture_deinit)(struct lib2d_r_ctx*, struct lib2d_texture*);
    void (*texture_data)(struct lib2d_r_texture_data_info*);
};

extern struct lib2d_render_interface * LIB2D_RI;


static inline int lib2d_render_api_init(void* device, struct lib2d_r_ctx** ctx) { return LIB2D_RI->init(device, ctx); }
static inline void lib2d_render_api_shutdown(struct lib2d_r_ctx* ctx) { LIB2D_RI->shutdown(ctx); }
static inline void lib2d_r_clear(float r, float g, float b, float a) { LIB2D_RI->clear(r,g,b,a); }

static inline struct lib2d_r_target* lib2d_r_target_new(struct lib2d_r_ctx* ctx) { return LIB2D_RI->target_new(ctx); }
static inline void lib2d_r_target_set_viewport(struct lib2d_r_target* t, int w, int h) { LIB2D_RI->target_set_viewport(t, w, h); }
static inline void lib2d_r_target_render(struct lib2d_r_target* t) { LIB2D_RI->target_render(t); }
static inline void lib2d_r_target_delete(struct lib2d_r_target* t) { LIB2D_RI->target_delete(t); }
static inline void lib2d_r_target_reset_layers(struct lib2d_r_target* t) { LIB2D_RI->target_reset_layers(t); }
static inline void lib2d_r_target_add_layer(struct lib2d_r_target* t, struct lib2d_r_layer* l) { LIB2D_RI->target_add_layer(t, l); }

static inline struct lib2d_r_layer* lib2d_r_layer_new(struct lib2d_r_ctx* ctx) { return LIB2D_RI->layer_new(ctx); }
static inline void lib2d_r_layer_delete(struct lib2d_r_layer* layer) { LIB2D_RI->layer_delete(layer); }
static inline struct lib2d_r_vertex* lib2d_r_layer_map_verticies(struct lib2d_r_layer* layer, int count) { return LIB2D_RI->layer_map_verticies(layer, count); }
static inline void                   lib2d_r_layer_unmap_verticies(struct lib2d_r_layer* layer) { LIB2D_RI->layer_unmap_verticies(layer); }
static inline struct lib2d_r_draw_cmd* lib2d_r_layer_map_draw_cmds(struct lib2d_r_layer* layer, int count) { return LIB2D_RI->layer_map_draw_cmds(layer, count); }
static inline void                     lib2d_r_layer_unmap_draw_cmds(struct lib2d_r_layer* layer) { LIB2D_RI->layer_unmap_draw_cmds(layer); }

static inline void lib2d_r_texture_init(struct lib2d_texture* tex){ LIB2D_RI->texture_init(tex); }
static inline void lib2d_r_texture_deinit(struct lib2d_r_ctx* ctx, struct lib2d_texture* tex) { LIB2D_RI->texture_deinit(ctx, tex); }
static inline void lib2d_r_texture_data(struct lib2d_r_texture_data_info* i) { LIB2D_RI->texture_data(i); }


#ifdef __cplusplus
}
#endif
#endif
