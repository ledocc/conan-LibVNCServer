cmake_minimum_required(VERSION 3.15.3)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package( LibVNCServer REQUIRED COMPONENTS vncserver vncclient )

add_executable(example example.cpp)
target_link_libraries(example PUBLIC LibVNCServer::vncclient LibVNCServer::vncserver)

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
