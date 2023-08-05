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

#ifdef IOS
#include <OpenGLES/ES2/gl.h>
#include <OpenGLES/ES2/glext.h>
#else
#ifdef GLES
#include <GLES2/gl2.h>
#include <GLES2/gl2ext.h>
#else
#include "gl_core_3_3.h"
#endif
#endif

#if 0
#define GLDEBUG(x) \
    x; \
    { \
        GLenum e; \
        if ((e=glGetError()) != GL_NO_ERROR) { \
            printf("glError 0x%x at %s line %d\n", e, __FILE__, __LINE__); \
            assert(false); \
        } \
    }
#else
#define GLDEBUG(x) (x)
#endif

#include "render_api.h"
#include "error.h"
#include "stretchy_buffer.h"
#include "small_vec.h"
#include "alloc.h"
#include "lib2dthread.h"

#include <stdio.h>

struct shader_handles {
    int32_t id;
    int32_t positionHandle;
    int32_t projectionHandle;
    int32_t texCoordHandle;
    int32_t colorAttrib;
    int32_t textureHandle;
};

struct shader {
    struct shader_handles handles;
};

struct lib2d_r_ctx {
    struct lib2d_r_vertex* VERT_POOL; // stretchy buffer
    struct shader shaders[LIB2D_SHADER_TYPE_END];
    THREAD_ID gl_thread_id;
    bool FEATURE_MAP;
};


struct lib2d_r_layer {
    struct lib2d_r_ctx* ctx;
    GLuint vbo;
    int vbo_count;
    small_vec(struct lib2d_r_draw_cmd, 4) draw_cmds;
};


struct lib2d_r_target {
    struct lib2d_r_ctx* ctx;
    int viewport[2];
    struct lib2d_r_layer** layers; // stretchy buffer
};

struct lib2d_r_texture {
    GLuint handle;
    GLenum texture_type;
};


static
int
init(void* device, struct lib2d_r_ctx** ctx) {
#ifndef GLES
    int res = ogl_LoadFunctions();
    if (res == ogl_LOAD_FAILED) {
        i_error("OpenGL failed to load functions");
        return res;
    }
#endif

    *ctx = i_calloc(sizeof(struct lib2d_r_ctx), 1);
    (*ctx)->gl_thread_id = THREAD_CURRENT_ID();

#ifndef GLES
    if (_ptrc_glMapBuffer) {
        (*ctx)->FEATURE_MAP = true;
    }
#endif

    return 0;
}

static
void
shutdown(struct lib2d_r_ctx* ctx) {
    i_free(ctx);
}




/////////////////////////////////////////////////////////////////////////////
// Shader templating
/////////////////////////////////////////////////////////////////////////////

struct template_var {
    const char* key;
    const char* value;
};

static
char*
template(struct template_var* vars, const char* source, const char* prefix) {
    // figure out the total size needed for the buffer
    size_t len = strlen(source) + strlen(prefix);
    for (size_t i=0; vars[i].key; i++) {
        len += strlen(vars[i].key) + strlen(vars[i].value);
    }

    char* result = i_malloc(len+1);
    strcpy(result, prefix);
    strcat(result, source);

    for (size_t i=0; vars[i].key; i++) {
        char* found = strstr(result, vars[i].key);
        if (found) {
            size_t len_key = strlen(vars[i].key);
            size_t len_value = strlen(vars[i].value);
            memmove(found+len_value, found+len_key, strlen(found+len_key)+1);
            memcpy(found, vars[i].value, len_value);
        }
    }

    return result;
}

/////////////////////////////////////////////////////////////////////////////
// Shaders
/////////////////////////////////////////////////////////////////////////////

#ifdef GLES
#define IN "varying "
#define OUT "varying "
#define ATTRIBUTE "attribute "
#else
#define IN "in "
#define OUT "out "
#define ATTRIBUTE "in "
#endif

static const char* defaultVertexSource =
        "VERSION"
        ATTRIBUTE"vec2 position;\n"
        ATTRIBUTE"vec2 texCoord;\n"
        ATTRIBUTE"vec4 colorAttrib;\n"
        OUT"vec2 uv;\n"
        OUT"vec4 color;\n"
        OUT"float alpha;\n"
        "uniform vec2 projection;\n"
        "void main() {\n"
        "    uv = texCoord;\n"
        "    color = vec4(colorAttrib.abg, 1.0);\n"
        "    alpha = colorAttrib.r;\n"
        "    vec2 p = position * projection - vec2(1.0, 1.0);\n"
        "    gl_Position = vec4(p.x, 0.0-p.y, 0.0, 1.0);\n"
        "}\n";

static const char* defaultFragmentSource =
        "VERSION"
        "PRECISION"
#ifndef GLES
        OUT"vec4 outColor;\n"
#endif
        IN"vec2 uv;\n"
        IN"vec4 color;\n"
        IN"float alpha;\n"
        "uniform SAMPLER0 tex0;\n"
        "void main() {\n"
#ifdef GLES
        "    vec4 sampled = texture2D(tex0, uv);\n"
#else
        "    vec4 sampled = texture(tex0, uv);\n"
#endif
        "    vec4 premult_sampled = vec4(sampled.rgb*sampled.a, sampled.a);\n"
        "    vec4 c = premult_sampled * color * alpha;\n"
#ifdef GLES
        "    gl_FragColor = c;\n"
#else
        "    outColor = c;\n"
#endif
        "}\n";

static const char* singleChannelFragmentSource =
        "VERSION"
        "PRECISION"
#ifndef GLES
        OUT"vec4 outColor;\n"
#endif
        IN"vec2 uv;\n"
        IN"vec4 color;\n"
        IN"float alpha;\n"
        "uniform SAMPLER0 tex0;\n"
        "void main() {\n"
#ifdef GLES
        "    float sampled = texture2D(tex0, uv).a;\n"
#else
        "    float sampled = texture(tex0, uv).r;\n"
#endif
        "    vec4 c = vec4(sampled) * color * alpha;\n"
#ifdef GLES
        "    gl_FragColor = c;\n"
#else
        "    outColor = c;\n"
#endif
        "}\n";

struct shader_source_pair {
    const char* vert_source;
    const char* frag_source;
};

struct shader_source_pair
new_shader_source_pair(const char* vert_source, const char* frag_source) {
    struct shader_source_pair out = {
        .vert_source = vert_source,
        .frag_source = frag_source,
    };
    return out;
}

struct shader_source_pair
get_shader(enum lib2d_shader_type t) {
    switch (t) {
    case LIB2D_SHADER_TYPE_DEFAULT:
        return new_shader_source_pair(defaultVertexSource, defaultFragmentSource);
    case LIB2D_SHADER_TYPE_SINGLE_CHANNEL:
        return new_shader_source_pair(defaultVertexSource, singleChannelFragmentSource);
    default:
        assert(false);
        return new_shader_source_pair(0, 0);
    }
}

static
GLuint
compileShader(GLenum type, const char* source) {
    GLuint shader = GLDEBUG(glCreateShader(type));
    GLDEBUG(glShaderSource(shader, 1, &source, NULL));
    GLDEBUG(glCompileShader(shader));

    GLint logLength;
    GLDEBUG(glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &logLength));
    if (logLength > 1) {
        char * log = i_malloc((logLength)*sizeof(char));
        GLDEBUG(glGetShaderInfoLog(shader, logLength, NULL, log));
        fprintf(stderr, "Shader error:\n%s\nSource:\n%s", log, source);
        i_free(log);
    }
    return shader;
}

static
void
load_program(struct lib2d_r_ctx* ctx, enum lib2d_shader_type type) {
    struct shader_handles* h = &ctx->shaders[type].handles;

    struct shader_source_pair source = get_shader(type);

    const char* fragmentPrefix = "";

    struct template_var vars[] = {
#ifdef GLES
        {"VERSION",""},
        {"PRECISION","precision mediump float;\n"},
#else
        {"VERSION","#version 130\n"},
        {"PRECISION",""},
#endif
        {"SAMPLER0","sampler2D"},
        {0,0}};


    char* fragSource = template(vars, source.frag_source, fragmentPrefix);

    char* vertSource = template(vars, source.vert_source, "");

    h->id = GLDEBUG(glCreateProgram());
    GLDEBUG(glAttachShader(h->id,
            compileShader(GL_VERTEX_SHADER, vertSource)));
    GLDEBUG(glAttachShader(h->id,
            compileShader(GL_FRAGMENT_SHADER, fragSource)));
    GLDEBUG(glLinkProgram(h->id));
    GLDEBUG(glUseProgram(h->id));

    GLint logLength;
    glGetProgramiv(h->id, GL_INFO_LOG_LENGTH, &logLength);
    if (logLength > 1) {
        char * log = i_malloc((logLength)*sizeof(char));
        glGetProgramInfoLog(h->id, logLength, NULL, log);
        fprintf(stderr, "Linker error: %s\n", log);
        i_free(log);
    }

    h->positionHandle = glGetAttribLocation(h->id, "position");
    h->texCoordHandle = glGetAttribLocation(h->id, "texCoord");
    h->colorAttrib = glGetAttribLocation(h->id, "colorAttrib");
    h->textureHandle = glGetUniformLocation(h->id, "tex0");

    i_free(vertSource);
    i_free(fragSource);
}

static
struct shader_handles*
use_shader(struct lib2d_r_ctx* ctx, enum lib2d_shader_type type) {
    struct shader_handles* sh = &ctx->shaders[type].handles;
    if (sh->id == 0) {
        load_program(ctx, type);
    }
    GLDEBUG(glUseProgram(sh->id));
    return sh;
}



/////////////////////////////////////////////////////////////////////////////
// Render
/////////////////////////////////////////////////////////////////////////////

static
void
clear(float r, float g, float b, float a) {
    GLDEBUG(glBindFramebuffer(GL_FRAMEBUFFER, 0));
    GLDEBUG(glClearColor(r,g,b,a));
    GLDEBUG(glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT));
}

static
void
render_start(int viewport_w, int viewport_h) {
    GLDEBUG(glBindFramebuffer(GL_FRAMEBUFFER, 0));
    GLDEBUG(glViewport(0,0, viewport_w, viewport_h));
    GLDEBUG(glDisable(GL_DEPTH_TEST));
    GLDEBUG(glDisable(GL_CULL_FACE));
    GLDEBUG(glDisable(GL_DITHER));
    GLDEBUG(glDisable(GL_SCISSOR_TEST));
    GLDEBUG(glDisable(GL_STENCIL_TEST));
}

struct state_tracker {
    struct lib2d_r_target* target;
    struct lib2d_r_batch_cfg last;
    struct shader_handles* shader;
    int texture_slot;
    GLuint vbo;
};

static
void
state_tracker_start(struct state_tracker* s, struct lib2d_r_target* target) {
    memset(s, 0, sizeof(*s));
    s->target = target;
    s->texture_slot = -1;
}

static
void
texture_bind(struct lib2d_texture* tex, int sampler_uniform, int texture_slot) {
    GLDEBUG(glUniform1i(sampler_uniform, texture_slot));
    GLDEBUG(glActiveTexture(GL_TEXTURE0+texture_slot));
    GLDEBUG(glBindTexture(tex->r->texture_type, tex->r->handle));
}

#define BUFFER_OFFSET(i) ((void*)(i))
void
state_tracker_transition(struct lib2d_r_ctx* ctx, struct state_tracker* s, struct lib2d_r_layer* layer, struct lib2d_r_batch_cfg* b) {
    bool is_first_time = !s->shader;
    if (is_first_time || b->blend != s->last.blend) {
        if (b->blend) {
            GLDEBUG(glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA));
            glEnable(GL_BLEND);
        } else {
            glDisable(GL_BLEND);
        }
    }

    struct shader_handles* shader;
    struct shader_handles* old_shader = s->shader;
    int texture_slot=0;
    bool shader_changed = false;
    if (!s->shader || b->shader != s->last.shader) {
        shader = use_shader(ctx, b->shader);
        shader_changed = true;
        s->shader = shader;
    } else {
        texture_slot = s->texture_slot;
        shader = s->shader;
    }

    if (s->texture_slot != texture_slot || s->last.tex != b->tex || shader_changed) {
        texture_bind(b->tex, shader->textureHandle, texture_slot);
    }


    if (shader_changed) {
        GLDEBUG(glUniform2f(shader->projectionHandle,
                2.f/s->target->viewport[0],
                2.f/s->target->viewport[1]));

        if (old_shader) {
            glDisableVertexAttribArray(old_shader->positionHandle);
            glDisableVertexAttribArray(old_shader->texCoordHandle);
            glDisableVertexAttribArray(old_shader->colorAttrib);
        }

        GLDEBUG(glEnableVertexAttribArray(shader->positionHandle));
        GLDEBUG(glEnableVertexAttribArray(shader->texCoordHandle));
        GLDEBUG(glEnableVertexAttribArray(shader->colorAttrib));

        s->shader = shader;
    }

    if (s->vbo != layer->vbo || shader_changed) {
        GLDEBUG(glBindBuffer(GL_ARRAY_BUFFER, layer->vbo));
        GLDEBUG(glVertexAttribPointer(shader->positionHandle,
                2, GL_FLOAT, GL_FALSE, sizeof(struct lib2d_r_vertex),
                BUFFER_OFFSET(0)));
        GLDEBUG(glVertexAttribPointer(shader->texCoordHandle,
                2, GL_FLOAT, GL_FALSE, sizeof(struct lib2d_r_vertex),
                BUFFER_OFFSET(8)));
        GLDEBUG(glVertexAttribPointer(shader->colorAttrib,
                4, GL_UNSIGNED_BYTE, GL_TRUE, sizeof(struct lib2d_r_vertex),
                BUFFER_OFFSET(8 + 8)));

        s->vbo = layer->vbo;
    }
    s->texture_slot = texture_slot;
    s->last = *b;
}

static
void
state_tracker_end(struct state_tracker* s) {
    if (s->shader) {
        GLDEBUG(glDisableVertexAttribArray(s->shader->positionHandle));
        GLDEBUG(glDisableVertexAttribArray(s->shader->texCoordHandle));
        GLDEBUG(glDisableVertexAttribArray(s->shader->colorAttrib));
    }
}

static
void
render_layer(struct lib2d_r_layer* layer, struct state_tracker* state_tracker) {
    sv_foreach_p(struct lib2d_r_draw_cmd* cmd, layer->draw_cmds) {
        state_tracker_transition(layer->ctx, state_tracker, layer, &cmd->batch_cfg);
        GLDEBUG(glDrawArrays(GL_TRIANGLES, cmd->start, cmd->count));
    }
}


/////////////////////////////////////////////////////////////////////////////
// Target
/////////////////////////////////////////////////////////////////////////////

static
struct lib2d_r_target*
target_new(struct lib2d_r_ctx* ctx) {
    struct lib2d_r_target* t = i_calloc(1, sizeof(*t));
    t->ctx = ctx;
    return t;
}

static
void
target_set_viewport(struct lib2d_r_target* t, int w, int h) {
    t->viewport[0] = w;
    t->viewport[1] = h;
}

static
void
target_reset_layers(struct lib2d_r_target* t) {
    sbresize(t->layers, 0);
}

static
void
target_add_layer(struct lib2d_r_target* t, struct lib2d_r_layer* l) {
    sbpush(t->layers, l);
}

static
void
target_render(struct lib2d_r_target* t) {
    render_start(t->viewport[0], t->viewport[1]);
    struct state_tracker tracker;
    state_tracker_start(&tracker, t);
    sbforeachv(struct lib2d_r_layer* l, t->layers) {
        render_layer(l, &tracker);
    }
    state_tracker_end(&tracker);
}


/////////////////////////////////////////////////////////////////////////////
// Layer
/////////////////////////////////////////////////////////////////////////////

static
struct lib2d_r_layer*
layer_new(struct lib2d_r_ctx* ctx) {
    struct lib2d_r_layer* l = i_calloc(1, sizeof(*l));
    l->ctx = ctx;
    sv_init(l->draw_cmds);
    return l;
}

static
void
layer_delete(struct lib2d_r_layer* l) {
    sv_free(l->draw_cmds);
    i_free(l);
}

static
struct lib2d_r_vertex*
layer_map_verticies(struct lib2d_r_layer* layer, int count) {
#ifndef GLES
    if (layer->ctx->FEATURE_MAP) {
        if (!layer->vbo) GLDEBUG(glGenBuffers(1, &layer->vbo));
        GLDEBUG(glBindBuffer(GL_ARRAY_BUFFER, layer->vbo));
        if (count > layer->vbo_count) {
            GLDEBUG(glBufferData(GL_ARRAY_BUFFER, sizeof(struct lib2d_r_vertex)*count, NULL, GL_STATIC_DRAW));
            layer->vbo_count = count;
        }
        return (struct lib2d_r_vertex*) GLDEBUG(glMapBuffer(GL_ARRAY_BUFFER, GL_WRITE_ONLY));
    } else
#endif
    {
        sbresize(layer->ctx->VERT_POOL, count);
        return layer->ctx->VERT_POOL;
    }
}

static
void
layer_unmap_verticies(struct lib2d_r_layer* layer) {
#ifndef GLES
    if (layer->ctx->FEATURE_MAP) {
        GLDEBUG(glBindBuffer(GL_ARRAY_BUFFER, layer->vbo));
        GLDEBUG(glUnmapBuffer(GL_ARRAY_BUFFER));
    } else
#endif
    {
        if (!layer->vbo) {
            GLDEBUG(glGenBuffers(1, &layer->vbo));
        }
        GLDEBUG(glBindBuffer(GL_ARRAY_BUFFER, layer->vbo));
        GLDEBUG(glBufferData(GL_ARRAY_BUFFER, sizeof(*layer->ctx->VERT_POOL)*sbcount(layer->ctx->VERT_POOL), layer->ctx->VERT_POOL, GL_STATIC_DRAW));
    }
}

static
struct lib2d_r_draw_cmd*
layer_map_draw_cmds(struct lib2d_r_layer* layer, int count) {
    sv_resize(layer->draw_cmds, count);
    return sv_array(layer->draw_cmds);
}

static
void
layer_unmap_draw_cmds(struct lib2d_r_layer* layer) {
}



/////////////////////////////////////////////////////////////////////////////
// Texture
/////////////////////////////////////////////////////////////////////////////

static
void
texture_init(struct lib2d_texture* tex) {
    tex->r = i_malloc(sizeof(*tex->r));
    tex->r->handle = 0;
    tex->r->texture_type = GL_TEXTURE_2D;
}

static
void
texture_deinit(struct lib2d_r_ctx* ctx, struct lib2d_texture* tex) {
    if (tex->r->handle) {
        if (THREAD_ID_EQUAL(ctx->gl_thread_id, THREAD_CURRENT_ID())) {
            GLDEBUG(glDeleteTextures(1, &tex->r->handle));
        }
    }
    i_free(tex->r);
    tex->r = 0;
}

static
void
texture_data(struct lib2d_r_texture_data_info* u) {
    GLuint type = u->texture->r->texture_type;
    if (u->texture->r->handle == 0) {
        GLDEBUG(glGenTextures(1, &u->texture->r->handle));
    }
    GLDEBUG(glBindTexture(type, u->texture->r->handle));
    GLDEBUG(glTexParameteri(type, GL_TEXTURE_MIN_FILTER, GL_LINEAR));
    GLDEBUG(glTexParameteri(type, GL_TEXTURE_MAG_FILTER, GL_LINEAR));

    GLenum glformat = GL_RGBA;
    GLenum gltype = GL_UNSIGNED_BYTE;

    switch (u->format) {
    case LIB2D_IMAGE_FORMAT_RGBA_8888:
        glformat = GL_RGBA;
        gltype = GL_UNSIGNED_BYTE;
        break;
    case LIB2D_IMAGE_FORMAT_RGB_888:
        glformat = GL_RGB;
        gltype = GL_UNSIGNED_BYTE;
        break;
    case LIB2D_IMAGE_FORMAT_RGB_565:
        glformat = GL_RGB;
        gltype = GL_UNSIGNED_SHORT_5_6_5;
        break;
    case LIB2D_IMAGE_FORMAT_A_8:
#ifdef GLES
        glformat = GL_ALPHA;
#else
        glformat = GL_RED;
#endif
        gltype = GL_UNSIGNED_BYTE;
        break;
    default:
        assert(false);
    }

    GLDEBUG(glPixelStorei(GL_UNPACK_ALIGNMENT, 1));
    GLDEBUG(glTexImage2D(type, 0, glformat, u->width, u->height, 0, glformat, gltype, u->data));
}


/////////////////////////////////////////////////////////////////////////////
// Register
/////////////////////////////////////////////////////////////////////////////

void
r_register_gl(struct lib2d_render_interface* r) {
    r->init = init;
    r->shutdown = shutdown;
    r->clear = clear;

    r->target_new = target_new;
    r->target_set_viewport = target_set_viewport;
    r->target_render = target_render;
    r->target_reset_layers = target_reset_layers;
    r->target_add_layer = target_add_layer;

    r->layer_new = layer_new;
    r->layer_delete = layer_delete;
    r->layer_map_verticies = layer_map_verticies;
    r->layer_unmap_verticies = layer_unmap_verticies;
    r->layer_map_draw_cmds = layer_map_draw_cmds;
    r->layer_unmap_draw_cmds = layer_unmap_draw_cmds;

    r->texture_init = texture_init;
    r->texture_deinit = texture_deinit;
    r->texture_data = texture_data;
}
