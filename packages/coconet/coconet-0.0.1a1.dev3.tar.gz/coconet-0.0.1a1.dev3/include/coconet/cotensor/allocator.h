#ifndef COCONET_COTENSOR_ALLOCATOR
#define COCONET_COTENSOR_ALLOCATOR

#include <coconet/tensor/allocator.h>

namespace coconet
{
	namespace cotensor
	{
		class CoTensorAllocator: public tensor::Allocator
		{
		public:
			virtual char* allocate(idx_type size) override;
			virtual void deallocate(char* ptr) override;
		private:

		};
	}
}

#endif // !COCONET_COTENSOR_ALLOCATOR
