################################################################################
##                                                                            ##
## Copyright (C) 2021-2022 Crypto Lab Inc.                                    ##
##                                                                            ##
## - This file is part of HEaaN homomorphic encryption library.               ##
## - HEaaN cannot be copied and/or distributed without the express permission ##
##  of Crypto Lab Inc.                                                        ##
##                                                                            ##
################################################################################

cmake_minimum_required(VERSION 3.13)
project(HEaaN_examples LANGUAGES CXX)

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp")

find_package(HEaaN REQUIRED)

# The executables read image/ and kernel/ from this directory.
add_executable(20 ResNet20.cpp)
target_link_libraries(20 PUBLIC HEaaN::HEaaN)
target_compile_definitions(20 PRIVATE DATA_DIR="${PROJECT_SOURCE_DIR}")

add_executable(110 ResNet110.cpp)
target_link_libraries(110 PUBLIC HEaaN::HEaaN)
target_compile_definitions(110 PRIVATE DATA_DIR="${PROJECT_SOURCE_DIR}")
