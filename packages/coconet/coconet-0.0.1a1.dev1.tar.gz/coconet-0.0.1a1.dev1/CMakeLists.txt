cmake_minimum_required(VERSION 3.14)

project(coconet)


set(COCONET_PATH ${PROJECT_SOURCE_DIR} CACHE STRING "Adds a path to coconet" FORCE)
set(COCONET_PATH_INCLUDE ${COCONET_PATH}/include CACHE STRING "Adds a path to coconet header" FORCE)
set(COCONET_PATH_HEADER ${COCONET_PATH}/include/coconet CACHE STRING "Adds a path to coconet header" FORCE)
set(COCONET_PATH_SOURCE ${COCONET_PATH}/source CACHE STRING "Adds a path to coconet source" FORCE)
set(COCONET_PATH_CONTRIB ${COCONET_PATH}/contrib CACHE STRING "Adds a path to coconet contrib" FORCE)


set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


# options
option(COCONET_BUILD_TESTS "build tests" ON)
option(COCONET_BUILD_BENCHMARK "build benchmark" ON)

# option(COCONET_OPENMP "openmp support" OFF)

option(COCONET_FEATURE_SIMD "SIMD support" ON)
option(COCONET_FEATURE_MULTI_THREAD "multi thread support" ON)

option(COCONET_INTERFACE_PYTHON "python interface" ON)

if(COCONET_FEATURE_SIMD)
    add_compile_definitions(COCONET_FEATURE_SIMD)
endif()

if(COCONET_FEATURE_MULTI_THREAD)
    add_compile_definitions(COCONET_FEATURE_MULTI_THREAD)
endif()


# sub dir
add_subdirectory(contrib)
add_subdirectory(source)
add_subdirectory(examples)
if(COCONET_BUILD_TESTS)
    add_subdirectory(tests)
endif()