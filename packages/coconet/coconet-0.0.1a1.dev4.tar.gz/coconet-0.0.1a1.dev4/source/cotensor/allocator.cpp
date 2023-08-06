#include <coconet/cotensor/allocator.h>

#include <cstdlib>

namespace coconet
{
	namespace cotensor
	{
		char * CoTensorAllocator::allocate(idx_type size)
		{
			if (size > 0)
				return (char *)malloc(size);
			else
				return nullptr;
		}

		void CoTensorAllocator::deallocate(char * ptr)
		{
			free(ptr);
		}
	}
}


