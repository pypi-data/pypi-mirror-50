#ifndef COCONET_CORE_PLATFORM_H_
#define COCONET_CORE_PLATFORM_H_

#if defined(_MSC_VER) || defined (_WIN32) || defined(_WIN64)
#	include <windows.h>

#	ifndef COCONET_PLATFORM_WINDOWS
#		define COCONET_PLATFORM_WINDOWS 1
#	endif

#	if defined(_WIN64) || defined(_M_X64) || defined(_M_AMD64)
#		define COCONET_PLATFORM_WIN64 1
#	elif defined(_WIN32) || defined(_M_IX86)
#		define COCONET_PLATFORM_WIN32 1
#	endif

#	undef EXPORT
#	undef CALL

#	undef min
#	undef max

#	undef RGB
#	undef RGBA

#	undef DELETE

#	if defined(COCONET_BUILD_DLL_EXPORT)
#		define COCONET_EXPORT __declspec(dllexport)
#		define COCONET_EXPORT_WINONLY __declspec(dllexport)
#	else
#		if defined(COCONET_STATIC)
#			define COCONET_EXPORT
#			define COCONET_EXPORT_WINONLY
#		else
#			define COCONET_EXPORT __declspec(dllimport)
#			define COCONET_EXPORT_WINONLY __declspec(dllimport)
#		endif
#	endif

#	define COCONET_CALL __stdcall
#	define COCONET_INLINE __forceinline
#	define COCONET_WONT_RETURN __declspec(noreturn)
#else
#	define COCONET_EXPORT __attribute__ ((visibility("default")))
#	define COCONET_EXPORT_WINONLY
#
#	define COCONET_CALL
#	define COCONET_INLINE inline
#	define COCONET_WONT_RETURN
#endif

#if defined(__MINGW64__) || defined(__MINGW32__)
#	define COCONET_PLATFORM_GNUWIN 1
#endif

#if defined(_AIX)
#	ifndef COCONET_PLATFORM_ATX
#		define COCONET_PLATFORM_ATX 1
#	endif
#endif

#if defined(__BEOS__)
#	define COCONET_PLATFORM_BEOS 1
#endif

#if defined(__HAIKU__)
#	define COCONET_PLATFORM_HAIKU 1
#endif

#if defined(bsdi) || defined(__bsdi) || defined(__bsdi__)
#	ifndef COCONET_PLATFORM_BSDI
#		define COCONET_PLATFORM_BSDI	1
#	endif
#endif

#if defined(_arch_dreamcast)
#	ifndef COCONET_PLATFORM_DREAMCAST
#		define COCONET_PLATFORM_DREAMCAST 1
#	endif
#endif

#if defined(SDL2) || defined(__SDL2) || defined(__SDL2__)
#	ifndef COCONET_PLATFORM_SDL2
#		define COCONET_PLATFORM_SDL2	1
#	endif
#endif

#if defined(__FreeBSD__) || defined(__FreeBSD_kernel__) || defined(__DragonFly__)
#	ifndef COCONET_PLATFORM_FREEBSD
#		define COCONET_PLATFORM_FREEBSD 1
#	endif
#endif

#if defined(hpux) || defined(__hpux) || defined(__hpux__)
#	ifndef COCONET_PLATFORM_HPUX
#		define COCONET_PLATFORM_HPUX 1
#	endif
#endif

#if defined(sgi) || defined(__sgi) || defined(__sgi__) || defined(_SGI_SOURCE)
#	ifndef COCONET_PLATFORM_IRIX
#		define COCONET_PLATFORM_IRIX 1
#	endif
#endif

#if defined(linux) || defined(__linux) || defined(__linux__) || defined(__gnu_linux__)
#	ifndef COCONET_PLATFORM_LINUX
#		define COCONET_PLATFORM_LINUX	1
#	endif

#	ifndef COCONET_PLATFORM_X11
#		define COCONET_PLATFORM_X11	1
#	endif
#endif

#if defined(APPLE) || defined(__APPLE) || defined(__APPLE__)
#	ifndef COCONET_PLATFORM_APPLE
#		define COCONET_PLATFORM_APPLE	1
#	endif
#endif

#if defined(__clang__)
#	ifndef COCONET_PLATFORM_CLANG
#		define COCONET_PLATFORM_CLANG 1
#	endif
#endif

#if defined(__llvm__)
#	ifndef COCONET_PLATFORM_LLVM
#		define COCONET_PLATFORM_LLVM  1
#	endif
#endif

#if defined(_M_IX86) || defined(_M_X64) || defined(i386) || defined(__i386) || defined(__i386__)
#	ifndef COCONET_PLATFORM_INTEL
#		define COCONET_PLATFORM_INTEL 1
#	endif
#endif

#if defined(__GO32__) || defined(__DJGPP__) || defined(__DOS__)
#	ifndef COCONET_PLATFORM_DOS
#		define COCONET_PLATFORM_DOS 1
#	endif
#endif

#if !defined(__UNIX__) && defined(__UNIX_LIKE__)
#		define COCONET_PLATFORM_UNIX 1
#endif

#if defined(__LP64__) || defined(__amd64__) || defined(__x86_64__) || defined(_M_X64)
#	ifndef COCONET_PLATFORM_64BIT_PTR
#		define COCONET_PLATFORM_64BIT_PTR
#	endif
#endif

#if defined(COCONET_PLATFORM_INTEL) && defined(_M_AMD64)
#	define COCONET_PLATFORM_SSE 1
#	define COCONET_PLATFORM_SSE2 1

#	if !defined(__SSE3__)  && defined(__SSE2__)
#		ifndef COCONET_PLATFORM_SSE3
#			define COCONET_PLATFORM_SSE3 1
#		endif
#	endif

#	if !defined(__SSE4__)  && defined(__SSE3__)
#		ifndef COCONET_PLATFORM_SSE4
#			define COCONET_PLATFORM_SSE4 1
#		endif
#	endif

#	if !defined(__AVX__)  && defined(__SSE__)
#		ifndef COCONET_PLATFORM_AVX
#			define COCONET_PLATFORM_AVX 1
#		endif
#	endif

#	if !defined(__AVX2__)  && defined(__AVX__)
#		ifndef COCONET_PLATFORM_AVX2
#			define COCONET_PLATFORM_AVX2 1
#		endif
#	endif

#endif

#if defined(COCONET_PLATFORM_INTEL) && defined(_M_IX86_FP)
#	if _M_IX86_FP > 0
#		ifndef COCONET_PLATFORM_SSE
#			define COCONET_PLATFORM_SSE 1
#		endif
#	endif

#	if _M_IX86_FP > 1
#		ifndef COCONET_PLATFORM_SSE2
#			define COCONET_PLATFORM_SSE2 1
#		endif
#	endif

#	if !defined(__SSE3__)  && defined(__SSE2__)
#		ifndef COCONET_PLATFORM_SSE3
#			define COCONET_PLATFORM_SSE3 1
#		endif
#	endif

#	if !defined(__SSE4__)  && defined(__SSE3__)
#		ifndef COCONET_PLATFORM_SSE4
#			define COCONET_PLATFORM_SSE4 1
#		endif
#	endif

#	if !defined(__AVX__)  && defined(__SSE__)
#		ifndef COCONET_PLATFORM_AVX
#			define COCONET_PLATFORM_AVX 1
#		endif
#	endif

#	if !defined(__AVX2__)  && defined(__AVX__)
#		ifndef COCONET_PLATFORM_AVX2
#			define COCONET_PLATFORM_AVX2 1
#		endif
#	endif
#endif

#if defined(ANDROID)
#	ifndef COCONET_PLATFORM_ANDROID
#		define COCONET_PLATFORM_ANDROID 1
#	endif
#endif

#if defined(_DEBUG) || defined(DEBUG)
#	ifndef COCONET_PLATFORM_DEBUG
#		define COCONET_PLATFORM_DEBUG 1
#	endif
#else
#	ifndef COCONET_PLATFORM_RELEASE
#		define COCONET_PLATFORM_RELEASE 1
#	endif
#endif

#if defined(_UNICODE) || defined(UNICODE)
#	ifndef COCONET_PLATFORM_UNICODE
#		define COCONET_PLATFORM_UNICODE 1
#	endif
#endif

#if defined(__UNIX__) || defined(__LINUX__) && !defined(__CLANG__)
#	define final
#endif

#if defined(__DEBUG__) && defined(_VISUAL_STUDIO_) && defined(_CRTDBG_MAP_ALLOC)
#	define __MEM_LEAK__  1
#	include <crtdbg.h>
#	define new new(_CLIENT_BLOCK, __FILE__, __LINE__)
#endif

#endif