#pragma once

#ifdef _WIN32
  #define libfoo_EXPORT __declspec(dllexport)
#else
  #define libfoo_EXPORT
#endif

libfoo_EXPORT void libfoo();
