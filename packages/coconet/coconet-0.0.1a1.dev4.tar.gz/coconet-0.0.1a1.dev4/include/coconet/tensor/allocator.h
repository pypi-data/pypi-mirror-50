#ifndef COCONET_TENSOR_ALLOCATOR_H_
#define COCONET_TENSOR_ALLOCATOR_H_

#include <coconet/core/type.h>

namespace coconet
{
	namespace tensor
	{
		class Buffer
		{
		public:
			Buffer()
				:buffer_ptr(nullptr), len(0) {}
			Buffer(char* ptr, idx_type l)
				:buffer_ptr(ptr), len(l) {}
		private:
			char* buffer_ptr;
			idx_type len;
		};

		class Allocator
		{
		public:
			virtual char* allocate(idx_type size) = 0;
			virtual void deallocate(char* ptr) = 0;
		private:

		};

		/*
		struct BufferDeleter
		{
		public:
			BufferDeleter(Allocator* alloc)
				:_alloc(alloc){}
			BufferDeleter(const BufferDeleter&) { }
			BufferDeleter(BufferDeleter&) { }
			BufferDeleter(BufferDeleter&&) { }
			void operator()(char* p) const {
				_alloc->deallocate(p);
			};
		private:
			Allocator* _alloc;
		};
		*/
	}
}

#endif //! COCONET_TENSOR_ALLOCATOR_H_