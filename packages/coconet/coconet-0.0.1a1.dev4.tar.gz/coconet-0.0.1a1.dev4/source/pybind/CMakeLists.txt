set(LIB_NAME pybind)
set(LIB_OUTNAME coconet-${LIB_NAME})
set(LIB_PYTHONNAME coconet)

set(HEADER_PATH ${COCONET_PATH_HEADER}/${LIB_NAME})
set(SOURCE_PATH ${COCONET_PATH_SOURCE}/${LIB_NAME})

set(PYBIND_LIST
    ${HEADER_PATH}/coconet.h
    ${SOURCE_PATH}/coconet.cpp
)

# add_library(${LIB_OUTNAME} SHARED ${CORE_LIST})

pybind11_add_module(${LIB_PYTHONNAME} ${PYBIND_LIST})

target_link_libraries(${LIB_PYTHONNAME} PRIVATE coconet-core)
target_link_libraries(${LIB_PYTHONNAME} PRIVATE coconet-util)
target_link_libraries(${LIB_PYTHONNAME} PRIVATE coconet-tensor)
target_link_libraries(${LIB_PYTHONNAME} PRIVATE coconet-cotensor)
target_link_libraries(${LIB_PYTHONNAME} PRIVATE coconet-autograd)
target_link_libraries(${LIB_PYTHONNAME} PRIVATE coconet-nn)

# include_directories(${PYTHON_INCLUDE_DIRS})
# target_link_libraries(${LIB_OUTNAME}  ${PYTHON_LIBRARIES})
# target_link_libraries(${LIB_OUTNAME} pybind11)
