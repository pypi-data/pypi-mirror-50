SET(LIB_NAME tensor)
SET(LIB_OUTNAME coconet-${LIB_NAME})

SET(HEADER_PATH ${COCONET_PATH_HEADER}/${LIB_NAME})
SET(SOURCE_PATH ${COCONET_PATH_SOURCE}/${LIB_NAME})

SET(TENSOR_LIST
	${HEADER_PATH}/tensor.h
	${SOURCE_PATH}/tensor.cpp
	${HEADER_PATH}/index.h
	${SOURCE_PATH}/index.cpp
	${HEADER_PATH}/allocator.h
	${SOURCE_PATH}/allocator.cpp
	${HEADER_PATH}/storage.h
	${SOURCE_PATH}/storage.cpp
)

ADD_LIBRARY(${LIB_OUTNAME} ${TENSOR_LIST})
