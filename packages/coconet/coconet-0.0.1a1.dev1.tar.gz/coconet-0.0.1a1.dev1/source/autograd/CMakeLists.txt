set(LIB_NAME autograd)
set(LIB_OUTNAME coconet-${LIB_NAME})

set(HEADER_PATH ${COCONET_PATH_HEADER}/${LIB_NAME})
set(SOURCE_PATH ${COCONET_PATH_SOURCE}/${LIB_NAME})

set(AUTOGRAD_LIST
    ${HEADER_PATH}/function.h
    ${SOURCE_PATH}/function.cpp
    ${HEADER_PATH}/variable.h
    ${SOURCE_PATH}/variable.cpp
    ${HEADER_PATH}/executor.h
    ${SOURCE_PATH}/executor.cpp
)

add_library(${LIB_OUTNAME} ${AUTOGRAD_LIST})
