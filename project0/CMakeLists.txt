cmake_minimum_required(VERSION 3.8.2 FATAL_ERROR)

set(CMAKE_CXX_STANDARD 17)

project(project0)

include_directories(includes/)

add_subdirectory(sources)
add_subdirectory(client)
add_subdirectory(server)