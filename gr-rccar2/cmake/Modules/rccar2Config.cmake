INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_RCCAR2 rccar2)

FIND_PATH(
    RCCAR2_INCLUDE_DIRS
    NAMES rccar2/api.h
    HINTS $ENV{RCCAR2_DIR}/include
        ${PC_RCCAR2_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    RCCAR2_LIBRARIES
    NAMES gnuradio-rccar2
    HINTS $ENV{RCCAR2_DIR}/lib
        ${PC_RCCAR2_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(RCCAR2 DEFAULT_MSG RCCAR2_LIBRARIES RCCAR2_INCLUDE_DIRS)
MARK_AS_ADVANCED(RCCAR2_LIBRARIES RCCAR2_INCLUDE_DIRS)

