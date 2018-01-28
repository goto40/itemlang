cmake_minimum_required(VERSION 3.0)

project(ItemLangCppTest)

set(TSTNAME Tester.exe)

set(SRCGEN src-gen)
set(TSTSRC tests)


# set compiler flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED on)

# add catch include (https://github.com/catchorg/Catch2)
include_directories(../catch/single_include)

# add include_directories
include_directories(${SRCGEN})

# get all source files
file(GLOB TSTFILES "${TSTSRC}/*.cpp")

# define tester
add_executable(${TSTNAME} ${TSTFILES})
#set_target_properties(${TSTNAME} PROPERTIES COMPILE_FLAGS "-coverage -g -O0") # gcc
#target_link_libraries(${TSTNAME} gcov) # gcc

add_custom_target(
    item_code
    COMMAND itemc items/*.item --generate-cpp
)
add_dependencies(${TSTNAME} item_code)
