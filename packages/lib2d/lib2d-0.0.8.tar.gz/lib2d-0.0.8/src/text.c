/*
 * Copyright (C) 2019  Joseph Marshall
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
#include "stb_truetype.h"
#include "stretchy_buffer.h"
#include "error.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define TTF_BUFFER_SIZE (1<<25)

#define IS_WS(c) ((c) == ' ' || (c) == '\n')
#define U8_NEXT(s, i, length, c) { \
    (c)=(uint8_t)(s)[(i)++]; \
    if((c)>=0x80) { \
        uint8_t __t1, __t2; \
        if( /* handle U+1000..U+CFFF inline */ \
            (0xe0<(c) && (c)<=0xec) && \
            (((i)+1)<(length) || (length)<0) && \
            (__t1=(uint8_t)((s)[i]-0x80))<=0x3f && \
            (__t2=(uint8_t)((s)[(i)+1]-0x80))<= 0x3f \
        ) { \
            /* no need for (c&0xf) because the upper bits are truncated after <<12 in the cast to (UChar) */ \
            (c)=(unsigned char)(((c)<<12)|(__t1<<6)|__t2); \
            (i)+=2; \
        } else if( /* handle U+0080..U+07FF inline */ \
            ((c)<0xe0 && (c)>=0xc2) && \
            ((i)!=(length)) && \
            (__t1=(uint8_t)((s)[i]-0x80))<=0x3f \
        ) { \
            (c)=(((c)&0x1f)<<6)|__t1; \
            ++(i); \
        } else { \
            /* Skip "complicated" and error cases */ \
            ++(i); \
        } \
    } \
}

typedef struct f_glyph {
    int codepoint;
    lib2d_image im;
    int w, h, xoff, yoff;
} f_glyph;

typedef struct f_glyph_set {
    float font_size;
    f_glyph* glyphs; // stretchy_buffer
} f_glyph_set;

// lib2d_font.internal 
typedef struct f_internal {
    unsigned char ttf_buffer[TTF_BUFFER_SIZE];
    stbtt_fontinfo font;
    f_glyph_set* glyph_sets; // stretchy_buffer
} f_internal;

LIB2D_EXPORT
int lib2d_font_load(const char* path, lib2d_font* font) {
    font->internal = calloc(1, sizeof(f_internal));
    f_internal* f = (f_internal*) font->internal;
    FILE* fp = fopen(path, "rb");
    if (fp == NULL) {
        i_error("Failed to open font file at \"%s\"", path);
        return -1;
    }
    if (fread(f->ttf_buffer, 1, TTF_BUFFER_SIZE, fp) == 0) {
        if (ferror(fp)) {
            i_error("Failed to read font file at \"%s\"", path);
            fclose(fp);
            return -1;
        }
    }
    if (stbtt_InitFont(&f->font, f->ttf_buffer,
            stbtt_GetFontOffsetForIndex(f->ttf_buffer,0)) == 0) {
        i_error("Failed to load font at \"%s\"", path);
        fclose(fp);
        return -1;
    }
    fclose(fp);
    return 0;
}

LIB2D_EXPORT
void lib2d_font_delete(lib2d_font font) {
    f_internal* f = (f_internal*) font.internal;
    sbforeachp(f_glyph_set* gs, f->glyph_sets) {
        sbforeachp(f_glyph* g, gs->glyphs) {
            lib2d_image_delete(g->im);
        }
        sbfree(gs->glyphs);
    }
    sbfree(f->glyph_sets);
    free(font.internal);
    font.internal = 0;
}

static
f_glyph* f_get_or_create_glyph(f_internal* f, float font_size, int codepoint) {
    f_glyph_set* gs = 0;
    sbforeachp(f_glyph_set* check, f->glyph_sets) {
        if (check->font_size == font_size) {
            gs = check;
            break;
        }
    }
    if (gs == 0) {
        gs = sbadd(f->glyph_sets, 1);
        gs->font_size = font_size;
        gs->glyphs = 0;
    }
    sbforeachp(f_glyph* g, gs->glyphs) {
        if (g->codepoint == codepoint) {
            return g;
        }
    }
    f_glyph* g = sbadd(gs->glyphs, 1);
    g->codepoint = codepoint;
    unsigned char* bitmap = stbtt_GetCodepointBitmap(&f->font, 0,
            font_size, codepoint,
            &g->w, &g->h, &g->xoff, &g->yoff);
    lib2d_image_load_buffer(bitmap, &g->im, g->w, g->h, 1);
    return g;
}

LIB2D_EXPORT
void lib2d_text(const lib2d_font font, float font_size,
        const char* text, int x, int y, uint32_t color) {
    if (!text) return;
    f_internal* f = (f_internal*) font.internal;

    int t_len = strlen(text);
    if (t_len == 0) return;
    int i = 0;
    uint32_t codepoint = 0, last_codepoint = 0;
    float scale = stbtt_ScaleForPixelHeight(&f->font, font_size);
    while (i < t_len) {
        if (i) {
            x += scale*stbtt_GetCodepointKernAdvance(&f->font, codepoint, last_codepoint);
        }
        int cluster = i;
        U8_NEXT(text, i, t_len, codepoint);

        f_glyph* g = f_get_or_create_glyph(f, scale, codepoint);

        int advance, lsb;
        stbtt_GetCodepointHMetrics(&f->font, codepoint, &advance, &lsb);

        if (!IS_WS(text[cluster])) {
            lib2d_drawable d = {
                .x = x + g->xoff,
                .y = y + g->yoff,
                .w = g->w,
                .h = g->h,
                .image = g->im,
                .color = color
            };
            lib2d_draw(&d);
        }

        x += advance * scale;
        last_codepoint = codepoint;
    }
}

