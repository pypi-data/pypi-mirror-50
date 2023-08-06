#ifndef COCONET_TENSOR_TENSOR_TENSOR_H_
#define COCONET_TENSOR_TENSOR_TENSOR_H_

#include <algorithm>
#include <stdexcept>

#include <coconet/core/type.h>
#include <coconet/tensor/index.h>

namespace coconet
{
    namespace tensor
	{
        class ITensor
        {
        public:
            // virtual char* data_ptr() = 0;
            // virtual const char* data_ptr() const = 0;
            /*virtual device_id device() = 0;
            virtual DataType dtype() const = 0;
            virtual bool equal(const ITensor& other) const = 0;

            virtual idx_type ndimension() const = 0;
            virtual idx_type offset() const = 0;
            virtual void permute_(const DimVector& dims) const = 0;
            virtual PlatformType platform() const = 0;
            virtual DimVector size() const = 0;
            virtual idx_type size(idx_type i) const = 0;
            virtual DimVector stride() const = 0;
            virtual idx_type stride(idx_type i) const = 0;
            virtual std::string to_string() const = 0;*/
        };

		inline bool broadcastable(const DimVector &lhs, const DimVector & rhs)
		{
			if (lhs.size() < 1 || rhs.size() < 1)
				return false;

			idx_type min = std::min(lhs.size(), rhs.size());
			for (idx_type i = min - 1; i >= 0; --i)
				if (lhs[i] != rhs[i] && lhs[i] != 1 && rhs[i] != 1)
					return false;

			return true;
		}

		inline DimVector broadcast_shape(const DimVector &lhs, const DimVector & rhs)
		{
			bool is_broadcastable = broadcastable(lhs, rhs);
			if (!is_broadcastable)
				throw std::runtime_error("The size of tensor a must match the size of tensor b");
			auto max_size = std::max(lhs.size(), rhs.size());
			DimVector result_dim(max_size);

			for (idx_type i = max_size - 1; i >= 0; --i)
			{
				idx_type lhs_size = i >= max_size - lhs.size() ? lhs[i] : 1;
				idx_type rhs_size = i >= max_size - rhs.size() ? rhs[i] : 1;
				result_dim[max_size + i] = std::max(lhs_size, rhs_size);
			}
			return result_dim;
		}
    }
}

#endif // !COCONET_CORE_TENSOR_H_
