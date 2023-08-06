
include_directories(${COCONET_PATH_INCLUDE})

add_executable(example_tensor main.cpp)

target_link_libraries(example_tensor coconet-cppbind)