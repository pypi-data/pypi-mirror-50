include_directories(${COCONET_PATH_CONTRIB}/catch2/single_include)

include_directories(${COCONET_PATH_INCLUDE})

add_executable(test main.cpp)

target_link_libraries(test coconet-cppbind)