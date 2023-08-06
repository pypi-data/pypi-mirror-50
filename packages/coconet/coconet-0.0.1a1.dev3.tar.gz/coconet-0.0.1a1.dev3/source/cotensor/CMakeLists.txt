SET(LIB_NAME cotensor)
SET(LIB_OUTNAME coconet-${LIB_NAME})

SET(HEADER_PATH ${COCONET_PATH_HEADER}/${LIB_NAME})
SET(SOURCE_PATH ${COCONET_PATH_SOURCE}/${LIB_NAME})

SET(TENSOR_LIST
    ${HEADER_PATH}/apply.h
    ${SOURCE_PATH}/apply.cpp
    ${HEADER_PATH}/tensor.h
    ${SOURCE_PATH}/tensor.cpp
    ${HEADER_PATH}/storage.h
    ${SOURCE_PATH}/storage.cpp
    ${HEADER_PATH}/math.h
    ${SOURCE_PATH}/math.cpp
    ${HEADER_PATH}/allocator.h
    ${SOURCE_PATH}/allocator.cpp
    ${HEADER_PATH}/blas.h
    ${SOURCE_PATH}/blas.cpp
    ${HEADER_PATH}/view.h
    ${SOURCE_PATH}/view.cpp
)

ADD_LIBRARY(${LIB_OUTNAME} ${TENSOR_LIST})

target_link_libraries(${LIB_OUTNAME} coconet-tensor)
target_link_libraries(${LIB_OUTNAME} coconet-util)

