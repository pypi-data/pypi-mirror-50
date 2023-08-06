
include_directories(${COCONET_PATH_INCLUDE})

add_executable(example_variable main.cpp)

target_link_libraries(example_variable coconet-cppbind)