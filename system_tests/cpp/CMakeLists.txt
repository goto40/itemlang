cmake_minimum_required(VERSION 3.0)

project(ItemLangCppTest)

set(TSTNAME Tester.exe)
set(ALGOSLIB Algos.lib)

set(SRCGEN src-gen)
set(TSTSRC tests)
set(ALGOSSRC src)


# set compiler flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED on)

# add catch include (https://github.com/catchorg/Catch2)
include_directories(catch/single_include)
include_directories(GSL/include)
include_directories(src)

# add include_directories
include_directories(${SRCGEN})

# get all source files
file(GLOB_RECURSE TSTFILES "${TSTSRC}/*.cpp")
file(GLOB_RECURSE ALGOSFILES "${ALGOSSRC}/*.cpp")

#define lib
add_library(${ALGOSLIB} STATIC ${ALGOSFILES})
# define tester
add_executable(${TSTNAME} ${TSTFILES})
target_link_libraries(${TSTNAME} ${ALGOSLIB})
###set_target_properties(${TSTNAME} PROPERTIES COMPILE_FLAGS "-coverage -g -O0") # gcc

add_custom_target(
    item_code
    COMMAND itemc ../model/items/*.item --generate-cpp
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
)
add_dependencies(${TSTNAME} item_code)
