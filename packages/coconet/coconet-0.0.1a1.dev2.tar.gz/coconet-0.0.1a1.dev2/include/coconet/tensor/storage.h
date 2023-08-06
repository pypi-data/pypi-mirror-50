#ifndef COCONET_TENSOR_STORAGE_H_
#define COCONET_TENSOR_STORAGE_H_

#include <memory>
#include <coconet/core/type.h>
#include <coconet/tensor/allocator.h>

namespace coconet
{
	namespace tensor
	{
		class Storage
		{
		public:

			// convert
			virtual void to_byte() = 0;
			virtual void to_char() = 0;
			virtual void to_short() = 0;
			virtual void to_int() = 0;
			virtual void to_long() = 0;
			virtual void to_float() = 0;
			virtual void to_double() = 0;
			// info
			virtual char* data_ptr() = 0;
			virtual const char* data_ptr() const = 0;
			virtual DataType dtype() const = 0;
			virtual PlatformType platform() const = 0;
			virtual idx_type size() const = 0;
			virtual std::int32_t element_size() const = 0;
			virtual idx_type numel() const = 0;

			// manipulate
			virtual void resize_(idx_type n) = 0;
		};
	}
}

#endif //! COCONET_TENSOR_STORAGE_H_