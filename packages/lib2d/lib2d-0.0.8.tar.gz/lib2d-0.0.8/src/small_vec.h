/*
 * Copyright (C) 2018  Matthew Marshall, Joseph Marshall
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

#ifndef SMALL_VEC_H
#define SMALL_VEC_H

#include <stdint.h>
#include <string.h> // for memcpy, memmove
#include <stdlib.h>
#include <stdbool.h>
#include "alloc.h"

typedef struct {
    uint32_t on_heap :1;
    uint32_t count :31;
} sv__count_and_heap_t;

#define small_vec(T, N) struct { \
    sv__count_and_heap_t sv_h; \
    union { \
        T stack[N]; \
        struct { \
            uint32_t allocated; \
            T* buffer; \
        } heap; \
    } u; \
}

// NOTE sv_add and sv_resize do not initialize new memory

#define sv_init(a)         (memset(&a, 0, sizeof(a)))
#define sv_reserve(a, n)   (sv__realloc(a, n))
#define sv_free(a)         ((a).sv_h.on_heap ? i_free(a.u.heap.buffer),0 : 0)
#define sv_add(a,n)        (sv__grow(a,n), sv_array(a)+sv_count(a)-(n))
#define sv_push(a,v)       (*sv_add(a, 1) = (v))
#define sv_pop(a)          (sv_resize(a, sv_count(a)-1), sv_array(a)[sv_count(a)])
#define sv_array(a)        ((a).sv_h.on_heap ? (a).u.heap.buffer : (a).u.stack)
#define sv_count(a)        ((a).sv_h.count)
// NOTE sv_pop expects sv_resize to leave memory valid while shrinking
#define sv_resize(a, n)    (((uint32_t)(n) > sv_count(a)) ? sv__grow(a, (n)-sv_count(a)) : (((a).sv_h.count = n), (void)0))
#define sv_last(a)         (sv_array(a)[sv_count(a)-1])
#define sv_remove(a,i,n)   (memmove(sv_array(a)+(i), sv_array(a)+(i)+(n), (sv_count(a)-((i)+(n)))*sizeof((a).u.stack[0])), sv_count(a)-=(n))
#define sv_sort(a, f)      (qsort(sv_array(a), sv_count(a), sizeof((a).u.stack[0]), f))

#define sv__stack_count(a) (sizeof(a.u.stack)/sizeof(a.u.stack[0]))
#define sv__grow(a, add)   (sv__realloc(a, sv_count(a)+(add)), (a).sv_h.count += (add), (void)0)
#define sv__realloc(a, needed) sv__reallocf(&(a).sv_h, (a).u.stack, &(a).u.heap.allocated, (void**)&(a).u.heap.buffer, needed, sizeof((a).u.stack[0]), sv__stack_count(a))

#define sv_foreach_p(v, a) \
    for (uint32_t stb__counter=0, stb__loop_break_outer=false; \
            stb__counter<sv_count((a)) /* counter */ \
            && !stb__loop_break_outer /* only continue if the inner loop didn't hit a break statement */ \
            && (stb__loop_break_outer = true); /* set the variable so we can track if the inner loop completed without a break */ \
            stb__counter++) \
        for (v = &sv_array(a)[stb__counter]; /* inner loop is executed once, so that we can initialize a variable */ \
                stb__loop_break_outer;\
                stb__loop_break_outer = false /* signal that we've finished an iteration without breaking */)

#define sv_foreach(v, a) \
    for (uint32_t stb__counter=0, stb__loop_break_outer=false; \
            stb__counter<sv_count((a)) /* counter */ \
            && !stb__loop_break_outer /* only continue if the inner loop didn't hit a break statement */ \
            && (stb__loop_break_outer = true); /* set the variable so we can track if the inner loop completed without a break */ \
            stb__counter++) \
        for (v = sv_array(a)[stb__counter]; /* inner loop is executed once, so that we can initialize a variable */ \
                stb__loop_break_outer;\
                stb__loop_break_outer = false /* signal that we've finished an iteration without breaking */)

#define sv_keep(a, v, f) \
    for (uint32_t sv__to=0, sv__from=0; sv__from<sv_count((a)); sv__from++) {\
        for (v = sv_array(a)[sv__from]; true; ) { /* inner loop is executed once, so that we can initialize a variable */ \
            if (f) {\
                if (sv__to != sv__from) { \
                    sv_array(a)[sv__to] = sv_array(a)[sv__from]; \
                }\
                sv__to++;\
            }\
            break;\
        }\
        if (sv__from == sv_count((a)) - 1) {\
            sv_resize((a), sv__to); \
        }\
    }\

#define sv_filter_append(a_from, a_to, v, f) \
    for (uint32_t sv__from=0; stb__from<sv_count((a)); sv__from++) {\
        for (v = sv_array(a_from)[sv__from]; true; ) { /* inner loop is executed once, so that we can initialize a variable */ \
            if (f) {\
                sv_push(a_to, sv_array(a_from)[sv__from]); \
            }\
            break;\
        }\
    }\

#ifndef _MSC_VER
__attribute__ ((unused))
#endif
static
void
sv__reallocf(sv__count_and_heap_t* h, void* stack, uint32_t* allocated, void** buffer, int needed, int item_size, int stack_count) {
    if (h->on_heap) {
        if ((uint32_t)needed > *allocated) {
            *allocated = needed;
            *buffer = i_realloc(*buffer, needed*item_size);
        }
    } else {
        if (needed > stack_count) {
            void* new_buffer = i_malloc(needed*item_size);
            memcpy(new_buffer, stack, stack_count*item_size);
            h->on_heap = true;
            *allocated = needed;
            *buffer = new_buffer;
        }
    }
}


#endif

