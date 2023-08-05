#ifndef STRETCHY_BUFFER_H
#define STRETCHY_BUFFER_H

#include <assert.h>
#include <string.h> // for memmove
#include "alloc.h"

// stretchy buffer // init: NULL // free: sbfree() // push_back: sbpush() // size: sbcount() //
#define sbfree(a)         ((a) ? i_free(stb__sbraw(a)),0 : 0)
#define sbpush(a,v)       (stb__sbmaybegrow(a,1), (a)[stb__sbn(a)++] = (v))
#define sbcount(a)        ((a) ? stb__sbn(a) : 0)
#define sbadd(a,n)        (stb__sbmaybegrow(a,n), stb__sbn(a)+=(n), &(a)[stb__sbn(a)-(n)])
#define sblast(a)         ((a)[stb__sbn(a)-1])
#define sbremove(a,i,n)   (memmove((a)+(i), (a)+(i)+(n), (stb__sbn(a)-((i)+(n)))*sizeof(*(a))), stb__sbn(a)-=(n))
#define sbinsert(a,i,n)   (stb__sbmaybegrow(a,n), stb__sbn(a)+=(n), memmove((a)+(i)+(n), (a)+(i), (stb__sbn(a)-(i))*sizeof(*(a))), &(a)[(i)])
#define sbremovelast(a)   sbremove(a, stb__sbn(a)-1, 1)
#define sbconcat(a, b) (memcpy(sbadd((a), sbcount(b)), (b), sbcount(b)*sizeof(*(b))))
#define sbempty(a) ((a) ? stb__sbn(a)=0 : 0)
#define sbresize(a,n)     (stb__sbmaybegrow(a,n), ((a) ? (stb__sbn(a)=(n)) : 0))
#define sbsort(a, f)      stb__sbsort((a), sbcount(a), sizeof(*(a)), f)

// foreach, with a pointer into the array
#define sbforeachp(v, a) \
    for (int stb__counter=0, stb__loop_break_outer=false; \
            stb__counter<sbcount((a)) /* counter */ \
            && !stb__loop_break_outer /* only continue if the inner loop didn't hit a break statement */ \
            && (stb__loop_break_outer = true); /* set the variable so we can track if the inner loop completed without a break */ \
            stb__counter++) \
        for (v = &(a)[stb__counter]; /* inner loop is executed once, so that we can initialize a variable */ \
                stb__loop_break_outer;\
                stb__loop_break_outer = false /* signal that we've finished an iteration without breaking */)
// foreach, copying the values of the array
#define sbforeachv(v, a) \
    for (int stb__counter=0, stb__loop_break_outer=false; \
            stb__counter<sbcount((a)) /* counter */ \
            && !stb__loop_break_outer /* only continue if the inner loop didn't hit a break statement */ \
            && (stb__loop_break_outer = true); /* set the variable so we can track if the inner loop completed without a break */ \
            stb__counter++) \
        for (v = (a)[stb__counter]; /* inner loop is executed once, so that we can initialize a variable */ \
                stb__loop_break_outer;\
                stb__loop_break_outer = false /* signal that we've finished an iteration without breaking */)

#include <stdlib.h>
#define stb__sbraw(a) ((int *) (a) - 2)
#define stb__sbm(a)   stb__sbraw(a)[0]
#define stb__sbn(a)   stb__sbraw(a)[1]

#define stb__sbneedgrow(a,n)  ((a)==0 || stb__sbn(a)+n >= stb__sbm(a))
#define stb__sbmaybegrow(a,n) (stb__sbneedgrow(a,(n)) ? stb__sbgrow(a,n) : (void)0)
#define stb__sbgrow(a,n)  stb__sbgrowf((void **) &(a), (n), sizeof(*(a)))

#ifndef _MSC_VER
__attribute__ ((unused))
#endif
static void stb__sbgrowf(void **arr, int increment, int itemsize)
{
   int m = *arr ? 2*stb__sbm(*arr)+increment : increment+1;
   void *p = i_realloc(*arr ? stb__sbraw(*arr) : 0, itemsize * m + sizeof(int)*2);
   assert(p);
   if (p) {
      if (!*arr) ((int *) p)[1] = 0;
      *arr = (void *) ((int *) p + 2);
      stb__sbm(*arr) = m;
   }
}

#ifndef _MSC_VER
__attribute__ ((unused))
#endif
static void stb__sbsort(void *base, size_t nmemb, size_t size, int(*compar)(const void*, const void*)) {
    // qsort doesn't always behave well with a null base, even if nmemb is 0.
    if (base) {
        qsort(base, nmemb, size, compar);
    }
}

#endif
