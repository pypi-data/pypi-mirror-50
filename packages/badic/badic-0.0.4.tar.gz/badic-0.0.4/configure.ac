dnl                                               -*- Autoconf -*-
dnl Process this file with autoconf to produce a configure script.

dnl Not sure which autoconf version we need, but 2.68 (from 2010)
dnl is widely available.
AC_PREREQ([2.68])

AC_INIT([badic], VERSION, [https://gitlab.com/mercatp/badic])
AC_COPYRIGHT([GNU Lesser General Public License version 2 or later])
AC_CONFIG_FILES([config.json])

dnl Check SDL2 presence
AC_CHECK_HEADER([SDL2/SDL.h],
             [AC_SUBST(HAVE_SDL2, true)],
             [AC_SUBST(HAVE_SDL2, false)])
AC_OUTPUT
