set(target client)

file(GLOB_RECURSE sources ${CMAKE_CURRENT_SOURCE_DIR}/*.cc)

add_executable(${target} ${sources})

target_link_libraries(${target} PRIVATE tcp)