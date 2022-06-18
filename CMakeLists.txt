cmake_minimum_required(VERSION 3.15)
project(libfoo CXX)

include(cmake/PreventInSourceBuilds.cmake)
find_package(armadillo REQUIRED)
find_package(date REQUIRED COMPONENTS date-tz)
set(EXTERNAL_LIBS
    armadillo::armadillo
    date::date-tz
    )

add_library(libfoo src/libfoo.cpp)
target_include_directories(libfoo PUBLIC include)

set_target_properties(libfoo PROPERTIES PUBLIC_HEADER "include/libfoo.h")
target_link_libraries(
  libfoo
  PUBLIC ${EXTERNAL_LIBS}
  )
install(TARGETS libfoo)
