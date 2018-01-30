cmake_minimum_required(VERSION 3.0)

project(ItemLangCppTest)

set(TSTNAME Tester.exe)
set(ALGOSLIB Algos.lib)

# set compiler flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED on)

# -------------------------------------------------------------
set(SRCGEN src-gen)
add_custom_target(
    item_code
    COMMAND itemc ../model/items/*.item --generate-cpp --src-gen=${SRCGEN}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
)

# -------------------------------------------------------------
# add catch include (https://github.com/catchorg/Catch2)
include_directories(catch/single_include)
include_directories(GSL/include)
include_directories(src)

# add include_directories
include_directories(${SRCGEN})

# -------------------------------------------------------------
#define lib
set(ALGOSSRC src)
file(GLOB_RECURSE ALGOSFILES "${ALGOSSRC}/*.cpp")
add_library(${ALGOSLIB} STATIC ${ALGOSFILES})
add_dependencies(${ALGOSLIB} item_code)

# -------------------------------------------------------------
# define tester
set(TSTSRC tests)
file(GLOB_RECURSE TSTFILES "${TSTSRC}/*.cpp")
add_executable(${TSTNAME} ${TSTFILES})
target_link_libraries(${TSTNAME} ${ALGOSLIB})
###set_target_properties(${TSTNAME} PROPERTIES COMPILE_FLAGS "-coverage -g -O0") # gcc
add_dependencies(${TSTNAME} item_code)

