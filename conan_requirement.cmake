
include("${CMAKE_CURRENT_LIST_DIR}/conan_paths.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    link_libraries( ${CMAKE_DL_LIBS} )
endif()
