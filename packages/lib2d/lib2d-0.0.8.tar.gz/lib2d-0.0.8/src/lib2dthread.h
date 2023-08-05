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

#ifdef _WIN32
#include <windows.h>
#define THREAD HANDLE
#define THREAD_JOIN(t) WaitForSingleObject((t), INFINITE) 
// TODO implement naming the thread on windows
#define THREAD_CREATE(t, name, func, data) ((t) = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE) func, data, 0, &unused_threadid))
#define THREAD_ID DWORD
#define THREAD_ID_EQUAL(a, b) (a == b)
#define THREAD_CURRENT_ID() GetCurrentThreadId()
static DWORD unused_threadid;
#else
#include <pthread.h>
#define THREAD pthread_t
#define THREAD_JOIN(t) pthread_join((t), 0)
#define THREAD_CREATE(t, name, func, data) pthread_create(&t, 0, func, data), pthread_setname_np(t, name)
#define THREAD_ID pthread_t
#define THREAD_ID_EQUAL(a, b) pthread_equal(a, b)
#define THREAD_CURRENT_ID() pthread_self()
#endif
